#!/usr/bin/env python3
"""
EDI Trainer - CLI Interface

Generate realistic EDI transactions with controllable error rates for learning.
"""

import argparse
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.segment_generators import generate_isa_iea_pair


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate EDI transactions with controllable error rates for learning",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 5 clean ISA/IEA pairs
  python edi_trainer.py --count=5 --error-rate=0.0
  
  # Generate 10 pairs with 20% error rate, no explanations
  python edi_trainer.py --count=10 --error-rate=0.2
  
  # Generate single pair with errors and display error info
  python edi_trainer.py --count=1 --error-rate=0.3 --display-error
  
  
  # Save to file
  python edi_trainer.py --count=5 --output=training_data.txt
        """
    )
    
    parser.add_argument(
        "--count", "-c",
        type=int,
        default=1,
        help="Number of ISA/IEA pairs to generate (default: 1)"
    )
    
    parser.add_argument(
        "--error-rate", "-e",
        type=float,
        default=0.0,
        help="Error rate (0.0-1.0) - probability of introducing errors (default: 0.0)"
    )
    
    parser.add_argument(
        "--display-error", "-d",
        action="store_true",
        help="Display error information"
    )
    
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Output file path (default: stdout)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Include human-readable comments and field descriptions"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not 0.0 <= args.error_rate <= 1.0:
        print("Error: error-rate must be between 0.0 and 1.0", file=sys.stderr)
        sys.exit(1)
    
    if args.count < 1:
        print("Error: count must be at least 1", file=sys.stderr)
        sys.exit(1)
    
    # Generate transactions
    try:
        output_lines = []
        
        for i in range(args.count):
            if args.verbose:
                output_lines.append(f"# Transaction {i+1}/{args.count}")
                output_lines.append("")
            
            # Generate ISA/IEA pair
            result = generate_isa_iea_pair(
                with_errors=args.error_rate > 0.0
            )
            
            # Add segments
            output_lines.append(result["isa_segment"])
            output_lines.append(result["iea_segment"])
            output_lines.append("")
            
            # Add error information if requested
            if args.display_error and result["error_info"]:
                output_lines.append(f"# Error Type: {result['error_info']['error_type']}")
                output_lines.append(f"# Error Target: {result['error_info']['error_target']}")
                output_lines.append(f"# {result['error_info']['explanation']}")
                output_lines.append("")
            
            if args.verbose:
                output_lines.append("# End Transaction")
                output_lines.append("")
        
        # Output results
        output_text = "\n".join(output_lines)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output_text)
            print(f"Generated {args.count} ISA/IEA pairs to {args.output}")
        else:
            print(output_text)
            
    except Exception as e:
        print(f"Error generating transactions: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
