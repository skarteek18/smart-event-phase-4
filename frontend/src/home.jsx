

import { useEffect, useState } from "react";
import axios from "axios";
import EventCard from "../components/EventCard";
import Chatbot from "../components/Chatbot";
import "./Home.css";

const API_URL = "http://127.0.0.1:8000";

function Home() {
  const [events, setEvents] = useState([]);
  const [trending, setTrending] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [category, setCategory] = useState("");
  const [location, setLocation] = useState("");
  const [maxPrice, setMaxPrice] = useState("");

  const userId = 1; // Demo user ID

  // Load events when the page opens
  useEffect(() => {
    fetchEvents();
    fetchTrending();
    fetchRecommendations();
  }, []);

  // Get all events
  const fetchEvents = async () => {
    try {
      const response = await axios.get(`${API_URL}/events/`);
      setEvents(response.data);
    } catch (error) {
      console.error("Unable to load events", error);
    }
  };

  // Get trending events
  const fetchTrending = async () => {
    try {
      const response = await axios.get(
        `${API_URL}/recommendations/trending/events`
      );
      setTrending(response.data);
    } catch (error) {
      console.error("Unable to load trending events", error);
    }
  };

  // Get personalized recommendations
  const fetchRecommendations = async () => {
    try {
      const response = await axios.get(
        `${API_URL}/recommendations/${userId}`
      );
      setRecommendations(response.data);
    } catch (error) {
      console.error("Unable to load recommendations", error);
    }
  };

  // Search events
  const searchEvents = async () => {
    try {
      const response = await axios.get(
        `${API_URL}/events/search/filter`,
        {
          params: {
            category: category || undefined,
            location: location || undefined,
            max_price: maxPrice || undefined
          }
        }
      );

      setEvents(response.data);
    } catch (error) {
      console.error("Event search failed", error);
    }
  };

  // Book tickets
  const bookEvent = async (event) => {
    const quantity = window.prompt(
      "Enter number of tickets:",
      "1"
    );

    if (quantity === null) return;

    const count = Number(quantity);

    if (!Number.isInteger(count) || count < 1 || count > 20) {
      alert("Enter a valid quantity between 1 and 20.");
      return;
    }

    try {
      const response = await axios.post(
        `${API_URL}/events/${event.id}/book`,
        null,
        {
          params: {
            user_id: userId,
            quantity: count
          }
        }
      );

      alert(response.data.message);
      fetchEvents();
      fetchTrending();
      fetchRecommendations();
    } catch (error) {
      alert(
        error.response?.data?.detail ||
        "Unable to book tickets"
      );
    }
  };

  // Reusable event list
  const renderEvents = (eventList) => (
    <div className="event-list">
      {eventList.length > 0 ? (
        eventList.map((event) => (
          <EventCard
            key={event.id}
            event={event}
            userId={userId}
            onBook={bookEvent}
          />
        ))
      ) : (
        <p>No events available.</p>
      )}
    </div>
  );

  return (
    <div className="home-page">
      <header className="home-header">
        <h1>SmartEvent</h1>
        <p>Discover events. Book tickets. Make memories.</p>
      </header>

      <section className="search-section">
        <h2>Find Your Event</h2>

        <div className="search-filters">
          <input
            type="text"
            placeholder="Category"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          />

          <input
            type="text"
            placeholder="Location"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          />

          <input
            type="number"
            min="0"
            placeholder="Maximum price"
            value={maxPrice}
            onChange={(e) => setMaxPrice(e.target.value)}
          />

          <button onClick={searchEvents}>
            Search
          </button>

          <button
            onClick={() => {
              setCategory("");
              setLocation("");
              setMaxPrice("");
              fetchEvents();
            }}
          >
            Reset
          </button>
        </div>
      </section>

      <section>
        <h2>All Events</h2>
        {renderEvents(events)}
      </section>

      <section>
        <h2>Trending Events</h2>
        {renderEvents(trending)}
      </section>

      <section>
        <h2>Recommended for You</h2>
        {renderEvents(recommendations)}
      </section>

      <section className="chatbot-section">
        <h2>Need Help?</h2>
        <Chatbot />
      </section>

      <footer className="home-footer">
        <p>© 2026 SmartEvent. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default Home;
