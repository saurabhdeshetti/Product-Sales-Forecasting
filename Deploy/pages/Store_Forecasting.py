import streamlit as st
from services.individual_store import forecast
import plotly.express as px
import pandas as pd

st.set_page_config(layout="wide")
st.title("Individual Store Forecasting")
st.image("./deploy/img/sales-forecasting.svg", use_container_width=True)
# train_data = pd.read_parquet("deploy/data/train_data.parquet")
st.markdown("###")
with st.form(key='forecast_form', border=True):
    col1, col2 = st.columns([3, 1], vertical_alignment="bottom")

    with col1:
        store_id = st.number_input(
            "Select a Store ID between 1 to 365", min_value=1, max_value=365, value=3)

    with col2:
        forecast_btn = st.form_submit_button(
            "Forecast", use_container_width=True, type="primary")

if forecast_btn:
    with st.spinner("Forecasting Sales..."):
        forecast_data = forecast(
            Store_id=store_id, days=60)
        forecast_data.index = forecast_data["Date"]
        fig = px.line(forecast_data, x=forecast_data.index, y="Sales",

                      color="Type",
                      color_discrete_map={
                          "Current": "#03a9f4",
                          "Forecasted": "#4caf50"
                      })
        fig.update_xaxes(title_text="Date")
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_layout(
            height=600,
            title={
                'text': f"Sales Forecast for Store {store_id}",
                'font': {
                    'size': 24
                }
            },
            legend=dict(
                orientation="h",
                yanchor="top",
                y=1.15,
                xanchor="right",
                x=1
            ),
            margin=dict(l=0, r=0, t=100, b=0)
        )
        st.plotly_chart(fig)
        st.divider()


st.subheader("Technical Details")

details = """
- **Model Used**: LightGBM
- **Forecasting Method**: Recursive Forecasting
  This method uses the last 30 days of sales data to forecast the next day's
  sales. The forecasted sales are then used to forecast the next day's sales.
- **Feature Engineering**
  - Target Encoding: Store_id
  - Lag Features: 1, 7, 12, 30 days lag features
  - Rolling Window Features: 7, 12, 30 days exponential weighted moving average, standard deviation, min, max values
  - Date Features: Cyclical Day, Week, Month, Quarter features
  - Other Features: Is_Holiday, Is_Weekend
"""

st.markdown(details)
st.divider()
st.subheader("Try Other Forecasting Types")


st.markdown(
    """
<style>
button[kind="secondary"] {
    min-height: 3rem!important;
}
button[kind="secondary"] p {
    font-size: 1.1rem;
}
</style>
""",
    unsafe_allow_html=True,
)


col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("Regional Forecasting",  use_container_width=True, icon=":material/group_work:",  type="secondary"):
        st.switch_page("pages/Regional_Forecasting.py")

with col2:
    if st.button("Global Forecasting",  use_container_width=True, icon=":material/language:",  type="secondary"):
        st.switch_page("pages/Global_Forecasting.py")

with col3:
    if st.button("Home", use_container_width=True, icon=":material/home:", type="secondary"):
        st.switch_page("Home.py")
