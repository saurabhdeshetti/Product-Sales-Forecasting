import streamlit as st
from services.individual_region import forecast
import plotly.express as px
import pandas as pd

st.set_page_config(layout="wide")
st.title("Individual Regions Forecasting")
st.image("./deploy/img/sales-forecasting.svg", use_container_width=True)
st.markdown("###")
with st.form(key='forecast_form', border=True):
    col1, col2 = st.columns([3, 1], vertical_alignment="bottom")

    with col1:
        region_code = st.selectbox(
            "Select a Region",
            ("R1", "R2", "R3", "R4"),
        )

    with col2:
        forecast_btn = st.form_submit_button(
            "Forecast", use_container_width=True, type="primary")

if forecast_btn:
    with st.spinner("Forecasting Sales..."):
        forecast_data = forecast(
            Region_Code=region_code, days=60)
        forecast_data.index = forecast_data["Date"]
        fig = px.line(forecast_data, x=forecast_data.index, y="Total_Sales",

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
                'text': f"Sales Forecast for Region {region_code}",
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
- **Model Used**: Prophet
- **Forecasting Method**: Batch Forecasting
- **Regressors**
    - Holidays
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
    if st.button("Home", use_container_width=True, icon=":material/home:", type="secondary"):
        st.switch_page("Home.py")

with col2:
    if st.button("Global Forecasting",  use_container_width=True, icon=":material/language:",  type="secondary"):
        st.switch_page("pages/Global_Forecasting.py")

with col3:
    if st.button("Store Forecasting",  use_container_width=True, icon=":material/store:",  type="secondary"):
        st.switch_page("pages/Store_Forecasting.py")
