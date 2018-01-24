import os
import pandas as pd

# Take 3 paths and create an internal database of dicoms and contours 

class DicomContourMatcher(object):
    """ Cross reference file names and find the right dataset."""
    def __init__(self, dicom_path, contour_path, link_file_path):
        self.dicom_path = dicom_path
        self.contour_path = contour_path
        self.link_file_path = link_file_path

    def process_data(self):
        """Returns a list of all image/contour file paths that match. 
        """
        patients = self._get_all_filenames(self.dicom_path)
        links = pd.read_csv(self.link_file_path, index_col = 0)

        all_entries = []
        for patient in patients:
            patient_entries = self._parse_patient(patient, links)
            all_entries.extend(patient_entries)

        return all_entries 

    def _get_all_filenames(self, path):
        """
        Ignores hidden files while returning filenames in a directory
        """

        list_of_files = os.listdir(path)
        for idx, file in enumerate(list_of_files):
            if file.startswith('.'):
                del list_of_files[idx]

        return list_of_files

    def _number_to_filename(self, n, folder, type_of_file):
        # type_of_file should have been an enum. 
        if type_of_file == 'contour':  
            filename = os.path.join(self.contour_path, folder, 'i-contours', 'IM-0001-{}-icontour-manual'.format(str(n).zfill(4)) + ".txt")     
    
        if type_of_file == 'dicom':
            filename = os.path.join(self.dicom_path, folder, str(n) + ".dcm")
    
        return filename

    def _parse_patient(self, patient, links):
        """Matches per patient
        """
        corresponding_contour = links.get_value(patient, 'original_id')
        path = os.path.join(self.contour_path, corresponding_contour, 'i-contours')
        all_contour_filenames = self._get_all_filenames(path)
        #Extract Integers
        contour_file_numbers = set(map(lambda x: int(x[8:12]), all_contour_filenames))

    
        path = os.path.join(self.dicom_path, patient) 
        all_dicom_filenames = self._get_all_filenames(path)
        #Extract Integers
        dicom_file_numbers = set(map(lambda x: int(x.split('.')[0]), all_dicom_filenames))

        #Set Intersection to find dicom files that have corresponding contour files and vice versa
        all_entries = []
        common_file_numbers = contour_file_numbers.intersection(dicom_file_numbers)
        for item in common_file_numbers:
            new_entry = (self._number_to_filename(item, patient, 'dicom'), self._number_to_filename(item, corresponding_contour, 'contour'))
            all_entries.append(new_entry)

        return all_entries



        
