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

    preprocessor = pipeline[:-1]
    regressor = pipeline[-1]

    X_transformed = preprocessor.transform(one_df)

    tree_preds_log = np.array([
        tree.predict(X_transformed) for tree in regressor.estimators_
    ]).flatten()

    tree_preds_price = np.expm1(tree_preds_log)

    base_price = tree_preds_price.mean()
    low = np.percentile(tree_preds_price, 5)
    high = np.percentile(tree_preds_price, 95)

    st.success("#### Estimated Price")

    c1, c2, c3 = st.columns(3)

    c1.metric("Estimated Price", f"₹ {base_price:.2f} Cr")
    c2.metric("Lower Range (5th %ile)", f"₹ {low:.2f} Cr")
    c3.metric("Upper Range (95th %ile)", f"₹ {high:.2f} Cr")

    st.caption(
        "Range reflects the spread of predictions across the Random Forest's "
        "individual trees, not a fixed margin."
    )
