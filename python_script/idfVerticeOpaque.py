import os

# get the opaque surface information of models from idf  
def idfVerticeOpaque(model_source,prototype,climate_city,vintage,gem_version,path,opaque_surface):
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
    
    # identify the lines of the vertices
    for i in range(len(lines)):
        if lines[i].split(',')[0].replace(' ','').lower() == 'buildingsurface:detailed' or lines[i].split(',')[0].replace(' ','').lower() == 'fenestrationsurface:detailed':
            if lines[i+1].split(',')[0].replace(' ','').lower() == opaque_surface.replace(' ','').lower():
                vertices_id = []
                for m in range(i+2,i+30):
                    if 'Vertex' in lines[m]:
                        vertices_id.append(m)
                        if ';' in lines[m]:
                            break
                vertices_temp = []
                for n in range(len(vertices_id)/3):
                    temp = []
                    for t in vertices_id:
                        if ' '+str(n+1)+' ' in lines[t] and 'Xcoordinate' in lines[t]:
                            temp.append(lines[t].split(',')[0].replace(' ',''))
                    for t in vertices_id:
                        if ' '+str(n+1)+' ' in lines[t] and 'Ycoordinate' in lines[t]:
                            temp.append(lines[t].split(',')[0].replace(' ',''))
                    for t in vertices_id:
                        if ' '+str(n+1)+' ' in lines[t] and 'Zcoordinate' in lines[t]:
                            if ';' in lines[t]:
                                temp.append(lines[t].split(';')[0].replace(' ',''))
                            else:
                                temp.append(lines[t].split(',')[0].replace(' ',''))
                    vertices_temp.append(temp)
                break
    
    # adjust the sequence of the vertices
    Xmin = 1000000.0
    id_start = range(len(vertices_temp))
    id_start.reverse()
    for i in id_start:
        if float(vertices_temp[i][0]) < Xmin:
            Xmin = float(vertices_temp[i][0])
    remove_id = []
    for i in id_start:
        if float(vertices_temp[i][0]) > Xmin:
            remove_id.append(i)
    for i in remove_id:
        id_start.remove(i)
    if len(id_start) > 1:
        Ymin = 1000000.0
        for i in id_start:
            if float(vertices_temp[i][1]) < Ymin:
                Ymin = float(vertices_temp[i][1])
        remove_id = []
        for i in id_start:
            if float(vertices_temp[i][1]) > Ymin:
                remove_id.append(i)
        for i in remove_id:
            id_start.remove(i)
    if len(id_start) > 1:
        Zmin = 1000000.0
        for i in id_start:
            if float(vertices_temp[i][2]) < Zmin:
                Zmin = float(vertices_temp[i][2])
        remove_id = []
        for i in id_start:
            if float(vertices_temp[i][2]) > Zmin:
                remove_id.append(i)
        for i in remove_id:
            id_start.remove(i)
    
    if id_start[0] == 0:
        vertices = vertices_temp
    else:
        vertices = []
        for i in range(id_start[0],len(vertices_temp)):
            vertices.append(vertices_temp[i])
        for i in range(id_start[0]):
            vertices.append(vertices_temp[i])
    
    return vertices
    