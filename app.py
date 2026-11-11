import streamlit as st

st.set_page_config(page_title="Jan-Kalyan AI Welfare Portal", page_icon="🇮🇳", layout="centered")

st.title("🇮🇳 Jan-Kalyan AI Welfare Discovery")
st.caption("Deterministic Citizen Welfare & Direct Benefit Matching Engine")

SCHEME_DATABASE = [
    {
        "name": "UP Post-Matric Scholarship & Fee Reimbursement",
        "category": ["SC", "ST", "OBC", "GEN", "MINORITY"],
        "max_annual_income": 250000,
        "target_group": "student",
        "benefit": "100% Tuition Fee Reimbursement + Monthly Maintenance Allowance",
        "portal": "https://scholarship.up.gov.in"
    },
    {
        "name": "Ayushman Bharat (PM-JAY) Golden Health Card",
        "category": ["ALL"],
        "max_annual_income": 180000,
        "target_group": "all",
        "benefit": "Free Cashless Hospital Treatment up to Rs 5,00,000 per family/year",
        "portal": "https://setu.pmjay.gov.in"
    },
    {
        "name": "Mukhyamantri Kanya Sumangala Yojana",
        "category": ["ALL"],
        "max_annual_income": 300000,
        "target_group": "all",
        "requires_girl_child": True,
        "benefit": "Rs 25,000 Total Cash Assistance in 6 educational phases",
        "portal": "https://mksy.up.gov.in"
    },
    {
        "name": "PM Kisan Samman Nidhi",
        "category": ["ALL"],
        "max_annual_income": float("inf"),
        "target_group": "farmer",
        "benefit": "Rs 6,000 per year directly into bank account (3 installments)",
        "portal": "https://pmkisan.gov.in"
    },
    {
        "name": "UP Nirashrit Mahila Pension Yojana (Widow Pension)",
        "category": ["ALL"],
        "max_annual_income": 200000,
        "target_group": "widow",
        "benefit": "Rs 1,000 per month (Rs 12,000/year) direct DBT support",
        "portal": "https://sspy-up.gov.in"
    },
    {
        "name": "PM SVANidhi (Urban Street Vendors)",
        "category": ["ALL"],
        "max_annual_income": float("inf"),
        "target_group": "street_vendor",
        "benefit": "Collateral-free working capital loan up to Rs 50,000 with 7% interest subsidy",
        "portal": "https://pmsvanidhi.mohua.gov.in"
    }
]

st.subheader("Enter Citizen Details")

income_text = st.text_input("Annual Household Income in Rs (e.g. 0, 50000, 140000):", value="0")

category = st.radio(
    "Select Social Category:",
    ["GEN", "OBC", "SC", "ST", "MINORITY"],
    horizontal=True
)

role_display = st.radio(
    "Current Occupation / Status:",
    ["Student", "Farmer", "Street Vendor", "Widow / Destitute", "General / Other"],
    horizontal=True
)

role_map = {
    "Student": "student",
    "Farmer": "farmer",
    "Street Vendor": "street_vendor",
    "Widow / Destitute": "widow",
    "General / Other": "all"
}

girl_child_choice = st.radio("Is there a girl child in the household (under 18)?", ["No", "Yes"], horizontal=True)
has_girl_child = (girl_child_choice == "Yes")

if st.button("Find Eligible Schemes 🚀"):
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

    st.success(f"Matched {len(eligible)} Government Welfare Schemes!")

    for item in eligible:
        st.markdown(f"### {item['name']}")
        st.markdown(f"**Direct Benefit:** {item['benefit']}")
        st.markdown(f"[Open Official Portal]({item['portal']})")
        st.write("---")