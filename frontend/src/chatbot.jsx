

import { useState } from "react";
import axios from "axios";
import "./Chatbot.css";

function Chatbot() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hello! Welcome to SmartEvent. Ask me about events, bookings, or tickets."
    }
  ]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (text = message) => {
    if (!text.trim() || loading) return;

    setMessages((previous) => [
      ...previous,
      { sender: "user", text }
    ]);

    setMessage("");
    setLoading(true);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/chatbot/chat",
        { message: text }
      );

      const data = response.data;

      let reply = data.reply || "Here is the information you requested.";

      if (data.events?.length) {
        reply += "\n" + data.events
          .map((event) => `• ${event.title}`)
          .join("\n");
      }

      if (data.bookings?.length) {
        reply += "\n" + data.bookings
          .map((booking) =>
            `• Booking #${booking.booking_id}: ${booking.status}`
          )
          .join("\n");
      }

      setMessages((previous) => [
        ...previous,
        { sender: "bot", text: reply }
      ]);
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        {
          sender: "bot",
          text: "Unable to connect to SmartEvent. Please try again."
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chatbot">
      <h2>SmartEvent Assistant</h2>

      <div className="chat-messages">
        {messages.map((item, index) => (
          <div
            key={index}
            className={`message ${item.sender}`}
          >
            {item.text}
          </div>
        ))}

        {loading && (
          <div className="message bot">Typing...</div>
        )}
      </div>

      <div className="suggestions">
        <button onClick={() => sendMessage("Show trending events")}>
          Trending Events
        </button>

        <button onClick={() => sendMessage("Show music events")}>
          Music Events
        </button>

        <button onClick={() => sendMessage("Help with tickets")}>
          Ticket Help
        </button>
      </div>

      <form
        className="chat-input"
        onSubmit={(event) => {
          event.preventDefault();
          sendMessage();
        }}
      >
        <input
          type="text"
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          placeholder="Ask about events..."
          disabled={loading}
        />

        <button type="submit" disabled={loading || !message.trim()}>
          Send
        </button>
      </form>
    </div>
  );
}

export default Chatbot;
