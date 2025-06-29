def binomial_tree(S, K, T, r, sigma, N=100, option_type='call', american=False):
    import numpy as np

    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)
    discount = np.exp(-r * dt)

    # Step 1: Asset prices at maturity
    asset_prices = [S * (u ** j) * (d ** (N - j)) for j in range(N + 1)]

    # Step 2: Option values at maturity
    if option_type == 'call':
        option_values = [max(price - K, 0) for price in asset_prices]
    elif option_type == 'put':
        option_values = [max(K - price, 0) for price in asset_prices]
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    # Step 3: Backward induction
    for i in range(N - 1, -1, -1):
        for j in range(i + 1):
            asset_price = S * (u ** j) * (d ** (i - j))
            expected = discount * (p * option_values[j + 1] + (1 - p) * option_values[j])

            if american:
                # Check for early exercise
                if option_type == 'call':
                    exercise = max(asset_price - K, 0)
                else:
                    exercise = max(K - asset_price, 0)
                option_values[j] = max(expected, exercise)
            else:
                option_values[j] = expected

    return option_values[0]
