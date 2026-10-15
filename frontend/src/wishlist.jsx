

import { useEffect, useState } from "react";
import axios from "axios";
import EventCard from "../components/EventCard";
import "./Wishlist.css";

const API_URL = "http://127.0.0.1:8000";

function Wishlist() {
  const [wishlist, setWishlist] = useState([]);
  const [loading, setLoading] = useState(true);
  const userId = 1; // Demo user ID

  // Fetch wishlist
  const fetchWishlist = async () => {
    try {
      const response = await axios.get(
        `${API_URL}/wishlist/${userId}`
      );

      setWishlist(response.data);
    } catch (error) {
      console.error("Unable to load wishlist", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWishlist();
  }, []);

  // Remove event from wishlist
  const removeFromWishlist = async (eventId) => {
    try {
      await axios.delete(
        `${API_URL}/wishlist/${userId}/${eventId}`
      );

      setWishlist((previous) =>
        previous.filter((event) => event.event_id !== eventId)
      );
    } catch (error) {
      alert(
        error.response?.data?.detail ||
        "Unable to remove event"
      );
    }
  };

  // Book event
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
    } catch (error) {
      alert(
        error.response?.data?.detail ||
        "Booking failed"
      );
    }
  };

  if (loading) {
    return <p className="wishlist-message">Loading wishlist...</p>;
  }

  return (
    <div className="wishlist-page">
      <h1>My Wishlist ❤️</h1>
      <p>Events you have saved for later.</p>

      {wishlist.length === 0 ? (
        <div className="wishlist-empty">
          <h3>Your wishlist is empty</h3>
          <p>Explore events and save your favorites!</p>
        </div>
      ) : (
        <div className="wishlist-list">
          {wishlist.map((event) => (
            <div className="wishlist-item" key={event.wishlist_id}>
              <EventCard
                event={{
                  ...event,
                  id: event.event_id,
                  available_tickets: event.available_tickets ?? 1
                }}
                userId={userId}
                onBook={bookEvent}
              />

              <button
                className="remove-button"
                onClick={() =>
                  removeFromWishlist(event.event_id)
                }
              >
                Remove from Wishlist
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Wishlist;
