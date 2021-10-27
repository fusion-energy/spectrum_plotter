import openmc
import openmc_dagmc_wrapper as odw
import openmc_plasma_source as ops
import openmc_post_processor as opp
import paramak
from spectrum_plotter import plot_spectrum_from_tally
from stl_to_h5m import stl_to_h5m

# This minimal example makes a 3D volume and exports the shape to a stp file
# A surrounding volume called a graveyard is needed for neutronics simulations

my_shape = paramak.ExtrudeStraightShape(
    points=[(400, 100), (400, 200), (600, 200), (600, 100)],
    distance=180,
)

my_shape.export_stl("steel.stl")

# This script converts the CAD stp files generated into h5m files that can be
# used in DAGMC enabled codes. One of the key aspects of this is the assignment
# of materials to the volumes present in the CAD files.

stl_to_h5m(
    files_with_tags=[
        ("steel.stl", "mat1"),
    ],
    h5m_filename="dagmc.h5m",
)


# makes use of the previously created neutronics geometry (h5m file) and assigns
# actual materials to the material tags. Sets simulation intensity and specifies
# the neutronics results to record (know as tallies).


# defines a simple DT neutron point source
my_source = ops.FusionPointSource(coordinate=(0, 0, 0), temperature=20000.0, fuel="DT")

# set the geometry file to use
geometry = odw.Geometry(
    h5m_filename="dagmc.h5m",
)

# sets the material to use
materials = odw.Materials(
    h5m_filename="dagmc.h5m", correspondence_dict={"mat1": "eurofer"}
)

# creates a cell tally for neutron spectra
tally1 = odw.CellTally(tally_type="neutron_spectra", target="mat1", materials=materials)

tallies = openmc.Tallies([tally1])

settings = odw.FusionSettings()
settings.batches = 2
settings.particles = 50000

# assigns a ring source of DT energy neutrons to the source using the
# openmc_plasma_source package
settings.source = ops.FusionRingSource(fuel="DT", radius=350)


my_model = openmc.Model(
    materials=materials, geometry=geometry, settings=settings, tallies=tallies
)

# starts the simulation
statepoint_file = my_model.run()

# loads up the statepoint file with simulation results
statepoint = openmc.StatePoint(statepoint_file)

# gets the first tally using its name
my_tally = statepoint.get_tally(name="mat1_neutron_spectra")

# matplotlib style is the default
test_plot = plot_spectrum_from_tally(
    spectra=my_tally,
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
    spectra=my_tally,
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
