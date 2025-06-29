import numpy as np
from scipy.stats import norm

def theta(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    first_term = - (S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))

    if option_type == 'call':
        second_term = r * K * np.exp(-r * T) * norm.cdf(d2)
        return first_term - second_term
    elif option_type == 'put':
        second_term = r * K * np.exp(-r * T) * norm.cdf(-d2)
        return first_term + second_term
    else:
        raise ValueError("option_type must be 'call' or 'put'")
