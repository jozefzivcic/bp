import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame

from charts.histogram.data_for_histogram_drawer import DataForHistogramDrawer


class HistogramDrawer:
    def draw_chart(self, data: DataForHistogramDrawer, file: str):
        df = pd.read_json(data.json_data_string, orient='split')  # type: DataFrame
        plot = df.plot(kind="bar", title=data.title, legend=False)
        plot.set(xlabel=data.x_label, ylabel=data.y_label)
        fig = plot.get_figure()
        fig.autofmt_xdate()
        fig.savefig(file, dpi=300)
        fig.clf()
        plt.close(fig)
