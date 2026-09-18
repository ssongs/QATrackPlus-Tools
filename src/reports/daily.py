from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import mm

import calendar


def build_daily_report(
    records: dict,
    year_month: str,
) -> dict:
    """Build a Daily QA report structure from daily QA records."""

    year, month = map(int, year_month.split("-"))
    days_in_month = calendar.monthrange(year, month)[1]

    # Select records belonging to the requested month.
    month_records = {
        date: record
        for date, record in records.items()
        if date.startswith(year_month)
    }

    if not month_records:
        return {
            "year_month": year_month,
            "days": list(range(1, days_in_month + 1)),
            "rows": [],
        }

    # Use the test order from the first available QA record.
    first_record = next(iter(month_records.values()))

    rows = []

    for test in first_record.tests:

        # Display tolerance in the report.
        if test.test_type == "boolean":
            tolerance = "Func."
        elif test.reference is not None and test.tolerance is not None:
            tolerance = f"{test.reference:g}±{test.tolerance:g} {test.unit}"
        elif test.tolerance is not None:
            tolerance = f"±{test.tolerance:g} {test.unit}"
        else:
            tolerance = ""

        # Create one column for every day of the month.
        values = []

        for day in range(1, days_in_month + 1):
            date = f"{year_month}-{day:02d}"

            record = month_records.get(date)

            if record is None:
                values.append("")
                continue

            matching_test = next(
                (
                    item
                    for item in record.tests
                    if item.key == test.key
                ),
                None,
            )

            if matching_test is None:
                values.append("")
                continue

            if matching_test.skipped or matching_test.result is None:
                values.append("")
                continue

            if matching_test.test_type == "boolean":
                values.append(
                    "OK" if matching_test.result else "FAIL"
                )
            else:
                values.append(matching_test.result)

        rows.append({
            "key": test.key,
            "name": test.name,
            "tolerance": tolerance,
            "values": values,
        })

    return {
        "year_month": year_month,
        "days": list(range(1, days_in_month + 1)),
        "machine": first_record.machine,
        "protocol": first_record.protocol,
        "rows": rows,
    }


def print_daily_report(report: dict) -> None:
    """Print a monthly Daily QA report as a readable table."""

    days = report["days"]

    print()
    print(f"{report['protocol']} Report")
    print(f"Machine : {report['machine']}")
    print(f"Month   : {report['year_month']}")
    print()

    # Column widths
    test_width = max(
        len("Test Item"),
        *(len(row["name"]) for row in report["rows"])
    )

    tolerance_width = max(
        len("Tol."),
        *(len(str(row["tolerance"])) for row in report["rows"])
    )

    day_width = 6

    # Header
    header = (
        f"{'Test Item':<{test_width}} | "
        f"{'Tol.':<{tolerance_width}} | "
        + " | ".join(f"{day:^{day_width}}" for day in days)
    )

    print(header)
    print("-" * len(header))

    # Test rows
    for row in report["rows"]:
        formatted_values = []

        for value in row["values"]:
            if value == "":
                text = ""
            elif isinstance(value, float):
                text = f"{value:g}"
            else:
                text = str(value)

            formatted_values.append(
                f"{text:^{day_width}}"
            )

        print(
            f"{row['name']:<{test_width}} | "
            f"{row['tolerance']:<{tolerance_width}} | "
            + " | ".join(formatted_values)
        )

def generate_daily_pdf(
    report: dict,
    output_path: str | Path,
) -> None:
    """Generate a monthly Daily QA report as a PDF."""

    output_path = Path(output_path)

    # Use landscape A4 for the wider QA item columns.
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=landscape(A4),
        rightMargin=8 * mm,
        leftMargin=8 * mm,
        topMargin=8 * mm,
        bottomMargin=8 * mm,
    )

    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(
        Paragraph(
            f"<b>{report['protocol']} Report</b>",
            styles["Title"],
        )
    )

    elements.append(
        Paragraph(
            f"Machine : {report['machine']}<br/>"
            f"Month : {report['year_month']}",
            styles["Normal"],
        )
    )

    elements.append(Spacer(1, 5 * mm))

    # ---------------------------------------------------------
    # Table structure
    #
    # Date | Test 1 | Test 2 | Test 3 | ...
    # -----------------------------------------
    #   1  |   OK    |   OK    | 198.3  | ...
    #   2  |   OK    |   OK    | 198.8  | ...
    #   3  |   OK    |   OK    | 198.8  | ...
    # ---------------------------------------------------------

    rows = report["rows"]

    # Header
    header = ["Date"]

    for row in rows:
        header.append(
            f"{row['name']}\n{row['tolerance']}"
        )

    table_data = [header]

    # One row per day
    for day_index, day in enumerate(report["days"]):
        row_data = [str(day)]

        for row in rows:
            value = row["values"][day_index]

            if value == "":
                text = ""
            elif isinstance(value, float):
                text = f"{value:g}"
            else:
                text = str(value)

            row_data.append(text)

        table_data.append(row_data)

    # Column widths
    date_width = 10 * mm
    test_width = 28 * mm

    col_widths = (
        [date_width]
        + [test_width] * len(rows)
    )

    table = Table(
        table_data,
        colWidths=col_widths,
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                # Header
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

                # Grid
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),

                # Alignment
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

                # Font size
                ("FONTSIZE", (0, 0), (-1, 0), 6),
                ("FONTSIZE", (0, 1), (-1, -1), 7),

                # Padding
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("LEFTPADDING", (0, 0), (-1, -1), 2),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )

    elements.append(table)

    doc.build(elements)