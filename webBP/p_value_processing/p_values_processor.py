from managers.resultsmanager import ResultsManager
from p_value_processing.nist_loader import NistLoader
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_processing_error import PValuesProcessingError
from p_value_processing.processing_dto import ProcessingDto


class PValuesProcessor:
    def __init__(self):
        self._nist_loader = NistLoader()

    def process_p_values(self, dto: ProcessingDto) -> PValuesAccumulator:
        if dto is None or dto.empty():
            raise PValuesProcessingError('No directory for processing')

        accumulator = PValuesAccumulator()

        for test_id, directory in dto:
            self._nist_loader.load_p_values_in_dir(directory)
            dto = self._nist_loader.generate_dto()
            accumulator.add(test_id, dto)
            self._nist_loader.reset()

        return accumulator
