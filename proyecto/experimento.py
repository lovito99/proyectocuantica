"""Circuitos reversibles: validación ideal y comparación de recursos en Qiskit.

Ejecutar desde la raíz: python -m proyecto.experimento
Convención: q[0]=a, q[1]=auxiliar, q[2]=b; cadenas de Qiskit: q[2]q[1]q[0].
API: https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.QFTGate
"""

import argparse
import csv
import hashlib
import json
import platform
from importlib.metadata import version
from itertools import product
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit, qasm3, transpile
from qiskit.circuit.library import QFTGate
from qiskit.quantum_info import Operator, Statevector

GATES = ("AND", "NAND", "OR", "NOR", "XOR")
METHODS = ("Toffoli", "QFT")
DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / "informe/latex/resultados"
SEED = 42


def half_adder(method="QFT"):
    """|t>|b> -> |t+b mod 4>|b>, con t=q[0]+2*q[1].

    Con q[1]=0, q[0] contiene a XOR b y q[1] contiene a AND b.
    El circuito es unitario también cuando el auxiliar inicia en uno.
    """
    circuit = QuantumCircuit(3, name=f"Sumador_{method}")
    if method == "QFT":
        circuit.append(QFTGate(2), [0, 1])
        circuit.cp(np.pi / 2, 2, 0)
        circuit.cp(np.pi, 2, 1)
        circuit.append(QFTGate(2).inverse(), [0, 1])
    elif method == "Toffoli":
        circuit.ccx(0, 2, 1)
        circuit.cx(2, 0)
    else:
        raise ValueError(f"Método desconocido: {method}")
    return circuit


def logic_gate(gate, method="QFT"):
    """Familia de plantilla común; la salida lógica siempre está en q[1].

    Las otras líneas contienen información residual reversible. No se exige
    que ambas entradas originales se conserven en sus posiciones iniciales.
    """
    if gate not in GATES:
        raise ValueError(f"Compuerta desconocida: {gate}")
    circuit = QuantumCircuit(3, name=f"{gate}_{method}")
    if gate in ("OR", "NOR"):
        circuit.x(0)
        circuit.x(2)
    circuit.compose(half_adder(method), inplace=True)
    if gate in ("NAND", "OR"):
        circuit.x(1)
    if gate == "XOR":
        circuit.swap(0, 1)
    return circuit


def _validate_size(n):
    if not isinstance(n, int) or n < 2 or n & (n - 1):
        raise ValueError("N debe ser una potencia de dos mayor o igual que 2")


def population_count(n):
    """Cuenta N=2**k entradas, reutilizando la primera en el acumulador.

    Utiliza N+k qubits: N entradas, k auxiliares. El acumulador tiene k+1 bits.
    Devuelve sus índices de menor a mayor peso. No conserva la primera entrada.
    """
    _validate_size(n)
    k = n.bit_length() - 1
    accumulator = [0] + list(range(n, n + k))
    circuit = QuantumCircuit(n + k, name=f"Popcount_QFT_{n}")
    circuit.append(QFTGate(k + 1), accumulator)
    for control in range(1, n):
        for j, target in enumerate(accumulator):
            circuit.cp(2 * np.pi / 2 ** (k + 1 - j), control, target)
    circuit.append(QFTGate(k + 1).inverse(), accumulator)
    return circuit, accumulator


def and_ladder(n):
    """AND mediante N-1 Toffoli y N-1 auxiliares; salida en q[2*N-2].

    Conserva entradas y productos intermedios. No descomputa los auxiliares.
    """
    _validate_size(n)
    circuit = QuantumCircuit(2 * n - 1, name=f"AND_escalera_{n}")
    circuit.ccx(0, 1, n)
    for i in range(2, n):
        circuit.ccx(n + i - 2, i, n + i - 1)
    return circuit


def _basis_output(circuit, value, input_qubits):
    initial = QuantumCircuit(circuit.num_qubits)
    for bit, qubit in enumerate(input_qubits):
        if (value >> bit) & 1:
            initial.x(qubit)
    probabilities = Statevector.from_instruction(initial.compose(circuit)).probabilities()
    output = int(np.argmax(probabilities))
    return output, float(probabilities[output])


