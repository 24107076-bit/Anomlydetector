import streamlit as st
import google.generativeai as genai
import json
import pandas as pd
import plotly.express as px
from PIL import Image

# ==========================================
# 1. Page Configuration & Custom CSS
# ==========================================
st.set_page_config(page_title="AI Investigator Pro", page_icon="🕵️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ═══════════════════════════════════════
       GLOBAL & BACKGROUND
    ═══════════════════════════════════════ */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
    }

    /* Deep midnight background with an indigo radial glow at center */
    .stApp {
        background:
            radial-gradient(ellipse 80% 60% at 50% 0%,   rgba(79,70,229,0.18) 0%, transparent 70%),
            radial-gradient(ellipse 60% 40% at 80% 80%,  rgba(124,58,237,0.10) 0%, transparent 60%),
            radial-gradient(ellipse 50% 30% at 10% 60%,  rgba(6,182,212,0.07)  0%, transparent 60%),
            linear-gradient(160deg, #080c18 0%, #0c1025 50%, #080b16 100%) !important;
        background-attachment: fixed !important;
    }

    /* Header bar */
    [data-testid="stHeader"] {
        background: rgba(8,12,24,0.85) !important;
        backdrop-filter: blur(20px) !important;
        border-bottom: 1px solid rgba(79,70,229,0.2) !important;
    }

    /* Main content area */
    .main .block-container {
        background: transparent !important;
        padding-top: 2rem !important;
    }

    /* ═══════════════════════════════════════
       SIDEBAR
    ═══════════════════════════════════════ */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1128 0%, #0a0e1f 100%) !important;
        border-right: 1px solid rgba(79,70,229,0.25) !important;
        box-shadow: 4px 0 24px rgba(0,0,0,0.4) !important;
    }
    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 3px; height: 100%;
        background: linear-gradient(180deg, #4f46e5, #7c3aed, #06b6d4);
        border-radius: 0 2px 2px 0;
    }
    [data-testid="stSidebar"] * {
        color: #cbd5e1 !important;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #f1f5f9 !important;
        font-weight: 700 !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        padding: 8px 12px !important;
        border-radius: 8px !important;
        transition: background 0.2s;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: rgba(79,70,229,0.15) !important;
    }

    /* ═══════════════════════════════════════
       TYPOGRAPHY
    ═══════════════════════════════════════ */
    h1, h2, h3 {
        letter-spacing: -0.02em !important;
    }
    h1 {
        font-size: 2.4rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #e2e8f0 0%, #a5b4fc 50%, #818cf8 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }
    h2, h3, h4 {
        color: #e2e8f0 !important;
        font-weight: 700 !important;
    }
    p, span, label, div {
        color: #94a3b8;
    }

    /* ═══════════════════════════════════════
       METRIC CARDS (custom class)
    ═══════════════════════════════════════ */
    .metric-card {
        position: relative;
        background: linear-gradient(145deg, rgba(15,19,40,0.9), rgba(20,26,52,0.7));
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(79,70,229,0.2);
        box-shadow: 0 4px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
        margin-bottom: 16px;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 16px;
        padding: 1px;
        background: linear-gradient(135deg, rgba(79,70,229,0.4), rgba(124,58,237,0.2), rgba(6,182,212,0.2));
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        pointer-events: none;
    }

    /* ═══════════════════════════════════════
       STREAMLIT NATIVE METRIC COMPONENTS
    ═══════════════════════════════════════ */
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(15,19,40,0.95), rgba(20,26,52,0.8)) !important;
        border: 1px solid rgba(79,70,229,0.2) !important;
        border-radius: 14px !important;
        padding: 20px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.35) !important;
    }
    [data-testid="stMetricLabel"] {
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        color: #64748b !important;
    }
    [data-testid="stMetricValue"] {
        font-weight: 800 !important;
        font-size: 2rem !important;
        color: #f1f5f9 !important;
        letter-spacing: -0.02em !important;
    }
    [data-testid="stMetricDelta"] {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }

    /* ═══════════════════════════════════════
       REPORT / AI OUTPUT BOX
    ═══════════════════════════════════════ */
    .report-box {
        background: linear-gradient(145deg, rgba(12,16,32,0.95), rgba(18,22,45,0.85));
        padding: 28px;
        border-radius: 16px;
        border-left: 4px solid #4f46e5;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.04);
        font-size: 1.02rem;
        line-height: 1.75;
        color: #cbd5e1;
        font-family: 'Outfit', sans-serif;
    }

    /* ═══════════════════════════════════════
       TABS
    ═══════════════════════════════════════ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        padding: 6px;
        background: rgba(10,14,30,0.6) !important;
        border-radius: 14px !important;
        border: 1px solid rgba(79,70,229,0.15) !important;
        width: fit-content;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        border-radius: 10px !important;
        padding: 0 20px !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        color: #64748b !important;
        background: transparent !important;
        border: none !important;
        letter-spacing: 0.01em;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: #ffffff !important;
        box-shadow: 0 2px 12px rgba(79,70,229,0.5) !important;
    }

    /* ═══════════════════════════════════════
       BUTTONS
    ═══════════════════════════════════════ */
    [data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        padding: 12px 28px !important;
        box-shadow: 0 4px 20px rgba(79,70,229,0.4) !important;
        letter-spacing: 0.01em !important;
    }
    [data-testid="baseButton-primary"]:hover {
        box-shadow: 0 6px 28px rgba(79,70,229,0.6) !important;
        transform: translateY(-1px) !important;
    }

    /* ═══════════════════════════════════════
       INPUTS & SELECTS
    ═══════════════════════════════════════ */
    [data-testid="stSelectbox"] > div,
    [data-testid="stTextInput"] > div > div {
        background: rgba(10,14,30,0.8) !important;
        border: 1px solid rgba(79,70,229,0.25) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
    }
    [data-testid="stSelectbox"] > div:focus-within,
    [data-testid="stTextInput"] > div > div:focus-within {
        border-color: rgba(79,70,229,0.7) !important;
        box-shadow: 0 0 0 3px rgba(79,70,229,0.15) !important;
    }
    .stSelectbox [data-baseweb="select"] > div {
        background: rgba(10,14,30,0.8) !important;
        border-color: rgba(79,70,229,0.25) !important;
        color: #e2e8f0 !important;
    }

    /* ═══════════════════════════════════════
       SLIDERS
    ═══════════════════════════════════════ */
    [data-testid="stSlider"] [data-testid="stMarkdownContainer"] {
        color: #94a3b8 !important;
    }
    .stSlider [role="slider"] {
        background: #4f46e5 !important;
        box-shadow: 0 0 0 4px rgba(79,70,229,0.25) !important;
    }

    /* ═══════════════════════════════════════
       DATAFRAME / TABLE
    ═══════════════════════════════════════ */
    [data-testid="stDataFrame"] {
        border-radius: 14px !important;
        overflow: hidden !important;
        border: 1px solid rgba(79,70,229,0.15) !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
    }

    /* ═══════════════════════════════════════
       ALERTS & STATUS
    ═══════════════════════════════════════ */
    [data-testid="stAlert"] {
        border-radius: 12px !important;
        border: none !important;
    }
    .stSuccess {
        background: rgba(16,185,129,0.12) !important;
        border: 1px solid rgba(16,185,129,0.3) !important;
        color: #6ee7b7 !important;
    }
    .stError {
        background: rgba(239,68,68,0.12) !important;
        border: 1px solid rgba(239,68,68,0.3) !important;
        color: #fca5a5 !important;
    }
    .stWarning {
        background: rgba(245,158,11,0.12) !important;
        border: 1px solid rgba(245,158,11,0.3) !important;
        color: #fcd34d !important;
    }

    /* ═══════════════════════════════════════
       EXPANDER
    ═══════════════════════════════════════ */
    [data-testid="stExpander"] {
        background: rgba(10,14,30,0.6) !important;
        border: 1px solid rgba(79,70,229,0.15) !important;
        border-radius: 12px !important;
    }

    /* ═══════════════════════════════════════
       DIVIDER
    ═══════════════════════════════════════ */
    hr {
        border-color: rgba(79,70,229,0.15) !important;
    }

    /* ═══════════════════════════════════════
       SCROLLBAR
    ═══════════════════════════════════════ */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #080c18; }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(#4f46e5, #7c3aed);
        border-radius: 6px;
    }
    ::-webkit-scrollbar-thumb:hover { background: #6366f1; }

    </style>
""", unsafe_allow_html=True)




# Sidebar Configuration
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2830/2830284.png", width=60)
st.sidebar.title("System Config")
api_key = st.sidebar.text_input("Gemini API Key:", type="password", help="Enter your Google AI Studio key here.")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config={"response_mime_type": "application/json"}
    )
else:
    st.sidebar.warning("⚠️ API Key required to run investigations.")

# ==========================================
# 2. Database Loading
# ==========================================
@st.cache_data
def load_mock_database():
    try:
        with open("JSON/upi_customers.json", "r") as f:
            customers = {c["customer_uuid"]: c for c in json.load(f)}
        with open("JSON/upi_merchants.json", "r") as f:
            merchants = {m["merchant_uuid"]: m for m in json.load(f)}
        with open("JSON/upi_transactions.json", "r") as f:
            transactions = json.load(f)
            
        # Convert transactions to DataFrame for interactive plotting/filtering
        df_txn = pd.DataFrame(transactions)
        df_txn['timestamp'] = pd.to_datetime(df_txn['timestamp'])
        
        # Merge basic merch info into transaction df for filtering
        merch_list = []
        for t in transactions:
            m = merchants.get(t['merchant_uuid'])
            merch_list.append({
                'merchant_category': m['category'] if m else 'Unknown',
                'merchant_risk': m['merchant_risk_score'] if m else 0,
                'merchant_name': m['merchant_name'] if m else 'Unknown'
            })
        df_merch_meta = pd.DataFrame(merch_list)
        df_txn = pd.concat([df_txn, df_merch_meta], axis=1)

        return customers, merchants, transactions, df_txn
    except FileNotFoundError:
        return None, None, None, None

customers, merchants, transactions, df_txn = load_mock_database()

if not transactions:
    st.error("🚨 Database files missing! Check the `JSON` folder.")
    st.stop()

# ==========================================
# 3. AI Engines
# ==========================================
def analyze_relational_case(case_payload):
    prompt = """
    You are an expert banking fraud investigator. Analyze the provided structured JSON data.
    Compare the 'transaction' details against the 'customer' profile and 'merchant' data. 
    Pay special attention to IP location mismatches and device changes compared to the customer's base location and primary device.
    
    Output strictly in JSON:
    {
      "Investigation_Type": "UPI",
      "Decision": "Fraud" | "Safe" | "Manual Review",
      "Detected_Inconsistencies": ["list of specific red flags or 'None'"],
      "Investigation_Report": "A detailed reasoning summary."
    }
    """
    response = model.generate_content([prompt, json.dumps(case_payload)])
    text = response.text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return json.loads(text.strip())

def analyze_cheque(image):
    prompt = """
    You are an expert banking fraud investigator. Analyze this cheque image.
    Verify if Amount in Words matches Amount in Numbers, check for a signature, and validate the date.
    
    Output strictly in JSON:
    {
      "Investigation_Type": "Cheque",
      "Extracted_Data": {"Payee": "", "Amount_Words": "", "Amount_Numbers": "", "Date": "", "Signature_Present": true},
      "Decision": "Clear" | "Fraud" | "Manual Review",
      "Detected_Inconsistencies": ["list of issues or 'None'"],
      "Investigation_Report": "A detailed reasoning summary."
    }
    """
    response = model.generate_content([prompt, image])
    text = response.text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return json.loads(text.strip())

# ==========================================
# 4. Main UI Dashboard
# ==========================================
st.title("🕵️ Intelligent Investigation Hub Pro")
st.markdown("Advanced interactive anomaly detection, risk analytics, and AI reasoning.")

# Primary Navigation
menu = st.sidebar.radio("Navigation Menu", ["Global Dashboard", "UPI Investigations", "Cheque Clearing"])

# --- VIEW 1: GLOBAL DASHBOARD ---
if menu == "Global Dashboard":
    st.subheader("🌐 Fleet Overview & Risk Analytics")
    
    # KPIs
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Transactions", f"{len(df_txn):,}")
    kpi2.metric("Volume Processed", f"₹{df_txn['amount_inr'].sum():,.2f}")
    kpi3.metric("Avg Amount", f"₹{df_txn['amount_inr'].mean():,.2f}")
    kpi4.metric("High Risk Merchants", f"{len(df_txn[df_txn['merchant_risk'] > 7]):,}")

    st.divider()

    # Interactive Charts
    colA, colB = st.columns(2)
    
    with colA:
        st.markdown("**Transaction Spread by Category**")
        fig_pie = px.pie(df_txn, names='merchant_category', hole=0.4, 
                         color_discrete_sequence=px.colors.qualitative.Set3)
        fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_pie, use_container_width=True)

    with colB:
        st.markdown("**Amount vs. Merchant Risk Score**")
        fig_scatter = px.scatter(df_txn, x='amount_inr', y='merchant_risk', 
                                 color='merchant_category', hover_data=['transaction_uuid', 'merchant_name'],
                                 labels={'amount_inr': 'Transaction Amount (₹)', 'merchant_risk': 'Risk Score (0-10)'})
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("**Recent High-Value Transactions**")
    st.dataframe(df_txn.sort_values(by='amount_inr', ascending=False).head(10)[
        ['timestamp', 'transaction_uuid', 'merchant_name', 'amount_inr', 'ip_location', 'device_used']
    ], use_container_width=True)


# --- VIEW 2: UPI INVESTIGATIONS ---
elif menu == "UPI Investigations":
    st.subheader("🔍 Deep-Dive UPI Case Analysis")
    
    # Interactive Sidebar Filters
    st.sidebar.markdown("### 🎛️ Case Filters")
    min_amt = st.sidebar.slider("Minimum Amount (₹)", 0, int(df_txn['amount_inr'].max()), 0)
    risk_thresh = st.sidebar.slider("Minimum Merchant Risk", 0, 10, 0)
    
    categories = st.sidebar.multiselect("Merchant Category", options=df_txn['merchant_category'].unique(), default=list(df_txn['merchant_category'].unique()))

    # Apply Filters
    filtered_df = df_txn[
        (df_txn['amount_inr'] >= min_amt) & 
        (df_txn['merchant_risk'] >= risk_thresh) &
        (df_txn['merchant_category'].isin(categories))
    ]

    if filtered_df.empty:
        st.warning("No transactions match the selected filters.")
        st.stop()

    # Formatter for dropdown
    def format_txn(txn_uuid):
        txn_row = filtered_df[filtered_df['transaction_uuid'] == txn_uuid].iloc[0]
        amount = f"₹{txn_row['amount_inr']:,.2f}"
        date = str(txn_row['timestamp'])[:10]
        risk = txn_row['merchant_risk']
        return f"UUID: {txn_uuid[:8]} | {date} | {amount} | Risk: {risk}/10"

    selected_uuid = st.selectbox(
        f"Select from {len(filtered_df)} filtered cases:", 
        options=filtered_df['transaction_uuid'].tolist(), 
        format_func=format_txn
    )
    
    # Join Data for the single case
    txn = next((t for t in transactions if t['transaction_uuid'] == selected_uuid), None)
    cust = customers.get(txn["customer_uuid"])
    merch = merchants.get(txn["merchant_uuid"])
    
    full_case = {"transaction": txn, "customer": cust, "merchant": merch}

    # Beautiful Human-Readable Data Display
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("#### 🧑 Customer Profile")
        st.metric(label="Account Name", value=cust['name'])
        st.markdown(f"**📍 Base Location:** `{cust['base_location']}`<br>**📱 Primary Device:** `{cust['primary_device_id']}`<br>**🏦 Bank Name:** `{cust['bank_name']}`", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("#### 💳 Current Transaction")
        st.metric(label="Amount Attempted", value=f"₹{txn['amount_inr']:,.2f}")
        
        # Highlighting mismatches interactively
        ip_color = "red" if txn['ip_location'] != cust['base_location'] else "green"
        dev_color = "red" if txn['device_used'] != cust['primary_device_id'] else "green"
        
        st.markdown(f"**📍 TXN Location:** <span style='color:{ip_color}'>`{txn['ip_location']}`</span><br>**📱 TXN Device:** <span style='color:{dev_color}'>`{txn['device_used']}`</span><br>**⏰ Time:** {str(txn['timestamp'])[:19]}", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("#### 🏪 Merchant Data")
        st.metric(label="Merchant Name", value=merch['merchant_name'][:20])
        st.markdown(f"**🏷️ Category:** {merch['category']}<br>**⚠️ Risk Score:** {merch['merchant_risk_score']} / 10<br>**🆔 VPA:** `{merch['vpa']}`", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Raw Case Payload hidden from frontend

    st.divider()

    # The AI Trigger
    colA, colB, colC = st.columns([1, 1.5, 1])
    with colB:
        run_ai = st.button("✨ Run Comprehensive AI Forensic Investigation", type="primary", use_container_width=True)

    if run_ai:
        if not api_key:
            st.error("Please enter your API key in the sidebar.")
        else:
            with st.status("🧠 AI Agents Analyzing the Case...", expanded=True) as status:
                st.write("Cross-referencing customer base location with transaction IP...")
                st.write("Evaluating device fingerprint consistency...")
                st.write("Assessing merchant risk factors...")
                try:
                    result = analyze_relational_case(full_case)
                    status.update(label="✅ Analysis Complete", state="complete", expanded=False)
                    
                    st.markdown("### 📑 Official Investigation Report")
                    
                    # Tabbed AI Response
                    tab1, tab2 = st.tabs(["📋 Executive Summary", "🚨 Red Flags"])
                    
                    with tab1:
                        decision = result.get("Decision")
                        if decision == "Fraud":
                            st.error(f"**VERDICT: {decision.upper()}** - Immediate Block Recommended")
                        elif decision == "Safe":
                            st.success(f"**VERDICT: {decision.upper()}** - Clear for Processing")
                        else:
                            st.warning(f"**VERDICT: {decision.upper()}** - Escalate to Tier 2 Human Agent")
                        
                        st.markdown(f"<div class='report-box'><strong>AI Reasoning:</strong><br><br>{result.get('Investigation_Report')}</div>", unsafe_allow_html=True)
                    
                    with tab2:
                        inconsistencies = result.get("Detected_Inconsistencies", [])
                        if isinstance(inconsistencies, str):
                            inconsistencies = [inconsistencies]
                            
                        if inconsistencies and str(inconsistencies[0]).lower() != "none":
                            for flag in inconsistencies:
                                st.error(f"🚩 {flag}")
                        else:
                            st.success("✅ No critical inconsistencies detected.")
                            

                except Exception as e:
                    status.update(label="❌ Analysis Failed", state="error", expanded=True)
                    st.error(f"Error details: {e}")

# --- VIEW 3: CHEQUE CLEARING ---
elif menu == "Cheque Clearing":
    st.subheader("🏦 Smart Cheque OCR & Verification")
    
    uploaded_file = st.file_uploader("Upload a scanned Cheque image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        colimg, colderive = st.columns([1.2, 1])
        
        with colimg:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Instrument", use_container_width=True)
            
        with colderive:
            st.markdown("#### Instrument Verification")
            if st.button("🔍 Extract & Analyze Document", type="primary", use_container_width=True):
                if not api_key:
                    st.error("Please enter your API key in the sidebar.")
                else:
                    with st.spinner("Running Vision Model..."):
                        try:
                            result = analyze_cheque(image)
                            
                            decision = result.get("Decision")
                            if decision in ["Clear", "Safe"]:
                                st.success(f"**Verdict:** {decision} ✅")
                            elif decision == "Fraud":
                                st.error(f"**Verdict:** {decision} 🚨")
                            else:
                                st.warning(f"**Verdict:** {decision} ⚠️")
                                
                            # Display extracted data as a clean dataframe/table 
                            data = result.get("Extracted_Data", {})
                            st.markdown("**Extracted Data Points:**")
                            df_extract = pd.DataFrame([
                                {"Field": "Payee Name", "Value": data.get('Payee', 'N/A')},
                                {"Field": "Amount (Words)", "Value": data.get('Amount_Words', 'N/A')},
                                {"Field": "Amount (Numbers)", "Value": str(data.get('Amount_Numbers', 'N/A'))},
                                {"Field": "Date on Cheque", "Value": data.get('Date', 'N/A')},
                                {"Field": "Signature", "Value": '✅ Present' if data.get('Signature_Present') else '❌ Missing'}
                            ])
                            st.dataframe(df_extract, hide_index=True, use_container_width=True)
                            
                            st.markdown("**AI Context / Reasoning:**")
                            st.info(result.get("Investigation_Report"))
                            
                            inconsistencies = result.get("Detected_Inconsistencies", [])
                            if isinstance(inconsistencies, str):
                                inconsistencies = [inconsistencies]
                                
                            if inconsistencies and str(inconsistencies[0]).lower() != "none":
                                st.error("**Anomalies Flagged by AI:**")
                                for flag in inconsistencies:
                                    st.write(f"- 🚩 {flag}")
                                    
                        except Exception as e:
                            st.error(f"Analysis failed: {e}")