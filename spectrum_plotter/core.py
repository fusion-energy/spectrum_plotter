from pathlib import Path
from typing import Dict, Iterable, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from numpy import ndarray
from numpy.lib.function_base import trim_zeros


def plot_spectrum(
    spectrum: dict,
    x_label: Optional[str] = "",
    y_label: Optional[str] = "",
    x_scale: Optional[str] = "linear",
    y_scale: Optional[str] = "linear",
    title: Optional[str] = "",
    trim_zeros: bool = True,
    legend: bool = True,
    filename: Optional[str] = None,
    plotting_package="matplotlib",
):

    dictionary_of_values = {}

    for key, value in spectrum.items():

        if isinstance(value, tuple):

            dictionary_of_values[key] = value
        else:
            import openmc
            tally_df = value.get_pandas_dataframe()

            x = tally_df["energy low [eV]"]
            y = tally_df["mean"]
            y_err = tally_df["std. dev."]

            dictionary_of_values[key] = (x, y, y_err)

    figure = plot_spectrum_from_values(
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

    save_plot(plotting_package=plotting_package, filename=filename, figure=figure)

    return figure


def plot_spectra(
    spectra: Tuple[ndarray, ndarray, ndarray],
    x_label: Optional[str] = "",
    y_label: Optional[str] = "",
    x_scale: Optional[str] = "linear",
    y_scale: Optional[str] = "linear",
    title: Optional[str] = "",
    trim_zeros: bool = True,
    filename: Optional[str] = None,
    plotting_package="matplotlib",
):

    if isinstance(spectra, tuple):
        plot = plot_spectra_from_values(
            spectra=spectra,
            x_label=x_label,
            y_label=y_label,
            x_scale=x_scale,
            y_scale=y_scale,
            title=title,
            trim_zeros=trim_zeros,
            filename=filename,
            plotting_package=plotting_package,
        )
    else:
        plot = plot_spectra_from_tally(
            spectra=spectra,
            x_label=x_label,
            y_label=y_label,
            x_scale=x_scale,
            y_scale=y_scale,
            title=title,
            trim_zeros=trim_zeros,
            filename=filename,
            plotting_package=plotting_package,
        )
    return plot


def plot_spectrum_from_tally(
    spectrum: dict,
    x_label: Optional[str] = "",
    y_label: Optional[str] = "",
    x_scale: Optional[str] = "linear",
    y_scale: Optional[str] = "linear",
    title: Optional[str] = "",
    trim_zeros: bool = True,
    legend: bool = True,
    filename: Optional[str] = None,
    plotting_package="matplotlib",
):
    import openmc

    dictionary_of_values = {}

    for key, value in spectrum.items():
        tally_df = value.get_pandas_dataframe()

        x = tally_df["energy low [eV]"]
        y = tally_df["mean"]
        y_err = tally_df["std. dev."]

        dictionary_of_values[key] = (x, y, y_err)

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


def plot_spectra_from_tally(
    spectra: Tuple[ndarray, ndarray, ndarray],
    x_label: Optional[str] = "",
    y_label: Optional[str] = "",
    x_scale: Optional[str] = "linear",
    y_scale: Optional[str] = "linear",
    title: Optional[str] = "",
    trim_zeros: bool = True,
    filename: Optional[str] = None,
    plotting_package="matplotlib",
):

    import openmc

    tally_df = spectra.get_pandas_dataframe()

    x = tally_df["energy low [eV]"]
    y = tally_df["mean"]
    y_err = tally_df["std. dev."]

    plot = plot_spectra_from_values(
        spectra=(x, y, y_err),
        x_label=x_label,
        y_label=y_label,
        x_scale=x_scale,
        y_scale=y_scale,
        title=title,
        trim_zeros=trim_zeros,
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
    trim_zeros: bool = True,
    legend: bool = True,
    filename: Optional[str] = None,
    plotting_package="matplotlib",
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

    save_plot(plotting_package=plotting_package, filename=filename, figure=figure)

    return figure


def plot_spectra_from_values(
    spectra: Tuple[ndarray, ndarray, ndarray],
    x_label: Optional[str] = "",
    y_label: Optional[str] = "",
    x_scale: Optional[str] = "linear",
    y_scale: Optional[str] = "linear",
    title: Optional[str] = "",
    trim_zeros: bool = True,
    filename: Optional[str] = None,
    plotting_package="matplotlib",
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

    figure = add_axis_title_labels(
        x_label=x_label,
        y_label=y_label,
        y_scale=y_scale,
        x_scale=x_scale,
        title=title,
        legend=None,
        plotting_package=plotting_package,
    )

    figure = add_spectra_to_plot(
        spectra=spectra,
        trim_zeros=trim_zeros,
        label=None,
        plotting_package=plotting_package,
        figure=figure,
    )

    save_plot(plotting_package=plotting_package, filename=filename, figure=figure)

    return figure


def save_plot(plotting_package: "str", filename: "str", figure):

    if filename:
        if plotting_package == " matplotlib":
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

    if plotting_package == "matplotlib":
        plt.figure(0)
        plt.xlabel(x_label)
        plt.ylabel(y_label)

        plt.yscale(y_scale)
        plt.xscale(x_scale)

        plt.title(title)

        if legend:
            plt.legend()

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

        plt.step(x, y, where="pre", label=label)

        if len(spectra) == 3:
            lower_y = y - y_err
            upper_y = y + y_err
            plt.fill_between(x, lower_y, upper_y, step="pre", color="k", alpha=0.15)

        return plt

    elif plotting_package == "plotly":

        # options are 'linear', 'spline', 'hv', 'vh', 'hvh', 'vhv'
        shape = "vh"

        # adds a line for the upper stanadard deviation bound
        figure.add_trace(
            go.Scatter(
                mode="lines",
                x=x,
                y=y + y_err,
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
                name="std. dev.",
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
