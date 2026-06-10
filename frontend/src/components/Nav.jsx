import { Link, useNavigate } from "react-router-dom";
import { getToken, getUser, logout } from "../api";

export default function Nav() {
  const nav = useNavigate();
  const user = getUser();

  function signOut() {
    logout();
    nav("/login");
  }

  return (
    <header className="nav">
      <Link to="/" className="brand">🧭 Community Compass</Link>
      <nav className="nav-links">
        <Link to="/assistant">Assistant</Link>
        <Link to="/housing">Housing Map</Link>
        <Link to="/resources">Resources</Link>
        {getToken() && <Link to="/intake">Intake</Link>}
        {getToken() && <Link to="/dashboard">Dashboard</Link>}
        {getToken() && ["caseworker", "navigator", "admin"].includes(user?.role) && (
          <Link to="/caseworker">Caseworker</Link>
        )}
        {getToken() ? (
          <button className="link-btn" onClick={signOut}>
            Sign out{user?.email ? ` (${user.email})` : ""}
          </button>
        ) : (
          <Link to="/login">Sign in</Link>
        )}
      </nav>
    </header>
  );
}
