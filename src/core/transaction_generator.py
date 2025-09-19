"""
EDI 834 Transaction Generator

Generates complete EDI 834 transactions with controllable error injection.
Builds full transactions using segment generators.
"""

import random
import yaml
from pathlib import Path
from .envelope_segment_generator import generate_envelope_data
from .member_segment_generator import generate_member_data
from .coverage_segment_generator import generate_coverage_data


def load_segment_list(verbose=False):
    """Load authoritative list of segments from all YAML specification files."""
    data_dir = Path(__file__).parent.parent / "data"
    yaml_files = [
        "envelope_segment_specifications.yaml",
        "member_segment_specifications.yaml", 
        "coverage_segment_specifications.yaml"
    ]
    
    segment_list = []
    for yaml_file in yaml_files:
        yaml_path = data_dir / yaml_file
        
        if yaml_path.exists():
            try:
                with open(yaml_path, 'r') as f:
                    data = yaml.safe_load(f)
                    
                if data and 'segments' in data:
                    segments = list(data['segments'].keys())
                    segment_list.extend(segments)
                    if verbose:
                        print(f"Loaded {len(segments)} segments from {yaml_file}: {segments}")
                else:
                    if verbose:
                        print(f"No segments found in {yaml_file}")
                    
            except yaml.YAMLError as e:
                if verbose:
                    print(f"Warning: Invalid YAML in {yaml_file}: {e}")
        else:
            if verbose:
                print(f"Warning: YAML file not found: {yaml_file}")
    
    if verbose:
        print(f"Total segments loaded: {len(segment_list)}")
    return segment_list

def generate_834_transaction(error_rate=0.0, count=1):
    """
    Generate a complete EDI 834 transaction.
    
    Args:
        error_rate (float): Probability of injecting errors (0.0-1.0)
        count (int): Number of transaction sets (ST/SE loops) to generate
        
    Returns:
        dict: Contains transaction string and error_info
    """

    # Load authoritative segment list from YAML files
    segment_list = load_segment_list()

    
    # Shared error state dictionary - passed by reference through call chain 
    # With error value returned by error generators at the end of the chain
    error_info = {
        "error_target": None,      # "segment" or "field" 
        "error_segment": None,     # Which segment (ISA, IEA, etc) or None
        "error_field": None,       # Which field (ISA01, IEA02, etc) or None
        "error_type": None,        # invalid value, missing value, etc.
        "error_value": None,       # The actual erroneous value to use
        "error_explanation": None  # List the rule that was violated
    }

    # Determine if error occurs
    if random.random() < error_rate:
        # Generate error info for injection
        error_info["error_target"] = random.choices(["SEGMENT", "FIELD"], weights=[20, 80])[0]
        
        # Pick a random segment to target
        if segment_list:
            error_info["error_segment"] = random.choice(segment_list)
            
            # If field error, discover all fields for that specific segment
            if error_info["error_target"] == "FIELD":
                from .envelope_segment_generator import load_field_specs
                field_specs = load_field_specs()
                
                segment_name = error_info["error_segment"]
                if segment_name in field_specs and 'fields' in field_specs[segment_name]:
                    segment_fields = list(field_specs[segment_name]['fields'].keys())
                    if segment_fields:
                        error_info["error_field"] = random.choice(segment_fields)
    
    # PHASE 1: GENERATE - Generate all segment data
    envelope_data = generate_envelope_data(error_info)
    member_data = generate_member_data(error_info)
    coverage_data = generate_coverage_data(error_info)
    
    """
    TODO: Add different purposes for multiple N1, REF, DTP segments for realism
      - N1: Sponsor, Insurance Company, Broker, etc.
      - REF: Subscriber ID, Group Number, Policy Number, etc.
      - DTP: Eligibility Date, Coverage Begin, Coverage End, etc.
    """
    
    # Build transaction segments in order
    segments = []
    
    # Interchange and functional group headers
    segments.extend(envelope_data["isa"])
    segments.extend(envelope_data["gs"])
    
    # Transaction sets (ST/SE loops)
    for i in range(count):
        segments.extend(envelope_data["st"])
        segments.extend(envelope_data["bgn"])
        
        # N1 segments (e.g. Sponsor, Insurance Company, sometimes Broker)
        n1_count = random.choices([2, 3], weights=[70, 30])[0]
        segments.extend(coverage_data["n1_segments"][:n1_count])
        
        segments.extend(coverage_data["ins"])
        
        # REF segments (e.g. Subscriber ID, Group Number, Policy Number)
        ref_count = random.choices([1, 2, 3], weights=[60, 30, 10])[0]
        segments.extend(coverage_data["ref_segments"][:ref_count])
        
        # DTP segments (e.g. Eligibility Date, Coverage Begin/End)
        dtp_count = random.choices([1, 2, 3, 4], weights=[50, 30, 15, 5])[0]
        segments.extend(coverage_data["dtp_segments"][:dtp_count])
        
        segments.extend(member_data["nm1"])
        
        # PER segments (contact information)
        per_count = random.choices([0, 1, 2], weights=[60, 30, 10])[0]
        segments.extend(member_data["per_segments"][:per_count])
        
        # N3 segments (address information)
        n3_count = random.choices([0, 1], weights=[20, 80])[0]
        segments.extend(member_data["n3_segments"][:n3_count])
        
        # N4 segments (geographic location)
        n4_count = random.choices([0, 1], weights=[20, 80])[0]
        segments.extend(member_data["n4_segments"][:n4_count])
        
        # DMG segments (demographic information)
        dmg_count = random.choices([0, 1], weights=[30, 70])[0]
        segments.extend(member_data["dmg_segments"][:dmg_count])
        
        # HD segments (e.g. Health, Dental, Vision, Pet coverage)
        hd_count = random.choices([1, 2, 3], weights=[60, 30, 10])[0]
        segments.extend(coverage_data["hd_segments"][:hd_count])
        # Each HD segment typically has multiple DTP segments (Coverage Begin, End, etc.)
        for j in range(hd_count):
            hd_dtp_count = random.choices([1, 2, 3], weights=[40, 40, 20])[0]
            segments.extend(coverage_data["dtp_segments"][:hd_dtp_count])
        
        # COB segments (coordination of benefits)
        cob_count = random.choices([0, 1], weights=[80, 20])[0]
        segments.extend(coverage_data["cob"][:cob_count])
        
        segments.extend(envelope_data["se"])
    
    # Functional group and interchange trailers
    segments.extend(envelope_data["ge"])
    segments.extend(envelope_data["iea"])
    
    # Join segments with newlines
    transaction = '\n'.join(segments)
    
    return {
        "transaction": transaction,
        "error_info": error_info
    }
