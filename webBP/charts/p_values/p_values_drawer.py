from charts.p_values.data_for_chart import DataForChart
import matplotlib.pyplot as plt


class PValuesDrawer:

    y_axis_ticks = [0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0]
    y_axis_labels = ['0.0', '0.00001', '0.0001', '0.001', '0.01', '0.1', '1.0']

    def draw_chart(self, data: DataForChart, file: str):
        plt.title(data.title)
        plt.xlabel(data.x_label)
        plt.ylabel(data.y_label)

        plt.yscale('log')
        plt.ylim((0.000001, 1.0))
        plt.grid(axis='y', linestyle='-')

        plt.plot(data.x_values, data.y_values, '.', color='blue')

        plt.xticks(data.x_ticks_positions, data.x_ticks_labels, rotation='vertical')
        plt.yticks(PValuesDrawer.y_axis_ticks, PValuesDrawer.y_axis_labels)
        plt.axhline(y=data.alpha, color='r', linestyle='--')
        plt.savefig(file, bbox_inches='tight')
        plt.clf()
