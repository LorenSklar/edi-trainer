"""
EDI 834 Transaction Generator

Generates complete EDI 834 transactions with controllable error injection.
Builds full transactions using segment generators.
"""

import random
import yaml
from pathlib import Path
from .envelope_segment_generator import (
    generate_isa_segment, generate_iea_segment, generate_gs_segment, 
    generate_ge_segment, generate_st_segment, generate_se_segment, generate_bgn_segment
)
from .member_segment_generator import (
    generate_nm1_segment, generate_per_segment, generate_n3_segment, 
    generate_n4_segment, generate_dmg_segment
)
from .coverage_segment_generator import (
    generate_n1_segment, generate_ins_segment, generate_ref_segment,
    generate_dtp_segment, generate_hd_segment, generate_cob_segment
)


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

    
    error_info = {
        "error_target": None,      # "segment" or "field" where the error occurs
        "error_segment": None,     # Which segment (ISA, IEA, etc) or None
        "error_field": None,       # Which field (01, 02, etc) or None
        "error_type": None,        # invalid value, missing value, etc.
        "error_value": None,       # The actual erroneous value to use
        "error_explanation": None  # List the rule that was violated
    }

    # Determine if error occurs
    if random.random() < error_rate:
        # Generate error info for injection
        error_info["error_target"] = random.choices(["SEGMENT", "FIELD"], weights=[20, 80])[0]
        
        # Pick a random segment to fuck up
        if segment_list:
            error_info["error_segment"] = random.choice(segment_list)
    
    """
    TODO: Add different purposes for multiple N1, REF, DTP segments for realism
      - N1: Sponsor, Insurance Company, Broker, etc.
      - REF: Subscriber ID, Group Number, Policy Number, etc.
      - DTP: Eligibility Date, Coverage Begin, Coverage End, etc.
    """
    
    # Build transaction segments in order
    segments = []
    
    # Interchange and functional group headers
    segments.append(generate_isa_segment(error_info))
    segments.append(generate_gs_segment(error_info))
    
    # Transaction sets (ST/SE loops)
    for i in range(count):
        segments.append(generate_st_segment(error_info))
        segments.append(generate_bgn_segment(error_info))
        
        # N1 segments (e.g.Sponsor, Insurance Company, sometimes Broker)
        n1_count = random.choices([2, 3], weights=[70, 30])[0]
        for _ in range(n1_count):
            segments.append(generate_n1_segment(error_info))
        
        segments.append(generate_ins_segment(error_info))
        
        # REF segments (e.g. Subscriber ID, Group Number, Policy Number)
        ref_count = random.choices([1, 2, 3], weights=[60, 30, 10])[0]
        for _ in range(ref_count):
            segments.append(generate_ref_segment(error_info))
        
        # DTP segments (e.g. Eligibility Date, Coverage Begin/End)
        dtp_count = random.choices([1, 2, 3, 4], weights=[50, 30, 15, 5])[0]
        for _ in range(dtp_count):
            segments.append(generate_dtp_segment(error_info))
        
        segments.append(generate_nm1_segment(error_info))
        
        # PER segments (contact information)
        per_count = random.choices([0, 1, 2], weights=[60, 30, 10])[0]
        for _ in range(per_count):
            segments.append(generate_per_segment(error_info))
        
        # N3 segments (address information)
        n3_count = random.choices([0, 1], weights=[20, 80])[0]
        for _ in range(n3_count):
            segments.append(generate_n3_segment(error_info))
        
        # N4 segments (geographic location)
        n4_count = random.choices([0, 1], weights=[20, 80])[0]
        for _ in range(n4_count):
            segments.append(generate_n4_segment(error_info))
        
        # DMG segments (demographic information)
        dmg_count = random.choices([0, 1], weights=[30, 70])[0]
        for _ in range(dmg_count):
            segments.append(generate_dmg_segment(error_info))
        
        # HD segments (e.g. Health, Dental, Vision, Pet coverage)
        hd_count = random.choices([1, 2, 3], weights=[60, 30, 10])[0]
        for _ in range(hd_count):
            segments.append(generate_hd_segment(error_info))
            # Each HD segment typically has multiple DTP segments (Coverage Begin, End, etc.)
            hd_dtp_count = random.choices([1, 2, 3], weights=[40, 40, 20])[0]
            for _ in range(hd_dtp_count):
                segments.append(generate_dtp_segment(error_info))
        
        # COB segments (coordination of benefits)
        cob_count = random.choices([0, 1], weights=[80, 20])[0]
        for _ in range(cob_count):
            segments.append(generate_cob_segment(error_info))
        
        segments.append(generate_se_segment(error_info))
    
    # Functional group and interchange trailers
    segments.append(generate_ge_segment(error_info))
    segments.append(generate_iea_segment(error_info))
    
    # Join segments with newlines
    transaction = '\n'.join(segments)
    
    return {
        "transaction": transaction,
        "error_info": error_info
    }
