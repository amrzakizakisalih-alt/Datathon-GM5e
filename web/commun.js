// Socle de l'interface : données, état de navigation, carte et composants. Aucune dépendance, aucune donnée inventée : tout vient de web/data/
// (format décrit dans web/data/LISEZ-MOI.md). L'état de navigation vit dans l'URL (#t=territoire&p=profil…),
// si bien qu'un lien, un rechargement ou un passage d'une maquette à l'autre garde le contexte.
export const $ = (s, el = document) => el.querySelector(s);
export const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const nf = d => new Intl.NumberFormat("fr-FR", { maximumFractionDigits: d });
export const fmt = (n, d) => n == null || Number.isNaN(n) ? "—" : nf(d ?? (Math.abs(n) >= 100 ? 0 : 1)).format(n);

/* ---------- données ---------- */
const J = u => fetch("data/" + u).then(r => { if (!r.ok) throw new Error(u); return r.json(); });
const cache = new Map();
const unefois = (k, f) => { if (!cache.has(k)) cache.set(k, f()); return cache.get(k); };

export async function charger() {
  const [rg, index, geo] = await Promise.all([J("regional.json"), J("epci_index.json"), J("epci_contours.geojson")]);
  const D = { rg, index, parCode: Object.fromEntries(index.map(e => [e.code, e])), profils: Object.keys(rg.profils) };
  D.proj = projeteur(geo.features);
  D.chemins = Object.fromEntries(geo.features.map(f => [f.properties.code, tracer(f.geometry, D.proj.p)]));
  return D;
}
export const fiche = code => unefois("f" + code, () => J(`epci/${code}.json`));
export const frichesDe = code => unefois("d" + code, () => J(`friches/${code}.json`));
export const pointsFriches = D => unefois("pts", () => J("friches.geojson").then(g => g.features.map(x => {
  const [X, Y] = D.proj.p(x.geometry.coordinates); return { ...x.properties, X, Y };
})));
// Même forme pour la région et pour un territoire : les blocs s'écrivent une seule fois
export const perimetre = (D, code) => code ? fiche(code)
  : Promise.resolve({ code: "", nom: "Normandie", region: true, perimetre: "71 intercommunalités, parties normandes", ...D.rg.totaux, serie: D.rg.serie, trajectoires: D.rg.trajectoires });

export const INDICATEURS = [
  // Libellés écrits pour un élu qui découvre l'outil : pas de jargon, l'unité en toutes lettres
  { k: "perte_anciennes_pct_stock_an", n: "Prairies anciennes disparues", u: "% de leur surface par an", d: 2 },
  { k: "charrue_anciennes_ha_an", n: "Prairies anciennes mises en culture", u: "hectares par an" },
  { k: "perte_pct_stock_an", n: "Toutes prairies disparues (estimation haute)", u: "% de leur surface par an", d: 2 },
  { k: "beton_total_ha_an", n: "Terrains construits ou aménagés", u: "hectares par an" },
  { k: "enveloppe_consommee_pct", n: "Terres urbanisées de 2021 à 2024", u: "% du repère national", d: 0 },
  { k: "t1_2035_pct_stock", n: "Prairies anciennes mises en culture d'ici 2035", u: "% de leur surface de 2024" },
  { k: "friches_gain_rapide_ha", n: "Friches à restaurer en priorité", u: "hectares", d: 0 },
];
// Ni bleu (réservé à la charrue et aux cartes) ni orange (réservé au béton) : les points restent lisibles sur le fond
export const CLASSES_FRICHES = { gain_rapide: ["Gain rapide", "f3"], fort_potentiel_contraintes: ["Fort potentiel, contraintes", "f5"], potentiel_modere: ["Potentiel modéré", "f4"], projet_engage: ["Projet engagé", "fn"] };

/* ---------- état dans l'URL ---------- */
export const lire = () => Object.fromEntries(new URLSearchParams(location.hash.slice(1)));
export function ecrire(patch) {
  const s = { ...lire(), ...patch };
  for (const k of Object.keys(s)) if (s[k] == null || s[k] === "") delete s[k];
  const h = new URLSearchParams(s).toString();
  if (h !== location.hash.slice(1)) location.hash = h;
}
export function surChangement(f) { addEventListener("hashchange", f); f(); }

