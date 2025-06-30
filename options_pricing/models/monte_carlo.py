import numpy as np

def monte_carlo_option_price(S, K, T, r, sigma, option_type="call", simulations=10000):
    """
    Monte Carlo simulation for European option pricing.

    Parameters:
        S: Spot price
        K: Strike price
        T: Time to expiration (in years)
        r: Risk-free interest rate
        sigma: Volatility
        option_type: 'call' or 'put'
        simulations: Number of simulated paths

    Returns:
        Estimated option price (float)
    """
    np.random.seed(42)
    Z = np.random.standard_normal(simulations)
    ST = S * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * Z)

    if option_type.lower() == "call":
        payoff = np.maximum(ST - K, 0)
    else:
        payoff = np.maximum(K - ST, 0)

    return np.exp(-r * T) * np.mean(payoff)

def generate_convergence_data(S, K, T, r, sigma, option_type, max_simulations=50000, step=1000):
    simulation_counts = []
    estimated_prices = []

    for n in range(step, max_simulations + 1, step):
        np.random.seed(42)
        Z = np.random.standard_normal(n)
        ST = S * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * Z)

        if option_type.lower() == "call":
            payoff = np.maximum(ST - K, 0)
        else:
            payoff = np.maximum(K - ST, 0)

        price = np.exp(-r * T) * np.mean(payoff)
        simulation_counts.append(n)
        estimated_prices.append(price)

    return simulation_counts, estimated_prices
