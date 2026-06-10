import { useEffect, useState } from "react";
import { api } from "../../api";
import { isSaved, toggleSaved } from "../../saved";

// Resource directory — food / transportation / clothing emphasized, all browsable.
const CATEGORIES = [
  "", "food", "transportation", "clothing", "housing", "employment", "wellness",
  "education", "documents", "safety", "youth_services", "financial_literacy", "legal_aid", "mentorship",
];

export default function ResourcesSection() {
  const [items, setItems] = useState([]);
  const [q, setQ] = useState("");
  const [category, setCategory] = useState("");
  const [error, setError] = useState("");
  const [, force] = useState(0);

  function load() {
    const p = new URLSearchParams();
    if (q) p.set("q", q);
    if (category) p.set("category", category);
    const qs = p.toString();
    api.resources(qs ? `?${qs}` : "").then(setItems).catch((e) => setError(e.message));
  }
  useEffect(() => { load(); }, []); // eslint-disable-line

  return (
    <section>
      <h2>🧰 Resources</h2>
      <form className="filters" onSubmit={(e) => { e.preventDefault(); load(); }}>
        <input placeholder="Search…" value={q} onChange={(e) => setQ(e.target.value)} />
        <select value={category} onChange={(e) => setCategory(e.target.value)}>
          {CATEGORIES.map((c) => <option key={c} value={c}>{c ? c.replace("_", " ") : "All categories"}</option>)}
        </select>
        <button className="btn" type="submit">Search</button>
      </form>
      {error && <p className="error">{error}</p>}
      <div className="cards">
        {items.map((r) => {
          const item = { id: `resource:${r.id}`, type: "resource", label: r.name };
          return (
            <article key={r.id} className="rec">
              <h3>{r.name}</h3>
              <span className="tag">{r.category.replace("_", " ")}</span>
              {r.description && <p>{r.description}</p>}
              <p className="muted">{[r.city && `${r.city}, ${r.state}`, r.contact_phone].filter(Boolean).join(" · ")}</p>
              <button className="btn small outline" onClick={() => { toggleSaved(item); force((n) => n + 1); }}>
                {isSaved(item.id) ? "★ Saved" : "☆ Save"}
              </button>
            </article>
          );
        })}
      </div>
      {items.length === 0 && <p className="muted">No resources found.</p>}
    </section>
  );
}
