#!/usr/bin/env python3
"""Genera index.html: el muestrario de los 61 formatos con sus cuadros de referencia corriendo.

Uso: python3 muestrario.py [carpeta-del-editor] [--publico]   (por defecto ../editor-iriza o ~/proyectos/editor-iriza)

Lee plantillas/formatos/formatos.json del editor (nombres, familias, descripciones, paletas) y la lista de
cuadros de formatos/<formato>/cuadros/ de este repo, y escribe index.html con todo incrustado. La página
usa rutas relativas a las imágenes de este repo: se abre con doble clic, sin servidor.
"""

import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def editor() -> Path:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    candidatos = [Path(args[0]).expanduser()] if args else [AQUI.parent / "editor-iriza", Path.home() / "proyectos" / "editor-iriza"]
    for c in candidatos:
        f = c / "plantillas" / "formatos" / "formatos.json"
        if f.is_file():
            return f
    sys.exit("✗ No encuentro plantillas/formatos/formatos.json; pasa la carpeta del editor")


def tiempo(nombre: str) -> float:
    m = re.match(r"(\d+(?:\.\d+)?)s", nombre)
    return float(m.group(1)) if m else 0.0


def main() -> None:
    fj = editor()
    d = json.loads(fj.read_text())
    familias = {k: {c: v.get(c, "") for c in ("nombre", "idea", "texto", "mov", "audio")} for k, v in d["familias"].items()}
    formatos = []
    for e in d["editores"]:
        carpeta = Path(e["carpeta"]).name
        cu = AQUI / "formatos" / carpeta / "cuadros"
        if not cu.is_dir():
            print(f"· sin cuadros: {carpeta}")
            continue
        cuadros = sorted((f.name for f in cu.iterdir() if f.suffix == ".jpg"), key=tiempo)
        horizontal = False
        try:   # ancho y alto del primer cuadro (JPEG SOF), sin dependencias
            b = (cu / cuadros[0]).read_bytes()
            i = 2
            while i < len(b):
                marca, largo = b[i + 1], int.from_bytes(b[i + 2:i + 4], "big")
                if marca in (0xC0, 0xC1, 0xC2):
                    alto, ancho = int.from_bytes(b[i + 5:i + 7], "big"), int.from_bytes(b[i + 7:i + 9], "big")
                    horizontal = ancho > alto
                    break
                i += 2 + largo
        except (IndexError, OSError):
            pass
        formatos.append({
            "n": e["n"], "nombre": e["nombre"], "apodo": e.get("apodo", ""), "familia": e.get("familia", ""),
            "detalle": e.get("detalle", ""), "dur": e.get("dur", 0), "cortes": e.get("cortes", 0),
            "paleta": e.get("paleta", []), "pct": e.get("paleta_pct", []), "dir": carpeta,
            "cuadros": [[tiempo(c), c] for c in cuadros], "horizontal": horizontal,
            "hoja": (AQUI / "formatos" / carpeta / "hoja.jpg").is_file(),
        })
    datos = json.dumps({"familias": familias, "formatos": formatos}, ensure_ascii=False, separators=(",", ":"))
    plantilla = (AQUI / "muestrario.plantilla.html").read_text()
    salida = plantilla.replace("/*__DATOS__*/null", datos.replace("</", "<\\/"))
    salida = salida.replace("__TOTAL__", str(len(formatos))).replace("__FAMILIAS__", str(len({f["familia"] for f in formatos})))
    pie = ("Los cuadros son de videos de otros creadores y siguen siendo de sus autores: están aquí como guía de look "
               "para editar, no para copiar su contenido. Si eres autor de alguno y quieres que lo quite, abre un issue en el repo.")
    salida = salida.replace("__PIE__", pie)
    (AQUI / "index.html").write_text(salida)
    print(f"✓ index.html · {len(formatos)} formatos · {sum(len(f['cuadros']) for f in formatos)} cuadros")


if __name__ == "__main__":
    main()
