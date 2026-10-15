

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Database import get_db
from Models import User, Event, EventActivity, Booking

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


# 1. Get personalized recommendations
@router.get("/{user_id}")
def get_recommendations(
    user_id: int,
    db: Session = Depends(get_db)
):
    # Check user
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Find categories of events the user has booked
    booked_events = db.query(Event).join(
        Booking,
        Booking.event_id == Event.id
    ).filter(
        Booking.user_id == user_id,
        Booking.status == "CONFIRMED"
    ).all()

    categories = list(set(
        event.category
        for event in booked_events
        if event.category
    ))

    # Find events the user has already booked
    booked_ids = [
        event.id for event in booked_events
    ]

    # Get available events
    query = db.query(Event).filter(
        Event.available_tickets > 0
    )

    if booked_ids:
        query = query.filter(
            ~Event.id.in_(booked_ids)
        )

    all_events = query.all()

    # Sort by category, location, and popularity
    def recommendation_score(event):
        score = event.popularity or 0

        if event.category in categories:
            score += 100

        if user.location and event.location == user.location:
            score += 50

        return score

    all_events.sort(
        key=recommendation_score,
        reverse=True
    )

    return [
        {
            "id": event.id,
            "title": event.title,
            "category": event.category,
            "location": event.location,
            "price": event.price,
            "available_tickets": event.available_tickets,
            "popularity": event.popularity
        }
        for event in all_events[:10]
    ]


# 2. Get trending events
@router.get("/trending/events")
def get_trending_events(
    db: Session = Depends(get_db)
):
    events = db.query(Event).filter(
        Event.available_tickets > 0
    ).order_by(
        Event.popularity.desc()
    ).limit(10).all()

    return [
        {
            "id": event.id,
            "title": event.title,
            "category": event.category,
            "location": event.location,
            "price": event.price
        }
        for event in events
    ]


# 3. Record event views
@router.post("/{user_id}/view/{event_id}")
def record_event_view(
    user_id: int,
    event_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(404, "User not found")

    event = db.query(Event).filter(
        Event.id == event_id
    ).first()

    if not event:
        raise HTTPException(404, "Event not found")

    activity = EventActivity(
        user_id=user_id,
        event_id=event_id,
        activity_type="VIEW"
    )

    db.add(activity)
    db.commit()

    return {
        "message": "Event view recorded successfully"
    }