/* ---------- carte ---------- */
function projeteur(features) {
  let x0 = 99, x1 = -99, y0 = 99, y1 = -99;
  const voir = c => typeof c[0] === "number" ? (x0 = Math.min(x0, c[0]), x1 = Math.max(x1, c[0]), y0 = Math.min(y0, c[1]), y1 = Math.max(y1, c[1])) : c.forEach(voir);
  features.forEach(f => voir(f.geometry.coordinates));
  const k = Math.cos((y0 + y1) / 2 * Math.PI / 180), S = 1000 / ((x1 - x0) * k);
  return { p: c => [(c[0] - x0) * k * S, (y1 - c[1]) * S], H: (y1 - y0) * S };
}
function tracer(geom, p) {
  const polys = geom.type === "Polygon" ? [geom.coordinates] : geom.coordinates;
  return polys.map(poly => poly.map(an => "M" + an.map(c => p(c).map(v => v.toFixed(1)).join(" ")).join("L") + "Z").join("")).join("");
}
const seuils = vals => { const s = vals.filter(v => v != null).sort((a, b) => a - b); return [.2, .4, .6, .8].map(q => s[Math.floor(q * (s.length - 1))]); };

// Carte choroplèthe en 5 classes d'effectifs égaux. `actif` grise les territoires hors filtre ; `points` ajoute les friches.
export function carte(svg, D, { ind, sel = "", actif = () => true, points = null, classes = null, couleurPoints = null, plat = false, choisir }) {
  const q = seuils(D.index.filter(actif).map(e => e[ind.k]));
  svg.setAttribute("viewBox", `-6 -6 1012 ${D.proj.H + 12}`);
  svg.setAttribute("class", "carte-svg");
  svg.setAttribute("role", "img");
  svg.setAttribute("aria-label", `Carte des intercommunalités normandes : ${ind.n}. Le tableau donne les mêmes valeurs.`);
  svg.innerHTML = D.index.map(e => {
    // plat : fond de carte neutre, sans valeur (les points portent alors l'information)
    const v = e[ind.k], cl = plat ? "plat" : !actif(e) || v == null ? "hors" : "c" + q.filter(x => v > x).length;
    return `<path class="zone ${cl}" data-code="${e.code}" d="${D.chemins[e.code]}" data-tip="${esc(e.nom)}|${plat ? "cliquer pour voir ses friches" : actif(e) ? `${fmt(v, ind.d)} ${ind.u}` : "hors filtre"}${e.exclu_comparaisons ? " · partie normande" : ""}"/>`;
  }).join("") + (sel && D.chemins[sel] ? `<path class="contour-sel" d="${D.chemins[sel]}"/>` : "")
    + (points ? `<g class="pts">${points.filter(x => !classes || classes.has(x.classe)).map(x => `<circle class="${couleurPoints || CLASSES_FRICHES[x.classe][1]}" cx="${x.X.toFixed(1)}" cy="${x.Y.toFixed(1)}" r="${x.epci === sel ? 5 : 3}" data-code="${x.epci}" data-tip="${esc(CLASSES_FRICHES[x.classe][0])}|${fmt(x.ha)} ha · score ${x.bio}/100"/>`).join("")}</g>` : "");
  svg.onclick = ev => { const c = ev.target.dataset?.code; if (c) choisir(c === sel ? "" : c); };
  return `<b>${esc(ind.n)}</b> (${esc(ind.u)}) ` + ["c0", "c1", "c2", "c3", "c4"].map((c, i) => `<span><i class="${c}" style="background:var(--seq${i + 1})"></i>${i === 0 ? "≤ " + fmt(q[0], ind.d) : i === 4 ? "> " + fmt(q[3], ind.d) : fmt(q[i - 1], ind.d) + " à " + fmt(q[i], ind.d)}</span>`).join("") + `<span><i style="background:var(--hors)"></i>hors filtre</span>`;
}

/* ---------- infobulle unique, pilotée par l'attribut data-tip="titre|détail" ---------- */
export function infobulles() {
  const t = document.createElement("div"); t.className = "tip"; t.hidden = true; document.body.append(t);
  addEventListener("pointermove", e => {
    const el = e.target.closest?.("[data-tip]");
    if (!el || e.pointerType === "touch") { t.hidden = true; return; }
    const [a, b] = el.dataset.tip.split("|");
    t.innerHTML = `<b>${esc(a)}</b>${b ? `<span>${esc(b)}</span>` : ""}`; t.hidden = false;
    t.style.left = Math.max(4, Math.min(innerWidth - t.offsetWidth - 8, e.clientX + 14)) + "px";
    t.style.top = Math.min(innerHeight - t.offsetHeight - 8, e.clientY + 14) + "px";
  });
}

