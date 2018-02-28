from charts.p_values.data_for_p_values_drawer import DataForPValuesDrawer
import matplotlib.pyplot as plt


class PValuesDrawer:
    def draw_chart(self, data: DataForPValuesDrawer, file: str):
        plt.title(data.title)
        plt.xlabel(data.x_label)
        plt.ylabel(data.y_label)

        plt.yscale('log')
        if data.zoomed:
            plt.ylim((0.000001, data.y_axis_ticks[-1]))
        else:
            plt.ylim((0.000001, 1.0))
        plt.grid(axis='y', linestyle='-')

        plt.plot(data.x_values, data.y_values, '^', color='blue', markersize=5.0, alpha=0.3)

        plt.xticks(data.x_ticks_positions, data.x_ticks_labels, rotation='vertical')
        plt.yticks(data.y_axis_ticks, data.y_axis_labels)
        if not data.zoomed:
            plt.axhline(y=data.alpha, color='r', linestyle='--')
        plt.savefig(file, bbox_inches='tight', dpi=300)
        plt.clf()
        plt.close('all')
