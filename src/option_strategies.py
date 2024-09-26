import pandas as pd
import numpy as np
from datetime import datetime,timezone

class OptionStrategies:
    def __init__(self, strike):
        '''
        Args:
            strike (float): Strike price of the option
            premium (float): Paid premium for the option
            expiration (datetime): Expiration date of the option (YYYY-MM-DD format)
        '''

        if not isinstance(strike, (int, float)):
            raise ValueError("Strike price must be a number.")
        # if not isinstance(premium, (int, float)):
        #     raise ValueError("Premium must be a number.")

        self.strike = strike
        # premium = self.premium


    def long_call(self, spot, premium):
        '''
        Args:
            spot (float): The current spot price of the underlying asset
            
        Returns:
            net_payoff (float): The net payoff from the trade 
        '''
        intrinsic_value = max(0, spot - self.strike)
        net_payoff = intrinsic_value - premium
        return net_payoff         

    def long_put(self, spot, premium):
        '''
        Args:
            spot (float): The current spot price of the underlying asset
            
        Returns:
            net_payoff (float): The net payoff from the trade
        '''
        intrinsic_value = max(0, self.strike - spot)
        net_payoff = intrinsic_value - premium
        return net_payoff  # Profit if the spot is lower than the strike
    
    def short_call(self, spot, premium):
        '''
        Args:
            spot (float): The current spot price of the underlying asset
            
        Returns:
            net_payoff (float): The net payoff from the trade
        '''
        intrinsic_value = max(0, spot - self.strike)
        net_payoff = premium - intrinsic_value
        return net_payoff         
    
    def short_put(self, spot, premium):
        '''
        Args:
            spot (float): The current spot price of the underlying asset
        Returns:
            net_payoff (float): The net payoff from the trade
        '''
        intrinsic_value = max(0, self.strike - spot)
        net_payoff = premium - intrinsic_value
        return net_payoff
    
    def long_straddle(self, spot, call_premium, put_premium):
        '''
        Long both Call and Put at the same strike and same maturity.
        Profits made when undelrying shows volatility to cover cost of the trade.

        Args:
            spot (float): The current spot price of the underlying asset
            call_premium (float): The premium received for the short call option
            put_premium (float): The premium received for the short put option
        Returns:
            tuple: all the payoffs
        '''
        long_call_payoff = self.long_call(spot, call_premium)
        long_put_payoff = self.long_put(spot, put_premium)
        net_payoff = long_call_payoff + long_put_payoff
        return long_call_payoff, long_put_payoff, net_payoff
    
    def short_straddle(self, spot, call_premium, put_premium):
        '''
        Short both Call and Put at same strike and same expiry.
        Expects payoff characteristics similar to holding the stock. It has benefit of being much cheaper than buying the underlying outright.
        
        Args:
            spot (float): The current spot price of the underlying asset
            call_premium (float): The premium received for the short call option
            put_premium (float): The premium received for the short put option
        
        Returns:
            tuple: all the payoffs 
        '''
        short_call_payoff = self.short_call(spot, call_premium)
        short_put_payoff = self.short_put(spot, put_premium)
        net_payoff = short_call_payoff + short_put_payoff
        return short_call_payoff, short_put_payoff, net_payoff
    
    def long_synthetic(self, spot, call_premium, put_premium):
        '''
        Long Call and Short Put at the same strike and same maturity.
        Profits made when undelrying shows volatility to cover cost of the trade.

        Args:
            spot (float): The current spot price of the underlying asset
            call_premium (float): The premium received for the short call option
            put_premium (float): The premium received for the short put option
        Returns:
            tuple: all the payoffs
        '''
        long_call_payoff = self.long_call(spot, call_premium)
        short_put_payoff = self.short_put(spot, put_premium)
        net_payoff = long_call_payoff + short_put_payoff
        return long_call_payoff, short_put_payoff, net_payoff

    def short_synthetic(self, spot, call_premium, put_premium):
        '''
        Short Call and Long Put at same strike and same expiry.
        Behaves exactly like being short on underlying. 
        
        Args:
            spot (float): The current spot price of the underlying asset
            call_premium (float): The premium received for the short call option
            put_premium (float): The premium received for the short put option
        
        Returns:
            tuple: all the payoffs
        '''
        short_call_payoff = self.short_call(spot, call_premium)
        long_put_payoff = self.long_put(spot, put_premium)
        net_payoff = short_call_payoff + long_put_payoff
        return short_call_payoff, long_put_payoff, net_payoff

    def bull_call_spread(self, spot, lower_strike, upper_strike, lower_premium, upper_premium):
        '''
        Long Call with lower strike & Short Call with higher strike (short call)
        Args:
            spot (float): The current spot price of the underlying asset
            lower_strike (float): Strike price for the long call
            upper_strike (float): Strike price for the short call
            lower_premium (float): Premium paid for the long call
            upper_premium (float): Premium received for the short call
            
        Returns:
            tuple: all the payoffs
        '''
        
        self.strike = lower_strike
        long_call_payoff = self.long_call(spot, lower_premium)

        self.strike = upper_strike
        short_call_payoff = self.short_call(spot, upper_premium)

        net_payoff = long_call_payoff + short_call_payoff

        return long_call_payoff, short_call_payoff, net_payoff
    
    def bull_put_spread(self, spot, lower_strike, upper_strike, lower_premium, upper_premium):
        '''
        Long Put with lower strike & Short Put with higher strike
        Args:
            lower_strike (float): Strike price for the long put
            upper_strike (float): Strike price for the short put
            lower_premium (float): Premium paid for the long put
            upper_premium (float): Premium received for the short put
            
        Returns:
            tuple: all the payoffs
        '''
        self.strike = lower_strike
        long_put_payoff = self.long_put(spot, lower_premium)

        self.strike = upper_strike
        short_put_payoff = self.short_put(spot, upper_premium)

        net_payoff = long_put_payoff = short_put_payoff
        return long_put_payoff, short_put_payoff, net_payoff
    
    def bear_call_spread(self, spot, lower_strike, upper_strike, lower_premium, upper_premium):
        '''
        Short Call with lower strike & Long Call with higher strike 
        
        Args:
            spot (float): The current spot price of the underlying asset
            lower_strike (float): Strike price for the short call
            upper_strike (float): Strike price for the long call
            lower_premium (float): Premium received for the short call
            upper_premium (float): Premium paid for the long call
            
        Returns:
            tuple: Payoffs for short call, long call, and total net payoff
        '''
        self.strike = lower_strike
        short_call_payoff = self.short_call(spot, lower_premium)

        self.strike = upper_strike
        long_call_payoff = self.long_call(spot, upper_premium)

        net_payoff = short_call_payoff + long_call_payoff        
        return short_call_payoff, long_call_payoff, net_payoff

    def bear_call_spread(self, spot, lower_strike, upper_strike, lower_premium, upper_premium):
        '''
        Short put with lower strike & Long Put at higher strike
        
        Args:
            spot (float): The current spot price of the underlying asset
            lower_strike (float): Strike price for the short put
            upper_strike (float): Strike price for the long put
            lower_premium (float): Premium received for the short put
            upper_premium (float): Premium paid for the long put
        
        Returns:
            tuple: Payoffs for long put, short put, and total net payoff
        '''
        self.strike = upper_strike 
        long_put_payoff = self.long_put(spot, upper_premium)

        self.strike = lower_premium
        short_put_payoff = self.short_put(spot, lower_premium)

        net_payoff = long_put_payoff + short_put_payoff
        return short_put_payoff, long_put_payoff, net_payoff
    

    def call_backspread(self, spot, lower_strike, upper_strike, lower_premium, upper_premium):
        '''
        Short Call with with lower strike & Long 2 Calls with higher strike
        Works well for bullish market and/or bearish on market with bias to the upside

        Args:
            spot (float): The current spot price of the underlying asset
            lower_strike (float): Strike price for the short call
            upper_strike (float): Strike price for the long calls
            lower_premium (float): Premium received for the short call
            upper_premium (float): Premium paid for each long call
            
        Returns:
            tuple: Payoffs for short call, long calls, and total net payoff
        '''
        self.strike = lower_strike
        short_call_payoff = self.short_call(spot, lower_premium)

        self.strike = upper_strike
        long_call_payoff = 2 * self.long_call(spot, upper_premium)

        net_payoff = short_call_payoff + long_call_payoff

        return short_call_payoff, long_call_payoff, net_payoff

    def put_backspread(self, spot, lower_strike, upper_strike, lower_premium, upper_premium):
        '''
        Put Backspread Strategy:
        - Sell a put at a higher strike (short put).
        - Buy two puts at a lower strike (long puts).
        
        Args:
            spot (float): The current spot price of the underlying asset
            lower_strike (float): Strike price for the long puts
            upper_strike (float): Strike price for the short put
            lower_premium (float): Premium paid for each long put
            upper_premium (float): Premium received for the short put
            
        Returns:
            tuple: Payoffs for short put, long puts, and total net payoff
        '''
        self.strike = lower_strike
        short_put_payoff = self.short_put(spot, lower_premium)

        self.strike = upper_strike
        long_put_payoff = 2 * self.long_put(spot, upper_premium)

        net_payoff = short_put_payoff + long_put_payoff

        return short_put_payoff, long_put_payoff, net_payoff
    
    def long_combo(self, spot, lower_strike, upper_strike, call_premium, put_premium):
        '''
        Short Put at lower strike & Long Call at higher strike
        Quite similar to Long Synthetic (Short Put & Long Call same strike) but only with different strikes
        Args:
            spot (float): The current spot price of the underlying asset
            lower_strike (float): Strike price for the short put
            upper_strike (float): Strike price for the long call
            call_premium (float): Premium paid for the long call
            put_premium (float): Premium received for the short put
        
        Returns:
            tuple: Payoffs for long call, short put, and total net payoff
        '''
        self.strike = lower_strike
        short_put_payoff = self.short_put(spot, put_premium)

        self.strike = upper_strike
        long_call_payoff = 2 * self.long_call(spot, call_premium)

        net_payoff = short_put_payoff + long_call_payoff

        return short_put_payoff, long_call_payoff, net_payoff
    
    def long_strangle(self, spot, lower_strike, upper_strike, call_premium, put_premium):
        '''
        Long Put at lower strike & Long Call at higher strike
        
        Args:
            spot (float): The current spot price of the underlying asset
            lower_strike (float): Strike price for the long put
            upper_strike (float): Strike price for the long call
            call_premium (float): Premium paid for the long call
            put_premium (float): Premium paid for the long put
            
        Returns:
            tuple: Payoffs for long call, long put, and total net payoff
        '''
        self.strike = lower_strike
        long_put_payoff = self.long_put(spot, put_premium)

        self.strike = upper_strike
        long_call_payoff = self.long_call(spot, call_premium)

        net_payoff = long_call_payoff + long_put_payoff
        return long_put_payoff, long_call_payoff, net_payoff
    
    def short_strangle(self, spot, lower_strike, upper_strike, call_premium, put_premium):
        '''
        Short Put at lower strike & Short Call at higher strike

        Args:
            spot (float): The current spot price of the underlying asset
            lower_strike (float): Strike price for the short put
            upper_strike (float): Strike price for the short call
            call_premium (float): Premium received for the short call
            put_premium (float): Premium received for the short put
        
        Returns:
            tuple: Payoffs for short call, short put, and total net payoff
        '''
        self.strike = lower_strike
        short_put_payoff = self.short_put(spot, put_premium)

        self.strike = upper_strike
        short_call_payoff = self.short_call(spot, call_premium)

        net_payoff = short_put_payoff + short_call_payoff
        return short_put_payoff, short_call_payoff, net_payoff
    
    def strap(self, spot, call_premium, put_premium):
        '''
        Long 2 Calls & Long 1 Put at same strike
        
        Args:
            spot (float): The current spot price of the underlying asset
            strike (float): Strike price for both calls and the put
            call_premium (float): Premium paid for each long call
            put_premium (float): Premium paid for the long put
            
        Returns:
            tuple: Payoffs for long calls, long put, and total net payoff
        '''
        long_call_payoff = 2 * self.long_call(spot, call_premium)  # Buy two calls

        # Long one put at the same strike
        long_put_payoff = self.long_put(spot, put_premium)

        # Total net payoff is the sum of the two long calls and one long put
        net_payoff = long_call_payoff + long_put_payoff
    
        return long_call_payoff, long_put_payoff, net_payoff
    
    def strip(self, spot, call_premium, put_premium):
        '''
        Long 2 Puts & Long Call at same strike
        
        Args:
            spot (float): The current spot price of the underlying asset
            strike (float): Strike price for both puts and the call
            call_premium (float): Premium paid for the long call
            put_premium (float): Premium paid for each long put
            
        Returns:
            tuple: Payoffs for long call, long puts, and total net payoff
        '''
        long_call_payoff = self.long_call(spot, call_premium)
        long_put_payoff = 2 * self.long_put(spot, put_premium)

        net_payoff = long_call_payoff + long_put_payoff
        
        return long_call_payoff, long_put_payoff, net_payoff
    
    def long_call_ladder(self, spot, lower_strike, middle_strike, upper_strike, lower_premium, middle_premium, upper_premium):
        '''
        - Long a call at a lower strike price.
        - Short a call at a middle strike price.
        - Long a call at a higher strike price.
        
        Args:
            spot (float): The current spot price of the underlying asset
            lower_strike (float): Strike price for the lower call
            middle_strike (float): Strike price for the short call
            upper_strike (float): Strike price for the upper call
            lower_premium (float): Premium paid for the lower long call
            middle_premium (float): Premium received for the short middle call
            upper_premium (float): Premium paid for the upper long call
            
        Returns:
            tuple: Payoffs for lower long call, short middle call, upper long call, and total net payoff
        '''
        # Long call at lower strike
        self.strike = lower_strike
        lower_call_payoff = self.long_call(spot, lower_premium)

        # Short call at middle strike
        self.strike = middle_strike
        middle_call_payoff = self.short_call(spot, middle_premium)

        # Long call at upper strike
        self.strike = upper_strike
        upper_call_payoff = self.long_call(spot, upper_premium)

        net_payoff = lower_call_payoff + middle_call_payoff + upper_call_payoff
        
        return lower_call_payoff, middle_call_payoff, upper_call_payoff, net_payoff
    
    def long_put_ladder(self, spot, upper_strike, middle_strike, lower_strike, upper_premium, middle_premium, lower_premium):
        '''
        - Long a put at a higher strike price.
        - Short a put at a middle strike price.
        - Long a put at a lower strike price.
        
        Args:
            spot (float): The current spot price of the underlying asset
            upper_strike (float): Strike price for the upper put
            middle_strike (float): Strike price for the short middle put
            lower_strike (float): Strike price for the lower put
            upper_premium (float): Premium paid for the upper long put
            middle_premium (float): Premium received for the short middle put
            lower_premium (float): Premium paid for the lower long put
            
        Returns:
            tuple: Payoffs for upper long put, short middle put, lower long put, and total net payoff
        '''
        # Long put at upper strike
        self.strike = upper_strike
        upper_put_payoff = self.long_put(spot, upper_premium)

        # Short put at middle strike
        self.strike = middle_strike
        middle_put_payoff = self.short_put(spot, middle_premium)

        # Long put at lower strike
        self.strike = lower_strike
        lower_put_payoff = self.long_put(spot, lower_premium)

        net_payoff = upper_put_payoff + middle_put_payoff + lower_put_payoff
        
        return upper_put_payoff, middle_put_payoff, lower_put_payoff, net_payoff
    
    def short_call_ladder(self, spot, lower_strike, middle_strike, upper_strike, lower_premium, middle_premium, upper_premium):
        '''
        Short Call Ladder Strategy:
        - Short a call at a lower strike price.
        - Long a call at a middle strike price.
        - Long a call at a higher strike price.
        
        Args:
            spot (float): The current spot price of the underlying asset
            lower_strike (float): Strike price for the lower call
            middle_strike (float): Strike price for the middle call
            upper_strike (float): Strike price for the upper call
            lower_premium (float): Premium received for the short lower call
            middle_premium (float): Premium paid for the middle long call
            upper_premium (float): Premium paid for the upper long call
            
        Returns:
            tuple: Payoffs for lower short call, middle long call, upper long call, and total net payoff
        '''
        # Short call at lower strike
        self.strike = lower_strike
        lower_call_payoff = self.short_call(spot, lower_premium)

        # Long call at middle strike
        self.strike = middle_strike
        middle_call_payoff = self.long_call(spot, middle_premium)

        # Long call at upper strike
        self.strike = upper_strike
        upper_call_payoff = self.long_call(spot, upper_premium)

        # Total net payoff
        net_payoff = lower_call_payoff + middle_call_payoff + upper_call_payoff
        return lower_call_payoff, middle_call_payoff, upper_call_payoff, net_payoff    
    
    def short_call_ladder(self, spot, lower_strike, middle_strike, upper_strike, lower_premium, middle_premium, upper_premium):
        '''
        Short Call Ladder Strategy:
        - Sell a call at a lower strike price (short call).
        - Buy a call at a middle strike price (long call).
        - Buy a call at a higher strike price (long call).
        
        Args:
            spot (float): The current spot price of the underlying asset
            lower_strike (float): Strike price for the lower call
            middle_strike (float): Strike price for the middle call
            upper_strike (float): Strike price for the upper call
            lower_premium (float): Premium received for the short lower call
            middle_premium (float): Premium paid for the middle long call
            upper_premium (float): Premium paid for the upper long call
            
        Returns:
            tuple: Payoffs for lower short call, middle long call, upper long call, and total net payoff
        '''
        # Short call at lower strike
        self.strike = lower_strike
        lower_call_payoff = self.short_call(spot, lower_premium)

        # Long call at middle strike
        self.strike = middle_strike
        middle_call_payoff = self.long_call(spot, middle_premium)

        # Long call at upper strike
        self.strike = upper_strike
        upper_call_payoff = self.long_call(spot, upper_premium)

        # Total net payoff
        net_payoff = lower_call_payoff + middle_call_payoff + upper_call_payoff
        return lower_call_payoff, middle_call_payoff, upper_call_payoff, net_payoff
    
    def short_put_ladder(self, spot, upper_strike, middle_strike, lower_strike, upper_premium, middle_premium, lower_premium):
        '''
        Short Put Ladder Strategy:
        - Sell a put at a higher strike price (short put).
        - Buy a put at a middle strike price (long put).
        - Buy a put at a lower strike price (long put).
        
        Args:
            spot (float): The current spot price of the underlying asset
            upper_strike (float): Strike price for the upper put
            middle_strike (float): Strike price for the middle put
            lower_strike (float): Strike price for the lower put
            upper_premium (float): Premium received for the short upper put
            middle_premium (float): Premium paid for the middle long put
            lower_premium (float): Premium paid for the lower long put
            
        Returns:
            tuple: Payoffs for upper short put, middle long put, lower long put, and total net payoff
        '''
        # Short put at upper strike
        self.strike = upper_strike
        upper_put_payoff = self.short_put(spot, upper_premium)

        # Long put at middle strike
        self.strike = middle_strike
        middle_put_payoff = self.long_put(spot, middle_premium)

        # Long put at lower strike
        self.strike = lower_strike
        lower_put_payoff = self.long_put(spot, lower_premium)

        # Total net payoff
        net_payoff = upper_put_payoff + middle_put_payoff + lower_put_payoff
        return upper_put_payoff, middle_put_payoff, lower_put_payoff, net_payoff
    
    def long_call_butterfly(self, spot, lower_strike, middle_strike, upper_strike, lower_premium, middle_premium, upper_premium):
        '''
        Long Call Butterfly Strategy:
        - Buy a call at a lower strike price (long call).
        - Sell two calls at a middle strike price (short calls).
        - Buy a call at a higher strike price (long call).
        
        Args:
            spot (float): The current spot price of the underlying asset
            lower_strike (float): Strike price for the lower call
            middle_strike (float): Strike price for the middle short calls
            upper_strike (float): Strike price for the upper call
            lower_premium (float): Premium paid for the lower long call
            middle_premium (float): Premium received for the middle short calls
            upper_premium (float): Premium paid for the upper long call
            
        Returns:
            tuple: Payoffs for lower long call, middle short calls, upper long call, and total net payoff
        '''
        # Long call at lower strike
        self.strike = lower_strike
        lower_call_payoff = self.long_call(spot, lower_premium)

        # Short two calls at middle strike
        self.strike = middle_strike
        middle_call_payoff = 2 * self.short_call(spot, middle_premium)

        # Long call at upper strike
        self.strike = upper_strike
        upper_call_payoff = self.long_call(spot, upper_premium)

        # Total net payoff
        net_payoff = lower_call_payoff + middle_call_payoff + upper_call_payoff
        return lower_call_payoff, middle_call_payoff, upper_call_payoff, net_payoff
    
    def short_call_butterfly(self, spot, lower_strike, middle_strike, upper_strike, lower_premium, middle_premium, upper_premium):
        '''
        Short Call Butterfly Strategy:
        - Sell a call at a lower strike price (short call).
        - Buy two calls at a middle strike price (long calls).
        - Sell a call at a higher strike price (short call).
        
        Args:
            spot (float): The current spot price of the underlying asset
            lower_strike (float): Strike price for the lower call
            middle_strike (float): Strike price for the middle long calls
            upper_strike (float): Strike price for the upper call
            lower_premium (float): Premium received for the lower short call
            middle_premium (float): Premium paid for the middle long calls
            upper_premium (float): Premium received for the upper short call
            
        Returns:
            tuple: Payoffs for lower short call, middle long calls, upper short call, and total net payoff
        '''
        # Short call at lower strike
        self.strike = lower_strike
        lower_call_payoff = self.short_call(spot, lower_premium)

        # Long two calls at middle strike
        self.strike = middle_strike
        middle_call_payoff = 2 * self.long_call(spot, middle_premium)

        # Short call at upper strike
        self.strike = upper_strike
        upper_call_payoff = self.short_call(spot, upper_premium)

        # Total net payoff
        net_payoff = lower_call_payoff + middle_call_payoff + upper_call_payoff
        return lower_call_payoff, middle_call_payoff, upper_call_payoff, net_payoff
    
    def long_call_condor(self, spot, lower_strike, lower_middle_strike, upper_middle_strike, upper_strike, lower_premium, lower_middle_premium, upper_middle_premium, upper_premium):
        '''
        Long Call Condor Strategy:
        - Buy a call at a lower strike price (long call).
        - Sell a call at a lower middle strike price (short call).
        - Sell a call at an upper middle strike price (short call).
        - Buy a call at a higher strike price (long call).
        
        Args:
            spot (float): The current spot price of the underlying asset
            lower_strike (float): Strike price for the lower call
            lower_middle_strike (float): Strike price for the lower middle call
            upper_middle_strike (float): Strike price for the upper middle call
            upper_strike (float): Strike price for the higher call
            lower_premium (float): Premium paid for the lower long call
            lower_middle_premium (float): Premium received for the lower middle short call
            upper_middle_premium (float): Premium received for the upper middle short call
            upper_premium (float): Premium paid for the higher long call
            
        Returns:
            tuple: Payoffs for lower long call, lower middle short call, upper middle short call, higher long call, and total net payoff
        '''
        # Long call at lower strike
        self.strike = lower_strike
        lower_call_payoff = self.long_call(spot, lower_premium)

        # Short call at lower middle strike
        self.strike = lower_middle_strike
        lower_middle_call_payoff = self.short_call(spot, lower_middle_premium)

        # Short call at upper middle strike
        self.strike = upper_middle_strike
        upper_middle_call_payoff = self.short_call(spot, upper_middle_premium)

        # Long call at higher strike
        self.strike = upper_strike
        upper_call_payoff = self.long_call(spot, upper_premium)

        # Total net payoff
        net_payoff = lower_call_payoff + lower_middle_call_payoff + upper_middle_call_payoff + upper_call_payoff
        return lower_call_payoff, lower_middle_call_payoff, upper_middle_call_payoff, upper_call_payoff, net_payoff
    
    def short_call_condor(self, spot, lower_strike, lower_middle_strike, upper_middle_strike, upper_strike, lower_premium, lower_middle_premium, upper_middle_premium, upper_premium):
        '''
        Short Call Condor Strategy:
        - Sell a call at a lower strike price (short call).
        - Buy a call at a lower middle strike price (long call).
        - Buy a call at an upper middle strike price (long call).
        - Sell a call at a higher strike price (short call).
        
        Args:
            spot (float): The current spot price of the underlying asset
            lower_strike (float): Strike price for the lower short call
            lower_middle_strike (float): Strike price for the lower middle long call
            upper_middle_strike (float): Strike price for the upper middle long call
            upper_strike (float): Strike price for the higher short call
            lower_premium (float): Premium received for the lower short call
            lower_middle_premium (float): Premium paid for the lower middle long call
            upper_middle_premium (float): Premium paid for the upper middle long call
            upper_premium (float): Premium received for the higher short call
            
        Returns:
            tuple: Payoffs for lower short call, lower middle long call, upper middle long call, higher short call, and total net payoff
        '''
        # Short call at lower strike
        self.strike = lower_strike
        lower_call_payoff = self.short_call(spot, lower_premium)

        # Long call at lower middle strike
        self.strike = lower_middle_strike
        lower_middle_call_payoff = self.long_call(spot, lower_middle_premium)

        # Long call at upper middle strike
        self.strike = upper_middle_strike
        upper_middle_call_payoff = self.long_call(spot, upper_middle_premium)

        # Short call at higher strike
        self.strike = upper_strike
        upper_call_payoff = self.short_call(spot, upper_premium)

        # Total net payoff
        net_payoff = lower_call_payoff + lower_middle_call_payoff + upper_middle_call_payoff + upper_call_payoff
        return lower_call_payoff, lower_middle_call_payoff, upper_middle_call_payoff, upper_call_payoff, net_payoff