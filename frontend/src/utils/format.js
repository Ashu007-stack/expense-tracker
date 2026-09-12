export const CATEGORIES = ["Food", "Travel", "Shopping", "Entertainment", "Bills", "Health", "Education", "Others"];
export const categoryIcons = { Food: "🍴", Travel: "🚗", Shopping: "🛍", Entertainment: "🎬", Bills: "⚡", Health: "♥", Education: "📚", Others: "◈" };
export function money(value) { return new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 2 }).format(Number(value) || 0); }
export function shortDate(value) { if (!value) return "—"; return new Intl.DateTimeFormat("en-IN", { day: "2-digit", month: "short", year: "numeric" }).format(new Date(value)); }
export function monthKey(value) { const d = new Date(value); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`; }
export function monthLabel(value) { return new Intl.DateTimeFormat("en-IN", { month: "short" }).format(new Date(`${value}-01`)); }
