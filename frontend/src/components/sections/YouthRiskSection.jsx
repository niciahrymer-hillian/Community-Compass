import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../../api";

// Youth Risk section — explainable risk score from Future-Path's actual engine.
export default function YouthRiskSection() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api.risk().then(setData).catch((e) => setError(e.message));
  }, []);

  if (error) {
    return (
      <section>
        <h2>🧭 Youth transition &amp; risk</h2>
        <div className="card">
          <p>{error}</p>
          <Link className="btn" to="/intake">Start a youth intake</Link>
        </div>
      </section>
    );
  }
  if (!data) return <p className="muted">Calculating risk…</p>;

  return (
    <section>
      <h2>🧭 Youth transition &amp; risk</h2>
      <div className="card">
        <div className="section-head">
          <h3>Risk score: {data.score}/100</h3>
          <span className={`badge ${data.level.toLowerCase()}`}>{data.level}</span>
        </div>
        <p className="muted">Powered by the Future-Path explainable risk engine — here's what drove it:</p>
        {data.factors.length === 0 ? (
          <p>No elevated risk factors from your current intake. 🎉</p>
        ) : (
          <ul className="reasons">
            {data.factors.map((f) => (
              <li key={f.name}><strong>{f.name.replace(/_/g, " ")}</strong> (+{f.score}) — {f.reason}</li>
            ))}
          </ul>
        )}
        <Link className="btn outline small" to="/intake">Update intake</Link>
      </div>
    </section>
  );
}
