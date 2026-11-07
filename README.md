# Editor Iriza · referencias de estilo

Las imágenes de referencia de los 61 formatos de [Editor Iriza](https://github.com/davidiriza-lab/editor-iriza) (Editor 1–50, Pizarra Pro y los 10 "Editor N · pantalla"), más un muestrario para verlas corriendo.

| Archivo | Qué es |
|---|---|
| `index.html` | Muestrario: los 61 formatos con sus cuadros corriendo a su tiempo real, buscador, familias y una ficha por formato con el encargo para Claude. Se abre con doble clic |
| `formatos/<formato>/hoja.jpg` | Hoja de contacto del video de referencia |
| `formatos/<formato>/paleta.png` | Paleta de colores medida |
| `formatos/<formato>/cuadros/` | Cuadros en los momentos clave (`000.50s.jpg` = segundo 0.5) |

## Instalar todo (editor + referencias)

Necesitas una Mac con chip Apple, [Claude Code](https://claude.com/claude-code) y las herramientas base:

```
brew install ffmpeg node uv
xcode-select --install
brew install --cask google-chrome
```

Luego:

```
git clone https://github.com/davidiriza-lab/editor-iriza-referencias.git
cd editor-iriza-referencias
./instalar.sh
```

Baja el editor junto a esta carpeta (`../editor-iriza`), le pone las referencias e instala todo (entorno de Python, Whisper, paquetes y la skill de Claude). Si ya tienes el editor: `./instalar.sh <carpeta-del-editor>` solo copia las referencias. En el editor esas imágenes están en `.gitignore`, así que no terminan en tus commits.

## De quién son las imágenes

Los cuadros salen de videos públicos de otros creadores y **siguen siendo de sus autores**. Están aquí como guía de look para editar (ritmo, tipografía, color, composición), no para copiar su contenido ni su identidad. No están cubiertos por la licencia MIT de este repo.

Si eres autor de alguno de esos videos y quieres que se quite, abre un issue y se retira.

## Licencia

El código (`instalar.sh`, `muestrario.py`, `muestrario.plantilla.html`) es MIT. Las imágenes de `formatos/` son de sus autores (ver arriba).
