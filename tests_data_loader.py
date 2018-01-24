import unittest

import data_loader


class DataLoaderTests(unittest.TestCase):
    def setUp(self):
        dicom_path = "./final_data/dicoms"
        contour_path = "./final_data/contourfiles"
        link_file_path = "./final_data/link.csv"
        self.dl = data_loader.DataLoader(dicom_path, contour_path, link_file_path)

    def test_load(self):
        img, msks = self.dl.load()
        assert len(img) == 96


    def test_batch_generator(self):
        batch_size = 8
        gen = self.dl.batch_generator(batch_size)        
        assert len(list(gen)[0][0]) == batch_size



if __name__ == '__main__':
    unittest.main()