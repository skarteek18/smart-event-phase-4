

import { BrowserRouter, Routes, Route, Navigate, Link } from "react-router-dom";

import Home from "./pages/Home";
import EventDetails from "./pages/EventDetails";
import Wishlist from "./pages/Wishlist";
import Profile from "./pages/Profile";

import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        {/* Navigation Bar */}
        <header className="navbar">
          <Link to="/" className="logo">
            SmartEvent
          </Link>

          <nav className="nav-links">
            <Link to="/">Home</Link>
            <Link to="/wishlist">Wishlist</Link>
            <Link to="/profile">My Profile</Link>
          </nav>
        </header>

        {/* Main Content */}
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />

            <Route
              path="/events/:eventId"
              element={<EventDetails />}
            />

            <Route
              path="/wishlist"
              element={<Wishlist />}
            />

            <Route
              path="/profile"
              element={<Profile />}
            />

            <Route
              path="*"
              element={<Navigate to="/" replace />}
            />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="footer">
          <p>
            © 2026 SmartEvent | Discover. Book. Experience.
          </p>
        </footer>
      </div>
    </BrowserRouter>
  );
}

export default App;
