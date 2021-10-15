from spectrum_plotter import plot_spectrum
import numpy as np

x1 = np.array([1, 2, 3, 4, 5, 6])
y1 = np.array([0, 1, 1, 0.5, 0.4, 3])
y_err1 = np.array([0.2, 0.1, 0.4, 0.1, 0.1, 0.2])
x2 = np.array([1, 2, 3, 4, 5, 6])
y2 = np.array([3, 4, 2, 5, 0.5, 2])
y_err2 = np.array([0.2, 0.1, 0.4, 0.1, 0.1, 0.2])

spectrum_with_error = {
    "test plot 1": (x1, y1, y_err1),
    "test plot 2": (x2, y2, y_err2),
}

test_plot = plot_spectrum(
    spectrum=spectrum_with_error,
    x_label="Energy [MeV]",
    y_label="Flux [n/cm^2s]",
    x_scale="linear",
    y_scale="linear",
    title="example plot 1",
)

test_plot.show()
