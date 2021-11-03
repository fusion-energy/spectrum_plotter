import openmc
from spectrum_plotter import plot_spectrum_from_tally

# loads up the statepoint file with simulation results
statepoint = openmc.StatePoint("statepoint.2.h5")

# gets the first tally using its name
my_tally = statepoint.get_tally(name="neutron_spectra")

# gets the first tally using its name
my_tally_1 = statepoint.get_tally(name="neutron_spectra")
my_tally_2 = statepoint.get_tally(name="photon_spectra")

# matplotlib style is the default
test_plot = plot_spectrum_from_tally(
    spectrum={"neutron spectra": my_tally_1, "photon spectra": my_tally_2},
    x_label="Energy [MeV]",
    y_label="Flux [n/cm^2s]",
    x_scale="linear",
    y_scale="linear",
    title="example plot 1",
    legend=True,
    filename="example_spectra_from_tally_plotly.png",
)

test_plot.show()
