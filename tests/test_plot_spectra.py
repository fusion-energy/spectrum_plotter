import unittest
from spectrum_plotter.core import plot_spectra
import numpy as np
import matplotlib


class TestPlotSpectra(unittest.TestCase):
    def setUp(self):

        x = np.array([1, 2, 3, 4, 5, 6])
        y = np.array([0, 1, 1, 0.5, 0.4, 3])
        y_err = np.array([0.2, 0.1, 0.4, 0.1, 0.1, 0.2])
        self.spectra = (x, y)
        self.spectra_with_error = (x, y, y_err)

    def test_plot_spectra(self):

        test_plot = plot_spectra(
            spectra=self.spectra
        )

        assert isinstance(test_plot, type(matplotlib.pyplot))