def _resources(circuit):
    # Base y conectividad comunes; no modela un dispositivo físico concreto.
    compiled = transpile(circuit, basis_gates=["u", "cx"], optimization_level=3,
                         seed_transpiler=SEED, qubits_initially_zero=False)
    return {"qubits": compiled.num_qubits, "cx": int(compiled.count_ops().get("cx", 0)),
            "depth": compiled.depth(), "gates": compiled.size(),
            "output_permutation": (compiled.layout.final_index_layout() if compiled.layout
                                   else list(range(compiled.num_qubits)))}, compiled


def _write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _write_latex(output, report):
    commands = {
        "QiskitVersion": report["config"]["versions"]["qiskit"],
        "ValidationCases": str(sum(r["cases"] for r in report["validation"])),
        "MaxUnitaryError": f'{max(max(r["max_error"], r["compiled_error"]) for r in report["unitaries"]):.2e}',
        "MinTruthProbability": f'{min(r["probability"] for r in report["truth_tables"]):.6f}',
        "TwoInputRows": "\n".join(
            f'{r["gate"]} & {r["method"]} & {r["cx"]} & {r["depth"]} & {r["gates"]} \\\\'
            for r in report["two_input_resources"]),
        "ScalingRows": "\n".join(
            f'{r["n_inputs"]} & {r["method"]} & {r["qubits"]} & {r["cx"]} & {r["depth"]} \\\\'
            for r in report["scaling"]),
        "ValidationRows": "\n".join(
            f'{r["n_inputs"]} & {r["method"]} & {r["cases"]} & {r["min_probability"]:.6f} \\\\'
            for r in report["validation"]),
    }
    text = "% Generado por proyecto/experimento.py; no editar cifras manualmente.\n"
    text += "\n".join(f"\\newcommand{{\\{name}}}{{{value}}}" for name, value in commands.items())
    (output / "resultados.tex").write_text(text + "\n", encoding="utf-8")


def _write_figures(output, report):
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False,
                         "axes.spines.right": False, "savefig.dpi": 220})
    colors = {"QFT": "#8b1e24", "Toffoli": "#246481"}
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.1), layout="constrained")
    for method in METHODS:
        rows = [r for r in report["scaling"] if r["method"] == method]
        for ax, metric, label in zip(axes, ("qubits", "cx", "depth"),
                                     ("Qubits", "Compuertas CX", "Profundidad")):
            ax.plot([r["n_inputs"] for r in rows], [r[metric] for r in rows],
                    "o-", label=method, color=colors[method])
            ax.set(xlabel="Entradas N", ylabel=label, xticks=[2, 4, 8, 16])
            ax.grid(alpha=.18)
    axes[0].legend(frameon=False)
    fig.savefig(output / "comparacion_recursos.png")
    plt.close(fig)

    for method in METHODS:
        figure = half_adder(method).draw(output="mpl", fold=-1, style="bw")
        figure.savefig(output / f"semisumador_{method.lower()}.png", bbox_inches="tight", dpi=220)
        plt.close(figure)
    circuit = half_adder("QFT")
    circuit.measure_all()
    compiled = _resources(circuit)[1]
    (output / "semisumador_qft.qasm").write_text(qasm3.dumps(compiled), encoding="utf-8")
    (output / "circuitos.txt").write_text(
        "\n\n".join(f"{method}\n{half_adder(method).draw(output='text')}" for method in METHODS),
        encoding="utf-8")

    fig, ax = plt.subplots(figsize=(5, 3), layout="constrained")
    labels = ["00", "01", "10"]
    observed = [report["superposition_counts"].get(label, 0) / 4096 for label in labels]
    x = np.arange(3)
    ax.bar(x - .18, [.25, .5, .25], .36, label="Probabilidad exacta", color="#246481")
    ax.bar(x + .18, observed, .36, label="4096 mediciones simuladas", color="#8b1e24")
    ax.set(xticks=x, xticklabels=labels, xlabel="Acumulador |q₁q₀⟩", ylabel="Probabilidad", ylim=(0, .65))
    ax.legend(frameon=False, fontsize=8)
    fig.savefig(output / "superposicion.png")
    plt.close(fig)


