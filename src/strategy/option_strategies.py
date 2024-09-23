# strategy/option_strategies.py

import pandas as pd
import numpy as np
from datetime import datetime,timezone
from dataclass import Option

class OptionStrategies:
    def __init__(self, strike, premium, expiration):
        '''
        Initialize parameters.
        :param strike: Strike price of the option
        :param premium: Paid premium for the option
        :param expiration: Expiration date of the option (YYYY-MM-DD format)
        '''

        if not isinstance(strike, (int, float)):
            raise ValueError("Strike price must be a number.")
        if not isinstance(premium, (int, float)):
            raise ValueError("Premium must be a number.")
        if isinstance(expiration,str):
            try:
                expiration = datetime.strptime(expiration, '%Y-%m-%d')
            except:
                raise ValueError("Expiration date must be in YYYY-MM-DD format.")
        if current_time is None:
            current_time = datetime.now(timezone.utc)

        self.strike = strike
        self.premium = premium
        self.expiration = expiration.replace(tzinfo=timezone.utc)
        self.current = current_time

    def expired(self) -> bool:
        '''Check if the option has expired.'''
        return self.current > self.expiration

    def long_call(self, spot):
        '''
        Calculate payoff for a long call option.
        
        Args:
            spot (float): The current spot price of the underlying asset
            
        Returns:
            float: The net payoff from the call option  
        '''
        if self.expired():
            return "You cannot enter this expired Option."
        intrinsic_value = max(0, spot - self.strike)
        net_payoff = intrinsic_value - self.premium
        return net_payoff         #range(-prem, ∞)

    def long_put(self, spot):
        '''
        Calculate payoff for a long put strategy:
        
        Args:
            spot (float): The current spot price of the underlying asset
            
        Returns:
            float: The net payoff from the put option  
        '''
        if self.expired():
            return "You cannot enter this expired Option."
        intrinsic_value = max(0, spot - self.strike)
        net_payoff = intrinsic_value - self.premium
        return net_payoff  # Profit if the spot is lower than the strike

    def bull_call_spread(self, spot, lower_strike, upper_strike, lower_premium, upper_premium):
        '''
        Bull Call Spread Strategy:
        - Buy a call with a lower strike, sell a call with a higher strike.
        '''
        net_premium = lower_premium - upper_premium  # Net premium received/spent
        if self.expired():
            return -net_premium
        if spot < lower_strike:
            return -net_premium  # Loss of net premium if below lower strike
        elif lower_strike <= spot <= upper_strike:
            return (spot - lower_strike) - net_premium  # Profit if spot is between the two strikes
        return (upper_strike - lower_strike) - net_premium  # Maximum profit if above upper strike

    def bear_call_spread(self, spot, lower_strike, upper_strike, lower_premium, upper_premium):
        '''
        Bear Call Spread Strategy:
        - Sell a call with a lower strike, buy a call with a higher strike.
        '''
        net_premium = lower_premium - upper_premium
        if self.expired():
            return -net_premium
        if spot < lower_strike:
            return net_premium  # Profit if below lower strike
        elif spot > upper_strike:
            return net_premium - (spot - upper_strike)  # Loss if above upper strike
        return net_premium - (spot - lower_strike)  # Partial profit if between strikes

class OptionStrategies:
    def __init__(self, strike: float, premium: float, expiration: str, current_time: datetime = None):
        if isinstance(expiration, str):
            self.expiration = datetime.strptime(expiration, '%Y-%m-%d').replace(tzinfo=timezone.utc)
        else:
            self.expiration = expiration
        self.strike = strike
        self.premium = premium
        self.current = current_time if current_time else datetime.now(timezone.utc)

    def expired(self) -> bool:
        '''Check if the option has expired.'''
        return self.current > self.expiration