/* ---------- composants ---------- */
export function entete(lettre, titre) {
  const liens = [["a-atlas.html", "A · Atlas"], ["b-tableau-de-bord.html", "B · Tableau de bord"], ["c-territoire.html", "C · Dossier de territoire"]];
  $("#barre").innerHTML = `<a class="marque" href="index.html">Béton &amp; Charrue<small>maquette ${lettre} · ${titre}</small></a>
    <nav aria-label="Maquettes">${liens.map(([h, n]) => `<a data-h="${h}" href="${h}"${n[0] === lettre ? ' aria-current="page"' : ""}>${n}</a>`).join("")}</nav>`;
  const maj = () => document.querySelectorAll("#barre nav a").forEach(a => { a.href = a.dataset.h + location.hash; });
  addEventListener("hashchange", maj); maj();
}
export const optionsTerritoires = (D, sel) => `<option value="">Toute la Normandie</option>` + [...D.index].sort((a, b) => a.nom.localeCompare(b.nom, "fr")).map(e => `<option value="${e.code}"${e.code === sel ? " selected" : ""}>${esc(e.nom)}</option>`).join("");
export const optionsProfils = (D, sel) => `<option value="">Tous les profils</option>` + D.profils.map(p => `<option${p === sel ? " selected" : ""}>${esc(p)}</option>`).join("");
export const tuile = (lab, val, sous = "") => `<div class="tuile"><span class="t-lab">${lab}</span><b>${val}</b><span class="t-sous">${sous}</span></div>`;
export function barres(lignes) {
  const m = Math.max(...lignes.map(x => x.v || 0), 1e-9);
  return `<div class="barres">${lignes.map(x => `<div class="ligne-b" data-tip="${esc(x.n)}|${esc(x.t)}"><span>${esc(x.n)}</span><i><u class="${x.c}" style="width:${100 * (x.v || 0) / m}%"></u></i><em>${esc(x.t)}</em></div>`).join("")}</div>`;
}
function pasNet(v) { const e = 10 ** Math.floor(Math.log10(v || 1)), f = (v || 1) / e; return (f <= 1 ? 1 : f <= 2 ? 2 : f <= 5 ? 5 : 10) * e; }

// Hectares retournés par an : prairies anciennes, et au-dessus celles devenues permanentes après 2015
export function serieSvg(serie, { l = 520, h = 170 } = {}) {
  const m = { g: 44, d: 6, h: 8, b: 20 }, pas = pasNet(Math.max(...serie.map(x => x.charrue_toutes), 1) / 3), yMax = Math.ceil(Math.max(...serie.map(x => x.charrue_toutes), 1) / pas) * pas;
  const bw = (l - m.g - m.d) / serie.length, W = Math.min(24, bw * .6), Y = v => h - m.b - (h - m.b - m.h) * v / yMax;
  let o = `<svg class="graphe" viewBox="0 0 ${l} ${h}" role="img" aria-label="Hectares de prairies permanentes retournés par an, de 2016 à 2024.">`;
  for (let v = 0; v <= yMax + 1e-9; v += pas) o += `<line class="grille" x1="${m.g}" x2="${l - m.d}" y1="${Y(v)}" y2="${Y(v)}"/><text class="axe" x="${m.g - 5}" y="${Y(v) + 4}" text-anchor="end">${fmt(v, 0)}</text>`;
  serie.forEach((x, i) => {
    const X = m.g + i * bw + (bw - W) / 2, ya = Y(x.charrue_anciennes), yt = Y(x.charrue_toutes);
    o += `<g data-tip="${x.annee - 1} → ${x.annee}|anciennes ${fmt(x.charrue_anciennes, 0)} ha · toutes ${fmt(x.charrue_toutes, 0)} ha"><rect class="touche" x="${m.g + i * bw}" y="${m.h}" width="${bw}" height="${h - m.b - m.h}"/><rect class="f1" x="${X}" y="${ya}" width="${W}" height="${Y(0) - ya}"/>${ya - yt > 3 ? `<rect class="f1b" x="${X}" y="${yt}" width="${W}" height="${ya - yt - 2}" rx="2"/>` : ""}</g><text class="axe" x="${X + W / 2}" y="${h - 5}" text-anchor="middle">${x.annee}</text>`;
  });
  return o + `</svg><p class="leg"><i class="f1"></i>prairies anciennes<i class="f1b"></i>prairies plus récentes · hectares mis en culture chaque année. Le pic de 2019 vient en partie d'un changement de règle administrative en 2018.</p>`;
}

