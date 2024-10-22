import os
from pathlib import Path

import numpy as np
import pytest

from goals.goals_model import Model

## Unit tests for Goals input initialization from Excel

def test_external_clhiv():
    print(os.getcwd())
    path = Path("inputs") / "test-external-clhiv.xlsx"
    goals = Model()
    goals.init_from_xlsx(path)

    goals.project(2049)

    ## Reference values
    ref_by_year = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 8, 16,
                            31, 50, 76, 118, 176, 268, 381, 549, 762, 1052,
                            1417, 1863, 2392, 2994, 3644, 4328, 4952, 5518, 6003, 6362,
                            6645, 6840, 6958, 7060, 7170, 7199, 7132, 7050, 6930, 6811,
                            6650, 6385, 5806, 5528, 5202, 4348, 4170, 4008, 3655, 3131,
                            2583, 2583, 2583, 2583, 2583, 2583, 2583, 2583, 2583, 2583,
                            2583, 2583, 2583, 2583, 2583, 2583, 2583, 2583, 2583, 2583])
    ref_by_sex = np.array([107550, 105748])
    ref_by_age = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 213298])
    ref_by_cd4 = np.array([19761, 21823, 36314, 46410, 44504, 44486])
    ref_by_art = np.array([0, 0, 94155, 9741, 0, 109402])

    ## Output values
    out_by_year = goals.pop_child_hiv.sum((1, 2, 3, 4))
    out_by_sex = [goals.pop_child_hiv[:, 0, :, :].sum(),
                  goals.pop_child_hiv[:, 1:, :, :].sum()]  # aggregate circumcised and uncircumcised males
    out_by_age = goals.pop_child_hiv.sum((0, 1, 3, 4))
    out_by_cd4 = goals.pop_child_hiv.sum((0, 1, 2, 4))
    out_by_art = goals.pop_child_hiv.sum((0, 1, 2, 3))

    np.testing.assert_allclose(out_by_year[:80], ref_by_year, rtol=1e-10)
    np.testing.assert_allclose(out_by_sex, ref_by_sex, rtol=1e-10)
    np.testing.assert_allclose(out_by_age, ref_by_age, rtol=1e-10)
    np.testing.assert_allclose(out_by_cd4[:6], ref_by_cd4, rtol=1e-10)
    np.testing.assert_allclose(out_by_art, ref_by_art, rtol=1e-10)
