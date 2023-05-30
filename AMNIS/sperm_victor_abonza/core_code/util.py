import tifffile
from pathlib import Path

def imread(filename):
    ext = Path(filename).suffix
    if ext== '.tif' or ext=='.tiff':
        return tifffile.imread(filename)
        
def imwrite(filename, arr):
    ext = Path(filename).suffix
    if ext== '.tif' or ext=='.tiff':
        tifffile.imsave(filename, arr) 
        
        
def get_image_file_names(file_path):
    file_path = Path(file_path)
    ext = file_path.suffix
    img_file_path = []
    if file_path.is_dir():
        img_file_path.extend(file_path.glob('*.tif'))
        img_file_path.extend(file_path.glob('*.tiff'))
    elif ext=='.tif' or ext=='.tiff':
        img_file_path = [file_path]
    else:
        raise ValueError('Input file format not recognized. Currently only tif files can be processed (.tif or .tiff)')
    return img_file_path   

def create_file_in_case_not_exist(folder_path):
    folder_path.mkdir(parents=True, exist_ok=True)
    return