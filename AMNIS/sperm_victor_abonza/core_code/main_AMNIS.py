from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
from . import util
from .Preprocess.preprocess import preprocess_image
import re


def histogram_sizes_images(folder_images):
    file_names = [item.name for item in Path(folder_images).iterdir() if ((item.is_file() & (item.suffix=='.tif') | (item.suffix=='.tiff')))]
    
    height_list = []
    width_list = []
    
    for file_name in file_names:
        #reading image
        img = util.imread(Path(folder_images, file_name))
        
        height_list.append(img.shape[0])
        width_list.append(img.shape[1])
    
    
    plt.subplot(1,2,1)
    plt.hist(width_list, bins=30, rwidth=.95)
    plt.title('Width histogram')
    plt.subplot(1,2,2)
    plt.hist(height_list, rwidth=.95, bins=30)
    plt.title('Height histogram')
    
def convert_amnis_to_single_tif_file(folder_input_imgs_campo_claro, folder_input_imgs_fluorescence, folder_output, img_shape): 
    folder_output_input = Path(folder_output, 'imgs')
    
    util.create_file_in_case_not_exist(folder_output_input) 
        
    #Output image // Visually obtained using the histogram of width and height of all the images
    output_img_shape = np.array(img_shape)
    
    input_files = [item.name for item in Path(folder_input_imgs_campo_claro).iterdir() if ((item.is_file() & (item.suffix=='.tif') | (item.suffix=='.tiff')))]   
    
    n_files = len(input_files)
    for index, file_name in enumerate(input_files):
        print('Running file: ' + str(index+1) + '/' + str(n_files))
        #reading target images image
        print(file_name)
        
        #writing_image, make sure mask name is the same as input_image
        index = file_name.lower().find('ch')
        output_name = file_name[0:index]  +'.tif'
    
        #reading input images to create a 2 channel images of shape [2, width, height]
        file_name_brightfield = file_name
        img_campo_claro = util.imread(Path(folder_input_imgs_campo_claro, file_name_brightfield))
        img_campo_claro = preprocess_image(img_campo_claro, percentile_range=[1,99], normalization_range=[0,1])
        img_campo_claro = img_campo_claro.squeeze(0)        
        img_campo_claro = convert_img_to_shape(img_campo_claro, output_img_shape)
        
        
        file_name_fluorescence = file_name.replace("Campo claro", "Fluorescencia").replace("Ch1","Ch5")
        img_fluorescence = util.imread(Path(folder_input_imgs_fluorescence, file_name_fluorescence))
        img_fluorescence = preprocess_image(img_fluorescence, percentile_range=[1,99], normalization_range=[0,1])
        img_fluorescence = img_fluorescence.squeeze(0)        
        img_fluorescence = convert_img_to_shape(img_fluorescence, output_img_shape)
        
        img_input = np.zeros((2,img_campo_claro.shape[0],img_campo_claro.shape[1]), dtype = img_campo_claro.dtype)
        img_input[0,:,:] = img_campo_claro
        img_input[1,:,:] = img_fluorescence
        
        util.imwrite(Path(folder_output_input, output_name), img_input)
        
    print('------------------------------')
    print('\033[47m' '\033[1m' 'Algorithm has finished generating training set.' '\033[0m')
    print('------------------------------')  
    print('\nTraining set saved in path: ')
    print(folder_output)
    print('\n')        
    return    
    
def create_training_set(folder_input_imgs_campo_claro, 
                        folder_input_imgs_fluorescence, 
                        folder_target_cabeza, 
                        folder_target_flagelo, 
                        folder_output, output_img_shape,
                        folder_input_NO_MASK_brightfield = '',
                        folder_input_NO_MASK_fluorescence = ''):
   
    folder_output_input = Path(folder_output, 'input')
    folder_output_target = Path(folder_output, 'target')
    
    util.create_file_in_case_not_exist(folder_output_input)
    util.create_file_in_case_not_exist(folder_output_target)
       
    
    #Output image // Visually obtained using the histogram of width and height of all the images
    output_img_shape = np.array(output_img_shape)
    
    

    print('------------------------------')
    print('\033[47m' '\033[1m' 'GENERATING TRAINING SET FOR IMAGES WITH MASK' '\033[0m')
    print('------------------------------')    
    n_training_images = create_and_save_training_image(folder_input_imgs_campo_claro, 
                                                      folder_input_imgs_fluorescence,
                                                      folder_output_input,
                                                      folder_target_cabeza,
                                                      folder_target_flagelo,
                                                      folder_output_target,
                                                      output_img_shape,
                                                      0)                
    
    print('------------------------------')
    print('\033[47m' '\033[1m' 'GENERATING TRAINING SET FOR IMAGES WITHOUT MASK (OUT OF FOCUS)' '\033[0m')
    print('------------------------------')      
        
    create_and_save_training_image(folder_input_NO_MASK_brightfield, 
                                   folder_input_NO_MASK_fluorescence,
                                   folder_output_input,
                                   '',
                                   '',
                                   folder_output_target,
                                   output_img_shape,
                                   n_training_images)       

    
    print('------------------------------')
    print('\033[47m' '\033[1m' 'Algorithm has finished generating training set.' '\033[0m')
    print('------------------------------')  
    print('\nTraining set saved in path: ')
    print(folder_output)
    print('\n')        
    return

