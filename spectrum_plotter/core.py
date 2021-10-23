from typing import Dict, Iterable, Optional, Tuple, Union
import plotly.graph_objects as go


import matplotlib.pyplot as plt
import numpy as np
from numpy import ndarray
from numpy.lib.function_base import trim_zeros


def plot_spectrum(
    spectrum: Dict[str, Tuple[ndarray, ndarray, ndarray]],
    x_label: Optional[str] = "",
    y_label: Optional[str] = "",
    x_scale: Optional[str] = "linear",
    y_scale: Optional[str] = "linear",
    title: Optional[str] = "",
    trim_zeros: bool = True,
    legend: bool = True,
    filename: Optional[str] = None,
    ploting_package='matplotlib'
) -> plt:
    """Plots a stepped line graph with optional shaded region for Y error.
    Intended use for ploting neutron / photon spectra

    Arguments:
        spectrum: A dictionary of x, y, y_error values
        x_label: the label to use on the x axis,
        y_label: the label to use on the y axis,
        x_scale: the scale to use for the x axis. Options are 'linear', 'log'
        y_scale: the scale to use for the y axis. Options are 'linear', 'log'
        title: the plot title
        filename: the filename to save the plot as
        trim_zeros: whether any zero values at the end of the x iterable
            should be removed from the plot.

    Returns:
        the matplotlib.pyplot object produced
    """

    plt = add_axis_title_labels(
        x_label,
        y_label,
        y_scale,
        x_scale,
        title,
        ploting_package,
    )

    for key, value in spectrum.items():

        add_spectra_to_matplotlib_plot(value, trim_zeros, label=key)

    if legend:
        plt.legend()
    plt.title(title)
    if filename:
        plt.savefig(filename, bbox_inches="tight", dpi=400)

    return plt


def plot_spectra(
    spectra: Tuple[ndarray, ndarray, ndarray],
    x_label: Optional[str] = "",
    y_label: Optional[str] = "",
    x_scale: Optional[str] = "linear",
    y_scale: Optional[str] = "linear",
    title: Optional[str] = "",
    trim_zeros: bool = True,
    filename: Optional[str] = None,
    ploting_package='matplotlib'
) -> plt:
    """Plots a stepped line graph with optional shaded region for Y error.
    Intended use for ploting neutron / photon spectra

    Arguments:
        spectra: An iterable of x, y, y_error values
        x_label: the label to use on the x axis,
        y_label: the label to use on the y axis,
        x_scale: the scale to use for the x axis. Options are 'linear', 'log'
        y_scale: the scale to use for the y axis. Options are 'linear', 'log'
        title: the plot title
        filename: the filename to save the plot as
        trim_zeros: whether any zero values at the end of the x iterable
            should be removed from the plot.

    Returns:
        the matplotlib.pyplot object produced
    """

    plt = add_axis_title_labels(
        x_label,
        y_label,
        y_scale,
        x_scale,
        title,
        ploting_package,
    )

    add_spectra_to_matplotlib_plot(spectra=spectra, trim_zeros=trim_zeros, label=None)

    if filename:
        plt.savefig(filename, bbox_inches="tight", dpi=400)

    return plt


def add_axis_title_labels(
    x_label,
    y_label,
    y_scale,
    x_scale,
    title,
    ploting_package
):

    if ploting_package == 'matplotlib':
        plt.figure(0)
        plt.xlabel(x_label)
        plt.ylabel(y_label)

        plt.yscale(y_scale)
        plt.xscale(x_scale)

        plt.title(title)

        return plt
    elif ploting_package == 'plotly':
        figure = go.Figure()

        figure.update_layout(
            xaxis={
                "title": x_label,
                # "range": (0, 14.1e6)
            },
            yaxis={
                "title": y_label
            },
        )

        # this adds the dropdown box for log and lin axis selection
        # figure.update_layout(
        #     updatemenus=[
        #         go.layout.Updatemenu(
        #             buttons=list(
        #                 [
        #                     dict(
        #                         args=[
        #                             {
        #                                 "xaxis.type": "lin",
        #                                 "yaxis.type": "lin",
        #                                 "xaxis.range": (0, 14.1e6),
        #                             }
        #                         ],
        #                         label="linear(x) , linear(y)",
        #                         method="relayout",
        #                     ),
        #                     dict(
        #                         args=[{"xaxis.type": "log", "yaxis.type": "log"}],
        #                         label="log(x) , log(y)",
        #                         method="relayout",
        #                     ),
        #                     dict(
        #                         args=[{"xaxis.type": "log", "yaxis.type": "lin"}],
        #                         label="log(x) , linear(y)",
        #                         method="relayout",
        #                     ),
        #                     dict(
        #                         args=[
        #                             {
        #                                 "xaxis.type": "lin",
        #                                 "yaxis.type": "log",
        #                                 "xaxis.range": (0, 14.1e6),
        #                             }
        #                         ],
        #                         label="linear(x) , log(y)",
        #                         method="relayout",
        #                     ),
        #                 ]
        #             ),
        #             pad={"r": 10, "t": 10},
        #             showactive=True,
        #             x=0.5,
        #             xanchor="left",
        #             y=1.1,
        #             yanchor="top",
        #         ),
        #     ]
        # )
    else:
        msg = f'ploting_package must be set to "matplotlib" or "plotly" not {ploting_package}'
        raise ValueError(msg)


def add_spectra_to_matplotlib_plot(
    spectra: Tuple[ndarray, ndarray, ndarray], trim_zeros: bool, label: Union[str, None]
):
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

    plt.step(x, y, where="pre", label=label)

    if len(spectra) == 3:
        lower_y = y - y_err
        upper_y = y + y_err
        plt.fill_between(x, lower_y, upper_y, step="pre", color="k", alpha=0.15)
