from charts.data_source_info import DataSourceInfo
from charts.ecdf.data_for_ecdf_drawer import DataForEcdfDrawer
from charts.dto.ecdf_dto import EcdfDto
from charts.extracted_data import ExtractedData
from charts.tests_in_chart import TestsInChart
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_dto import PValuesDto
from p_value_processing.p_values_file_type import PValuesFileType


class EcdfExtractor:
    def get_data_from_accumulator(self, acc: PValuesAccumulator, ecdf_dto: EcdfDto) -> ExtractedData:
        ex_data = ExtractedData()
        for seq in ecdf_dto.sequences:
            p_values_dto = acc.get_dto_for_test_safe(seq.test_id)
            if p_values_dto is None:
                continue
            p_values = self.get_p_values(p_values_dto, seq)
            data = DataForEcdfDrawer(ecdf_dto.alpha, ecdf_dto.title, ecdf_dto.x_label, ecdf_dto.y_label,
                                     ecdf_dto.empirical_label, ecdf_dto.theoretical_label, p_values)
            ds_info = DataSourceInfo(TestsInChart.SINGLE_TEST, seq)
            ex_data.add_data(ds_info, data)
        return ex_data

    def get_p_values(self, p_values_dto: PValuesDto, seq: PValueSequence) -> list:
        if seq.p_values_file == PValuesFileType.RESULTS:
            return p_values_dto.get_results_p_values()
        elif seq.p_values_file == PValuesFileType.DATA:
            return p_values_dto.get_data_p_values(seq.data_num)
        else:
            raise ValueError('Unsupported file type {}'.format(seq.p_values_file))
