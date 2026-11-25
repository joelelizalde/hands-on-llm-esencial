# LLM en la práctica — Edición esencial en español

Manual de estudio estático (sin build para el lector y sin dependencias en el navegador) para entender y aplicar modelos de lenguaje: tokens, embeddings, atención, decodificación, clasificación, prompting, búsqueda semántica, RAG, fine-tuning y multimodalidad.
Alineado temáticamente con *Hands-On Large Language Models*, de Jay Alammar y Maarten Grootendorst, pero con texto, ejemplos y diagramas originales.

## Qué incluye

- **21 lecciones** en **7 módulos** (3 lecciones y 1 evaluación por módulo), siguiendo el recorrido del libro: fundamentos del lenguaje → tokens y embeddings → interior del Transformer → clasificación y agrupamiento → prompt engineering → búsqueda y RAG → adaptación y producción.
- Lectura continua: botón «Completar y seguir», navegación con ← y →, temario lateral siempre disponible.
- **7 evaluaciones** de 4 preguntas con explicaciones y **21 ejercicios** aplicados.
- Progreso guardado en `localStorage`, glosario con buscador y modo claro/oscuro.
- Buscador global con atajo `⌘K` / `Ctrl+K`.
- **21 diagramas originales** en SVG (flujo, capas, bucle, matriz, curva, barras y atención).
- **68 términos** en el glosario.
- Manual en PDF: `Hands-On-LLM-Esencial.pdf` (54 páginas).
- Tipografías locales (Fraunces + Inter), sin depender de Google Fonts.

## Estructura

```
index.html                      Portada y temario completo
hllm1l1.html … hllm7q.html      21 lecciones y 7 evaluaciones
glosario.html                   Glosario con búsqueda y filtro por letra
progreso.html                   Progreso por módulo
css/curso.css                   Diseño editorial responsive
js/curso.js                     Navegación, progreso, búsqueda y quizzes
assets/fonts/                   Tipografías locales
modulos/m01.py … m07.py         Contenido de cada módulo
contenido.py                    Reúne módulos, metadatos y glosario
build_site.py                   Generador del sitio
build_pdf.py                    Generador del PDF (WeasyPrint)
Hands-On-LLM-Esencial.pdf
```

## Módulos

1. **Del texto al modelo** — representación vectorial, atención, Transformer y fases de entrenamiento.
2. **Tokens y embeddings** — tokenización, embeddings contextuales, similitud y recomendación.
3. **Dentro del Transformer** — recorrido de una predicción, decodificación, contexto y mejoras modernas.
4. **Clasificar y agrupar texto** — encoders, clasificación generativa, clustering y modelado de temas.
5. **Prompt engineering** — anatomía del prompt, ejemplos en contexto, razonamiento y verificación.
6. **Búsqueda semántica y RAG** — recuperación híbrida, chunking, generación fundamentada y evaluación.
7. **Adaptar y ampliar el modelo** — fine-tuning de encoders, LoRA/QLoRA, multimodalidad y sistemas en producción.

## Correspondencia con el libro

| Capítulo | Tema | Lección |
|---|---|---|
| 01 | Introducción a los LLM | `hllm1l1` |
| 01 | Atención y familias de modelos | `hllm1l2` |
| 01 | Entrenamiento y aplicación | `hllm1l3` |
| 02 | Tokens y tokenización | `hllm2l1` |
| 02 | Embeddings de tokens y contexto | `hllm2l2` |
| 02 | Embeddings de texto y recomendación | `hllm2l3` |
| 03 | Recorrido y decodificación | `hllm3l1`, `hllm3l2` |
| 03 | Mejoras de arquitectura | `hllm3l3` |
| 04 | Clasificación con representaciones y generación | `hllm4l1`, `hllm4l2` |
| 05 | Clustering y topic modeling | `hllm4l3` |
| 06 | Prompt engineering | `hllm5l1`, `hllm5l2`, `hllm5l3` |
| 07 | Cadenas, memoria y agentes | `hllm5l2`, `hllm7l3` |
| 08 | Búsqueda semántica y RAG | `hllm6l1`, `hllm6l2`, `hllm6l3` |
| 09 | Modelos multimodales | `hllm7l3` |
| 10 | Crear modelos de embedding | `hllm2l3`, `hllm7l1` |
| 11 | Fine-tuning de representación | `hllm7l1` |
| 12 | Fine-tuning generativo y preferencias | `hllm7l2` |

## Regenerar

```bash
python3 build_site.py          # solo el sitio
python3 build_site.py --pdf    # sitio + manual en PDF
```

El PDF se compone con WeasyPrint (probado con 70.x) a partir del mismo contenido y las mismas fuentes.

## Añadir o editar contenido

Cada módulo vive en `modulos/mNN.py` y expone un diccionario `MODULE`:

- `num`, `title`, `sub`
- `lessons`: lista de lecciones con `id`, `lnum`, `title`, `minutes`, `lead`, `diagram`, `caption`, `sections`, `brief`, `keys`, `example`, `caution`, `search`.
- `quiz`: `id`, `title`, `summary`, `questions`, `exercises`, `search`.

Los diagramas se declaran como tuplas: `("flow", [...])`, `("stack", [...])`, `("loop", [...])`, `("attention", [...])`, `("matrix", {...})`, `("curve", {...})`, `("latency", {...})` o `("bars", [...])`.
Al cambiar contenido, vuelve a ejecutar `build_site.py --pdf` para regenerar páginas y PDF.

## Atajos

| Tecla | Acción |
|---|---|
| ← / → | Lección anterior / siguiente |
| `C` | Marcar la página actual como completada |
| `/` o `⌘K` | Abrir el buscador |
| `Esc` | Cerrar buscador o menú |
| `?` | Recordatorio de atajos |

## Datos locales

El progreso y el tema se guardan solo en el navegador:

- `hllm_progress_v1`
- `hllm_theme`

No se envía nada a un servidor.

## Publicar en GitHub Pages

1. Crea un repositorio con el contenido de esta carpeta en la raíz.
2. **Settings → Pages → Deploy from a branch → main → / (root)**.
3. El sitio quedará en `https://<usuario>.github.io/<repositorio>/`.

No subas claves ni tokens al repositorio: el curso es estático y no necesita credenciales.
