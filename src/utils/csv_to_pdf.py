from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def convert_csv_to_pdf(csv_file_path, pdf_file_path):
    # Read lines
    with open(csv_file_path, encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    # Split into sections
    metadata, summary_data, transaction_data = [], [], []
    summary_header = transaction_header = ""
    section = "meta"

    for line in lines:
        clean_line = line.replace('"', '').strip()
        if section == "meta":
            metadata.append(clean_line)
            if clean_line.startswith("MARKNADSNAMN"):
                summary_header = clean_line
                section = "summary_data"
        elif section == "summary_data":
            if clean_line.startswith("DATUM"):
                transaction_header = clean_line
                section = "transaction_data"
            else:
                summary_data.append(clean_line)
        elif section == "transaction_data":
            transaction_data.append(clean_line)

    # Prepare document
    doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Summary (filtered columns + clean search date)
    if summary_data:
        elements.append(Paragraph("Översikt", styles["Heading3"]))

        # Extract and clean search date range
        search_line = next((line for line in metadata if line.startswith("Sök:")), "")
        search_date = search_line.split(';')[1].split(',')[0].strip() if ";" in search_line else "N/A"

        # Filter columns
        summary_cols_to_keep = ["ANTAL SWISH-BETALNINGAR", "TOTALT INBETALAT BELOPP"]
        all_summary_cols = summary_header.split(';')
        keep_indices = [i for i, col in enumerate(all_summary_cols) if col in summary_cols_to_keep]

        filtered_header = ["SÖKDATUM"] + [all_summary_cols[i] for i in keep_indices]
        first_summary_row = summary_data[0].split(';') if summary_data else []
        filtered_data = [[search_date] + [first_summary_row[i] for i in keep_indices]]

        table_data = [filtered_header] + filtered_data

        # Fixed width for summary table
        table_width = 600
        num_summary_cols = len(filtered_header)
        summary_col_widths = [table_width / num_summary_cols] * num_summary_cols

        t = Table(table_data, colWidths=summary_col_widths)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('ALIGN', (0, 0), (-1, 0), 'LEFT'),    # Header
            ('ALIGN', (0, 1), (-2, -1), 'LEFT'),   # All but last column
            ('ALIGN', (-1, 1), (-1, -1), 'RIGHT'), # Last column (amount)
        ]))
        elements.append(t)
        elements.append(Spacer(1, 12))

    # Transactions table
    transaction_cols = ["DATUM", "TID", "MARKNADSNAMN", "SWISH NUMMER", "NAMN", "MOBILNUMMER", "BELOPP"]
    all_cols = transaction_header.split(';')
    col_indices = [i for i, col in enumerate(all_cols) if col in transaction_cols]
    table_data = [[all_cols[i] for i in col_indices]]

    for row in transaction_data:
        parts = row.split(';')
        selected = [parts[i] if i < len(parts) else '' for i in col_indices]
        table_data.append(selected)

    # Dynamic column widths, total table width same as summary
    max_col_lengths = [max(len(str(row[i])) for row in table_data) for i in range(len(col_indices))]
    total_length = sum(max_col_lengths)
    transaction_col_widths = [(600 * (length / total_length)) for length in max_col_lengths]

    t = Table(table_data, colWidths=transaction_col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),     # Header row
        ('ALIGN', (0, 1), (-2, -1), 'LEFT'),    # All columns except amount
        ('ALIGN', (-1, 1), (-1, -1), 'RIGHT'),  # Right-align BELOPP
    ]))
    elements.append(Paragraph("Transaktioner", styles["Heading3"]))
    elements.append(t)

    # Build PDF
    doc.build(elements)
