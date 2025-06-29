import matplotlib.pyplot as plt
import numpy as np
from models.black_scholes import black_scholes

def plot_option_prices_vs_strike(S, T, r, sigma):
    strike_prices = np.linspace(80, 120, 50)
    call_prices = [black_scholes(S, K, T, r, sigma, 'call') for K in strike_prices]
    put_prices  = [black_scholes(S, K, T, r, sigma, 'put') for K in strike_prices]

    plt.plot(strike_prices, call_prices, label='Call Price')
    plt.plot(strike_prices, put_prices, label='Put Price')
    plt.xlabel("Strike Price (K)")
    plt.ylabel("Option Price")
    plt.title("Option Price vs Strike Price (Black-Scholes)")
    plt.legend()
    plt.grid(True)
    plt.show()