# connect_ib_insync.py
import sys
import asyncio

# macOS Python 3.10+ asyncio fix (safe to include)
if sys.version_info >= (3, 10):
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

from ib_insync import IB, Stock, Option, Future, Forex, LimitOrder

def plot_live_butterfly(lower_strike, middle_strike, upper_strike, expiry, contracts, unbalanced):
    # Connect IB
    ib = IB()
    ib.connect('127.0.0.1', 7496, clientId=1)
    
    # Create option contracts
    right = 'C'
    option_contracts = [Option('SPX', expiry, s, right, exchange='SMART') for s in [lower_strike, middle_strike, upper_strike]]
    
    tickers = [ib.reqMktData(c) for c in option_contracts]
    ib.sleep(2)
    
    # Extract mid prices as premiums
    premiums = [((t.bid or 0) + (t.ask or 0)) / 2 for t in tickers]
    premium_lower, premium_middle, premium_upper = premiums
    
    # Disconnect IB
    ib.disconnect()
    
    # Adjust for standard/unbalanced butterfly
    if not unbalanced:
        upper_strike = middle_strike + (middle_strike - lower_strike)
    
    S = np.arange(lower_strike-100, upper_strike+100, 1)
    payoff = butterfly_payoff(lower_strike, middle_strike, upper_strike,
                              premium_lower, premium_middle, premium_upper,
                              contracts, S)
    
    max_profit = np.max(payoff)
    max_loss = np.min(payoff)
    breakeven_points = S[np.where(np.isclose(payoff, 0, atol=0.1))]
    
    print(f"Premiums: Lower={premium_lower}, Middle={premium_middle}, Upper={premium_upper}")
    print(f"Max Profit: {max_profit}, Max Loss: {max_loss}, Breakeven: {breakeven_points}")
    
    plt.figure(figsize=(10,6))
    plt.plot(S, payoff, label='Butterfly P/L', color='blue', linewidth=2)
    plt.axhline(0, color='black', linestyle='--')
    plt.axvline(middle_strike, color='red', linestyle='--', label='Middle Strike')
    plt.title('Live Road Trip Butterfly Payoff')
    plt.xlabel('Underlying Price at Expiration')
    plt.ylabel('Profit / Loss')
    plt.legend()
    plt.grid(True)
    plt.show()
