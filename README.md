# Circuitos cuánticos reversibles en Qiskit

Avance del proyecto semestral de Computación Cuántica (IF460AIN), UNSAAC,
semestre 2026-II. Conserva los cuatro antecedentes de la primera entrega y añade
implementaciones, comprobaciones y resultados propios. El artículo sigue la
presentación del PDF modelo: dos columnas, franja de título, resumen en español
e inglés, objetivos, metodología, resultados y referencias IEEE.

Integrantes: Brayan Vladymir Molocho Condori (164244), Haider Alex Carpio Hermoza
(164563) y Efraín Vitorino Marín (160337). Docente: Raúl Huillca Huallparimachi.

## Archivos de entrega

- [Monografía del grupo 2](informe/monografia/monografia.pdf), [fuente LaTeX y compilación](informe/monografia/README.md), siguiendo el modelo de la primera entrega.

- [Artículo PDF](informe/avance_circuitos_reversibles.pdf).
- [ZIP para importar en Overleaf](informe/avance_overleaf.zip).
- [Fuente LaTeX](informe/latex/main.tex) y [bibliografía](informe/latex/referencias.bib).
- [Código Qiskit](proyecto/experimento.py) y [pruebas](tests/test_experimento.py).
- [Datos, métricas y figuras](informe/latex/resultados/).
- [Diapositivas en PDF](ppt/diapositivas.pdf), [PowerPoint](ppt/diapositivas.pptx) y [fuente Beamer](ppt/diapositivas.tex).

Los dos PDF proporcionados se mantienen en `informe/`. La revisión es dirigida,
basada en esos cuatro antecedentes; los resultados de simulación se generan
localmente. El alcance de esta entrega es circuitos reversibles. La guía adjunta
de aprendizaje automático exige además un modelo de clasificación o regresión y
una comparación de aprendizaje clásico/cuántico para cubrir esa rúbrica específica.

## Instalación

