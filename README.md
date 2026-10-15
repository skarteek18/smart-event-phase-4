# smart-event-phase-4


SmartEvent – Event Discovery & Ticket Booking System

Phase 4: Real-Time Experience, Personalization & AI Features

1. Project Overview

SmartEvent is a full-stack event discovery and ticket booking platform developed using FastAPI and React. Phase 4 focuses on improving user experience through real-time ticket availability, personalized recommendations, wishlist management, live event updates, advanced search, enhanced user profiles, and an AI-powered chatbot assistant.

2. Objectives

- Provide real-time ticket availability updates.
- Prevent overbooking during concurrent booking requests.
- Recommend events based on user preferences and activity.
- Allow users to save and manage favorite events.
- Display live announcements and event updates.
- Improve profile management and booking summaries.
- Enable advanced event search and filtering.
- Provide AI-powered assistance for event discovery and booking support.

3. Technology Stack

Backend

- Python 3.9+
- FastAPI
- Pydantic
- SQLAlchemy
- JWT Authentication
- WebSockets
- Uvicorn

Frontend

- React.js
- Vite
- JavaScript
- HTML5
- CSS3
- Axios
- React Router

Database

- SQLite / PostgreSQL

Additional Technologies

- AI chatbot API
- Swagger UI
- Postman
- Git and GitHub

4. Modules

Module 18: Real-Time Seat Availability & Booking Updates

- Display live available ticket counts.
- Broadcast ticket availability changes using WebSockets or polling.
- Prevent overbooking through database transactions and concurrency control.
- Disable booking when tickets are unavailable.

Module 19: Personalized Event Recommendations

- Track viewed events and booked categories.
- Recommend events based on category preferences, location, and popularity.
- Display a "Recommended for You" section.
- Display trending events on the homepage.

Module 20: Wishlist / Save Events

- Add events to a user's wishlist.
- Remove events from the wishlist.
- Retrieve saved events.
- Provide a dedicated wishlist page.
- Allow users to navigate from saved events to booking.

Module 21: Live Event Updates & Announcements

- Create an event updates system.
- Allow authorized organizers and administrators to publish announcements.
- Display announcements on event detail pages.
- Highlight important updates.
- Provide a Live Updates section.

Module 22: User Profile Enhancements

- View and update user profile information.
- Support optional profile picture uploads.
- Display booking summaries.
- Show relevant user activity.
- Validate profile ownership and submitted data.

Module 23: Advanced Search & Smart Filters

- Search events by name or keywords.
- Filter by category and location.
- Filter by minimum and maximum ticket price.
- Filter by date range.
- Sort events by popularity, price, or date.
- Provide a user-friendly multi-filter interface.

Module 24: AI Chatbot Assistant

- Provide a floating chatbot interface.
- Assist users with event discovery.
- Suggest events based on user queries.
- Help users access their bookings.
- Answer frequently asked questions.
- Provide ticket booking guidance and navigation assistance.
- Optionally maintain conversation history.

Example chatbot queries:

- "Find events near me."
- "Suggest music events this weekend."
- "Show my bookings."
- "What are the trending events?"
- "Help me with my ticket booking."

5. Database Design

New Tables

Wishlist

Column| Description
id| Primary key
user_id| Reference to the user
event_id| Reference to the event
created_at| Date and time added

EventUpdates

Column| Description
id| Primary key
event_id| Reference to the event
message| Announcement content
created_at| Date and time created

Existing Tables

- Users
- Events
- Bookings
- Tickets
- Payments
- Coupons
- Reviews
- Notifications

6. Suggested Project Structure

SmartEvent/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── config.py
│   ├── auth.py
│   ├── events.py
│   ├── bookings.py
│   ├── payments.py
│   ├── wishlist.py
│   ├── recommendations.py
│   ├── event_updates.py
│   ├── profile.py
│   ├── chatbot.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chatbot.jsx
│   │   │   └── EventCard.jsx
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Wishlist.jsx
│   │   │   ├── Profile.jsx
│   │   │   └── EventDetails.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
├── .gitignore
└── README.md

Note: This is a suggested structure. Integrate the new modules with the existing Phase 1–3 codebase and reuse existing authentication, event, booking, and payment functionality.

7. Installation and Setup

Prerequisites

- Python 3.9 or later
- Node.js and npm
- SQLite or PostgreSQL
- Git

Backend Setup

1. Clone the repository:

git clone <your-repository-url>
cd SmartEvent

2. Navigate to the backend:

cd backend

3. Create and activate a virtual environment:

python -m venv venv

Windows:

venv\Scripts\activate

Linux/macOS:

source venv/bin/activate

4. Install dependencies:

pip install -r requirements.txt

5. Configure the environment variables in ".env" using ".env.example" as a reference.

6. Start the FastAPI server:

uvicorn main:app --reload

7. Open the API documentation:

"http://127.0.0.1:8000/docs"

Frontend Setup

Open another terminal:

cd frontend
npm install
npm run dev

Open the local URL printed by Vite in the terminal.

8. Environment Configuration

Example ".env.example":

DATABASE_URL=sqlite:///./smartevent.db
SECRET_KEY=replace_with_a_secure_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
AI_API_KEY=your_ai_api_key

Use the appropriate database URL for PostgreSQL if required. Keep real API keys and secret values in ".env"; never commit them to GitHub.

9. Security Requirements

- Use JWT authentication for protected endpoints.
- Validate ownership of wishlist items and profile updates.
- Restrict event announcements to authorized organizers and administrators.
- Validate incoming requests with Pydantic.
- Prevent overbooking using database transactions and appropriate concurrency controls.
- Protect AI integrations and API credentials.
- Handle exceptions and invalid requests securely.
- Do not expose private booking or profile data to unauthorized users.

10. Testing

Test the following scenarios:

- Real-time ticket count changes after successful bookings.
- Concurrent booking requests do not exceed available capacity.
- Personalized recommendations return relevant events.
- Wishlist items can be added, retrieved, and removed.
- Only authorized users can publish event announcements.
- Users can update their own profiles.
- Search filters and sorting return the expected results.
- Chatbot queries receive appropriate responses.
- Protected endpoints reject unauthorized requests.

Recommended tools: Swagger UI, Postman, and Pytest.

11. Expected Deliverables

- Real-time ticket availability and booking updates.
- Personalized event recommendation engine.
- Wishlist management system.
- Live event announcements.
- Enhanced user profile management.
- Advanced event search and filtering.
- AI chatbot assistant.
- Integrated backend APIs and React UI.
- API testing and documentation.

12. Task Duration

Estimated Duration: 2 Days

13. Future Enhancements

- Push notifications for important event updates.
- Machine-learning-based recommendations.
- Multilingual chatbot support.
- Advanced analytics for organizers.
- Improved event discovery based on user behavior.

14. Conclusion

Phase 4 transforms SmartEvent into a more interactive, personalized, and intelligent event booking platform. By combining real-time communication, personalized recommendations, secure booking workflows, and AI-powered assistance, the platform aims to deliver a better event discovery and ticket booking experience.

Project: SmartEvent – Event Discovery & Ticket Booking System

Phase: Phase 4 – Real-Time Experience, Personalization & AI Features

Status: Implementation in Progress
