import unittest
from spectrum_plotter.core import plot_spectrum
import numpy as np
import matplotlib.pyplot as plt
import matplotlib


class TestPlotSpectrum(unittest.TestCase):
    def setUp(self):

        x = np.array([1, 2, 3, 4, 5, 6])
        y = np.array([0, 1, 1, 0.5, 0.4, 3])
        y_err = np.array([0.2, 0.1, 0.4, 0.1, 0.1, 0.2])
        self.spectrum = {'test plot': (x, y)}
        self.spectrum_with_error = {'test plot': (x, y, y_err)}
    
    def test_plot_spectrum(self):

        test_plot = plot_spectrum(
            spectrum=self.spectrum
        )

        assert isinstance(test_plot, type(matplotlib.pyplot))
