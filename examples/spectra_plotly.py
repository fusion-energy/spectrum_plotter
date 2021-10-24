from spectrum_plotter import plot_spectra
import numpy as np

x = np.array([1, 2, 3, 4, 5, 6])
y = np.array([0, 1, 1, 0.5, 0.4, 3])
y_err = np.array([0.2, 0.1, 0.4, 0.1, 0.1, 0.2])

test_plot = plot_spectra(
    spectra=(x, y, y_err),
    x_label="Energy [MeV]",
    y_label="Flux [n/cm^2s]",
    x_scale="linear",
    y_scale="linear",
    title="example plot 1",
    plotting_package="plotly",
    # filename='example_spectra_plotly.png'  # static image export requires kaleido package
    filename='example_spectra_plotly.html'
)

test_plot.show()
