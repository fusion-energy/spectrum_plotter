from spectrum_plotter import plot_spectrum_from_values
import numpy as np

x = np.array([1, 2, 3, 4, 5, 6])
y = np.array([0, 1, 1, 0.5, 0.4, 3])
y_err = np.array([0.2, 0.1, 0.4, 0.1, 0.1, 0.2])

# matplotlib style is the default
test_plot = plot_spectrum_from_values(
    spectrum={'my spectra': (x, y, y_err)},
    x_label="Energy [MeV]",
    y_label="Flux [n/cm^2s]",
    x_scale="linear",
    y_scale="linear",
    title="example plot 1",
    filename="example_spectra_matplotlib.png",
)

test_plot.show()
