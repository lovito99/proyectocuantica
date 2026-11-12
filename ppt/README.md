# Presentación del proyecto

- **[diapositivas.pdf](diapositivas.pdf)**: presentación completa, 31 páginas en 16:9.
- **[diapositivas.tex](diapositivas.tex)**: fuente editable en LaTeX Beamer.
- **[`imagenes/`](imagenes/)**: logos originales de la UNSAAC y de la carrera,
  extraídos del PDF `Computacion_Cuantica_Proyecto_semestral_parte_1.pdf`, con
  su transparencia. La portada conserva su distribución: universidad a la
  izquierda y carrera a la derecha, bajo los nombres institucionales.

Las diapositivas 1–25 están pensadas para una exposición de unos 20 minutos.
Las 26–31 contienen tablas detalladas y referencias para apoyar las preguntas.

| Diapositivas | Contenido |
| --- | --- |
| 1–3 | Presentación, pregunta de investigación, problema y objetivos |
| 4–6 | Qubits, Dirac, producto tensorial, unitariedad, compuertas y QFT |
| 7–11 | Los cuatro artículos y su comparación |
| 12–19 | Metodología, registros, semisumadores, funciones, código y compilación |
| 20–23 | Corrección, superposición, tablas y gráficas de recursos |
| 24–25 | Limitaciones, trabajo pendiente, conclusiones y reproducción |
| 26–31 | Tablas de apoyo, fundamentos complementarios y las 16 referencias |

Para regenerar desde la raíz del repositorio:

```bash
make presentacion
```

También funciona `make ppt`. Se necesitan `latexmk`, pdfLaTeX, Beamer, TikZ y
listings. La presentación utiliza las macros y figuras de
`../informe/latex/resultados/`; deben conservarse esas rutas al editarla.

Las cifras corresponden al experimento ideal ya incluido en el repositorio.
El caso de 16 entradas describe compilación; la validación exhaustiva llega a
8 entradas. Las métricas de costo excluyen preparación y mediciones.

Las 16 referencias se generan con BibTeX desde
`../informe/latex/referencias.bib`, compartida con el informe. Las páginas 29–31
contienen la lista completa; la página 28 explica las seis fuentes añadidas.
