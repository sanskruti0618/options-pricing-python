import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from scipy.optimize import brentq

# Default to Black-Scholes model if needed externally
from options_pricing.models.black_scholes import black_scholes


def implied_volatility(market_price, S, K, T, r, option_type, model_fn):
    """
    Compute implied volatility given market price using Brent's method.
    """
    def objective(sigma):
        return model_fn(S, K, T, r, sigma, option_type) - market_price

    try:
        return brentq(objective, 1e-6, 5.0)
    except ValueError:
        return np.nan


def generate_iv_surface(model_fn, option_type, T_fixed, r,
                        S_range=(60, 140), K_range=(60, 140), steps=30, **kwargs):
    """
    Generate a 2D implied volatility surface matrix across Spot and Strike prices.
    """
    spot_prices = np.linspace(*S_range, steps)
    strike_prices = np.linspace(*K_range, steps)
    iv_surface = np.zeros((steps, steps))

    for i, S in enumerate(spot_prices):
        for j, K in enumerate(strike_prices):
            try:
                # Theoretical option price using initial guess volatility of 0.2
                theo_price = model_fn(S, K, T_fixed, r, 0.2, option_type, **kwargs)
                iv = implied_volatility(theo_price, S, K, T_fixed, r, option_type, model_fn)
                iv_surface[i, j] = iv
            except Exception:
                iv_surface[i, j] = np.nan

    return spot_prices, strike_prices, iv_surface


def plot_iv_surface(model_fn, model_name, option_type, T, r,
                    S_range=(60, 140), K_range=(60, 140), steps=30, **kwargs):
    """
    Create a 3D surface plot of implied volatilities.
    """
    S_vals, K_vals, Z = generate_iv_surface(
        model_fn=model_fn,
        option_type=option_type,
        T_fixed=T,
        r=r,
        S_range=S_range,
        K_range=K_range,
        steps=steps,
        **kwargs
    )
    K_mesh, S_mesh = np.meshgrid(K_vals, S_vals)

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(K_mesh, S_mesh, Z, cmap='viridis', edgecolor='k')

    ax.set_xlabel("Strike Price (K)")
    ax.set_ylabel("Spot Price (S)")
    ax.set_zlabel("Implied Volatility")
    ax.set_title(f"Implied Volatility Surface - {model_name} ({option_type.capitalize()} Option)")

    return fig
