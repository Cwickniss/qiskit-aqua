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

from qiskit.aqua.components.optimizers import Optimizer
from ._nloptimizer import minimize
from ._nloptimizer import check_pluggable_valid as check_nlopt_valid
import logging

logger = logging.getLogger(__name__)

try:
    import nlopt
except ImportError:
    logger.info('nlopt is not installed. Please install it if you want to use them.')


class DIRECT_L(Optimizer):
    """DIRECT is the DIviding RECTangles algorithm for global optimization.

    DIRECT-L is the "locally biased" variant
    NLopt global optimizer, derivative-free
    http://nlopt.readthedocs.io/en/latest/NLopt_Algorithms/#direct-and-direct-l
    """

    CONFIGURATION = {
        'name': 'DIRECT_L',
        'description': 'GN_DIRECT_L Optimizer',
        'input_schema': {
            '$schema': 'http://json-schema.org/schema#',
            'id': 'direct_l_schema',
            'type': 'object',
            'properties': {
                'max_evals': {
                    'type': 'integer',
                    'default': 1000
                }
            },
            'additionalProperties': False
        },
        'support_level': {
            'gradient': Optimizer.SupportLevel.ignored,
            'bounds': Optimizer.SupportLevel.supported,
            'initial_point': Optimizer.SupportLevel.required
        },
        'options': ['max_evals'],
        'optimizer': ['global']
    }

    def __init__(self, max_evals=1000):
        """
        Constructor.

        Args:
            max_evals (int): Maximum allowed number of function evaluations.
        """
        self.validate(locals())
        super().__init__()
        for k, v in locals().items():
            if k in self._configuration['options']:
                self._options[k] = v

    @staticmethod
    def check_pluggable_valid():
        check_nlopt_valid(DIRECT_L.CONFIGURATION['name'])

    def optimize(self, num_vars, objective_function, gradient_function=None,
                 variable_bounds=None, initial_point=None):
        super().optimize(num_vars, objective_function, gradient_function, variable_bounds, initial_point)

        return minimize(nlopt.GN_DIRECT_L, objective_function, variable_bounds, initial_point, **self._options)
