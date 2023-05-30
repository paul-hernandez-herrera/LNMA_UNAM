import ipywidgets as widgets
from IPython.display import display


def parameters_amnis_to_tif():
    print('------------------------------')
    print('\033[47m' '\033[1m' 'REQUIRED PARAMETERS' '\033[0m')
    print('------------------------------')

    folder_input_campoclaro_w = set_parameter_text('Folder images - brightfield: ', 'Insert path here')
    folder_input_fluorescence_w = set_parameter_text('Folder images - fluorescence: ', 'Insert path here')
    folder_output_w = set_parameter_text('Folder output: ', 'Insert path here')


    parameters = {'folder_brightfield' : folder_input_campoclaro_w,
                  'folder_fluorescence' : folder_input_fluorescence_w,
                  'folder_output' : folder_output_w
                  }
    
    return parameters

def parameters_training_images():
    print('------------------------------')
    print('\033[47m' '\033[1m' 'REQUIRED PARAMETERS' '\033[0m')
    print('------------------------------')

    folder_input_w = set_parameter_text('Folder path input images:', 'Insert path here')   
    folder_target_w = set_parameter_text('Folder path target mask:', 'Insert path here')


    parameters = {'folder_input_w' : folder_input_w,
                  'folder_target_w' : folder_target_w
                  }
    
    return parameters

def parameters_create_training_set():
    print('------------------------------')
    print('\033[47m' '\033[1m' 'FOLDER IMAGES WITH MASK: ' '\033[0m')
    folder_input_campoclaro_w = set_parameter_text('brightfield: ', 'Insert path here')
    folder_input_fluorescence_w = set_parameter_text('fluorescence: ', 'Insert path here')
    print('\033[47m' '\033[1m' 'FOLDER MASKS: ' '\033[0m')
    folder_target_head_w = set_parameter_text('Head: ', 'Insert path here')
    folder_target_flagellum_w = set_parameter_text('Flagellum: ', 'Insert path here')
    print('------------------------------')
    print('------------------------------')
    print('\033[47m' '\033[1m' 'FOLDER IMAGES WITHOUT MASK - OUT OF FOCUS(OPTIONAL): ' '\033[0m')   
    folder_input_no_mask_campoclaro_w = set_parameter_text('brightfield: ', 'Insert path here')
    folder_input_no_mask_fluorescence_w = set_parameter_text('fluorescence: ', 'Insert path here')    
    print('------------------------------')
    print('\033[47m' '\033[1m' 'OUTPUT TRAINING SET: ' '\033[0m')       
    
    folder_output_w = set_parameter_text('Folder output: ', 'Insert path here')
    
    parameters = {'folder_input_campoclaro_w' : folder_input_campoclaro_w,
                  'folder_input_fluorescence_w' : folder_input_fluorescence_w,
                  'folder_target_head_w' : folder_target_head_w,
                  'folder_target_flagellum_w' : folder_target_flagellum_w,
                  'folder_no_mask_brightfield': folder_input_no_mask_campoclaro_w,
                  'folder_no_mask_fluorescence': folder_input_no_mask_fluorescence_w,                  
                  'folder_output_w' : folder_output_w
                  }    
    
    return parameters

def parameters_unet_model():
    print('------------------------------')
    print('\033[47m' '\033[1m' 'REQUIRED PARAMETERS' '\033[0m')
    print('------------------------------')

    n_channels_input = set_parameter_Int('#channels for input image: ', 0)
    n_channels_target = set_parameter_Int('#channels for target image ', 0)
    
    return []

def set_parameter_intSlider(string_name, low_val, high_val):
    widget_intSlider = widgets.IntRangeSlider(
        value=[low_val, high_val],
        min=0,
        max=100,
        step=1,
        description=string_name,
        disabled=False,
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='d',
        layout=widgets.Layout(flex='1 1 auto', width='auto')
    )
    display(widget_intSlider)
    return widget_intSlider

def set_parameter_text(string_name, string_default_val):
    widget_text = widgets.Text(
        value = '',
        placeholder = string_default_val,
        description= '',
        disable = False,
        layout=widgets.Layout(flex='1 1 auto', width='auto'))
    
    a = widgets.HBox([widgets.Label(string_name, layout=widgets.Layout( width='200px')),widget_text])
    display(a)
    return widget_text 

def set_parameter_Int(string_name, default_value):
    widget_int =widgets.IntText(
        value = default_value,
        description = '',
        disabled=False,
        layout=widgets.Layout(flex='1 1 auto', width='auto'))    
    
    a = widgets.HBox([widgets.Label(string_name, layout=widgets.Layout( width='200px')), widget_int])
    display(a)
    return widget_int 

def set_parameter_checkbox(string_name, default_value):
    widget_checkbox = widgets.Checkbox(
        value=default_value,
        description= string_name,
        disabled=False,
        indent=False,
    )
    display(widget_checkbox)
    return widget_checkbox     