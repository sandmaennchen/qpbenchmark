#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Stéphane Caron
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Validate primal-dual solutions to a quadratic program.
"""

import numpy as np
from numpy import linalg


def is_valid_primal_solution(problem, x, eps_abs: float) -> bool:
    """
    Validate optimality condition of a given primal solution.

    Args:
        x: Primal solution.
        eps_abs: Absolute tolerance.

    Returns:
        True if and only if (x, y) is a valid primal-dual solution.

    Note:
        This function is adapted from `is_qp_solution_optimal` in
        proxqp_benchmark. The original function included the relative
        tolerance parameter specified in the OSQP paper, set to zero.
    """
    C, l, u = problem.constraints_as_double_sided_ineq()
    C_x = C.dot(x)
    primal_residual = np.minimum(C_x - l, 0.0) + np.maximum(C_x - u, 0.0)
    primal_error = linalg.norm(primal_residual, np.inf)
    if primal_error > eps_abs:
        print(f"Error in primal residual: {primal_error} > {eps_abs}")
        return False
    return True


def is_valid_dual_solution(problem, y, x, eps_abs: float) -> bool:
    """
    Validate optimality condition of a given primal solution.

    Args:
        x: Primal solution.
        y: Dual solution.
        eps_abs: Absolute tolerance.

    Returns:
        True if and only if (x, y) is a valid primal-dual solution.

    Note:
        This function is adapted from `is_qp_solution_optimal` in
        proxqp_benchmark. The original function included the relative
        tolerance parameter specified in the OSQP paper, set to zero.
    """
    P, q = problem.P, problem.q
    C, _, _ = problem.constraints_as_double_sided_ineq()
    dual_residual = P.dot(x) + q + C.T.dot(y)
    dual_error = linalg.norm(dual_residual, np.inf)
    if dual_error > eps_abs:
        print(f"Error in dual residual: {dual_error} > {eps_abs}")
        return False
    return True
