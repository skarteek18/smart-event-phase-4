

import { useEffect, useState } from "react";
import axios from "axios";
import "./Profile.css";

const API_URL = "http://127.0.0.1:8000";

function Profile() {
  const userId = 1; // Demo user ID

  const [profile, setProfile] = useState({
    name: "",
    email: "",
    location: "",
    profile_picture: "",
  });

  const [bookings, setBookings] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProfile();
    fetchBookings();
  }, []);

  // Fetch user profile
  const fetchProfile = async () => {
    try {
      const response = await axios.get(
        `${API_URL}/profile/${userId}`
      );

      setProfile({
        name: response.data.name || "",
        email: response.data.email || "",
        location: response.data.location || "",
        profile_picture: response.data.profile_picture || "",
      });
    } catch (error) {
      setMessage("Unable to load profile.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  // Fetch booking summary
  const fetchBookings = async () => {
    try {
      const response = await axios.get(
        `${API_URL}/profile/${userId}/bookings`
      );

      setBookings(
        Array.isArray(response.data)
          ? response.data
          : response.data.bookings || []
      );
    } catch (error) {
      console.error("Unable to load bookings:", error);
    }
  };

  // Update input fields
  const handleChange = (event) => {
    const { name, value } = event.target;

    setProfile((previousProfile) => ({
      ...previousProfile,
      [name]: value,
    }));
  };

  // Save profile changes
  const handleSubmit = async (event) => {
    event.preventDefault();
    setMessage("");

    try {
      const response = await axios.put(
        `${API_URL}/profile/${userId}`,
        {
          name: profile.name,
          location: profile.location,
          profile_picture: profile.profile_picture || null,
        }
      );

      setProfile((previousProfile) => ({
        ...previousProfile,
        ...response.data,
      }));

      setMessage("Profile updated successfully!");
    } catch (error) {
      setMessage(
        error.response?.data?.detail || "Failed to update profile."
      );
    }
  };

  if (loading) {
    return <p className="profile-loading">Loading profile...</p>;
  }

  return (
    <div className="profile-page">
      <div className="profile-card">
        <h2>My Profile</h2>
        <p className="profile-subtitle">
          Manage your SmartEvent account
        </p>

        <div className="profile-avatar">
          {profile.profile_picture ? (
            <img
              src={profile.profile_picture}
              alt="Profile"
            />
          ) : (
            <span>
              {profile.name
                ? profile.name.charAt(0).toUpperCase()
                : "U"}
            </span>
          )}
        </div>

        <form onSubmit={handleSubmit}>
          <label htmlFor="name">Full Name</label>
          <input
            id="name"
            type="text"
            name="name"
            value={profile.name}
            onChange={handleChange}
            required
          />

          <label htmlFor="email">Email Address</label>
          <input
            id="email"
            type="email"
            name="email"
            value={profile.email}
            readOnly
          />

          <label htmlFor="location">Location</label>
          <input
            id="location"
            type="text"
            name="location"
            value={profile.location}
            onChange={handleChange}
            placeholder="Enter your city"
          />

          <label htmlFor="profile_picture">
            Profile Picture URL
          </label>
          <input
            id="profile_picture"
            type="url"
            name="profile_picture"
            value={profile.profile_picture}
            onChange={handleChange}
            placeholder="https://example.com/photo.jpg"
          />

          <button type="submit" className="profile-save-btn">
            Save Changes
          </button>
        </form>

        {message && (
          <p className="profile-message">{message}</p>
        )}
      </div>

      <div className="booking-summary">
        <h2>My Bookings</h2>
        <p>Total bookings: {bookings.length}</p>

        {bookings.length === 0 ? (
          <p>You haven't booked any events yet.</p>
        ) : (
          <div className="booking-list">
            {bookings.map((booking) => (
              <div
                className="booking-item"
                key={booking.id}
              >
                <h3>
                  {booking.event?.title ||
                    booking.event_title ||
                    `Booking #${booking.id}`}
                </h3>

                <p>
                  Tickets: {booking.quantity ?? 1}
                </p>

                <p>
                  Status: {booking.status || "Confirmed"}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Profile;
