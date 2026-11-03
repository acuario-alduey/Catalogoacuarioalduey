/* ===== CONFIGURACION (edita aqui) ===================================
   WHATSAPP: tu numero con codigo de pais, sin + ni espacios. Ej: "18095551234"
   Si lo dejas vacio ("") el boton de WhatsApp no aparece.
   EXT_FOTOS: formatos de foto que buscara en la carpeta /fotos
====================================================================== */
const WHATSAPP = "";
const EXT_FOTOS = ["jpg", "jpeg", "png", "webp"];

const CATEGORIAS = [
  { id: "todos",      nombre: "🐠 Todos" },
  { id: "peces",      nombre: "🐟 Peces" },
  { id: "peceras",    nombre: "🪟 Peceras y Kits" },
  { id: "filtros",    nombre: "🌀 Filtros, Bombas y Oxígeno" },
  { id: "adornos",    nombre: "⚓ Adornos" },
  { id: "sustratos",  nombre: "🌿 Grava, Arena y Plantas" },
  { id: "alimentos",  nombre: "🍤 Alimentos" },
  { id: "cuidado",    nombre: "💧 Medicinas y Acondicionadores" },
  { id: "accesorios", nombre: "🧰 Accesorios" },
];

const $ = id => document.getElementById(id);
const fmt = n => "RD$ " + Number(n).toLocaleString("en-US", { minimumFractionDigits: n % 1 ? 2 : 0 });
const esc = s => String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const norm = s => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");

let cat = "todos";
const MODO_FOTOS = new URLSearchParams(location.search).has("fotos");   // abre index.html?fotos para ver el nombre de archivo de cada foto

// Burbujas del encabezado
(() => {
  const w = document.querySelector(".burbujas");
  for (let i = 0; i < 16; i++) {
    const b = document.createElement("i"); b.className = "burbuja";
    const s = 6 + Math.random() * 18;
    b.style.cssText = `left:${Math.random() * 100}%;width:${s}px;height:${s}px;animation-duration:${6 + Math.random() * 9}s;animation-delay:${-Math.random() * 12}s`;
    w.appendChild(b);
  }
})();

// WhatsApp opcional
if (WHATSAPP) { const a = $("wa"); a.hidden = false; a.href = "https://wa.me/" + WHATSAPP + "?text=" + encodeURIComponent("Hola Acuario Alduey, quiero consultar por un producto."); }

// Chips
function pintarChips() {
  $("chips").innerHTML = CATEGORIAS.map(c => {
    const n = c.id === "todos" ? PRODUCTOS.length : PRODUCTOS.filter(p => p.cat === c.id).length;
    return `<button class="chip${c.id === cat ? " on" : ""}" data-c="${c.id}">${c.nombre}<small>${n}</small></button>`;
  }).join("");
}
$("chips").addEventListener("click", e => {
  const b = e.target.closest(".chip"); if (!b) return;
  cat = b.dataset.c; pintarChips(); pintar();
  window.scrollTo({ top: document.querySelector(".barra").offsetTop - 2, behavior: "smooth" });
});

// Foto: busca fotos/CODIGO.jpg y, si no existe, fotos/nombre-del-producto.jpg (tambien .jpeg .png .webp)
// Si no hay ninguna, queda el pez de ejemplo.
function fotoHTML(p) {
  const bases = [...new Set([p.codigo && p.foto, p.foto_nombre].filter(Boolean))].map(x => "fotos/" + encodeURIComponent(x));
  return `<img loading="lazy" alt="${esc(p.nombre)}" data-bases="${bases.join("|")}" data-i="0" src="${bases[0]}.${EXT_FOTOS[0]}">
    <svg class="ph" viewBox="0 0 120 60" aria-hidden="true"><use href="#pez"/></svg><span class="ph-t">Foto próximamente</span>${MODO_FOTOS ? `<span class="arch">${p.codigo ? esc(p.foto) + ".jpg  ó  " : ""}${esc(p.foto_nombre)}.jpg</span>` : ""}`;
}
document.addEventListener("error", e => {
  const img = e.target; if (img.tagName !== "IMG" || !img.dataset.bases) return;
  const bases = img.dataset.bases.split("|"), i = +img.dataset.i + 1, n = bases.length * EXT_FOTOS.length;
  if (i < n) { img.dataset.i = i; img.src = `${bases[Math.floor(i / EXT_FOTOS.length)]}.${EXT_FOTOS[i % EXT_FOTOS.length]}`; }
  else img.remove();
}, true);
document.addEventListener("load", e => {            // con foto real, ocultar el pez de ejemplo
  if (e.target.tagName === "IMG" && e.target.dataset.bases) e.target.parentElement.querySelectorAll(".ph,.ph-t").forEach(x => x.remove());
}, true);

function pintar() {
  const q = norm($("buscar").value.trim());
  let lista = PRODUCTOS.filter(p => (cat === "todos" || p.cat === cat) && (!q || norm(p.nombre + " " + p.descripcion + " " + p.codigo).includes(q)));
  const o = $("orden").value;
  if (o === "asc") lista.sort((a, b) => a.precio - b.precio);
  if (o === "desc") lista.sort((a, b) => b.precio - a.precio);
  if (o === "az") lista.sort((a, b) => a.nombre.localeCompare(b.nombre, "es"));
  $("cuenta").textContent = lista.length + (lista.length === 1 ? " producto" : " productos");
  $("vacio").hidden = lista.length > 0;
  $("grid").innerHTML = lista.map(p => `
    <article class="card">
      <div class="foto">${fotoHTML(p)}</div>
      <div class="info">
        <h3 class="nombre">${esc(p.nombre)}</h3>
        <p class="desc">${esc(p.descripcion)}</p>
        ${p.codigo ? `<span class="cod">Cód. ${esc(p.codigo)}</span>` : ""}
        <div class="precio">${fmt(p.precio)}</div>
      </div>
    </article>`).join("");
}
$("grid").addEventListener("click", e => { const c = e.target.closest(".card"); if (c) c.classList.toggle("abierta"); });   // ver descripcion completa
$("buscar").addEventListener("input", pintar);
$("orden").addEventListener("change", pintar);
pintarChips(); pintar();
