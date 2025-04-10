import streamlit as st
import pandas as pd

# ---------- Custom Styles ----------
st.markdown("""
    <style>
        .stApp {
            background-color: #334050;
            color: white;
        }

        div.stButton > button {
            background-color: #334050;
            color: white;
            border: 1px solid #019cab;
            height: 70px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            white-space: normal;
        }

        div.stButton > button:hover {
            background-color: #019cab;
            color: white;
        }

        div.stButton > button:focus:not(:active) {
            border-color: #019cab;
            box-shadow: 0 0 0 0.2rem rgba(1, 156, 171, 0.25);
        }

        section[data-testid="stSidebar"] .stSelectbox {
            background-color: #334050 !important;
            border-radius: 6px;
            color: white !important;
        }

        section[data-testid="stSidebar"] label {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)


# ---------- Load Data ----------
@st.cache_data
def load_data():
    return pd.read_excel("ioa_data.xlsx")

df = load_data()

# ---------- Grouped Fields ----------
groups = {
    "Borderland Information": [
        ("Country", "country"),
        ("Borderland", "borderland"),
        ("Locations", "location"),
        ("Level of stability", "stability"),
        ("Development of Regional Integration Infrastructure", "reg_integ"),
        ("Typology Categorisation", "category"),
    ],
    "Sector Justification": [
        ("Sector", "sector_identification"),
        ("Sector justification", "sector_justification"),
        ("Sub-sector", "subsector_identification"),
        ("Sub-sector justification", "subsector_justification"),
        ("Industry", "industry"),
    ],
    "IOA Business Model": [
        ("Investment Opportunity Area (IOA)", "ioa_title"),
        ("IOA Business Model", "ioa_model"),
        ("Cases in IOA space", "ioa_casestudy"),
        ("Market Size (USD value)", "market_size1"),
        ("Market Size (CAGR)", "market_size2"),
        ("Market Size (in critican IOA unit)", "market_size3"),
        ("Market size justification", "marketsize_justif"),
        ("Indicative Return (IRR)", "return_irr"),
        ("Indicative Return (ROI)", "return_roi"),
        ("Indicative Return (GPM)", "return_gpm"),
        ("Return Profile justification", "return_justif"),
        ("Timeframe", "timeframe"),
        ("Investment Timeframe justification", "timeframe_justif"),
        ("Ticket Size", "ticket_size"),
        ("Market Risks & Scale Obstacles Identification", "market_risks_identification"),
        ("Market Risks & Scale Obstacles Justification", "market_risks_justif"),
        ("Expected Financing Model", "financing_model"),
        ("IOA Business Criteria", "ioa_business_criteria"),
    ],
    "Impact Case": [
        ("Sustainable Development Need", "dev_need_desc"),
        ("Gender & Marginalisation needs", "dev_need_gender"),
        ("Development Outcome", "dev_outcome_desc"),
        ("Gender & Marginalisation Outcome", "dev_outcome_gender"),
        ("Primary SDGs addressed", "sdg_prim_ident"),
        ("Primary SDG indicators impacted", "sdg_prim_impact"),
        ("SDG Indicators - current levels", "sdg_prim_current"),
        ("SDG Indicators - targets", "sdg_prim_target"),
        ("Secondary SDGs addressed", "sdg_second"),
        ("Stakeholders directly impacted", "stakeholders_impact_direct"),
        ("Stakeholders indirectly impacted", "stakeholders_impact_indirect"),
        ("Outcome Risks", "outcome_risks"),
        ("Impact Risks", "impact_risks"),
        ("IMP Impact Dimensions", "impact_dimensions"),
        ("IMP Impact Class", "impact_class"),
        ("Impact - Gender & Marginalisation", "impact_gender"),
        ("Impact Thesis", "impact_thesis"),
    ],
    "Enabling Environment": [
        ("Policy Environment", "env_policy"),
        ("Regulatory Environment", "env_reg"),
        ("Cross-border Policy and Regulatory Environment", "cross_border_pol"),
        ("Capital structure and funding", "fin_structure"),
        ("Financial incentives", "fin_incentives"),
        ("Security environment", "env_sec"),
        ("Socio-political environment", "env_socio"),
        ("Risk mitigation strategies", "risks_mitig"),
        ("Actors in IOA space", "actors"),
    ],
    "References": [
        ("Sector-level references", "sources_sector"),
        ("IOA-level references", "sources_ioa"),
    ],
}

# ---------- Sidebar Filters ----------
st.sidebar.header("Filter IOAs")
sectors = df["sector_identification"].dropna().unique()
selected_sector = st.sidebar.selectbox("Select Sector", ["All"] + list(sectors))

if selected_sector == "All":
    available_subsectors = df["subsector_identification"].dropna().unique()
else:
    available_subsectors = df[df["sector_identification"] == selected_sector]["subsector_identification"].dropna().unique()

selected_subsector = st.sidebar.selectbox("Select Sub-sector", ["All"] + list(available_subsectors))

filtered_df = df.copy()
if selected_sector != "All":
    filtered_df = filtered_df[filtered_df["sector_identification"] == selected_sector]
if selected_subsector != "All":
    filtered_df = filtered_df[filtered_df["subsector_identification"] == selected_subsector]

# ---------- Page State ----------
if "selected_ioa" not in st.session_state:
    st.session_state.selected_ioa = None

# ---------- IOA Detail View ----------
if st.session_state.selected_ioa:
    if st.button("⬅️ Back to IOA List"):
        st.session_state.selected_ioa = None
        st.rerun()

    selected_row = df[df["ioa_title"] == st.session_state.selected_ioa].iloc[0]
    st.header(st.session_state.selected_ioa)

    for group_name, fields in groups.items():
        with st.expander(group_name, expanded=False):
            for label, var in fields:
                value = selected_row.get(var, "")
                if pd.notna(value):
                    st.markdown(f"**{label}:**")
                    st.markdown(value)

# ---------- IOA List View ----------
else:
    st.title("Investment Opportunity Areas (IOAs)")
    cols = st.columns([0.5, 0.5])  # Forces equal width columns

    for index, (_, row) in enumerate(filtered_df.iterrows()):
        col = cols[index % 2]
        with col:
            with st.container():
                st.markdown(
                    """
                    <div style="
                        background-color: white;
                        border-radius: 12px;
                        padding: 12px;
                        margin-bottom: 20px;
                        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                        text-align: center;
                        width: 100%;
                    ">
                    """,
                    unsafe_allow_html=True
                )

                if pd.notna(row["image"]):
                    st.image(row["image"], use_container_width=True)

                if st.button(row["ioa_title"], key=row["ioa_title"]):
                    st.session_state.selected_ioa = row["ioa_title"]
                    st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)
