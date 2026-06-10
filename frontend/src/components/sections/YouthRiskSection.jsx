import { Link } from "react-router-dom";

// Youth Risk section. The explainable risk-scoring engine (Future-Path) lands in
// its own branch; for now this frames the section and routes into intake.
export default function YouthRiskSection() {
  return (
    <section>
      <h2>🧭 Youth transition &amp; risk</h2>
      <div className="card">
        <p>
          For young adults aging into independence, Community Compass will calculate
          an <strong>explainable risk score</strong> from your intake — housing,
          income, transportation, food, documents, safety, and support network —
          and surface the most urgent next steps.
        </p>
        <p className="muted">Risk scoring + youth support plan are coming in the next build.</p>
        <Link className="btn" to="/intake">Start a youth intake</Link>
      </div>
    </section>
  );
}
