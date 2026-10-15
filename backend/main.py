

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="SmartEvent Phase 4")

# Temporary in-memory data for beginners
events = [
    {
        "id": 1,
        "title": "Music Festival",
        "category": "Music",
        "location": "Hyderabad",
        "price": 500,
        "available_tickets": 100,
        "popularity": 90
    },
    {
        "id": 2,
        "title": "Tech Conference",
        "category": "Technology",
        "location": "Bangalore",
        "price": 300,
        "available_tickets": 50,
        "popularity": 80
    }
]

wishlist = []
event_updates = []
user_profiles = {
    1: {"name": "Kishore", "location": "Hyderabad"}
}
bookings = []
event_views = {}


class WishlistRequest(BaseModel):
    user_id: int
    event_id: int


class UpdateRequest(BaseModel):
    message: str


class ProfileRequest(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None


class ChatRequest(BaseModel):
    message: str


# MODULE 18: Ticket Availability

@app.get("/events/{event_id}/availability")
def ticket_availability(event_id: int):
    for event in events:
        if event["id"] == event_id:
            return {
                "event_id": event_id,
                "available_tickets": event["available_tickets"]
            }

    raise HTTPException(404, "Event not found")


@app.post("/events/{event_id}/book")
def book_tickets(event_id: int, quantity: int = 1):
    for event in events:
        if event["id"] == event_id:
            if quantity < 1:
                raise HTTPException(400, "Invalid quantity")

            if event["available_tickets"] < quantity:
                raise HTTPException(400, "Tickets unavailable")

            event["available_tickets"] -= quantity

            bookings.append({
                "event_id": event_id,
                "quantity": quantity
            })

            return {
                "message": "Booking successful",
                "available_tickets": event["available_tickets"]
            }

    raise HTTPException(404, "Event not found")


# MODULE 19: Recommendations

@app.get("/users/{user_id}/recommendations")
def recommendations(user_id: int):
    return sorted(
        events,
        key=lambda event: event["popularity"],
        reverse=True
    )


@app.get("/events/trending")
def trending_events():
    return sorted(
        events,
        key=lambda event: event["popularity"],
        reverse=True
    )


# MODULE 20: Wishlist

@app.post("/wishlist")
def add_wishlist(data: WishlistRequest):
    for item in wishlist:
        if (
            item["user_id"] == data.user_id
            and item["event_id"] == data.event_id
        ):
            raise HTTPException(400, "Already in wishlist")

    wishlist.append(data.model_dump())
    return {"message": "Event added to wishlist"}


@app.get("/wishlist/{user_id}")
def get_wishlist(user_id: int):
    return [
        item for item in wishlist
        if item["user_id"] == user_id
    ]


@app.delete("/wishlist/{user_id}/{event_id}")
def remove_wishlist(user_id: int, event_id: int):
    for item in wishlist:
        if (
            item["user_id"] == user_id
            and item["event_id"] == event_id
        ):
            wishlist.remove(item)
            return {"message": "Event removed"}

    raise HTTPException(404, "Wishlist item not found")


# MODULE 21: Event Updates

@app.post("/events/{event_id}/updates")
def add_event_update(event_id: int, data: UpdateRequest):
    if not any(e["id"] == event_id for e in events):
        raise HTTPException(404, "Event not found")

    update = {
        "event_id": event_id,
        "message": data.message
    }

    event_updates.append(update)
    return {"message": "Event update added"}


@app.get("/events/{event_id}/updates")
def get_event_updates(event_id: int):
    return [
        update for update in event_updates
        if update["event_id"] == event_id
    ]


# MODULE 22: User Profile

@app.get("/profile/{user_id}")
def get_profile(user_id: int):
    if user_id not in user_profiles:
        raise HTTPException(404, "User not found")

    return {
        **user_profiles[user_id],
        "booking_count": len(bookings)
    }


@app.put("/profile/{user_id}")
def update_profile(user_id: int, data: ProfileRequest):
    if user_id not in user_profiles:
        raise HTTPException(404, "User not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        user_profiles[user_id][key] = value

    return {
        "message": "Profile updated",
        "profile": user_profiles[user_id]
    }


# MODULE 23: Advanced Search

@app.get("/events/search")
def search_events(
    category: Optional[str] = None,
    location: Optional[str] = None,
    max_price: Optional[float] = None
):
    result = events

    if category:
        result = [
            e for e in result
            if e["category"].lower() == category.lower()
        ]

    if location:
        result = [
            e for e in result
            if location.lower() in e["location"].lower()
        ]

    if max_price is not None:
        result = [
            e for e in result
            if e["price"] <= max_price
        ]

    return result


# MODULE 24: Simple Chatbot

@app.post("/chatbot")
def chatbot(data: ChatRequest):
    message = data.message.lower()

    if "trending" in message:
        return {"reply": "Check the /events/trending endpoint"}

    if "music" in message:
        music_events = [
            e for e in events
            if e["category"].lower() == "music"
        ]
        return {
            "reply": "Here are the music events",
            "events": music_events
        }

    if "booking" in message:
        return {
            "reply": "Use the /events/{event_id}/book endpoint"
        }

    return {
        "reply": "Hello! Ask me about music, trending events, or bookings."
    }


@app.get("/")
def home():
    return {"message": "Welcome to SmartEvent Phase 4 API"}
