from unittest import TestCase

from pdf_generating.report_to_latex import parse_line


class TestReportToLatex(TestCase):
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

    def test_parse_lines_ret_none(self):
        line = '  1   9   12   125 45a   505   11   6   456   87456  0.437274    0.675978   0.785465    BlockFrequency'
        groups = parse_line(line)
        self.assertIsNone(groups)

        line = '  1   9   12   125 45 505  11  6  456   87456  0.437274    0.675978   0.785465 Block Fr equ ency'
        groups = parse_line(line)
        self.assertIsNone(groups)

    def test_get_header(self):
        content = ['line 1', 'line 2', 'line 3', 'line 4', 'line 5', 'line 6', 'line 7', 'line 8']
