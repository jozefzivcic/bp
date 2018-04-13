from configparser import ConfigParser
from unittest import TestCase
from unittest.mock import patch, call

from enums.nist_test_type import NistTestType
from pdf_generating.report_to_latex import parse_line, get_header, get_begin_of_table, get_end_of_table, get_latex_line, \
    get_test_type_from_name, get_shorten_test_name


class TestReportToLatex(TestCase):
    def test_get_type_from_name_raises(self):
        with self.assertRaises(RuntimeError) as ex:
            get_test_type_from_name('asdf')
        self.assertEqual('Undefined name of test: "asdf"', str(ex.exception))

    def test_get_type_from_name(self):
        names = ['Frequency', 'Block Frequency', 'Cumulative Sums', 'Runs', 'Longest Run of Ones', 'Rank',
                 'Discrete Fourier Transform', 'Nonperiodic Template Matchings', 'Overlapping Template Matchings',
                 'Universal Statistical', 'Approximate Entropy', 'Random Excursions', 'Random Excursions Variant',
                 'Serial', 'Linear Complexity']
        for i, t_type in enumerate(NistTestType):
            name = names[i]
            ret = get_test_type_from_name(name)
            self.assertEqual(t_type, ret)

    def test_get_shorten_test_name_raises(self):
        with self.assertRaises(RuntimeError) as ex:
            get_shorten_test_name(16, None)
        self.assertEqual('Undefined type of test: "16"', str(ex.exception))

    def test_get_shorten_test_name(self):
        in_dict = {'Freq': 'Frequency', 'BFreq': 'Block Frequency', 'CuSums': 'Cummulative Sums', 'Runs': 'Runs',
                   'LongRun': 'Longest Run', 'Rank': 'Rank', 'FFT': 'FFT', 'Nonperiodic': 'Nonperiodic Template Match',
                   'Overlapping': 'Overlapping Template Matchings', 'Universal': 'Universal Statistical',
                   'Approx': 'Approximate Entropy', 'RandExcs': 'Random Excursions',
                   'RandExcsVar': 'Random Excursions Variant', 'Serial': 'Serial', 'Linear': 'Linear'}
        data = {'ShortNames': in_dict}
        cfg = ConfigParser()
        cfg.read_dict(data)

        test_name = get_shorten_test_name(NistTestType.TEST_FREQUENCY, cfg)
        self.assertEqual(in_dict['Freq'], test_name)

        test_name = get_shorten_test_name(NistTestType.TEST_BLOCK_FREQUENCY, cfg)
        self.assertEqual(in_dict['BFreq'], test_name)

        test_name = get_shorten_test_name(NistTestType.TEST_CUSUM, cfg)
        self.assertEqual(in_dict['CuSums'], test_name)

        test_name = get_shorten_test_name(NistTestType.TEST_RUNS, cfg)
        self.assertEqual(in_dict['Runs'], test_name)

        test_name = get_shorten_test_name(NistTestType.TEST_LONGEST_RUN, cfg)
        self.assertEqual(in_dict['LongRun'], test_name)

        test_name = get_shorten_test_name(NistTestType.TEST_RANK, cfg)
        self.assertEqual(in_dict['Rank'], test_name)

        test_name = get_shorten_test_name(NistTestType.TEST_FFT, cfg)
        self.assertEqual(in_dict['FFT'], test_name)

        test_name = get_shorten_test_name(NistTestType.TEST_NONPERIODIC, cfg)
        self.assertEqual(in_dict['Nonperiodic'], test_name)

        test_name = get_shorten_test_name(NistTestType.TEST_OVERLAPPING, cfg)
        self.assertEqual(in_dict['Overlapping'], test_name)

        test_name = get_shorten_test_name(NistTestType.TEST_UNIVERSAL, cfg)
        self.assertEqual(in_dict['Universal'], test_name)

        test_name = get_shorten_test_name(NistTestType.TEST_APEN, cfg)
        self.assertEqual(in_dict['Approx'], test_name)

        test_name = get_shorten_test_name(NistTestType.TEST_RND_EXCURSION, cfg)
        self.assertEqual(in_dict['RandExcs'], test_name)

        test_name = get_shorten_test_name(NistTestType.TEST_RND_EXCURSION_VAR, cfg)
        self.assertEqual(in_dict['RandExcsVar'], test_name)

        test_name = get_shorten_test_name(NistTestType.TEST_SERIAL, cfg)
        self.assertEqual(in_dict['Serial'], test_name)

        test_name = get_shorten_test_name(NistTestType.TEST_LINEARCOMPLEXITY, cfg)
        self.assertEqual(in_dict['Linear'], test_name)

    def test_parse_line(self):
        line = '  1   9   12   125 4567   505   11   6   456   87456  0.437274    0.675978   0.785465 Block Fr equency'
        groups = parse_line(line)
        self.assertEqual(1, int(groups[0]))
        self.assertEqual(9, int(groups[1]))
        self.assertEqual(12, int(groups[2]))
        self.assertEqual(125, int(groups[3]))
        self.assertEqual(4567, int(groups[4]))
        self.assertEqual(505, int(groups[5]))
        self.assertEqual(11, int(groups[6]))
        self.assertEqual(6, int(groups[7]))
        self.assertEqual(456, int(groups[8]))
        self.assertEqual(87456, int(groups[9]))
        self.assertAlmostEqual(0.437274, float(groups[10]), 1e-6)
        self.assertAlmostEqual(0.675978, float(groups[11]), 1e-6)
        self.assertAlmostEqual(0.785465, float(groups[12]), 1e-6)
        self.assertEqual('Block Fr equency', groups[13])

    def test_parse_line_tests(self):
        line = '  1   9   12   125 467   505   11   6   456   87456  0.437274    0.675978   0.785465 Frequency'
        groups = parse_line(line)
        self.assertEqual('Frequency', groups[13])

        line = '  1   9   12   125 467   505   11   6   456   87456  0.437274    0.675978   0.785465 Block Frequency'
        groups = parse_line(line)
        self.assertEqual('Block Frequency', groups[13])

        line = '  1   9   12   125 467   505   11   6   456   87456  0.437274    0.675978   0.785465 Cumulative Sums'
        groups = parse_line(line)
        self.assertEqual('Cumulative Sums', groups[13])

        line = '  1   9   12   125 467   505   11   6   456   87456  0.437274    0.675978   0.785465 Runs'
        groups = parse_line(line)
        self.assertEqual('Runs', groups[13])

        line = '  1   9   12   125 467   505   11   6   456  87456  0.437274    0.675978   0.785465 Longest Run of Ones'
        groups = parse_line(line)
        self.assertEqual('Longest Run of Ones', groups[13])

        line = '  1   9   12   125 467   505   11   6   456   87456  0.437274    0.675978   0.785465 Rank'
        groups = parse_line(line)
        self.assertEqual('Rank', groups[13])

        line = '  1   9   12  125 467 505 11 6 456 87456  0.437274 0.675978   0.785465 Discrete Fourier Transform'
        groups = parse_line(line)
        self.assertEqual('Discrete Fourier Transform', groups[13])

        line = '  1   9   12   125 467   505 11 6 456 87456 0.437274 0.675978 0.785465 Nonperiodic Template Matchings'
        groups = parse_line(line)
        self.assertEqual('Nonperiodic Template Matchings', groups[13])

        line = '  1   9   12   125 467 505 11 6 456 87456 0.437274 0.675978 0.785465 Overlapping Template Matchings'
        groups = parse_line(line)
        self.assertEqual('Overlapping Template Matchings', groups[13])

        line = '  1   9   12   125 467   505   11   6   456   87456  0.437274  0.675978 0.785465 Universal Statistical'
        groups = parse_line(line)
        self.assertEqual('Universal Statistical', groups[13])

        line = '  1   9   12   125 467 505 11 6 456 87456 0.437274  0.675978 0.785465 Approximate Entropy'
        groups = parse_line(line)
        self.assertEqual('Approximate Entropy', groups[13])

        line = '  1   9   12   125 467   505   11   6   456   87456  0.437274    0.675978   0.785465 Random Excursions'
        groups = parse_line(line)
        self.assertEqual('Random Excursions', groups[13])

        line = '  1   9   12   125 467  505 11 6 456 87456 0.437274  0.675978 0.785465 Random Excursions Variant'
        groups = parse_line(line)
        self.assertEqual('Random Excursions Variant', groups[13])

        line = '  1   9   12   125 467   505   11   6   456   87456  0.437274    0.675978   0.785465 Serial'
        groups = parse_line(line)
        self.assertEqual('Serial', groups[13])

        line = '  1   9   12   125 467   505   11   6   456   87456  0.437274    0.675978   0.785465 Linear Complexity'
        groups = parse_line(line)
        self.assertEqual('Linear Complexity', groups[13])

    def test_parse_lines_ret_none(self):
        line = '  1   9   12   125 45a   505   11   6   456   87456  0.437274    0.675978   0.785465    BlockFrequency'
        groups = parse_line(line)
        self.assertIsNone(groups)

        line = '  1   9   12   125 45 505  11  6  456   87456  0.437274    0.675978   0.785465 Block Fr equ ency'
        groups = parse_line(line)
        self.assertIsNone(groups)

    @patch('pdf_generating.report_to_latex.escape_latex_special_chars', side_effect=lambda x: x)
    def test_get_header(self, f_escape):
        content = ['line 1', 'line 2', 'line 3', 'line 4', 'line 5', 'line 6', 'line 7', 'line 8']
        end_line = r'\\' + '\n'
        expected = ''
        for l in content[:5]:
            expected += l
            expected += end_line
        ret = get_header(content)
        self.assertEqual(expected, ret)
        calls = [call('line 1'), call('line 2'), call('line 3'), call('line 4'), call('line 5')]
        f_escape.assert_has_calls(calls)

    def test_get_begin_of_table(self):
        expected = r'\hskip-0.7cm\begin{tabular}{llllllllllllll}' + '\n' \
                   + r'C1 & C2 & C3 & C4 & C5 & C6 & C7 & C8 & C9 & C10 & p-value & p (KS) & prop & test\\ \hline'
        ret = get_begin_of_table()
        self.assertEqual(expected, ret)

    def test_get_end_of_table(self):
        expected = r'\end{tabular}' + '\n'
        ret = get_end_of_table()
        self.assertEqual(expected, ret)

    @patch('pdf_generating.report_to_latex.parse_line', return_value=None)
    def test_get_latex_line_raises(self, f_parse):
        with self.assertRaises(RuntimeError) as ex:
            get_latex_line('some line', None)
        self.assertEqual('Wrong format of line: "some line"', str(ex.exception))
        calls = [call('some line')]
        f_parse.assert_has_calls(calls)

    @patch('pdf_generating.report_to_latex.parse_line', return_value=['0', '45', '0.0456', 'Text'])
    def test_get_latex_line(self, f_parse):
        expected = '0 & 45 & 0.0456 & Replaced text'
