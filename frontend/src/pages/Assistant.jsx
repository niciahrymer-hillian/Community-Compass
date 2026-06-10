import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api";

// CC-05/06: AI-guided intake + search. The assistant classifies the need,
// returns real resource links, and offers the right form to launch next.
const GREETING = {
  role: "assistant",
  content: "Hi — tell me what's going on and I'll find matches and the right next step.",
};

function clean(suggestions) {
  return Object.fromEntries(Object.entries(suggestions || {}).filter(([, v]) => v != null));
}

export default function Assistant() {
  const [messages, setMessages] = useState([GREETING]);
  const [input, setInput] = useState("");
  const [suggestions, setSuggestions] = useState({});
  const [resources, setResources] = useState([]);
  const [action, setAction] = useState(null);
  const [error, setError] = useState("");
  const nav = useNavigate();

  async function send(e) {
    e.preventDefault();
    if (!input.trim()) return;
    const convo = [...messages, { role: "user", content: input }];
    setMessages(convo);
    setInput("");
    setError("");
    try {
      const res = await api.assistantChat(convo);
      setMessages((m) => [...m, { role: "assistant", content: res.reply }]);
      setSuggestions((s) => ({ ...s, ...clean(res.suggestions) }));
      setResources(res.resources || []);
      setAction(res.action || null);
    } catch (err) {
      setError(err.message);
    }
  }

  function runAction(a) {
    if (a.kind === "housing") {
      nav("/housing");
      return;
    }
    // intake / risk both start from the intake form (risk derives from it).
    if (a.prefill && Object.keys(a.prefill).length) {
      localStorage.setItem("cc_intake_prefill", JSON.stringify(a.prefill));
    } else if (Object.keys(suggestions).length) {
      localStorage.setItem("cc_intake_prefill", JSON.stringify(suggestions));
    }
    nav("/intake");
  }

  return (
    <div className="card">
      <h1>Intake assistant</h1>
      <p className="muted">I can search resources and start the right form — you review before saving.</p>

      <div className="chat">
        {messages.map((m, i) => <div key={i} className={`bubble ${m.role}`}>{m.content}</div>)}
      </div>

      {error && <p className="error">{error}</p>}

      <form className="filters" onSubmit={send}>
        <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="e.g. I need a ride, or food this week" />
        <button className="btn" type="submit">Send</button>
      </form>

      {action && (
        <button className="btn" onClick={() => runAction(action)} style={{ marginTop: "0.5rem" }}>
          {action.label} →
        </button>
      )}

      {resources.length > 0 && (
        <div className="suggestions">
          <h3>Matches</h3>
          <div className="cards">
            {resources.map((r) => (
              <article key={r.id} className="rec">
                <h3>{r.name}</h3>
                <span className="tag">{r.category}</span>
                <p className="muted">
                  {r.website
                    ? <a href={r.website} target="_blank" rel="noreferrer">{[r.city, r.contact_phone].filter(Boolean).join(" · ") || "Visit site"}</a>
                    : [r.city, r.contact_phone].filter(Boolean).join(" · ")}
                </p>
              </article>
            ))}
          </div>
        </div>
      )}

      {Object.keys(suggestions).length > 0 && (
        <div className="suggestions">
          <h3>What I picked up</h3>
          <ul>{Object.keys(suggestions).map((k) => <li key={k}>{k.replace(/_/g, " ")}: {String(suggestions[k])}</li>)}</ul>
          <button className="btn" onClick={() => { localStorage.setItem("cc_intake_prefill", JSON.stringify(suggestions)); nav("/intake"); }}>
            Use these in my intake →
          </button>
        </div>
      )}
    </div>
  );
}
