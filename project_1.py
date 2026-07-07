import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

# setup page
st.set_page_config(
    page_title='Project 1', page_icon='📊', layout='wide'
)

# project description
st.header('Project 1')
st.markdown('**Collection and visualization of quotes for a financial asset.**')

### side bar

# Title
st.sidebar.header('Options Menu')

# text box to select the ticker
ticker = st.sidebar.text_input('Write the asset ticker here', value='VALE3.SA').upper()

# period selection
period_options = {
    'Last 30 days': 30, 
    'Last 60 days': 60, 
    'Last 200 days': 200
}
period = st.sidebar.selectbox('Select the period', list(period_options.keys()))

# get the number of days selected
days = period_options[period]

# candles interval select
interval_options = {
    'Daily': '1d',
    'Weekly': '1wk',
    'Hour by hour': '1h'
}
interval = st.sidebar.selectbox('Select the interval', list(interval_options.keys()))

# get the interval selected
interval_value = interval_options[interval]

# End data is date today and the start date is the number of days ago
end_date = datetime.today().date()
start_date = end_date - timedelta(days=days)

# Coleta as cotações do ativo
# Colect the ticker quotes
data = yf.Ticker(ticker).history(start=start_date, end=end_date, interval=interval_value)

# Check if there is available data
if not data.empty:
    # Plot a candles chart using the Plotly library
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=data.index, 
                open=data['Open'], 
                high=data['High'], 
                low=data['Low'], 
                close=data['Close']
            )
        ]
    )

    # Add the title for the chart and set up the layout
    fig.update_layout(
        title={
            'text': f'Quotes for the asset {ticker} over the last {days} ({interval})',
            'x': 0.5,  # centralize the title in horizontal way
            'xanchor': 'center',  #set up the anchor point to the centre
        },
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis={
            'rangeslider': {'visible': False},  # Hide the ranger slider
                                                # The range slider prevents effective selection of the chart (without zoom),
                                                # So keep it hidden.
        }            
    )

     # Exhibit the chart
    st.plotly_chart(fig)
else:
    st.error(f'No data was found for the asset {ticker} for the selected period.')

 # Add the footnote with instagram link. Very useful to disclose your page
st.sidebar.markdown('''
    <p style="margin-top: 30px; text-align: center">
        My Python project to the financial market<br>
    </p>
''', unsafe_allow_html=True)

