import streamlit as st

# Page setup
st.set_page_config(
    page_title="Jan-Kalyan AI | Citizen Welfare Portal",
    page_icon="🏛️",
    layout="wide"
)

# Custom High-Trust Styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0d3b66, #001e3d);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
    }
    .scheme-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 18px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        color: #1a202c;
    }
    .badge-tag {
        display: inline-block;
        background-color: #ebf8ff;
        color: #2b6cb0;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 6px;
    }
    .benefit-box {
        background-color: #f0fff4;
        border-left: 4px solid #38a169;
        padding: 10px 14px;
        border-radius: 4px;
        margin: 12px 0;
        font-weight: 600;
        color: #22543d;
    }
    .doc-box {
        background-color: #f7fafc;
        border-radius: 6px;
        padding: 10px;
        font-size: 13px;
        color: #4a5568;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Welfare Database with Eligibility & Docs
SCHEME_DATABASE = [
    {
        "name": "UP Post-Matric Scholarship & Fee Reimbursement",
        "ministry": "Social Welfare Dept, Uttar Pradesh",
        "category": ["SC", "ST", "OBC", "GEN", "MINORITY"],
        "max_annual_income": 250000,
        "target_group": "student",
        "benefit": "100% Tuition Fee Waiver + Up to Rs 12,000 Annual Stipend",
        "docs": "Aadhaar Card, Cast Certificate, Income Certificate, College Fee Receipt",
        "portal": "https://scholarship.up.gov.in"
    },
    {
        "name": "Ayushman Bharat (PM-JAY) Golden Health Card",
        "ministry": "National Health Authority",
        "category": ["ALL"],
        "max_annual_income": 180000,
        "target_group": "all",
        "benefit": "Cashless Hospital Treatment up to Rs 5,00,000 per family/year",
        "docs": "Ration Card, Aadhaar Card, Active Mobile Number",
        "portal": "https://setu.pmjay.gov.in"
    },
    {
        "name": "Mukhyamantri Kanya Sumangala Yojana",
        "ministry": "Women & Child Development, UP",
        "category": ["ALL"],
        "max_annual_income": 300000,
        "target_group": "all",
        "requires_girl_child": True,
        "benefit": "Rs 25,000 Cash Support distributed across 6 educational phases",
        "docs": "Child Birth Certificate, Parents Aadhaar, Bank Passbook, Residence Proof",
        "portal": "https://mksy.up.gov.in"
    },
    {
        "name": "PM Kisan Samman Nidhi",
        "ministry": "Ministry of Agriculture & Farmers Welfare",
        "category": ["ALL"],
        "max_annual_income": float("inf"),
        "target_group": "farmer",
        "benefit": "Rs 6,000 per year directly credited in 3 equal installments",
        "docs": "Khatoni/Land Records, Aadhaar Card, NPCI-linked Bank Account",
        "portal": "https://pmkisan.gov.in"
    },
    {
        "name": "UP Nirashrit Mahila Pension (Widow Pension)",
        "ministry": "Dept of Women & Child Development, UP",
        "category": ["ALL"],
        "max_annual_income": 200000,
        "target_group": "widow",
        "benefit": "Rs 1,000 monthly DBT support directly into beneficiary account",
        "docs": "Husband Death Certificate, Income Certificate, Bank Account Details",
        "portal": "https://sspy-up.gov.in"
    },
    {
        "name": "PM SVANidhi Micro-Credit Scheme",
        "ministry": "Ministry of Housing and Urban Affairs",
        "category": ["ALL"],
        "max_annual_income": float("inf"),
        "target_group": "street_vendor",
        "benefit": "Working Capital Loan up to Rs 50,000 with 7% Interest Subsidy",
        "docs": "Vending Certificate / Urban Local Body ID, Aadhaar Card",
        "portal": "https://pmsvanidhi.mohua.gov.in"
    }
]

# Header Section
st.markdown("""
<div class="main-header">
    <h1 style="margin:0; font-size: 28px;">🏛️ Jan-Kalyan AI Welfare Portal</h1>
    <p style="margin:6px 0 0 0; opacity: 0.9; font-size: 14px;">Instant Eligibility Screener & Direct Benefit Transfer (DBT) Scheme Discovery</p>
</div>
""", unsafe_allow_html=True)

# Layout: 2 Columns (Form on left, live tips on right)
col_form, col_info = st.columns([2, 1], gap="medium")

with col_form:
    st.subheader("1. Enter Citizen Profile")
    
    c1, c2 = st.columns(2)
    with c1:
        income_text = st.text_input("Annual Household Income (₹):", value="120000", help="Enter total family yearly income")
    with c2:
        category = st.selectbox("Social Category:", ["GEN", "OBC", "SC", "ST", "MINORITY"])

    c3, c4 = st.columns(2)
    with c3:
        role_display = st.selectbox(
            "Primary Occupation / Status:",
            ["Student", "Farmer", "Street Vendor", "Widow / Destitute", "General Citizen"]
        )
    with c4:
        girl_child_choice = st.selectbox("Any girl child under 18 in household?", ["No", "Yes"])

    role_map = {
        "Student": "student",
        "Farmer": "farmer",
        "Street Vendor": "street_vendor",
        "Widow / Destitute": "widow",
        "General Citizen": "all"
    }
    has_girl_child = (girl_child_choice == "Yes")

    search_clicked = st.button("Check Scheme Eligibility 🚀", use_container_width=True, type="primary")

with col_info:
    st.subheader("📌 Key Citizen Notice")
    st.info(
        "**Zero-Fee Advisory:** All state and central government portals do not charge registration fees. Always keep your **Aadhaar-linked mobile number** active for DBT verification."
    )
    st.markdown("""
    - 🔒 **Privacy:** No citizen data is logged or stored.
    - ⚡ **DBT Direct:** Benefits directly credit to NPCI bank accounts.
    """)

st.write("---")

# Execution & Matching Engine
if search_clicked or True:
    try:
        income = float(income_text.strip().replace(",", ""))
    except ValueError:
        income = 0.0

    role = role_map[role_display]
    eligible = []

    for s in SCHEME_DATABASE:
        if income > s["max_annual_income"]:
            continue
        if "ALL" not in s["category"] and category not in s["category"]:
            continue
        if s["target_group"] != "all" and s["target_group"] != role:
            continue
        if s.get("requires_girl_child", False) and not has_girl_child:
            continue
        eligible.append(s)

    # Summary Metrics Row
    m1, m2, m3 = st.columns(3)
    m1.metric("Eligible Schemes", f"{len(eligible)} Schemes")
    m2.metric("Target Department", "State & Central Govt")
    m3.metric("Verification Status", "Direct Portal Links Available")

    st.write("### 2. Available Schemes For Your Profile")

    if not eligible:
        st.warning("No specific welfare schemes matched these income and category thresholds.")
    else:
        for item in eligible:
            st.markdown(f"""
            <div class="scheme-card">
                <span class="badge-tag">{item['ministry']}</span>
                <span class="badge-tag">Category: {', '.join(item['category'])}</span>
                <h3 style="margin: 10px 0 6px 0; color: #1a365d;">{item['name']}</h3>
                <div class="benefit-box">💰 Benefit: {item['benefit']}</div>
                <div class="doc-box">📑 <b>Required Documents:</b> {item['docs']}</div>
            </div>
            """, unsafe_allow_html=True)

            c_link, c_help = st.columns([1, 1])
            with c_link:
                st.link_button(f"Apply on Official Portal ↗", item["portal"], use_container_width=True)
            with c_help:
                # Direct Assisted Apply CTA via WhatsApp
                whatsapp_url = f"https://wa.me/?text=Hello%20I%20need%20assistance%20applying%20for%20{item['name'].replace(' ', '%20')}"
                st.link_button("Get Form Fill Assistance (Jan Seva) 💬", whatsapp_url, use_container_width=True)

            st.write("")
