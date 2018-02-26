from charts.ecdf.data_for_ecdf_drawer import DataForEcdfDrawer
from charts.ecdf_dto import EcdfDto
from charts.extracted_data import ExtractedData
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_file_type import PValuesFileType


class EcdfExtractor:
    def get_data_from_accumulator(self, acc: PValuesAccumulator, ecdf_dto: EcdfDto) -> DataForEcdfDrawer:
        seq = ecdf_dto.sequence
        p_values_dto = acc.get_dto_for_test(seq.test_id)
        if seq.p_values_file == PValuesFileType.RESULTS:
            p_values = p_values_dto.get_results_p_values()
        elif seq.p_values_file == PValuesFileType.DATA:
            p_values = p_values_dto.get_data_p_values(seq.data_num)
        else:
            raise ValueError('Unsupported file type {}'.format(seq.p_values_file))
        data = DataForEcdfDrawer(ecdf_dto.alpha, ecdf_dto.title, ecdf_dto.x_label, ecdf_dto.y_label,
                                 ecdf_dto.empirical_label, ecdf_dto.theoretical_label, p_values)
        return ExtractedData(data)
