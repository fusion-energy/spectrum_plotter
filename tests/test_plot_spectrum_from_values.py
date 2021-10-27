import unittest
from spectrum_plotter import plot_spectrum_from_values
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

        self.spectrum = {'test plot_1': (x1, y1)}
        self.spectrum_with_error = {'test plot_1': (x1, y1, y_err1)}

        self.spectrum_2 = {"test plot_1": (x1, y1), "test plot 2": (x2, y2)}
        self.spectrum_2_with_error = {
            "test plot 1": (x1, y1, y_err1),
            "test plot 2": (x2, y2, y_err2),
        }

    def test_plot_single_spectrum_from_values(self):

        test_plot = plot_spectrum_from_values(spectrum=self.spectrum)

        assert isinstance(test_plot, type(matplotlib.pyplot))

    def test_plot_single_spectrum_from_values_with_error(self):

        test_plot = plot_spectrum_from_values(spectrum=self.spectrum_with_error)

        assert isinstance(test_plot, type(matplotlib.pyplot))

    def test_plot_spectrum_from_values(self):

        test_plot = plot_spectrum_from_values(spectrum=self.spectrum_2)

        assert isinstance(test_plot, type(matplotlib.pyplot))

    def test_plot_spectrum_from_values_with_error(self):

        test_plot = plot_spectrum_from_values(spectrum=self.spectrum_2_with_error)

        assert isinstance(test_plot, type(matplotlib.pyplot))
