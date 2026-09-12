from http.client import HTTPException

from fastapi import FastAPI,HTTPException
import uvicorn
import sqlite3
from pydantic import BaseModel

app=FastAPI()
class ProductCreate(BaseModel):
    category: str
    brand: str
    size_value: int
    size_unit: str
    price: int
    stock: int

@app.get("/")
def greet():
    return "Welcome TO Rattan Karyana Store!"

@app.get("/products")
def database():
    connection = sqlite3.connect("store.db")
    connection.row_factory = sqlite3.Row
    cursor=connection.cursor()
    cursor.execute("SELECT ProductID, Category, Brand, Price, Stock, SizeValue, SizeUnit, COALESCE(image_url, '') AS image_url FROM Products")
    data=cursor.fetchall()
    cursor.close()
    return [dict(row) for row in data]

@app.get("/sales")
def sales():
    connection = sqlite3.connect("store.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""
                SELECT
                    Sales.SaleID,
                    Products.Brand,
                    Products.Category,
                    Products.SizeValue,
                    Products.SizeUnit,
                    Sales.Quantity,
                    Sales.TotalAmount,
                    Sales.SaleTimestamp
                FROM Sales
                INNER JOIN Products ON Sales.ProductID = Products.ProductID
                ORDER BY Sales.SaleTimestamp DESC
                               
                """)
    data=cursor.fetchall()
    connection.close()
    return data

@app.post("/products")
def insert_items(product:ProductCreate):
    connection = sqlite3.connect("store.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Products (Category, Brand, SizeValue, SizeUnit, Price, Stock) VALUES (?, ?, ?, ?, ?, ?)",
                   (product.category,product.brand,product.size_value,product.size_unit,product.price,product.stock))
    connection.commit()
    new_id=cursor.lastrowid
    cursor.close()
    connection.close()
    return {"status": "success", "product_id":new_id}

@app.post("/products/{product_id}/sell")
def sell_item(product_id: int,quantity: int = 1):
    connection = sqlite3.connect("store.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT Stock, Brand, Price FROM Products WHERE ProductID = ?",(product_id,))
    product=cursor.fetchone()

    if quantity <= 0:
        connection.close()
        raise HTTPException(status_code=400, detail="Quantity must be greater than zero")

    if not product:
        connection.close()
        raise HTTPException(status_code=404, detail=f"Product ID {product_id} not found.")

    current_stock=product["Stock"]
    if current_stock < quantity :
        connection.close()
        raise HTTPException(status_code=400, detail=f"{product['Brand']} is out of stock")
    total_amount = product["Price"] * quantity
    cursor.execute("INSERT INTO Sales (ProductID, Quantity, TotalAmount) VALUES (?, ?, ?)",
                  (product_id, quantity, total_amount))
    cursor.execute("UPDATE Products SET Stock = Stock - ? WHERE ProductID = ?", (quantity,product_id))
    connection.commit()
    connection.close()

    return {
        "status": "success",
        "message": f"Sold {quantity} unit of {product['Brand']}",
        "remaining_stock": current_stock - quantity
    }


@app.post("/products/{product_id}/restock")
def restock_product(product_id: int, quantity: int = 1):
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Restock quantity must be positive")

    conn = sqlite3.connect("store.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE Products SET Stock = Stock + ? WHERE ProductID = ?", (quantity, product_id))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Product not found")

    conn.commit()
    conn.close()
    return {"status": "success", "added": quantity}