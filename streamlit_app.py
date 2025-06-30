import streamlit as st
import matplotlib.pyplot as plt

from options_pricing.models.black_scholes import black_scholes
from options_pricing.models.binomial import binomial_tree
from options_pricing.models.monte_carlo import monte_carlo_option_price, generate_convergence_data

from options_pricing.greeks.black_scholes_greeks import calculate_greeks
from options_pricing.greeks.binomial_greeks import calculate_binomial_greeks
from options_pricing.greeks.monte_carlo_greeks import monte_carlo_delta_vega

from options_pricing.visualization.greek_plots import plot_greek_vs_variable
from options_pricing.visualization.implied_vol_surface import plot_iv_surface

st.set_page_config(page_title="Options Pricing Calculator", layout="centered")
st.title("📈 Options Pricing Tool")

# --- User Inputs ---
model = st.selectbox("Select Model", ["Black-Scholes", "Binomial", "Monte Carlo"])
option_type = st.selectbox("Option Type", ["Call", "Put"])

S = st.slider("Spot Price (S)", 50, 200, 100)
K = st.slider("Strike Price (K)", 50, 200, 100)
T = st.slider("Time to Expiration (T in years)", 1, 365, 30) / 365
r = st.slider("Risk-Free Rate (r)", 0.0, 0.2, 0.05, step=0.005)
sigma = st.slider("Volatility (σ)", 0.01, 1.0, 0.2, step=0.01)

# --- Model-specific Parameters ---
N = st.slider("Steps (N)", 10, 500, 100) if model == "Binomial" else 100
is_american = st.checkbox("American Option", value=False) if model == "Binomial" else False
simulations = st.slider("Number of Simulations", 1000, 50000, 10000, step=1000) if model == "Monte Carlo" else 10000

# --- Calculate Option Price ---
if st.button("Calculate Option Price"):
    if model == "Black-Scholes":
        price = black_scholes(S, K, T, r, sigma, option_type=option_type.lower())
        greeks = calculate_greeks(S, K, T, r, sigma, option_type=option_type.lower())

    elif model == "Binomial":
        price = binomial_tree(S, K, T, r, sigma, N=N, option_type=option_type.lower(), american=is_american)
        greeks = calculate_binomial_greeks(S, K, T, r, sigma, N=N, option_type=option_type.lower(), american=is_american)

    elif model == "Monte Carlo":
        price = monte_carlo_option_price(S, K, T, r, sigma, option_type=option_type.lower(), simulations=simulations)
        greeks = monte_carlo_delta_vega(S, K, T, r, sigma, option_type=option_type.lower(), simulations=simulations)

    st.success(f"💵 {model} {option_type} Option Price: **{price:.4f}**")

    st.subheader(f"📊 Greeks ({model})")
    for greek, value in greeks.items():
        st.write(f"**{greek}**: {value:.4f}")

    if model == "Monte Carlo":
        st.subheader("📉 Convergence Plot")
        sims, prices = generate_convergence_data(
            S, K, T, r, sigma, option_type, max_simulations=simulations, step=simulations // 50
        )
        fig, ax = plt.subplots()
        ax.plot(sims, prices, label='Estimated Price')
        ax.axhline(price, color='red', linestyle='--', label='Final Estimate')
        ax.set_xlabel("Number of Simulations")
        ax.set_ylabel("Option Price")
        ax.set_title("Monte Carlo Convergence")
        ax.legend()
        st.pyplot(fig)

# --- Greek Visualization ---
st.header("📈 Visualize Greeks")
with st.expander("Greek Sensitivity Visualization"):
    selected_greek = st.selectbox("Select Greek to Visualize", ["Delta", "Vega", "Gamma", "Theta", "Rho"])
    vary_by = st.selectbox("Vary By", ["S", "T", "sigma"])

    fig = plot_greek_vs_variable(
        model=model,
        greek=selected_greek,
        vary_by=vary_by,
        S=S, K=K, T=T, r=r, sigma=sigma,
        option_type=option_type.lower(),
        N=N,
        simulations=simulations
    )
    st.pyplot(fig)

# --- IV Surface ---
if model == "Black-Scholes":
    with st.expander("📊 Show Implied Volatility Surface"):
        show_iv = st.checkbox("Generate IV Surface")
        if show_iv:
            fig = plot_iv_surface(
                model_fn=black_scholes,
                model_name="Black-Scholes",
                option_type=option_type.lower(),
                T=T, r=r
            )
            st.pyplot(fig)
