import numpy as np


def calculate_beta(user_returns, sp500_returns):
    # Convert to numpy arrays
    user_returns = np.array(user_returns)
    sp500_returns = np.array(sp500_returns)

    # Calculate covariance and variance
    covariance = np.cov(user_returns, sp500_returns, bias=True)[0][1]
    variance_sp500 = np.var(sp500_returns)

    # Calculate Beta
    beta = covariance / variance_sp500
    return beta


def calculate_alpha(user_returns, sp500_returns, beta, risk_free_rate):
    # Calculate average returns
    avg_user_return = np.mean(user_returns)
    avg_sp500_return = np.mean(sp500_returns)

    # Calculate Alpha
    alpha = (avg_user_return - risk_free_rate) - beta * (avg_sp500_return - risk_free_rate)
    return alpha
