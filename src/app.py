# import streamlit as st
# import numpy as np
# import matplotlib.pyplot as plt
# from strategy.option_strategies import OptionStrategies
# from datetime import datetime, timedelta

# st.title('Options Strategy Visualizer')

# # Select an option strategy
# strategy_name = st.selectbox(
#     'Select an Options Strategy',
#     ('Long Call', 'Long Put', 'Bull Call Spread', 'Bear Call Spread')
# )

# # Input method for expiration
# exp_method = st.radio(
#     "Specify expiration by:",
#     ('Date', 'Number of Days')
# )

# if exp_method == 'Date':
#     expiration = st.date_input('Expiration Date', min_value=datetime.now())
#     st.write('Current Date: ', datetime.now().date())
# else:
#     days_until_expiration = st.number_input('Days until Expiration', min_value=0, max_value=365, step=1)
#     expiration = datetime.now() + timedelta(days=days_until_expiration)

# # Common inputs for all strategies
# strike = st.number_input('Strike Price', value=100, step=1)
# premium = st.number_input('Premium Paid', value=10.0, min_value=0.0, max_value=1000.0, step=0.1)
# spot_range_factor = 0.5  # Adjust this factor based on typical price ranges observed
# spot_prices = np.linspace(max(0, strike - strike * spot_range_factor), strike + strike * spot_range_factor, 300)

# # Optional additional inputs
# volume = st.number_input('Volume (Number of Contracts)', min_value=1, max_value=1000, value=1, step=1, format='%d')

# strategy = OptionStrategies(strike, premium, expiration.strftime('%Y-%m-%d'))

# # Plotting setup
# fig, ax = plt.subplots()

# # Strategy-specific inputs and calculations
# if strategy_name == 'Long Call' or strategy_name == 'Long Put':
#     if strategy_name == 'Long Call':
#         payoffs = np.array([strategy.long_call(spot) * volume for spot in spot_prices])
#     else:
#         payoffs = np.array([strategy.long_put(spot) * volume for spot in spot_prices])
#     ax.plot(spot_prices, payoffs, label=f'{strategy_name} Payoff')


# elif strategy_name in ('Bull Call Spread', 'Bear Call Spread'):
#     lower_strike = st.number_input('Lower Strike Price', value=strike-10, step=1)
#     upper_strike = st.number_input('Upper Strike Price', value=strike+10, step=1)
#     lower_premium = st.number_input('Lower Premium Paid', value=premium, min_value=0.0, max_value=1000.0, step=0.1)
#     upper_premium = st.number_input('Upper Premium Paid', value=float(premium)/2, min_value=0.0, max_value=1000.0, step=0.1)
    
#     # Calculate individual leg payoffs
#     lower_call_payoffs = np.array([strategy.long_call_individual(spot, lower_strike, lower_premium) * volume for spot in spot_prices])
#     upper_call_payoffs = -np.array([strategy.long_call_individual(spot, upper_strike, upper_premium) * volume for spot in spot_prices])
    
#     if strategy_name == 'Bull Call Spread':
#         payoffs = lower_call_payoffs + upper_call_payoffs
#         # Plot each leg with lower opacity
#         ax.plot(spot_prices, lower_call_payoffs, 'r--', alpha=0.5, label='Lower Call Leg')
#         ax.plot(spot_prices, upper_call_payoffs, 'b--', alpha=0.5, label='Upper Call Leg')

#     ax.plot(spot_prices, payoffs, 'g-', label=f'{strategy_name} Payoff')

# # Enhancements to the plot
# ax.set_xlabel('Spot Price')
# ax.set_ylabel('Payoff')
# ax.axhline(0, color='gray', lw=1)
# ax.legend()

# st.pyplot(fig)

import streamlit as st
from strategy.option_strategies import OptionStrategies
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

st.title('Options Strategy Visualizer')
st.sidebar.header('Input Parameters')

# User input for the base parameters in the sidebar
strike = st.sidebar.number_input('Strike Price', value=100.0, step=0.5)
premium = st.sidebar.number_input('Premium', value=10.0, step=0.5)
expiration = st.sidebar.text_input('Expiration Date (YYYY-MM-DD)', value='2024-12-31')
spot_price = st.sidebar.number_input('Spot Price', value=100.0, step=0.5)

# Dropdown to select an options strategy
strategy_list = [
    'long call', 'long put', 'short call', 'short put', 'long straddle', 'short straddle',
    'long synthetic', 'short synthetic', 'bull call spread', 'bull put spread', 
    'bear call spread', 'bear put spread', 'call backspread', 'put backspread',
    'long combo', 'long strangle', 'short strangle', 'strap', 'strip', 
    'long call butterfly', 'long put butterfly', 'covered call', 'covered put', 'collar'
]
selected_strategy = st.sidebar.selectbox('Choose an options strategy', strategy_list)