def create_and_save_training_image(folder_brightfield, 
                                   folder_fluorescence,
                                   folder_output_input,
                                   folder_mask_head,
                                   folder_mask_flagellum,
                                   folder_output_target,
                                   output_img_shape,
                                   index_shift):
    
    #verify each file has been correctly save in each file
    verify_file_name_in_each_folder(folder_brightfield, 
                                    folder_fluorescence, 
                                    folder_mask_head, 
                                    folder_mask_flagellum)  
    
    input_files = [item.name for item in Path(folder_brightfield).iterdir() if ((item.is_file() & (item.suffix=='.tif') | (item.suffix=='.tiff')))]   
    n_files = len(input_files)
    for num_id, file_name in enumerate(input_files):
        print('Running file: ' + str(num_id+1) + '/' + str(n_files))
        #reading target images image
        print(file_name)    
        #writing_image, make sure mask name is the same as input_image
        index = file_name.lower().find('ch')
        output_name = 'img_' + str(index_shift + num_id).zfill(5) + '_' + file_name[0:index] +  '.tif'    
        
        # Creating input image to create a 2 channel images of shape [2, width, height]
        file_name_brightfield = get_corresponding_file_in_folder(folder_brightfield, file_name)[0]
        img_campo_claro = util.imread(Path(folder_brightfield, file_name_brightfield))
        img_campo_claro = preprocess_image(img_campo_claro, percentile_range=[1,99], normalization_range=[0,1])
        img_campo_claro = img_campo_claro.squeeze(0)
        img_campo_claro = convert_img_to_shape(img_campo_claro, output_img_shape)
        
        file_name_fluorescence = get_corresponding_file_in_folder(folder_fluorescence, file_name)[0]
        img_fluorescence = util.imread(Path(folder_fluorescence, file_name_fluorescence))
        img_fluorescence = preprocess_image(img_fluorescence, percentile_range=[1,99], normalization_range=[0,1])
        img_fluorescence = img_fluorescence.squeeze(0)
        img_fluorescence = convert_img_to_shape(img_fluorescence, output_img_shape)
        
        img_input = np.zeros((2,img_campo_claro.shape[0],img_campo_claro.shape[1]), dtype = img_campo_claro.dtype)    
        img_input[0,:,:] = img_campo_claro
        img_input[1,:,:] = img_fluorescence
        util.imwrite(Path(folder_output_input, output_name), img_input)         
        
        
        output = np.zeros((2, output_img_shape[0], output_img_shape[1]), dtype = np.uint8)
        if folder_mask_head and folder_mask_flagellum:            
            file_name_head = get_corresponding_file_in_folder(folder_mask_head, file_name)[0]
            img_cabeza = util.imread(Path(folder_mask_head, file_name_head))
            
            file_name_flagellum = get_corresponding_file_in_folder(folder_mask_flagellum, file_name)[0]
            img_flagelo = util.imread(Path(folder_mask_flagellum, file_name_flagellum))
            
            #converting to binary
            img_cabeza = img_cabeza> 0
            img_flagelo = img_flagelo>0
            
            img_cabeza_filled_holes = ndimage.binary_fill_holes(img_cabeza) * (1-img_flagelo)
            
            
            output[0,:,:] = convert_img_to_shape(img_cabeza_filled_holes, output_img_shape)
            output[1,:,:] = convert_img_to_shape(img_flagelo, output_img_shape)
        
        util.imwrite(Path(folder_output_target, output_name), output.astype(np.uint8))
    return len(input_files)

def convert_img_to_shape(img, new_shape):
    old_shape = img.shape
    
    temp_shape = np.maximum(old_shape,new_shape)
    
    new_img = np.zeros(temp_shape)
    
    new_img[0:old_shape[0], 0:old_shape[1]] = img
    
    return new_img[0:new_shape[0], 0:new_shape[1]]

def verify_file_name_in_each_folder(folder_brightfield, folder_fluorescence, folder_head, folder_flagellum):
    for item in Path(folder_brightfield).iterdir():
        if item.is_file() and item.suffix in ('.tif', '.tiff'):
            file_name = str(item.name)
            for folder_path in [folder_fluorescence, folder_head, folder_flagellum]:
                if folder_path:
                    file_id = get_corresponding_file_in_folder(folder_path, file_name)
                    if not file_id or len(file_id) > 1:
                        print(f"output_corresponding_file_in_folder: {file_id}")
                        raise Exception(f"No file identified for {file_name} -- {folder_path}")

def get_corresponding_file_in_folder(folder_path, file_name):
    index = file_name.lower().find('ch')
    file_base = file_name[0:index] + '*'
    file_base = re.sub(r"\s+", '*', file_base)
    return list(Path(folder_path).glob(file_base)) if index >= 0 else None