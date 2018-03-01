import matplotlib.pyplot as plt
import pandas as pd

from charts.histogram.data_for_histogram_drawer import DataForHistogramDrawer


class HistogramDrawer:
    def draw_chart(self, data: DataForHistogramDrawer, file: str):
        df = pd.read_json(data.json_data_string)
        plot = df.plot(kind="bar", x=df[0], title=data.title, legend=False)
        plot.set(xlabel=data.x_label, ylabel=data.y_label)
        fig = plot.get_figure()
        fig.autofmt_xdate()
        fig.savefig(file, dpi=300)
        fig.clf()
        plt.close(fig)
