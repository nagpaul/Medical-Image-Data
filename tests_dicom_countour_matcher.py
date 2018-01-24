import unittest

import dicom_contour_matcher


class DicomContourMatcherTests(unittest.TestCase):
    def setUp(self):
        dicom_path = "./final_data/dicoms"
        contour_path = "./final_data/contourfiles"
        link_file_path = "./final_data/link.csv"
        self.dcm = dicom_contour_matcher.DicomContourMatcher(dicom_path, contour_path, link_file_path)

    def test_process_data(self):
        all_entries = self.dcm.process_data()
        assert len(all_entries) == 96


if __name__ == '__main__':
    unittest.main()