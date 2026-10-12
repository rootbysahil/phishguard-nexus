"""
PHISHGUARD//NEXUS - Incident Report PDF Generation
POST /api/report
"""

import io
import json
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from backend.app.db.models import ScanRecord
from backend.app.db.session import get_db

router = APIRouter(tags=["Report"])


class ReportRequest(BaseModel):
    scan_id: str


@router.post("/report")
def generate_report(req: ReportRequest, db: Session = Depends(get_db)):
    record = db.query(ScanRecord).filter(ScanRecord.id == req.scan_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Scan record not found")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading1"],
        fontSize=20,
        textColor=colors.HexColor("#0D0F18"),
        spaceAfter=10
    )
    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#6B7BA4"),
        spaceAfter=15
    )

    elements = []
    elements.append(Paragraph("PHISHGUARD//NEXUS — INCIDENT REPORT", title_style))
    elements.append(Paragraph(f"Generated at: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')} | ID: {record.id}", subtitle_style))
    elements.append(Spacer(1, 12))

    # Summary Table
    verdict_color = colors.HexColor("#FF2E4D") if record.verdict == "PHISHING" else colors.HexColor("#39FF14")
    summary_data = [
        ["Target Analyzed", record.target],
        ["Modality", record.type.upper()],
        ["Final Verdict", record.verdict],
        ["Calibrated Threat Probability", f"{round(record.probability * 100, 2)}%"],
        ["Risk Level", f"{record.risk_level} / 10"],
        ["SHA-256 Content Hash", record.content_hash[:32] + "..."]
    ]

    t = Table(summary_data, colWidths=[200, 340])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F5F7FB")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#1A2040")),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1"))
    ]))
    elements.append(t)
    elements.append(Spacer(1, 16))

    # Red Flags
    elements.append(Paragraph("<b>Identified Red Flags & Behavioral Anomaly Markers:</b>", styles["Heading3"]))
    red_flags = json.loads(record.red_flags_json)
    if red_flags:
        for rf in red_flags:
            elements.append(Paragraph(f"• {rf}", styles["Normal"]))
    else:
        elements.append(Paragraph("• No malicious anomaly markers identified.", styles["Normal"]))
    elements.append(Spacer(1, 16))

    # AI Advisory
    elements.append(Paragraph("<b>AI Security Analyst Advisory (Powered by IBM watsonx.ai):</b>", styles["Heading3"]))
    expl = json.loads(record.explanation_json)
    elements.append(Paragraph(expl.get("en", "No advisory available."), styles["Normal"]))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"<b>Recommended Action:</b> {expl.get('what_to_do', 'N/A')}", styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)

    pdf_bytes = buffer.getvalue()
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=phishguard-report-{record.id}.pdf"}
    )
