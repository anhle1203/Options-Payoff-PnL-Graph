import streamlit as st
import numpy as np
import plotly.graph_objects as go
from src.option_strategies import OptionStrategies
from datetime import datetime
import json

# Load strategy insights from JSON file
with open('strategies_info.json', 'r') as file:
    strategy_info = json.load(file)

st.title('Options Strategy Visualizer')
st.sidebar.header('Strategy Selection')

# User selects the strategy type
strategy_type = st.sidebar.selectbox('Choose Strategy Type', ['Basic', 'Advanced'])
strategy_name = st.sidebar.selectbox(
    'Select a Strategy',
    [key for key in strategy_info if ('Advanced' in key) == (strategy_type == 'Advanced')]
)

# User inputs
strike = st.sidebar.number_input('Strike Price', value=100.0)
premium = st.sidebar.number_input('Premium Paid', value=10.0)
multiplier = st.sidebar.number_input('Multiplier', value=100)
contracts = st.sidebar.number_input('Number of Contracts', value=1, min_value=1)
spot_price_range = st.sidebar.slider('Spot Price Range', 0, 200, (80, 120))

# Initialize the strategy
expiration = datetime.now().strftime('%Y-%m-%d')  # Assuming current date for simplicity
strategies = OptionStrategies(strike, premium, expiration)
strategy_func = getattr(strategies, strategy_name.replace(' ', '_').lower())

# Displaying the selected strategy insights
info = strategy_info[strategy_name]
st.write(f"### Strategy Insights: {strategy_name}")
st.write(f"**Investor View:** {info['Investor View']}")
st.write(f"**Risk:** {info['Risk']}")
st.write(f"**Reward:** {info['Reward']}")
st.write(f"**Breakeven:** {info['Breakeven']}")

# Calculate payoffs
spot_prices = np.linspace(*spot_price_range, 300)
payoffs = np.vectorize(strategy_func)(spot_prices) * multiplier * contracts

# Plot the results
fig = go.Figure(go.Scatter(x=spot_prices, y=payoffs, mode='lines'))
fig.update_layout(
    title=f"Payoff Diagram for {strategy_name}",
    xaxis_title='Spot Price',
    yaxis_title='Payoff',
    plot_bgcolor='white'
)
st.plotly_chart(fig, use_container_width=True)