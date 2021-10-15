from typing import Dict, Iterable, Optional

import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.function_base import trim_zeros


def plot_spectrum(
    spectrum: Dict[str, Iterable[float]],
    x_label: Optional[str] = "",
    y_label: Optional[str] = "",
    x_scale: Optional[str] = "linear",
    y_scale: Optional[str] = "linear",
    title: Optional[str] = "",
    trim_zeros: Optional[bool] = True,
    legend: Optional[bool] = True,
    filename: Optional[str] = None,
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

    for key, value in spectrum.items():
        x = value[0]
        y = value[1]
        if len(value) == 3:
            y_err = value[2]

        # trimming required for spectra energy groups which have one more energy bin
        if len(x) == len(y) + 1:
            x = x[:-1]

        if trim_zeros is True:
            y = np.trim_zeros(np.array(y))
            x = np.array(x[: len(y)])
            if len(value) == 3:
                y_err = np.array(y_err[: len(y)])
        else:
            y = np.array(y)
            x = np.array(x)
            if len(value) == 3:
                y_err = np.array(y_err)

        plt.figure(1)

        plt.xlabel(x_label)
        plt.ylabel(y_label)

        # mid and post are also options but pre is used as energy bins start from 0
        plt.step(x, y, where="pre", label=key)

        plt.yscale(y_scale)
        plt.xscale(x_scale)

        if len(value) == 3:
            lower_y = y - y_err
            upper_y = y + y_err
            plt.fill_between(x, lower_y, upper_y, step="pre", color="k", alpha=0.15)

    if legend:
        plt.legend()
    plt.title(title)
    if filename:
        plt.savefig(filename, bbox_inches="tight", dpi=400)

    return plt


def plot_spectra(
    spectra: Iterable[float],
    x_label: Optional[str] = "",
    y_label: Optional[str] = "",
    x_scale: Optional[str] = "linear",
    y_scale: Optional[str] = "linear",
    title: Optional[str] = "",
    trim_zeros: Optional[bool] = True,
    filename: Optional[str] = None,
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

    x = spectra[0]
    y = spectra[1]
    if len(spectra) == 3:
        y_err = spectra[2]

    # trimming required for spectra energy groups which have one more energy bin
    if len(x) == len(y) + 1:
        x = x[:-1]

    if trim_zeros is True:
        y = np.trim_zeros(np.array(y))
        x = np.array(x[: len(y)])
        if len(spectra) == 3:
            y_err = np.array(y_err[: len(y)])
    else:
        y = np.array(y)
        x = np.array(x)
        if len(spectra) == 3:
            y_err = np.array(y_err)

    plt.figure(0)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # mid and post are also options but pre is used as energy bins start from 0
    plt.step(x, y, where="pre")

    plt.yscale(y_scale)
    plt.xscale(x_scale)

    if len(spectra) == 3:
        lower_y = y - y_err
        upper_y = y + y_err
        plt.fill_between(x, lower_y, upper_y, step="pre", color="k", alpha=0.15)

    plt.title(title)

    if filename:
        plt.savefig(filename, bbox_inches="tight", dpi=400)

    return plt
