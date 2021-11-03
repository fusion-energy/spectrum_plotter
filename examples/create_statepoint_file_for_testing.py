# This minimal example makes a 3D volume and exports the shape to a stp file
# A surrounding volume called a graveyard is needed for neutronics simulations

import openmc
import openmc_dagmc_wrapper as odw
import openmc_plasma_source as ops
import openmc_data_downloader as odd
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-b", "--batches", type=int, default=2, help="number of batches")
parser.add_argument(
    "-p", "--particles", type=int, default=1000000, help="number of particles"
)
args = parser.parse_args()

# MATERIALS
breeder_material = openmc.Material(1, "PbLi")  # Pb84.2Li15.8
breeder_material.add_element("Pb", 84.2, percent_type="ao")
breeder_material.add_element(
    "Li",
    15.8,
    percent_type="ao",
    enrichment=50.0,
    enrichment_target="Li6",
    enrichment_type="ao",
)  # 50% enriched
breeder_material.set_density("atom/b-cm", 3.2720171e-2)  # around 11 g/cm3

iron = openmc.Material(name="iron")
iron.set_density("g/cm3", 7.75)
iron.add_element("Pb", 0.95, percent_type="wo")

materials = openmc.Materials([breeder_material, iron])

odd.just_in_time_library_generator(libraries="TENDL-2019", materials=materials)

# GEOMETRY

# surfaces
vessel_inner = openmc.Sphere(r=500)
first_wall_outer_surface = openmc.Sphere(r=510)
breeder_blanket_outer_surface = openmc.Sphere(r=610, boundary_type="vacuum")


# cells
inner_vessel_region = -vessel_inner
inner_vessel_cell = openmc.Cell(region=inner_vessel_region)

first_wall_region = -first_wall_outer_surface & +vessel_inner
first_wall_cell = openmc.Cell(region=first_wall_region)
first_wall_cell.fill = iron

breeder_blanket_region = +first_wall_outer_surface & -breeder_blanket_outer_surface
breeder_blanket_cell = openmc.Cell(region=breeder_blanket_region)
breeder_blanket_cell.fill = breeder_material

universe = openmc.Universe(
    cells=[inner_vessel_cell, first_wall_cell, breeder_blanket_cell]
)
geometry = openmc.Geometry(universe)

tally1 = odw.CellTally(
    tally_type="neutron_spectra",
    target=2,
)

tally2 = odw.CellTally(
    tally_type="neutron_spectra",
    target=2,
)

tally3 = odw.CellTally(
    tally_type="neutron_spectra",
    target=3,
)

tally4 = odw.CellTally(
    tally_type="photon_spectra",
    target=2,
)


tallies = openmc.Tallies(
    [
        tally1,
        tally2,
        tally3,
        tally4,
    ]
)


settings = odw.FusionSettings()
settings.batches = args.batches
settings.particles = args.particles
# assigns a ring source of DT energy neutrons to the source using the
# openmc_plasma_source package
settings.source = ops.FusionPointSource()


my_model = openmc.model.Model(
    materials=materials, geometry=geometry, settings=settings, tallies=tallies
)
statepoint_file = my_model.run()
