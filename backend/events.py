

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from Database import get_db
from Models import Event, EventUpdate
from Schemas import EventUpdateCreate

router = APIRouter(prefix="/events", tags=["Events"])


# 1. Get all events
@router.get("/")
def get_events(db: Session = Depends(get_db)):
    return db.query(Event).all()


# 2. Get event by ID
@router.get("/{event_id}")
def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    event = db.query(Event).filter(
        Event.id == event_id
    ).first()

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return event


# 3. Search and filter events
@router.get("/search/filter")
def search_events(
    category: Optional[str] = None,
    location: Optional[str] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Event)

    if category:
        query = query.filter(
            Event.category.ilike(f"%{category}%")
        )

    if location:
        query = query.filter(
            Event.location.ilike(f"%{location}%")
        )

    if max_price is not None:
        query = query.filter(Event.price <= max_price)

    return query.all()


# 4. Get trending events
@router.get("/trending/list")
def trending_events(
    db: Session = Depends(get_db)
):
    return db.query(Event).order_by(
        Event.popularity.desc()
    ).limit(10).all()


# 5. Check ticket availability
@router.get("/{event_id}/availability")
def ticket_availability(
    event_id: int,
    db: Session = Depends(get_db)
):
    event = db.query(Event).filter(
        Event.id == event_id
    ).first()

    if not event:
        raise HTTPException(404, "Event not found")

    return {
        "event_id": event.id,
        "event_title": event.title,
        "available_tickets": event.available_tickets,
        "total_tickets": event.total_tickets
    }


# 6. Add event announcement
@router.post("/{event_id}/updates")
def add_event_update(
    event_id: int,
    data: EventUpdateCreate,
    db: Session = Depends(get_db)
):
    event = db.query(Event).filter(
        Event.id == event_id
    ).first()

    if not event:
        raise HTTPException(404, "Event not found")

    update = EventUpdate(
        event_id=event_id,
        message=data.message
    )

    db.add(update)
    db.commit()
    db.refresh(update)

    return {
        "message": "Event announcement added",
        "update_id": update.id
    }


# 7. Get event announcements
@router.get("/{event_id}/updates")
def get_event_updates(
    event_id: int,
    db: Session = Depends(get_db)
):
    event = db.query(Event).filter(
        Event.id == event_id
    ).first()

    if not event:
        raise HTTPException(404, "Event not found")

    return db.query(EventUpdate).filter(
        EventUpdate.event_id == event_id
    ).order_by(EventUpdate.created_at.desc()).all()
