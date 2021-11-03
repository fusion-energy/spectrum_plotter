import openmc
from spectrum_plotter import plot_spectrum_from_tally

# loads up the statepoint file with simulation results
statepoint = openmc.StatePoint("statepoint.2.h5")

# gets the first tally using its name
my_tally = statepoint.get_tally(name="neutron_spectra")

# matplotlib style is the default
test_plot = plot_spectrum_from_tally(
    spectrum={"neutron spectra": my_tally},
    x_label="Energy [MeV]",
    y_label="Flux [n/cm^2s]",
    x_scale="linear",
    y_scale="linear",
    title="example plot 1",
    filename="example_spectra_from_tally_matplotlib.png",
)

test_plot.show()

# plotly style
test_plot = plot_spectrum_from_tally(
    spectrum={"neutron spectra": my_tally},
    x_label="Energy [MeV]",
    y_label="Flux [n/cm^2s]",
    x_scale="linear",
    y_scale="linear",
    title="example plot 1",
    plotting_package="plotly",
    filename="example_spectra_from_tally_plotly.html",
    required_units="meters / simulated_particle",
)

test_plot.show()
