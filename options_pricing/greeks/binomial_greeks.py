from options_pricing.models.binomial import binomial_tree

def calculate_binomial_greeks(S, K, T, r, sigma, N, option_type="call", american=False, h=1e-2):
    # Delta: Change in price w.r.t. underlying asset price
    delta = (binomial_tree(S + h, K, T, r, sigma, N, option_type, american) -
             binomial_tree(S - h, K, T, r, sigma, N, option_type, american)) / (2 * h)

    # Gamma: Change in Delta w.r.t. underlying asset price
    gamma = (binomial_tree(S + h, K, T, r, sigma, N, option_type, american)
             - 2 * binomial_tree(S, K, T, r, sigma, N, option_type, american)
             + binomial_tree(S - h, K, T, r, sigma, N, option_type, american)) / (h ** 2)

    # Vega: Change in price w.r.t. volatility
    vega = (binomial_tree(S, K, T, r, sigma + h, N, option_type, american) -
            binomial_tree(S, K, T, r, sigma - h, N, option_type, american)) / (2 * h)

    # Theta: Change in price w.r.t. time to maturity
    theta = (binomial_tree(S, K, T + h, r, sigma, N, option_type, american) -
             binomial_tree(S, K, T - h, r, sigma, N, option_type, american)) / (2 * h)

    # Rho: Change in price w.r.t. interest rate
    rho = (binomial_tree(S, K, T, r + h, sigma, N, option_type, american) -
           binomial_tree(S, K, T, r - h, sigma, N, option_type, american)) / (2 * h)

    return {
        "Delta": delta,
        "Gamma": gamma,
        "Vega": vega,
        "Theta": theta,
        "Rho": rho
    }
