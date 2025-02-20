import streamlit as st
import requests
import pandas as pd

# FastAPI server URL
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Bonfood Billing System", layout="wide")

# Apply custom styling
st.markdown(
    """
    <style>
    body {
        background-color: #f4f4f4;
        color: #333;
    }
    .main-title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #ff6600;
    }
    .sidebar .stButton>button {
        background-color: #ff6600;
        color: white;
        font-weight: bold;
    }
    .stDataFrame {
        border-radius: 10px;
        background-color: white;
        padding: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    }
    .balance-box {
        background-color: #28a745;
        color: white;
        padding: 10px;
        text-align: center;
        border-radius: 8px;
        font-size: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 class='main-title'>🛒 Bonfood Retail Sales - Billing System</h1>", unsafe_allow_html=True)

# --- SESSION STATE TO STORE CART ---
if "cart" not in st.session_state:
    st.session_state.cart = []


# --- FUNCTION TO FETCH ITEM DESCRIPTIONS ---
def fetch_item_descriptions():
    response = requests.get(f"{API_URL}/get_all_items")
    if response.status_code == 200:
        return {item["item_id"]: item["item_description"] for item in response.json()}
    return {}


item_dict = fetch_item_descriptions()


# --- FUNCTION TO ADD ITEM TO CART ---
def add_item_to_cart(item_id, quantity):
    response = requests.get(f"{API_URL}/get_item/{item_id}")
    if response.status_code == 200:
        item = response.json()
        item_name = item["name"]
        price = item["price"]
        total_price = price * quantity

        for cart_item in st.session_state.cart:
            if cart_item["item_id"] == item_id:
                cart_item["quantity"] += quantity
                cart_item["total_price"] = cart_item["quantity"] * price
                return

        st.session_state.cart.append({
            "item_id": item_id,
            "item_name": item_name,
            "quantity": quantity,
            "price": price,
            "total_price": total_price
        })
    else:
        st.error("❌ Item not found!")


# --- FUNCTION TO CALCULATE TOTAL BILL ---
def calculate_total():
    return sum(item["total_price"] for item in st.session_state.cart)


# --- FUNCTION TO PRINT BILL ---
def print_bill(amount_given):
    total_bill = calculate_total()
    balance = amount_given - total_bill

    st.subheader("🧾 **Bill Summary**")
    st.write(f"**Total Amount: ₹{total_bill:.2f}**")
    st.write(f"**Amount Given: ₹{amount_given:.2f}**")
    st.markdown(f"<div class='balance-box'>Balance to Return: ₹{balance:.2f}</div>", unsafe_allow_html=True)

    st.subheader("🛍 Purchased Items:")
    df = pd.DataFrame(st.session_state.cart)
    st.table(df[["item_name", "quantity", "price", "total_price"]])

    st.success("✅ Transaction Complete! Thank you for shopping at Bonfood!")


# --- LAYOUT ---
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🆕 Add Item")
    item_id = st.text_input("Enter Item ID")
    item_description = st.selectbox("Select Item Description",
                                    options=[item_dict[i] for i in item_dict if i == item_id],
                                    index=0 if item_id in item_dict else None)
    quantity = st.number_input("Quantity", min_value=1, value=1, step=1)
    if st.button("➕ Add to Cart", key="add_cart", help="Click to add item to cart"):
        if item_id and item_description:
            add_item_to_cart(item_id, quantity)
        else:
            st.error("Please enter an item ID.")

    st.subheader("🛒 Your Cart")
    if st.session_state.cart:
        df_cart = pd.DataFrame(st.session_state.cart)
        st.table(df_cart[["item_name", "quantity", "price", "total_price"]])
    else:
        st.info("Your cart is empty. Add some items to proceed.")

with col2:
    st.header("💵 Payment")
    total_amount = calculate_total()
    st.subheader(f"Total Bill: ₹{total_amount:.2f}")

    amount_given = st.radio("Select Payment Amount", [10, 20, 50, 100, 200, 500, 1000], horizontal=True)
    balance_to_return = amount_given - total_amount if amount_given >= total_amount else 0

    st.markdown(f"<div class='balance-box'>Balance to Return: ₹{balance_to_return:.2f}</div>", unsafe_allow_html=True)
    if st.button("Print Bill", key="print_bill", help="Click to print the final bill"):
        print_bill(amount_given)

st.sidebar.markdown("---")
st.sidebar.write("👨‍💻 Developed by: **Harish Mohammed**")