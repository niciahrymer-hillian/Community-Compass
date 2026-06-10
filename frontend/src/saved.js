// Saved items (resources/listings) persisted in localStorage, mirroring the
// prototype's "Saved Items" tab. Components subscribe via the custom event so
// the panel updates the moment a card is saved/unsaved.

const KEY = "cc_saved";

export const getSaved = () => JSON.parse(localStorage.getItem(KEY) || "[]");
export const isSaved = (id) => getSaved().some((x) => x.id === id);

export function toggleSaved(item) {
  const list = getSaved();
  const i = list.findIndex((x) => x.id === item.id);
  if (i >= 0) list.splice(i, 1);
  else list.push(item);
  localStorage.setItem(KEY, JSON.stringify(list));
  window.dispatchEvent(new Event("cc-saved-changed"));
  return list;
}
