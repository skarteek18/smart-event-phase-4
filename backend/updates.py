

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from Database import get_db
from Models import Event, EventUpdate

router = APIRouter(
    prefix="/event-updates",
    tags=["Event Updates"]
)


# Request schema
class EventUpdateRequest(BaseModel):
    message: str = Field(min_length=1, max_length=5000)


# 1. Create an event announcement
@router.post("/{event_id}")
def create_event_update(
    event_id: int,
    data: EventUpdateRequest,
    db: Session = Depends(get_db)
):
    # Check whether event exists
    event = db.query(Event).filter(
        Event.id == event_id
    ).first()

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    # Create update
    update = EventUpdate(
        event_id=event_id,
        message=data.message
    )

    db.add(update)
    db.commit()
    db.refresh(update)

    return {
        "message": "Event announcement created successfully",
        "update_id": update.id,
        "event_id": update.event_id,
        "announcement": update.message,
        "created_at": update.created_at
    }


# 2. Get all announcements for an event
@router.get("/{event_id}")
def get_event_updates(
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

    updates = db.query(EventUpdate).filter(
        EventUpdate.event_id == event_id
    ).order_by(
        EventUpdate.created_at.desc()
    ).all()

    return updates


# 3. Delete an announcement
@router.delete("/update/{update_id}")
def delete_event_update(
    update_id: int,
    db: Session = Depends(get_db)
):
    update = db.query(EventUpdate).filter(
        EventUpdate.id == update_id
    ).first()

    if not update:
        raise HTTPException(
            status_code=404,
            detail="Event update not found"
        )

    db.delete(update)
    db.commit()

    return {
        "message": "Event announcement deleted successfully"
    }
