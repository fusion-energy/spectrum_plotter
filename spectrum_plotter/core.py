from pathlib import Path
from typing import Dict, Iterable, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import openmc_tally_unit_converter as otuc
import plotly.graph_objects as go
from numpy import ndarray
from numpy.lib.function_base import trim_zeros


def plot_spectrum_from_tally(
    spectrum: dict,
    x_label: Optional[str] = "",
    y_label: Optional[str] = "",
    x_scale: Optional[str] = "linear",
    y_scale: Optional[str] = "linear",
    title: Optional[str] = "",
    legend: bool = True,
    filename: Optional[str] = None,
    plotting_package: Optional[str] = "matplotlib",
    trim_zeros: bool = True,
    required_units: str = "centimeters / source_particle",
    required_energy_units: str = "eV",
    source_strength: float = None,
    volume: float = None,
):
    """Plots a stepped line graph with optional shaded region for Y error.
    Intended use for ploting neutron / photon spectra

    Arguments:
        spectrum: A dictionary of where the key is the spectra title and the
            dictionary values openmc.Tally objects. The tally objects can be
            accessed with the regular openmc.StatePoint('statepoint.batches.h5')
            method. Spectrum tallies should include an
            openmc.filter.EnergyFilter
        x_label: the label to use on the x axis,
        y_label: the label to use on the y axis,
        x_scale: the scale to use for the x axis. Options are 'linear', 'log'
        y_scale: the scale to use for the y axis. Options are 'linear', 'log'
        title: the title applied to the top of the plot
        legend: controls if a legend should be displayed or not. If set to True
            a legend with spectra titles will be displayed and if set to False
            the legend will not be displayed.
        filename: the filename to save the plot as should end with the correct
            extention supported by matplotlib (e.g .png) or plotly (e.g .html)
        plotting_package: the name of the python package to use when producing
            the plots. Options are 'matplotlib' or 'plotly'
        trim_zeros: whether any zero values at the end of the x iterable
            should be removed from the plot. This is useful when using standard
            energy groups that go beyond the energy of the particles simulated.
        required_units: The units desired for the Y axis. Defaults to
            "centimeters / source_particle" but supports units identified in
            the Python Pint package. If volume normalisation or source strength
            normalisation are required by the units then these arguments must
            also be provided.
        required_energy_units: "eV",
        source_strength: The strength of the source which is to be used for
            source normalization. A numeric value is expected but the units are
            assumed to be in particles per second or particles per pulse.
        volume: The volume which is to be used for volume normalisation. A
            numeric value is expected but the units are assumed to be in cm**3
            (centimeters cubed).

    Returns:
        the matplotlib.pyplot or plotly.graph_objects object produced
    """

    dictionary_of_values = {}

    for key, value in spectrum.items():

        x_y_y_err = otuc.process_spectra_tally(
            tally=value,
            required_units=required_units,
            required_energy_units=required_energy_units,
            source_strength=source_strength,
            volume=volume,
        )
        if len(x_y_y_err) == 3:
            x, y, y_err = x_y_y_err
            dictionary_of_values[key] = (x, y, y_err)
        else:
            x, y = x_y_y_err
            dictionary_of_values[key] = (x, y)

    plot = plot_spectrum_from_values(
        spectrum=dictionary_of_values,
        x_label=x_label,
        y_label=y_label,
        x_scale=x_scale,
        y_scale=y_scale,
        title=title,
        trim_zeros=trim_zeros,
        legend=legend,
        filename=filename,
        plotting_package=plotting_package,
    )

    return plot


def plot_spectrum_from_values(
    spectrum: Dict[str, Tuple[ndarray, ndarray, ndarray]],
    x_label: Optional[str] = "",
    y_label: Optional[str] = "",
    x_scale: Optional[str] = "linear",
    y_scale: Optional[str] = "linear",
    title: Optional[str] = "",
    legend: bool = True,
    filename: Optional[str] = None,
    plotting_package: Optional[str] = "matplotlib",
    trim_zeros: bool = True,
):
    """Plots a stepped line graph with optional shaded region for Y error.
    Intended use for ploting neutron / photon spectra

    Arguments:
        spectrum: A dictionary of where the key is the spectra title and the
            dictionary values are a list containing x and y values. Optionally
            y_error values can also be included in the list. x, y and y_error
            should all be numpy arrays.
        x_label: the label to use on the x axis,
        y_label: the label to use on the y axis,
        x_scale: the scale to use for the x axis. Options are 'linear', 'log'
        y_scale: the scale to use for the y axis. Options are 'linear', 'log'
        title: the title applied to the top of the plot
        legend: controls if a legend should be displayed or not. If set to True
            a legend with spectra titles will be displayed and if set to False
            the legend will not be displayed.
        filename: the filename to save the plot as should end with the correct
            extention supported by matplotlib (e.g .png) or plotly (e.g .html)
        plotting_package: the name of the python package to use when producing
            the plots. Options are 'matplotlib' or 'plotly'
        trim_zeros: whether any zero values at the end of the x iterable
            should be removed from the plot. This is useful when using standard
            energy groups that go beyond the energy of the particles simulated.

    Returns:
        the matplotlib.pyplot or plotly.graph_objects object produced
    """

    figure = add_axis_title_labels(
        x_label=x_label,
        y_label=y_label,
        y_scale=y_scale,
        x_scale=x_scale,
        title=title,
        legend=legend,
        plotting_package=plotting_package,
    )

    for key, value in spectrum.items():

        figure = add_spectra_to_plot(
            value,
            trim_zeros,
            label=key,
            plotting_package=plotting_package,
            figure=figure,
        )
    # add legend to matplotlib after label names have been set
    if legend and plotting_package == "matplotlib":
        figure.legend()

    save_plot(plotting_package=plotting_package, filename=filename, figure=figure)

    return figure


