def plot_greek_vs_variable(model, greek, vary_by, S, K, T, r, sigma, option_type, N=100, simulations=10000):
    import numpy as np
    import matplotlib.pyplot as plt
    from options_pricing.greeks.black_scholes_greeks import calculate_greeks
    from options_pricing.greeks.binomial_greeks import calculate_binomial_greeks
    from options_pricing.greeks.monte_carlo_greeks import monte_carlo_delta_vega

    x_vals = []
    y_vals = []

    if vary_by == "S":
        x_range = np.linspace(50, 150, 50)
        for S_ in x_range:
            if model == "Black-Scholes":
                value = calculate_greeks(S_, K, T, r, sigma, option_type).get(greek)
            elif model == "Binomial":
                value = calculate_binomial_greeks(S_, K, T, r, sigma, N, option_type).get(greek)
            elif model == "Monte Carlo":
                value = monte_carlo_delta_vega(S_, K, T, r, sigma, option_type, simulations).get(greek)
            x_vals.append(S_)
            y_vals.append(value)

    elif vary_by == "sigma":
        x_range = np.linspace(0.01, 1.0, 50)
        for sigma_ in x_range:
            if model == "Black-Scholes":
                value = calculate_greeks(S, K, T, r, sigma_, option_type).get(greek)
            elif model == "Binomial":
                value = calculate_binomial_greeks(S, K, T, r, sigma_, N, option_type).get(greek)
            elif model == "Monte Carlo":
                value = monte_carlo_delta_vega(S, K, T, r, sigma_, option_type, simulations).get(greek)
            x_vals.append(sigma_)
            y_vals.append(value)

    elif vary_by == "T":
        x_range = np.linspace(0.01, 1.0, 50)
        for T_ in x_range:
            if model == "Black-Scholes":
                value = calculate_greeks(S, K, T_, r, sigma, option_type).get(greek)
            elif model == "Binomial":
                value = calculate_binomial_greeks(S, K, T_, r, sigma, N, option_type).get(greek)
            elif model == "Monte Carlo":
                value = monte_carlo_delta_vega(S, K, T_, r, sigma, option_type, simulations).get(greek)
            x_vals.append(T_)
            y_vals.append(value)

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, label=f"{greek} vs {vary_by}")
    ax.set_xlabel(vary_by)
    ax.set_ylabel(greek)
    ax.set_title(f"{greek} vs {vary_by} for {model}")
    ax.grid(True)
    ax.legend()
    return fig
