import numpy as np

def monte_carlo_delta_vega(S, K, T, r, sigma, option_type="call", simulations=10000):
    np.random.seed(42)
    Z = np.random.standard_normal(simulations)
    ST = S * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * Z)

    if option_type.lower() == "call":
        payoff = np.maximum(ST - K, 0)
    else:
        payoff = np.maximum(K - ST, 0)

    discounted_payoff = np.exp(-r * T) * payoff

    # Delta using path-wise derivative
    delta_path = np.where(ST > K, 1, 0) if option_type.lower() == "call" else np.where(ST < K, -1, 0)
    delta = np.mean(delta_path * ST / S) * np.exp(-r * T)

    # Vega using likelihood ratio method (LRM)
    d_log_ST = (np.log(ST / S) - (r - 0.5 * sigma ** 2) * T) / (sigma * T)
    vega = np.mean(discounted_payoff * (d_log_ST - sigma * T)) / sigma

    return {
        "Delta": delta,
        "Vega": vega / 100  # to scale like BSM vega
    }
