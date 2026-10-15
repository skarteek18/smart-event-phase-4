

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Database import get_db
from Models import Booking, Event, User
from Schemas import BookingCreate

router = APIRouter(prefix="/bookings", tags=["Bookings"])


# 1. Create a booking
@router.post("/")
def create_booking(
    data: BookingCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    # Check user
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(404, "User not found")

    # Check event
    event = db.query(Event).filter(
        Event.id == data.event_id
    ).first()

    if not event:
        raise HTTPException(404, "Event not found")

    # Check ticket quantity
    if data.quantity < 1:
        raise HTTPException(400, "Invalid ticket quantity")

    if event.available_tickets < data.quantity:
        raise HTTPException(400, "Tickets not available")

    # Update available tickets
    try:
        event.available_tickets -= data.quantity

        booking = Booking(
            user_id=user_id,
            event_id=data.event_id,
            quantity=data.quantity,
            status="CONFIRMED"
        )

        db.add(booking)
        db.commit()
        db.refresh(booking)

        return {
            "message": "Booking successful",
            "booking_id": booking.id,
            "event_id": booking.event_id,
            "quantity": booking.quantity,
            "status": booking.status,
            "available_tickets": event.available_tickets
        }

    except Exception:
        db.rollback()
        raise HTTPException(500, "Booking failed")


# 2. Get all bookings
@router.get("/")
def get_bookings(db: Session = Depends(get_db)):
    return db.query(Booking).all()


# 3. Get bookings for a user
@router.get("/user/{user_id}")
def get_user_bookings(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(404, "User not found")

    return db.query(Booking).filter(
        Booking.user_id == user_id
    ).all()


# 4. Get booking by ID
@router.get("/{booking_id}")
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(404, "Booking not found")

    return booking


# 5. Cancel a booking
@router.put("/{booking_id}/cancel")
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(404, "Booking not found")

    if booking.status == "CANCELLED":
        raise HTTPException(400, "Booking already cancelled")

    event = db.query(Event).filter(
        Event.id == booking.event_id
    ).first()

    try:
        if event:
            event.available_tickets += booking.quantity

        booking.status = "CANCELLED"

        db.commit()

        return {
            "message": "Booking cancelled successfully",
            "booking_id": booking.id,
            "status": booking.status
        }

    except Exception:
        db.rollback()
        raise HTTPException(500, "Cancellation failed")
