from src.protocol.loader import load_protocol
from src.builders.record_builder import build_record

protocol = load_protocol(
    "config/protocols/ct/siemens_go_sim.yaml"
)

results = {
    "gantry_moving_laser_alignment": True,
    "moving_laser_scan_plane_alignment": True,
    "spatial_integrity": 199.8,
    "hu_water": 2,
    "hu_air": -999,
    "noise_water": 4.1,
    "noise_air": 1.9,
    "sentinel_isocenter_check": True,
    "couch_profile_deviation": 0.8,
}

record = build_record(protocol, results)

print(record)
print(record.passed)