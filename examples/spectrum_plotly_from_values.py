from spectrum_plotter import plot_spectrum_from_values
import numpy as np

x1 = np.array([1, 2, 3, 4, 5, 6])
y1 = np.array([0, 1, 1, 0.5, 0.4, 3])
y_err1 = np.array([0.2, 0.1, 0.4, 0.1, 0.1, 0.2])

x2 = np.array([1, 2, 3, 4, 5, 6])
y2 = np.array([3, 4, 3, 5, 3.8, 4.1])
y_err2 = np.array([0.2, 0.1, 0.4, 0.2, 0.1, 0.2])

spectrum_with_error = {
    "test plot 1": (x1, y1, y_err1),
    "test plot 2": (x2, y2, y_err2),
}

test_plot = plot_spectrum_from_values(
    spectrum=spectrum_with_error,
    x_label="Energy [MeV]",
    y_label="Flux [n/cm^2s]",
    x_scale="linear",
    y_scale="linear",
    title="example plot 1",
    plotting_package="plotly",
    # filename='example_spectra_plotly.png'  # static png image export requires kaleido package
    filename="example_spectrum_plotly.html",
)

test_plot.show()
