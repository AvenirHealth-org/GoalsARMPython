import goals_proj as GoalsProj
import numpy as np
import pytest


def test_init_pasfrs_from_5yr():
    dtype = np.float64
    order = "C"
    year_first = 1970
    year_final = 1971
    proj = GoalsProj.Projection(year_first, year_final)

    pasfrs5y = 0.01 * np.array([[12.02, 21.08, 20.45, 17.70, 14.93, 9.99, 3.83],
                                [12.05, 21.10, 20.38, 17.65, 14.96, 10.03, 3.83]], dtype=dtype, order=order)

    try:
        proj.init_pasfrs_from_5yr(pasfrs5y)
    except RuntimeError:
        pytest.fail("Unexpected runtime error during init_pasfrs_from_5yr(births)")
