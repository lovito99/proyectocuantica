# Presentación del grupo 2

- `diapositivas.pdf`: 25 páginas en formato 16:9.
- `diapositivas.pptx`: 25 diapositivas para presentar en PowerPoint.
- `diapositivas.tex`: fuente editable en LaTeX Beamer.

Se mantiene el orden: proyecto y fundamentos (1–5), antecedentes (6–8),
diseño e implementación (9–16), resultados (17–18), limitaciones y conclusiones
(19–20), tablas y fundamentos de apoyo (21–22), las 16 referencias (23–25).
Se agruparon pregunta/objetivos, pares de antecedentes, validación/resultados
y tabla/gráfica de recursos. Se mantienen las cifras y los límites del estudio.
La fuente usa 12 pt; las páginas densas ajustan el contenido a la zona disponible.

El PowerPoint conserva cada página como una imagen de alta resolución, con
transición y avance manual. Puede exponerse con F5 o Mayús+F5. Los textos y
fórmulas se editan en el archivo LaTeX y luego se regeneran ambos formatos;
no son cuadros de texto editables dentro de PowerPoint.

Desde la raíz:

```bash
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error ppt/diapositivas.tex
python3 herramientas/exportar_powerpoint.py
```

La exportación necesita Poppler (`pdftoppm`) y Python 3. Usa la plantilla OOXML
incluida en `herramientas/recursos/plantilla_presentacion.pptx`. Las tablas y
figuras proceden de `informe/latex/resultados/`, y la bibliografía compartida es
`informe/latex/referencias.bib`.
