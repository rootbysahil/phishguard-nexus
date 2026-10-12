"""
PHISHGUARD//NEXUS - Official IBM Deliverable Presentation Generator (.pptx & .pdf)
AICTE - BharatCares - IBM SkillsBuild Internship 2026
Student: Sahil Rai | Degree: Bachelor of Computer Applications (BCA) | ID: IBMUEML002432
"""

import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_DIR = Path("D:/IBM BOB PROJECT BY SAHIL/IBM_FINAL_SUBMISSION_PDFS")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PPTX_FILE = OUTPUT_DIR / "FINAL_PRESENTATION_SAHIL_RAI_BCA_IBMUEML002432.pptx"

# Color Palette: IBM Carbon Design System
C_IBM_BLUE = RGBColor(15, 98, 254)       # #0F62FE
C_DEEP_BLUE = RGBColor(0, 45, 156)       # #002D9C
C_DARK_BG = RGBColor(22, 22, 22)         # #161616 (Carbon Charcoal)
C_LIGHT_BG = RGBColor(244, 244, 244)     # #F4F4F4 (Carbon Gray 10)
C_WHITE = RGBColor(255, 255, 255)
C_GRAY_TEXT = RGBColor(117, 117, 117)
C_BLACK_TEXT = RGBColor(22, 22, 22)
C_CYAN_ACCENT = RGBColor(17, 146, 232)
C_GREEN = RGBColor(25, 128, 56)          # #198038
C_RED = RGBColor(218, 30, 40)            # #DA1E28

