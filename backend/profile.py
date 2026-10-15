

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from Database import get_db
from Models import User, Booking, Event

router = APIRouter(
    prefix="/profile",
    tags=["User Profile"]
)


# Request schema
class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    profile_picture: Optional[str] = None


# 1. Get user profile
@router.get("/{user_id}")
def get_profile(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "location": user.location,
        "profile_picture": user.profile_picture
    }


# 2. Update user profile
@router.put("/{user_id}")
def update_profile(
    user_id: int,
    data: ProfileUpdate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if data.name is not None:
        user.name = data.name

    if data.location is not None:
        user.location = data.location

    if data.profile_picture is not None:
        user.profile_picture = data.profile_picture

    db.commit()
    db.refresh(user)

    return {
        "message": "Profile updated successfully",
        "id": user.id,
        "name": user.name,
        "location": user.location,
        "profile_picture": user.profile_picture
    }


# 3. Get user booking summary
@router.get("/{user_id}/bookings")
def get_booking_summary(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    bookings = db.query(Booking).filter(
        Booking.user_id == user_id
    ).all()

    return {
        "user_id": user_id,
        "total_bookings": len(bookings),
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
