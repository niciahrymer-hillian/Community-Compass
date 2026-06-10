import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api";

// CC-05: AI-guided intake. Chat with the assistant; it extracts structured
// intake suggestions you can carry into the intake form to review + submit.
const GREETING = {
  role: "assistant",
  content: "Hi — tell me what's going on and I'll help you find housing and support.",
};

function clean(suggestions) {
  // Drop null/undefined so we only carry forward what was detected.
  return Object.fromEntries(Object.entries(suggestions || {}).filter(([, v]) => v != null));
}

export default function Assistant() {
  const [messages, setMessages] = useState([GREETING]);
  const [input, setInput] = useState("");
  const [suggestions, setSuggestions] = useState({});
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
    } catch (err) {
      setError(err.message);
    }
  }

  function useInIntake() {
    localStorage.setItem("cc_intake_prefill", JSON.stringify(suggestions));
    nav("/intake");
  }

  const detected = Object.keys(suggestions);

  return (
    <div className="card">
      <h1>Intake assistant</h1>
      <p className="muted">I support your intake — you'll review every answer before saving.</p>

      <div className="chat">
        {messages.map((m, i) => (
          <div key={i} className={`bubble ${m.role}`}>{m.content}</div>
        ))}
      </div>

      {error && <p className="error">{error}</p>}

      <form className="filters" onSubmit={send}>
        <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="e.g. I was evicted and need food" />
        <button className="btn" type="submit">Send</button>
      </form>

      {detected.length > 0 && (
        <div className="suggestions">
          <h3>What I picked up</h3>
          <ul>{detected.map((k) => <li key={k}>{k.replace(/_/g, " ")}: {String(suggestions[k])}</li>)}</ul>
          <button className="btn" onClick={useInIntake}>Use these in my intake →</button>
        </div>
      )}
    </div>
  );
}
