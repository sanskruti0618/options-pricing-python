import numpy as np
from scipy.stats import norm

def vega(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + 0.5 * sigma**2)*T) / (sigma * np.sqrt(T))
    return S * norm.pdf(d1) * np.sqrt(T)
