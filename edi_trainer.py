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


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate realistic EDI 834 transactions with controllable error rates"
    )
    
    parser.add_argument(
        "-c", "--count", 
        type=int, 
        default=1,
        help="Number of transactions to generate (default: 1)"
    )
    
    parser.add_argument(
        "-e", "--error-rate",
        type=float,
        default=0.0,
        help="Error injection rate (0.0-1.0, default: 0.0)"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Output file path (default: stdout)"
    )
    
    parser.add_argument(
        "-l", "--learning-mode",
        action="store_true",
        default=True,
        help="Learning mode: generate transaction, wait for user input, then show error report."
    )
    
    parser.add_argument(
        "-d", "--display-error",
        action="store_true",
        help="Disable learning mode and show error report immediately"
    )
    
    args = parser.parse_args()
    
    # Input validation
    if args.count < 1:
        parser.error("Please provide a count of at least 1")
    
    if not 0.0 <= args.error_rate <= 1.0:
        parser.error("Please provide an error rate between 0.0 and 1.0")
    
    # Generate single transaction using transaction_generator
    from core.transaction_generator import generate_834_transaction
    
    result = generate_834_transaction(error_rate=args.error_rate)
    
    # Print transaction to stdout
    print(result["transaction"])
    
    # Handle learning mode
    if args.learning_mode and not args.display_error:
        error_info = result["error_info"]
        
        # Check if there are any errors to reveal
        error_found = any(value is not None for value in error_info.values())
        
        if error_found:
            # Generate list of hints and solution
            hints = []
            
            # Hint 1: Segment OR Field (not both)
            if error_info.get("error_target") == "SEGMENT" and error_info.get("error_segment", None):
                hints.append("❓ FIRST HINT:\n" + f"Segment with error: {error_info['error_segment']}")
            elif error_info.get("error_target") == "FIELD" and error_info.get("error_field", None):
                hints.append("❓ FIRST HINT:\n" + f"Field with error: {error_info['error_field']}")
            
            # Hint 2: Error Type
            hint_parts = []
            if error_info.get("error_type", None):
                hint_parts.append(f"Error type: {error_info['error_type'].replace('_', ' ').title()}")
            if hint_parts:
                hints.append("🔍 SECOND HINT:\n" + "\n".join(hint_parts))
            
            # Hint 3: Error Value
            hint_parts = []
            if error_info.get("error_value", None):
                hint_parts.append(f"Erroneous value: '{error_info['error_value']}'")
            if hint_parts:
                hints.append("🎯 THIRD HINT:\n" + "\n".join(hint_parts))
            
            # Solution: Error explanation
            if error_info.get("error_explanation", None):
                hints.append(f"✅ SOLUTION:\n{error_info['error_explanation']}")
            
            # Interactive hint system
            current_index = 0
            while current_index < len(hints):
                print("\nPress <ENTER> for hints or A + <ENTER> for answer...")
                
                user_input = input()
                if user_input == "":
                    # Show next hint
                    print(hints[current_index])
                    current_index += 1
                else:
                    # Show all remaining hints and solution
                    while current_index < len(hints):
                        print(hints[current_index])
                        current_index += 1
                    break

            
        else:
            print("\nPress <ENTER> for hints or A + <ENTER> for answer...")
            input()
            print("✅ No errors found. This is a valid EDI 834 transaction")
    
    # Handle immediate error display if --display-error flag is set
    elif args.display_error:
        print("\n--- ERROR REPORT ---")
        error_info = result["error_info"]
        
        error_found = False
        for key, value in error_info.items():
            if value is not None:
                print(f"{key.replace('_', ' ').title()}: {value}")
                error_found = True
        
        if not error_found:
            print("No errors found")


if __name__ == "__main__":
    main()