// Trois trajectoires jusqu'en 2035 (hectares cumulés de prairies anciennes retournés depuis 2025)
export function trajSvg(tj, { l = 520, h = 200 } = {}) {
  const p = tj.prairies;
  if (tj.fiabilite === "fragile") return `<p class="note">Trop peu de prairies mises en culture ici pour tracer une courbe fiable. D'ici 2035 : entre ${fmt(p.on_laisse_faire.bas.at(-1), 0)} et ${fmt(p.on_laisse_faire.haut.at(-1), 0)} hectares.</p>`;
  const S = [["on_laisse_faire", "Si rien ne change", "1"], ["proteger_fragile", "Si on protège les zones sensibles", "2"], ["objectif", "Si on se fixe un objectif de réduction", "3"]];
  const an = p.annees, m = { g: 52, d: 84, h: 10, b: 22 }, top = Math.max(...p.on_laisse_faire.haut, 1), pas = pasNet(top / 3), yMax = Math.ceil(top / pas) * pas;
  const X = i => m.g + (l - m.g - m.d) * i / (an.length - 1), Y = v => h - m.b - (h - m.b - m.h) * v / yMax;
  const trait = vals => "M" + vals.map((v, i) => `${X(i).toFixed(1)} ${Y(v).toFixed(1)}`).join("L");
  let o = `<svg class="graphe" viewBox="0 0 ${l} ${h}" role="img" aria-label="Trois trajectoires de prairies anciennes retournées, en hectares cumulés de 2025 à 2035.">`;
  for (let v = 0; v <= yMax + 1e-9; v += pas) o += `<line class="grille" x1="${m.g}" x2="${l - m.d}" y1="${Y(v)}" y2="${Y(v)}"/><text class="axe" x="${m.g - 5}" y="${Y(v) + 4}" text-anchor="end">${fmt(v, 0)}</text>`;
  an.forEach((a, i) => { if (i % 2 === 0) o += `<text class="axe" x="${X(i)}" y="${h - 5}" text-anchor="middle">${a}</text>`; });
  const b = p.on_laisse_faire;
  o += `<path class="bande" d="${trait(b.haut)}L${b.bas.map((v, i) => `${X(i).toFixed(1)} ${Y(v).toFixed(1)}`).reverse().join("L")}Z"/>`;
  const fins = S.map(([k, , n]) => ({ n, v: p[k].median.at(-1), y: Y(p[k].median.at(-1)) })).sort((a, c) => a.y - c.y);
  fins.forEach((e, i) => { if (i && e.y < fins[i - 1].y + 13) e.y = fins[i - 1].y + 13; });
  S.forEach(([k, , n]) => { o += `<path class="ligne l${n}" d="${trait(p[k].median)}"/><circle class="bout f${n}" cx="${X(an.length - 1)}" cy="${Y(p[k].median.at(-1))}" r="4"/>`; });
  fins.forEach(e => { o += `<text class="etiq" x="${X(an.length - 1) + 8}" y="${e.y + 4}">${fmt(e.v, 0)} ha</text>`; });
  const lw = (l - m.g - m.d) / (an.length - 1);
  an.forEach((a, i) => { o += `<g data-tip="D'ici ${a}|${S.map(([k, nom]) => `${nom.split(" (")[0]} : ${fmt(p[k].median[i], 0)} ha`).join(" · ")}"><rect class="touche" x="${X(i) - lw / 2}" y="${m.h}" width="${lw}" height="${h - m.b - m.h}"/></g>`; });
  return o + `</svg><p class="leg">${S.map(([, nom, n]) => `<i class="trait f${n}"></i>${nom}`).join("")} · zone claire : marge d'incertitude du premier scénario. Hectares cumulés depuis 2025.</p>`;
}

