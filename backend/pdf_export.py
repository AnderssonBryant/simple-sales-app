from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO


def generate_detailed_sales_pdf(df, start_date, end_date):
    if df.empty:
        return None

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(
        Paragraph(
            f"<b>Sales Report</b><br/>{start_date} to {end_date}",
            styles["Title"]
        )
    )
    elements.append(Spacer(1, 12))

    table_data = [
        ["Date", "Product", "Price (Rp)", "Qty", "Total (Rp)"]
    ]

    total_amount = 0
    total_qty = 0

    for _, row in df.iterrows():
        total_amount += int(row["total"])
        total_qty += int(row["qty"])
        table_data.append([
            str(row["date"]),
            row["product_name"],
            f"{int(row['price']):,}",
            int(row["qty"]),
            f"{int(row['total']):,}"
        ])

    table_data.append(["", "TOTAL", "", f"{total_qty:,}", f"{total_amount:,}"])

    table = Table(table_data, colWidths=[70, 160, 80, 50, 90])

    table.setStyle(TableStyle([
        # Header
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
        ("LINEBELOW", (0, 0), (-1, 0), 1, colors.black),

        # Alignment
        ("ALIGN", (2, 1), (-1, -1), "RIGHT"),

        # TOTAL row
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("LINEABOVE", (0, -1), (-1, -1), 1.2, colors.black),
        ("TOPPADDING", (0, -1), (-1, -1), 8),
    ]))

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    return buffer.getvalue()



def generate_sales_summary_pdf(summary_df, start_date, end_date):
    """
    Generate a sales summary PDF grouped by product.
    Returns PDF bytes.
    """

    if summary_df.empty:
        return None

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(
        Paragraph(
            f"<b>Sales Summary</b><br/>{start_date} to {end_date}",
            styles["Title"]
        )
    )
    elements.append(Spacer(1, 12))

    table_data = [
        ["Product", "Quantity", "Total (Rp)"]
    ]

    grand_total = 0

    for _, row in summary_df.iterrows():
        grand_total += int(row["total"])
        table_data.append([
            row["product_name"],
            int(row["qty"]),
            f"{int(row['total']):,}"
        ])

    # Total row
    table_data.append([
        "TOTAL",
        "",
        f"{grand_total:,}"
    ])

    table = Table(table_data, colWidths=[220, 80, 120])

    table.setStyle(TableStyle([
        # Header
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
        ("LINEBELOW", (0, 0), (-1, 0), 1, colors.black),

        # Alignment
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),

        # Total row
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("LINEABOVE", (0, -1), (-1, -1), 1.2, colors.black),
        ("TOPPADDING", (0, -1), (-1, -1), 8),
    ]))

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    return buffer.getvalue()