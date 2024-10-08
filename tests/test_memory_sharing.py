import goals_proj as GoalsProj
import numpy as np
import pytest

import goals.goals_const as CONST


class TestMemorySharing:
    dtype = np.float64
    order = "C"
    year_first = 1970
    year_final = 2030
    num_years = year_final - year_first + 1
    proj = GoalsProj.Projection(year_first, year_final)

    def test_births(self):
        births = np.zeros((self.num_years, CONST.N_SEX), dtype=self.dtype, order=self.order)
        try:
            self.proj.share_output_births(births)
        except RuntimeError:
            pytest.fail("Unexpected runtime error during share_output_births(births)")

    def test_births_ndim(self):
        births = np.zeros(self.num_years, dtype=self.dtype, order=self.order)
        with pytest.raises(RuntimeError):
            self.proj.share_output_births(births)


    def test_births_shape(self):
        births = np.zeros((CONST.N_SEX, self.num_years), dtype=self.dtype, order=self.order)
        with pytest.raises(RuntimeError):
            self.proj.share_output_births(births)


    def test_births_layout(self):
        births = np.zeros((self.num_years, CONST.N_SEX), dtype=self.dtype, order="F")
        with pytest.raises(RuntimeError):
            self.proj.share_output_births(births)
