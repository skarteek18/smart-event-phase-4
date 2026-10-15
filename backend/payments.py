

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from Database import get_db
from Models import Booking, Payment

router = APIRouter(prefix="/payments", tags=["Payments"])


# Payment request schema
class PaymentCreate(BaseModel):
    booking_id: int = Field(gt=0)
    payment_method: str = Field(min_length=1, max_length=50)


# 1. Create payment
@router.post("/")
def create_payment(
    data: PaymentCreate,
    db: Session = Depends(get_db)
):
    booking = db.query(Booking).filter(
        Booking.id == data.booking_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    if booking.status == "CANCELLED":
        raise HTTPException(
            status_code=400,
            detail="Cannot pay for a cancelled booking"
        )

    existing_payment = db.query(Payment).filter(
        Payment.booking_id == data.booking_id,
        Payment.payment_status == "SUCCESS"
    ).first()

    if existing_payment:
        raise HTTPException(
            status_code=400,
            detail="Booking is already paid"
        )

    # Demonstration payment simulation.
    # Integrate a real payment gateway for production.
    payment = Payment(
        booking_id=data.booking_id,
        payment_method=data.payment_method,
        payment_status="SUCCESS",
        transaction_id=f"DEMO-{data.booking_id}",
        amount=0
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return {
        "message": "Payment successful (demo)",
        "payment_id": payment.id,
        "booking_id": payment.booking_id,
        "payment_status": payment.payment_status,
        "transaction_id": payment.transaction_id
    }


# 2. Get all payments
@router.get("/")
def get_payments(db: Session = Depends(get_db)):
    return db.query(Payment).all()


# 3. Get payment by ID
@router.get("/{payment_id}")
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):
    payment = db.query(Payment).filter(
        Payment.id == payment_id
    ).first()

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return payment


# 4. Check payment status
@router.get("/{payment_id}/status")
def payment_status(
    payment_id: int,
    db: Session = Depends(get_db)
):
    payment = db.query(Payment).filter(
        Payment.id == payment_id
    ).first()

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return {
        "payment_id": payment.id,
        "status": payment.payment_status,
        "transaction_id": payment.transaction_id
    }


# 5. Get payments for a booking
@router.get("/booking/{booking_id}")
def get_booking_payments(
    booking_id: int,
    db: Session = Depends(get_db)
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(404, "Booking not found")

    return db.query(Payment).filter(
        Payment.booking_id == booking_id
    ).all()
