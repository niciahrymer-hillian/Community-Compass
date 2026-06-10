import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";

// CC-07: personalized dashboard — one call to /recommendations/me.
export default function Dashboard() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api.recommendations().then(setData).catch((e) => setError(e.message));
  }, []);

  // No intake yet → the API returns 400 "Complete an intake first".
  if (error) {
    return (
      <div className="card narrow">
        <p>{error}</p>
        <Link className="btn" to="/intake">Start your intake</Link>
      </div>
    );
  }
  if (!data) return <p className="muted">Loading your matches…</p>;

  return (
    <div>
      <h1>Your matches</h1>

      <section>
        <h2>Recommended resources</h2>
        {data.resources.length === 0 && <p className="muted">No resource matches yet.</p>}
        <div className="cards">
          {data.resources.map((r) => (
            <article key={r.resource.id} className="rec">
              <h3>{r.resource.name}</h3>
              <span className="tag">{r.resource.category.replace("_", " ")}</span>
              <ul className="reasons">{r.reasons.map((x, i) => <li key={i}>{x}</li>)}</ul>
              {r.resource.contact_phone && <p className="muted">{r.resource.contact_phone}</p>}
            </article>
          ))}
        </div>
      </section>

      <section>
        <h2>Housing matches</h2>
        {data.housing.length === 0 && <p className="muted">No housing matches yet.</p>}
        <div className="cards">
          {data.housing.map((m) => (
            <article key={m.listing.id} className="rec">
              <h3>{m.listing.title}</h3>
              <p>${Number(m.listing.rent_amount).toLocaleString()}/mo · {m.listing.city}, {m.listing.state}</p>
              <ul className="reasons">{m.reasons.map((x, i) => <li key={i}>{x}</li>)}</ul>
            </article>
          ))}
        </div>
        <Link to="/housing">View all on the map →</Link>
      </section>
    </div>
  );
}
