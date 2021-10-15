import unittest
from spectrum_plotter import plot_spectrum
import numpy as np
import matplotlib


class TestPlotSpectrum(unittest.TestCase):
    def setUp(self):

        x1 = np.array([1, 2, 3, 4, 5, 6])
        y1 = np.array([0, 1, 1, 0.5, 0.4, 3])
        y_err1 = np.array([0.2, 0.1, 0.4, 0.1, 0.1, 0.2])
        x2 = np.array([1, 2, 3, 4, 5, 6])
        y2 = np.array([0, 1, 1, 0.5, 0.4, 3])
        y_err2 = np.array([0.2, 0.1, 0.4, 0.1, 0.1, 0.2])
        self.spectrum = {"test plot_1": (x1, y1), "test plot 2": (x2, y2)}
        self.spectrum_with_error = {
            "test plot 1": (x1, y1, y_err1),
            "test plot 2": (x2, y2, y_err2),
        }

    def test_plot_spectrum(self):

        test_plot = plot_spectrum(spectrum=self.spectrum)

        assert isinstance(test_plot, type(matplotlib.pyplot))

    def test_plot_spectrum_with_error(self):

        test_plot = plot_spectrum(spectrum=self.spectrum_with_error)

        assert isinstance(test_plot, type(matplotlib.pyplot))
