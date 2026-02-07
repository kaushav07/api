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

class Sale(BaseModel):
    book_id: int
    sale_date: str
    quantity_sold: int
    royalty_earned: float

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
    {"book_id": 1, "sale_date": "2026-02-05", "quantity_sold": 1, "royalty_earned": 50}
]

withdrawals = [
    {"author_id": 1, "amount": 500, "status": "Pending", "request_date": "2026-02-05"},
    {"author_id": 2, "amount": 300, "status": "Approved", "request_date": "2026-02-04"},
    {"author_id": 3, "amount": 400, "status": "Rejected", "request_date": "2026-02-03"}
]

# ---- END SAMPLE DATA ----------------

@app.get("/dashboard/{author_id}")
def get_dashboard(author_id: int):
    # AUTHOR INFO
    author = next((a for a in authors if a["id"] == author_id), None)
    if author is None:
        return {"error": "Author not found"}

    # BOOKS
    author_books = [b for b in books if b["author_id"] == author_id]

    # SALES
    author_sales = [s for s in sales if any(b["id"] == s["book_id"] for b in author_books)]

    # TOTAL EARNINGS
    total_earnings = sum(s["royalty_earned"] for s in author_sales)

    # RECENT SALES (last 10)
    recent_sales = sorted(author_sales, key=lambda x: x["sale_date"], reverse=True)[:10]

    # WITHDRAWALS
    author_withdrawals = [w for w in withdrawals if w["author_id"] == author_id]

    return {
        "total_earnings": total_earnings,
        "current_balance": author["current_balance"],
        "total_books": len(author_books),
        "books": author_books,
        "recent_sales": recent_sales,
        "withdrawals": author_withdrawals
    }
