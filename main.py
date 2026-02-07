from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import date

app = FastAPI()

# Allow Bubble to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- SAMPLE DATA ----------------
# You can replace this with your own database or mock data
class Book(BaseModel):
    id: int
    title: str
    author_id: int
    royalty_per_sale: float
    total_royalties: float = 0  # Added field

class Sale(BaseModel):
    book_id: int
    sale_date: str
    quantity_sold: int
    royalty_earned: float
    book_title: str = ""  # Added field for Bubble

class Withdrawal(BaseModel):
    author_id: int
    amount: float
    status: str
    request_date: str

authors = [
    {"id": 1, "name": "Author1", "current_balance": 1000},
    {"id": 2, "name": "Author2", "current_balance": 400},
    {"id": 3, "name": "Author3", "current_balance": 600}
]

books = [
    {"id": 1, "title": "Book A1-1", "author_id": 1, "royalty_per_sale": 50},
    {"id": 2, "title": "Book A1-2", "author_id": 1, "royalty_per_sale": 75},
    {"id": 3, "title": "Book A1-3", "author_id": 1, "royalty_per_sale": 100},
    {"id": 4, "title": "Book A2-1", "author_id": 2, "royalty_per_sale": 60},
    {"id": 5, "title": "Book A2-2", "author_id": 2, "royalty_per_sale": 80},
    {"id": 6, "title": "Book A2-3", "author_id": 2, "royalty_per_sale": 120},
    {"id": 7, "title": "Book A3-1", "author_id": 3, "royalty_per_sale": 55},
    {"id": 8, "title": "Book A3-2", "author_id": 3, "royalty_per_sale": 70},
    {"id": 9, "title": "Book A3-3", "author_id": 3, "royalty_per_sale": 90}
]

sales = [
    {"book_id": 1, "sale_date": "2026-02-01", "quantity_sold": 5, "royalty_earned": 250},
    {"book_id": 2, "sale_date": "2026-02-02", "quantity_sold": 3, "royalty_earned": 225},
    {"book_id": 3, "sale_date": "2026-02-03", "quantity_sold": 2, "royalty_earned": 200},
    {"book_id": 4, "sale_date": "2026-02-01", "quantity_sold": 4, "royalty_earned": 240},
    {"book_id": 5, "sale_date": "2026-02-03", "quantity_sold": 2, "royalty_earned": 160},
    {"book_id": 6, "sale_date": "2026-02-04", "quantity_sold": 1, "royalty_earned": 120},
    {"book_id": 7, "sale_date": "2026-02-02", "quantity_sold": 3, "royalty_earned": 165},
    {"book_id": 8, "sale_date": "2026-02-03", "quantity_sold": 2, "royalty_earned": 140},
    {"book_id": 9, "sale_date": "2026-02-04", "quantity_sold": 4, "royalty_earned": 360},
    {"book_id": 1, "sale_date": "2026-02-05", "quantity_sold": 1, "royalty_earned": 50},
    {"book_id": 2, "sale_date": "2026-02-05", "quantity_sold": 1, "royalty_earned": 75},
    {"book_id": 3, "sale_date": "2026-02-05", "quantity_sold": 1, "royalty_earned": 100},
    {"book_id": 4, "sale_date": "2026-02-06", "quantity_sold": 1, "royalty_earned": 60},
    {"book_id": 5, "sale_date": "2026-02-06", "quantity_sold": 1, "royalty_earned": 80},
    {"book_id": 6, "sale_date": "2026-02-06", "quantity_sold": 1, "royalty_earned": 120}
]

withdrawals = [
    {"author_id": 1, "amount": 500, "status": "Pending", "request_date": "2026-02-05"},
    {"author_id": 2, "amount": 300, "status": "Approved", "request_date": "2026-02-04"},
    {"author_id": 3, "amount": 400, "status": "Rejected", "request_date": "2026-02-03"}
]

# ---- END SAMPLE DATA ----------------

#@app.get("/dashboard/{author_id}")
@app.get("/dashboard")
def get_dashboard(author_id: str = Query(..., description="Author ID")):
    try:
        author_id = int(author_id)  # Convert string to int
    except:
        return {"error": "author_id must be a number"}

    # Author info
    author = next((a for a in authors if a["id"] == author_id), None)
    if not author:
        return {"error": "Author not found"}

    # Books with total royalties
    author_books = [b for b in books if b["author_id"] == author_id]
    books_data = []
    for b in author_books:
        total = sum(s["royalty_earned"] for s in sales if s["book_id"] == b["id"])
        books_data.append({
            "id": b["id"],
            "title": b["title"],
            "royalty_per_sale": b["royalty_per_sale"],
            "total_royalty": total
        })

    # Recent sales
    author_sales = [s for s in sales if s["book_id"] in [b["id"] for b in author_books]]
    recent_sales = sorted(author_sales, key=lambda x: x["sale_date"], reverse=True)[:10]
    recent_sales_data = []
    for s in recent_sales:
        book_title = next((b["title"] for b in books if b["id"] == s["book_id"]), "")
        recent_sales_data.append({
            "book_title": book_title,
            "sale_date": s["sale_date"],
            "quantity_sold": s["quantity_sold"],
            "royalty_earned": s["royalty_earned"]
        })

    # Total earnings
    total_earnings = sum(s["royalty_earned"] for s in author_sales)

    # Withdrawals
    author_withdrawals = [w for w in withdrawals if w["author_id"] == author_id]

    return {
        "total_earnings": total_earnings,
        "current_balance": author["current_balance"],
        "total_books": len(author_books),
        "books": books_data,
        "recent_sales": recent_sales_data,
        "withdrawals": author_withdrawals
    }
