import os
import htmlOpaque as html
import idfMaterialOpaque as mat
import idfVerticeOpaque as ver

def compareOpaqueSurface(osstd_prototype,climate,vintage,gem_version):
    # create a file to record the differences
    f = open('diff-'+osstd_prototype+'-'+climate+'-'+vintage+'-'+gem_version,'w')
    f.close()
    
    # get the information from the html
    model_sources = ['PNNL','OpenStudio_Standards']
    osstd_prototypes = ['FullServiceRestaurant','HighriseApartment','Hospital',
                        'LargeHotel','LargeOffice','MediumOffice','MidriseApartment',
                        'Outpatient','PrimarySchool','QuickServiceRestaurant',
                        'RetailStandalone','RetailStripmall','SecondarySchool',
                        'SmallHotel','SmallOffice','Warehouse']
    pnnl_prototypes = ['RestaurantSitDown','ApartmentHighRise','Hospital',
                       'HotelLarge','OfficeLarge','OfficeMedium','ApartmentMidRise',
                       'OutPatientHealthCare','SchoolPrimary','RestaurantFastFood',
                       'RetailStandalone','RetailStripmall','SchoolSecondary',
                       'HotelSmall','OfficeSmall','Warehouse']
    climates = ['1A','2A','2B','3A','3B','3C','4A','4B','4C','5A','5B','6A','6B','7A','8A']
    cities = ['Miami','Houston','Phoenix','Memphis','El_Paso','San_Francisco','Baltimore',
              'Albuquerque','Salem','Chicago','Boise','Burlington','Helena','Duluth','Fairbanks']
    os.chdir('..')
    path = os.getcwd()
    opaque_exterior_pnnl,exterior_door_pnnl = html.htmlOpaque(model_sources[0],pnnl_prototypes[osstd_prototypes.index(osstd_prototype)],
                                                              cities[climates.index(climate)],'STD'+vintage,'',path)
    opaque_exterior_osstd,exterior_door_osstd = html.htmlOpaque(model_sources[1],osstd_prototype,climate,'90.1-'+vintage,gem_version,path)
    
    # get the material information from the idf
    idf_material_pnnl = []
    for i in range(1,len(opaque_exterior_pnnl)):
        idf_material_pnnl.append(mat.idfMaterialOpaque(model_sources[0],pnnl_prototypes[osstd_prototypes.index(osstd_prototype)],
                                                       cities[climates.index(climate)],'STD'+vintage,'',path,opaque_exterior_pnnl[1][i]))
    if len(exterior_door_pnnl) > 0 and exterior_door_pnnl[0][1] != 'None':
        for i in range(1,len(exterior_door_pnnl)):
            idf_material_pnnl.append(mat.idfMaterialOpaque(model_sources[0],pnnl_prototypes[osstd_prototypes.index(osstd_prototype)],
                                                           cities[climates.index(climate)],'STD'+vintage,'',path,exterior_door_pnnl[1][i]))

    idf_material_osstd = []
    for i in range(1,len(opaque_exterior_osstd)):
        idf_material_osstd.append(mat.idfMaterialOpaque(model_sources[1],osstd_prototype,climate,'90.1-'+vintage,gem_version,path,
                                                        opaque_exterior_osstd[1][i]))
    if len(exterior_door_osstd) > 0 and exterior_door_osstd[0][1] != 'None':
        for i in range(1,len(exterior_door_osstd)):
            idf_material_osstd.append(mat.idfMaterialOpaque(model_sources[1],osstd_prototype,climate,'90.1-'+vintage,gem_version,path,
                                                            exterior_door_osstd[1][i]))

    # get the vertices information from the idf
    idf_vertex_pnnl = []
    idf_surface_pnnl = []
    for i in range(1,len(opaque_exterior_pnnl)):
        idf_surface_pnnl.append(opaque_exterior_pnnl[0][i])
        idf_vertex_pnnl.append(ver.idfVerticeOpaque(model_sources[0],pnnl_prototypes[osstd_prototypes.index(osstd_prototype)],
                                                    cities[climates.index(climate)],'STD'+vintage,'',path,opaque_exterior_pnnl[0][i]))
    if len(exterior_door_pnnl) > 0 and exterior_door_pnnl[0][1] != 'None':
        for i in range(1,len(exterior_door_pnnl)):
            idf_surface_pnnl.append(exterior_door_pnnl[0][i])
            idf_vertex_pnnl.append(ver.idfVerticeOpaque(model_sources[0],pnnl_prototypes[osstd_prototypes.index(osstd_prototype)],
                                                        cities[climates.index(climate)],'STD'+vintage,'',path,exterior_door_pnnl[0][i]))

    idf_vertex_osstd = []
    idf_surface_osstd = []
    for i in range(1,len(opaque_exterior_osstd)):
        idf_surface_osstd.append(opaque_exterior_osstd[0][i])
        idf_vertex_osstd.append(ver.idfVerticeOpaque(model_sources[1],osstd_prototype,climate,'90.1-'+vintage,gem_version,path,
                                                     opaque_exterior_osstd[0][i]))
    if len(exterior_door_osstd) > 0 and exterior_door_osstd[0][1] != 'None':
        for i in range(1,len(exterior_door_osstd)):
            idf_surface_osstd.append(exterior_door_osstd[0][i])
            idf_vertex_osstd.append(ver.idfVerticeOpaque(model_sources[1],osstd_prototype,climate,'90.1-'+vintage,gem_version,path,
                                                         exterior_door_osstd[0][i]))
    
    # comparison
    #1. identify the corresponding surfaces between two models
    rel_id_pnnl = []
    for i in range(len(idf_vertex_pnnl)):
        rel_id_pnnl.append(-1)
        
    rel_id_osstd = []
    for i in range(len(idf_vertex_osstd)):
        rel_id_osstd.append(-1)
        
    for ind_pnnl in range(len(idf_vertex_pnnl)):
        vertices_pnnl = idf_vertex_pnnl[ind_pnnl]
        for ind_osstd in range(len(idf_vertex_osstd)):
            vertices_osstd = idf_vertex_osstd[ind_osstd]
            k = 0
            if len(vertices_pnnl) == len(vertices_osstd):
                for i in range(len(vertices_pnnl)):
                    for j in range(3):
                        if abs(float(vertices_pnnl[i][j])-float(vertices_osstd[i][j])) < 0.01:
                            k += 1
                if k == len(vertices_pnnl)*3:
                    rel_id_pnnl[ind_pnnl] = ind_osstd
                    rel_id_osstd[ind_osstd] = ind_pnnl
        
    id_osstd_nofind = []
    for ind,x in enumerate(rel_id_osstd):
        if x == -1:
            id_osstd_nofind.append(ind)
    if len(id_osstd_nofind) > 0:
        for ind_osstd in id_osstd_nofind:
            vertices_osstd = idf_vertex_osstd[ind_osstd]
            for ind_pnnl in range(len(idf_vertex_pnnl)):
                vertices_pnnl = idf_vertex_pnnl[ind_pnnl]
                k = 0
                if len(vertices_pnnl) == len(vertices_osstd):
                    for i in range(len(vertices_pnnl)):
                        for j in range(3):
                            if abs(float(vertices_pnnl[i][j])-float(vertices_osstd[i][j])) < 0.01:
                                k += 1
                    if k == len(vertices_pnnl)*3:
                        rel_id_pnnl[ind_pnnl] = ind_osstd
                        rel_id_osstd[ind_osstd] = ind_pnnl
    
    # record the differences
    os.chdir(path+'\\python_script')
    for ind,x in enumerate(rel_id_pnnl):
        if x == -1:
            f = open('diff-'+osstd_prototype+'-'+climate+'-'+vintage+'-'+gem_version,'a')
            f.writelines('The surface, '+idf_surface_pnnl[ind]+', in PNNL model has no corresponding surfaces in OSSTD model.'+'\n')
            f.close()
    
    for ind,x in enumerate(rel_id_osstd):
        if x == -1:
            f = open('diff-'+osstd_prototype+'-'+climate+'-'+vintage+'-'+gem_version,'a')
            f.writelines('The surface, '+idf_surface_osstd[ind]+', in OSSTD model has no corresponding surfaces in PNNL model.'+'\n')
            f.close()
    
    #2. identify the differences of the number of the layers
    rel_id_pnnl_change = []
    for i in range(len(rel_id_pnnl)):
        if rel_id_pnnl[i] != -1:
            construction_id_pnnl = i
            construction_id_osstd = rel_id_pnnl[i]
            if len(idf_material_pnnl[construction_id_pnnl]) != len(idf_material_osstd[construction_id_osstd]):
                rel_id_pnnl_change.append(i)
                f = open('diff-'+osstd_prototype+'-'+climate+'-'+vintage+'-'+gem_version,'a')
                f.writelines('The construction, '+idf_material_pnnl[construction_id_pnnl][0]+', of surface,'+idf_surface_pnnl[construction_id_pnnl]
                             +', in PNNL model and the construction, '+idf_material_osstd[construction_id_osstd][0]+', of surface, '+idf_surface_osstd[construction_id_osstd]
                             +', in OSSTD model have different number of layers.'+'\n')
                f.close()
    for i in rel_id_pnnl_change:
        rel_id_pnnl[i] = -1
    
    #3. identify the differences of the paramters of the materials
    material = ['roughness','thickness','conductivity','density','specificheat','thermalabsorptance',
                'solarabsorptance','visibleabsorptance']
    materialnomass = ['roughness','thermalresistance','thermalabsorptance','solarabsorptance',
                      'visibleabsorptance']
    for i in range(len(rel_id_pnnl)):
        if rel_id_pnnl[i] != -1:
            construction_id_pnnl = i
            construction_id_osstd = rel_id_pnnl[i]
            for j in range(1,len(idf_material_pnnl[construction_id_pnnl])):
                layer_pnnl = []
                for x in idf_material_pnnl[construction_id_pnnl][j].split(',')[1:]:
                    layer_pnnl.append(x)
                layer_osstd = []
                for x in idf_material_osstd[construction_id_osstd][j].split(',')[1:]:
                    layer_osstd.append(x)
                if len(layer_pnnl) == len(material):
                    for m in range(len(layer_pnnl)):
                        if layer_pnnl[m] != layer_osstd[m]:
                            f = open('diff-'+osstd_prototype+'-'+climate+'-'+vintage+'-'+gem_version,'a')
                            f.writelines('The layer, '+idf_material_pnnl[construction_id_pnnl][j].split(',')[0]+', of construction, '+idf_material_pnnl[construction_id_pnnl][0]
                                         +', of surface, '+idf_surface_pnnl[construction_id_pnnl]+', in PNNL model and the layer, '
                                         +idf_material_osstd[construction_id_osstd][j].split(',')[0]+', of construction, '+idf_material_osstd[construction_id_osstd][0]
                                         +', of surface, '+idf_surface_osstd[construction_id_osstd]+', in OSSTD model have different values of '+material[m]
                                         +': PNNL: '+layer_pnnl[m]+', OSSTD: '+layer_osstd[m]+'.'+'\n')
                            f.close()
                else:
                    for m in range(len(layer_pnnl)):
                        if layer_pnnl[m] != layer_osstd[m]:
                            f = open('diff-'+osstd_prototype+'-'+climate+'-'+vintage+'-'+gem_version,'a')
                            f.writelines('The layer, '+idf_material_pnnl[construction_id_pnnl][j].split(',')[0]+', of construction, '+idf_material_pnnl[construction_id_pnnl][0]
                                         +', of surface, '+idf_surface_pnnl[construction_id_pnnl]+', in PNNL model and the layer, '
                                         +idf_material_osstd[construction_id_osstd][j].split(',')[0]+', of construction, '+idf_material_osstd[construction_id_osstd][0]
                                         +', of surface, '+idf_surface_osstd[construction_id_osstd]+', in OSSTD model have different values of '+materialnomass[m]
                                         +': PNNL: '+layer_pnnl[m]+', OSSTD: '+layer_osstd[m]+'.'+'\n')
                            f.close()
