import streamlit as st

st.set_page_config(layout="wide", page_title="Sales Forecasting")

st.title("Sales Forecasting")

st.image("./deploy/img/sales-forecasting.svg", use_container_width=True)

st.subheader("About the App")

string = """
Welcome to the Sales Forecasting App. This app uses a time series
forecasting model to predict future sales. The model is trained on the
sales data of a multiple retail stores. The data consists of daily
sales of a store for a period of 1 year and 5 months.

I have divided the forecasting into 3 parts:

1. Global Forecasting: This part of the app predicts the sales of
all the stores combined.
1. Regional Forecasting: This part of the app predicts the combined sales of
each region.
1. Store Forecasting: This part of the app predicts the sales of
each store.
"""

st.markdown(string)

st.subheader("Choose Forecasting Type")

st.markdown(
    """
<style>
button[kind="primary"] {
    min-height: 3rem!important;
}
button[kind="primary"] p {
    font-size: 1.1rem;
}
</style>
""",
    unsafe_allow_html=True,
)


col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("Global Forecasting", use_container_width=True, icon=":material/language:", type="primary"):
        st.switch_page("pages/Global_Forecasting.py")

with col2:
    if st.button("Regional Forecasting",  use_container_width=True, icon=":material/group_work:",  type="primary"):
        st.switch_page("pages/Regional_Forecasting.py")

with col3:
    if st.button("Store Forecasting",  use_container_width=True, icon=":material/store:",  type="primary"):
        st.switch_page("pages/Store_Forecasting.py")