// Tableau triable. cols : [{ k, n, d?, texte? }] ; le clic sur un en-tête appelle trier(k), sur une ligne choisir(code)
export function tableau(el, lignes, cols, { sel = "", tri, choisir, trier }) {
  const c = cols.find(x => x.k === tri) || cols[1];
  // Les territoires exclus des comparaisons (presque entièrement hors de Normandie) restent en fin de tableau
  const rows = [...lignes].sort((a, b) => (!!a.exclu_comparaisons - !!b.exclu_comparaisons) || (c.texte ? String(a[c.k]).localeCompare(String(b[c.k]), "fr") : (b[c.k] ?? -Infinity) - (a[c.k] ?? -Infinity)));
  el.innerHTML = `<table class="t"><thead><tr>${cols.map(x => `<th scope="col" data-k="${x.k}"${x.k === c.k ? ' aria-sort="descending"' : ""}>${esc(x.n)}</th>`).join("")}</tr></thead><tbody>${rows.map(r => `<tr data-code="${r.code}"${r.code === sel ? ' class="sel"' : ""}>${cols.map((x, i) => i ? `<td>${x.texte ? esc(r[x.k]) : fmt(r[x.k], x.d)}</td>` : `<td>${esc(r[x.k])}</td>`).join("")}</tr>`).join("")}</tbody></table>`;
  el.onclick = e => { const th = e.target.closest("th[data-k]"), tr = e.target.closest("tr[data-code]"); if (th) trier(th.dataset.k); else if (tr) choisir(tr.dataset.code === sel ? "" : tr.dataset.code); };
}

/* ---------- blocs métier, communs aux maquettes (d = région ou fiche de territoire) ---------- */
export const tuilesCles = d => `<div class="tuiles">
  ${tuile("Prairies anciennes disparues", `${fmt(d.bilan.prairies_anciennes_perdues_ha_an, 0)} ha par an`, `soit ${fmt(d.bilan.perte_anciennes_pct_stock_an, 2)} % de leur surface chaque année`)}
  ${tuile("Part due aux constructions", `${fmt(d.bilan.part_beton_anciennes_pct, 1)} à ${fmt(d.bilan.part_beton_anciennes_haute_pct, 1)} %`, "le reste vient de la mise en culture")}
  ${tuile("En comptant les prairies récentes", `${fmt(d.bilan.prairies_perdues_ha_an, 0)} ha par an`, "estimation haute")}
  ${tuile("Terres urbanisées, 2021 à 2024", `${fmt(d.sobriete.enveloppe_consommee_pct, 0)} %`, "du repère national pour 2021-2030")}
  ${tuile("Friches à restaurer en priorité", fmt(d.friches.n_gain_rapide, 0), `${fmt(d.friches.friches_gain_rapide_ha, 0)} hectares, à vérifier sur place`)}</div>`;
export const barresBilan = d => barres([
  { n: "Prairies anciennes mises en culture", v: d.charrue.charrue_anciennes_fenetre_ha_an, c: "f1", t: `${fmt(d.charrue.charrue_anciennes_fenetre_ha_an)} ha par an` },
  { n: "… avec les prairies récentes", v: d.charrue.charrue_fenetre_ha_an, c: "f1b", t: `${fmt(d.charrue.charrue_fenetre_ha_an)} ha par an` },
  { n: "Prairies anciennes construites", v: d.beton.beton_sur_pp_anciennes_ha_an, c: "f2", t: `${fmt(d.beton.beton_sur_pp_anciennes_ha_an)} ha par an` },
  { n: "Tous terrains construits", v: d.beton.beton_total_ha_an, c: "f2b", t: `${fmt(d.beton.beton_total_ha_an)} ha par an` }])
  + `<p class="note">Mêmes années pour les quatre lignes : 2019 à 2023 selon le département. Une prairie est dite « mise en culture » quand l'agriculteur y déclare une culture l'année suivante.</p>`;
