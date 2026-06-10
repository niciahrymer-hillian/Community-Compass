import { useEffect, useState } from "react";
import { api } from "../api";

// CC-23 caseworker/navigator dashboard + CC-24 resident profile (master-detail).
export default function Caseworker() {
  const [summary, setSummary] = useState(null);
  const [list, setList] = useState([]);
  const [risk, setRisk] = useState("");
  const [selected, setSelected] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api.caseworkerSummary().then(setSummary).catch((e) => setError(e.message));
  }, []);

  useEffect(() => {
    api.residents(risk).then(setList).catch((e) => setError(e.message));
  }, [risk]);

  function open(id) {
    api.resident(id).then(setSelected).catch((e) => setError(e.message));
  }

  if (error) return <div className="card narrow"><p className="error">{error}</p><p className="muted">This area is for caseworkers/navigators.</p></div>;

  return (
    <div>
      <h1>Caseworker dashboard</h1>

      {summary && (
        <div className="tiles">
          <Metric label="Residents" value={summary.total_residents} />
          <Metric label="High risk" value={summary.high_risk} tone="high" />
          <Metric label="Housing-urgent" value={summary.housing_urgent} tone="medium" />
          <Metric label="Missing documents" value={summary.missing_documents} />
        </div>
      )}

      <div className="caseworker-grid">
        <div>
          <div className="section-head">
            <h2>Residents</h2>
            <select value={risk} onChange={(e) => setRisk(e.target.value)}>
              <option value="">All risk levels</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>
          </div>
          {list.length === 0 && <p className="muted">No residents with intakes yet.</p>}
          <ul className="resident-list">
            {list.map((r) => (
              <li key={r.user_id}>
                <button className="resident-row" onClick={() => open(r.user_id)}>
                  <span>{r.full_name || r.email}</span>
                  <span className={`badge ${r.risk_level.toLowerCase()}`}>{r.risk_level} · {r.risk_score}</span>
                </button>
                <span className="muted">{[r.housing_status, r.location].filter(Boolean).join(" · ")}</span>
              </li>
            ))}
          </ul>
        </div>

        <div>
          {!selected ? (
            <p className="muted">Select a resident to view their profile.</p>
          ) : (
            <article className="card">
              <h2>{selected.full_name || selected.email}</h2>
              <div className="section-head">
                <h3>Risk: {selected.risk.score}/100</h3>
                <span className={`badge ${selected.risk.level.toLowerCase()}`}>{selected.risk.level}</span>
              </div>
              <ul className="reasons">
                {selected.risk.factors.map((f) => (
                  <li key={f.name}><strong>{f.name.replace(/_/g, " ")}</strong> (+{f.score}) — {f.reason}</li>
                ))}
              </ul>

              <h3>Intake summary</h3>
              <p className="muted">
                {[`Housing: ${selected.intake.housing_status || "—"}`,
                  `Location: ${selected.intake.location || "—"}`,
                  `Assistance: ${selected.intake.housing_assistance_type || "—"}`].join(" · ")}
              </p>

              <h3>Recommended resources</h3>
              <ul>{selected.resources.slice(0, 5).map((r) => <li key={r.resource.id}>{r.resource.name} <span className="muted">({r.resource.category})</span></li>)}</ul>

              <h3>Housing matches</h3>
              <ul>{selected.housing.map((m) => <li key={m.listing.id}>{m.listing.title} — ${Number(m.listing.rent_amount).toLocaleString()}/mo</li>)}</ul>
            </article>
          )}
        </div>
      </div>
    </div>
  );
}

function Metric({ label, value, tone }) {
  return (
    <div className="tile">
      <strong className={tone ? `badge ${tone}` : ""} style={{ fontSize: "1.4rem" }}>{value}</strong>
      <span className="muted">{label}</span>
    </div>
  );
}
