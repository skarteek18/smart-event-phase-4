

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# MODULE 1: User Profile Schema

class ProfileBase(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    profile_picture: Optional[str] = None


class ProfileUpdate(ProfileBase):
    pass


class ProfileResponse(ProfileBase):
    id: int
    email: str

    class Config:
        from_attributes = True


# MODULE 2: Event Schema

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    location: str
    price: float = Field(ge=0)
    total_tickets: int = Field(ge=0)
    available_tickets: int = Field(ge=0)
    event_date: Optional[datetime] = None


class EventResponse(EventBase):
    id: int
    popularity: int = 0

    class Config:
        from_attributes = True


# MODULE 3: Booking Schema

class BookingCreate(BaseModel):
    event_id: int
    quantity: int = Field(ge=1, le=20)


class BookingResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    quantity: int
    status: str

    class Config:
        from_attributes = True


# MODULE 4: Wishlist Schema

class WishlistCreate(BaseModel):
    event_id: int


class WishlistResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# MODULE 5: Event Updates Schema

class EventUpdateCreate(BaseModel):
    message: str = Field(min_length=1, max_length=5000)


class EventUpdateResponse(BaseModel):
    id: int
    event_id: int
    message: str
    created_at: datetime

    class Config:
        from_attributes = True


# MODULE 6: Event Activity Schema

class EventActivityCreate(BaseModel):
    event_id: int
    activity_type: str = "VIEW"


class EventActivityResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    activity_type: str
    created_at: datetime

    class Config:
        from_attributes = True


# MODULE 7: Event Search Schema

class EventSearch(BaseModel):
    keyword: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    min_price: Optional[float] = Field(default=None, ge=0)
    max_price: Optional[float] = Field(default=None, ge=0)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    sort_by: str = "date"


# MODULE 8: Chatbot Schema

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    reply: str
    events: list[dict] = []


# MODULE 9: Ticket Availability Schema

class TicketAvailability(BaseModel):
    event_id: int
    available_tickets: int
    total_tickets: int


# MODULE 10: Recommendation Schema

class RecommendationResponse(BaseModel):
    id: int
    title: str
    category: Optional[str] = None
    location: Optional[str] = None
    price: float

    class Config:
        from_attributes = True
