import numpy as np
import os
import pandas as pd
import random
from parsing import *
from dicom_contour_matcher import *

np.random.seed(42)

class DataLoader(object):
    """docstring for DataLoader"""
    def __init__(self, dicom_path, contour_path, link_file_path):
        self.dicom_path = dicom_path
        self.contour_path = contour_path
        self.link_file_path = link_file_path
        self._get_data_from_matcher()


    def _get_data_from_matcher(self):
        dcm = DicomContourMatcher(self.dicom_path,self.contour_path, self.link_file_path)
        data_file_tuples = dcm.process_data()
        df = pd.DataFrame(columns = ['_dicom', "_contour"])
        df['_dicom'] = [x[0] for x in data_file_tuples]
        df['_contour'] = [x[1] for x in data_file_tuples]

        self.filepaths_df = df

    def batch_generator(self, batch_size, shuffle = True):
        """
            gen = batch_generator(5)
            for imgs,masks in gen:
            print(imgs.shape)
        """
        
        dataset_size = len(self.filepaths_df)
        list_of_indices = list(range(dataset_size))
        if shuffle==True:
            random.shuffle(list_of_indices)
        
        while (len(list_of_indices)>=batch_size):
            use_values = list_of_indices[:batch_size]
            del list_of_indices[:batch_size]
            batch_df = self.filepaths_df.iloc[use_values]
        
            images = [parse_dicom_file(f) for f in batch_df._dicom.values]
            contour_polys = [parse_contour_file(f) for f in batch_df._contour.values]
            masks = list(map(lambda x: poly_to_mask(x, 256, 256), contour_polys))

            masks = np.array(masks)
            images = np.array(images)
            yield (images, masks)

    def load(self, batch_size = -1, shuffle = False):

        if batch_size is -1:
            dataset_size = len(self.filepaths_df)
        else: 
            dataset_size = batch_size

        return self._load_batches(batch_size = dataset_size, shuffle = shuffle)


    def _load_batches(self, batch_size = 8, shuffle = False):
        gen = self.batch_generator(batch_size, shuffle)
        for img, msks in gen:
            return (img, msks)
            








