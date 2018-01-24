# Dicom Images of Hearts and Contours


## Files
    - data_loader.py 
    - test_data_loader.py
    - dicom_contour_matcher.py 
    - test_dicom_contour_matcher.py

### What do they do? (and Usage)
    - data_loader.py containts the DataLoader class whose objects take in file paths to dicom and contourfiles directories and produce a dataset. 
        usage: 
            - dl = data_loader.DataLoader(dicom_path, contour_path, link_file_path)
            - X, Y = dl.load() # load takes an optional batch_size argument that only returns the specified number of datapoints if fewer are requested, otherwise it returns all. 
            - gen = dl.batch_generator(batch_size) gives a generator for random batches for each epoch. 

    - dicom_contour_matcher.py contains the functionality to cross reference file names to find matching ones and generate paths to image/ contour pairs. 
        useage:
            - dcm = dicom_contour_matcher.DicomContourMatcher(dicom_path, contour_path, link_file_path)
            - dcm.process_data() returns a list of tuples which pairs up file paths for images and contours. 


### How to run the unit-tests?
        - To test a file run: 
            python test_file.py

For more information, please refer to the write up(write_up.pdf) and jupyter notebook titled 'Exploratory Analysis'in the nbs folder (added 'final_data' folder to the home directory to run the notebook). 

Needs Python3 to run.
