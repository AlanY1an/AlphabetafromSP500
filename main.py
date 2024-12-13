import firebase_admin
from firebase_admin import credentials, firestore

from data_fetch import get_daily_risk_free_rate, load_user_data, fetch_sp500_data
from alpha_beta import calculate_alpha, calculate_beta


def init_firebase():
    cred = credentials.Certificate("firebase-service-account.json")
    firebase_admin.initialize_app(cred)
    return firestore.client()

def push_to_firebase(db, alpha, beta):
    """
    Push alpha and beta values to Firestore.
    """
    db.collection('performance_metrics').add({
        'alpha': alpha,
        'beta': beta,
        'timestamp': firestore.SERVER_TIMESTAMP
    })
    print(f"Successfully pushed alpha: {alpha} and beta: {beta} to Firebase!")


def main():
    # Step 1: Load User Data
    print("Loading user data...")
    user_data = load_user_data("user_data.json")
    print(f"User Returns: {user_data}")

    # Step 2: Fetch SP500 Data
    print("\nFetching SP500 data...")
    sp500_data = fetch_sp500_data()
    print(f"SP500 Returns: {sp500_data}")

    # Step 3: Calculate Beta
    print("\nCalculating Beta...")
    beta = calculate_beta(user_data, sp500_data)
    print(f"Beta: {beta}")

    # Step 4: Calculate Alpha
    print("\nCalculating Alpha...")
    risk_free_rate = get_daily_risk_free_rate()
    alpha = calculate_alpha(user_data, sp500_data, beta, risk_free_rate)
    print(f"Alpha: {alpha}")

    db = init_firebase()
    push_to_firebase(db, alpha, beta)
    print("Test upload completed.")

if __name__ == "__main__":
    main()