# Monografía del grupo 2

`monografia.pdf` es la versión compilada según el modelo
`../Computacion_Cuantica_Proyecto_semestral_parte_1.pdf`: portada institucional,
logos, tabla de integrantes, índice, texto en una columna, encabezados y páginas
numeradas. Conserva el título del proyecto y desarrolla el contenido del informe
revisado: fundamentos, cuatro antecedentes, fuentes complementarias, metodología,
resultados propios, limitaciones y 16 referencias.

Para compilar desde esta carpeta:

```bash
latexmk -jobname=monografia -pdf -interaction=nonstopmode -halt-on-error main.tex
```

En Overleaf, cargar todos los archivos de esta carpeta y seleccionar `main.tex`
como documento principal; compilador pdfLaTeX con bibliografía BibTeX.

- `main.tex`: formato, portada e índice.
- `resumen.tex` y `contenido.tex`: texto editable.
- `referencias.bib`: copia de las 16 referencias revisadas.
- `resultados.tex`: copia de las macros generadas por el experimento.
- `imagenes/`: logos, circuitos y gráficas necesarios para compilar.

La carpeta es autónoma para su compilación. Si se regeneran los resultados del
experimento o se modifica la bibliografía del artículo, actualizar sus copias
antes de recompilar esta monografía. Los algoritmos y resultados originales no
se modificaron. El código de Efraín se conserva como 160337, igual que en el PDF
modelo, a falta de una corrección confirmada.
