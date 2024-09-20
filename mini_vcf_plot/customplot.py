from typing import IO
from dae.genomic_resources.histogram import CategoricalHistogram
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("agg")


def plot_clnsig(
    outfile: IO,
    histogram: CategoricalHistogram,
    xlabel: str,
    _small_values_description: str | None = None,
    _large_values_description: str | None = None,
) -> None:
    """Plot histogram and save it into outfile."""
    # pylint: disable=import-outside-toplevel
    values = list(sorted(histogram.raw_values.items(), key=lambda x: -x[1]))
    values = [v for v in values if "|" not in v[0]]
    labels = [v[0] for v in values]
    counts = [v[1] for v in values]

    plt.figure(figsize=(40, 80), tight_layout=True)
    _, ax = plt.subplots()
    ax.bar(
        x=labels,
        height=counts,
        tick_label=[str(v) for v in labels],
        log=histogram.config.y_log_scale,
        align="center",
    )
    plt.xlabel(f"\n{xlabel}")
    plt.ylabel("gaga")
    plt.tick_params(axis="x", labelrotation=90, direction="out")
    plt.tight_layout()
    plt.savefig(outfile)
    plt.clf()
