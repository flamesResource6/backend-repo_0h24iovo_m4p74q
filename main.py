import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List

from database import db, create_document, get_documents
from schemas import Newsletter, Product

app = FastAPI(title="Ookinhetpaars API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Ookinhetpaars backend is running"}

# Newsletter endpoint
class NewsletterIn(BaseModel):
    email: EmailStr
    source: Optional[str] = None

@app.post("/api/newsletter")
def subscribe_newsletter(payload: NewsletterIn):
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    doc = Newsletter(email=payload.email, source=payload.source)
    _id = create_document("newsletter", doc)
    return {"ok": True, "id": _id}

# Products list (for future expansion, returns demo or DB if available)
@app.get("/api/products")
def list_products() -> List[dict]:
    if db is not None:
        try:
            items = get_documents("product", {}, limit=24)
            # Convert ObjectId to str
            for it in items:
                it["_id"] = str(it.get("_id"))
            return items
        except Exception:
            pass
    # fallback demo
    return [
        {
            "id": 1,
            "name": "Knitted Merino Blanket",
            "price": 149,
            "color": "Rosewood",
            "image": "https://images.unsplash.com/photo-1540574163026-643ea20ade25?q=80&w=1600&auto=format&fit=crop",
        },
        {
            "id": 2,
            "name": "Woolen Throw",
            "price": 99,
            "color": "Moss",
            "image": "https://images.unsplash.com/photo-1524758631624-e2822e304c36?q=80&w=1600&auto=format&fit=crop",
        },
        {
            "id": 3,
            "name": "Lambswool Cushion",
            "price": 59,
            "color": "Oat",
            "image": "https://images.unsplash.com/photo-1519710164239-da123dc03ef4?q=80&w=1600&auto=format&fit=crop",
        },
        {
            "id": 4,
            "name": "Chunky Knit Throw",
            "price": 179,
            "color": "Ivory",
            "image": "https://images.unsplash.com/photo-1523419409543-41f5a3a39b2b?q=80&w=1600&auto=format&fit=crop",
        },
    ]

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
