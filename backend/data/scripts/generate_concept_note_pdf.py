"""
PHISHGUARD//NEXUS - Official Concept Note & Lean Canvas PDF Generator
AICTE - BharatCares - IBM SkillsBuild Internship 2026
Student: Sahil Rai | ID: IBMUEML002432
"""

from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

def build_pdf(output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    primary_color = colors.HexColor('#0F62FE')    # IBM Carbon Blue
    dark_header = colors.HexColor('#161616')      # Carbon Gray 100
    light_bg = colors.HexColor('#F4F4F4')         # Carbon Gray 10
    border_color = colors.HexColor('#C6C6C6')

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=21,
        textColor=primary_color,
        alignment=1
    )

    sub_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#525252'),
        alignment=1
    )

    h2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=dark_header,
        spaceBefore=6,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#262626')
    )

    cell_style = ParagraphStyle(
        'Cell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor('#262626')
    )

    cell_header = ParagraphStyle(
        'CellHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=primary_color
    )

    elements = []

    # 1. Header
    elements.append(Paragraph('AICTE – BharatCares – IBM SkillsBuild Machine Learning and Applied AI Internship 2026', sub_style))
    elements.append(Paragraph('PROJECT CONCEPT NOTE & LEAN CANVAS', title_style))
    elements.append(Paragraph('Capstone Project Submission | Masterclass 5 Framework', sub_style))
    elements.append(Spacer(1, 8))

    # 2. Metadata Table
    meta_data = [
        [Paragraph('<b>Project Title:</b>', cell_style), Paragraph('PHISHGUARD//NEXUS: Explainable AI Phishing & Scam Detection Platform', cell_style)],
        [Paragraph('<b>Student Name:</b>', cell_style), Paragraph('Sahil Rai', cell_style)],
        [Paragraph('<b>Internship ID:</b>', cell_style), Paragraph('IBMUEML002432', cell_style)],
        [Paragraph('<b>Academic Institution:</b>', cell_style), Paragraph('Lovely Professional University (LPU), Punjab', cell_style)],
        [Paragraph('<b>Live Cloud URL:</b>', cell_style), Paragraph('https://phishguard-nexus.vercel.app/ &nbsp;(Shortlink: tinyurl.com/pg-nexus)', cell_style)],
        [Paragraph('<b>GitHub Repository:</b>', cell_style), Paragraph('https://github.com/rootbysahil/phishguard-nexus', cell_style)],
    ]
    t_meta = Table(meta_data, colWidths=[1.6*inch, 5.7*inch])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_bg),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(t_meta)
    elements.append(Spacer(1, 8))

    # 3. Executive Summary & UN SDG
    elements.append(Paragraph('1. Executive Summary & UN SDG Alignment', h2_style))
    elements.append(Paragraph(
        '<b>PHISHGUARD//NEXUS</b> is an Explainable AI (XAI) cybersecurity system engineered to detect and mitigate zero-day phishing across URLs, emails, and SMS without external network lookups. Driven by 24 lexical signals, a calibrated Logistic Regression classifier (ROC-AUC: 1.000, F2: 0.9989), directional SHAP feature attribution, and an IBM watsonx / Granite LLM advisory interface, it links high-precision AI detection with India\'s National Cybercrime infrastructure (Helpline 1930 / cybercrime.gov.in).',
        body_style
    ))
    elements.append(Spacer(1, 3))
    elements.append(Paragraph(
        '• <b>UN SDG 9 (Industry, Innovation & Infrastructure - Target 9.c):</b> Delivers equitable, zero-latency phishing defense infrastructure accessible to Indian citizens, MSMEs, and educational institutions.<br/>'
        '• <b>UN SDG 16 (Peace, Justice & Strong Institutions - Target 16.4):</b> Actively counters financial cybercrime, identity harvesting, and digital extortion.',
        body_style
    ))
    elements.append(Spacer(1, 8))

    # 4. Problem Statement
    elements.append(Paragraph('2. Problem Statement & Critical Industry Gaps', h2_style))
    elements.append(Paragraph(
        '<b>1. Lagged Static Blacklists:</b> Over 70% of modern phishing domains operate for less than 4 hours; conventional blacklists lag by 12–48 hours.<br/>'
        '<b>2. Black-Box Neural Networks:</b> Deep learning models output opaque risk probabilities with zero forensic explanations, causing user distrust.<br/>'
        '<b>3. Privacy Leakage & Latency:</b> Standard scanners perform live DNS/HTTP queries, alerting attackers and exposing victim IP addresses.<br/>'
        '<b>4. Lack of Vernacular Recourse:</b> Non-technical citizens lack actionable guidance in regional languages (Hindi, Punjabi) or immediate emergency escalation.',
        body_style
    ))
    elements.append(Spacer(1, 8))

    # 5. Lean Canvas Table
    elements.append(Paragraph('3. The Lean Canvas (9-Box Framework | Masterclass 5)', h2_style))

    box1 = Paragraph('<b>1. PROBLEM</b><br/>• Zero-day phishing expires before blacklists update.<br/>• Black-box AI lacks forensic trust.<br/>• Scanners leak victim IP.<br/><br/><i>Existing Alternatives:</i><br/>VirusTotal, Google Safe Browsing.', cell_style)
    box2 = Paragraph('<b>4. SOLUTION</b><br/>• 24 pure-Python lexical features (0 network calls).<br/>• Calibrated ML (ROC-AUC 1.000, F2 0.9989).<br/>• Directional SHAP XAI.<br/>• Multilingual watsonx advisories.<br/>• Automated forensic PDF reports.', cell_style)
    box3 = Paragraph('<b>3. UNIQUE VALUE PROP</b><br/><b>Core Value:</b><br/>"Zero-latency forensic defense that explains WHY a link is dangerous and WHAT TO DO in regional languages."<br/><br/><b>High-Level Concept:</b><br/>VirusTotal + IBM XAI + 1930 Helpline.', cell_style)
    box4 = Paragraph('<b>9. UNFAIR ADVANTAGE</b><br/>• Zero-leakage domain-grouped training split.<br/>• Privacy-first zero-call architecture.<br/>• Native Indian Cybercrime 1930 / portal escalation.', cell_style)
    box5 = Paragraph('<b>2. CUSTOMER SEGMENTS</b><br/>• Everyday Indian mobile & UPI banking users.<br/>• Elderly citizens prone to KYC scams.<br/>• MSMEs without dedicated SOCs.<br/><br/><i>Early Adopters:</i><br/>University students & fintech users.', cell_style)

    box_metrics = Paragraph('<b>8. KEY METRICS</b><br/>• ROC-AUC (1.000) & F2 (0.9989)<br/>• Inference Latency (&lt;15ms)<br/>• Citizen scans logged & PDF reports exported', cell_style)
    box_channels = Paragraph('<b>5. CHANNELS</b><br/>• Vercel Cloud Web App (tinyurl.com/pg-nexus)<br/>• Mobile QR Code & PWA<br/>• AICTE & IBM SkillsBuild Showcase', cell_style)

    box_cost = Paragraph('<b>7. COST STRUCTURE</b><br/>• Vercel Serverless Hosting (Hobby Tier: $0)<br/>• Model Storage & Compute: Local / Edge SQLite<br/>• IBM watsonx.ai Token Usage', cell_style)
    box_rev = Paragraph('<b>6. REVENUE / SUSTAINABILITY STREAMS</b><br/>• Free Community Tier: Public citizen protection<br/>• Enterprise B2B API: Pay-per-scan endpoint for Indian fintechs & banks<br/>• Institutional Audits: Branded forensic compliance reports', cell_style)

    canvas_grid = [
        [box1, box2, box3, box4, box5],
        ['', box_metrics, '', box_channels, ''],
        [box_cost, '', box_rev, '', '']
    ]

    t_canvas = Table(canvas_grid, colWidths=[1.46*inch, 1.46*inch, 1.46*inch, 1.46*inch, 1.46*inch])
    t_canvas.setStyle(TableStyle([
        ('SPAN', (0,0), (0,1)),
        ('SPAN', (2,0), (2,1)),
        ('SPAN', (4,0), (4,1)),
        ('SPAN', (0,2), (1,2)),
        ('SPAN', (2,2), (4,2)),
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('GRID', (0,0), (-1,-1), 0.6, primary_color),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 3.5),
        ('RIGHTPADDING', (0,0), (-1,-1), 3.5),
    ]))
    elements.append(t_canvas)

    # Page Break for clean two-page structure
    elements.append(PageBreak())

    # 6. Technical Accomplishments
    elements.append(Paragraph('4. Machine Learning & Applied AI Architecture', h2_style))
    elements.append(Paragraph(
        '• <b>Champion ML Classifier:</b> Calibrated Logistic Regression using Platt probability scaling, mitigating path-length bias with balanced benign samples.<br/>'
        '• <b>Validation Rigor:</b> Strict GroupShuffleSplit on registered domains; zero test-train domain leakage.<br/>'
        '• <b>Explainability (XAI):</b> LinearExplainer assigning directional weights to 24 features (entropy, brand displacement, homoglyphs).<br/>'
        '• <b>IBM watsonx.ai Integration:</b> Synthesizes forensic findings into plain language and powers regional translations (English, Hindi, Punjabi).<br/>'
        '• <b>Automated Forensic PDF:</b> Real-time audit generation stamped with SHA-256 cryptographic verification.',
        body_style
    ))
    elements.append(Spacer(1, 10))

    # 7. Milestone Mapping
    elements.append(Paragraph('5. IBM SkillsBuild 6-Week Masterclass Milestones Alignment', h2_style))
    mile_data = [
        [Paragraph('<b>Week</b>', cell_header), Paragraph('<b>SkillsBuild Masterclass</b>', cell_header), Paragraph('<b>Project Accomplishment Executed</b>', cell_header)],
        [Paragraph('Week 1', cell_style), Paragraph('Kickstart ML & Tools (VS Code, BOB)', cell_style), Paragraph('Environment setup, dataset collation & API contracts.', cell_style)],
        [Paragraph('Week 2', cell_style), Paragraph('Supervised Learning & IBM watsonx', cell_style), Paragraph('24-feature extractor, baseline heuristics & classifier benchmarking.', cell_style)],
        [Paragraph('Week 3', cell_style), Paragraph('Unsupervised Patterns & Deep Learning', cell_style), Paragraph('Shannon entropy, homoglyph clustering & GroupShuffle validation.', cell_style)],
        [Paragraph('Week 4', cell_style), Paragraph('Intelligent Agents & Lifelong Skills', cell_style), Paragraph('SHAP XAI engine, watsonx advisory prompt orchestration.', cell_style)],
        [Paragraph('Week 5', cell_style), Paragraph('Project Completion & Q&A', cell_style), Paragraph('FastAPI backend, Cyberpunk UI & ReportLab PDF engine.', cell_style)],
        [Paragraph('Week 6', cell_style), Paragraph('Project Submission (PPT & Code)', cell_style), Paragraph('Live Vercel cloud deployment, automated test verification (8/8).', cell_style)],
    ]
    t_mile = Table(mile_data, colWidths=[0.8*inch, 2.4*inch, 4.1*inch])
    t_mile.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), light_bg),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(t_mile)
    elements.append(Spacer(1, 12))

    # 8. Sign-off & Verification Statement
    elements.append(Paragraph('6. Student Undertaking & Submission Declaration', h2_style))
    elements.append(Paragraph(
        'I hereby declare that this project, <b>PHISHGUARD//NEXUS</b>, has been developed as the final capstone deliverable for the 6-week virtual IBM SkillsBuild Machine Learning and Applied AI Internship (2026) in collaboration with AICTE and BharatCares. The platform is fully operational, publicly hosted at <b>https://phishguard-nexus.vercel.app/</b> (accessible via <b>tinyurl.com/pg-nexus</b>), and backed by a clean version-controlled repository on GitHub.<br/><br/>'
        '<b>Student Signature:</b> <u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sahil Rai&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; '
        '<b>Date of Submission:</b> <u>&nbsp;&nbsp;&nbsp;&nbsp;13/10/2026&nbsp;&nbsp;&nbsp;&nbsp;</u>',
        body_style
    ))

    doc.build(elements)
    print(f"Generated PDF successfully: {output_path}")

if __name__ == "__main__":
    out_file = Path("D:/IBM BOB PROJECT BY SAHIL/PHISHGUARD_NEXUS_CONCEPT_NOTE_AND_LEAN_CANVAS.pdf")
    build_pdf(str(out_file))
