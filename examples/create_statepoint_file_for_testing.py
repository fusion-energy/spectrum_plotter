# This minimal example makes a 3D volume and exports the shape to a stp file
# A surrounding volume called a graveyard is needed for neutronics simulations

import openmc
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

odd.just_in_time_library_generator(
    libraries=["ENDFB-7.1-NNDC", "TENDL-2019"], materials=materials
)

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

cell_filter = openmc.CellFilter(first_wall_cell)
energy_bins = openmc.mgxs.GROUP_STRUCTURES["CCFE-709"]
energy_filter = openmc.EnergyFilter(energy_bins)
photon_particle_filter = openmc.ParticleFilter(["photon"])
neutron_particle_filter = openmc.ParticleFilter(["neutron"])

tally1 = openmc.Tally(1, "neutron_spectra")
tally1.scores = ["flux"]
tally1.filters.append(cell_filter)
tally1.filters.append(energy_filter)
tally1.filters.append(neutron_particle_filter)

tally2 = openmc.Tally(2, "photon_spectra")
tally2.scores = ["flux"]
tally2.filters.append(cell_filter)
tally2.filters.append(energy_filter)
tally2.filters.append(photon_particle_filter)

tallies = openmc.Tallies(
    [
        tally1,
        tally2,
    ]
)

settings = openmc.Settings()
settings.inactive = 0
settings.run_mode = "fixed source"
settings.batches = args.batches
settings.particles = args.particles
settings.photon_transport = True
# assigns a ring source of DT energy neutrons to the source using the
# openmc_plasma_source package

source = openmc.Source()
source.space = openmc.stats.Point((0, 0, 0))
source.angle = openmc.stats.Isotropic()
settings.source = source

my_model = openmc.model.Model(
    materials=materials, geometry=geometry, settings=settings, tallies=tallies
)
statepoint_file = my_model.run()
