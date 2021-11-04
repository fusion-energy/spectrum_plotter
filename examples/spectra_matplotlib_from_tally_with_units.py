import openmc
from spectrum_plotter import plot_spectrum_from_tally


# open the simulation results file
results = openmc.StatePoint('statepoint.2.h5')

my_tally = results.get_tally(name='neutron_spectra')

# this is the volume of the cell used in both plots
volume_of_cell_in_cm3 = 10

# in this plot the required_units scale the results to per meter^2
test_plot = plot_spectrum_from_tally(
    spectrum={'neutron spectrum':my_tally},
    required_units="1 / meter ** 2",
    volume = volume_of_cell_in_cm3,
    x_label="Energy [MeV]",
    y_label="Flux [n/m^2s]",
    x_scale="linear",
    y_scale="linear",
    title="example plot with flux in meters",
    filename="flux_in_per_m_2.html",
    plotting_package='plotly',
)

# in this plot the required_units scale the results to per centimeter^2
test_plot = plot_spectrum_from_tally(
    spectrum={'neutron spectrum':my_tally},
    required_units="1 / centimeter ** 2",
    volume = volume_of_cell_in_cm3,
    x_label="Energy [MeV]",
    y_label="Flux [n/cm^2s]",
    x_scale="linear",
    y_scale="linear",
    title="example plot with flux in centimeters",
    filename="flux_in_per_cm_2.html",
    plotting_package='plotly'
)