Entorno comprobado: Python 3.12.13, Qiskit 2.6.2, NumPy 2.5.4 y Matplotlib 3.11.2.
No requiere cuenta IBM, credenciales ni conexión a una QPU. Con
[uv](https://docs.astral.sh/uv/):

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements.txt
```

Si ya tienes Python 3.12 y pip:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Las versiones directas están fijadas en `requirements.txt`; el entorno completo
usado para obtener las cifras está en `requirements-lock.txt`. Para reconstruir
exactamente las versiones instaladas, usa ese archivo en lugar de `requirements.txt`.

## Ejecutar y verificar

Desde la raíz del repositorio:

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m proyecto.experimento
```

La ejecución verifica **40 casos** de tablas de verdad y **552 casos** de
escalamiento. Compara operadores completos de tres qubits, incluida la
compilación y sus permutaciones de salida, y obtiene 4096 muestras de un
semisumador con entradas en superposición. Los 12 tests incluyen suma modular,
tablas de verdad, fases, reversibilidad, conteo de población y exportación.

Para guardar una ejecución aparte:

```bash
.venv/bin/python -m proyecto.experimento --output /tmp/resultados-cuantica
```

Ejemplo de construcción interactiva:

```python
from proyecto.experimento import logic_gate, population_count

print(logic_gate("AND", "QFT").draw())
print(logic_gate("XOR", "Toffoli").draw())
circuito, acumulador = population_count(4)
print(circuito.draw())
print("Bits del conteo, de menor a mayor peso:", acumulador)
```

## Convenciones y comparación

Para dos entradas: `q[0]=a`, `q[1]=auxiliar=0`, `q[2]=b`. El semisumador deja
`a XOR b` en `q[0]`, `a AND b` en `q[1]` y conserva `b` en `q[2]`. Todas las
funciones de `logic_gate` colocan su salida en `q[1]`, mediante inversiones y un
SWAP cuando corresponde. Las cadenas impresas por Qiskit se leen `q[2]q[1]q[0]`.

La QFT implementa `t → (t+b) mod 4`, donde `t=q[0]+2*q[1]`; el diseño Toffoli
realiza exactamente la misma permutación. La comparación de matrices incluye los
ocho estados de entrada, también cuando el auxiliar vale uno. Las otras líneas
contienen información residual: estas plantillas no exigen conservar ambas entradas
originales. La plantilla XOR completa tampoco es un XOR mínimo de dos CNOT.

Para `N=2**k`, `population_count` usa `N+k` qubits. El acumulador reutiliza la
primera entrada y añade `k` auxiliares; sus índices se devuelven de menor a mayor
peso. El bit superior da AND y el inferior da paridad. `and_ladder` usa `2*N-1`
qubits, conserva las entradas y productos intermedios, y entrega AND en `q[2*N-2]`.
La tabla multientrada compara la tarea AND: sus registros residuales son distintos.

Ambos diseños se compilan a `{u, cx}`, con nivel 3, semilla 42, conectividad
completa y `qubits_initially_zero=False`. Los conteos excluyen preparación y
mediciones. Se guardan las permutaciones finales: un SWAP final puede eliminarse
mediante el etiquetado de salidas, y la comparación de operadores compilados las
considera con `Operator.from_circuit`.

Resultados propios para AND multientrada:

| Entradas | Qubits QFT / escalera | CX QFT / escalera | Profundidad QFT / escalera |
| --- | --- | --- | --- |
| 2 | 3 / 3 | 9 / 6 | 19 / 11 |
| 4 | 6 / 7 | 27 / 18 | 38 / 23 |
| 8 | 11 / 15 | 73 / 42 | 70 / 47 |
| 16 | 20 / 31 | 175 / 90 | 118 / 95 |

Se simulan exhaustivamente 2, 4 y 8 entradas; para 16 solo se construye y compila.
Las muestras y probabilidades corresponden a simulación ideal en CPU. El estudio
de ruido, conectividad física, MCX y QFT aproximada se reserva para la siguiente etapa.

## Datos y figuras

La carpeta `informe/latex/resultados/` contiene:

- `tablas_verdad.csv`: entradas, función, diseño, salida esperada/observada y probabilidad.
- `recursos_dos_entradas.csv` y `escalamiento.csv`: qubits, CX, profundidad, total y permutación.
- `validacion.csv`: número de casos y probabilidad mínima por tamaño/diseño.
- `metricas.json`: resultados completos, configuración, versiones, errores de operadores,
  muestras y hash SHA-256 del código que los generó.
- `resultados.tex`: macros y filas de tablas usadas directamente en el artículo.
- Diagramas PNG, gráficos de recursos y superposición, y `circuitos.txt`.
- `semisumador_qft.qasm`: OpenQASM 3 con mediciones; entradas iniciales `000`.
  Para probar otras entradas, prepara `q[0]` y `q[2]` con X antes del sumador.

Las tablas de verdad son el conjunto de datos del experimento; se generan
exhaustivamente en el código, sin fuentes externas de datos.

## Compilar el informe e importar en Overleaf

El PDF tiene **7 páginas**. Para compilar localmente se necesitan `latexmk`,
pdfLaTeX, BibTeX y los paquetes usuales de TeX Live (`newtx`, `babel-spanish`,
`listings`, `IEEEtran`, entre otros):

```bash
make informe
make overleaf
```

`make all` ejecuta pruebas, regenera el experimento, compila el artículo y las
diapositivas, y crea el ZIP de Overleaf del artículo.
Los resultados existentes permiten compilar el artículo sin ejecutar Python.
En Overleaf: **New Project → Upload Project → avance_overleaf.zip**. Selecciona
`main.tex` como documento principal y **pdfLaTeX** como compilador.

## Diapositivas de la exposición

La carpeta [`ppt/`](ppt/) contiene la presentación completa en PDF, con formato
panorámico 16:9: **25 diapositivas en total, incluidas las referencias** para una exposición
de aproximadamente 20 minutos. Incluye fundamentos, los cuatro artículos,
metodología, circuitos, código Qiskit, validación, recursos, limitaciones y conclusiones.

```bash
make presentacion
```

También se puede usar `make ppt`. El resultado es `ppt/diapositivas.pdf`.
La fuente `ppt/diapositivas.tex` lee las tablas y figuras existentes en
`informe/latex/resultados/`, por lo que las cifras se mantienen vinculadas al
experimento. Los recursos existentes permiten compilar sin volver a simular.
Para actualizar todo: `make experimento` y después `make informe presentacion`.
Se requiere TeX Live con Beamer, TikZ y listings.

## Fuentes verificadas

La bibliografía incluye **16 referencias**: los cuatro artículos de la primera
entrega, ocho fuentes académicas de fundamentos y síntesis y cuatro referencias
oficiales de Qiskit. El informe y las diapositivas comparten la base BibTeX.
La [revisión de cada fuente](informe/revision_bibliografica.md) explica su aporte,
las verificaciones realizadas y los límites de su aplicación al proyecto. Se corrigió la paginación del artículo de Clarino et al.
a **320–329**, conforme a su [publicación oficial](https://www.jstage.jst.go.jp/article/transinf/E108.D/4/E108.D_2024EDP7194/_article).

API utilizadas:

- [QFTGate](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.QFTGate).
- [Statevector](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Statevector).
- [Transpile](https://quantum.cloud.ibm.com/docs/en/api/qiskit/compiler).
- [Operator y sus permutaciones](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Operator).

El modelo visual se toma del artículo de gestión de riesgos entregado como
referencia. El encabezado y los autores corresponden a este proyecto académico.
