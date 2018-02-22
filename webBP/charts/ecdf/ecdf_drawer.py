import matplotlib.pyplot as plt
import numpy as np

from charts.ecdf.data_for_ecdf_drawer import DataForEcdfDrawer


class EcdfDrawer:
    def draw_chart(self, data: DataForEcdfDrawer, file: str):
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.set_title(data.title)
        ax.set_xlabel(data.x_label)
        ax.set_ylabel(data.y_label)
        ax.legend(loc='right')
        ax.set_xlim(0.0, 1.0)
        ax.set_ylim(0.0, 1.0)

        bins = np.arange(0.0, 1.000001, 0.001).tolist()

        ax.hist(data.p_values, bins, density=True, histtype='step', cumulative=True,
                label=data.empirical_label, linewidth=1.5)

        c_x = [0.0, 1.0]
        c_y = [0.0, 1.0]
        ax.plot(c_x, c_y, 'k--', linewidth=1.0, label=data.theoretical_label)

        plt.savefig(file, dpi=300)
