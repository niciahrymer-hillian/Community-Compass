import { useEffect, useState } from "react";
import { api } from "../../api";

// Weekly community updates from the Java service (/api/news). The payload is
// FirstStep's NewsItem shape (headline / summary / why_it_matters / etc.).
export default function NewsSection() {
  const [items, setItems] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api.news().then(setItems).catch((e) => setError(e.message));
  }, []);

  if (error) return <p className="muted">News service offline ({error}). Start the Java service on :8080.</p>;
  if (!items) return <p className="muted">Loading updates…</p>;

  return (
    <section>
      <h2>📰 News &amp; weekly updates</h2>
      <div className="cards">
        {items.map((n) => (
          <article key={n.id} className="rec">
            <div className="section-head">
              <h3>{n.headline}</h3>
              {n.urgency && <span className={`badge ${n.urgency}`}>{n.urgency}</span>}
            </div>
            {n.type && <span className="tag">{n.type}</span>}
            <p>{n.summary}</p>
            {n.why_it_matters && <p className="why"><strong>Why it matters:</strong> {n.why_it_matters}</p>}
            <p className="muted">
              {[n.source_name, n.expires && `Expires: ${n.expires}`].filter(Boolean).join(" · ")}
            </p>
          </article>
        ))}
      </div>
    </section>
  );
}
