"""
PHISHGUARD//NEXUS - Combined Concept Note with Lean Canvas PDF Generator
AICTE - BharatCares - IBM SkillsBuild Internship 2026
Student: Sahil Rai | Degree: Bachelor of Computer Applications (BCA) | ID: IBMUEML002432
"""

from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

def build_combined_pdf():
    pdf_path = "D:/IBM BOB PROJECT BY SAHIL/IBM_FINAL_SUBMISSION_PDFS/CONCEPT_NOTE_WITH_LEAN_CANVAS_SAHIL_RAI_BCA_IBMUEML002432.pdf"

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=32,
        rightMargin=32,
        topMargin=26,
        bottomMargin=26
    )

    IBM_BLUE = colors.HexColor('#0F62FE')
    CHARCOAL = colors.HexColor('#161616')
    LIGHT_BG = colors.HexColor('#F4F4F4')
    BORDER_COLOR = colors.HexColor('#D0D0D0')

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=15, leading=19, textColor=IBM_BLUE, alignment=1)
    sub_style = ParagraphStyle('Sub', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=11.5, textColor=colors.HexColor('#525252'), alignment=1)
    h2_style = ParagraphStyle('H2', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=10.5, leading=13.5, textColor=CHARCOAL, spaceBefore=4, spaceAfter=2)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=7.8, leading=10.8, textColor=CHARCOAL)
    cell_style = ParagraphStyle('Cell', parent=styles['Normal'], fontName='Helvetica', fontSize=7.2, leading=9.5, textColor=CHARCOAL)
    cell_header = ParagraphStyle('CellHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.5, leading=10, textColor=IBM_BLUE)

    elements = []

    # ==========================
    # PAGE 1: CONCEPT NOTE & LEAN CANVAS
    # ==========================
    elements.append(Paragraph('AICTE &ndash; BharatCares &ndash; IBM SkillsBuild Machine Learning and Applied AI Internship 2026', sub_style))
    elements.append(Paragraph('PROJECT CONCEPT NOTE &amp; LEAN CANVAS', title_style))
    elements.append(Paragraph('Capstone Project Final Submission | Masterclass 5 Framework', sub_style))
    elements.append(Spacer(1, 4))

    meta_data = [
        [Paragraph('<b>Project Title:</b>', cell_style), Paragraph('PHISHGUARD//NEXUS: Explainable AI Phishing &amp; Scam Detection Platform', cell_style)],
        [Paragraph('<b>Student Name:</b>', cell_style), Paragraph('Sahil Rai &nbsp;&nbsp;|&nbsp;&nbsp; <b>Degree Program:</b> Bachelor of Computer Applications (BCA)', cell_style)],
        [Paragraph('<b>Internship ID:</b>', cell_style), Paragraph('IBMUEML002432 &nbsp;&nbsp;|&nbsp;&nbsp; <b>Institution:</b> Lovely Professional University (LPU), Punjab', cell_style)],
        [Paragraph('<b>Live Cloud URL:</b>', cell_style), Paragraph('https://phishguard-nexus.vercel.app/ &nbsp;(Shortlink: tinyurl.com/pg-nexus)', cell_style)],
        [Paragraph('<b>GitHub Repository:</b>', cell_style), Paragraph('https://github.com/rootbysahil/phishguard-nexus', cell_style)],
    ]
    t_meta = Table(meta_data, colWidths=[1.4*inch, 6.0*inch])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(t_meta)
    elements.append(Spacer(1, 5))

    # 1. Executive Summary & UN SDG
    elements.append(Paragraph('1. Executive Summary &amp; UN Sustainable Development Goals (SDGs)', h2_style))
    elements.append(Paragraph(
        '<b>PHISHGUARD//NEXUS</b> is an Explainable AI (XAI) cybersecurity system engineered to detect zero-day phishing across URLs, emails, and SMS without external network lookups. Operating on 24 pure-Python lexical signals and a calibrated Logistic Regression classifier (ROC-AUC: 1.000, F2: 0.9989), it integrates directional SHAP feature attributions, IBM watsonx / Granite LLM multilingual advisories, and direct integration with India\'s National Cybercrime infrastructure (Helpline 1930 / cybercrime.gov.in).<br/>'
        '&bull; <b>UN SDG 9 (Target 9.c):</b> Equitable, zero-latency phishing defense infrastructure accessible to Indian citizens, MSMEs, and educational bodies.<br/>'
        '&bull; <b>UN SDG 16 (Target 16.4):</b> Actively counters financial cybercrime, identity harvesting, and digital extortion.',
        body_style
    ))
    elements.append(Spacer(1, 5))

    # 2. Problem Statement
    elements.append(Paragraph('2. Problem Statement &amp; Critical Industry Inefficiencies', h2_style))
    elements.append(Paragraph(
        '<b>1. Lagged Static Blacklists:</b> 70%+ of phishing attacks expire within 4 hours; static feeds like Google Safe Browsing lag by 12&ndash;48 hours.<br/>'
        '<b>2. Black-Box Neural Networks:</b> Deep learning models output raw probabilities without actionable forensic explanations, causing user distrust.<br/>'
        '<b>3. Privacy Leakage &amp; Latency:</b> Standard scanners perform live DNS/HTTP queries, alerting attackers and exposing victim IP addresses.<br/>'
        '<b>4. Lack of Vernacular Recourse:</b> Non-technical citizens lack guidance in regional languages (Hindi, Punjabi) or immediate emergency escalation.',
        body_style
    ))
    elements.append(Spacer(1, 5))

    # 3. Lean Canvas Matrix
    elements.append(Paragraph('3. The Lean Canvas (9-Box Business &amp; Technical Framework)', h2_style))

    b_prob = Paragraph('<b>1. PROBLEM</b><br/>&bull; Zero-day links bypass blacklists (&lt;4h lifespan).<br/>&bull; Black-box AI causes mistrust.<br/>&bull; Tools leak victim IP via live lookups.<br/><br/><i>Existing Alternatives:</i><br/>VirusTotal, Google Safe Browsing.', cell_style)
    b_sol = Paragraph('<b>4. SOLUTION</b><br/>&bull; 24 pure-Python lexical features (0 network calls).<br/>&bull; Calibrated ML (ROC-AUC 1.000, F2 0.9989).<br/>&bull; Directional SHAP XAI.<br/>&bull; Multilingual watsonx advisories.<br/>&bull; Automated forensic PDF reports.', cell_style)
    b_uvp = Paragraph('<b>3. UNIQUE VALUE PROP</b><br/><b>Core Message:</b><br/>\"Forensic, zero-latency defense that explains WHY a link is dangerous and WHAT TO DO in regional languages.\"<br/><br/><b>High-Level Concept:</b><br/>VirusTotal + IBM XAI + 1930 Helpline.', cell_style)
    b_adv = Paragraph('<b>9. UNFAIR ADVANTAGE</b><br/>&bull; Zero-leakage domain-grouped training split.<br/>&bull; Privacy-first zero-call architecture.<br/>&bull; Native Indian Cybercrime 1930 / portal escalation.', cell_style)
    b_cust = Paragraph('<b>2. CUSTOMER SEGMENTS</b><br/>&bull; Everyday Indian mobile &amp; UPI banking users.<br/>&bull; Elderly citizens prone to KYC scams.<br/>&bull; MSMEs without dedicated SOCs.<br/><br/><i>Early Adopters:</i><br/>University students &amp; fintech users.', cell_style)
    b_met = Paragraph('<b>8. KEY METRICS</b><br/>&bull; ROC-AUC (1.000) &amp; F2 (0.9989)<br/>&bull; Latency (&lt;15ms)<br/>&bull; Citizen scans logged &amp; PDF audits generated', cell_style)
    b_chan = Paragraph('<b>5. CHANNELS</b><br/>&bull; Vercel Web App (tinyurl.com/pg-nexus)<br/>&bull; Mobile QR Code &amp; PWA<br/>&bull; AICTE &amp; IBM SkillsBuild Showcase', cell_style)
    b_cost = Paragraph('<b>7. COST STRUCTURE</b><br/>&bull; Vercel Serverless Hosting ($0 Hobby)<br/>&bull; Model Compute: Local / Edge SQLite<br/>&bull; IBM watsonx.ai Token Usage', cell_style)
    b_rev = Paragraph('<b>6. REVENUE / SUSTAINABILITY STREAMS</b><br/>&bull; Free Community Tier: Public citizen protection<br/>&bull; Enterprise B2B API: Pay-per-scan endpoint for Indian fintechs &amp; banks<br/>&bull; Institutional Audits: Branded forensic compliance reports', cell_style)

    canvas_grid = [
        [b_prob, b_sol, b_uvp, b_adv, b_cust],
        ['', b_met, '', b_chan, ''],
        [b_cost, '', b_rev, '', '']
    ]
    t_canvas = Table(canvas_grid, colWidths=[1.48*inch, 1.48*inch, 1.48*inch, 1.48*inch, 1.48*inch])
    t_canvas.setStyle(TableStyle([
        ('SPAN', (0,0), (0,1)),
        ('SPAN', (2,0), (2,1)),
        ('SPAN', (4,0), (4,1)),
        ('SPAN', (0,2), (1,2)),
        ('SPAN', (2,2), (4,2)),
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('GRID', (0,0), (-1,-1), 0.6, IBM_BLUE),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    elements.append(t_canvas)

    # ==========================
    # PAGE 2: ARCHITECTURE, MILESTONES & BENCHMARKS
    # ==========================
    elements.append(PageBreak())

    elements.append(Paragraph('4. Machine Learning &amp; Applied AI Architecture', h2_style))
    elements.append(Paragraph(
        '&bull; <b>Zero-Network Feature Extraction:</b> Evaluates 24 lexical, syntactic, and structural signals (Shannon entropy, Punycode/homoglyph detection, brand keyword displacement in subdomains, path depth, TLD risk analysis) with 0 network calls, ensuring zero latency and zero victim IP exposure.<br/>'
        '&bull; <b>Champion Classifier:</b> Calibrated Logistic Regression using Platt probability scaling, mitigating path-length bias with balanced benign samples.<br/>'
        '&bull; <b>Validation Rigor:</b> Strict GroupShuffleSplit on registered domains; zero test-train domain leakage.<br/>'
        '&bull; <b>Explainability (XAI):</b> LinearExplainer assigning directional weights to 24 features (entropy, brand displacement, homoglyphs).<br/>'
        '&bull; <b>IBM watsonx.ai Integration:</b> Synthesizes forensic findings into plain language and powers regional translations (English, Hindi, Punjabi).<br/>'
        '&bull; <b>Automated Forensic PDF:</b> Real-time audit generation stamped with SHA-256 cryptographic verification.',
        body_style
    ))
    elements.append(Spacer(1, 6))

    elements.append(Paragraph('5. IBM SkillsBuild 6-Week Masterclass Milestones Alignment', h2_style))
    mile_data = [
        [Paragraph('<b>Week</b>', cell_header), Paragraph('<b>SkillsBuild Masterclass</b>', cell_header), Paragraph('<b>Project Accomplishment Executed</b>', cell_header)],
        [Paragraph('Week 1', cell_style), Paragraph('Kickstart ML &amp; Tools (VS Code, BOB)', cell_style), Paragraph('Environment setup, dataset collation &amp; API contracts.', cell_style)],
        [Paragraph('Week 2', cell_style), Paragraph('Supervised Learning &amp; IBM watsonx', cell_style), Paragraph('24-feature extractor, baseline heuristics &amp; classifier benchmarking.', cell_style)],
        [Paragraph('Week 3', cell_style), Paragraph('Unsupervised Patterns &amp; Deep Learning', cell_style), Paragraph('Shannon entropy, homoglyph clustering &amp; GroupShuffle validation.', cell_style)],
        [Paragraph('Week 4', cell_style), Paragraph('Intelligent Agents &amp; Lifelong Skills', cell_style), Paragraph('SHAP XAI engine, watsonx advisory prompt orchestration.', cell_style)],
        [Paragraph('Week 5', cell_style), Paragraph('Project Completion &amp; Q&amp;A', cell_style), Paragraph('FastAPI backend, Cyberpunk UI &amp; ReportLab PDF engine.', cell_style)],
        [Paragraph('Week 6', cell_style), Paragraph('Project Submission (PPT &amp; Code)', cell_style), Paragraph('Live Vercel cloud deployment, automated test verification (8/8).', cell_style)],
    ]
    t_mile = Table(mile_data, colWidths=[0.8*inch, 2.4*inch, 4.2*inch])
    t_mile.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(t_mile)
    elements.append(Spacer(1, 6))

    elements.append(Paragraph('6. Performance Evaluation &amp; Champion Model Benchmark', h2_style))
    perf_data = [
        [Paragraph('<b>Metric</b>', cell_header), Paragraph('<b>Logistic Regression (Champion)</b>', cell_header), Paragraph('<b>Random Forest</b>', cell_header), Paragraph('<b>Decision Tree</b>', cell_header)],
        [Paragraph('ROC-AUC Score', cell_style), Paragraph('<b>1.0000</b>', cell_style), Paragraph('0.9995', cell_style), Paragraph('0.9850', cell_style)],
        [Paragraph('F2 Score (Recall-Weighted)', cell_style), Paragraph('<b>0.9989</b> [0.997, 1.000]', cell_style), Paragraph('0.9940', cell_style), Paragraph('0.9810', cell_style)],
        [Paragraph('Recall (Phishing)', cell_style), Paragraph('<b>1.0000</b> (0 Missed)', cell_style), Paragraph('0.9950', cell_style), Paragraph('0.9820', cell_style)],
        [Paragraph('Inference Latency', cell_style), Paragraph('<b>&lt;15ms</b>', cell_style), Paragraph('~45ms', cell_style), Paragraph('&lt;20ms', cell_style)],
        [Paragraph('Explainability', cell_style), Paragraph('<b>Exact SHAP Linear Coefficients</b>', cell_style), Paragraph('Tree approximations', cell_style), Paragraph('Opaque branches', cell_style)],
    ]
    t_perf = Table(perf_data, colWidths=[1.8*inch, 2.1*inch, 1.7*inch, 1.8*inch])
    t_perf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(t_perf)
    elements.append(Spacer(1, 8))

    elements.append(Paragraph('7. Student Undertaking &amp; Submission Declaration', h2_style))
    elements.append(Paragraph(
        'I hereby declare that this project, <b>PHISHGUARD//NEXUS</b>, has been developed as the final capstone deliverable for the 6-week virtual IBM SkillsBuild Machine Learning and Applied AI Internship (2026) in collaboration with AICTE and BharatCares. The platform is fully operational, publicly hosted at <b>https://phishguard-nexus.vercel.app/</b> (accessible via <b>tinyurl.com/pg-nexus</b>), and backed by a clean version-controlled repository on GitHub.<br/><br/>'
        '<b>Student Name:</b> Sahil Rai &nbsp;&nbsp;|&nbsp;&nbsp; <b>Degree:</b> Bachelor of Computer Applications (BCA)<br/>'
        '<b>Internship ID:</b> IBMUEML002432 &nbsp;&nbsp;|&nbsp;&nbsp; <b>Institution:</b> Lovely Professional University (LPU), Punjab<br/>'
        '<b>Student Signature:</b> <u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sahil Rai&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; '
        '<b>Date of Submission:</b> <u>&nbsp;&nbsp;&nbsp;&nbsp;13/10/2026&nbsp;&nbsp;&nbsp;&nbsp;</u>',
        body_style
    ))

    doc.build(elements)
    print("SUCCESS: Generated unified Concept Note + Lean Canvas PDF at:", pdf_path)

if __name__ == "__main__":
    build_combined_pdf()
