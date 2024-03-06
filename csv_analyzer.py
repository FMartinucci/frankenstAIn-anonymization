import csv
from typing import Iterable

from presidio_analyzer import BatchAnalyzerEngine, DictAnalyzerResult

class CSVAnalyzer(BatchAnalyzerEngine):

    def __init__(self, engine=None):
        if engine is not None:
            self.analyzer_engine = engine
    

    def analyze_csv(
        self,
        csv_full_path: str,
        language: str,
        **kwargs,
    ) -> Iterable[DictAnalyzerResult]:

        with open(csv_full_path, 'r') as csv_file:
            csv_list = list(csv.reader(csv_file))
            csv_dict = {header: list(map(str, values)) for header, *values in zip(*csv_list)}
            analyzer_results = self.analyze_dict(csv_dict, language, **kwargs)
            return list(analyzer_results)
