from os import makedirs
from unittest import TestCase

from os.path import exists, dirname, abspath, join

from shutil import rmtree
from unittest.mock import patch, MagicMock

from charts.boxplot_per_test.boxplot_pt_creator import BoxplotPTCreator
from charts.boxplot_per_test.data_for_boxplot_pt_creator import DataForBoxplotPTCreator
from charts.boxplot_pt_dto import BoxplotPTDto
from charts.chart_type import ChartType
from charts.charts_storage import ChartsStorage
from charts.data_source_info import DataSourceInfo
from charts.tests_in_chart import TestsInChart
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_file_type import PValuesFileType
from tests.data_for_tests.common_data import TestsIdData, FileIdData
from tests.data_for_tests.common_functions import db_test_dao_get_test_by_id, nist_dao_get_nist_param_for_test, \
    func_prepare_acc

this_dir = dirname(abspath(__file__))
working_dir = join(this_dir, 'working_dir_boxplot_pt_creator')


class TestBoxplotPTCreator(TestCase):
    def setUp(self):
        if not exists(working_dir):
            makedirs(working_dir)
        mock = patch('managers.dbtestmanager.DBTestManager.get_test_by_id', side_effect=db_test_dao_get_test_by_id)
        self.addCleanup(mock.stop)
        mock.start()
        mock = patch('managers.nisttestmanager.NistTestManager.get_nist_param_for_test',
                     side_effect=nist_dao_get_nist_param_for_test)
        self.addCleanup(mock.stop)
        mock.start()
        storage = MagicMock(nist='nist')
        self.creator = BoxplotPTCreator(None, storage)

    def tearDown(self):
        if exists(working_dir):
            rmtree(working_dir)

    def test_create_one_boxplot(self):
        acc = func_prepare_acc()
        seqcs = [[PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 1),
                  PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 2)]]
        dto = BoxplotPTDto('Boxplot(s) per test', seqcs)
        data = DataForBoxplotPTCreator(dto, acc, working_dir, FileIdData.file1_id)
        ret = self.creator.create_boxplots(data)

        self.assertEqual(ChartsStorage, type(ret))
        self.assertEqual(1, len(ret.get_all_infos()))

        ch_info = ret.get_all_infos()[0]
        ds_info = DataSourceInfo(TestsInChart.MULTIPLE_TESTS, seqcs[0])
        self.assertEqual(ds_info, ch_info.ds_info)
        self.assertTrue(exists(ch_info.path_to_chart))
        self.assertEqual(ChartType.BOXPLOT_PT, ch_info.chart_type)
        self.assertEqual(FileIdData.file1_id, ch_info.file_id)

    def test_create_two_boxplots_more_data(self):
        acc = func_prepare_acc()
        seqcs = [[PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)],
                 [PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 1),
                  PValueSequence(TestsIdData.test3_id, PValuesFileType.DATA, 2)]]
        dto = BoxplotPTDto('Boxplot(s) per test', seqcs)
        data = DataForBoxplotPTCreator(dto, acc, working_dir, FileIdData.file1_id)
        ret = self.creator.create_boxplots(data)

        self.assertEqual(ChartsStorage, type(ret))
        self.assertEqual(2, len(ret.get_all_infos()))

        for i, ch_info in enumerate(ret.get_all_infos()):
            ds_info = DataSourceInfo(TestsInChart.MULTIPLE_TESTS, seqcs[i])
            self.assertEqual(ds_info, ch_info.ds_info)
            self.assertTrue(exists(ch_info.path_to_chart))
            self.assertEqual(ChartType.BOXPLOT_PT, ch_info.chart_type)
            self.assertEqual(FileIdData.file1_id, ch_info.file_id)

    def test_get_filename(self):
        ret = self.creator.get_filename(working_dir, 5)
        self.assertEqual(join(working_dir, 'boxplot_pt_5.png'), ret)

        ret = self.creator.get_filename(working_dir, 54)
        self.assertEqual(join(working_dir, 'boxplot_pt_54.png'), ret)
