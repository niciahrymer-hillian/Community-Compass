import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, setToken, setUser } from "../api";

// Dev sign-in: hits POST /auth/dev-login (no Supabase needed locally).
export default function Login() {
  const [email, setEmail] = useState("demo@compass.dev");
  const [role, setRole] = useState("client");
  const [error, setError] = useState("");
  const nav = useNavigate();

  async function submit(e) {
    e.preventDefault();
    setError("");
    try {
      const r = await api.devLogin(email, role);
      setToken(r.access_token);
      setUser(r.user);
      nav("/intake");
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="card narrow">
      <h1>Sign in</h1>
      <p className="muted">Dev login — no password. (Production uses Supabase.)</p>
      <form onSubmit={submit}>
        <label>Email
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </label>
        <label>Role
          <select value={role} onChange={(e) => setRole(e.target.value)}>
            <option value="client">Resident</option>
            <option value="navigator">Navigator</option>
            <option value="admin">Admin</option>
          </select>
        </label>
        {error && <p className="error">{error}</p>}
        <button type="submit" className="btn">Continue</button>
      </form>
    </div>
  );
}
