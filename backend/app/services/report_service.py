import io
import csv
from datetime import datetime
from sqlalchemy.orm import Session

from app.repositories.report_repository import (
    get_all_reports,
    get_report_summary_data,
    get_all_policies_data,
    get_all_schemes_data,
    get_all_feedback_data
)

def get_all_reports_service(db: Session):
    return get_all_reports(db)

def get_report_summary_service(db: Session):
    return get_report_summary_data(db)

def generate_pdf_report_bytes(db: Session) -> bytes:
    """Generate a PDF report containing Policy, Scheme, and Feedback summary data."""
    data = get_report_summary_data(db)
    policies = get_all_policies_data(db)
    schemes = get_all_schemes_data(db)
    feedbacks = get_all_feedback_data(db)

    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontSize=22,
            leading=26,
            textColor=colors.HexColor('#1E3A8A'),
            spaceAfter=12
        )
        subtitle_style = ParagraphStyle(
            'ReportSubTitle',
            parent=styles['Heading2'],
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#2563EB'),
            spaceBefore=12,
            spaceAfter=8
        )
        body_style = styles['Normal']

        story = []
        story.append(Paragraph("PolicyGPT System Summary & Intelligence Report", title_style))
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}", body_style))
        story.append(Spacer(1, 12))

        # Metrics Table
        summary_table_data = [
            ["Metric", "Value"],
            ["Total Policies", str(data["total_policies"])],
            ["Published Policies", str(data["published_policies"])],
            ["Pending Policies", str(data["pending_policies"])],
            ["Total Welfare Schemes", str(data["total_schemes"])],
            ["Active Welfare Schemes", str(data["active_schemes"])],
            ["Total User Feedback", str(data["total_feedback"])],
            ["Average Rating", f"{data['average_rating']} / 5.0"]
        ]
        st_table = Table(summary_table_data, colWidths=[200, 200])
        st_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#1E3A8A')),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8FAFC')),
        ]))
        story.append(st_table)
        story.append(Spacer(1, 16))

        # Schemes Table
        story.append(Paragraph("Government Schemes", subtitle_style))
        scheme_rows = [["ID", "Title", "Category", "Status"]]
        for s in schemes[:15]:
            scheme_rows.append([str(s.id), (s.title[:35] + '...') if len(s.title) > 35 else s.title, s.category or 'N/A', s.status or 'Active'])
        sc_table = Table(scheme_rows, colWidths=[30, 220, 150, 60])
        sc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
        ]))
        story.append(sc_table)
        story.append(Spacer(1, 16))

        # Feedback Table
        story.append(Paragraph("User Feedback Entries", subtitle_style))
        fb_rows = [["ID", "User Name", "Rating", "Message"]]
        for f in feedbacks[:15]:
            fb_msg = f.message or f.content or ""
            fb_rows.append([str(f.id), f.user_name or "Anonymous", f"{f.rating or 5} ★", (fb_msg[:40] + '...') if len(fb_msg) > 40 else fb_msg])
        fb_table = Table(fb_rows, colWidths=[30, 120, 60, 250])
        fb_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0D9488')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
        ]))
        story.append(fb_table)

        doc.build(story)
        return buffer.getvalue()
    except ImportError:
        # Fallback PDF generator using standard 1.4 PDF structure
        text_lines = []
        text_lines.append("PolicyGPT System Summary & Intelligence Report")
        text_lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        text_lines.append("")
        text_lines.append(f"Total Policies: {data['total_policies']} | Published: {data['published_policies']}")
        text_lines.append(f"Total Schemes: {data['total_schemes']} | Active: {data['active_schemes']}")
        text_lines.append(f"Total Feedback: {data['total_feedback']} | Avg Rating: {data['average_rating']}/5.0")
        text_lines.append("")
        text_lines.append("--- Welfare Schemes ---")
        for s in schemes[:10]:
            text_lines.append(f"[{s.id}] {s.title} ({s.category}) - Status: {s.status}")
        text_lines.append("")
        text_lines.append("--- User Feedback ---")
        for f in feedbacks[:10]:
            msg = f.message or f.content or ""
            text_lines.append(f"[{f.id}] {f.user_name or 'Anonymous'} ({f.rating or 5}/5): {msg}")

        full_content = "\n".join(text_lines)
        
        # Build simple valid PDF
        pdf_stream = f"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj
