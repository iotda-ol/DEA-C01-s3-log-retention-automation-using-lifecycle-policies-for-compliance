#!/usr/bin/env python3
"""Advanced example: Cost optimization analysis."""

from s3_log_retention.cost_analysis import CostAnalyzer

def analyze_bucket_costs(bucket_name: str):
    """Analyze costs for a bucket."""
    analyzer = CostAnalyzer(bucket_name)
    
    print(f"Analyzing costs for bucket: {bucket_name}\n")
    
    # Get current costs
    costs = analyzer.analyze_bucket_costs()
    
    print("Current Monthly Costs:")
    print("-" * 50)
    for storage_class, cost in costs.items():
        if storage_class != 'TOTAL':
            print(f"{storage_class:20s}: ${cost:>10.2f}")
    print("-" * 50)
    print(f"{'TOTAL':20s}: ${costs['TOTAL']:>10.2f}")
    
    # Estimate savings from lifecycle transitions
    print("\n\nEstimated Savings from Lifecycle Policies:")
    print("-" * 50)
    
    scenarios = [
        (30, 'STANDARD_IA'),
        (90, 'GLACIER'),
        (180, 'DEEP_ARCHIVE')
    ]
    
    for days, target_class in scenarios:
        savings = analyzer.estimate_savings(days, target_class)
        print(f"\nTransition to {target_class} after {days} days:")
        print(f"  Current Cost:   ${savings['current_cost']:.2f}/month")
        print(f"  Projected Cost: ${savings['projected_cost']:.2f}/month")
        print(f"  Monthly Savings: ${savings['monthly_savings']:.2f}")
        print(f"  Annual Savings:  ${savings['annual_savings']:.2f}")

def main():
    """Main function."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python cost_optimization.py <bucket-name>")
        sys.exit(1)
    
    bucket_name = sys.argv[1]
    analyze_bucket_costs(bucket_name)

if __name__ == '__main__':
    main()
