import streamlit as st

st.set_page_config(page_title="SACI Calculator", layout="centered")
st.title("Severity-Adjusted Caries Index (SACI) Calculator")

st.sidebar.header("Input Parameters")
S1_2 = st.sidebar.number_input("Number of surfaces with ICDAS 1-2 scores (S1-2)", min_value=0, step=1)
S3_4 = st.sidebar.number_input("Number of surfaces with ICDAS 3-4 scores (S3-4)", min_value=0, step=1)
S5_6 = st.sidebar.number_input("Number of surfaces with ICDAS 5-6 scores (S5-6)", min_value=0, step=1)
NMc_ant = st.sidebar.number_input("Anterior teeth missing due to caries (NMc_ant)", min_value=0, step=1)
NMc_post = st.sidebar.number_input("Posterior teeth missing due to caries (NMc_post)", min_value=0, step=1)
NF1 = st.sidebar.number_input("Single-surface fillings (NF1)", min_value=0, step=1)
NF2_3 = st.sidebar.number_input("2-3 surface fillings (NF2-3)", min_value=0, step=1)
NF4_plus = st.sidebar.number_input("4+ surface fillings or crowns (NF4+)", min_value=0, step=1)
NMnc_ant = st.sidebar.number_input("Anterior teeth missing non-caries (NMnc_ant)", min_value=0, step=1)
NMnc_post = st.sidebar.number_input("Posterior teeth missing non-caries (NMnc_post)", min_value=0, step=1)

# Calculate component scores
da_score = 0.5 * S1_2 + 1.0 * S3_4 + 2.0 * S5_6
mc_score = 4 * NMc_ant + 5 * NMc_post
fc_score = 1 * NF1 + 2 * NF2_3 + 3 * NF4_plus

# Calculate total available surfaces
total_surfaces = 128 - (4 * NMnc_ant) - (5 * NMnc_post)

st.subheader("Component Scores")
st.write(f"**Weighted Active Caries Score (Dₐ):** {da_score:.2f}")
st.write(f"**Missing Due to Caries Score (M_c):** {mc_score:.2f}")
st.write(f"**Restored Due to Caries Score (F_c):** {fc_score:.2f}")
st.write(f"**Total Available Surfaces (S_total):** {total_surfaces}")

# Compute submodel scores if valid
def compute_scores():
    if total_surfaces <= 0:
        return None, None, None, None
    saci_total = (da_score + mc_score + fc_score) / total_surfaces * 100
    saci_active = (da_score / total_surfaces) * 100
    saci_loss = (mc_score / total_surfaces) * 100
    saci_restoration = (fc_score / total_surfaces) * 100
    return saci_total, saci_active, saci_loss, saci_restoration

saci_total, saci_active, saci_loss, saci_restoration = compute_scores()

st.subheader("SACI Scores")
if saci_total is None:
    st.error("Invalid total surface count (≤0). Adjust non-caries tooth counts.")
else:
    st.write(f"**SACI-total:** {saci_total:.2f}%")
    st.write(f"**SACI-active:** {saci_active:.2f}%")
    st.write(f"**SACI-loss:** {saci_loss:.2f}%")
    st.write(f"**SACI-restoration:** {saci_restoration:.2f}%")

st.markdown("---")
st.markdown("Developed based on the SACI framework integrating active lesions, caries-related tooth loss, and restorations, with submodel breakdown for granular analysis.")