# ------------------------- Strategies --------------------------------------

    def long_call(self, spot: float) -> float:
        '''Buy a call option to profit from rising prices.'''
        if self.expired():
            return -self.premium
        return max(spot - self.strike, 0) - self.premium

    def long_put(self, spot: float) -> float:
        '''Buy a put option to profit from falling prices.'''
        if self.expired():
            return -self.premium
        return max(self.strike - spot, 0) - self.premium

    def short_call(self, spot: float) -> float:
        '''Sell a call option to profit from falling or stagnant prices.'''
        if self.expired():
            return self.premium
        return min(self.premium - (spot - self.strike), self.premium)

    def short_put(self, spot: float) -> float:
        '''Sell a put option to profit from rising or stagnant prices.'''
        if self.expired():
            return self.premium
        return min(self.premium - (self.strike - spot), self.premium)

    def long_straddle(self, spot: float) -> float:
        '''Buy both a call and a put at the same strike, profiting from significant price moves in either direction.'''
        return self.long_call(spot) + self.long_put(spot)

    def short_straddle(self, spot: float) -> float:
        '''Sell both a call and a put at the same strike, profiting from low volatility and price staying near the strike.'''
        return self.short_call(spot) + self.short_put(spot)

    def long_synthetic(self, spot: float) -> float:
        '''Buy a Call and sell a Put at the same Strike price, with same underlying security and expiration month'''
        return self.long_call(spot) + self.short_put(spot)

    def short_synthetic(self, spot: float) -> float:
        '''Simulate a short position in the stock using options. Equivalent to selling a call and buying a put.'''
        return self.short_call(spot) + self.long_put(spot)

    def bull_call_spread(self, spot: float) -> float:
        '''Long ITM Call (lower strike) and Short OTM Call (higher strike)'''
        return self.long_call(spot) - self.short_call(spot + 10)

    def bull_put_spread(self, spot: float) -> float:
        '''Long OTM Put (lower strike) and Short ITM Call (higher strike)'''
        return self.short_put(spot) + self.long_put(spot - 10)

    def bear_call_spread(self, spot: float) -> float:
        '''A vertical spread intended to profit from a decline in the price of the underlying asset.'''
        return self.short_call(spot) + self.long_call(spot + 10)

    def bear_put_spread(self, spot: float) -> float:
        '''A vertical spread designed to profit from a drop in the price of the underlying asset.'''
        return self.long_put(spot) - self.short_put(spot - 10)

    def call_backspread(self, spot: float) -> float:
        '''Selling one call option and buying more call options at a higher strike, benefiting from rising markets.'''
        return -2 * self.short_call(spot) + 3 * self.long_call(spot + 10)

    def put_backspread(self, spot: float) -> float:
        '''Selling one put option and buying more put options at a lower strike, profiting from falling markets.'''
        return -2 * self.short_put(spot) + 3 * self.long_put(spot - 10)

    def long_combo(self, spot: float) -> float:
        '''A synthetic long position using options, combining a long call and a short put at different strikes.'''
        return self.long_call(spot + 10) + self.short_put(spot - 10)

    def long_strangle(self, spot: float) -> float:
        '''Buying a call and a put with different strikes, profiting from large movements in either direction.'''
        return self.long_call(spot + 10) + self.long_put(spot - 10)

    def short_strangle(self, spot: float) -> float:
        '''Selling a call and a put with different strikes, profiting from price stability near the strikes.'''
        return self.short_call(spot + 10) + self.short_put(spot - 10)

    def strap(self, spot: float) -> float:
        '''A bullish version of a straddle, involves buying two calls for every put bought.'''
        return 2 * self.long_call(spot) + self.long_put(spot)

    def strip(self, spot: float) -> float:
        '''A bearish version of a straddle, involves buying two puts for every call bought.'''
        return self.long_call(spot) + 2 * self.long_put(spot)

    def long_call_butterfly(self, spot: float) -> float:
        '''Buying one in-the-money call, selling two at-the-money calls, and buying one out-of-the-money call.'''
        itm_call = self.long_call(spot - 10)
        atm_calls = 2 * self.short_call(spot)
        otm_call = self.long_call(spot + 10)
        return itm_call - atm_calls + otm_call

    def long_put_butterfly(self, spot: float) -> float:
        '''Buying one in-the-money put, selling two at-the-money puts, and buying one out-of-the-money put.'''
        itm_put = self.long_put(spot + 10)
        atm_puts = 2 * self.short_put(spot)
        otm_put = self.long_put(spot - 10)
        return itm_put - atm_puts + otm_put

    def covered_call(self, spot: float) -> float:
        '''Selling a call option on a stock owned to generate income and potentially sell the stock at a higher price.'''
        owned_stock_profit = spot - self.strike
        call_option = self.short_call(spot)
        return owned_stock_profit + call_option

    def covered_put(self, spot: float) -> float:
        '''Selling a put option on a stock shorted to generate income and potentially repurchase the stock at a lower price.'''
        shorted_stock_profit = self.strike - spot
        put_option = self.short_put(spot)
        return shorted_stock_profit + put_option

    def collar(self, spot: float) -> float:
        '''Buying a put and selling a call to limit the range of possible returns, usually on a stock owned.'''
        owned_stock_profit = spot - self.strike
        put_option = self.long_put(spot)
        call_option = self.short_call(spot)
        return owned_stock_profit + put_option + call_option
