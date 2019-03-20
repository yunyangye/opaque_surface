import compareOpaqueSurface as comp

'''
osstd_prototypes = ['FullServiceRestaurant','HighriseApartment','Hospital',
                    'LargeHotel','LargeOffice','MediumOffice','MidriseApartment',
                    'Outpatient','PrimarySchool','QuickServiceRestaurant',
                    'RetailStandalone','RetailStripmall','SecondarySchool',
                    'SmallHotel','SmallOffice','Warehouse']
climates = ['1A','2A','2B','3A','3B','3C','4A','4B','4C','5A','5B','6A','6B','7A','8A']
vintages = ['2004','2007','2010','2013']
gem_versions = ['nrel_master','pnnl','nrel_master_base']
'''
# all the names are for OSSTD models
osstd_prototypes = ['SmallOffice']
climates = ['4A']
vintages = ['2013']
gem_versions = ['nrel_master']

for x in osstd_prototypes:
    for y in climates:
        for z in vintages:
            for k in gem_versions:
                comp.compareOpaqueSurface(x,y,z,k)

