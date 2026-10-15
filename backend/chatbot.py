

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from Database import get_db
from Models import Event, Booking

router = APIRouter(
    prefix="/chatbot",
    tags=["AI Chatbot"]
)


# Chat request schema
class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    user_id: int | None = None


# Chatbot endpoint
@router.post("/chat")
def chat(
    data: ChatRequest,
    db: Session = Depends(get_db)
):
    message = data.message.lower().strip()

    # Trending events
    if "trending" in message or "popular" in message:
        events = db.query(Event).filter(
            Event.available_tickets > 0
        ).order_by(
            Event.popularity.desc()
        ).limit(5).all()

        return {
            "reply": "Here are the trending events!",
            "events": [
                {
                    "id": event.id,
                    "title": event.title,
                    "location": event.location,
                    "price": event.price
                }
                for event in events
            ]
        }

    # Music events
    elif "music" in message:
        events = db.query(Event).filter(
            Event.category.ilike("%music%"),
            Event.available_tickets > 0
        ).limit(5).all()

        return {
            "reply": "Here are some music events!",
            "events": [
                {
                    "id": event.id,
                    "title": event.title,
                    "location": event.location,
                    "price": event.price
                }
                for event in events
            ]
        }

    # Event discovery
    elif "event" in message:
        events = db.query(Event).filter(
            Event.available_tickets > 0
        ).limit(5).all()

        return {
            "reply": "Here are some available events!",
            "events": [
                {
                    "id": event.id,
                    "title": event.title,
                    "category": event.category,
                    "location": event.location
                }
                for event in events
            ]
        }

    # Booking history
    elif "booking" in message:
        if data.user_id is None:
            return {
                "reply": "Please log in to view your bookings."
            }

        bookings = db.query(Booking).filter(
            Booking.user_id == data.user_id
        ).all()

        return {
            "reply": "Here is your booking summary.",
            "bookings": [
                {
                    "booking_id": booking.id,
                    "event_id": booking.event_id,
                    "quantity": booking.quantity,
                    "status": booking.status
                }
                for booking in bookings
            ]
        }

    # Ticket assistance
    elif "ticket" in message or "help" in message:
        return {
            "reply": (
                "For ticket assistance, check event availability "
                "and your booking status. Contact support if "
                "your issue is unresolved."
            )
        }

    # Default response
    else:
        return {
            "reply": (
                "Hello! Welcome to SmartEvent Assistant. "
                "Ask me about trending events, music events, "
                "available events, bookings, or ticket help."
            )
        }