def run_experiment(output=DEFAULT_OUTPUT, validation_sizes=(2, 4, 8)):
    """Genera datos, métricas y figuras. N=16 se compila, pero no se simula."""
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    truth_tables, unitaries, two_input, scaling, validation = [], [], [], [], []
    functions = {"AND": lambda a, b: a & b, "NAND": lambda a, b: 1 - (a & b),
                 "OR": lambda a, b: a | b, "NOR": lambda a, b: 1 - (a | b),
                 "XOR": lambda a, b: a ^ b}
    for gate in GATES:
        matrices = [Operator(logic_gate(gate, m)).data for m in METHODS]
        error = float(np.max(np.abs(matrices[0] - matrices[1])))
        inverse_error = float(np.max(np.abs(matrices[1].conj().T @ matrices[1] - np.eye(8))))
        if max(error, inverse_error) > 1e-10:
            raise RuntimeError(f"Falló la equivalencia o reversibilidad de {gate}")
        compiled_error = 0.
        for method in METHODS:
            circuit = logic_gate(gate, method)
            metrics, compiled = _resources(circuit)
            # El layout conserva el significado lógico si se eliminan SWAP finales.
            difference = float(np.max(np.abs(Operator.from_circuit(compiled).data - Operator(circuit).data)))
            compiled_error = max(compiled_error, difference)
            if difference > 1e-10:
                raise RuntimeError(f"La compilación alteró el operador de {gate}, {method}")
            two_input.append({"gate": gate, "method": method, **metrics})
            for a, b in product(range(2), repeat=2):
                observed, probability = _basis_output(circuit, a + 2 * b, [0, 2])
                result = (observed >> 1) & 1
                if result != functions[gate](a, b) or probability < 1 - 1e-10:
                    raise RuntimeError(f"Tabla incorrecta: {gate}, {method}, {a}, {b}")
                truth_tables.append({"gate": gate, "method": method, "a": a, "b": b,
                                     "expected": functions[gate](a, b), "observed": result,
                                     "probability": probability})
        unitaries.append({"gate": gate, "max_error": error, "inverse_error": inverse_error,
                          "compiled_error": compiled_error})

    for n in (2, 4, 8, 16):
        fourier, accumulator = population_count(n)
        for method, circuit in (("QFT", fourier), ("Toffoli", and_ladder(n))):
            scaling.append({"n_inputs": n, "method": method, **_resources(circuit)[0]})
            if n not in validation_sizes:
                continue
            minimum = 1.
            for value in range(2**n):
                observed, probability = _basis_output(circuit, value, range(n))
                if method == "QFT":
                    count = sum(((observed >> q) & 1) << j for j, q in enumerate(accumulator))
                    valid = count == value.bit_count()
                else:
                    valid = ((observed >> (2 * n - 2)) & 1) == int(value == 2**n - 1)
                if not valid or probability < 1 - 1e-10:
                    raise RuntimeError(f"Salida incorrecta: N={n}, {method}, entrada={value}")
                minimum = min(minimum, probability)
            validation.append({"n_inputs": n, "method": method, "cases": 2**n,
                               "min_probability": minimum})

    coherent = QuantumCircuit(3)
    coherent.h(0)
    coherent.h(2)
    coherent.compose(half_adder("QFT"), inplace=True)
    state = Statevector.from_instruction(coherent)
    state.seed(SEED)
    counts = {k: int(v) for k, v in state.sample_counts(4096, qargs=[0, 1]).items()}
    report = {
        "config": {"seed": SEED, "shots_superposition": 4096,
                   "backend": "Statevector (simulación ideal en CPU)",
                   "basis_gates": ["u", "cx"], "optimization_level": 3,
                   "qubits_initially_zero": False,
                   "connectivity": "all-to-all; sin enrutamiento físico",
                   "python": platform.python_version(),
                   "versions": {p: version(p) for p in ("qiskit", "numpy", "matplotlib")},
                   "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
        "truth_tables": truth_tables, "unitaries": unitaries,
        "two_input_resources": two_input, "scaling": scaling,
        "validation": validation, "superposition_counts": counts,
    }
    (output / "metricas.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                                         encoding="utf-8")
    for name, rows in (("tablas_verdad", truth_tables), ("recursos_dos_entradas", two_input),
                       ("escalamiento", scaling), ("validacion", validation)):
        _write_csv(output / f"{name}.csv", rows)
    _write_latex(output, report)
    _write_figures(output, report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT,
                        help="Carpeta para CSV, JSON, figuras y macros LaTeX")
    args = parser.parse_args()
    report = run_experiment(args.output)
    print(f"40 casos de compuertas y {sum(r['cases'] for r in report['validation'])} casos de escalamiento correctos.")
    print(f"Resultados: {args.output.resolve()}")


if __name__ == "__main__":
    main()