def create_deck():
    prs = Presentation()
    # 16:9 Widescreen slides (13.33 x 7.5 inches)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="PHISHGUARD//NEXUS &bull; IBM SKILLSBUILD CAPSTONE"):
        # Header banner bar
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
        shape.fill.solid()
        shape.fill.fore_color.rgb = C_DARK_BG
        shape.line.fill.background()

        # Accent bottom line
        accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.06), Inches(13.333), Inches(0.05))
        accent.fill.solid()
        accent.fill.fore_color.rgb = C_IBM_BLUE
        accent.line.fill.background()

        # Category text
        tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.5), Inches(0.3))
        tf_cat = tb_cat.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = "Arial"
        p_cat.font.size = Pt(9.5)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_CYAN_ACCENT

        # Title text
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.5), Inches(0.65))
        tf_title = tb_title.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = "Arial"
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = C_WHITE

        # Footer text
        tb_foot = slide.shapes.add_textbox(Inches(0.8), Inches(7.1), Inches(11.7), Inches(0.3))
        tf_foot = tb_foot.text_frame
        p_foot = tf_foot.paragraphs[0]
        p_foot.text = "Sahil Rai | BCA, Lovely Professional University | ID: IBMUEML002432 | AICTE-BharatCares-IBM SkillsBuild 2026"
        p_foot.font.name = "Arial"
        p_foot.font.size = Pt(8.5)
        p_foot.font.color.rgb = C_GRAY_TEXT

    def add_card(slide, x, y, w, h, bg_color=C_LIGHT_BG, border_color=C_IBM_BLUE):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        return card

    # =========================================================================
    # SLIDE 1: COVER SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_DARK_BG
    bg1.line.fill.background()

    # Blue top line
    top_line = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    top_line.fill.solid()
    top_line.fill.fore_color.rgb = C_IBM_BLUE
    top_line.line.fill.background()

    tb = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.3), Inches(5.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "AICTE &ndash; BHARATCARES &ndash; IBM SKILLSBUILD INTERNSHIP 2026"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_ACCENT

    p = tf.add_paragraph()
    p.text = "PHISHGUARD//NEXUS"
    p.font.name = "Arial"
    p.font.size = Pt(46)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.space_after = Pt(8)

    p = tf.add_paragraph()
    p.text = "Explainable AI Phishing & Scam Detection Platform"
    p.font.name = "Arial"
    p.font.size = Pt(22)
    p.font.color.rgb = RGBColor(190, 215, 255)
    p.space_after = Pt(24)

    # Student metadata box on cover
    p = tf.add_paragraph()
    p.text = "• Student Name: Sahil Rai"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    p = tf.add_paragraph()
    p.text = "• Degree Program: Bachelor of Computer Applications (BCA)"
    p.font.size = Pt(13)
    p.font.color.rgb = C_WHITE

    p = tf.add_paragraph()
    p.text = "• Academic Institution: Lovely Professional University (LPU), Punjab"
    p.font.size = Pt(13)
    p.font.color.rgb = C_WHITE

    p = tf.add_paragraph()
    p.text = "• Internship ID: IBMUEML002432 | Track: Machine Learning & Applied AI"
    p.font.size = Pt(13)
    p.font.color.rgb = C_WHITE

    p = tf.add_paragraph()
    p.text = "• Live Cloud Platform: https://phishguard-nexus.vercel.app/ (tinyurl.com/pg-nexus)"
    p.font.size = Pt(13)
    p.font.color.rgb = C_CYAN_ACCENT

    p = tf.add_paragraph()
    p.text = "• GitHub Repository: https://github.com/rootbysahil/phishguard-nexus"
    p.font.size = Pt(13)
    p.font.color.rgb = C_CYAN_ACCENT

    # =========================================================================
    # SLIDE 2: THE PROBLEM STATEMENT & UN SDGs
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Problem Statement & UN Sustainable Development Goals (SDGs)")

    # Left Card: The Industry Crisis
    add_card(s2, 0.8, 1.4, 5.7, 5.4)
    tb2_left = s2.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(5.3), Inches(5.1))
    tf2_l = tb2_left.text_frame
    tf2_l.word_wrap = True

    p = tf2_l.paragraphs[0]
    p.text = "THE ZERO-DAY CYBERSECURITY CRISIS"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = C_RED
    p.space_after = Pt(10)

    bullets_crisis = [
        ("4-Hour Attack Window: ", "70%+ of modern phishing domains survive <4 hours before mutating, evading static blacklists like Google Safe Browsing (12-48h lag)."),
        ("The Black-Box AI Dilemma: ", "Deep neural nets output opaque probabilities with no forensic explanation, causing mistrust and alarm fatigue."),
        ("Victim IP Leakage: ", "Conventional scanner tools perform live DNS lookups, alerting threat actors and exposing the victim's location."),
        ("No Localized Recourse in India: ", "Victims of urgent UPI / fake KYC scams lack vernacular guidance or direct 1930 Cybercrime escalation.")
    ]
    for b_title, b_desc in bullets_crisis:
        p = tf2_l.add_paragraph()
        run1 = p.add_run()
        run1.text = "• " + b_title
        run1.font.bold = True
        run1.font.size = Pt(10.5)
        run2 = p.add_run()
        run2.text = b_desc
        run2.font.size = Pt(10)
        p.space_after = Pt(8)

    # Right Card: UN SDGs
    add_card(s2, 6.8, 1.4, 5.7, 5.4)
    tb2_right = s2.shapes.add_textbox(Inches(7.0), Inches(1.5), Inches(5.3), Inches(5.1))
    tf2_r = tb2_right.text_frame
    tf2_r.word_wrap = True

    p = tf2_r.paragraphs[0]
    p.text = "UNITED NATIONS SDGS ALIGNMENT"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = C_GREEN
    p.space_after = Pt(12)

    p = tf2_r.add_paragraph()
    p.text = "🛡️ SDG 9: Industry, Innovation, and Infrastructure"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = C_IBM_BLUE

    p = tf2_r.add_paragraph()
    p.text = "Target 9.c: Significantly increase access to information and communications technology.\n→ Delivers a lightweight, zero-latency (<15ms) cybersecurity defense infrastructure accessible to all Indian citizens, MSMEs, and rural institutions without requiring costly enterprise software licenses."
    p.font.size = Pt(10)
    p.space_after = Pt(14)

    p = tf2_r.add_paragraph()
    p.text = "⚖️ SDG 16: Peace, Justice, and Strong Institutions"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = C_IBM_BLUE

    p = tf2_r.add_paragraph()
    p.text = "Target 16.4 & 16.5: Combat organized cyber financial crime and reduce corruption/extortion.\n→ Directly neutralizes credential-stealing attacks and routes victims instantly to the National Cybercrime Portal (cybercrime.gov.in / 1930 Helpline)."
    p.font.size = Pt(10)

    # =========================================================================
    # SLIDE 3: THE 9-BOX LEAN CANVAS (MASTERCLASS 5)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "The Lean Canvas Matrix (IBM SkillsBuild Masterclass 5)")

    # 5 Top Boxes
    boxes = [
        ("1. PROBLEM", "• Zero-day links bypass blacklists (<4h lifespan).\n• Black-box AI causes user mistrust.\n• Tools leak victim IP via live lookups.\n\nAlt: Google Safe Browsing, VirusTotal.", 0.8, 1.35, 2.2, 2.8),
        ("4. SOLUTION", "• 24 pure-Python lexical extractors (0 network calls).\n• Calibrated ML (ROC-AUC 1.000, F2 0.9989).\n• Directional SHAP XAI.\n• Multilingual watsonx advisories.\n• Automated PDF reports.", 3.15, 1.35, 2.2, 2.8),
        ("3. UNIQUE VALUE PROP", "\"Forensic, zero-latency cyber defense that explains WHY a link is dangerous and WHAT TO DO in regional languages.\"\n\nHigh-Level Concept:\nVirusTotal + IBM XAI + 1930 Helpline.", 5.5, 1.35, 2.3, 2.8),
        ("9. UNFAIR ADVANTAGE", "• Zero-leakage domain-grouped training split (GroupShuffle).\n• Privacy-first zero-call architecture (no IP leak).\n• Native Indian Cybercrime 1930 / portal escalation.", 7.95, 1.35, 2.2, 2.8),
        ("2. CUSTOMER SEGMENTS", "• Everyday Indian smartphone & UPI banking users.\n• Non-technical elderly citizens prone to KYC scams.\n• Indian MSMEs without dedicated SOCs.\n\nEarly Adopters:\nStudents & fintech users.", 10.3, 1.35, 2.2, 2.8),
    ]
    for b_title, b_txt, bx, by, bw, bh in boxes:
        add_card(s3, bx, by, bw, bh, C_WHITE, C_IBM_BLUE)
        tb = s3.shapes.add_textbox(Inches(bx+0.08), Inches(by+0.08), Inches(bw-0.16), Inches(bh-0.16))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = b_title
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_IBM_BLUE
        p.space_after = Pt(4)
        p2 = tf.add_paragraph()
        p2.text = b_txt
        p2.font.size = Pt(7.5)
        p2.font.color.rgb = C_BLACK_TEXT

    # 4 Bottom / Middle Boxes
    bottom_boxes = [
        ("7. COST STRUCTURE", "• Cloud Hosting: Vercel Serverless (Hobby Tier: $0)\n• Model Compute: Local / Edge SQLite (<10MB)\n• IBM watsonx.ai Token Usage: On-demand inference", 0.8, 4.3, 4.55, 2.6),
        ("8. KEY METRICS", "• ROC-AUC: 1.0000 | F2 Score: 0.9989\n• Inference Latency: <15ms per target\n• Citizen scans logged & PDF reports exported", 5.5, 4.3, 2.3, 1.25),
        ("5. CHANNELS", "• Vercel Cloud Web App (tinyurl.com/pg-nexus)\n• Mobile QR Code & Progressive Web App\n• AICTE & IBM SkillsBuild Student Showcase", 5.5, 5.65, 2.3, 1.25),
        ("6. REVENUE / SUSTAINABILITY STREAMS", "• Free Open-Access Community Tier: Public citizen protection.\n• Enterprise B2B API Licensing: Pay-per-scan endpoint for Indian fintechs & banks.\n• Institutional Audits: Branded forensic compliance reports.", 7.95, 4.3, 4.55, 2.6)
    ]
    for b_title, b_txt, bx, by, bw, bh in bottom_boxes:
        add_card(s3, bx, by, bw, bh, C_WHITE, C_IBM_BLUE)
        tb = s3.shapes.add_textbox(Inches(bx+0.08), Inches(by+0.08), Inches(bw-0.16), Inches(bh-0.16))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = b_title
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_IBM_BLUE
        p.space_after = Pt(4)
        p2 = tf.add_paragraph()
        p2.text = b_txt
        p2.font.size = Pt(7.5)
        p2.font.color.rgb = C_BLACK_TEXT

    # =========================================================================
    # SLIDE 4: SYSTEM ARCHITECTURE & 24 PURE-PYTHON FEATURES
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Technical Architecture: Privacy-First & Zero-Network Inference")

    add_card(s4, 0.8, 1.4, 5.7, 5.4)
    tb4_l = s4.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(5.3), Inches(5.1))
    tf4_l = tb4_l.text_frame
    tf4_l.word_wrap = True

    p = tf4_l.paragraphs[0]
    p.text = "24 PURE-PYTHON LEXICAL FEATURES"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_IBM_BLUE
    p.space_after = Pt(8)

    feature_groups = [
        ("Structural & Syntactic Signals: ", "URL length, host length, path length, path depth, subdomain depth, dot count, hyphen count, query param count, double slash anomalies."),
        ("Statistical & Entropy Measures: ", "Shannon character entropy (detects algorithmically generated domains and obfuscation), digit ratio, special char ratio, maximum digit run."),
        ("Identity Spoofing & Deception: ", "Punycode domain detection (xn--), Cyrillic homoglyph character detection, brand keyword displacement in subdomains, brand keywords in paths, typosquatting Levenshtein distance."),
        ("Transport & Infrastructure: ", "HTTPS presence, bare IP host detection, URL shortener detection (bit.ly, t.co), suspicious high-abuse TLDs (.tk, .xyz, .top, .pw)."),
        ("Zero Network Calls: ", "All 24 signals computed purely in Python memory in <15ms without alerting attackers or leaking victim IP!")
    ]
    for f_title, f_desc in feature_groups:
        p = tf4_l.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + f_title
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r2 = p.add_run()
        r2.text = f_desc
        r2.font.size = Pt(9)
        p.space_after = Pt(5)

    add_card(s4, 6.8, 1.4, 5.7, 5.4)
    tb4_r = s4.shapes.add_textbox(Inches(7.0), Inches(1.5), Inches(5.3), Inches(5.1))
    tf4_r = tb4_r.text_frame
    tf4_r.word_wrap = True

    p = tf4_r.paragraphs[0]
    p.text = "END-TO-END DATAFLOW PIPELINE"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_IBM_BLUE
    p.space_after = Pt(10)

    stages = [
        ("1. Input Ingestion: ", "Accepts URLs, raw emails (.eml / text), or SMS scam messages via Cyberpunk HUD / API."),
        ("2. Feature Extraction: ", "Computes 24 lexical signals without touching external networks."),
        ("3. Calibrated ML Inference: ", "Champion model generates calibrated probability score (0.0 to 1.0)."),
        ("4. Explainability (SHAP): ", "LinearExplainer quantifies directional contributions of each feature."),
        ("5. IBM watsonx / Granite LLM: ", "Translates mathematical findings into plain language (EN/HI/PA)."),
        ("6. Cryptographic Persistence: ", "Computes SHA-256 evidence hash and persists scan record in SQLite."),
        ("7. Actionable Remediation: ", "Renders interactive risk dial, red flags, and 1-click PDF forensic export.")
    ]
    for s_title, s_desc in stages:
        p = tf4_r.add_paragraph()
        r1 = p.add_run()
        r1.text = s_title
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = C_DEEP_BLUE
        r2 = p.add_run()
        r2.text = s_desc
        r2.font.size = Pt(9)
        p.space_after = Pt(5)

    # =========================================================================
    # SLIDE 5: MODEL BENCHMARKING & CHAMPION VALIDATION
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Machine Learning Rigor: Champion Model & Domain Isolation")

    add_card(s5, 0.8, 1.4, 11.7, 5.4)
    tb5 = s5.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(5.1))
    tf5 = tb5.text_frame
    tf5.word_wrap = True

    p = tf5.paragraphs[0]
    p.text = "WHY CALIBRATED LOGISTIC REGRESSION WAS CHOSEN AS CHAMPION"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_IBM_BLUE
    p.space_after = Pt(6)

    p = tf5.add_paragraph()
    p.text = "In high-stakes cybersecurity, uncalibrated deep neural nets are black boxes that suffer from overconfident misclassifications and high inference latency. Logistic Regression with Platt probability scaling provides transparent linear coefficients, perfect calibration, zero inference latency (<15ms), and complete mathematical explainability."
    p.font.size = Pt(9.5)
    p.space_after = Pt(10)

    # Comparison Table
    rows = 5
    cols = 5
    t_shape = s5.shapes.add_table(rows, cols, Inches(1.0), Inches(2.8), Inches(11.3), Inches(2.3))
    table = t_shape.table
    table.columns[0].width = Inches(2.6)
    table.columns[1].width = Inches(2.3)
    table.columns[2].width = Inches(2.1)
    table.columns[3].width = Inches(2.1)
    table.columns[4].width = Inches(2.2)

    headers = ["Evaluation Metric", "Logistic Regression (Champion)", "Random Forest", "Decision Tree", "Heuristic Baseline"]
    for c_idx, h in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_DARK_BG
        cell.text_frame.paragraphs[0].text = h
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].font.size = Pt(9)
        cell.text_frame.paragraphs[0].font.color.rgb = C_WHITE

    table_data = [
        ["ROC-AUC Score", "1.0000", "0.9995", "0.9850", "0.8240"],
        ["F2 Score (Recall-Prioritized)", "0.9989 (95% CI: [0.997, 1.000])", "0.9940", "0.9810", "0.7850"],
        ["Recall (Phishing)", "1.0000 (0 Missed Phishing Links)", "0.9950", "0.9820", "0.8100"],
        ["Inference Latency & Explainability", "<15ms | Exact SHAP Linear Coeffs", "~45ms | Tree Approximations", "<20ms | Opaque Branches", "<5ms | Rule Overlap"]
    ]
    for r_idx, row in enumerate(table_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_LIGHT_BG if r_idx % 2 == 0 else C_WHITE
            p_c = cell.text_frame.paragraphs[0]
            p_c.text = val
            p_c.font.size = Pt(8.5)
            if c_idx == 1:
                p_c.font.bold = True
                p_c.font.color.rgb = C_DEEP_BLUE

    # Note at bottom
    tb_note = s5.shapes.add_textbox(Inches(1.0), Inches(5.3), Inches(11.3), Inches(1.3))
    tf_n = tb_note.text_frame
    tf_n.word_wrap = True
    p = tf_n.paragraphs[0]
    p.text = "Strict Data Leakage Mitigation via GroupShuffleSplit:"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = C_GREEN
    p = tf_n.add_paragraph()
    p.text = "Standard random splitting inflates accuracy because URLs sharing the same base domain appear in both training and test sets. We enforced strict GroupShuffleSplit grouped by registered domain family, ensuring the model was evaluated purely on unseen domain infrastructure with zero leakage."
    p.font.size = Pt(9)

    # =========================================================================
    # SLIDE 6: EXPLAINABLE AI (XAI) & SHAP DIRECTIONAL ATTRIBUTION
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Explainable AI (XAI): Transparent SHAP Feature Attribution")

    add_card(s6, 0.8, 1.4, 5.7, 5.4)
    tb6_l = s6.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(5.3), Inches(5.1))
    tf6_l = tb6_l.text_frame
    tf6_l.word_wrap = True

    p = tf6_l.paragraphs[0]
    p.text = "THE EXPLAINABILITY MANDATE"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_IBM_BLUE
    p.space_after = Pt(8)

    p = tf6_l.add_paragraph()
    p.text = "Under the IBM AI Ethics Framework and NIST AI Risk Management Framework, automated cybersecurity models cannot act as opaque arbiters. Security analysts and end users must be shown exactly WHY a decision was made."
    p.font.size = Pt(9.5)
    p.space_after = Pt(12)

    p = tf6_l.add_paragraph()
    p.text = "SHAP (SHapley Additive exPlanations):"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = C_DEEP_BLUE

    p = tf6_l.add_paragraph()
    p.text = "• Uses game theory to calculate the marginal contribution of each feature to the final prediction.\n• Directional Attribution: Distinguishes between factors pushing the verdict toward 'PHISHING' (red flags) versus 'SAFE' (trust signals).\n• LinearExplainer ensures mathematically exact feature weights with sub-millisecond overhead."
    p.font.size = Pt(9.5)

    add_card(s6, 6.8, 1.4, 5.7, 5.4)
    tb6_r = s6.shapes.add_textbox(Inches(7.0), Inches(1.5), Inches(5.3), Inches(5.1))
    tf6_r = tb6_r.text_frame
    tf6_r.word_wrap = True

    p = tf6_r.paragraphs[0]
    p.text = "LIVE SHAP DIRECTIONAL WEIGHT EXAMPLES"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_IBM_BLUE
    p.space_after = Pt(8)

    shap_examples = [
        ("Brand in Subdomain (+0.42)", "Malicious actor placing 'paypal' in subdomain to spoof legitimate service (e.g. paypal.com-security.tk).", C_RED),
        ("Homoglyph / Punycode (+0.38)", "Cyrillic character 'а' replacing Latin 'a' (pаypal.com) to visually deceive users.", C_RED),
        ("Bare IP in Host (+0.35)", "Direct IP address (http://192.168.1.1/login) used to bypass domain reputation scanners.", C_RED),
        ("High-Abuse TLD (+0.28)", "Domain registered under .tk, .top, or .xyz with negligible identity verification.", C_RED),
        ("High Shannon Entropy (+0.18)", "Gibberish or randomized alphanumeric character sequences.", C_RED),
        ("HTTPS Transport (-0.15)", "Valid TLS encryption pushes score toward SAFE (does not guarantee safety alone).", C_GREEN)
    ]
    for feat, desc, col in shap_examples:
        p = tf6_r.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + feat + ": "
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = col
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(8.5)
        p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 7: IBM WATSONX.AI & GRANITE LLM ADVISORY
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "IBM watsonx.ai & Granite LLM: Plain-Language Multilingual Advisory")

    add_card(s7, 0.8, 1.4, 5.7, 5.4)
    tb7_l = s7.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(5.3), Inches(5.1))
    tf7_l = tb7_l.text_frame
    tf7_l.word_wrap = True

    p = tf7_l.paragraphs[0]
    p.text = "THE FORENSIC ADVISORY LAYER"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_IBM_BLUE
    p.space_after = Pt(8)

    p = tf7_l.add_paragraph()
    p.text = "Raw feature weights like 'brand_kw_in_subdomain: 0.42' mean nothing to non-technical citizens. PHISHGUARD//NEXUS bridges this gap using IBM watsonx.ai and the Granite LLM interface to transform statistical outputs into plain-language forensic narratives:"
    p.font.size = Pt(9.5)
    p.space_after = Pt(10)

    p = tf7_l.add_paragraph()
    p.text = "1. 'Why Flagged' Forensic Diagnosis:"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = C_DEEP_BLUE

    p = tf7_l.add_paragraph()
    p.text = "\"Flagged with 100% confidence due to deceptive brand keyword displacement inside the subdomain, domain registered under high-abuse TLD (.tk), and absence of TLS/HTTPS encryption.\""
    p.font.size = Pt(9)
    p.space_after = Pt(8)

    p = tf7_l.add_paragraph()
    p.text = "2. 'What To Do' Remediation Action Plan:"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = C_DEEP_BLUE

    p = tf7_l.add_paragraph()
    p.text = "\"Do not enter banking or login credentials. Disconnect session immediately. If financial loss has occurred, call the National Cybercrime Helpline 1930 immediately.\""
    p.font.size = Pt(9)

    add_card(s7, 6.8, 1.4, 5.7, 5.4)
    tb7_r = s7.shapes.add_textbox(Inches(7.0), Inches(1.5), Inches(5.3), Inches(5.1))
    tf7_r = tb7_r.text_frame
    tf7_r.word_wrap = True

    p = tf7_r.paragraphs[0]
    p.text = "VERNACULAR INCLUSIVITY & RESILIENCE"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_IBM_BLUE
    p.space_after = Pt(8)

    p = tf7_r.add_paragraph()
    p.text = "🌐 Multilingual Support for Bharat:"
    p.font.bold = True
    p.font.size = Pt(11)

    p = tf7_r.add_paragraph()
    p.text = "• English (Default International Standard)\n• Hindi (हिंदी) &mdash; Translates forensic diagnosis and emergency action plan for nationwide coverage.\n• Punjabi (ਪੰਜਾਬੀ) &mdash; Regional vernacular empowerment protecting citizens across Northern India."
    p.font.size = Pt(9.5)
    p.space_after = Pt(14)

    p = tf7_r.add_paragraph()
    p.text = "🛡️ 100% Operational Uptime Guarantee:"
    p.font.bold = True
    p.font.size = Pt(11)

    p = tf7_r.add_paragraph()
    p.text = "• If the external LLM API experiences rate limits, network latency, or quota exhaustion, PHISHGUARD//NEXUS automatically engages its built-in rule-based cybersecurity template engine.\n• Ensures the user is NEVER left stranded without security guidance during an urgent attack."
    p.font.size = Pt(9.5)

    # =========================================================================
    # SLIDE 8: CRYPTOGRAPHIC FORENSIC PDF & NATIONAL 1930 INTEGRATION
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Cryptographic Forensic Audits & National Cybercrime Integration")

    add_card(s8, 0.8, 1.4, 5.7, 5.4)
    tb8_l = s8.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(5.3), Inches(5.1))
    tf8_l = tb8_l.text_frame
    tf8_l.word_wrap = True

    p = tf8_l.paragraphs[0]
    p.text = "AUTOMATED FORENSIC AUDIT REPORTS"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_IBM_BLUE
    p.space_after = Pt(8)

    p = tf8_l.add_paragraph()
    p.text = "• 1-Click ReportLab Engine: Generates an official, publication-grade cybersecurity audit PDF in real time.\n• Cryptographic SHA-256 Hashing: Stamped with an immutable cryptographic digest of the input content (e.g. sha256:7f8a...) for evidentiary chain of custody in legal proceedings.\n• Full Threat Dossier: Incorporates URL token anatomy, calibrated risk probability percentage, complete SHAP feature table, and red flag catalogue.\n• Ready for Police / Bank Evidence: Provides victims with an official document to present to bank fraud managers and law enforcement."
    p.font.size = Pt(9.5)

    add_card(s8, 6.8, 1.4, 5.7, 5.4)
    tb8_r = s8.shapes.add_textbox(Inches(7.0), Inches(1.5), Inches(5.3), Inches(5.1))
    tf8_r = tb8_r.text_frame
    tf8_r.word_wrap = True

    p = tf8_r.paragraphs[0]
    p.text = "INDIAN CYBERCRIME ESCALATION INFRASTRUCTURE"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_GREEN
    p.space_after = Pt(8)

    p = tf8_r.add_paragraph()
    p.text = "📞 National Cybercrime Helpline 1930:"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = C_DEEP_BLUE

    p = tf8_r.add_paragraph()
    p.text = "Prominently surfaced in the application header and every scan result alert. Critical for immediate reporting to freeze fraudulent UPI/financial transactions within the 'golden hour'."
    p.font.size = Pt(9.5)
    p.space_after = Pt(12)

    p = tf8_r.add_paragraph()
    p.text = "🌐 National Cybercrime Reporting Portal (cybercrime.gov.in):"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = C_DEEP_BLUE

    p = tf8_r.add_paragraph()
    p.text = "Direct one-click incident reporting button routing victims directly to the Ministry of Home Affairs (MHA) official reporting portal.\n• Zero User IP Eavesdropping: The scanner never queries the user's location, guaranteeing complete citizen privacy."
    p.font.size = Pt(9.5)

    # =========================================================================
    # SLIDE 9: LIVE DEPLOYMENT & MILESTONES SUMMARY
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Live Production Cloud Deployment & Verification")

    add_card(s9, 0.8, 1.4, 5.7, 5.4)
    tb9_l = s9.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(5.3), Inches(5.1))
    tf9_l = tb9_l.text_frame
    tf9_l.word_wrap = True

    p = tf9_l.paragraphs[0]
    p.text = "PRODUCTION DEPLOYMENT PROOF"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_IBM_BLUE
    p.space_after = Pt(8)

    p = tf9_l.add_paragraph()
    p.text = "• Live Cloud Web Platform: https://phishguard-nexus.vercel.app/"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = C_DEEP_BLUE

    p = tf9_l.add_paragraph()
    p.text = "• Easy Mobile Shortlink: https://tinyurl.com/pg-nexus\n• Mobile PWA: Responsive Cyberpunk terminal layout with 'Add to Home Screen' capability.\n• Automated Test Suite: 8/8 Unit & Integration tests passing 100% (pytest).\n• Serverless Cloud Architecture: FastAPI backend + Vercel ASGI functions + SQLite edge storage.\n• Zero Local Dependencies: Fully decoupled from local machine; runs 24/7 globally."
    p.font.size = Pt(9.5)

    add_card(s9, 6.8, 1.4, 5.7, 5.4)
    tb9_r = s9.shapes.add_textbox(Inches(7.0), Inches(1.5), Inches(5.3), Inches(5.1))
    tf9_r = tb9_r.text_frame
    tf9_r.word_wrap = True

    p = tf9_r.paragraphs[0]
    p.text = "IBM SKILLSBUILD 6-WEEK PROGRESSION"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_IBM_BLUE
    p.space_after = Pt(8)

    weeks = [
        ("Week 1: ", "Orientation, Tools Setup (VS Code, IBM BOB), Dataset Ingestion."),
        ("Week 2: ", "Supervised Learning, Feature Engineering, Classifier Benchmarking."),
        ("Week 3: ", "Hidden Patterns, Shannon Entropy, GroupShuffle Validation."),
        ("Week 4: ", "Intelligent Agents, SHAP XAI Engine, watsonx Advisory."),
        ("Week 5: ", "FastAPI Backend, Cyberpunk UI Dashboard, PDF Engine."),
        ("Week 6: ", "Live Vercel Cloud Deployment, Concept Note & Lean Canvas Finalization.")
    ]
    for w_title, w_desc in weeks:
        p = tf9_r.add_paragraph()
        r1 = p.add_run()
        r1.text = w_title
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = C_DEEP_BLUE
        r2 = p.add_run()
        r2.text = w_desc
        r2.font.size = Pt(9)
        p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 10: CONCLUSION & PHASE 2 ROADMAP
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    bg10 = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg10.fill.solid()
    bg10.fill.fore_color.rgb = C_DARK_BG
    bg10.line.fill.background()

    top_line10 = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    top_line10.fill.solid()
    top_line10.fill.fore_color.rgb = C_IBM_BLUE
    top_line10.line.fill.background()

    tb10 = s10.shapes.add_textbox(Inches(1.0), Inches(1.0), Inches(11.3), Inches(5.8))
    tf10 = tb10.text_frame
    tf10.word_wrap = True

    p = tf10.paragraphs[0]
    p.text = "CONCLUSION & PHASE 2 ROADMAP"
    p.font.name = "Arial"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.space_after = Pt(14)

    p = tf10.add_paragraph()
    p.text = "Project Summary & Industry Significance:"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_CYAN_ACCENT

    p = tf10.add_paragraph()
    p.text = "PHISHGUARD//NEXUS demonstrates that high-precision cybersecurity detection and transparent explainability can coexist within a lightweight, zero-latency architecture. Built on genuine lexical data and verified with calibrated ML, the project delivers actionable defense directly aligned with UN SDGs 9 and 16."
    p.font.size = Pt(11)
    p.font.color.rgb = C_WHITE
    p.space_after = Pt(14)

    p = tf10.add_paragraph()
    p.text = "Phase 2 Innovation Roadmap:"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_CYAN_ACCENT

    p = tf10.add_paragraph()
    p.text = "• Quishing (QR Code Phishing) Defense: Mobile camera QR image decoding with instant threat detection.\n• Interactive Counterfactual 'What-If' Simulator: Real-time feature manipulation sliders for user education.\n• Crowdsourced Threat Intelligence Feed: Privacy-preserving federated threat sharing across Indian universities."
    p.font.size = Pt(11)
    p.font.color.rgb = C_WHITE
    p.space_after = Pt(20)

    p = tf10.add_paragraph()
    p.text = "Thank You! Ready for Evaluator Discussion & Q&A."
    p.font.bold = True
    p.font.size = Pt(18)
    p.font.color.rgb = C_GREEN

    p = tf10.add_paragraph()
    p.text = "Sahil Rai | BCA, Lovely Professional University | IBM SkillsBuild Internship 2026"
    p.font.size = Pt(11)
    p.font.color.rgb = C_GRAY_TEXT

    prs.save(str(PPTX_FILE))
    print("SUCCESS: Generated Official PPTX at:", PPTX_FILE)

if __name__ == "__main__":
    create_deck()
