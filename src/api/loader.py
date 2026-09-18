from src.models.qa_test import QATest


def load_qa_tests(client, unit_id: int, protocol) -> list[QATest]:
    """Load QA tests defined in a protocol from a QATrack+ unit."""

    qa_tests = []

    for section in protocol.sections:
        for test_definition in section.tests:

            slug = test_definition.key

            infos = client.get(
                f"/api/qc/unittestinfos/?unit={unit_id}&test__slug={slug}"
            )

            if infos["count"] == 0:
                continue

            info = infos["results"][0]

            test_data = client.get(info["test"])

            if test_data["type"] == "upload":
                continue

            test_type = test_data["type"]

            if test_type == "boolean":
                qa_test_type = "boolean"
            else:
                qa_test_type = "numeric"

            reference_data = (
                client.get(info["reference"])
                if info["reference"]
                else None
            )

            tolerance_data = (
                client.get(info["tolerance"])
                if info["tolerance"]
                else None
            )

            if qa_test_type == "boolean":
                reference = None
                tolerance = None

            else:
                reference = (
                    reference_data["value"]
                    if reference_data
                    else None
                )

                if tolerance_data and tolerance_data["type"] == "absolute":
                    tolerance = tolerance_data["act_high"]
                else:
                    tolerance = None

            qa_test = QATest(
                key=test_data["slug"],
                name=test_data["display_name"],
                test_type=qa_test_type,
                result=None,
                unit=test_definition.unit,
                reference=reference,
                tolerance=tolerance,
                trend=test_definition.trend,
            )

            qa_tests.append(qa_test)

    return qa_tests

def load_qa_results(client, unit_id: int, protocol):
    """Load QA measurement results for tests defined in a protocol."""

    results = {}

    for section in protocol.sections:
        for test_definition in section.tests:

            slug = test_definition.key

            infos = client.get(
                f"/api/qc/unittestinfos/?unit={unit_id}&test__slug={slug}"
            )

            if infos["count"] == 0:
                continue

            info = infos["results"][0]

            unit_test_info_id = info["url"].rstrip("/").split("/")[-1]

            instances = client.get(
                f"/api/qc/testinstances/?unit_test_info={unit_test_info_id}"
            )

            test_results = []

            for instance in instances["results"]:
                print(instance)

                test_results.append({
                    "date": instance["work_completed"],
                    "value": instance["value"],
                    "pass_fail": instance["pass_fail"],
                    "skipped": instance["skipped"],
                    "comment": instance["comment"],
                })

            test_results.sort(key=lambda x: x["date"])

            results[slug] = test_results

    return results