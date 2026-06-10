import { useEffect, useState } from "react";
import { api } from "../api";

const CATEGORIES = [
  "", "housing", "food", "employment", "transportation", "education", "wellness",
  "documents", "safety", "youth_services", "financial_literacy", "legal_aid", "mentorship",
];

// CC-14: search + filter community resources. Public.
export default function Resources() {
  const [items, setItems] = useState([]);
  const [q, setQ] = useState("");
  const [category, setCategory] = useState("");
  const [error, setError] = useState("");

  function load() {
    const params = new URLSearchParams();
    if (q) params.set("q", q);
    if (category) params.set("category", category);
    const qs = params.toString();
    api.resources(qs ? `?${qs}` : "").then(setItems).catch((e) => setError(e.message));
  }

  useEffect(() => { load(); /* initial load */ }, []); // eslint-disable-line

  return (
    <div>
      <h1>Community resources</h1>
      <form className="filters" onSubmit={(e) => { e.preventDefault(); load(); }}>
        <input placeholder="Search…" value={q} onChange={(e) => setQ(e.target.value)} />
        <select value={category} onChange={(e) => setCategory(e.target.value)}>
          {CATEGORIES.map((c) => (
            <option key={c} value={c}>{c ? c.replace("_", " ") : "All categories"}</option>
          ))}
        </select>
        <button className="btn" type="submit">Search</button>
      </form>
      {error && <p className="error">{error}</p>}
      <div className="cards">
        {items.map((r) => (
          <article key={r.id} className="rec">
            <h3>{r.name}</h3>
            <span className="tag">{r.category.replace("_", " ")}</span>
            {r.description && <p>{r.description}</p>}
            <p className="muted">
              {[r.city && `${r.city}, ${r.state}`, r.contact_phone, r.website].filter(Boolean).join(" · ")}
            </p>
          </article>
        ))}
      </div>
      {items.length === 0 && <p className="muted">No resources found.</p>}
    </div>
  );
}