4 0 obj
<< /Length {len(full_content) * 2 + 100} >>
stream
BT
/F1 12 Tf
50 750 Td
14 TL
"""
        for line in text_lines:
            escaped_line = line.replace("(", "\\(").replace(")", "\\)")
            pdf_stream += f"({escaped_line}) '\n"
        pdf_stream += """ET
endstream
endobj
5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000244 00000 n 
0000000450 00000 n 
trailer
<< /Size 6 /Root 1 0 R >>
startxref
535
%%EOF"""
        return pdf_stream.encode('latin1')

def generate_excel_report_bytes(db: Session) -> bytes:
    """Generate an Excel / Spreadsheet report containing Schemes, Policies, and Feedback."""
    data = get_report_summary_data(db)
    policies = get_all_policies_data(db)
    schemes = get_all_schemes_data(db)
    feedbacks = get_all_feedback_data(db)

    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment

        wb = openpyxl.Workbook()
        
        # Sheet 1: Summary Metrics
        ws_summary = wb.active
        ws_summary.title = "Summary"
        ws_summary.append(["PolicyGPT Platform Analytics & Summary Report"])
        ws_summary.append(["Generated Date", datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")])
        ws_summary.append([])
        ws_summary.append(["Metric", "Count / Value"])
        ws_summary.append(["Total Policies", data["total_policies"]])
        ws_summary.append(["Published Policies", data["published_policies"]])
        ws_summary.append(["Pending Policies", data["pending_policies"]])
        ws_summary.append(["Draft Policies", data["draft_policies"]])
        ws_summary.append(["Total Welfare Schemes", data["total_schemes"]])
        ws_summary.append(["Active Welfare Schemes", data["active_schemes"]])
        ws_summary.append(["Total User Feedback", data["total_feedback"]])
        ws_summary.append(["Average Rating", data["average_rating"]])

        # Sheet 2: Schemes
        ws_schemes = wb.create_sheet(title="Schemes")
        ws_schemes.append(["ID", "Title", "Category", "Department", "State", "Status", "Eligibility Criteria", "Benefits"])
        for s in schemes:
            ws_schemes.append([
                s.id, s.title, s.category, s.department, s.state, s.status, s.eligibility_criteria, s.benefits
            ])

        # Sheet 3: Policies
        ws_policies = wb.create_sheet(title="Policies")
        ws_policies.append(["ID", "Title", "Category", "Department", "State", "Status", "Description"])
        for p in policies:
            ws_policies.append([
                p.id, p.title, p.category, p.department, p.state, p.status, p.description
            ])

        # Sheet 4: Feedback
        ws_feedback = wb.create_sheet(title="Feedback")
        ws_feedback.append(["ID", "User Name", "Rating", "Message", "Created At"])
        for f in feedbacks:
            ws_feedback.append([
                f.id,
                f.user_name or "Anonymous",
                f.rating or 5,
                f.message or f.content or "",
                f.created_at.strftime("%Y-%m-%d %H:%M:%S") if f.created_at else ""
            ])

        output = io.BytesIO()
        wb.save(output)
        return output.getvalue()
    except ImportError:
        # Fallback CSV format
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(["=== SUMMARY METRICS ==="])
        writer.writerow(["Metric", "Value"])
        writer.writerow(["Total Policies", data["total_policies"]])
        writer.writerow(["Published Policies", data["published_policies"]])
        writer.writerow(["Total Welfare Schemes", data["total_schemes"]])
        writer.writerow(["Active Welfare Schemes", data["active_schemes"]])
        writer.writerow(["Total User Feedback", data["total_feedback"]])
        writer.writerow(["Average Rating", data["average_rating"]])
        writer.writerow([])

        writer.writerow(["=== WELFARE SCHEMES ==="])
        writer.writerow(["ID", "Title", "Category", "Department", "Status", "Eligibility"])
        for s in schemes:
            writer.writerow([s.id, s.title, s.category, s.department, s.status, s.eligibility_criteria])
        writer.writerow([])

        writer.writerow(["=== GOVERNMENT POLICIES ==="])
        writer.writerow(["ID", "Title", "Category", "Department", "Status"])
        for p in policies:
            writer.writerow([p.id, p.title, p.category, p.department, p.status])
        writer.writerow([])

        writer.writerow(["=== USER FEEDBACK ==="])
        writer.writerow(["ID", "User Name", "Rating", "Message", "Created At"])
        for f in feedbacks:
            writer.writerow([f.id, f.user_name or "Anonymous", f.rating or 5, f.message or f.content or "", f.created_at])

        return output.getvalue().encode('utf-8')

