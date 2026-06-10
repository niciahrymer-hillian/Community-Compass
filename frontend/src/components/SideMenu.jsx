// Left directory (kindConnect-style side menu): the four main sections + overview.
const SECTIONS = [
  { key: "overview", label: "Overview", icon: "▦" },
  { key: "housing", label: "Housing", icon: "🏘️" },
  { key: "resources", label: "Resources", icon: "🧰" },
  { key: "youth", label: "Youth Risk", icon: "🧭" },
  { key: "news", label: "News & Updates", icon: "📰" },
];

export default function SideMenu({ active, onSelect }) {
  return (
    <nav className="side-menu" aria-label="Sections">
      {SECTIONS.map((s) => (
        <button
          key={s.key}
          className={active === s.key ? "active" : ""}
          onClick={() => onSelect(s.key)}
        >
          <span aria-hidden="true">{s.icon}</span> {s.label}
        </button>
      ))}
    </nav>
  );
}