export const tableMilieux = d => `<table class="t"><thead><tr><th scope="col">Milieu naturel, hectares par an</th><th scope="col">Construit</th><th scope="col">Mis en culture</th></tr></thead><tbody>${[
  ["Zones humides recensées", d.milieux_beton.beton_zh_ha_an, d.milieux_charrue.charrue_zh_fen_ha_an], ["Zones probablement humides", d.milieux_beton.beton_mph_ha_an, d.milieux_charrue.charrue_mph_fen_ha_an],
  ["Sites Natura 2000", d.milieux_beton.beton_natura2000_ha_an, d.milieux_charrue.charrue_natura2000_fen_ha_an], ["Zones d'intérêt écologique majeur (ZNIEFF 1)", d.milieux_beton.beton_znieff1_ha_an, d.milieux_charrue.charrue_znieff1_fen_ha_an],
  ["Grands ensembles naturels (ZNIEFF 2)", d.milieux_beton.beton_znieff2_ha_an, null]].map(r => `<tr><td>${r[0]}</td><td>${fmt(r[1])}</td><td>${fmt(r[2])}</td></tr>`).join("")}</tbody></table>
  <p class="note">Mettre une prairie en culture dans ces zones n'est pas interdit en soi.</p>`;
export const blocFoncier = d => `<div class="tuiles">
  ${tuile("Terres urbanisées de 2021 à 2024", `${fmt(d.sobriete.conso_2021_2025_ha, 0)} ha`, `soit ${fmt(d.sobriete.enveloppe_consommee_pct, 0)} % du repère national`)}
  ${tuile("Si le rythme continue, fin 2030", `${fmt(d.sobriete.projection_2031_pct, 0)} %`, "du repère national")}
  ${tuile("Sols rendus à la nature", `${fmt(d.sols_rendus.desartif_sols_ha_an)} ha par an`, "anciens sols bâtis ou goudronnés redevenus végétaux")}</div>
  <p class="note">Le repère national : urbaniser moitié moins de terres en 2021-2030 qu'en 2011-2020. Ce n'est pas l'objectif du territoire : la Région fixe à chacun son propre taux dans son schéma d'aménagement (SRADDET).${d.sobriete.alerte_flux_unique ? " Attention : un seul projet pèse plus de la moitié du total de ce territoire." : ""}</p>`;
const SOLIDITE = { exploitable: "bonne", indicative: "moyenne", fragile: "faible", "région": "bonne" };
export function blocTrajectoires(d, hyp, taille) {
  const p = d.trajectoires.prairies, fragile = d.trajectoires.fiabilite === "fragile";
  return trajSvg(d.trajectoires, taille) + (fragile ? "" : `<div class="tuiles" style="margin-top:8px">
    ${tuile("Si rien ne change, d'ici 2035", `${fmt(p.on_laisse_faire.median.at(-1), 0)} ha`, `de prairies anciennes mises en culture, soit ${fmt(p.on_laisse_faire.pct_stock_2035, 1)} % de celles qui restent`)}
    ${tuile("Si on protège les zones sensibles", `${fmt(p.proteger_fragile.epargne_2035_ha, 0)} ha sauvés`, "zones humides et sites naturels reconnus")}
    ${tuile(`Pour limiter la perte à ${fmt(hyp.objectif_perte_2035_pct, 0)} %`, `${fmt(p.objectif.effort_pct, 0)} % de moins`, `passer de ${fmt(p.labour_actuel_ha_an, 0)} à ${fmt(p.objectif.labour_cible_ha_an, 0)} hectares par an`)}</div>`)
    + `<p class="note">Ce sont des scénarios, pas des prévisions. L'objectif de ${fmt(hyp.objectif_perte_2035_pct, 0)} % est un exemple. Solidité de l'estimation ici : ${SOLIDITE[d.trajectoires.fiabilite] || "moyenne"}.</p>`;
}
export const tableFriches = (liste, n = 8) => liste.length ? `<table class="t"><thead><tr><th scope="col">Friche</th><th scope="col">ha</th><th scope="col">Score</th><th scope="col">Classe</th><th scope="col">À vérifier</th></tr></thead><tbody>${liste.slice(0, n).map(f => `<tr data-tip="${esc(f.libelle)}|${esc(f.raisons.join(" · "))}"><td>${esc(f.libelle)}</td><td>${fmt(f.surface_ha)}</td><td>${fmt(f.score_biodiversite, 0)}</td><td><span class="etq">${esc(CLASSES_FRICHES[f.classe]?.[0] || f.classe)}</span></td><td style="white-space:normal;text-align:left">${esc(f.vigilance.join(" · ") || "—")}</td></tr>`).join("")}</tbody></table>${liste.length > n ? `<p class="note">${liste.length - n} autres friches dans ce territoire.</p>` : ""}` : `<p class="note">Aucune friche d'au moins 0,1 ha recensée ici.</p>`;
