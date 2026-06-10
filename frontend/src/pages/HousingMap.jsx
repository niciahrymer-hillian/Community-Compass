import { useEffect, useState } from "react";
import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";
import L from "leaflet";
// Vite bundles these PNGs as URLs; without this Leaflet's default marker 404s.
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";
import { api } from "../api";

L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

function programs(l) {
  return [
    l.section8_accepted && "Section 8",
    l.srap_accepted && "SRAP",
    l.age_55_plus && "55+",
    l.income_restricted && "Income-restricted",
  ].filter(Boolean);
}

// CC-11: housing opportunities on a Leaflet map. Public (no auth).
export default function HousingMap() {
  const [listings, setListings] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    api.housing().then(setListings).catch((e) => setError(e.message));
  }, []);

  const pins = listings.filter((l) => l.lat != null && l.lng != null);

  return (
    <div>
      <h1>Housing map</h1>
      {error && <p className="error">{error}</p>}
      <MapContainer center={[39.3, -75.55]} zoom={9} className="map">
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {pins.map((l) => (
          <Marker key={l.id} position={[Number(l.lat), Number(l.lng)]}>
            <Popup>
              <strong>{l.title}</strong>
              <br />${Number(l.rent_amount).toLocaleString()}/mo · {l.bedrooms ?? "?"} bd
              <br />{l.address}, {l.city}, {l.state}
              {programs(l).length > 0 && <><br />{programs(l).join(" · ")}</>}
              {l.contact_phone && <><br />{l.contact_phone}</>}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
      <p className="muted">{pins.length} listing(s) with map locations.</p>
    </div>
  );
}
