import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="Recommend Appartments")

location_df = pickle.load(open('datasets/location_distance.pkl','rb'))
apartment_link=pickle.load(open('datasets/apartment_link.pkl','rb'))
cosine_sim1 = pickle.load(open('datasets/cosine_sim1.pkl', 'rb'))
cosine_sim2 = pickle.load(open('datasets/cosine_sim2.pkl', 'rb'))
cosine_sim3 = pickle.load(open('datasets/cosine_sim3.pkl', 'rb'))

def recommend_properties_with_scores(property_name, top_n=5):
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]
    top_properties = location_df.index[top_indices].tolist()
    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })
    return recommendations_df


st.title('Select Location and Radius')
selected_location = st.selectbox(
    'Location',
    sorted(location_df.columns.to_list())
)
radius = st.number_input('Radius in Kms')
if st.button("Search"):
    st.session_state.result_ser = location_df[location_df[selected_location] < radius * 1000][selected_location].sort_values()
if "result_ser" in st.session_state:
    result_ser = st.session_state.result_ser
    if result_ser.empty:
        st.warning("No apartments found near this location.")
    else:
        st.success(f"Found {len(result_ser)} apartment(s).")
        nearby_apartments = result_ser.index.tolist()
        selected_apartment = st.radio(
            "Select an apartment",
            nearby_apartments
        )
        st.header("Recommended Apartments")
        if st.button("Recommend"):
            recommendation_df = recommend_properties_with_scores(selected_apartment)
            recommendation_df = recommendation_df.merge(
                apartment_link,
                on='PropertyName',
                how='left'
            )
            for i, row in recommendation_df.iterrows():
                with st.container(border=True):
                    col1, col2 = st.columns([5, 1])
                    with col1:
                        st.subheader(row["PropertyName"])
                        st.caption(f"⭐ Similarity Score: {row['SimilarityScore']:.3f}")
                    with col2:
                        st.metric("Rank", f"#{i + 1}")
                    st.link_button(
                        "🔗 View Property",
                        row["Link"],
                        )