

import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import "./EventDetails.css";

const API_URL = "http://127.0.0.1:8000";

function EventDetails() {
  const { eventId } = useParams();
  const navigate = useNavigate();

  const userId = 1; // Demo user ID

  const [event, setEvent] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [isSaved, setIsSaved] = useState(false);

  // Fetch event details
  useEffect(() => {
    fetchEventDetails();
    checkWishlist();
  }, [eventId]);

  const fetchEventDetails = async () => {
    try {
      const response = await axios.get(
        `${API_URL}/events/${eventId}`
      );

      setEvent(response.data);
    } catch (error) {
      console.error("Error fetching event:", error);
      setMessage("Unable to load event details.");
    } finally {
      setLoading(false);
    }
  };

  // Check whether the event is saved
  const checkWishlist = async () => {
    try {
      const response = await axios.get(
        `${API_URL}/wishlist/${userId}`
      );

      const savedEvents = Array.isArray(response.data)
        ? response.data
        : response.data.wishlist || [];

      setIsSaved(
        savedEvents.some(
          (item) =>
            Number(item.event_id ?? item.id) === Number(eventId)
        )
      );
    } catch (error) {
      console.error("Error checking wishlist:", error);
    }
  };

  // Add or remove event from wishlist
  const handleWishlist = async () => {
    try {
      if (isSaved) {
        await axios.delete(
          `${API_URL}/wishlist/${userId}/${eventId}`
        );

        setIsSaved(false);
        setMessage("Event removed from wishlist.");
      } else {
        await axios.post(
          `${API_URL}/wishlist/?user_id=${userId}`,
          { event_id: Number(eventId) }
        );

        setIsSaved(true);
        setMessage("Event added to wishlist.");
      }
    } catch (error) {
      setMessage(
        error.response?.data?.detail ||
          "Unable to update wishlist."
      );
    }
  };

  // Book event tickets
  const handleBooking = async () => {
    if (!event) return;

    if (quantity < 1 || quantity > event.available_tickets) {
      setMessage("Please select a valid ticket quantity.");
      return;
    }

    try {
      const response = await axios.post(
        `${API_URL}/bookings/?user_id=${userId}`,
        {
          event_id: Number(eventId),
          quantity: Number(quantity),
        }
      );

      setMessage("Tickets booked successfully!");
      setEvent((previousEvent) => ({
        ...previousEvent,
        available_tickets:
          previousEvent.available_tickets - quantity,
      }));

      console.log("Booking created:", response.data);
    } catch (error) {
      setMessage(
        error.response?.data?.detail ||
          "Booking failed. Please try again."
      );
    }
  };

  if (loading) {
    return <p className="event-loading">Loading event details...</p>;
  }

  if (!event) {
    return (
      <div className="event-error">
        <h2>Event not found</h2>
        <button onClick={() => navigate("/")}>
          Back to Home
        </button>
      </div>
    );
  }

  return (
    <div className="event-details-page">
      <button
        className="back-button"
        onClick={() => navigate(-1)}
      >
        ← Back
      </button>

      <div className="event-details-card">
        {event.image_url && (
          <img
            className="event-details-image"
            src={event.image_url}
            alt={event.title}
          />
        )}

        <div className="event-details-content">
          <h1>{event.title}</h1>

          <p className="event-category">
            {event.category || "General"}
          </p>

          <p>
            <strong>Description:</strong>{" "}
            {event.description || "No description available."}
          </p>

          <p>
            <strong>Location:</strong>{" "}
            {event.location || "Location not specified"}
          </p>

          <p>
            <strong>Date:</strong>{" "}
            {event.event_date
              ? new Date(event.event_date).toLocaleString()
              : "Date not announced"}
          </p>

          <p>
            <strong>Ticket Price:</strong> ₹{event.price ?? 0}
          </p>

          <p>
            <strong>Available Tickets:</strong>{" "}
            {event.available_tickets ?? 0}
          </p>

          <div className="ticket-selection">
            <label htmlFor="quantity">
              Number of tickets:
            </label>

            <input
              id="quantity"
              type="number"
              min="1"
              max={event.available_tickets ?? 1}
              value={quantity}
              onChange={(e) =>
                setQuantity(Number(e.target.value))
              }
              disabled={!event.available_tickets}
            />
          </div>

          <p className="total-price">
            Total: ₹{(event.price ?? 0) * quantity}
          </p>

          <div className="event-actions">
            <button
              className="book-button"
              onClick={handleBooking}
              disabled={
                !event.available_tickets ||
                quantity < 1 ||
                quantity > event.available_tickets
              }
            >
              Book Tickets
            </button>

            <button
              className="wishlist-button"
              onClick={handleWishlist}
            >
              {isSaved
                ? "♥ Remove from Wishlist"
                : "♡ Add to Wishlist"}
            </button>
          </div>

          {message && (
            <p className="event-message">{message}</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default EventDetails;
