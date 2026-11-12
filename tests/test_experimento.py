"""Validación independiente de tablas, fases y circuitos reversibles."""

import json
from itertools import product

import numpy as np
import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Statevector

from proyecto.experimento import (
    and_ladder,
    half_adder,
    logic_gate,
    population_count,
    run_experiment,
)


def test_fourier_adder_adds_modulo_four_without_relative_phases():
    expected = np.zeros((8, 8), dtype=complex)
    for accumulator, control in product(range(4), range(2)):
        expected[(accumulator + control) % 4 + 4 * control,
                 accumulator + 4 * control] = 1
    for method in ("QFT", "Toffoli"):
        np.testing.assert_allclose(Operator(half_adder(method)).data, expected,
                                   atol=1e-12)


@pytest.mark.parametrize("gate", ["AND", "NAND", "OR", "NOR", "XOR"])
def test_both_families_implement_truth_table_and_same_full_unitary(gate):
    functions = {
        "AND": lambda a, b: a & b,
        "NAND": lambda a, b: 1 - (a & b),
        "OR": lambda a, b: a | b,
        "NOR": lambda a, b: 1 - (a | b),
        "XOR": lambda a, b: a ^ b,
    }
    direct = Operator(logic_gate(gate, "Toffoli")).data
    fourier = Operator(logic_gate(gate, "QFT")).data
    np.testing.assert_allclose(fourier, direct, atol=1e-12)
    np.testing.assert_allclose(fourier.conj().T @ fourier, np.eye(8), atol=1e-12)
    for a, b in product(range(2), repeat=2):
        probabilities = np.abs(fourier[:, a + 4 * b]) ** 2
        success = sum(p for k, p in enumerate(probabilities)
                      if (k >> 1) & 1 == functions[gate](a, b))
        assert success == pytest.approx(1)


def test_popcount_and_ladder_match_independent_integer_arithmetic():
    for n in (2, 4):
        popcount, accumulator = population_count(n)
        ladder = and_ladder(n)
        for value in range(2**n):
            initial = QuantumCircuit(popcount.num_qubits)
            for bit in range(n):
                if (value >> bit) & 1:
                    initial.x(bit)
            state = Statevector.from_instruction(initial.compose(popcount))
            output = int(np.argmax(state.probabilities()))
            count = sum(((output >> qubit) & 1) << j
                        for j, qubit in enumerate(accumulator))
            assert count == value.bit_count()
            assert state.probabilities()[output] == pytest.approx(1)
            initial_ladder = QuantumCircuit(ladder.num_qubits)
            for bit in range(n):
                if (value >> bit) & 1:
                    initial_ladder.x(bit)
            state_ladder = Statevector.from_instruction(initial_ladder.compose(ladder))
            output_ladder = int(np.argmax(state_ladder.probabilities()))
            assert (output_ladder >> (2 * n - 2)) & 1 == int(value == 2**n - 1)


@pytest.mark.parametrize("n", [0, 1, 3, -2])
def test_scaling_requires_power_of_two_inputs(n):
    with pytest.raises(ValueError, match="potencia de dos"):
        population_count(n)
    with pytest.raises(ValueError, match="potencia de dos"):
        and_ladder(n)


def test_experiment_exports_real_metrics_and_latex(tmp_path):
    report = run_experiment(tmp_path, validation_sizes=(2, 4))
    assert json.loads((tmp_path / "metricas.json").read_text()) == report
    assert report["config"]["backend"] == "Statevector (simulación ideal en CPU)"
    assert len(report["truth_tables"]) == 40
    assert all(row["probability"] > 1 - 1e-12 for row in report["truth_tables"])
    assert all(row["max_error"] < 1e-12 for row in report["unitaries"])
    assert all(row["compiled_error"] < 1e-12 for row in report["unitaries"])
    assert len(report["scaling"]) == 8
    assert sum(row["cases"] for row in report["validation"]) == 40
    assert sum(report["superposition_counts"].values()) == 4096
    assert (tmp_path / "resultados.tex").is_file()
    assert (tmp_path / "comparacion_recursos.png").is_file()
    assert (tmp_path / "semisumador_qft.png").is_file()
