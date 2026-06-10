import { useEffect, useState } from "react";
import { api } from "../../api";

// Weekly community updates from the Java service (/api/news), incl. "why it matters".
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
              <span className={`badge ${n.urgency}`}>{n.urgency}</span>
            </div>
            <span className="tag">{n.category}</span>
            <p>{n.summary}</p>
            {n.whyItMatters && <p className="why"><strong>Why it matters:</strong> {n.whyItMatters}</p>}
            <p className="muted">{[n.source, n.deadline && `Deadline: ${n.deadline}`].filter(Boolean).join(" · ")}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
