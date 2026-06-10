import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../../api";
import { isSaved, toggleSaved } from "../../saved";

// Housing matches from /recommendations/me (ranked, with reasons) + map link.
export default function HousingSection() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [, force] = useState(0);

  useEffect(() => {
    api.recommendations().then(setData).catch((e) => setError(e.message));
  }, []);

  if (error) {
    return (
      <div className="card narrow">
        <p>{error}</p>
        <Link className="btn" to="/intake">Start your intake</Link>
      </div>
    );
  }
  if (!data) return <p className="muted">Loading housing matches…</p>;

  return (
    <section>
      <div className="section-head">
        <h2>🏘️ Housing matches</h2>
        <Link to="/housing">Open map →</Link>
      </div>
      {data.housing.length === 0 && <p className="muted">No housing matches yet — update your intake.</p>}
      <div className="cards">
        {data.housing.map((m) => {
          const item = { id: `listing:${m.listing.id}`, type: "listing", label: m.listing.title };
          return (
            <article key={m.listing.id} className="rec">
              <h3>{m.listing.title}</h3>
              <p>${Number(m.listing.rent_amount).toLocaleString()}/mo · {m.listing.city}, {m.listing.state}</p>
              <ul className="reasons">{m.reasons.map((x, i) => <li key={i}>{x}</li>)}</ul>
              <button className="btn small outline" onClick={() => { toggleSaved(item); force((n) => n + 1); }}>
                {isSaved(item.id) ? "★ Saved" : "☆ Save"}
              </button>
            </article>
          );
        })}
      </div>
    </section>
  );
}
