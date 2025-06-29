import streamlit as st
from options_pricing.models.black_scholes import black_scholes
from options_pricing.models.binomial import binomial_tree

st.set_page_config(page_title="Options Pricing Calculator", layout="centered")

st.title("📈 Options Pricing Tool")

model = st.selectbox("Select Model", ["Black-Scholes", "Binomial"])
option_type = st.selectbox("Option Type", ["Call", "Put"])

S = st.slider("Spot Price (S)", 50, 200, 100)
K = st.slider("Strike Price (K)", 50, 200, 100)
T = st.slider("Time to Expiration (T in years)", 1, 365, 30) / 365
r = st.slider("Risk-Free Rate (r)", 0.0, 0.2, 0.05, step=0.005)
sigma = st.slider("Volatility (σ)", 0.01, 1.0, 0.2, step=0.01)

if model == "Binomial":
    N = st.slider("Steps (N)", 10, 500, 100)
    is_american = st.checkbox("American Option", value=False)

if st.button("Calculate Option Price"):
    if model == "Black-Scholes":
        price = black_scholes(S, K, T, r, sigma, option_type=option_type.lower())
    else:
        price = binomial_tree(S, K, T, r, sigma, N=N, option_type=option_type.lower(), american=is_american)

    st.success(f"💵 {model} {option_type} Option Price: **{price:.4f}**")
