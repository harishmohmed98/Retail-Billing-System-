from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import mysql.connector

# Initialize FastAPI app
app = FastAPI()


# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="shoppin_item"
    )


# Item model
class Item(BaseModel):
    item_id: int
    quantity: int


# Cart to hold items
cart = {}


# Fetch item price from the database
def get_item_price(item_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT item_name, price FROM items WHERE item_id = %s", (item_id,))
    result = cursor.fetchone()
    connection.close()
    if result:
        return {"name": result[0], "price": result[1]}
    else:
        return None


# Fetch transaction details from the database
def get_transaction_details():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT Transaction_number, DateTime FROM transactions ORDER BY Transaction_number DESC LIMIT 1")
    result = cursor.fetchone()
    connection.close()
    if result:
        return {"Transaction_number": result[0], "DateTime": result[1]}
    else:
        return None


# Add item to cart
@app.post("/add_item/")
def add_item(item: Item):
    item_details = get_item_price(item.item_id)
    if not item_details:
        raise HTTPException(status_code=404, detail="Item not found")

    if item.item_id in cart:
        cart[item.item_id]["quantity"] += item.quantity
    else:
        cart[item.item_id] = {"name": item_details["name"], "price": item_details["price"], "quantity": item.quantity}

    return {"message": "Item added successfully", "cart": cart}


# Remove item from cart
@app.delete("/remove_item/{item_id}")
def remove_item(item_id: int):
    if item_id in cart:
        del cart[item_id]
        return {"message": "Item removed successfully", "cart": cart}
    else:
        raise HTTPException(status_code=404, detail="Item not in cart")


# Update item quantity
@app.put("/update_quantity/")
def update_quantity(item: Item):
    if item.item_id in cart:
        cart[item.item_id]["quantity"] = item.quantity
        return {"message": "Quantity updated successfully", "cart": cart}
    else:
        raise HTTPException(status_code=404, detail="Item not in cart")


# Calculate total bill
@app.get("/calculate_bill/")
def calculate_bill():
    total_amount = sum(item["price"] * item["quantity"] for item in cart.values())
    return {"total_bill": total_amount, "cart": cart}


# Process payment and calculate change
@app.post("/process_payment/")
def process_payment(payment: float):
    total_amount = sum(item["price"] * item["quantity"] for item in cart.values())
    if payment < total_amount:
        raise HTTPException(status_code=400, detail="Insufficient payment")
    change = payment - total_amount
    return {"message": "Payment successful", "total_bill": total_amount, "change": change}


# Print bill
@app.get("/print_bill/")
def print_bill():
    transaction_details = get_transaction_details()
    if not transaction_details:
        raise HTTPException(status_code=404, detail="No transactions found")

    bill = f"Bonfood\n\nTransaction Number: {transaction_details['Transaction_number']}\t\tDate & Time: {transaction_details['DateTime']}\n"
    bill += "\nSerial No | Item ID | Item Name | Quantity | Price\n"
    serial_no = 1
    total_amount = 0
    for item_id, details in cart.items():
        line = f"{serial_no} | {item_id} | {details['name']} | {details['quantity']} | {details['price'] * details['quantity']}\n"
        bill += line
        total_amount += details['price'] * details['quantity']
        serial_no += 1

    bill += f"\nTotal Bill: {total_amount}\n\nThank you, Visit Again!"
    return {"bill": bill}