# Initialize the strategy object
strategies = OptionStrategies(strike, premium, expiration)

# Setup dynamic inputs based on selected strategy if necessary
additional_strike = additional_premium = 0
if 'spread' in selected_strategy or 'backspread' in selected_strategy or 'butterfly' in selected_strategy:
    additional_strike = st.sidebar.number_input('Additional Strike Price', value=110.0)
    additional_premium = st.sidebar.number_input('Additional Premium', value=5.0)

# Function mapping with lambda to handle additional parameters
strategy_function_map = {
    'long call': lambda x: strategies.long_call(x),
    'long put': lambda x: strategies.long_put(x),
    'short call': lambda x: strategies.short_call(x),
    'short put': lambda x: strategies.short_put(x),
    'long straddle': lambda x: strategies.long_straddle(x),
    'short straddle': lambda x: strategies.short_straddle(x),
    'long synthetic': lambda x: strategies.long_synthetic(x),
    'short synthetic': lambda x: strategies.short_synthetic(x),
    'bull call spread': lambda x: strategies.bull_call_spread(x, strike, premium, additional_strike, additional_premium),
    'bull put spread': lambda x: strategies.bull_put_spread(x, strike, premium, additional_strike, additional_premium),
    'bear call spread': lambda x: strategies.bear_call_spread(x, strike, premium, additional_strike, additional_premium),
    'bear put spread': lambda x: strategies.bear_put_spread(x, strike, premium, additional_strike, additional_premium),
    'call backspread': lambda x: strategies.call_backspread(x, strike, additional_strike, premium, additional_premium),
    'put backspread': lambda x: strategies.put_backspread(x, strike, additional_strike, premium, additional_premium),
    'long combo': lambda x: strategies.long_combo(x, strike, additional_strike, premium),
    'long strangle': lambda x: strategies.long_strangle(x, strike, additional_strike, premium),
    'short strangle': lambda x: strategies.short_strangle(x, strike, additional_strike, premium),
    'strap': lambda x: strategies.strap(x),
    'strip': lambda x: strategies.strip(x),
    'long call butterfly': lambda x: strategies.long_call_butterfly(x, strike, additional_strike, premium, additional_premium),
    'long put butterfly': lambda x: strategies.long_put_butterfly(x, strike, additional_strike, premium, additional_premium),
    'covered call': lambda x: strategies.covered_call(x, strike, premium),
    'covered put': lambda x: strategies.covered_put(x, strike, premium),
    'collar': lambda x: strategies.collar(x, strike, additional_strike, premium, additional_premium)
}

# Function mapping for strategy calculations
def get_strategy_payoffs(spot_range):
    if selected_strategy == 'bull call spread':
        leg1_payoffs = np.vectorize(lambda x: strategies.long_call(x, strike, premium))(spot_range)
        leg2_payoffs = np.vectorize(lambda x: strategies.short_call(x, strike + 10, premium / 2))(spot_range)
        total_payoffs = leg1_payoffs + leg2_payoffs
        return total_payoffs, [leg1_payoffs, leg2_payoffs]
    # Add more strategies here similarly
    return None, []

# Plotting function using Plotly
def plot_strategy(spot_range, total_payoffs, leg_payoffs):
    fig = go.Figure()
    # Plot individual legs
    leg_colors = ['rgba(255,0,0,0.5)', 'rgba(0,0,255,0.5)']  # Define more colors as needed
    for i, leg in enumerate(leg_payoffs):
        fig.add_trace(go.Scatter(x=spot_range, y=leg, mode='lines', line=dict(color=leg_colors[i], dash='dash'), name=f'Leg {i+1}'))
    # Plot total payoff
    fig.add_trace(go.Scatter(x=spot_range, y=total_payoffs, mode='lines', line=dict(color='green', width=3), name='Total Payoff'))
    fig.update_layout(title='Payoff Diagram', xaxis_title='Spot Price', yaxis_title='Payoff', plot_bgcolor='white')
    st.plotly_chart(fig, use_container_width=True)

# Respond to changes in input
def update_graph():
    spot_range = np.linspace(spot_price - 50, spot_price + 50, 400)
    total_payoffs, leg_payoffs = get_strategy_payoffs(spot_range)
    plot_strategy(spot_range, total_payoffs, leg_payoffs)

update_graph()