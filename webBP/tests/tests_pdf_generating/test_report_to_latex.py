from configparser import ConfigParser
from os import makedirs
from shutil import rmtree, copy2

from os.path import dirname, abspath, join, exists
from unittest import TestCase
from unittest.mock import patch, call, MagicMock

from enums.nist_test_type import NistTestType
from pdf_generating.report_to_latex import parse_line, get_header, get_begin_of_table, get_end_of_table, get_latex_line, \
    get_test_type_from_name, get_shorten_test_name, convert_report_to_latex

this_dir = dirname(abspath(__file__))
working_dir = abspath(join(this_dir, 'working_report_to_latex'))
sample_files_dir = abspath(join(this_dir, '..', 'sample_files_for_tests'))


class TestReportToLatex(TestCase):
    tests_dict = {
        'Freq': 'FrequencyT', 'BFreq': 'Block FrequencyT', 'CuSums': 'Cumulative SumsT', 'Runs': 'RunsT',
        'LongRun': 'Longest RunT', 'Rank': 'RankT', 'FFT': 'FFTT', 'Nonperiodic': 'Nonperiodic Template MatchT',
        'Overlapping': 'Overlapping Template MatchingsT', 'Universal': 'Universal StatisticalT',
        'Approx': 'Approximate EntropyT', 'RandExcs': 'Random ExcursionsT',
        'RandExcsVar': 'Random Excursions VariantT', 'Serial': 'SerialT', 'Linear': 'LinearT'
    }

    def setUp(self):
        if not exists(working_dir):
            makedirs(working_dir)

    def tearDown(self):
        if exists(working_dir):
            rmtree(working_dir)

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
        tests_dict = TestReportToLatex.tests_dict
        data = {'ShortNames': tests_dict}
        cfg = ConfigParser()
        cfg.read_dict(data)

        test_name = get_shorten_test_name(NistTestType.TEST_FREQUENCY, cfg)
        self.assertEqual(tests_dict['Freq'], test_name)

        test_name = get_shorten_test_name(NistTestType.TEST_BLOCK_FREQUENCY, cfg)
        self.assertEqual(tests_dict['BFreq'], test_name)

        test_name = get_shorten_test_name(NistTestType.TEST_CUSUM, cfg)
        self.assertEqual(tests_dict['CuSums'], test_name)

        test_name = get_shorten_test_name(NistTestType.TEST_RUNS, cfg)
        self.assertEqual(tests_dict['Runs'], test_name)

        test_name = get_shorten_test_name(NistTestType.TEST_LONGEST_RUN, cfg)
        self.assertEqual(tests_dict['LongRun'], test_name)

        test_name = get_shorten_test_name(NistTestType.TEST_RANK, cfg)
        self.assertEqual(tests_dict['Rank'], test_name)

        test_name = get_shorten_test_name(NistTestType.TEST_FFT, cfg)
        self.assertEqual(tests_dict['FFT'], test_name)

        test_name = get_shorten_test_name(NistTestType.TEST_NONPERIODIC, cfg)
        self.assertEqual(tests_dict['Nonperiodic'], test_name)

        test_name = get_shorten_test_name(NistTestType.TEST_OVERLAPPING, cfg)
        self.assertEqual(tests_dict['Overlapping'], test_name)

        test_name = get_shorten_test_name(NistTestType.TEST_UNIVERSAL, cfg)
        self.assertEqual(tests_dict['Universal'], test_name)

        test_name = get_shorten_test_name(NistTestType.TEST_APEN, cfg)
        self.assertEqual(tests_dict['Approx'], test_name)

        test_name = get_shorten_test_name(NistTestType.TEST_RND_EXCURSION, cfg)
        self.assertEqual(tests_dict['RandExcs'], test_name)

        test_name = get_shorten_test_name(NistTestType.TEST_RND_EXCURSION_VAR, cfg)
        self.assertEqual(tests_dict['RandExcsVar'], test_name)

        test_name = get_shorten_test_name(NistTestType.TEST_SERIAL, cfg)
        self.assertEqual(tests_dict['Serial'], test_name)

        test_name = get_shorten_test_name(NistTestType.TEST_LINEARCOMPLEXITY, cfg)
        self.assertEqual(tests_dict['Linear'], test_name)

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

    def test_parse_line_asterisks(self):
        line = '  1   9   12   125 467   505   11   6   456   87456  0.437274 *   0.675978   0.785465 Frequency'
        groups = parse_line(line)
        self.assertEqual('0.437274 *', groups[10])

        line = '  1   9   12   125 467   505   11   6   456   87456  0.437274    0.675978   *  0.785465 Frequency'
        groups = parse_line(line)
        self.assertEqual('0.675978   *', groups[11])

        line = '  1   9   12   125 467   505   11   6   456   87456  0.437274    0.675978 0.785465   * Frequency'
        groups = parse_line(line)
        self.assertEqual('0.785465   *', groups[12])

        line = '  1   9   12   125 4567   505   11   6   456   87456  0.437274 * 0.675978 * 0.785465 * Frequency'
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
        self.assertEqual('0.437274 *', groups[10])
        self.assertEqual('0.675978 *', groups[11])
        self.assertEqual('0.785465 *', groups[12])
        self.assertEqual('Frequency', groups[13])

    def test_parse_lines_ret_none(self):
        line = '  1   9   12   125 45a   505   11   6   456   87456  0.437274    0.675978   0.785465    BlockFrequency'
        groups = parse_line(line)
        self.assertIsNone(groups)

        line = '  1   9   12   125 45 505  11  6  456   87456  0.437274    0.675978   0.785465 Block Fr equ e ncy'
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
                   + r'C1 & C2 & C3 & C4 & C5 & C6 & C7 & C8 & C9 & C10 & p-value & p (KS) & prop & test\\ \hline' \
                   + '\n'
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

    @patch('pdf_generating.report_to_latex.get_test_type_from_name',
           side_effect=lambda x: 'Test type' if 'Text' else None)
    @patch('pdf_generating.report_to_latex.get_shorten_test_name',
           side_effect=lambda x, texts: 'Replaced text' if 'Test type' else None)
    @patch('pdf_generating.report_to_latex.parse_line', return_value=['0', '45', '0.0456', 'Text'])
    def test_get_latex_line(self, f_parse, f_get_shorten_name, f_get_test_type):
        expected = r'0 & 45 & 0.0456 & Replaced text\\'
        mck = MagicMock(some_id=456)
        ret = get_latex_line('some line', mck)
        self.assertEqual(expected, ret)
        f_parse.assert_called_once_with('some line')
        f_get_test_type.assert_called_once_with('Text')
        f_get_shorten_name.assert_called_once_with('Test type', mck)

    def test_convert_report_to_latex_raises_non_existing_file(self):
        non_existing_file = join(working_dir, 'non_existing_file')
        with self.assertRaises(RuntimeError) as ex:
            convert_report_to_latex(non_existing_file, MagicMock())
        self.assertEqual('Given path does not exist: "{}"'.format(non_existing_file), str(ex.exception))

    def test_convert_report_to_latex_raises_none_texts(self):
        report_file = join(working_dir, 'report_file')
        with open(report_file, 'w'):
            pass
        with self.assertRaises(RuntimeError) as ex:
            convert_report_to_latex(report_file, None)
        self.assertEqual('Texts cannot be None', str(ex.exception))

    def test_convert_report_to_latex(self):
        report_path = join(sample_files_dir, 'sample_nist_report.txt')
        dst = join(working_dir, 'sample_nist_report.txt')
        copy2(report_path, dst)
        cfg = ConfigParser()
        data = {'ShortNames': TestReportToLatex.tests_dict}
        cfg.read_dict(data)
        ret = convert_report_to_latex(dst, cfg)
        exp = r'------------------------------------------------------------------------------\\' + '\n' \
              r'RESULTS FOR THE UNIFORMITY OF P-VALUES AND THE PROPORTION OF PASSING SEQUENCES\\' + '\n'  \
              r'------------------------------------------------------------------------------\\' + '\n'  \
              r'   generator is \textless data.sha1\textgreater \\' + '\n'  \
              r'------------------------------------------------------------------------------\\' + '\n'  \
              r'\hskip-0.7cm\begin{tabular}{llllllllllllll}' + '\n'  \
              r'C1 & C2 & C3 & C4 & C5 & C6 & C7 & C8 & C9 & C10 & p-value & p (KS) & prop & test\\ \hline' + '\n' \
              r'98 & 94 & 88 & 111 & 108 & 70 & 93 & 87 & 150 & 77 & 0.000001 * & 0.206107 & 0.9826 & FrequencyT\\' + '\n' \
              r'95 & 82 & 100 & 116 & 83 & 93 & 75 & 135 & 78 & 119 & 0.000027 * & 0.028351 & 0.9857 & Cumulative SumsT\\' + '\n' \
              r'99 & 91 & 101 & 87 & 100 & 97 & 97 & 127 & 84 & 93 & 0.167805 & 0.129834 & 0.9836 & Cumulative SumsT\\' + '\n' \
              r'\end{tabular}' + '\n\n\n'  \
              r'- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\\' + '\n' \
              r'The minimum pass rate for each statistical test with the exception of the\\' + '\n' \
              r'random excursion (variant) test is approximately = 0.980561 for a\\' + '\n' \
              r'sample size = 1000 binary sequences.\\' + '\n\n' \
              r'For further guidelines construct a probability table using the MAPLE program\\' + '\n' \
              r'provided in the addendum section of the documentation.\\' + '\n' \
              r'- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\\' + '\n'
        self.assertEqual(exp, ret)
