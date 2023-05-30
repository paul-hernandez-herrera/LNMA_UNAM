from pathlib import Path
import matplotlib.pyplot as plt
import util

def main():
    folder_input = "/home/paul/Documents/Python/github/segmentation-UNet2D/data_AMNIS_sperm/training_set/Input/Campo_claro/"
    
    file_names = [item.name for item in Path(folder_input).iterdir() if ((item.is_file() & (item.suffix=='.tif') | (item.suffix=='.tiff')))]
    
    height_list = []
    width_list = []
    
    for file_name in file_names:
        #reading image
        img = util.imread(Path(folder_input, file_name))
        
        height_list.append(img.shape[0])
        width_list.append(img.shape[1])
    
    plt.subplot(1,2,1)
    plt.hist(height_list, density=True, bins=30)
    plt.title('Height histogram')
    plt.subplot(1,2,2)
    plt.hist(width_list, density=True, bins=30)
    plt.title('Width histogram')
    
if __name__ == '__main__':
    main()