import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import pickle
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.set_page_config(page_title='Plotting Demo')

st.title('Analytics')

#-------------------------------------------------
st.header('Sector Price per Sqft Geomap')
new_df=pd.read_csv('datasets/data_viz1.csv')
group_df = new_df.groupby('sector').mean(numeric_only=True)[['price','price_per_sqft','built_up_area','latitude','longitude']]
fig = px.scatter_mapbox(group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
                  color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                  mapbox_style="open-street-map",width=1800,height=700,hover_name=group_df.index)
st.plotly_chart(fig,use_container_width=True)

#----------------------------------------------------
st.header('Features WordCloud')
wordcloud_df = pickle.load(open('datasets/sector_features.pkl', 'rb'))
sector_options = sorted(
    new_df["sector"].unique(),
    key=lambda x: (x != "sohna",
                   int(x.split()[1]) if x.startswith("sector") else float("inf"))
)
sector_options.insert(0, 'overall')
selected_sector = st.selectbox(
    "Select Sector for WordCloud",
    sector_options
)
if selected_sector == "overall":
    feature_text = " ".join(wordcloud_df.values())
else:
    feature_text = wordcloud_df[selected_sector]
wordcloud = WordCloud(
    width=1000,
    height=1000,
    background_color=None,
    mode="RGBA",
    stopwords={'s'},
    colormap="viridis",
    prefer_horizontal=0.85,
    random_state=42
).generate(feature_text)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(wordcloud.to_array(), width=700)

#----------------------------------------------------------------
st.header('Area Vs Price')
property_type = st.selectbox('Select Property Type', ['flat','house'])
if property_type == 'house':
    fig1 = px.scatter(new_df[new_df['property_type'] == 'house'], x="built_up_area", y="price", color="bedRoom", title="Area Vs Price")
    st.plotly_chart(fig1, use_container_width=True)
else:
    fig1 = px.scatter(new_df[new_df['property_type'] == 'flat'], x="built_up_area", y="price", color="bedRoom",title="Area Vs Price")
    st.plotly_chart(fig1, use_container_width=True)

#---------------------------------------------------------
st.header('BHK Pie Chart')
selected_sector1 = st.selectbox('Select Sector', sector_options)
if selected_sector1 == 'overall':
    fig2 = px.pie(new_df, names='bedRoom')
    st.plotly_chart(fig2, use_container_width=True)
else:
    fig2 = px.pie(new_df[new_df['sector'] == selected_sector1], names='bedRoom')
    st.plotly_chart(fig2, use_container_width=True)

#---------------------------------------------------------------
st.header('Side by Side BHK price comparison')
fig3 = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price', title='BHK Price Range')
st.plotly_chart(fig3, use_container_width=True)

#-----------------------------------------------------------
import plotly.figure_factory as ff
house = new_df[new_df['property_type'] == 'house']['price']
flat = new_df[new_df['property_type'] == 'flat']['price']
fig = ff.create_distplot(
    [house, flat],
    ['House', 'Flat'],
    show_hist=True,
    show_curve=True,
    show_rug=False
)
st.plotly_chart(fig, use_container_width=True)

#---------------------------------------------------------
st.header("Top 10 Most Expensive Sectors")
top_sector = (
    new_df.groupby("sector")["price_per_sqft"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
fig = px.bar(
    top_sector,
    x="price_per_sqft",
    y="sector",
    orientation="h",
    color="price_per_sqft",
    title="Average Price per Sq.ft"
)
fig.update_layout(yaxis=dict(categoryorder="total ascending"))
st.plotly_chart(fig, use_container_width=True)

#-------------------------------------------------------
st.header("Top 10 Affordable Sectors")
cheap_sector = (
    new_df.groupby("sector")["price_per_sqft"]
    .mean()
    .sort_values()
    .head(10)
    .reset_index()
)
fig = px.bar(
    cheap_sector,
    x="price_per_sqft",
    y="sector",
    orientation="h",
    color="price_per_sqft"
)
fig.update_layout(yaxis=dict(categoryorder="total ascending"))
st.plotly_chart(fig, use_container_width=True)

#-------------------------------------------------------------------
st.header("Property Type Distribution")
fig = px.histogram(
    new_df,
    x="property_type",
    color="property_type"
)
st.plotly_chart(fig, use_container_width=True)

#-------------------------------------------------------------------
st.header("Average Price by BHK")
avg_price = (
    new_df.groupby("bedRoom")["price"]
    .mean()
    .reset_index()
)
fig = px.line(
    avg_price,
    x="bedRoom",
    y="price",
    markers=True
)
st.plotly_chart(fig, use_container_width=True)

#-------------------------------------------------------------
with open('df.pkl','rb') as file:
    df = pickle.load(file)
st.header("Luxury Category")
fig = px.histogram(
        df,
    x="luxury_category",
    color="luxury_category"
)
st.plotly_chart(fig, use_container_width=True)

#----------------------------------------------------------------
st.header("Furnishing Type")
fig = px.pie(
    new_df,
    names="furnishing_type"
)
st.plotly_chart(fig, use_container_width=True)

#---------------------------------------------------
st.header("Correlation Heatmap")
corr = new_df[
    ["price",
     "price_per_sqft",
     "built_up_area",
     "bedRoom",
     "bathroom"]
].corr()
fig, ax = plt.subplots(figsize=(4.5, 4.5))
sns.heatmap(
    corr,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    square=True,
    linewidths=0.5,
    annot_kws={"size": 10},
    cbar_kws={"shrink": 0.8},
    ax=ax
)
plt.xticks(rotation=45, ha="right", fontsize=9)
plt.yticks(rotation=0, fontsize=9)
plt.tight_layout()
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.pyplot(fig)

#-------------------------------------------------------
st.header("Property Price Distribution")
fig = px.histogram(
    new_df,
    x="price",
    nbins=60
)
st.plotly_chart(fig, use_container_width=True)

#------------------------------------------------------
st.header("Feature Relationships")
fig = px.scatter_matrix(
    new_df,
    dimensions=[
        "price",
        "built_up_area",
        "price_per_sqft",
        "bathroom"
    ],
    color="property_type"
)
st.plotly_chart(fig, use_container_width=True)

#-----------------------------------------------------------------
st.header("Property Age vs Price")
age_df = (
    new_df.groupby("agePossession")["price"]
    .mean()
    .reset_index()
)
fig = px.bar(
    age_df,
    x="agePossession",
    y="price",
    color="price"
)
st.plotly_chart(fig, use_container_width=True)

#----------------------------------------------------------
st.header("Compare Two Sectors")
c1, c2 = st.columns(2)
sector1 = c1.selectbox(
    "Sector 1",
    sector_options
)
sector2 = c2.selectbox(
    "Sector 2",
    sector_options,
    index=1
)
compare = new_df[
    new_df["sector"].isin([sector1, sector2])
]
fig = px.box(
    compare,
    x="sector",
    y="price",
    color="sector"
)
st.plotly_chart(fig, use_container_width=True)

#------------------------------------------------------------
st.markdown("---")
st.subheader("📊 Market Summary")
c1, c2, c3, c4 = st.columns(4)
with c1:
    with st.container(border=True):
        st.metric("🏠 Properties", f"{len(new_df):,}")

with c2:
    with st.container(border=True):
        st.metric("📍 Sectors", new_df["sector"].nunique())

with c3:
    with st.container(border=True):
        st.metric("💰 Avg Price", f"{new_df['price'].mean():.2f} Cr")

with c4:
    with st.container(border=True):
        st.metric("📈 Avg Price/Sq.ft", f"₹ {int(new_df['price_per_sqft'].mean()):,}")