# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM Corp. 2017 and later.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

import unittest
import itertools
import math
from parameterized import parameterized
from qiskit import BasicAer
from qiskit.aqua import QuantumInstance
from qiskit.aqua.components.oracles import TruthTableOracle
from qiskit.aqua.algorithms import BernsteinVazirani
from test.common import QiskitAquaTestCase

bitmaps = ['00111100', '01011010']
mct_modes = ['basic', 'basic-dirty-ancilla', 'advanced', 'noancilla']
optimizations = ['off', 'qm-dlx']


class TestBernsteinVazirani(QiskitAquaTestCase):
    @parameterized.expand(
        itertools.product(bitmaps, mct_modes, optimizations)
    )
    def test_bernstein_vazirani(self, bv_input, mct_mode, optimization='off'):
        nbits = int(math.log(len(bv_input), 2))
        # compute the ground-truth classically
        parameter = ""
        for i in reversed(range(nbits)):
            bit = bv_input[2 ** i]
            parameter += bit

        backend = BasicAer.get_backend('qasm_simulator')
        oracle = TruthTableOracle(bv_input, optimization=optimization, mct_mode=mct_mode)
        algorithm = BernsteinVazirani(oracle)
        quantum_instance = QuantumInstance(backend)
        result = algorithm.run(quantum_instance=quantum_instance)
        # print(result['circuit'].draw(line_length=10000))
        self.assertEqual(result['result'], parameter)


if __name__ == '__main__':
    unittest.main()
