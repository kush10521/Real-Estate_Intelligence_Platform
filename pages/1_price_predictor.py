import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Price Predictor",
    page_icon="🏠",
    layout="wide"
)

with open('datasets/df.pkl','rb') as file:
    df = pickle.load(file)

with open('pipeline.pkl','rb') as file:
    pipeline = pickle.load(file)

st.title("🏠 Property Price Predictor")
st.write("Fill in the property details below to estimate its market price.")

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.subheader("Property Details")

    property_type = st.selectbox(
        "Property Type",
        ["flat","house"]
    )

    sector = st.selectbox(
        "Sector",
        sorted(df['sector'].unique())
    )

    built_up_area = st.number_input(
        "Built-up Area (sq.ft.)",
        min_value=100.0,
        step=50.0
    )

    bedrooms = float(
        st.selectbox(
            "Bedrooms",
            sorted(df['bedRoom'].unique())
        )
    )

    bathroom = float(
        st.selectbox(
            "Bathrooms",
            sorted(df['bathroom'].unique())
        )
    )

    balcony = st.selectbox(
        "Balconies",
        sorted(df['balcony'].unique())
    )

with col2:

    st.subheader("Additional Features")

    property_age = st.selectbox(
        "Property Age",
        sorted(df['agePossession'].unique())
    )

    furnishing_type = st.selectbox(
        "Furnishing Type",
        sorted(df['furnishing_type'].unique())
    )

    luxury_category = st.selectbox(
        "Luxury Category",
        sorted(df['luxury_category'].unique())
    )

    floor_category = st.selectbox(
        "Floor Category",
        sorted(df['floor_category'].unique())
    )

    servant_room = st.selectbox(
        "Servant Room",
        [0,1]
    )

    store_room = st.selectbox(
        "Store Room",
        [0,1]
    )

st.divider()

if st.button("🔍 Predict Price", use_container_width=True):

    data = [[
        property_type,
        sector,
        bedrooms,
        bathroom,
        balcony,
        property_age,
        built_up_area,
        float(servant_room),
        float(store_room),
        furnishing_type,
        luxury_category,
        floor_category
    ]]

    columns = [
        'property_type',
        'sector',
        'bedRoom',
        'bathroom',
        'balcony',
        'agePossession',
        'built_up_area',
        'servant room',
        'store room',
        'furnishing_type',
        'luxury_category',
        'floor_category'
    ]

    one_df = pd.DataFrame(data, columns=columns)

    base_price = np.expm1(pipeline.predict(one_df))[0]

    low = base_price - 0.22
    high = base_price + 0.22

    st.success("#### Estimated Price")

    c1, c2, c3 = st.columns(3)

    c1.metric("Estimated Price", f"₹ {base_price:.2f} Cr")
    c2.metric("Lower Range", f"₹ {low:.2f} Cr")
    c3.metric("Upper Range", f"₹ {high:.2f} Cr")