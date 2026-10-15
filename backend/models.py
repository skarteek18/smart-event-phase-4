

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Text,
    UniqueConstraint
)
from datetime import datetime

from Database import Base


# MODULE 1: Users
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    location = Column(String(150))
    profile_picture = Column(String(255))


# MODULE 2: Events
class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    location = Column(String(150))
    price = Column(Float, default=0)
    total_tickets = Column(Integer, default=0)
    available_tickets = Column(Integer, default=0)
    popularity = Column(Integer, default=0)
    event_date = Column(DateTime)


# MODULE 3: Bookings
class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    quantity = Column(Integer, default=1)
    status = Column(String(30), default="CONFIRMED")


# MODULE 4: Wishlist
class Wishlist(Base):
    __tablename__ = "wishlist"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "event_id",
            name="unique_user_event"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# MODULE 5: Event Updates
class EventUpdate(Base):
    __tablename__ = "event_updates"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# MODULE 6: Event Activity
class EventActivity(Base):
    __tablename__ = "event_activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    activity_type = Column(String(30), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# Create all database tables
if __name__ == "__main__":
    from Database import engine

    Base.metadata.create_all(bind=engine)
    print("SmartEvent database tables created successfully!")
