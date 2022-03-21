[![N|Python](https://www.python.org/static/community_logos/python-powered-w-100x40.png)](https://www.python.org)

[![CI with install](https://github.com/fusion-energy/spectrum_plotter/actions/workflows/ci_with_install.yml/badge.svg)](https://github.com/fusion-energy/spectrum_plotter/actions/workflows/ci_with_install.yml)

[![Upload Python Package](https://github.com/fusion-energy/spectrum_plotter/actions/workflows/python-publish.yml/badge.svg)](https://github.com/fusion-energy/spectrum_plotter/actions/workflows/python-publish.yml)

# Spectrum Plotter
A Python package for creating standard plots for neutron / photon / particle spectrum

# Installation

To make use of this package you wll need OpenMC installed.
See the instructions [here](https://docs.openmc.org/en/stable/quickinstall.html) for installing OpenMC.

```bash
pip install spectrum_plotter
```

# Usage

There are two main functions for plotting spectrum:

```plot_spectrum_from_values()``` - allows users to pass in the tally via a dictionary of tuples where each tuple contains x,y and optionally y_error values as numpy arrays.

```plot_spectrum_from_tally()``` - allows users to pass in an OpenMC tally and plot the result. Units can be automatically scaled,normalised and converted.

:point_right: [Examples](https://github.com/fusion-energy/spectrum_plotter/tree/main/examples)
