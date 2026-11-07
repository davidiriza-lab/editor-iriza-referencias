#!/bin/bash
# Copia las referencias de estilo a una copia del editor.
# Uso: ./instalar.sh                          baja el editor público junto a esta carpeta (../editor-iriza) si no
#                                             existe, le pone las referencias e instala todo
#      ./instalar.sh <carpeta-del-editor>     solo copia las referencias a esa copia del editor
# Solo escribe hoja.jpg, paleta.png y cuadros/ dentro de plantillas/formatos/<formato>/; no toca nada más.
# En el editor, esos archivos están en .gitignore: no se suben aunque la copia tenga remoto.
set -e
AQUI="$(cd "$(dirname "$0")" && pwd)"
COMPLETO=0
if [ -z "$1" ]; then
  COMPLETO=1; ED="$(dirname "$AQUI")/editor-iriza"
  if [ ! -d "$ED" ]; then
    echo "Bajando el editor en $ED…"
    git clone -q https://github.com/davidiriza-lab/editor-iriza.git "$ED"
  else
    echo "Uso el editor que ya está en $ED"
  fi
else
  ED="$1"
fi
F="$ED/plantillas/formatos"
[ -d "$F" ] || { echo "No encuentro $F: ¿es la carpeta del editor?"; exit 1; }
grep -q "hoja.jpg" "$ED/.gitignore" 2>/dev/null || { echo "El .gitignore de $ED no ignora las referencias; no copio nada."; exit 1; }
n=0
for o in "$AQUI"/formatos/*/; do
  d=$(basename "$o")
  [ -d "$F/$d" ] || { echo "· se salta $d (no existe en el editor)"; continue; }
  rsync -a "$o" "$F/$d/"; n=$((n + 1))
done
echo "Listo: referencias de $n formatos en $F"
if [ "$COMPLETO" = 1 ]; then
  echo "Instalando el editor (entorno, Whisper, paquetes, skill)…"
  (cd "$ED" && ./instalar.sh) && (cd "$ED" && ./verificar.sh --sin-render || true)
  echo "Todo listo. Abre $ED con Claude Code y pásale tu video."
fi
