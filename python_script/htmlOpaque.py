import os
import pandas as pd

# get the opaque surface information of models from html  
def htmlOpaque(model_source,prototype,climate_city,vintage,gem_version,path):
    if model_source == 'PNNL':
        os.chdir(path + '\\PNNL')
    else:
        os.chdir(path + '\\OpenStudio_Standards')
    path_source = os.getcwd()
    folders = os.listdir(path_source)
    
    # find the target folder
    for x in folders:
        if prototype in x and climate_city in x and vintage in x:
            if model_source == 'PNNL':
                folder = x
            else:
                if gem_version in x:
                    folder = x
    
    os.chdir(path_source + '\\' + folder)
    path_html = os.getcwd()
    files = os.listdir(path_html)
    
    # find the target html file
    for x in files:
        if '.htm' in x:
            html_file = x
    
    # read all the table in html
    data = pd.read_html('./'+html_file)
    
    # get the tables, "Opaque Exterior" and "Exterior Door"
    opaque_exterior = []
    exterior_door = []
    for x in data:
        k = 0
        m = 0
        for i in range(1,len(x.columns)):
            if 'Construction' in str(x[i][0]):
                k += 1
                m += 1
            if 'U-Factor with Film [W/m2-K]' in str(x[i][0]):
                k += 1
                m += 1
            if 'Cardinal Direction' in str(x[i][0]):
                k += 1
            if 'Parent Surface' in str(x[i][0]):
                m += 1
        if k == 3:
            opaque_exterior = x
        if m == 3:
            exterior_door = x

    return opaque_exterior,exterior_door
