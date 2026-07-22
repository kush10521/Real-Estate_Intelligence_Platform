import streamlit as st

st.set_page_config(
    page_title="RealEstate Intelligence Platform",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 RealEstate Intelligence Platform")

st.markdown("""
### Data-Driven Insights for Gurgaon Real Estate

This application combines **Machine Learning**, **Data Analytics**, and **Interactive Visualizations**
to help users analyze the Gurgaon real estate market and estimate property prices.
""")

st.divider()
st.subheader("🚀 Explore the Platform")
col1, col2, col3 = st.columns(3)
with col1:
    with st.container(border=True):
        st.markdown("### 💰 Price Predictor")
        st.write(
            "Estimate property prices using a Machine Learning model based on property features."
        )

with col2:
    with st.container(border=True):
        st.markdown("### 📊 Market Analytics")
        st.write(
            "Analyze price trends, sector insights, and interactive visualizations of Gurgaon properties."
        )

with col3:
    with st.container(border=True):
        st.markdown("### 🏠 Recommender System")
        st.write(
            "Find similar apartments using feature-based similarity and location data."
        )

st.divider()
st.subheader("📊 Market Summary")
c1, c2, c3, c4 = st.columns(4)
with c1:
    with st.container(border=True):
        st.metric("🏠 Properties", '3600+')

with c2:
    with st.container(border=True):
        st.metric("📍 Sectors", '95+')

with c3:
    with st.container(border=True):
        st.metric("💰 Avg Price", "2-3 Cr")

with c4:
    with st.container(border=True):
        st.metric("📈 Avg Price/Sq.ft", "11k-12k")