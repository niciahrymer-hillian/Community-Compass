import { useState } from "react";
import SideMenu from "../components/SideMenu.jsx";
import AssistantPanel from "../components/AssistantPanel.jsx";
import OverviewSection from "../components/sections/OverviewSection.jsx";
import HousingSection from "../components/sections/HousingSection.jsx";
import ResourcesSection from "../components/sections/ResourcesSection.jsx";
import YouthRiskSection from "../components/sections/YouthRiskSection.jsx";
import NewsSection from "../components/sections/NewsSection.jsx";

// CC-07: kindConnect-style dashboard — left directory + section content + the
// persistent assistant/notes/saved panel (ported from the prototype).
export default function Dashboard() {
  const [active, setActive] = useState("overview");

  return (
    <div className="dash">
      <SideMenu active={active} onSelect={setActive} />
      <div className="dash-main">
        {active === "overview" && <OverviewSection onNav={setActive} />}
        {active === "housing" && <HousingSection />}
        {active === "resources" && <ResourcesSection />}
        {active === "youth" && <YouthRiskSection />}
        {active === "news" && <NewsSection />}
      </div>
      <AssistantPanel />
    </div>
  );
}
