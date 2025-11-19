from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Newsletter subscriptions -> collection name: "newsletter"
class Newsletter(BaseModel):
    email: EmailStr
    source: Optional[str] = Field(None, description="Where the user subscribed from")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# Product showcase (for future expansion) -> collection name: "product"
class Product(BaseModel):
    name: str
    price: float
    color: Optional[str] = None
    image: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
