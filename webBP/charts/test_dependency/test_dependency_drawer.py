from charts.test_dependency.data_for_test_dependency_drawer import DataForTestDependencyDrawer
import matplotlib.pyplot as plt


class TestDependencyDrawer:
    def draw_chart(self, data: DataForTestDependencyDrawer, file: str):
        plt.plot(data.p_values1, data.p_values2, '.')
        plt.title(data.title)
        plt.xlabel(data.x_label)
        plt.ylabel(data.y_label)
        plt.xlim((0.0, 1.0))
        plt.ylim((0.0, 1.0))
        plt.savefig(file, bbox_inches='tight', dpi=300)
        plt.clf()
        plt.close(plt.gcf())
