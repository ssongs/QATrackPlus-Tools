from datetime import date

from src.builders.record_builder import build_record
from src.protocol.loader import load_protocol


def main():
    protocol = load_protocol(
        "config/protocols/ct/siemens_go_sim_daily.yaml"
    )

    results = {
        "gantry_moving_laser_alignment": {
            "result": True,
        },

        "moving_laser_scan_plane_alignment": {
            "result": True,
        },

        "spatial_integrity": {
            "result": 199.8,
        },

        "hu_water": {
            "result": 2,
        },

        "hu_air": {
            "result": -999,
        },

        "noise_water": {
            "result": 4.1,
        },

        "noise_air": {
            "result": 1.9,
        },

        "sentinel_isocenter_check": {
            "result": None,
            "skipped": True,
            "comment": "Sentinel phantom unavailable",
        },

        "couch_profile_deviation": {
            "result": 0.8,
        },
    }

    record = build_record(
        protocol=protocol,
        results=results,
    )

    print(record)
    print(record.status)
    print(record.passed)


if __name__ == "__main__":
    main()