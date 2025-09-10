import streamlit as st
import requests
import pandas as pd
from utils import display_response_as_table

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Crypto Trading App", page_icon="💹", layout="wide")

# ---------------- SESSION STATE ----------------
if "token" not in st.session_state:
    st.session_state["token"] = None
if "section" not in st.session_state:
    st.session_state["section"] = "Login / Signup"  # default section

# ---------------- SIDEBAR ----------------
st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Go to:",
    ["Login / Signup", "User", "Wallets", "Coins", "Order Status", "Logout"],
    index=["Login / Signup", "User", "Wallets", "Coins", "Order Status", "Logout"].index(st.session_state["section"])
)
st.session_state["section"] = section

# ---------------- LOGIN / SIGNUP ----------------
if section == "Login / Signup":
    tab = st.tabs(["🔑 Login", "📝 Signup"])

    with tab[0]:
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            response = requests.post(f"{API_URL}/login", data={
                "username": username, "password": password
            })
            if response.status_code == 200:
                st.session_state["token"] = response.json()["access_token"]
                st.success("✅ Logged in successfully")
            else:
                st.error("❌ Invalid credentials")

    with tab[1]:
        st.subheader("Signup")
        username = st.text_input("Username", key="signup_username")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        if st.button("Create Account"):
            response = requests.post(f"{API_URL}/signup", json={
                "username": username, "email": email, "password": password
            })
            if response.status_code == 200:
                st.success("✅ Account created successfully")
            else:
                st.error(response.text)

# ---------------- USER ----------------
elif section == "User":
    if not st.session_state["token"]:
        st.warning("⚠️ Please login first")
    else:
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        tab = st.tabs(["👤 Info", "✏️ Update", "💰 Recharge", "👛 Wallets", "📊 Trades","👤 All Users", "🗑️ Delete"])

        with tab[0]:
            res = requests.get(f"{API_URL}/user/info", headers=headers)
            display_response_as_table(res)

        with tab[1]:
            st.subheader("Update Profile")

            new_username = st.text_input("New Username")
            new_email = st.text_input("New Email")
            new_password = st.text_input("New Password", type="password")

            if st.button("Update"):
                payload = {}
                if new_username:
                    payload["username"] = new_username
                if new_email:
                    payload["email"] = new_email
                if new_password:
                    payload["password"] = new_password

                if not payload:
                    st.warning("⚠️ Please enter at least one field to update.")
                else:
                    res = requests.put(f"{API_URL}/user/update", headers=headers, json=payload)
                    st.success("Profile updated successfully")
                    display_response_as_table(res)

        with tab[2]:
            amount = st.number_input("Amount", min_value=1.0)
            if st.button("Recharge"):
                res = requests.post(f"{API_URL}/user/recharge", headers=headers, json={"amount": amount})
                st.success("Recharge Successfully Balance added to your account")
                display_response_as_table(res)

        with tab[3]:
            res = requests.get(f"{API_URL}/user/wallets", headers=headers)
            display_response_as_table(res)

        with tab[4]:
            res = requests.get(f"{API_URL}/user/trades", headers=headers)
            display_response_as_table(res, sort = False)

        with tab[5]:
            res = requests.get(f"{API_URL}/user/all_users", headers=headers)
            display_response_as_table(res)

        with tab[6]:
            if st.button("Delete Account"):
                res = requests.delete(f"{API_URL}/user/me", headers=headers)
                st.write("✅ Deleted" if res.ok else res.text)

# ---------------- WALLETS ----------------
elif section == "Wallets":
    if not st.session_state["token"]:
        st.warning("⚠️ Please login first")
    else:
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        tab = st.tabs(["➕ Create", "💵 Deposit", "💸 Withdraw"])

        with tab[0]:
            coin_id = st.number_input("Coin ID", min_value=1)
            if st.button("Create Wallet"):
                res = requests.post(f"{API_URL}/wallets/create", headers=headers, json={"coin_id": coin_id})
                st.write(res.json() if res.ok else res.text)

        with tab[1]:
            wallet_id = st.number_input("Wallet ID (Deposit)", min_value=1)
            amount = st.number_input("Amount to Deposit", min_value=1.0)
            if st.button("Deposit"):
                res = requests.post(f"{API_URL}/wallets/deposit", headers=headers, json={"wallet_id": wallet_id, "amount": amount})
                display_response_as_table(res)

        with tab[2]:
            wallet_id = st.number_input("Wallet ID (Withdraw)", min_value=1)
            amount = st.number_input("Amount to Withdraw", min_value=1.0)
            if st.button("Withdraw"):
                res = requests.post(f"{API_URL}/wallets/withdraw", headers=headers, json={"wallet_id": wallet_id, "amount": amount})
                display_response_as_table(res)

# ---------------- COINS ----------------
elif section == "Coins":
    if not st.session_state["token"]:
        st.warning("⚠️ Please login first")
    else:
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        tab = st.tabs(["📋 Available", "➕ Add", "🛒 Buy", "💰 Sell"])

        with tab[0]:
            if st.button("Show Coins"):
                res = requests.get(f"{API_URL}/coin/available_coins", headers=headers)
                display_response_as_table(res)

        with tab[1]:
            symbol = st.text_input("Symbol")
            name = st.text_input("Name")
            if st.button("Add Coin"):
                res = requests.post(f"{API_URL}/coin/add", headers=headers, json={"symbol": symbol, "name": name})
                display_response_as_table(res)

        with tab[2]:
            coin_id = st.number_input("Coin ID (Buy)", min_value=1)
            quantity = st.number_input("Quantity to Buy", min_value=1.0)
            price = st.number_input("Price per coin to buy", min_value=0.01)

            if st.button("Buy"):
                res = requests.post(f"{API_URL}/coin/buy", headers=headers, json={"coin_id": coin_id, "quantity": quantity, "price": price})
                display_response_as_table(res)

        with tab[3]:
            coin_id = st.number_input("Coin ID (Sell)", min_value=1)
            quantity = st.number_input("Quantity to Sell", min_value=1.0)
            price = st.number_input("Price per coin to sell", min_value=0.01)
            if st.button("Sell"):
                res = requests.post(f"{API_URL}/coin/sell", headers=headers, json={"coin_id": coin_id, "quantity": quantity, "price": price})
                display_response_as_table(res)

# ---------------- ORDER STATUS ----------------
elif section == "Order Status":
    st.subheader("Check the status of your order")
    task_id = st.text_input("Enter the Task ID")

    if st.button("Check"):
        res = requests.get(f"{API_URL}/coin/tasks/{task_id}")
        display_response_as_table(res)

# ---------------- LOGOUT ----------------
elif section == "Logout":
    if st.session_state["token"]:
        st.session_state["token"] = None
        st.session_state["section"] = "Login / Signup"
        st.success("✅ Logged out successfully!")
        # st.experimental_rerun()
    else:
        st.info("You are already logged out.")
