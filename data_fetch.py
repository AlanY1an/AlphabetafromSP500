import json
import yfinance as yf


def load_user_data(file_path="user_data.json"):
    try:
        input_file = open(file_path, "r")
        data = json.load(input_file)
        input_file.close()
        return data["user_returns"]
    except Exception as e:
        raise ValueError(f"Failed to load user data: {e}")


def fetch_sp500_data():
    try:
        # Fetch SP500 data
        sp500 = yf.Ticker("^GSPC")
        historical_monthlydata = sp500.history(period="1mo")
        # Calculate daily percentage returns
        closing_prices = historical_monthlydata["Close"]
        daily_returns = closing_prices.pct_change()
        sp500_returns = daily_returns.tolist()
        # Past week (5 days) exclude today
        return sp500_returns[-6:-1]
    except Exception as e:
        raise ValueError(f"Failed to fetch SP500 data: {e}")


def get_daily_risk_free_rate():
    try:
        tnx = yf.Ticker("^TNX")
        tnx_data = tnx.history(period="1d") 
        annualized_rate = tnx_data["Close"].iloc[-1] / 100 
        daily_rate = annualized_rate / 252
        return daily_rate
    except Exception as e:
        raise ValueError(f"Failed to fetch daily risk-free rate: {e}")


if __name__ == "__main__":
    # Load user data
    print("Loading user data...")
    user_data = load_user_data()
    print("User Returns:", user_data)

    # Fetch SP500 data
    print("\nFetching SP500 data...")
    sp500_data = fetch_sp500_data()
    print("SP500 Returns:", sp500_data)

    # Fetch Daily Risk Free Rate
    print("\nFetch Daily Risk Free Rate data...")
    risk_data = get_daily_risk_free_rate()
    print("Risk Free Rate:", risk_data)
