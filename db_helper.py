import mysql.connector
from contextlib import contextmanager
import pandas as pd

# Database Connection
@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="shoppin_item"
    )
    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()

# Fetch item price from DB
def get_item_price(item_id):
    with get_db_cursor() as cursor:
        cursor.execute("SELECT item_name, price FROM items WHERE item_id = %s", (item_id,))
        result = cursor.fetchone()
    return result if result else None

# Cart Management
cart = []  # Stores items as dictionaries

def add_item(item_id, quantity):
    item = get_item_price(item_id)
    if item:
        cart.append({
            "item_id": item_id,
            "item_name": item["item_name"],
            "price": item["price"],
            "quantity": quantity
        })
        return f"Added {quantity} of {item['item_name']} to cart."
    return "Item not found."


def update_quantity(item_id, quantity):
    for item in cart:
        if item["item_id"] == item_id:
            item["quantity"] += quantity
            if item["quantity"] <= 0:
                cart.remove(item)
            return "Quantity updated."
    return "Item not found in cart."


def remove_item(item_id):
    global cart
    cart = [item for item in cart if item["item_id"] != item_id]
    return "Item removed."

# Calculate total bill
def calculate_total():
    return sum(item["price"] * item["quantity"] for item in cart)

# Payment processing
def calculate_change(amount_given):
    total = calculate_total()
    return amount_given - total if amount_given >= total else "Insufficient amount provided."

# Generate bill
def generate_bill(amount_given):
    total = calculate_total()
    change = calculate_change(amount_given)
    bill_data = pd.DataFrame(cart)
    bill_str = "\n" + "Bonfood".center(30) + "\n"
    bill_str += "Serial | Item ID | Item Name | Qty | Price | Total\n"
    bill_str += "-" * 50 + "\n"
    for idx, item in enumerate(cart, start=1):
        bill_str += f"{idx:<6} | {item['item_id']:<7} | {item['item_name']:<10} | {item['quantity']:<3} | {item['price']:<5} | {item['price'] * item['quantity']:.2f}\n"
    bill_str += "-" * 50 + "\n"
    bill_str += f"TOTAL BILL: {total:.2f}\n"
    bill_str += f"AMOUNT GIVEN: {amount_given:.2f}\n"
    bill_str += f"CHANGE: {change:.2f}\n"
    bill_str += "Thank You, Visit Again!".center(30) + "\n"
    return bill_str
