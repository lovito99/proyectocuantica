# Revisión bibliográfica y coherencia del proyecto

Fecha: 12 de noviembre de 2026. Se encontraron 10 entradas en la base original;
se añadieron seis fuentes pertinentes para completar 16: 12 académicas y cuatro
referencias de API. No son 16 artículos experimentales. La primera entrega PDF
contenía cuatro antecedentes, que se conservaron. Esta revisión es dirigida.

Se contrastaron metadatos y aportes con publicaciones, preprints de autores y
documentación oficial. No equivale a reproducir todos los experimentos ni a leer
íntegramente el libro de Nielsen y Chuang. Cuando la página editorial no fue
accesible se indica la alternativa consultada. Las claves son estables; la
numeración IEEE depende del orden de cita de cada documento.

| Clave | Fuente contrastada | Aporte y correspondencia con el proyecto |
| --- | --- | --- |
| `kaltehei2026` | [Wiley, DOI 10.1155/que2/9882453](https://onlinelibrary.wiley.com/doi/10.1155/que2/9882453), 2026, art. 9882453 | Arquitectura de semisumador QFT, X/SWAP y contador de población. El código adopta la arquitectura y calcula métricas propias. Los resultados físicos del artículo no son resultados del proyecto. |
| `escanez2026` | [Oxford, 34(1), jzaf019](https://academic.oup.com/jigpal/article/34/1/jzaf019/8443240), 2026 | QuantumSolver Composer y composición de lógica y cifradores. Fundamenta la organización modular; no se implementan sus cifradores ni reset. |
| `clarino2025` | [Texto editorial J-STAGE](https://www.jstage.jst.go.jp/article/transinf/E108.D/4/E108.D_2024EDP7194/_article), E108-D(4), 320–329 | Shannon/Davio y reducción T en pares de cómputo/descomputación. Motiva revisar fases; no se ejecuta su síntesis LUT ni se reporta reducción T propia. La paginación 320–327 de la primera entrega ya estaba corregida en el LaTeX actual. |
| `hajjdiab2024` | [Preprint de los autores](https://arxiv.org/abs/2303.00075); edición Physica Scripta 99(8), 085127, DOI 10.1088/1402-4896/ad5c17 | Q-Map es una técnica visual de realización booleana. Se usa como antecedente; no está implementada. El preprint es de 2023 y la edición citada de 2024; el DOI editorial no se pudo abrir con el navegador de consulta. |
| `nielsen2010` | [Ficha de Cambridge, edición del décimo aniversario](https://www.cambridge.org/highereducation/books/quantum-computation-and-quantum-information/01E10196D0A682A6AEFFEA52D53BE9AE) | Estados, medición, tensor y unitariedad. Se comprobaron los datos de edición; no se realizó lectura íntegra del libro. |
| `draper2000` | [Preprint original](https://arxiv.org/abs/quant-ph/0008033), 2000 | Suma mediante QFT y fases controladas; respalda la ecuación de suma modular. |
| `qftdocs` | [IBM QFTGate](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.QFTGate) | Definición y API de QFT usada por `half_adder` y `population_count`. |
| `statedocs` | [IBM Statevector](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Statevector) | Simulación ideal de entradas y muestreo; no modela ruido físico por sí sola. |
| `compiledocs` | [IBM compiler/transpile](https://quantum.cloud.ibm.com/docs/en/api/qiskit/compiler) | Base, semilla, optimización y `qubits_initially_zero`; corresponde a `_resources`. |
| `operatordocs` | [IBM Operator](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Operator) | Matrices y consideración del layout con `from_circuit`; respalda la comparación de operadores compilados. |
| `bennett1973` | [Artículo original digitalizado](https://worrydream.com/refs/Bennett_1973_-_Logical_Reversibility_of_Computation.pdf), IBM J. Res. Dev. 17(6), 525–532 | Cómputo reversible y eliminación de historia. Fundamenta la discusión de registros residuales; su limpieza queda pendiente. Copiar bits de la base con CNOT no permite clonar estados arbitrarios. |
| `barenco1995` | [Preprint original](https://arxiv.org/abs/quant-ph/9503016), Phys. Rev. A 52, 3457–3467 | Universalidad de puertas de un qubit y CNOT, controles múltiples. Respalda la base común; no prueba que nuestra compilación sea mínima. |
| `cuccaro2004` | [Preprint original](https://arxiv.org/abs/quant-ph/0410184), 2004 | Sumador ripple-carry lineal con un auxiliar. Delimita la comparación: una escalera AND no representa todos los diseños Toffoli. No se implementa este sumador. |
| `maslov2016` | [Preprint y referencia editorial](https://arxiv.org/abs/1508.03273), Phys. Rev. A 93, 022311 | Identidades de fase relativa bajo condiciones concretas. Respalda la precaución con fases; se mantienen Toffoli exactas. Preprint de 2015, edición de 2016. |
| `shende2006` | [Versión de autores](https://arxiv.org/abs/quant-ph/0406176) y [registro NIST](https://www.nist.gov/publications/synthesis-quantum-logic-circuits) | Síntesis de unitarias, costo CNOT y conectividad. Fundamenta las métricas, no se implementa su algoritmo. Preprint de 2004 revisado en 2006. |
| `coppersmith2002` | [Preprint original e identificación del informe](https://arxiv.org/abs/quant-ph/0201067) | QFT aproximada: informe IBM RC 19642 de 1994 depositado en 2002. Solo fundamenta trabajo futuro; no se atribuyen sus garantías de factorización a la suma de este proyecto. |

## Correcciones de coherencia

- El informe cita las 16 entradas en pasajes que explican su función.
- Las diapositivas leen la misma base BibTeX que el informe, evitando listas divergentes.
- Se añadió una explicación de las seis fuentes complementarias en ambos documentos.
- Se precisó que QFT reduce el ancho frente a la escalera considerada para N ≥ 4; con dos entradas ambos usan tres qubits.
- Se cambió «validación experimental» por «validación ideal» en la presentación para describir con precisión la ejecución en CPU.
- Se conservan los límites: 16 entradas solo compiladas; validación exhaustiva hasta ocho; sin ruido, QPU, Q-Map, síntesis LUT ni descomputación implementada.
- Las API son documentos vivos: 2026 se usa como año de consulta, no como fecha de publicación demostrada. La consulta se actualizó al 12 de noviembre.

El código existente concuerda con la arquitectura descrita: QFT exacta, fases
controladas, Toffoli/CNOT, salida lógica identificada, contador y escalera sin
limpieza. No se modificaron algoritmos ni cifras generadas para ajustarlos a
resultados ajenos. Las extensiones de las fuentes permanecen explícitamente
como antecedentes o trabajo futuro.