def save_plot(plotting_package: str, filename: str, figure):
    """Saves the matplotlib or plotly graph object as a file."""
    if filename:
        if plotting_package == "matplotlib":
            figure.savefig(filename, bbox_inches="tight", dpi=400)
        elif plotting_package == "plotly":
            if Path(filename).suffix == ".html":
                figure.write_html(filename)
            else:
                figure.write_image(filename)


def add_axis_title_labels(
    x_label: str,
    y_label: str,
    y_scale: str,
    x_scale: str,
    title: str,
    legend: bool,
    plotting_package: str,
):
    """Adds axis labels and the title to the matplot lib or plotlg graph object"""

    if plotting_package == "matplotlib":

        plt.close()
        plt.cla()
        plt.clf()
        plt.figure(1, clear=True)

        plt.xlabel(x_label)
        plt.ylabel(y_label)

        plt.yscale(y_scale)
        plt.xscale(x_scale)

        plt.title(title)

        return plt

    elif plotting_package == "plotly":
        figure = go.Figure()

        figure.update_layout(
            title=title,
            xaxis={"title": x_label, "type": x_scale},
            yaxis={"title": y_label, "type": y_scale},
        )

        if x_scale == "log":
            not_x_scale = "lin"
        else:
            not_x_scale = "log"

        if y_scale == "log":
            not_y_scale = "lin"
        else:
            not_y_scale = "log"

        buttons_list = []
        for xscale in [x_scale, not_x_scale]:
            for yscale in [y_scale, not_y_scale]:
                buttons_list.append(
                    {
                        "args": [
                            {
                                "xaxis.type": xscale,
                                "yaxis.type": yscale,
                            }
                        ],
                        "label": f"{xscale}(x) , {yscale}(y)",
                        "method": "relayout",
                    }
                )

        # this adds the dropdown box for log and lin axis selection
        figure.update_layout(
            updatemenus=[
                go.layout.Updatemenu(
                    buttons=buttons_list,
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.5,
                    xanchor="left",
                    y=1.1,
                    yanchor="top",
                ),
            ]
        )

        return figure

    else:
        msg = f'plotting_package must be set to "matplotlib" or "plotly" not {plotting_package}'
        raise ValueError(msg)


def add_spectra_to_plot(
    spectra: Tuple[ndarray, ndarray, ndarray],
    trim_zeros: bool,
    label: Union[str, None],
    plotting_package: str,
    figure,
):
    """Adds a step line to the matplotlib or plotly graph object"""
    # mid and post are also options but pre is used as energy bins start from 0

    x = spectra[0]
    y = spectra[1]
    if len(spectra) == 3:
        y_err = spectra[2]

    # trimming required for spectra energy groups which have one more energy bin
    if len(x) == len(y) + 1:
        x = x[:-1]

    if trim_zeros is True:
        y = np.trim_zeros(np.array(y), trim="b")
        x = np.array(x[: len(y)])
        if len(spectra) == 3:
            y_err = np.array(y_err[: len(y)])
    else:
        y = np.array(y)
        x = np.array(x)
        if len(spectra) == 3:
            y_err = np.array(y_err)

    if plotting_package == "matplotlib":

        figure.step(x, y, where="pre", label=label)

        if len(spectra) == 3:
            lower_y = y - y_err
            upper_y = y + y_err
            figure.fill_between(x, lower_y, upper_y, step="pre", color="k", alpha=0.15)

        return figure

    elif plotting_package == "plotly":

        # options are 'linear', 'spline', 'hv', 'vh', 'hvh', 'vhv'
        shape = "hv"

        if len(spectra) == 3:
            # adds a line for the upper stanadard deviation bound
            figure.add_trace(
                go.Scatter(
                    mode="lines",
                    x=x,
                    y=y + y_err,
                    name="std. dev. upper",
                    line=dict(shape=shape, width=0),
                )
            )

            # adds a line for the lower stanadard deviation bound
            figure.add_trace(
                go.Scatter(
                    mode="lines",
                    x=x,
                    # todo process std dev correction
                    y=y - y_err,
                    name="std. dev. lower",
                    # options are 'none', 'tozeroy', 'tozerox', 'tonexty', 'tonextx', 'toself', 'tonext'
                    fill="tonextx",
                    fillcolor=f"rgba{(0.2,0.2,0.2, 0.1)}",
                    line=dict(shape=shape, width=0),
                )
            )

        # adds a line for the tally result
        figure.add_trace(
            go.Scatter(
                mode="lines",
                x=x,
                y=y,
                name=label,
                line=dict(shape=shape),
            )
        )

        return figure

    else:
        msg = f'plotting_package must be set to "matplotlib" or "plotly" not {plotting_package}'
        raise ValueError(msg)
