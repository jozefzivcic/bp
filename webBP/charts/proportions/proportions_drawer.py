import matplotlib.pyplot as plt

from charts.proportions.data_for_proportions_drawer import DataForProportionsDrawer


class ProportionsDrawer(object):
    def draw_chart(self, data: DataForProportionsDrawer, file_name: str):
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.set_title(data.title)
        ax.set_xlabel(data.x_label)
        ax.set_ylabel(data.y_label)
        ax.set_ylim(data.y_lim_low, data.y_lim_high)
        ax.set_yscale('linear')
        ax.set_xticks(data.x_ticks_pos)
        ax.set_xticklabels(data.x_ticks_lab)
        ax.plot(data.x_values, data.y_values, marker='.', linestyle='None')
        ax.axhline(y=data.y_interval_low, color='r', linestyle='--', linewidth=0.5)
        ax.axhline(y=data.y_interval_high, color='r', linestyle='--', linewidth=0.5)

        fig.autofmt_xdate()
        fig.savefig(file_name, dpi=300)
        plt.clf()
        plt.close(fig)
