"""Regenera js/productos.js y fotos/LISTA_DE_FOTOS.csv a partir del CSV del catalogo.
Uso:   python tools/actualizar_catalogo.py Productos.csv
Columnas usadas: cbarras, nombre_producto, descripcion_producto, precio_venta
"""
import sys, re, csv, json, unicodedata, collections

EXCLUIR = {"LECTOR DE CODIGOS", "AGILER"}   # articulos de uso interno de la tienda

REGLAS = [  # (categoria, patron) -> se evalua en orden
    ("peces",      r"^(PECES|TETRAS|TIBURONES|GOLDFISH)\b"),
    ("adornos",    r"ADONO|ADORNO|TRONCO MOPAI"),
    ("alimentos",  r"^ALIMENTO\b"),
    ("peceras",    r"PECERA"),
    ("filtros",    r"FILTRO|BOMBA|REPUEST|CANUTILLOS|DIFUSORA"),
    ("sustratos",  r"GRABA|GRAVA|ARENA|PIEDRA NATURAL|PLANTA|SUSTRA[CT]O"),
    ("cuidado",    r"^PRODUCTO |AQUA PLUS|CLEAR FAST"),
]
CORRECCIONES = [("ADONOR", "ADORNO"), ("ADONO", "ADORNO"), ("REPUESTRO", "REPUESTO"), ("MEDI0", "MEDIO"),
    ("MEDIUN", "MEDIUM"), ("DONLE", "DOBLE"), (r"\bIFUSORA", "DIFUSORA"), ("ARMEJA", "ALMEJA"), ("SUMEGIBLE", "SUMERGIBLE"), ("HUMIFICADOR", "HUMIDIFICADOR"), ("ARTFICIALES", "ARTIFICIALES"),
    ("GRABA", "GRAVA"), ("SUSTRACTO", "SUSTRATO"), ("COLA DE ESPADAD", "COLA DE ESPADA"), ("KIT E PECERA", "KIT DE PECERA"),
    ("BOMBA  DE", "BOMBA DE"), ("PECES KOI TUCEDO", "PECES KOI TUXEDO")]
DESCRIPCIONES = {  # descripciones que en el CSV no correspondian al producto
    "ANILLO ALIMENTADOR DE PECES": "Anillo flotante para alimentar a los peces. Mantiene la comida en un solo punto de la superficie y evita que se disperse por el acuario.",
    "RED PARA PECES": "Red para peces. Útil para capturar y trasladar a los peces de forma segura durante la limpieza o el cambio de pecera.",
}
ACENTOS = [("Sifon","Sifón"),("Lampara","Lámpara"),("Oxigeno","Oxígeno"),("Bateria","Batería"),("Dias","Días"),("Avion","Avión"),
    ("Aerea","Aérea"),("Angeles","Ángeles"),("Magnetico","Magnético")]
UPPER = {"LED", "XXL", "GL", "GLS", "GR", "ML", "KG", "FM", "KF", "SF", "L", "M", "S", "XL"}
MINUS = {"DE", "DEL", "CON", "PARA", "EN", "Y", "P/"}

def sin_acentos(s): return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode()

def limpiar(n):
    n = re.sub(r"\s+", " ", n.replace("´´", '"').replace("´", "'")).strip()
    for a, b in CORRECCIONES: n = re.sub(a, b, n) if a.startswith("\\b") else n.replace(a, b)
    n = re.sub(r"(\w)- (\w)", r"\1-\2", n); n = re.sub(r"\(\s+", "(", n); n = re.sub(r"(\d)\(", r"\1 (", n)
    if n.count("(") > n.count(")"):                    # nombre cortado en el sistema
        i = n.rfind("("); frag = n[i:]
        n = n[:i].strip() if frag.rstrip().endswith(",") else n + ")"
    n = re.sub(r"\s*,\s*\)", ")", n).replace(" )", ")")
    def parte(w, i):
        core = re.sub(r"[^\w/]", "", w).upper()
        if core in UPPER or re.search(r"\d", w) and not re.fullmatch(r"[\d.]+", core): return w.upper()
        if core in MINUS and i: return w.lower()
        return re.sub(r"[A-Za-zÁÉÍÓÚÑ]+", lambda m: m.group().capitalize(), w, count=1)
    out = ["-".join(parte(x, i) for x in w.split("-")) for i, w in enumerate(n.split(" "))]
    n = " ".join(out)
    for a, b in ACENTOS: n = re.sub(r"\b" + a + r"\b", b, n)
    return n

def categoria(n):
    for cat, pat in REGLAS:
        if re.search(pat, n): return cat
    return "accesorios"

def slug(s): return re.sub(r"[^a-z0-9]+", "-", sin_acentos(s).lower()).strip("-")

filas = list(csv.DictReader(open(sys.argv[1], encoding="utf-8-sig", newline="")))
filas = [r for r in filas if r["nombre_producto"].strip() and r["nombre_producto"].strip().upper() not in EXCLUIR]
cuenta = collections.Counter(r["cbarras"].strip() for r in filas)
usados, usados_n, out = set(), set(), []
for r in filas:
    bruto, nom = r["nombre_producto"].strip(), r["nombre_producto"].strip().upper()
    cb = r["cbarras"].strip()
    valido = bool(cb) and not re.fullmatch(r"\d(\.\d+)?E\+\d+", cb, re.I) and cuenta[cb] == 1
    nombre = limpiar(bruto)
    foto = cb if valido else slug(nombre)
    base, k = foto, 2
    while foto in usados: foto, k = f"{base}-{k}", k + 1     # nunca dos productos con la misma foto
    usados.add(foto)
    fn = base_n = slug(nombre); k = 2
    while fn in usados_n: fn, k = f"{base_n}-{k}", k + 1
    usados_n.add(fn)
    out.append({"foto": foto, "foto_nombre": fn, "codigo": cb if valido else "", "nombre": nombre,
                "descripcion": DESCRIPCIONES.get(nom, r["descripcion_producto"].strip()),
                "precio": float(r["precio_venta"]) if "." in r["precio_venta"] else int(r["precio_venta"]),
                "cat": categoria(nombre.upper())})
with open("js/productos.js", "w", encoding="utf-8") as f:
    f.write("// Generado desde el CSV. Puedes editar nombre, descripcion, precio o categoria a mano.\n")
    f.write("// 'foto' = nombre del archivo en /fotos (sin .jpg). Es el codigo de barras si es valido; si no, un nombre corto.\n")
    f.write("const PRODUCTOS = " + json.dumps(out, ensure_ascii=False, indent=1) + ";\n")
with open("fotos/LISTA_DE_FOTOS.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f); w.writerow(["foto_con_codigo_de_barras", "foto_con_nombre (alternativa)", "producto"])
    for p in out: w.writerow([(p["foto"] + ".jpg") if p["codigo"] else "(sin codigo valido)", p["foto_nombre"] + ".jpg", p["nombre"]])
print(len(out), "productos |", sum(1 for p in out if p["codigo"]), "con codigo de barras valido")
