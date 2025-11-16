# connect_ib_insync.py
import sys
import asyncio

# macOS Python 3.10+ asyncio fix (safe to include)
if sys.version_info >= (3, 10):
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())
        # ---------------------------
# Imports
# ---------------------------
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, IntSlider, Text, Checkbox
from ib_insync import IB, Option

# ---------------------------
# Option payoff function
# ---------------------------
def call_payoff(strike, premium, underlying, long=True, multiplier=1):
    if long:
        return multiplier * np.maximum(underlying - strike, 0) - premium * multiplier
    else:
        return premium * multiplier - multiplier * np.maximum(underlying - strike, 0)

def butterfly_payoff(lower, middle, upper, premium_lower, premium_middle, premium_upper, contracts, price_range):
    # Individual leg payoffs
    long_lower = call_payoff(lower, premium_lower, price_range, long=True, multiplier=contracts)
    short_middle = call_payoff(middle, premium_middle, price_range, long=False, multiplier=2*contracts)
    long_upper = call_payoff(upper, premium_upper, price_range, long=True, multiplier=contracts)
    
    total = long_lower + short_middle + long_upper
    return total, long_lower, short_middle, long_upper

# ---------------------------
# Interactive function
# ---------------------------
def plot_live_butterfly_legs(lower_strike, middle_strike, upper_strike, expiry, contracts, unbalanced):
    # Connect to IBKR
    ib = IB()
    if not ib.isConnected():
        ib.connect('127.0.0.1', 7496, clientId=1)
    
    right = 'C'
    # Adjust upper strike for standard butterfly
    if not unbalanced:
        upper_strike = middle_strike + (middle_strike - lower_strike)
    
    # Create option contracts
    strikes = [lower_strike, middle_strike, upper_strike]
    option_contracts = [Option('SPX', expiry, s, right, exchange='SMART') for s in strikes]
    
    # Request market data
    tickers = [ib.reqMktData(c) for c in option_contracts]
    ib.sleep(2)  # wait for quotes
    
    # Extract mid prices as premiums
    premiums = [((t.bid or 0) + (t.ask or 0)) / 2 for t in tickers]
    premium_lower, premium_middle, premium_upper = premiums
    
    # Disconnect IB
    ib.disconnect()
    
    # Price range for plotting
    S = np.arange(lower_strike-100, upper_strike+100, 1)
    
    # Calculate payoff
    total_payoff, long_lower, short_middle, long_upper = butterfly_payoff(
        lower_strike, middle_strike, upper_strike,
        premium_lower, premium_middle, premium_upper,
        contracts, S
    )
    
    # Key metrics
    max_profit = np.max(total_payoff)
    max_loss = np.min(total_payoff)
    breakeven_points = S[np.where(np.isclose(total_payoff, 0, atol=0.1))]
    
    print(f"Premiums: Lower={premium_lower:.2f}, Middle={premium_middle:.2f}, Upper={premium_upper:.2f}")
    print(f"Max Profit: {max_profit:.2f}, Max Loss: {max_loss:.2f}, Breakeven Points: {breakeven_points}\n")
    
    # Plot
    plt.figure(figsize=(12,6))
    plt.plot(S, total_payoff, label='Total Butterfly P/L', color='blue', linewidth=2)
    plt.plot(S, long_lower, label='Long Lower Strike', linestyle='--', color='green')
    plt.plot(S, short_middle, label='Short Middle Strike', linestyle='--', color='red')
    plt.plot(S, long_upper, label='Long Upper Strike', linestyle='--', color='orange')
    
    plt.axhline(0, color='black', linestyle='--')
    plt.axvline(middle_strike, color='purple', linestyle='--', label='Middle Strike')
    plt.title('Live Road Trip Butterfly Payoff with Individual Legs')
    plt.xlabel('Underlying Price at Expiration')
    plt.ylabel('Profit / Loss')
    plt.legend()
    plt.grid(True)
    plt.show()

# ---------------------------
# Interactive function with fake data
# ---------------------------
def plot_fake_butterfly(lower_strike, middle_strike, upper_strike, contracts, unbalanced):
    # Simulate premiums (fake data)
    premium_lower = 55
    premium_middle = 30
    premium_upper = 10

    # Adjust upper strike for standard butterfly
    if not unbalanced:
        upper_strike = middle_strike + (middle_strike - lower_strike)
    
    # Price range for plotting
    S = np.arange(lower_strike-100, upper_strike+100, 1)
    
    # Calculate payoff
    total_payoff, long_lower, short_middle, long_upper = butterfly_payoff(
        lower_strike, middle_strike, upper_strike,
        premium_lower, premium_middle, premium_upper,
        contracts, S
    )
    
    # Key metrics
    max_profit = np.max(total_payoff)
    max_loss = np.min(total_payoff)
    breakeven_points = S[np.where(np.isclose(total_payoff, 0, atol=0.1))]
    
    print(f"Simulated Premiums: Lower={premium_lower}, Middle={premium_middle}, Upper={premium_upper}")
    print(f"Max Profit: {max_profit}, Max Loss: {max_loss}, Breakeven Points: {breakeven_points}\n")
    
    # Plot
    plt.figure(figsize=(12,6))
    plt.plot(S, total_payoff, label='Total Butterfly P/L', color='blue', linewidth=2)
    plt.plot(S, long_lower, label='Long Lower Strike', linestyle='--', color='green')
    plt.plot(S, short_middle, label='Short Middle Strike', linestyle='--', color='red')
    plt.plot(S, long_upper, label='Long Upper Strike', linestyle='--', color='orange')
    
    plt.axhline(0, color='black', linestyle='--')
    plt.axvline(middle_strike, color='purple', linestyle='--', label='Middle Strike')
    plt.title('Fake Road Trip Butterfly Payoff with Individual Legs')
    plt.xlabel('Underlying Price at Expiration')
    plt.ylabel('Profit / Loss')
    plt.legend()
    plt.grid(True)
    plt.show()


# ---------------------------
# Interactive widgets
# ---------------------------
interact(plot_fake_butterfly,
         lower_strike=IntSlider(min=4000, max=5000, step=10, value=4500, description='Lower Strike'),
         middle_strike=IntSlider(min=4050, max=5050, step=10, value=4550, description='Middle Strike'),
         upper_strike=IntSlider(min=4100, max=5200, step=10, value=4600, description='Upper Strike'),
         expiry=Text(value='20260201', description='Expiry YYYYMMDD'),
         contracts=IntSlider(min=1, max=50, step=1, value=10, description='Contracts'),
         unbalanced=Checkbox(value=False, description='Unbalanced')
)