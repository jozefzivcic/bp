import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from charts.boxplot_per_test.data_for_boxplot_pt_drawer import DataForBoxplotPTDrawer


class BoxplotPTDrawer:
    def draw_chart(self, data: DataForBoxplotPTDrawer, file: str):
        df = pd.read_json(data.json_data_str)
        ax = sns.boxplot(orient='v', data=df)
        ax.set_title(data.title)
        fig = ax.get_figure()
        fig.savefig(file)
        fig.clf()
        plt.close(fig)
