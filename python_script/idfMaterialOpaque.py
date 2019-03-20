import os

# get the opaque surface information of models from idf  
def idfMaterialOpaque(model_source,prototype,climate_city,vintage,gem_version,path,construction):
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
    
    os.chdir(path_source + '/' + folder)
    path_idf = os.getcwd()
    files = os.listdir(path_idf)
    
    # find the target idf file
    for x in files:
        if '.idf' in x:
            idf_file = x
    
    # read the lines in idf
    f = open(idf_file,'rb')
    lines = f.readlines()
    f.close()
    
    # get the layers for construction
    for i in range(len(lines)):
        if lines[i].split(',')[0].lower().replace(' ','') == 'construction':
            if lines[i+1].split(',')[0].lower().replace(' ','') == construction.lower().replace(' ',''):
                start = i+2
                for k in range(i+2,i+10):
                    if ';' in lines[k]:
                        end = k
                        break
                break
    layers = []
    for i in range(start,end):
        layers.append(lines[i].split(',')[0].lower().replace(' ',''))
    layers.append(lines[end].split(';')[0].lower().replace(' ',''))
    
    # get the information of each layer
    material = ['roughness','thickness','conductivity','density','specificheat','thermalabsorptance',
                'solarabsorptance','visibleabsorptance']
    materialnomass = ['roughness','thermalresistance','thermalabsorptance','solarabsorptance',
                      'visibleabsorptance']
    
    idf_opaque = [construction]
    for layer in layers:
        temp = layer
        for i in range(len(lines)):
            if lines[i].split(',')[0].lower().replace(' ','') == 'material':
                if lines[i+1].split(',')[0].lower().replace(' ','') == layer:
                    for x in material:
                        temp += ','
                        for m in range(i+2,i+10):
                            if x in lines[m].lower().replace(' ',''):
                                if ',' in lines[m]:
                                    temp += lines[m].split(',')[0].lower().replace(' ','')
                                else:
                                    temp += lines[m].split(';')[0].lower().replace(' ','')
                                break
            elif lines[i].split(',')[0].lower().replace(' ','') == 'material:nomass':
                if lines[i+1].split(',')[0].lower().replace(' ','') == layer:
                    for x in materialnomass:
                        temp += ','
                        for m in range(i+2,i+10):
                            if x in lines[m].lower().replace(' ',''):
                                if ',' in lines[m]:
                                    temp += lines[m].split(',')[0].lower().replace(' ','')
                                else:
                                    temp += lines[m].split(';')[0].lower().replace(' ','')
                                break
        idf_opaque.append(temp)

    return idf_opaque

