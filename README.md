# 🐠 Acuario Alduey – Catálogo web

Página estática (HTML/CSS/JS). No necesita instalar nada: abre `index.html` o súbela a GitHub Pages.

## Cómo agregar fotos
Pon la foto en la carpeta **`fotos/`**. Puedes nombrarla de **dos formas** (sirve cualquiera):
- **Con el nombre del producto**, en minúsculas, sin tildes y con guiones: `fotos/adorno-doris.jpg`, `fotos/peces-koi.jpg`
- **Con el código de barras**, si el producto lo tiene: `fotos/15561171014.jpg`

Formatos aceptados: `.jpg`, `.jpeg`, `.png`, `.webp`. Si no hay foto, la tarjeta muestra un pez ("Foto próximamente").

**¿Cómo sé cómo se llama el archivo de cada producto?**
- Abre la página con **`index.html?fotos`** (agrega `?fotos` al final de la dirección): cada tarjeta muestra el nombre exacto del archivo.
- O abre **`fotos/LISTA_DE_FOTOS.csv`** con Excel.

(En el CSV original Excel dañó el código de barras de varios productos, por eso esos solo tienen la opción del nombre.)

Tip: usa fotos cuadradas y livianas (unos 600×600 px, menos de 200 KB) para que la página cargue rápido.

## Cambiar nombres, descripciones, precios o categorías
Edita `js/productos.js` (cada producto tiene `foto`, `codigo`, `nombre`, `descripcion`, `precio`, `cat`).
Categorías: `peces`, `peceras`, `filtros`, `adornos`, `sustratos`, `alimentos`, `cuidado`, `accesorios`.

Si prefieres actualizar desde el CSV del sistema:
```
python tools/actualizar_catalogo.py Productos.csv
```
(esto vuelve a generar `js/productos.js`, así que se pierden los cambios hechos a mano).
Para que no se dañen los códigos de barras, exporta el CSV sin abrirlo y guardarlo con Excel.

## WhatsApp
En `js/app.js`, pon tu número en `WHATSAPP` (ej. `"18095551234"`) y aparecerá un botón al final de la página.

## Publicar en GitHub Pages
1. Sube todo el contenido de esta carpeta a un repositorio.
2. En el repo: **Settings → Pages → Deploy from a branch → main / (root)**.
3. Tu página quedará en `https://TU-USUARIO.github.io/NOMBRE-REPO/`.
