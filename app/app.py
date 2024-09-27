import sys
import os
import numpy as np
import plotly.graph_objects as go
import json
import streamlit as st
from datetime import datetime

# Add the parent directory to the system path for importing the module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from option_strategies import OptionStrategies

# Load strategy insights from JSON file
with open(os.path.join(os.path.dirname(__file__), '..', 'src', 'strategies_info.json'), 'r') as file:
    strategy_info = json.load(file)

st.title('Options Strategy Visualizer')
st.sidebar.header('Strategy Selection')

# Categorize strategies into Basic and Advanced
categories = {'Basic': [], 'Advanced': []}
for key, value in strategy_info.items():
    categories[value['Category']].append(key)

# User selects the strategy type
strategy_type = st.sidebar.selectbox('Choose Strategy Type', ['Basic', 'Advanced'])

# Display the corresponding strategies based on user selection
strategy_name = st.sidebar.selectbox('Select a Strategy', categories[strategy_type])

# Initialize user input variables for strategy parameters
spot_price = st.sidebar.number_input('Spot Price', value=100.0)
strike_price = st.sidebar.number_input('Strike Price', value=40.0)  # User-defined strike price

# Define the range of spot prices dynamically based on strike price
range_multiplier = 1.5
lower_bound = max(0, strike_price - strike_price * range_multiplier)
upper_bound = strike_price + strike_price * range_multiplier

# Dynamic range of spot prices for plotting
spot_prices = np.linspace(lower_bound, upper_bound, 300)

# Initialize the strategy object dynamically based on user inputs
strategies = OptionStrategies(strike=strike_price)

premium = st.sidebar.number_input('Premium', value=10.0)  # For single-leg strategies

# Displaying the selected strategy insights
info = strategy_info[strategy_name]
# st.write(f"### Strategy Insights: {strategy_name}")
st.write(f"**Investor View:** {info['Investor View']}")
st.write(f"**Risk:** {info['Risk']}")
st.write(f"**Reward:** {info['Reward']}")
st.write(f"**Breakeven:** {info['Breakeven'].replace('\\n', '<br>')}", unsafe_allow_html=True)

# Plot configuration using conditional fill
fig = go.Figure()

if strategy_name == 'Bull Call Spread':
    lower_strike = st.sidebar.number_input('Lower Strike Price', value=strike_price - 10)
    upper_strike = st.sidebar.number_input('Upper Strike Price', value=strike_price + 10)
    lower_premium = st.sidebar.number_input('Lower Premium', value=5.0)
    upper_premium = st.sidebar.number_input('Upper Premium', value=1.0)
    
    # Calculating individual leg payoffs
    long_call_payoffs = np.vectorize(lambda spot: strategies.long_call(spot, lower_strike, lower_premium))(spot_prices)
    short_call_payoffs = np.vectorize(lambda spot: strategies.short_call(spot, upper_strike, upper_premium))(spot_prices)
    total_payoffs = long_call_payoffs + short_call_payoffs
    
    # Adding individual legs to the plot
    fig.add_trace(go.Scatter(x=spot_prices, y=long_call_payoffs, mode='lines', name='Long Call Leg', line=dict(color='blue', width=2)))
    fig.add_trace(go.Scatter(x=spot_prices, y=short_call_payoffs, mode='lines', name='Short Call Leg', line=dict(color='purple', width=2)))

else:
    # Default to long call if no strategy selected
    payoffs = np.vectorize(lambda spot: strategies.long_call(spot, premium))(spot_prices)
    fig.add_trace(go.Scatter(x=spot_prices, y=payoffs, mode='lines', name='Total Payoff', line=dict(color='green', width=3)))

# Adjust the plot to include all lines
y_min = np.min([long_call_payoffs.min(), short_call_payoffs.min(), total_payoffs.min()]) - 10
y_max = np.max([long_call_payoffs.max(), short_call_payoffs.max(), total_payoffs.max()]) + 10

# Plotting profits (above zero)
fig.add_trace(go.Scatter(x=spot_prices, y=np.maximum(payoffs, 0), mode='lines', name='Profit', line=dict(color='green', width=3), fill='tozeroy'))

# Plotting losses (below zero)
fig.add_trace(go.Scatter(x=spot_prices, y=np.minimum(payoffs, 0), mode='lines', name='Loss', line=dict(color='red', width=3), fill='tozeroy'))

fig.update_layout(
    title=f"Payoff Diagram for {strategy_name}",
    xaxis_title='Spot Price',
    yaxis_title='Payoff',
    yaxis_range=[y_min, y_max],
    plot_bgcolor='white'
)

st.plotly_chart(fig, use_container_width=True)