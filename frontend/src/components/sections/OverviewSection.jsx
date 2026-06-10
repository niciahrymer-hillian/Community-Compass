import { getUser } from "../../api";

// Landing view of the dashboard: greeting + quick entry into the four sections.
const TILES = [
  { key: "housing", icon: "🏘️", title: "Housing", text: "See listings you may qualify for." },
  { key: "resources", icon: "🧰", title: "Resources", text: "Food, transportation, clothing & more." },
  { key: "youth", icon: "🧭", title: "Youth Risk", text: "Risk score & transition support." },
  { key: "news", icon: "📰", title: "News & Updates", text: "HUD/DSHA & local deadlines." },
];

export default function OverviewSection({ onNav }) {
  const user = getUser();
  return (
    <section>
      <div className="dash-top">
        <h2>Welcome{user?.full_name ? `, ${user.full_name}` : user?.email ? `, ${user.email}` : ""} 👋</h2>
        <p className="muted">Use the chat panel anytime — it can search resources and start the right intake for you.</p>
      </div>
      <div className="tiles">
        {TILES.map((t) => (
          <button key={t.key} className="tile" onClick={() => onNav(t.key)}>
            <span className="tile-icon" aria-hidden="true">{t.icon}</span>
            <strong>{t.title}</strong>
            <span className="muted">{t.text}</span>
          </button>
        ))}
      </div>
    </section>
  );
}
