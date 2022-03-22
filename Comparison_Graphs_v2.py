# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 14:51:52 2020

@author: jstreeck
"""

import numpy as np
import pandas as pd
import glob
import seaborn as sns
import matplotlib.pyplot as plt
import random
import os
import sys

main_path = os.getcwd()
module_path = os.path.join(main_path, 'modules')
sys.path.insert(0, module_path)
data_path_usa = os.path.join(main_path, 'output/USA/')
data_path_exio = os.path.join(main_path, 'output/Exiobase/')

'''
    #1 Load USA national tables
'''

years = [1963,1967,1972,1977,1982,1987,1992,1997,2002,2007,2012]

#1 read files for all methods and years into dictionaries

CBA_dict = {}
for year in years:
    for file in glob.glob(os.path.join((data_path_usa + 'CBA_' + str(year) + '_Base' + '*.xlsx'))):
        CBA_single = pd.read_excel(file, sheet_name='EndUse_shares_agg',index_col=[0,1],header=[0,1])
    CBA_dict[year] = CBA_single
    

Wio_dict = {}
for year in years:
    for file in glob.glob(os.path.join((data_path_usa + 'WIO_plain_' + str(year) + '_Base' + '*.xlsx'))):
        Wio_single = pd.read_excel(file, sheet_name='EndUse_shares_agg',index_col=[0,1],header=[0,1])
    Wio_dict[year] = Wio_single
    
Wio_ext_dict = {}
for year in years:
    for file in glob.glob(os.path.join((data_path_usa + 'WIO_plain_' + str(year) + '_ExtAgg' + '*.xlsx'))):
        Wio_single = pd.read_excel(file, sheet_name='EndUse_shares_agg',index_col=[0,1],header=[0,1])
    Wio_ext_dict[year] = Wio_single

Wio_withServiceInput_dict = {}
for year in years:
    for file in glob.glob(os.path.join((data_path_usa + 'WIO_withServiceInput_' + str(year) + '_Base' + '*.xlsx'))):
        Wio_single = pd.read_excel(file, sheet_name='EndUse_shares_agg',index_col=[0,1],header=[0,1])
    Wio_withServiceInput_dict[year] = Wio_single

Ghosh_dict = {}
for year in years:
    for file in glob.glob(os.path.join((data_path_usa + 'GhoshAMC_plain_' + str(year) + '_Base' + '*.xlsx'))):
        Ghosh_single = pd.read_excel(file, sheet_name='EndUse_shares_agg',index_col=[0,1],header=[0,1])
    Ghosh_dict[year] = Ghosh_single
    
ParGhosh_dict = {}
for year in years:
    for file in glob.glob(os.path.join((data_path_usa + 'PartialGhoshIO_plain_' + str(year) + '_Base' + '*.xlsx'))):
        ParGhosh_single = pd.read_excel(file, sheet_name='EndUse_shares_agg',index_col=[0,1],header=[0,1])
    ParGhosh_dict[year] = ParGhosh_single
    
HTWio_dict = {}
for year in years:
    for file in glob.glob(os.path.join((data_path_usa + 'HT_WIOMF_' + str(year) + '_Base' + '*.xlsx'))):
        HTWio_single = pd.read_excel(file, sheet_name='EndUse_shares_agg',index_col=[0,1],header=[0,1])
    HTWio_dict[year] = HTWio_single
    
HTWio_ext_dict = {}
for year in years:
    for file in glob.glob(os.path.join((data_path_usa + 'HT_WIOMF_' + str(year) + '_ExtAgg' + '*.xlsx'))):
        HTWio_single = pd.read_excel(file, sheet_name='EndUse_shares_agg',index_col=[0,1],header=[0,1])
    HTWio_ext_dict[year] = HTWio_single
    
HTWio_detail_dict = {}
for year in years:
    for file in glob.glob(os.path.join((data_path_usa + 'HT_WIOMF_' + str(year) + '_Base' + '*.xlsx'))):
        HTWio_detail_single = pd.read_excel(file, sheet_name='EndUse_shares',index_col=[0,1],header=[0,1])
    HTWio_detail_dict[year] = HTWio_detail_single 
    
phys_materials = ['pd_IronSteel','pd_Alu','pd_Copper','pd_Wood','pd_Cement','pd_Plastics']

phys_dict = {}
for material in phys_materials:
    frame= pd.read_excel('C:/Users/jstreeck/Desktop/EndUse_shortTermSave/SectorSplit_WasteFilter_physical/USA_SectorSplit/US_SectorSplitData.xlsx',sheet_name=material).set_index('Year')
    dict_ele = {material:frame}
    phys_dict.update(dict_ele)
    
    
    
    
    
'''
    #2 Load Exiobase tables/results (so far with HT_WIO only)
'''


year = 1995
years_exio = list(range(1995,2012))
# regions = ['US','AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI', 'FR', 'GR',\
#   'HR', 'HU', 'IE', 'IT', 'US', 'LT', 'LU', 'LV', 'MT', 'NL', 'PL', 'PT', 'RO',\
#      'SE', 'SI', 'SK', 'GB','JP', 'CN', 'CA', 'KR', 'BR', 'IN', 'MX',\
#       'RU', 'AU', 'CH', 'TR', 'TW', 'NO', 'ID', 'ZA', 'WA', 'WL', 'WE', 'WF',\
#        'WM'] #'US' not in above as already run
    
regions = ['US'] #'US' not in above as already run

Exio_dict = {}

for region in regions:
    Region_dict = {}
    for year in years_exio:
        for file in glob.glob(os.path.join((data_path_exio + 'Exio_HT_WIOMF_' + str(year) + '_' + region + '*.xlsx'))):
            Region_single = pd.read_excel(file, sheet_name='EndUse_shares_agg',index_col=[0,1],header=[0])
        Region_dict[year] = Region_single
    Exio_dict[region] = Region_dict

# single country all end-uses plot:
materials = ['steel', 'wood', 'Plastic', 'glass', 'alumin', 'tin', 'Copper']

region_dict ={}

for region in regions:
    material_dict = []
    for material in materials:
        material_single = []
        material_df = pd.DataFrame([], index=Exio_dict.get(region).get(year).index.get_level_values(1), columns=years_exio)
        for year in years_exio:
            material_single = Exio_dict.get(region).get(year).iloc[:,Exio_dict.get(region).get(year).columns.get_level_values(0).map(lambda t: (material) in t).to_list()]
            material_df[year] = material_single.values
        material_dict.append(material_df)        
        dict_1 = dict(zip(materials,material_dict))
    region_dict.update({region:dict_1})
    





'''
    #3 Assemble detailed comparison for USA national data + shipments + Exiobase (selected method)
'''





#methods = [CBA_dict, Wio_dict, Ghosh_dict, ParGhosh_dict, HTWio_dict] 
#method_names = ['CBA', 'WIO-MFA', 'Ghosh-IO AMC', 'Partial Ghosh-IO', 'HT-WIO' ]

#optionally with ExtAgg and WIO_filter diff
methods = [ Wio_dict, Wio_ext_dict , Wio_withServiceInput_dict,  HTWio_dict, HTWio_ext_dict] 
method_names = [ 'WIO-MFA', 'WIO-MFA_extAgg','WIO-MFA_filtDif', 'HT-WIO', 'HT-WIO_extAgg' ]

years = [1963,1967,1972,1977,1982,1987,1992,1997,2002,2007,2012]
#exio mat = ['steel', 'wood', 'Plastic', 'glass', 'alumin', 'tin', 'Copper']
#exio_enduse
#'Construction', 'Machinery and equipment n.e.c. ','Office machinery and computers (30)',
# 'Electrical machinery and apparatus n.e.c. (31)','Radio, television and communication equipment and apparatus (32)',
# 'Medical, precision and optical instruments, watches and clocks (33)','Motor vehicles, trailers and semi-trailers (34)',
# 'Other transport equipment (35)','Furniture; other manufactured goods n.e.c. (36)', 'Textiles (17)',
# 'Printed matter and recorded media (22)', 'Food', 'Other raw materials','Secondary materials', 
# 'Energy carriers', 'Energy carriers.1', 'Other','Products nec', 'Services']

# WOOD
year = 1963
Wood_dict = {}
count = -1
for method in methods:
    wood_single = []
    Wood_df = pd.DataFrame([], index=CBA_dict.get(year).index.get_level_values(1), columns=years)
    count= count +1
    for year in years:
        wood_single = method.get(year).iloc[:,method.get(year).columns.get_level_values(1).map(lambda t: ('Sawmill' or 'Wood') in t).to_list()]
        Wood_df[year] = wood_single.values
    Wood_dict[(method_names[count])] = Wood_df
    

#construction
wood_construction_df = pd.DataFrame([], index=list(range(1963,2013)), columns=method_names)
for method_name in method_names:
    wood_construction_df[method_name] = Wood_dict.get(method_name).loc['Residential'] + Wood_dict.get(method_name).loc['Non-Residential'] + Wood_dict.get(method_name).loc['Other buildings'] + Wood_dict.get(method_name ).loc['Infrastructure'] + Wood_dict.get(method_name).loc['Other construction']
wood_construction_df['Shipment_1'] = phys_dict.get('pd_Wood').T.loc['Construction total']*100 #'McKeever_constr.
wood_construction_df['Exio_HT-WIO'] = region_dict.get('US').get('wood').loc['Construction']
wood_construction_df.plot(kind='line',marker='o', title= 'Wood in Construction', legend = False)
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(years)
plt.ylabel('%')
plt.show()


#residential
wood_residential_df = pd.DataFrame([], index=list(range(1963,2013)), columns=method_names)
for method_name in method_names:
    wood_residential_df[method_name] = Wood_dict.get(method_name).loc['Residential']
wood_residential_df['Shipment_1'] = phys_dict.get('pd_Wood').T.loc['Total New Houses']*100 #'McKeever_resid.build.new.'
wood_residential_df.plot( kind='line',marker='o', title= 'Wood in Residential')
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(years)
plt.ylabel('%')
plt.show()

#non-residential
wood_nonresidential_df = pd.DataFrame([], index=list(range(1963,2013)), columns=method_names)
for method_name in method_names:
    wood_nonresidential_df[method_name] = Wood_dict.get(method_name).loc['Non-Residential']
wood_nonresidential_df['Shipment_1'] = phys_dict.get('pd_Wood').T.loc['Nonres Total']*100 #'McKeever_non.resid.constr.'
wood_nonresidential_df.plot(kind='line',marker='o', title= 'Wood in Non-Residential')
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(years)
plt.ylabel('%')
plt.show()

#furniture
wood_furniture_df = pd.DataFrame([], index=list(range(1963,2013)), columns=method_names)
for method_name in method_names:
    wood_furniture_df[method_name] = Wood_dict.get(method_name).loc['Furniture']
wood_furniture_df['Shipment_1'] = phys_dict.get('pd_Wood').T.loc['Furniture']*100 #'McKeever_furnit.'
wood_furniture_df['Exio_HT-WIO'] = region_dict.get('US').get('wood').loc['Furniture; other manufactured goods n.e.c.']
wood_furniture_df.plot(kind='line',marker='o', title= 'Wood in Furniture' )
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(years)
plt.ylabel('%')
plt.show()

#packaging
wood_packaging_df = pd.DataFrame([], index=list(range(1963,2013)), columns=method_names)
for method_name in method_names:
    wood_packaging_df[method_name] = Wood_dict.get(method_name).loc['Packaging']
wood_packaging_df['Shipment_1'] = phys_dict.get('pd_Wood').T.loc['Packaging and shippling']*100 #'McKeever_packag.'
wood_packaging_df['Exio_HT-WIO'] = region_dict.get('US').get('wood').loc['Food']
wood_packaging_df.plot(kind='line',marker='o', title= 'Wood in Packaging')
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(years)
plt.ylabel('%')
plt.show()

# # single-fam, multi-fam, manuf-houses, repair
# singleFam_df = pd.DataFrame([], index=list(range(1963,2013)), columns=method_names)
# singleFam_df [HTWIO_] = Wood_dict.get(method_name).loc['Packaging']


year = 1992
# ALUMINUM
alu_dict = {}
count = -1
for method in methods:
    alu_single = []
    alu_df = pd.DataFrame([], index=CBA_dict.get(year).index.get_level_values(1), columns=years)
    count= count +1
    for year in years:
        alu_single = method.get(year).iloc[:,method.get(year).columns.get_level_values(1).map(lambda t: ('alu' or 'Alu') in t).to_list()]
        alu_df[year] = alu_single.values
    alu_dict[(method_names[count])] = alu_df

#construction
alu_construction_df = pd.DataFrame([], index=list(range(1963,2013)), columns=method_names)
for method_name in method_names:
    alu_construction_df[method_name] = alu_dict.get(method_name).loc['Residential'] + alu_dict.get(method_name).loc['Non-Residential'] + alu_dict.get(method_name).loc['Other buildings'] + alu_dict.get(method_name ).loc['Infrastructure'] + alu_dict.get(method_name).loc['Other construction']
alu_construction_df['Shipment_1'] = phys_dict.get('pd_Alu').T.loc['USGS Construction']*100
alu_construction_df['Shipment_2'] = phys_dict.get('pd_Alu').T.loc['Liu Building & Construction']*100
alu_construction_df['Exio_HT-WIO'] = region_dict.get('US').get('alumin').loc['Construction']
alu_construction_df.plot(kind='line',marker='o', title= 'Aluminum in Construction' )
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(years)
plt.ylabel('%')
plt.show()

#transport
alu_transport_df = pd.DataFrame([], index=list(range(1963,2013)), columns=method_names)
for method_name in method_names:
    alu_transport_df[method_name] = alu_dict.get(method_name).loc['Motor vehicles'] + alu_dict.get(method_name).loc['Other transport equipment']
alu_transport_df['Shipment_1'] = phys_dict.get('pd_Alu').T.loc['USGS Transportation']*100
alu_transport_df['Shipment_2'] = phys_dict.get('pd_Alu').T.loc['Liu Transportation']*100
alu_transport_df['Exio_HT-WIO'] = region_dict.get('US').get('alumin').loc['Motor vehicles, trailers and semi-trailers'] +\
    region_dict.get('US').get('alumin').loc['Other transport equipment']
alu_transport_df.plot(kind='line',marker='o', title= 'Aluminum in Transportation' )
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(years)
plt.ylabel('%')
plt.show()


#packaging (assuming that also material in 'food products' is packaging)
alu_packaging_df = pd.DataFrame([], index=list(range(1963,2013)), columns=method_names)
for method_name in method_names:
    alu_packaging_df[method_name] = alu_dict.get(method_name).loc['Packaging'] + alu_dict.get(method_name).loc['Food products']
alu_packaging_df['Shipment_1'] = phys_dict.get('pd_Alu').T.loc['USGS Containers and packaging']*100
alu_packaging_df['Shipment_2'] = phys_dict.get('pd_Alu').T.loc['Liu Containers and packaging']*100
alu_packaging_df['Exio_HT-WIO'] = region_dict.get('US').get('alumin').loc['Food']
alu_packaging_df.plot(kind='line',marker='o', title= 'Aluminum in Packaging' )
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(years)
plt.ylabel('%')
plt.show()


#machinery
alu_machinery_df = pd.DataFrame([], index=list(range(1963,2013)), columns=method_names)
for method_name in method_names:
    alu_machinery_df[method_name] = alu_dict.get(method_name).loc['Electronic machinery'] + alu_dict.get(method_name).loc['Other machinery']
alu_machinery_df['Shipment_1'] = phys_dict.get('pd_Alu').T.loc['USGS Electrical']*100 +phys_dict.get('pd_Alu').T.loc['USGS Machinery and equipment']*100 #USGS_mach.&equipm.+electrical'
alu_machinery_df['Shipment_2'] = phys_dict.get('pd_Alu').T.loc['Liu Electrical']*100 +phys_dict.get('pd_Alu').T.loc['Liu Machinery and equipment']*100 #Liu_mach.&equipm.+electrical'
alu_machinery_df['Exio_HT-WIO'] = region_dict.get('US').get('alumin').loc['Machinery and equipment n.e.c. '] +\
    region_dict.get('US').get('alumin').loc['Electrical machinery and apparatus n.e.c.']
alu_machinery_df.plot(kind='line',marker='o', title= 'Aluminum in Machinery' )
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(years)
plt.ylabel('%')
plt.show()

#machinery electrical
alu_machineryElectric_df = pd.DataFrame([], index=list(range(1963,2013)), columns=method_names)
for method_name in method_names:
    alu_machineryElectric_df[method_name] = alu_dict.get(method_name).loc['Electronic machinery'] 
alu_machineryElectric_df['Shipment_1'] = phys_dict.get('pd_Alu').T.loc['USGS Electrical']*100 
alu_machineryElectric_df['Shipment_2'] = phys_dict.get('pd_Alu').T.loc['Liu Electrical']*100 
alu_machineryElectric_df.plot(kind='line',marker='o', title= 'Aluminum in Electronic machinery' )
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(years)
plt.ylabel('%')
plt.show()


#machinery other
alu_machineryOther_df = pd.DataFrame([], index=list(range(1963,2013)), columns=method_names)
for method_name in method_names:
    alu_machineryOther_df[method_name] = alu_dict.get(method_name).loc['Other machinery']
alu_machineryOther_df['Shipment_1'] = phys_dict.get('pd_Alu').T.loc['USGS Machinery and equipment']*100
alu_machineryOther_df['Shipment_2'] = phys_dict.get('pd_Alu').T.loc['Liu Machinery and equipment']*100
alu_machineryOther_df.plot(kind='line',marker='o', title= 'Aluminum in Other machinery' )
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(years)
plt.ylabel('%')
plt.show()


# STEEL
steel_dict = {}
count = -1
for method in methods:
    steel_single = []
    steel_df = pd.DataFrame([], index=CBA_dict.get(year).index.get_level_values(1), columns=years)
    count= count +1
    for year in years:
        steel_single = method.get(year).iloc[:,method.get(year).columns.get_level_values(1).map(lambda t: ('steel' or 'Blast') in t).to_list()]
        steel_df[year] = steel_single.values
    steel_dict[(method_names[count])] = steel_df
        
#construction
steel_construction_df = pd.DataFrame([], index=list(range(1963,2013)), columns=method_names)
for method_name in method_names:
    steel_construction_df[method_name] = steel_dict.get(method_name).loc['Residential'] + steel_dict.get(method_name).loc['Non-Residential'] + steel_dict.get(method_name).loc['Other buildings'] + steel_dict.get(method_name).loc['Infrastructure'] + steel_dict.get(method_name).loc['Other construction']
steel_construction_df['Shipment_1'] = phys_dict.get('pd_IronSteel').T.loc['Construction USGS+Trade']*100
steel_construction_df['Shipment_2'] = phys_dict.get('pd_IronSteel').T.loc['Construction YSTAFB']*100
steel_construction_df['Shipment_3'] = phys_dict.get('pd_IronSteel').T.loc['Construction Pauliuk']*100
steel_construction_df['Exio_HT-WIO'] = region_dict.get('US').get('steel').loc['Construction']
steel_construction_df.plot(kind='line',marker='o', title= 'Steel in Construction' )
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(years)
plt.ylabel('%')
plt.show()

#transport
steel_transport_df = pd.DataFrame([], index=list(range(1963,2013)), columns=method_names)
for method_name in method_names:
    steel_transport_df[method_name] = steel_dict.get(method_name).loc['Motor vehicles'] + steel_dict.get(method_name).loc['Other transport equipment']
steel_transport_df['Shipment_1'] = phys_dict.get('pd_IronSteel').T.loc['Transportation USGS+Trade']*100
steel_transport_df['Exio_HT-WIO'] = region_dict.get('US').get('steel').loc['Motor vehicles, trailers and semi-trailers'] +\
    region_dict.get('US').get('steel').loc['Other transport equipment']
steel_transport_df['Shipment_2'] = phys_dict.get('pd_IronSteel').T.loc['Transport YSTAFB']*100
steel_transport_df['Shipment_3'] = phys_dict.get('pd_IronSteel').T.loc['Automotive Pauliuk']*100 + phys_dict.get('pd_IronSteel').T.loc['Rail Transportation Pauliuk']*100\
    + phys_dict.get('pd_IronSteel').T.loc['Shipbuilding Pauliuk']*100 +  + phys_dict.get('pd_IronSteel').T.loc['Aircraft Pauliuk']*100
steel_transport_df.plot(kind='line',marker='o', title= 'Steel in Transportation' )
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(years)
plt.ylabel('%')
plt.show()

#packaging (assuming that also material in 'food products' is packaging)
steel_packaging_df = pd.DataFrame([], index=list(range(1963,2013)), columns=method_names)
for method_name in method_names:
    steel_packaging_df[method_name] = steel_dict.get(method_name).loc['Packaging'] + steel_dict.get(method_name).loc['Food products']
steel_packaging_df['Shipment_1'] = phys_dict.get('pd_IronSteel').T.loc['Containers USGS+Trade']*100
steel_packaging_df['Exio_HT-WIO'] = region_dict.get('US').get('steel').loc['Food']
steel_packaging_df['Shipment_3'] = phys_dict.get('pd_IronSteel').T.loc['Containers, shipping materials Pauliuk']*100
steel_packaging_df.plot(kind='line',marker='o', title= 'Steel in Packaging' )
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(years)
plt.ylabel('%')
plt.show()

#machinery
steel_machinery_df = pd.DataFrame([], index=list(range(1963,2013)), columns=method_names)
for method_name in method_names:
    steel_machinery_df[method_name] = steel_dict.get(method_name).loc['Other machinery']
steel_machinery_df['Shipment_2'] = phys_dict.get('pd_IronSteel').T.loc['Machinery & Appliances YSTAFB']*100
steel_machinery_df['Exio_HT-WIO'] = region_dict.get('US').get('steel').loc['Machinery and equipment n.e.c. '] +\
    region_dict.get('US').get('steel').loc['Electrical machinery and apparatus n.e.c.']
steel_machinery_df['Shipment_3'] = phys_dict.get('pd_IronSteel').T.loc['Machinery Pauliuk']*100 + phys_dict.get('pd_IronSteel').T.loc['Rail Transportation Pauliuk']*100\
        + phys_dict.get('pd_IronSteel').T.loc['Electrical Equipment Pauliuk']*100 +  + phys_dict.get('pd_IronSteel').T.loc['Appliances Pauliuk']*100
steel_machinery_df.plot(kind='line',marker='o', title= 'Steel in Machinery' )
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(years)
plt.ylabel('%')
plt.show()

#remainder
steel_remainder_df = pd.DataFrame([], index=list(range(1963,2013)), columns=method_names)
for method_name in method_names:
    steel_remainder_df[method_name] = 100 - (steel_dict.get(method_name).loc['Other machinery'] + \
    steel_dict.get(method_name).loc['Packaging'] + steel_dict.get(method_name).loc['Food products']+\
    steel_dict.get(method_name).loc['Motor vehicles'] + steel_dict.get(method_name).loc['Other transport equipment'] +\
    steel_dict.get(method_name).loc['Residential'] + steel_dict.get(method_name).loc['Non-Residential'] + steel_dict.get(method_name).loc['Other buildings'] + steel_dict.get(method_name).loc['Infrastructure'] + steel_dict.get(method_name).loc['Other construction'])
steel_remainder_df['Shipment_1'] = phys_dict.get('pd_IronSteel').T.loc['Service centers and distributors USGS+Trade']*100 +\
    phys_dict.get('pd_IronSteel').T.loc['Other USGS+Trade']*100 + phys_dict.get('pd_IronSteel').T.loc['Undistributed USGS+Trade']*100
steel_remainder_df['Shipment_2'] = phys_dict.get('pd_IronSteel').T.loc['Other products YSTAFB']*100
steel_remainder_df['Shipment_3'] = 100 - (phys_dict.get('pd_IronSteel').T.loc['Containers, shipping materials Pauliuk']*100 +\
    phys_dict.get('pd_IronSteel').T.loc['Automotive Pauliuk']*100 + phys_dict.get('pd_IronSteel').T.loc['Rail Transportation Pauliuk']*100\
        + phys_dict.get('pd_IronSteel').T.loc['Shipbuilding Pauliuk']*100 +  + phys_dict.get('pd_IronSteel').T.loc['Aircraft Pauliuk']*100 +\
          phys_dict.get('pd_IronSteel').T.loc['Construction Pauliuk']*100 +  phys_dict.get('pd_IronSteel').T.loc['Machinery Pauliuk']*100 + phys_dict.get('pd_IronSteel').T.loc['Rail Transportation Pauliuk']*100\
                  + phys_dict.get('pd_IronSteel').T.loc['Electrical Equipment Pauliuk']*100 +  + phys_dict.get('pd_IronSteel').T.loc['Appliances Pauliuk']*100)
steel_remainder_df.plot(kind='line',marker='o', title= 'Steel in Other' )
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(years)
plt.ylabel('%')
plt.show()



# COPPER (some problems assembling the material dict so took the easy way)
years_cop = [1963,1967,1972,1977,1982,1987,1992]
years_cop2 =  [1997]
years_cop3 = [2002]
years_cop4 = [2007,2012]
copper_dict = {}
count = -1
for method in methods:
    copper_single = []
    copper_df = pd.DataFrame([], index=CBA_dict.get(year).index.get_level_values(1), columns=years)
    count= count +1
    for year in years_cop:
        copper_single = method.get(year).iloc[:,method.get(year).columns.get_level_values(0).astype(str).map(lambda t: ('3801' ) in t).to_list()]
        copper_df[year] = copper_single.values
    copper_dict[(method_names[count])] = copper_df 
    for year2 in years_cop2:
        copper_single = method.get(year2).iloc[:,method.get(year2).columns.get_level_values(1).map(lambda t: ('smelting') in t).to_list()]
        copper_df[year2] = copper_single.values
    copper_dict[(method_names[count])] = copper_df
    for year3 in years_cop3:
        copper_single = method.get(year3).iloc[:,method.get(year3).columns.get_level_values(0).astype(str).map(lambda t: ('331411') in t).to_list()]
        copper_df[year3] = copper_single.values
    copper_dict[(method_names[count])] = copper_df
    for year4 in years_cop4:
        copper_single = method.get(year4).iloc[:,method.get(year4).columns.get_level_values(1).map(lambda t: ('Copper') in t).to_list()]
        copper_df[year4] = copper_single.values
    copper_dict[(method_names[count])] = copper_df
    
##values are NOT in the correct sequence --> plots still work I think, check!

#construction
copper_construction_df = pd.DataFrame([], index=list(range(1963,2013)), columns=method_names)
for method_name in method_names:
    copper_construction_df[method_name] = copper_dict.get(method_name).loc['Residential'] + copper_dict.get(method_name).loc['Non-Residential'] + copper_dict.get(method_name).loc['Other buildings'] + copper_dict.get(method_name).loc['Infrastructure'] + copper_dict.get(method_name).loc['Other construction']
copper_construction_df['Shipment_1'] = phys_dict.get('pd_Copper').T.loc['Building construction USGS+Trade']*100
copper_construction_df['Shipment_2'] = phys_dict.get('pd_Copper').T.loc['Building construction CDA+Trade']*100
copper_construction_df['Exio_HT-WIO'] = region_dict.get('US').get('Copper').loc['Construction']
copper_construction_df.plot(kind='line',marker='o', title= 'Copper in Construction' )
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(years)
plt.ylabel('%')
plt.show()

#transportation
copper_transport_df = pd.DataFrame([], index=list(range(1963,2013)), columns=method_names)
for method_name in method_names:
    copper_transport_df[method_name] = copper_dict.get(method_name).loc['Motor vehicles'] + copper_dict.get(method_name).loc['Other transport equipment']
copper_transport_df['Shipment_1'] = phys_dict.get('pd_Copper').T.loc['Transportation equipment USGS+Trade']*100
copper_transport_df['Shipment_2'] = phys_dict.get('pd_Copper').T.loc['Transportation equipment CDA+Trade']*100
copper_transport_df['Exio_HT-WIO'] = region_dict.get('US').get('Copper').loc['Motor vehicles, trailers and semi-trailers'] +\
    region_dict.get('US').get('Copper').loc['Other transport equipment']
copper_transport_df.plot(kind='line',marker='o', title= 'Copper in Transportation' )
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(years)
plt.ylabel('%')
plt.show()

#machinery
copper_machinery_df = pd.DataFrame([], index=list(range(1963,2013)), columns=method_names)
for method_name in method_names:
    copper_machinery_df[method_name] = copper_dict.get(method_name).loc['Electronic machinery'] + copper_dict.get(method_name).loc['Other machinery']
copper_machinery_df['Shipment_1'] = phys_dict.get('pd_Copper').T.loc['Electrical and electronic products USGS+Trade']*100 +phys_dict.get('pd_Copper').T.loc['Industrial machinery and equipment USGS+Trade']*100
copper_machinery_df['Shipment_2'] = phys_dict.get('pd_Copper').T.loc['Electrical and electronic products CDA+Trade']*100 +phys_dict.get('pd_Copper').T.loc['Industrial machinery and equipment CDA+Trade']*100
copper_machinery_df['Exio_HT-WIO'] = region_dict.get('US').get('Copper').loc['Machinery and equipment n.e.c. '] +\
    region_dict.get('US').get('Copper').loc['Electrical machinery and apparatus n.e.c.']
copper_machinery_df.plot(kind='line',marker='o', title= 'Copper in Machinery' )
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(years)
plt.ylabel('%')
plt.show()

#machinery electrical
copper_machineryElectric_df = pd.DataFrame([], index=list(range(1963,2013)), columns=method_names)
for method_name in method_names:
    copper_machineryElectric_df[method_name] = copper_dict.get(method_name).loc['Electronic machinery'] 
copper_machineryElectric_df['Shipment_1'] = phys_dict.get('pd_Copper').T.loc['Electrical and electronic products USGS+Trade']*100
copper_machineryElectric_df['Shipment_2'] = phys_dict.get('pd_Copper').T.loc['Electrical and electronic products CDA+Trade']*100
copper_machineryElectric_df.plot(kind='line',marker='o', title= 'Copper in Electronic machinery' )
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(years)
plt.ylabel('%')
plt.show()

#machinery other
copper_machineryOther_df = pd.DataFrame([], index=list(range(1963,2013)), columns=method_names)
for method_name in method_names:
    copper_machineryOther_df[method_name] = copper_dict.get(method_name).loc['Other machinery']
copper_machineryOther_df['Shipment_1'] = phys_dict.get('pd_Copper').T.loc['Industrial machinery and equipment USGS+Trade']*100
copper_machineryOther_df['Shipment_2'] = phys_dict.get('pd_Copper').T.loc['Industrial machinery and equipment CDA+Trade']*100
copper_machineryOther_df.plot(kind='line',marker='o', title= 'Copper in Other machinery' )
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(years)
plt.ylabel('%')
plt.show()



# CEMENT
cement_dict = {}
count = -1
for method in methods:
    cement_single = []
    cement_df = pd.DataFrame([], index=CBA_dict.get(year).index.get_level_values(1), columns=years)
    count= count +1
    for year in years:
        cement_single = method.get(year).iloc[:,method.get(year).columns.get_level_values(1).map(lambda t: ('Cement' or 'cement') in t).to_list()]
        cement_df[year] = cement_single.values
    cement_dict[(method_names[count])] = cement_df

cement_residential_df = pd.DataFrame([], index=list(range(1963,2017)), columns=method_names)
for method_name in method_names:
    cement_residential_df[method_name] = cement_dict.get(method_name).loc['Residential']
cement_residential_df['Shipment_1'] = phys_dict.get('pd_Cement').T.loc['Residential PCA']*100 #'PCA_resid.buildings'
cement_residential_df['Shipment_2'] = phys_dict.get('pd_Cement').T.loc['Residential Cao']*100 #'Cao_resid.building'
cement_residential_df['Shipment_3'] = phys_dict.get('pd_Cement').T.loc['Residential buildings PCA Kapur & web']*100
cement_residential_df.plot(kind='line',marker='o', title= 'Cement in Residential STRUCTURES' )
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(years)
plt.ylabel('%')
plt.show()

cement_nonRes_df = pd.DataFrame([], index=list(range(1963,2017)), columns=method_names)
for method_name in method_names:
    cement_nonRes_df[method_name] = cement_dict.get(method_name).loc['Non-Residential']
cement_nonRes_df['Shipment_1'] = phys_dict.get('pd_Cement').T.loc['Nonresidential buildings PCA']*100 #'PCA_nonres.buildings
cement_nonRes_df['Shipment_2'] = phys_dict.get('pd_Cement').T.loc['Non-Residential Cao']*100 #'Cao_nonres.building'
cement_nonRes_df['Shipment_3'] = phys_dict.get('pd_Cement').T.loc['Commercial buildings PCA Kapur & web']*100 + \
    phys_dict.get('pd_Cement').T.loc['Public Buildings PCA Kapur & web']*100 + phys_dict.get('pd_Cement').T.loc['Farm construction PCA Kapur & web']*100
cement_nonRes_df.plot(kind='line',marker='o', title= 'Cement in Non-residential STRUCTURES' )
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(years)
plt.ylabel('%')
plt.show()

cement_CE_df = pd.DataFrame([], index=list(range(1963,2017)), columns=method_names)
for method_name in method_names:
    cement_CE_df[method_name] = cement_dict.get(method_name).loc['Infrastructure'] + cement_dict.get(method_name).loc['Other construction']
cement_CE_df['Shipment_1'] = phys_dict.get('pd_Cement').T.loc['Civil engineering/Infra']*100 + phys_dict.get('pd_Cement').T.loc['Highways & Streets']*100 #'PCA_civ.eng+streets'
cement_CE_df['Shipment_2'] = phys_dict.get('pd_Cement').T.loc['Civil Engineering Cao']*100
cement_CE_df['Shipment_3'] = phys_dict.get('pd_Cement').T.loc['Utilities PCA Kapur & web']*100 + \
    phys_dict.get('pd_Cement').T.loc['Streets and Highways PCA Kapur & web']*100 + phys_dict.get('pd_Cement').T.loc['Others PCA Kapur & web']*100\
        + phys_dict.get('pd_Cement').T.loc['Water and waste management PCA Kapur & web']*100 #'PCAKapur_util.+streets+other'
cement_CE_df.plot(kind='line',marker='o', title= 'Cement in Civil Engineering' )
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(years)
plt.ylabel('%')
plt.show()

#make one for highways & streets

# PLASTIC
plastic_dict = {}
count = -1
for method in methods:
    plastic_single = []
    plastic_df = pd.DataFrame([], index=CBA_dict.get(year).index.get_level_values(1), columns=years)
    count= count +1
    for year in years:
        plastic_single = method.get(year).iloc[:,method.get(year).columns.get_level_values(1).map(lambda t: ('Plastic' or 'plastic') in t).to_list()]
        plastic_df[year] = plastic_single.values
    plastic_dict[(method_names[count])] = plastic_df

#construction
plastic_construction_df = pd.DataFrame([], index=list(range(1963,2013)), columns=method_names)
for method_name in method_names:
    plastic_construction_df[method_name] = plastic_dict.get(method_name).loc['Residential'] + plastic_dict.get(method_name).loc['Non-Residential'] + plastic_dict.get(method_name).loc['Other buildings'] + plastic_dict.get(method_name).loc['Infrastructure'] + plastic_dict.get(method_name).loc['Other construction']
plastic_construction_df['Shipment_1'] = phys_dict.get('pd_Plastics').T.loc['Construction industry Euromap USA']*100
plastic_construction_df['Shipment_2'] = phys_dict.get('pd_Plastics').T.loc['Building and construction PE']*100 #'PlasticsEurope_EU_'
plastic_construction_df['Exio_HT-WIO'] = region_dict.get('US').get('Plastic').loc['Construction']
plastic_construction_df.plot(kind='line',marker='o', title= 'Plastics in Construction' )
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(years)
plt.ylabel('%')
plt.show()



#packaging (assuming that also material in 'food products' is packaging)
plastic_packaging_df = pd.DataFrame([], index=list(range(1963,2013)), columns=method_names)
for method_name in method_names:
    plastic_packaging_df[method_name] = plastic_dict.get(method_name).loc['Packaging'] + plastic_dict.get(method_name).loc['Food products'] 
plastic_packaging_df['Shipment_1'] = phys_dict.get('pd_Plastics').T.loc['Packaging Euromap USA']*100
plastic_packaging_df['Shipment_2'] = phys_dict.get('pd_Plastics').T.loc['Packaging PE']*100 #'PlasticsEurope_EU_packag.'
plastic_packaging_df['Exio_HT-WIO'] = region_dict.get('US').get('Plastic').loc['Food']
plastic_packaging_df.plot(kind='line',marker='o', title= 'Plastics in Packaging/Food' )
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(years)
plt.ylabel('%')
plt.show()



#transport (assuming that also material in 'food products' is transport)
plastic_transport_df = pd.DataFrame([], index=list(range(1963,2013)), columns=method_names)
for method_name in method_names:
    plastic_transport_df[method_name] = plastic_dict.get(method_name).loc['Motor vehicles'] + plastic_dict.get(method_name).loc['Other transport equipment'] 
plastic_transport_df['Shipment_1'] = phys_dict.get('pd_Plastics').T.loc['Automotive Euromap USA']*100
plastic_transport_df['Shipment_2'] = phys_dict.get('pd_Plastics').T.loc['Automotive PE']*100
plastic_transport_df['Exio_HT-WIO'] = region_dict.get('US').get('Plastic').loc['Motor vehicles, trailers and semi-trailers'] +\
    region_dict.get('US').get('Plastic').loc['Other transport equipment']
plastic_transport_df.plot(kind='line',marker='o', title= 'Plastics in Transport/Automotive' )
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(years)
plt.ylabel('%')
plt.show()


#electronics (assuming that also material in 'food products' is transport)
plastic_electrical_df = pd.DataFrame([], index=list(range(1963,2013)), columns=method_names)
for method_name in method_names:
    plastic_electrical_df[method_name] = plastic_dict.get(method_name).loc['Electronic machinery']  
plastic_electrical_df['Shipment_1'] = phys_dict.get('pd_Plastics').T.loc['Electrical, electronics & telecom Euromap USA']*100
plastic_electrical_df['Shipment_2'] = phys_dict.get('pd_Plastics').T.loc['Electrical&Electronic PE']*100
plastic_electrical_df.plot(kind='line',marker='o', title= 'Plastics in Electronics' )
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(years)
plt.ylabel('%')
plt.show()





'''
 #plot above U.S dataframes into multi-plot
 
 '''
plastic_packaging_df
plastic_transport_df
plastic_construction_df
plastic_elect_df

alu_transport_df
alu_construction_df
alu_packaging_df
alu_machinery_df

alu_machineryElectric_df
alu_machineryOther_df

copper_construction_df
copper_transport_df
copper_machinery_df

steel_construction_df
steel_transport_df
steel_packaging_df
steel_machinery_df

steel_remainder_df

wood_construction_df
wood_residential_df
wood_nonresidential_df
wood_furniture_df
wood_packaging_df

'''STATISTICS'''

high_aggregation_numComp = [plastic_packaging_df, plastic_transport_df,plastic_construction_df,plastic_electrical_df,\
                    alu_transport_df,alu_construction_df,alu_packaging_df,alu_machinery_df,copper_construction_df,\
                    copper_transport_df,copper_machinery_df,\
                    steel_construction_df,steel_transport_df,steel_packaging_df,steel_machinery_df,
                    wood_construction_df,wood_furniture_df,wood_packaging_df]
    
high_aggregation_numComp_plast = [plastic_packaging_df, plastic_transport_df,\
                                  plastic_construction_df,plastic_electrical_df]
high_aggregation_numComp_alu = [alu_transport_df,alu_construction_df,alu_packaging_df,\
                                alu_machinery_df]
high_aggregation_numComp_steel = [steel_construction_df,steel_transport_df,steel_packaging_df,
                                  steel_machinery_df]
high_aggregation_numComp_wood = [wood_construction_df,wood_furniture_df,wood_packaging_df]

high_aggregation_numComp_cop = [copper_construction_df,copper_transport_df,copper_machinery_df]
                             


high_aggregation_numComp_const = [plastic_construction_df,copper_construction_df, wood_construction_df,\
                                  steel_construction_df,alu_construction_df]
high_aggregation_numComp_trans = [plastic_transport_df, alu_transport_df, steel_transport_df,\
                                  copper_transport_df]
high_aggregation_numComp_mach = [plastic_electrical_df,alu_machinery_df,steel_machinery_df,\
                                 copper_machinery_df]
high_aggregation_numComp_pack = [plastic_packaging_df, alu_packaging_df, steel_packaging_df,\
                                 wood_packaging_df]

total_deviation = []
rel_deviation = []
for frame in high_aggregation_numComp_pack:
    try:
        frame['HT-Shipment1'] = frame['HT-WIO'] - frame['Shipment_1']
        frame['HT-Shipment1_rel']  = (frame['HT-WIO'] - frame['Shipment_1'])/frame['Shipment_1']
        total_deviation.append(frame['HT-Shipment1'].dropna().values.tolist())
        rel_deviation.append(frame['HT-Shipment1_rel'].dropna().values.tolist())
    except:
        continue
    try:
        frame['HT-Shipment2']  = frame['HT-WIO'] - frame['Shipment_2']
        total_deviation.append(frame['HT-Shipment2'].dropna().values.tolist())
        frame['HT-Shipment2_rel']  = (frame['HT-WIO'] - frame['Shipment_2'])/frame['Shipment_2']
        total_deviation.append(frame['HT-Shipment2'].dropna().values.tolist())
        rel_deviation.append(frame['HT-Shipment2_rel'].dropna().values.tolist())
    except:
        continue
    try:
        frame['HT-Shipment3']  = frame['HT-WIO'] - frame['Shipment_3']
        frame['HT-Shipment3_rel']  = (frame['HT-WIO'] - frame['Shipment_3'])/frame['Shipment_3']
        total_deviation.append(frame['HT-Shipment3'].dropna().values.tolist())
        rel_deviation.append(frame['HT-Shipment3_rel'].dropna().values.tolist())
    except:
        continue


import statistics   
total_deviation_abs =  [abs(x) for x in sum(total_deviation, [])]
tot_dev_mean = sum(total_deviation_abs)/len(total_deviation_abs)
tot_dev_med = statistics.median(total_deviation_abs)

rel_deviation_abs =  [abs(x) for x in sum(rel_deviation, [])]
rel_dev_mean = sum(rel_deviation_abs )/len(rel_deviation_abs )
rel_dev_med = statistics.median(rel_deviation_abs )

print(tot_dev_mean,tot_dev_med, max(total_deviation_abs), min(total_deviation_abs), \
      rel_dev_mean*100, rel_dev_med*100, max(rel_deviation_abs)*100, min(rel_deviation_abs)*100) 
    
    
    
#####################    
    
    
    
    
    
    
##OPTIONAL: add ext_agg and differnt filter design to matrices:
    
Wio_withServiceInput_dict = {}
Wio_ext_dict = {}
HTWio_ext_dict = {}


'''PLOT: high sector aggregation'''

pal = sns.color_palette("colorblind") 

color_dict = {'CBA':pal[0], 'WIO-MFA': pal[1], 'Ghosh-IO AMC':pal[2],  \
              'Partial Ghosh-IO': pal[3], 'HT-WIO': pal[5], 'Exio_HT-WIO': pal[4],\
            'Shipment_1':pal[7], 'Shipment_2':pal[0],'Shipment_3':pal[3]}

marker_dict = {'CBA':'o', 'WIO-MFA': 'o', 'Ghosh-IO AMC':'o',  \
              'Partial Ghosh-IO': 'o', 'HT-WIO': 'v', 'Exio_HT-WIO': '.'}


name_list1 = ['wood_construction_df',  'steel_construction_df', 'alu_construction_df', 'copper_construction_df', 'plastic_construction_df','steel_transport_df', 'alu_transport_df',\
              'copper_transport_df', 'plastic_transport_df', 'steel_machinery_df', 'alu_machinery_df', 'copper_machinery_df', 'plastic_electrical_df', \
              'wood_packaging_df', 'steel_packaging_df','alu_packaging_df', 'plastic_packaging_df','wood_furniture_df']

plot_list1 = [eval(e) for e in name_list1]

k,i,j = 0,0,0     
fig, axs = plt.subplots(6,3 ,sharex=False, sharey=False, figsize=(14,20))
#axs[6,2].axis('off')

           
for i in range(0,6):
    for j in range (0,3):
        plot_list1[k].plot(ax=axs[i,j], color = [color_dict.get(r) for r in plot_list1[k]], style = [marker_dict.get(r, '*') for r in plot_list1[k]], kind='line', title= name_list1[k][:-3], legend = False)
        k = k+1
        axs[i,j].set_ylabel('%')
        axs[i,j].set_xticks([1963,1972,1982,1992,2002,2012])
             
#-->need to give different names to dataframes
#axs[0,1].annotate(label='lala',xy=(1990, 0.5),text='lala') #write text in plot

lgd = fig.legend(loc='center left', bbox_to_anchor=(0.145, -0.02),fontsize=14, ncol=5) #, bbox_to_anchor=(0.01, 0.5),fontsize=14)

def add_line(legend):
    ax1 = legend.axes
    from matplotlib.lines import Line2D

    import matplotlib.patches as mpatches
    handles, labels = axs[0,1].get_legend_handles_labels()
    legend._legend_box = None
    legend._init_legend_box(handles, labels)
    legend._set_loc(legend._loc)
    legend.set_title(legend.get_title().get_text())


           
add_line(lgd)
fig.suptitle('Comparison of end-use shares - high sector aggregation', y=1, fontsize = 16)
fig.tight_layout()



'''PLOT: SENSITIVITY high sector aggregation'''

pal = sns.color_palette("colorblind") 

#optionally with ExtAgg and WIO_filter diff
color_dict = {'WIO-MFA': pal[3], 'HT-WIO': pal[5], 'WIO-MFA_extAgg': pal[3],'WIO-MFA_filtDif': pal[3], \
            'HT-WIO_extAgg': pal[5],'Exio_HT-WIO': pal[4], 'Shipment_1':pal[7], 'Shipment_2':pal[0],'Shipment_3':pal[3]}

marker_dict = {'WIO-MFA': 'o', 'HT-WIO': 'v', 'WIO-MFA_extAgg': '*','WIO-MFA_filtDif': 'h' ,\
            'HT-WIO_extAgg': '*'}


name_list1 = ['wood_construction_df',  'steel_construction_df', 'alu_construction_df', 'copper_construction_df', 'plastic_construction_df','steel_transport_df', 'alu_transport_df',\
              'copper_transport_df', 'plastic_transport_df', 'steel_machinery_df', 'alu_machinery_df', 'copper_machinery_df', 'plastic_electrical_df', \
              'wood_packaging_df', 'steel_packaging_df','alu_packaging_df', 'plastic_packaging_df','wood_furniture_df']

plot_list1 = [eval(e) for e in name_list1]

k,i,j = 0,0,0     
fig, axs = plt.subplots(6,3 ,sharex=False, sharey=False, figsize=(14,20))
#axs[6,2].axis('off')

           
for i in range(0,6):
    for j in range (0,3):
        plot_list1[k].plot(ax=axs[i,j], color = [color_dict.get(r) for r in plot_list1[k]], style = [marker_dict.get(r, '*') for r in plot_list1[k]], kind='line', title= name_list1[k][:-3], legend = False)
        k = k+1
        axs[i,j].set_ylabel('%')
        axs[i,j].set_xticks([1963,1972,1982,1992,2002,2012])
             
#-->need to give different names to dataframes
#axs[0,1].annotate(label='lala',xy=(1990, 0.5),text='lala') #write text in plot

lgd = fig.legend(loc='center left', bbox_to_anchor=(0.145, -0.02),fontsize=14, ncol=5) #, bbox_to_anchor=(0.01, 0.5),fontsize=14)

def add_line(legend):
    ax1 = legend.axes
    from matplotlib.lines import Line2D

    import matplotlib.patches as mpatches
    handles, labels = axs[0,1].get_legend_handles_labels()
    legend._legend_box = None
    legend._init_legend_box(handles, labels)
    legend._set_loc(legend._loc)
    legend.set_title(legend.get_title().get_text())


           
add_line(lgd)
fig.suptitle('Sensitivity to extension choice & filter design (WIO-MFA, HT-WIO) @high aggregation', y=1, fontsize = 16)
#fig.suptitle('Comparison of end-use shares - high sector aggregation', y=1, fontsize = 16)
fig.tight_layout()



'''PLOT: medium sector aggregation'''

pal = sns.color_palette("colorblind") 
color_dict = {'CBA':pal[0], 'WIO-MFA': pal[1], 'Ghosh-IO AMC':pal[2],  \
              'Partial Ghosh-IO': pal[3], 'HT-WIO': pal[5], 'Exio_HT-WIO': pal[4],\
            'Shipment_1':pal[7], 'Shipment_2':pal[0],'Shipment_3':pal[3]}
marker_dict = {'CBA':'o', 'WIO-MFA': 'o', 'Ghosh-IO AMC':'o',  \
              'Partial Ghosh-IO': 'o', 'HT-WIO': 'v', 'Exio_HT-WIO': '.'}
name_list1 = ['wood_residential_df', 'wood_nonresidential_df', 'cement_residential_df', 'cement_nonRes_df', 'cement_CE_df']
plot_list1 = [eval(e) for e in name_list1]


k,i,j = 0,0,0     
fig, axs = plt.subplots(2,3 ,sharex=False, sharey=False, figsize=(14,7))
axs[1,2].axis('off')

for i in range(0,2):
    for j in range (0,3):
        try:
            plot_list1[k].plot(ax=axs[i,j], color = [color_dict.get(r,pal[0]) for r in plot_list1[k]], style = [marker_dict.get(r, '*') for r in plot_list1[k]], kind='line', title= name_list1[k][:-3], legend = False)
            k = k+1
            axs[i,j].set_ylabel('%')
            axs[i,j].set_xticks([1963,1972,1982,1992,2002,2012])
        except:
            continue
             
lgd = axs[1,2].legend(loc='center', fontsize=14) #, bbox_to_anchor=(0.01, 0.5),fontsize=14)

def add_line(legend):
    ax1 = legend.axes
    from matplotlib.lines import Line2D

    import matplotlib.patches as mpatches
    handles, labels = axs[1,0].get_legend_handles_labels()
    legend._legend_box = None
    legend._init_legend_box(handles, labels)
    legend._set_loc(legend._loc)
    legend.set_title(legend.get_title().get_text())
           
add_line(lgd)
fig.suptitle('Comparison of end-use shares - medium sector aggregation', y=1, fontsize = 16)
fig.tight_layout()
 
 
 
'''PLOT: combine medium and low sector aggregation'''

wood_detail = pd.read_excel(data_path_usa + 'Construction_detail_Run_220317-102202_manualEdit.xlsx',sheet_name='Wood_out', index_col=[0])
cement_detail = pd.read_excel(data_path_usa + 'Construction_detail_Run_220317-102202_manualEdit.xlsx',sheet_name='Cement_out', index_col=[0])


pal = sns.color_palette("colorblind") 
color_dict = {'CBA':pal[0], 'WIO-MFA': pal[1], 'Ghosh-IO AMC':pal[2],  \
              'Partial Ghosh-IO': pal[3], 'HT-WIO': pal[5], 'Exio_HT-WIO': pal[4],\
            'Shipment_1':pal[7], 'Shipment_2':pal[0],'Shipment_3':pal[3]}
marker_dict = {'CBA':'o', 'WIO-MFA': 'o', 'Ghosh-IO AMC':'o',  \
              'Partial Ghosh-IO': 'o', 'HT-WIO': 'v', 'Exio_HT-WIO': '.'}
name_list1 = ['wood_residential_df', 'wood_nonresidential_df', 'cement_residential_df', 'cement_nonRes_df', 'cement_CE_df']
plot_list1 = [eval(e) for e in name_list1]


k,i,j = 0,0,0     
fig, axs = plt.subplots(3,3 ,sharex=False, sharey=False, figsize=(14,11), gridspec_kw={'height_ratios':[1,1,1.4]}) #'width_ratios': [2,0.08],
axs[1,2].axis('off')
axs[2,2].axis('off')

for i in range(0,2):
    for j in range (0,3):
        try:
            plot_list1[k].plot(ax=axs[i,j], color = [color_dict.get(r,pal[0]) for r in plot_list1[k]], style = [marker_dict.get(r, '*') for r in plot_list1[k]], kind='line', title= name_list1[k][:-3], legend = False)
            k = k+1
            axs[i,j].set_ylabel('%')
            axs[i,j].set_xticks([1963,1972,1982,1992,2002,2012])
        except:
            continue
             


pal = sns.color_palette("colorblind") 
color_dict_low = {'MIOT new single-family*':pal[0],'MIOT new-multifamily*':pal[1],'MIOT resid. repairs/alterations':pal[2], 'MIOT resid. other':pal[3],\
              'MIOT highways & streets*':pal[4], 'PCA new single family buildings':pal[0], 'PCA new multi-family buildings':pal[1], \
              'PCA res. buildungs improvements':pal[2], 'PCA highways & streets':pal[4], 'McK new single-family housing':pal[0], \
              'McK new multi-family housing':pal[1], 'McK new manufactued housing':pal[3], 'McK resid. repair & remodeling':pal[2]}
					
marker_dict_low = {'MIOT new single-family*':'.-','MIOT new-multifamily*':'.-','MIOT resid. repairs/alterations':'.-', 'MIOT resid. other':'.-',\
              'MIOT highways & streets*':'.-',  'McK new single-family housing':'^', 'McK new multi-family housing':'^',
               'McK new manufactued housing':'^', 'McK resid. repair & remodeling':'^'}

name_list1_low = ['cement_detail', 'wood_detail']
plot_list1_low = [eval(e) for e in name_list1_low ]


k,i,j = 0,0,0     
for i in range(2,3):
    for j in range (0,2):
        try:
            plot_list1_low[k].plot(ax=axs[i,j], color = [color_dict_low.get(r,pal[0]) for r in plot_list1_low[k]], style = [marker_dict_low.get(r, '*') for r in plot_list1_low[k]], kind='line', title= name_list1_low [k][:-7], legend = False)
            #plot_list1_low[k].iloc[np.r_[0:7,8],:4].plot(ax=axs[i], color = [color_dict_low.get(r,pal[0]) for r in plot_list1_low[k]], style = [marker_dict_low.get(r, '*') for r in plot_list1_low[k]], kind='line', title= name_list1_low [k][:-7], legend = False)
            #plot_list1_low[k].iloc[np.r_[1:9,13],:4].plot(ax=axs[i], color = [color_dict_low.get(r,pal[0]) for r in plot_list1_low[k]], style = [marker_dict_low.get(r, '*') for r in plot_list1_low[k]], kind='line', title= name_list1_low [k][:-7], legend = False)
            k = k+1
            axs[i,j].set_ylabel('%')
        except:
            continue
        
plot_list1_low[0].iloc[np.r_[1:9,13],:].plot(ax=axs[2,0], color = [color_dict_low.get(r) for r in plot_list1_low[0]], style = [marker_dict_low.get(r, '*') for r in plot_list1_low[0]], kind='line', title= name_list1_low [0][:-7], legend = False)
plot_list1_low[1].iloc[np.r_[0:7,8],:3].plot(ax=axs[2,1], color = [color_dict_low.get(r) for r in plot_list1_low[1]], style = [marker_dict_low.get(r, '*') for r in plot_list1_low[1]], kind='line', title= name_list1_low [1][:-7], legend = False)
plot_list1_low[1].iloc[np.r_[0:6,8],3].plot(ax=axs[2,1], color = pal[3], style = [marker_dict_low.get(r, '*') for r in plot_list1_low[1]], kind='line', title= name_list1_low [1][:-7], legend = False)
                  

##lgd medium plot:
lgd = axs[1,2].legend(loc='center', fontsize=12) #, bbox_to_anchor=(0.01, 0.5),fontsize=14)

def add_line(legend):
    ax1 = legend.axes
    from matplotlib.lines import Line2D

    import matplotlib.patches as mpatches
    handles, labels = axs[1,0].get_legend_handles_labels()
    legend._legend_box = None
    legend._init_legend_box(handles, labels)
    legend._set_loc(legend._loc)
    legend.set_title(legend.get_title().get_text())
           
add_line(lgd)
    

#lgd low plot
lgd_low = axs[2,2].legend(loc='center', fontsize=12) #, bbox_to_anchor=(0.01, 0.5),fontsize=14)

def add_line(legend):
    ax1 = legend.axes
    from matplotlib.lines import Line2D

    import matplotlib.patches as mpatches
    a = axs[2,0].get_legend_handles_labels()[0][:9] + axs[2,1].get_legend_handles_labels()[0][4:8]
    b = axs[2,0].get_legend_handles_labels()[1][:9] + axs[2,1].get_legend_handles_labels()[1][4:8]
    c = tuple((a,b))
    handles, labels = c
    legend._legend_box = None
    legend._init_legend_box(handles, labels)
    legend._set_loc(legend._loc)
    legend.set_title(legend.get_title().get_text())
           
add_line(lgd_low)

axs[2,0].set_xticks([1963,1972,1982,1992,2002,2015])
axs[2,1].set_xticks([1967,1972,1977,1982,1987,1992,1997,2002,2007])
axs[2,0].xaxis.label.set_visible(False)
axs[2,0].xaxis.label.set_visible(False)

fig.suptitle('Comparison of end-use shares - medium & low sector aggregation', y=1, fontsize = 16)
fig.tight_layout()




'''
 Create detailed plots for WOOD and CEMENT in the CONSTRUCTION SECTOR
 '''
# isolate construction sector sub-sectors and save in excel for manual processing
# (no automatic processing as different for each year)
# constr_1963 = HTWio_detail_dict.get(1963).iloc[19:26,:]
# constr_1967 = HTWio_detail_dict.get(1967).iloc[26:76,:]
# constr_1972 = HTWio_detail_dict.get(1972).iloc[26:76,:]
# constr_1977 = HTWio_detail_dict.get(1977).iloc[30:83,:]
# constr_1982 = HTWio_detail_dict.get(1982).iloc[30:83,:]
# constr_1987 = HTWio_detail_dict.get(1987).iloc[30:83,:]
# constr_1992 = HTWio_detail_dict.get(1992).iloc[30:45,:] #checl if to add to this and the above minign stuff
# constr_1997 = HTWio_detail_dict.get(1997).iloc[26:45,:]
# constr_2002 = HTWio_detail_dict.get(2002).iloc[27:40,:]
# constr_2007 = HTWio_detail_dict.get(2007).iloc[19:36,:] 
# constr_2012 = HTWio_detail_dict.get(2012).iloc[19:36,:] 

# # save to Excel, including used filter matrices
# writer = pd.ExcelWriter(data_path_usa + '/Construction_detail' + '_Run_{}.xlsx'.format(pd.datetime.today().strftime('%y%m%d-%H%M%S')))
# constr_1963.to_excel(writer,'1963')
# constr_1967.to_excel(writer,'1967')
# constr_1972.to_excel(writer,'1972')
# constr_1977.to_excel(writer,'1977')
# constr_1982.to_excel(writer,'1982')
# constr_1987.to_excel(writer,'1987')
# constr_1992.to_excel(writer,'1992')
# constr_1997.to_excel(writer,'1997')
# constr_2002.to_excel(writer,'2002')
# constr_2007.to_excel(writer,'2007')
# constr_2012.to_excel(writer,'2012')
# writer.save()

wood_detail = pd.read_excel(data_path_usa + 'Construction_detail_Run_220317-102202_manualEdit.xlsx',sheet_name='Wood_out', index_col=[0])
cement_detail = pd.read_excel(data_path_usa + 'Construction_detail_Run_220317-102202_manualEdit.xlsx',sheet_name='Cement_out', index_col=[0])


  
'''PLOT: low sector aggregation'''

pal = sns.color_palette("colorblind") 
color_dict = {'MIOT new single-family*':pal[0],'MIOT new-multifamily*':pal[1],'MIOT resid. repairs/alterations':pal[2], 'MIOT resid. other':pal[3],\
              'MIOT highways & streets*':pal[4], 'PCA new single family buildings':pal[0], 'PCA new multi-family buildings':pal[1], \
              'PCA res. buildungs improvements':pal[2], 'PCA highways & streets':pal[4], 'McK new single-family housing':pal[0], \
              'McK new multi-family housing':pal[1], 'McK new manufactued housing':pal[3], 'McK resid. repair & remodeling':pal[2]}
					
marker_dict = {'MIOT new single-family*':'.-','MIOT new-multifamily*':'.-','MIOT resid. repairs/alterations':'.-', 'MIOT resid. other':'.-',\
              'MIOT highways & streets*':'.-',  'McK new single-family housing':'^', 'McK new multi-family housing':'^',
               'McK new manufactued housing':'^', 'McK resid. repair & remodeling':'^'}

name_list1 = ['cement_detail', 'wood_detail']
plot_list1 = [eval(e) for e in name_list1]


k,i,j = 0,0,0     
fig, axs = plt.subplots(1,3 ,sharex=False, sharey=False, figsize=(14,5))
axs[2].axis('off')

for i in range(0,3):
        try:
            plot_list1[k].plot(ax=axs[i], color = [color_dict.get(r,pal[0]) for r in plot_list1[k]], style = [marker_dict.get(r, '*') for r in plot_list1[k]], kind='line', title= name_list1[k][:-7], legend = False)
            #plot_list1[k].iloc[np.r_[0:7,8],:4].plot(ax=axs[i], color = [color_dict.get(r,pal[0]) for r in plot_list1[k]], style = [marker_dict.get(r, '*') for r in plot_list1[k]], kind='line', title= name_list1[k][:-7], legend = False)
            #plot_list1[k].iloc[np.r_[1:9,13],:4].plot(ax=axs[i], color = [color_dict.get(r,pal[0]) for r in plot_list1[k]], style = [marker_dict.get(r, '*') for r in plot_list1[k]], kind='line', title= name_list1[k][:-7], legend = False)
            k = k+1
            axs[i,j].set_ylabel('%')
        except:
            continue
        
plot_list1[0].iloc[np.r_[1:9,13],:].plot(ax=axs[0], color = [color_dict.get(r) for r in plot_list1[0]], style = [marker_dict.get(r, '*') for r in plot_list1[0]], kind='line', title= name_list1[0][:-7], legend = False)
plot_list1[1].iloc[np.r_[0:7,8],:3].plot(ax=axs[1], color = [color_dict.get(r) for r in plot_list1[1]], style = [marker_dict.get(r, '*') for r in plot_list1[1]], kind='line', title= name_list1[1][:-7], legend = False)
plot_list1[1].iloc[np.r_[0:6,8],3].plot(ax=axs[1], color = pal[3], style = [marker_dict.get(r, '*') for r in plot_list1[1]], kind='line', title= name_list1[1][:-7], legend = False)
                  
lgd = axs[2].legend(loc='center', fontsize=14) #, bbox_to_anchor=(0.01, 0.5),fontsize=14)

def add_line(legend):
    ax1 = legend.axes
    from matplotlib.lines import Line2D

    import matplotlib.patches as mpatches
    a = axs[0].get_legend_handles_labels()[0][:9] + axs[1].get_legend_handles_labels()[0][4:8]
    b = axs[0].get_legend_handles_labels()[1][:9] + axs[1].get_legend_handles_labels()[1][4:8]
    c = tuple((a,b))
    handles, labels = c
    legend._legend_box = None
    legend._init_legend_box(handles, labels)
    legend._set_loc(legend._loc)
    legend.set_title(legend.get_title().get_text())
           
add_line(lgd)

axs[0].set_xticks([1963,1972,1982,1992,2002,2015])
axs[1].set_xticks([1967,1972,1977,1982,1987,1992,1997,2002,2007])

fig.suptitle('Comparison of end-use shares - low sector aggregation (HT-WIO)', y=1, fontsize = 16)
fig.tight_layout()



'''
    #4 Assemble comparison of Exiobase countries and sectors (selected method)
    --> add global end-use data!!
'''

'''FOR NOW: assemnle old Exiobase data till calculated anew'''
data_path_exio = os.path.join('C:/Users/jstreeck/Desktop/EndUse_shortTermSave/Exiobase/output/')


year = 1995

years_exio = list(range(1995,2012))
regions = ['US','AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI', 'FR', 'GR',\
  'HR', 'HU', 'IE', 'IT', 'US', 'LT', 'LU', 'LV', 'MT', 'NL', 'PL', 'PT', 'RO',\
      'SE', 'SI', 'SK', 'GB','JP', 'CN', 'CA', 'KR', 'BR', 'IN', 'MX',\
      'RU', 'AU', 'CH', 'TR', 'TW', 'NO', 'ID', 'ZA', 'WA', 'WL', 'WE', 'WF',\
        'WM'] #'US' not in above as already run
    
# exio_sectors = ['Construction', 'Machinery and equipment n.e.c. ',
#        'Office machinery and computers (30)',
#        'Electrical machinery and apparatus n.e.c. (31)',
#        'Radio, television and communication equipment and apparatus (32)',
#        'Medical, precision and optical instruments, watches and clocks (33)',
#        'Motor vehicles, trailers and semi-trailers (34)',
#        'Other transport equipment (35)',
#        'Furniture; other manufactured goods n.e.c. (36)', 'Textiles (17)',
#        'Printed matter and recorded media (22)', 'Food', 'Other raw materials',
#        'Secondary materials', 'Energy carriers', 'Energy carriers.1', 'Other',
#        'Products nec', 'Services']
    

Exio_dict = {}
for region in regions:
    Region_dict = {}
    for year in years_exio:
        for file in glob.glob(os.path.join((data_path_exio + 'Exio_HT_WIOMF_' + str(year) + '_' + region + '*.xlsx'))):
            Region_single = pd.read_excel(file, sheet_name='EndUse_shares_agg',index_col=[0,1],header=[0])
        Region_dict[year] = Region_single
    Exio_dict[region] = Region_dict

# single country all end-uses plot:
materials = ['steel', 'wood', 'Plastic', 'glass', 'alumin', 'tin', 'Copper']

region_dict ={}

for region in regions:
    material_dict = []
    for material in materials:
        material_single = []
        material_df = pd.DataFrame([], index=Exio_dict.get(region).get(year).index.get_level_values(1), columns=years_exio)
        for year in years_exio:
            material_single = Exio_dict.get(region).get(year).iloc[:,Exio_dict.get(region).get(year).columns.get_level_values(0).map(lambda t: (material) in t).to_list()]
            material_df[year] = material_single.values
        material_dict.append(material_df)        
        dict_1 = dict(zip(materials,material_dict))
    region_dict.update({region:dict_1})


### LOAD PHYSICAL SHIPMENT DATA
load_path = 'C:/Users/jstreeck/Desktop/EndUse_shortTermSave/SectorSplit_WasteFilter_physical/Global'

#Intern = many countries, global = resl. for whole globe, country_name = data only for that country
physSplit_cement_Intern = pd.read_excel(load_path + '/2017_Cao_Cement_Split data.xlsx', sheet_name='Data_manip') #not applicable for Exiobase (only if using GLORIA)
physSplit_plastics_Intern  = pd.read_excel(load_path + '/EUROMAP.xlsx', sheet_name='clean data manip')
physSplit_plastics_China  = pd.read_excel(load_path + '/Plastics_ChinaEU28.xlsx', sheet_name='China').set_index('Year')*100
physSplit_plastics_EU28  = pd.read_excel(load_path + '/Plastics_ChinaEU28.xlsx', sheet_name='EU28').set_index('Year')*100

physSplit_steel_China = pd.read_excel(load_path + '/IronSteel.xlsx', sheet_name='China').set_index('Year')*100
physSplit_steel_India = pd.read_excel(load_path + '/IronSteel.xlsx', sheet_name='India').set_index('Year')*100
physSplit_steel_UK = pd.read_excel(load_path + '/IronSteel.xlsx', sheet_name='UK').set_index('Year')*100
physSplit_copper_EU28 = pd.read_excel(load_path + '/Copper.xlsx', sheet_name='EU').set_index('Year')*100
EU28 = ['GB', 'FR','IT','DE', 'PT', 'RU'] #might require expansion

physSplit_alu_intern = pd.read_excel(load_path + '/2013_Liu_AluData.xlsx', sheet_name='Liu_out', index_col=[0], header=[0,1])*100




'''EXIOBASE PLOTS & DATA ASSEMBLY FOR PLOTS'''



#Plot SELECTED COUNTRIES and MATERIALS, ALL END USES
plotRegions = ['CN', 'IN','GB']#['US', 'JP', 'GB', 'FR','IT','DE', 'PT', 'RU', 'IN','CN', 'ID', 'ZA']
region_transl = {'PT':'Portugal', 'US':'USA', 'GB':'Great Britain', 'FR':'France','IT':'Italy',\
                 'DE':'Germany','IN':'India','CN':'China','RU':'Russia','ZA':'South Africa', \
                 'JP':'Japan', 'AT':'Austria', 'AU':'Australia', 'BE':'Belgium', 'BR':'Brazil',\
                 'NL':'Netherlands', 'NO':'Norway', 'ES':'Spain', 'CH':'Switzerland'}
plotMaterials = [ 'Plastic', 'steel', 'Copper', 'alumin']
#plotMaterials = ['steel', 'wood', 'Plastic', 'glass', 'alumin', 'tin', 'Copper']

for plotMaterial in plotMaterials:
    for plotRegion in plotRegions:
        region_dict.get(plotRegion).get(plotMaterial).T.plot(kind='line',marker='o', title= (plotRegion + ' ' +plotMaterial) )
        plt.legend(bbox_to_anchor=(1,1), loc="upper left")
        plt.show()




#####



##assemble dictionary to use in COMPOUNT FIGURE construction later
lala_dict = {}
for plotMaterial in plotMaterials:
    Exio_region_plotDict = []
    for plotRegion in plotRegions:
        randomlist = []
        dict_2={}
        plot_frame = region_dict.get(plotRegion).get(plotMaterial).T
        plot_frame['Other machinery & appliances'] =  plot_frame['Machinery and equipment n.e.c. '] + \
            plot_frame['Medical, precision and optical instruments, watches and clocks (33)']
        plot_frame['Electrical machinery & appliances'] =  plot_frame['Office machinery and computers (30)'] + \
            plot_frame['Radio, television and communication equipment and apparatus (32)']+ \
               plot_frame['Electrical machinery and apparatus n.e.c. (31)']
        plot_frame['Transportation'] = plot_frame['Motor vehicles, trailers and semi-trailers (34)'] + \
            plot_frame['Other transport equipment (35)']
        plot_frame['All other'] = plot_frame['Printed matter and recorded media (22)'] + plot_frame['Other raw materials']+\
             + plot_frame['Secondary materials'] + plot_frame['Energy carriers'] + plot_frame[ 'Energy carriers.1'] \
                 + plot_frame[ 'Other'] + plot_frame[ 'Products nec'] + plot_frame['Services']
        if plotMaterial == 'Plastic':
            try:
                plot_frame['Packaging_Euromap'] = physSplit_plastics_Intern.loc[physSplit_plastics_Intern['Country'] == region_transl.get(plotRegion)].iloc[:,1:].set_index('Application').transpose()['Packaging']
                plot_frame['Automotive_Euromap'] = physSplit_plastics_Intern.loc[physSplit_plastics_Intern['Country'] == region_transl.get(plotRegion)].iloc[:,1:].set_index('Application').transpose()['Automotive']
                plot_frame['Electrical_Euromap'] = physSplit_plastics_Intern.loc[physSplit_plastics_Intern['Country'] == region_transl.get(plotRegion)].iloc[:,1:].set_index('Application').transpose()['Construction industry']
                plot_frame['Construction_Euromap'] = physSplit_plastics_Intern.loc[physSplit_plastics_Intern['Country'] == region_transl.get(plotRegion)].iloc[:,1:].set_index('Application').transpose()['Electrical, electronics & telecom']
                plot_frame['Other_Euromap'] = physSplit_plastics_Intern.loc[physSplit_plastics_Intern['Country'] == region_transl.get(plotRegion)].iloc[:,1:].set_index('Application').transpose()['Others']
            except:
                continue
            if plotRegion == 'CN':
                plot_frame['Jiang_Packaging'] = physSplit_plastics_China['Packaging']
                plot_frame['Jiang_B&C'] = physSplit_plastics_China['B&C']
                plot_frame['Jiang_Automobile'] = physSplit_plastics_China['Automobile']
                plot_frame['Jiang_Electronics'] = physSplit_plastics_China['Electronics']
                plot_frame['Jiang_Agriculture'] = physSplit_plastics_China['Agriculture']
                plot_frame['Jiang_Others'] = physSplit_plastics_China['Others']
            if plotRegion in EU28: #watch out: EU28 list not complete
                plot_frame['PlastEU_Packaging'] = physSplit_plastics_EU28['Packaging PE']
                plot_frame['PlastEU_B&C'] = physSplit_plastics_EU28['Building and construction PE']
                plot_frame['PlastEU_Automotive'] = physSplit_plastics_EU28['Automotive PE']
                plot_frame['PlastEU_Electrical'] = physSplit_plastics_EU28['Electrical&Electronic PE']
                plot_frame['PlastEU_Agriculture'] = physSplit_plastics_EU28['Agriculture PE']
                plot_frame['PlastEU_Others'] = physSplit_plastics_EU28['Others PE']
                
        if plotMaterial == 'steel':
            if plotRegion == 'CN':
                plot_frame['Wang_Construction'] = physSplit_steel_China['RFSCon']
                plot_frame['Wang_Transportation'] = physSplit_steel_China['RFSTra']
                plot_frame['Wang_Machinery'] = physSplit_steel_China['RFSM']
                plot_frame['Wang_Appliances'] = physSplit_steel_China['RFSA']
                plot_frame['Wang_Other'] = physSplit_steel_China['RFSOth']
            if plotRegion == 'IN':
                plot_frame['Pauliuk_Construction'] = physSplit_steel_India['construction']
                plot_frame['Pauliuk_Transportation'] = physSplit_steel_India['transportation']
                plot_frame['Pauliuk_Machinery'] = physSplit_steel_India['machinery']
                plot_frame['Pauliuk_Products'] = physSplit_steel_India['products']
            if plotRegion == 'GB':
                plot_frame['Pauliuk_Construction'] = physSplit_steel_UK['Construction']
                plot_frame['Pauliuk_Transportation'] = physSplit_steel_UK['Transportation']
                plot_frame['Pauliuk_Machinery'] = physSplit_steel_UK['Machinery']
                plot_frame['Pauliuk_Products'] = physSplit_steel_UK['Products']
        
        if plotMaterial == 'Copper':
            if plotRegion in EU28: #watch out: EU28 list not complete
                plot_frame['Ciacci_B&C'] = physSplit_copper_EU28['Building and construction']
                plot_frame['Ciacci_Electrical'] = physSplit_copper_EU28['Electrical and Electronic Goods']
                plot_frame['Ciacci_Machinery'] = physSplit_copper_EU28['Industrial Machinery and Equipment']
                plot_frame['Ciacci_Transportation'] = physSplit_copper_EU28['Transportation Equipment']
                plot_frame['Ciacci_Products'] = physSplit_copper_EU28['Consumer and General Products']
        
        if plotMaterial == 'alumin':
            try:
                alu_shipment = physSplit_alu_intern.xs(region_transl.get(plotRegion), level=0, axis=1)
                plot_frame['Liu_building&construction'] = alu_shipment['B&C']
                plot_frame['Liu_Transport'] = alu_shipment['Trans']
                plot_frame['Liu_Machinery&equipment'] = alu_shipment['M&E']
                plot_frame['Liu_Electric&electronics'] = alu_shipment['EE']
                plot_frame['Liu_Containers&packaging']= alu_shipment['C&P']
                plot_frame['Liu_Consumer Durables'] = alu_shipment['ConDur']
                plot_frame['Liu_Others'] = alu_shipment['Others']
            except:
                continue
        
        Exio_region_plotDict.append(plot_frame) 
        dict_2 = dict(zip(plotRegions,Exio_region_plotDict))
    lala_dict.update({plotMaterial:dict_2})   
    
    
    
    
#######   
    
    
    
##individual plots of dictionary
for plotRegion in plotRegions:                    
    for plotMaterial in plotMaterials:
        plot_graph = lala_dict.get(plotMaterial).get(plotRegion)
        style=['+-', 'o-', '.--', 's:']
        for i in range(0,plot_graph.shape[1]):
            n = random.randint(0,3)
            randomlist.append(n)
        c = [style[i] for i in randomlist]
        plot_graph.plot(kind='line',style=c, title= (plotRegion + ' ' +plotMaterial) )
        plt.legend(bbox_to_anchor=(1,1), loc="upper left")
        plt.show()
        
 
###direct plotting     
# for plotMaterial in plotMaterials:
#     for plotRegion in plotRegions:
#         randomlist = []
#         plot_frame = region_dict.get(plotRegion).get(plotMaterial).T
#         if plotMaterial == 'Plastic':
#             try:
#                 plot_frame['Packaging_Euromap'] = physSplit_plastics_Intern.loc[physSplit_plastics_Intern['Country'] == region_transl.get(plotRegion)].iloc[:,1:].set_index('Application').transpose()['Packaging']
#                 plot_frame['Automotive_Euromap'] = physSplit_plastics_Intern.loc[physSplit_plastics_Intern['Country'] == region_transl.get(plotRegion)].iloc[:,1:].set_index('Application').transpose()['Automotive']
#                 plot_frame['Electrical_Euromap'] = physSplit_plastics_Intern.loc[physSplit_plastics_Intern['Country'] == region_transl.get(plotRegion)].iloc[:,1:].set_index('Application').transpose()['Construction industry']
#                 plot_frame['Construction_Euromap'] = physSplit_plastics_Intern.loc[physSplit_plastics_Intern['Country'] == region_transl.get(plotRegion)].iloc[:,1:].set_index('Application').transpose()['Electrical, electronics & telecom']
#                 plot_frame['Other_Euromap'] = physSplit_plastics_Intern.loc[physSplit_plastics_Intern['Country'] == region_transl.get(plotRegion)].iloc[:,1:].set_index('Application').transpose()['Others']
#             except:
#                 continue
#             if plotRegion == 'CN':
#                 plot_frame['Jiang_Packaging'] = physSplit_plastics_China['Packaging']
#                 plot_frame['Jiang_B&C'] = physSplit_plastics_China['B&C']
#                 plot_frame['Jiang_Automobile'] = physSplit_plastics_China['Automobile']
#                 plot_frame['Jiang_Electronics'] = physSplit_plastics_China['Electronics']
#                 plot_frame['Jiang_Agriculture'] = physSplit_plastics_China['Agriculture']
#                 plot_frame['Jiang_Others'] = physSplit_plastics_China['Others']
#             if plotRegion in EU28: #watch out: EU28 list not complete
#                 plot_frame['PlastEU_Packaging'] = physSplit_plastics_EU28['Packaging PE']
#                 plot_frame['PlastEU_B&C'] = physSplit_plastics_EU28['Building and construction PE']
#                 plot_frame['PlastEU_Automotive'] = physSplit_plastics_EU28['Automotive PE']
#                 plot_frame['PlastEU_Electrical'] = physSplit_plastics_EU28['Electrical&Electronic PE']
#                 plot_frame['PlastEU_Agriculture'] = physSplit_plastics_EU28['Agriculture PE']
#                 plot_frame['PlastEU_Others'] = physSplit_plastics_EU28['Others PE']
                
#         if plotMaterial == 'steel':
#             if plotRegion == 'CN':
#                 plot_frame['Wang_Construction'] = physSplit_steel_China['RFSCon']
#                 plot_frame['Wang_Transportation'] = physSplit_steel_China['RFSTra']
#                 plot_frame['Wang_Machinery'] = physSplit_steel_China['RFSM']
#                 plot_frame['Wang_Appliances'] = physSplit_steel_China['RFSA']
#                 plot_frame['Wang_Other'] = physSplit_steel_China['RFSOth']
#             if plotRegion == 'IN':
#                 plot_frame['Pauliuk_Construction'] = physSplit_steel_India['construction']
#                 plot_frame['Pauliuk_Transportation'] = physSplit_steel_India['transportation']
#                 plot_frame['Pauliuk_Machinery'] = physSplit_steel_India['machinery']
#                 plot_frame['Pauliuk_Products'] = physSplit_steel_India['products']
#             if plotRegion == 'GB':
#                 plot_frame['Pauliuk_Construction'] = physSplit_steel_UK['Construction']
#                 plot_frame['Pauliuk_Transportation'] = physSplit_steel_UK['Transportation']
#                 plot_frame['Pauliuk_Machinery'] = physSplit_steel_UK['Machinery']
#                 plot_frame['Pauliuk_Products'] = physSplit_steel_UK['Products']
        
#         if plotMaterial == 'Copper':
#             if plotRegion in EU28: #watch out: EU28 list not complete
#                 plot_frame['Ciacci_B&C'] = physSplit_copper_EU28['Building and construction']
#                 plot_frame['Ciacci_Electrical'] = physSplit_copper_EU28['Electrical and Electronic Goods']
#                 plot_frame['Ciacci_Machinery'] = physSplit_copper_EU28['Industrial Machinery and Equipment']
#                 plot_frame['Ciacci_Transportation'] = physSplit_copper_EU28['Transportation Equipment']
#                 plot_frame['Ciacci_Products'] = physSplit_copper_EU28['Consumer and General Products']
#         style=['+-', 'o-', '.--', 's:']
#         for i in range(0,plot_frame.shape[1]):
#             n = random.randint(0,3)
#             randomlist.append(n)
#         c = [style[i] for i in randomlist]
#         plot_frame.plot(kind='line',style=c, title= (plotRegion + ' ' +plotMaterial) )
#         plt.legend(bbox_to_anchor=(1,1), loc="upper left")
#         plt.show()
        







###PLOTS ALL COUNTRIES 1 material, one end-use
#ALU CONSTRUCTION
end_use_all_aluConst =  pd.DataFrame([])# index=years_exio, columns=regions)
for region in regions:
    end_use_region = pd.DataFrame(region_dict.get(region).get('alumin').loc['Construction']).rename(columns = {'Construction':region})
    end_use_all_aluConst[region] = end_use_region
del end_use_region
#end_use_all.T.plot( kind='box', title= 'Copper to Construction')


#Steel CONSTRUCTION
end_use_all_steelConst =  pd.DataFrame([])# index=years_exio, columns=regions)
for region in regions:
    end_use_region = pd.DataFrame(region_dict.get(region).get('steel').loc['Construction']).rename(columns = {'Construction':region})
    end_use_all_steelConst[region] = end_use_region
del end_use_region

#Steel MOTOR VEHICLES
end_use_all_steelMotor =  pd.DataFrame([])# index=years_exio, columns=regions)
for region in regions:
    end_use_region = pd.DataFrame(region_dict.get(region).get('steel').loc['Motor vehicles, trailers and semi-trailers (34)']).rename(columns = {'Construction':region})
    end_use_all_steelMotor[region] = end_use_region
del end_use_region


'''PLOT: EXIOBASE - combine region-level with all-region plots'''

# pal = sns.color_palette("colorblind") 

# marker_dict = {'CBA':'o', 'WIO-MFA': 'o', 'Ghosh-IO AMC':'o',  \
#               'Partial Ghosh-IO': 'o', 'HT-WIO': 'v', 'Exio_HT-WIO': '.'}
# name_list1 = ['wood_residential_df', 'wood_nonresidential_df', 'cement_residential_df', 'cement_nonRes_df', 'cement_CE_df']
# plot_list1 = [eval(e) for e in name_list1]

                 
dropped_sectors = ['Machinery and equipment n.e.c. ', 'Medical, precision and optical instruments, watches and clocks (33)', \
                   'Office machinery and computers (30)','Radio, television and communication equipment and apparatus (32)',\
                    'Electrical machinery and apparatus n.e.c. (31)', 'Office machinery and computers (30)',  'Motor vehicles, trailers and semi-trailers (34)',
                    'Other transport equipment (35)', 'Secondary materials', 'Printed matter and recorded media (22)', 'Other raw materials',\
                      'Energy carriers','Energy carriers.1','Other','Products nec', 'Services' ]

pal = sns.color_palette("colorblind")
 
color_dict = {'Construction':pal[0], 'Packaging_Euromap':pal[4], 'Automotive_Euromap':pal[1],'Electrical_Euromap':pal[2],'Construction_Euromap':pal[0],
              'Other_Euromap':pal[7],'Jiang_Packaging':pal[4], 'Jiang_B&C':pal[0], 'Jiang_Automobile':pal[1],'Jiang_Electronics':pal[2],'Jiang_Agriculture':pal[8], 'Jiang_Others':pal[5],
'PlastEU_Packaging':pal[4], 'PlastEU_B&C':pal[0], 'PlastEU_Automotive':pal[1], 'PlastEU_Electrical':pal[2], 'PlastEU_Agriculture':pal[7],
'PlastEU_Others':pal[7], 'Wang_Construction':pal[0], 'Wang_Transportation':pal[1], 'Wang_Machinery':pal[3], 'Wang_Appliances':pal[3], 
'Wang_Other':pal[7], 'Pauliuk_Construction':pal[0], 'Pauliuk_Transportation':pal[1], 'Pauliuk_Machinery':pal[3],'Pauliuk_Products':pal[5],
 'Ciacci_B&C':pal[0], 'Ciacci_Electrical':pal[2], 'Ciacci_Machinery':pal[3], 'Ciacci_Transportation':pal[1], 'Ciacci_Products':pal[5],
 'Electrical machinery & appliances':pal[2], 'Transportation':pal[1], 'Other machinery & appliances':pal[3], 
 'Furniture; other manufactured goods n.e.c. (36)':pal[7], 'Textiles (17)':pal[9], 'Food':pal[9], 'All other':pal[5],
 'Liu_building&construction':pal[0], 'Liu_Transport':pal[1], 'Liu_Machinery&equipment':pal[3], 'Liu_Electric&electronics':pal[2],
 'Liu_Containers&packaging':pal[4], 'Liu_Consumer Durables':pal[7], 'Liu_Others':pal[7] } 

marker_dict = {'Construction':'.-', 'Electrical machinery & appliances':'.-', 'Transportation':'.-', 
               'Other machinery & appliances':'.-', 'Furniture; other manufactured goods n.e.c. (36)':'.-', 
               'Textiles (17)':'.-', 'Food':'.-', 'All other':'.-' }



china_steel = lala_dict.get('steel').get('CN').replace(0,np.nan).drop(dropped_sectors,axis=1)
india_steel = lala_dict.get('steel').get('IN').replace(0,np.nan).drop(dropped_sectors,axis=1)
britain_steel= lala_dict.get('steel').get('GB').replace(0,np.nan).drop(dropped_sectors,axis=1)
china_alumin = lala_dict.get('alumin').get('CN').replace(0,np.nan).drop(dropped_sectors,axis=1)
india_alumin = lala_dict.get('alumin').get('IN').replace(0,np.nan).drop(dropped_sectors,axis=1)
britain_alumin= lala_dict.get('alumin').get('GB').replace(0,np.nan).drop(dropped_sectors,axis=1)
china_Plastic = lala_dict.get('Plastic').get('CN').replace(0,np.nan).drop(dropped_sectors,axis=1)
india_Plastic = lala_dict.get('Plastic').get('IN').replace(0,np.nan).drop(dropped_sectors,axis=1)
britain_Plastic= lala_dict.get('Plastic').get('GB').replace(0,np.nan).drop(dropped_sectors,axis=1)

    'Construction', ,
          
fig, axs = plt.subplots(4,3 ,sharex=False, sharey=False, figsize=(14,14))
#axs[3,2].axis('off')

#check if summing up to 100%
#lafa = lala_dict.get('steel').get('CN').drop(dropped_sectors,axis=1)

china_steel.plot(ax=axs[0,0], kind='line', title= 'Steel China', legend = False, color= [color_dict.get(r) for r in china_steel], style=[marker_dict.get(r, '*') for r in china_steel])
india_steel.plot(ax=axs[0,1], kind='line',title= 'Steel India', legend = False, color= [color_dict.get(r) for r in india_steel], style=[marker_dict.get(r, '*') for r in india_steel])
britain_steel.plot(ax=axs[0,2], kind='line', title= 'Steel UK', legend = False, color= [color_dict.get(r) for r in britain_steel], style=[marker_dict.get(r, '*') for r in britain_steel])
china_alumin.plot(ax=axs[1,0], kind='line', title= 'Aluminum China', legend = False, color= [color_dict.get(r) for r in china_alumin], style=[marker_dict.get(r, '*') for r in china_alumin])
india_alumin.plot(ax=axs[1,1], kind='line',title= 'Aluminum India', legend = False, color= [color_dict.get(r) for r in india_alumin], style=[marker_dict.get(r, '*') for r in india_alumin])
britain_alumin.plot(ax=axs[1,2], kind='line', title= 'Aluminum UK', legend = False, color= [color_dict.get(r) for r in britain_alumin], style=[marker_dict.get(r, '*') for r in britain_alumin])
china_Plastic.plot(ax=axs[2,0], kind='line', title= 'Plastics China', legend = False, color= [color_dict.get(r) for r in china_Plastic], style=[marker_dict.get(r, '*') for r in china_Plastic])
india_Plastic.plot(ax=axs[2,1], kind='line',title= 'Plastics India', legend = False, color= [color_dict.get(r) for r in india_Plastic], style=[marker_dict.get(r, '*') for r in india_Plastic])
britain_Plastic.plot(ax=axs[2,2], kind='line', title= 'Plastics UK', legend = False, color= [color_dict.get(r) for r in britain_Plastic], style=[marker_dict.get(r, '*') for r in britain_Plastic])
# axs[0,0].set_ylim(5,lala_dict.get('steel').get('CN').max().max()+5)
# axs[0,1].set_ylim(5,lala_dict.get('steel').get('IN').max().max()+5)
# axs[0,2].set_ylim(5,lala_dict.get('steel').get('GB').max().max()+5)
sns.boxplot(ax=axs[3,0],data=end_use_all_aluConst.T,whis=[0, 100], width=.6, palette="vlag")
sns.swarmplot(ax=axs[3,0],data=end_use_all_aluConst.T, size=2)
sns.boxplot(ax=axs[3,1],data=end_use_all_steelConst.T,whis=[0, 100], width=.6, palette="vlag")
sns.swarmplot(ax=axs[3,1],data=end_use_all_steelConst.T, size=2)
sns.boxplot(ax=axs[3,2],data=end_use_all_steelMotor.T,whis=[0, 100], width=.6, palette="vlag")
sns.swarmplot(ax=axs[3,2],data=end_use_all_steelMotor.T, size=2)
axs[3,0].set(ylabel = '%', title = 'Aluminum Construction All Regions')
axs[3,1].set(ylabel = '%', title = 'Steel Construction All Regions')
axs[3,2].set(ylabel = '%', title = 'Steel Motor Vehicles All Regions')
axs[3,0].set_xticklabels(years_exio,fontsize = 6)
axs[3,1].set_xticklabels(years_exio,fontsize = 6)
axs[3,2].set_xticklabels(years_exio,fontsize = 6)
for i in range(0,3):
    for j in range (0,3):
            axs[i,j].set_ylabel('%')
            axs[i,j].set_xticks(list(range(1995,2012,2)))
 
lgd = fig.legend(loc='center left', bbox_to_anchor=(0.12, -0.12),fontsize=14, ncol=2) #, bbox_to_anchor=(0.01, 0.5),fontsize=14)

def add_line(legend):
    ax1 = legend.axes
    from matplotlib.lines import Line2D

    import matplotlib.patches as mpatches
    a = axs[0,0].get_legend_handles_labels()[0][:8] 
    b = axs[0,0].get_legend_handles_labels()[1][:8] 
    c = tuple((a,b))
    handles, labels = c
    legend._legend_box = None
    legend._init_legend_box(handles, labels)
    legend._set_loc(legend._loc)
    legend.set_title(legend.get_title().get_text())
    
    handles.append(Line2D([0],[0],color=pal[0],linewidth=3, marker='*', linestyle='None', markersize=9))
    labels.append("Shipment_Construction")
    handles.append(Line2D([0],[0],color=pal[1],linewidth=3, marker='*', linestyle='None', markersize=9))
    labels.append("Shipment_Transportation")
    handles.append(Line2D([0],[0],color=pal[2],linewidth=3, marker='*', linestyle='None', markersize=9))
    labels.append("Shipment_Electrical")
    handles.append(Line2D([0],[0],color=pal[3],linewidth=3, marker='*', linestyle='None', markersize=9))
    labels.append("Shipment_Machinery")
    handles.append(Line2D([0],[0],color=pal[4],linewidth=3, marker='*', linestyle='None', markersize=9))
    labels.append("Shipment_Packaging")
    handles.append(Line2D([0],[0],color=pal[7],linewidth=3, marker='*', linestyle='None', markersize=9))
    labels.append("Shipment_Other")
    
    legend._legend_box = None
    legend._init_legend_box(handles, labels)
    legend._set_loc(legend._loc)
    legend.set_title(legend.get_title().get_text())

           
add_line(lgd)
fig.suptitle('Exiobase end-uses for (a) selected regions and (b) selected end-uses', y=1, fontsize = 16)
#fig.suptitle('Comparison of end-use shares - high sector aggregation', y=1, fontsize = 16)
fig.tight_layout()

####---> match color codes and markers for shipments and categories

###---> plastics still going not much to food; might it here be better to not use HT-WIO but
# just WIO and then jsut assume that the plastics going to e.g. 'hotels and restaurants' is packaging????
#--> but in the end we dont know as which products the plastics go there ; so really, more resolution is required














#Plot VIOLIN PLOTS for ONE MATERIAL, ONE END-USE, ALL COUNTRIES
#COPPER

end_use_all =  pd.DataFrame([])# index=years_exio, columns=regions)
for region in regions:
    end_use_region = pd.DataFrame(region_dict.get(region).get('Copper').loc['Construction']).rename(columns = {'Construction':region})
    end_use_all[region] = end_use_region
#end_use_all.T.plot( kind='box', title= 'Copper to Construction')
ax =  sns.boxplot(data=end_use_all.T,whis=[0, 100], width=.6, palette="vlag")
ax =  sns.swarmplot(data=end_use_all.T, size=3, hue = end_use_all.T.index)
#sns.swarmplot(data=end_use_all.T,ax=ax,size=1)
ax.set_xticklabels(years_exio,fontsize = 7.5)
ax.set( ylabel = "%", title = 'Copper to Construction')
ax.annotate('blablabla', xy=(1997,0.5), xycoords='data', fontsize=20, color='r')
#ax.annotate('blablaa', xy=(90,'US'), xycoords='data', fontsize=20, color='r')
plt.show()
 # x, y, text
 
 ####---> I don't get, why annotation to plots does not work---

ax =  sns.swarmplot(data=end_use_all.T, size=3)
ax.annotate('blablabla', xy=(2000,8.0))

ax.annotate('blablabla', xy=(1997,90), xytext= (1997,90),arrowprops=dict(arrowstyle="->"))

ela=end_use_all.T.reset_index()
ela = pd.melt(ela,id_vars='index',value_vars=list(range(1995,2012)))

end_use_all =  pd.DataFrame([])# index=years_exio, columns=regions)
for region in regions:
    end_use_region = pd.DataFrame(region_dict.get(region).get('Copper').loc['Construction']).rename(columns = {'Construction':region})
    end_use_all[region] = end_use_region
#end_use_all.T.plot( kind='box', title= 'Copper to Construction')
ax =  sns.boxplot(data=end_use_all.T,whis=[0, 100], width=.6, palette="vlag")
ax =  sns.swarmplot(x = 'variable', y='value', data=ela, size=3)
#sns.swarmplot(data=end_use_all.T,ax=ax,size=1)
ax.set_xticklabels(years_exio,fontsize = 7.5)
ax.set( ylabel = "%", title = 'Copper to Construction')
ax.annotate('blablabla', xy=(80,1997))
#ax.annotate('blablaa', xy=(90,'US'), xycoords='data', fontsize=20, color='r')
plt.show()


lara = pd.DataFrame(end_use_all.idxmax(axis=1))
lral=end_use_all.max(axis=1)
lara['value'] = lral.iloc[:]
# label points on the plot
for x, y in zip(lara.index, lara['value']):
 # the position of the data label relative to the data point can be adjusted by adding/subtracting a value from the x &/ y coordinates
 plt.text(x = x, # x-coordinate position of data label
 y = y, # y-coordinate position of data label, adjusted to be 150 below the data point
 s = lara.loc[x][0], # data label, formatted to ignore decimals
 color = 'r') # set colour of line



#ALU CONSTRUCTION
end_use_all =  pd.DataFrame([])# index=years_exio, columns=regions)
for region in regions:
    end_use_region = pd.DataFrame(region_dict.get(region).get('alumin').loc['Construction']).rename(columns = {'Construction':region})
    end_use_all[region] = end_use_region
#end_use_all.T.plot( kind='box', title= 'Copper to Construction')
ax =  sns.boxplot(data=end_use_all.T,whis=[0, 100], width=.6, palette="vlag")
ax =  sns.swarmplot(data=end_use_all.T, size=3)

#Steel CONSTRUCTION
end_use_all =  pd.DataFrame([])# index=years_exio, columns=regions)
for region in regions:
    end_use_region = pd.DataFrame(region_dict.get(region).get('steel').loc['Construction']).rename(columns = {'Construction':region})
    end_use_all[region] = end_use_region
#end_use_all.T.plot( kind='box', title= 'Copper to Construction')
ax =  sns.boxplot(data=end_use_all.T,whis=[0, 100], width=.6, palette="vlag")
ax =  sns.swarmplot(data=end_use_all.T, size=3)


#Steel CONSTRUCTION
end_use_all =  pd.DataFrame([])# index=years_exio, columns=regions)
for region in regions:
    end_use_region = pd.DataFrame(region_dict.get(region).get('steel').loc['Construction']).rename(columns = {'Construction':region})
    end_use_all[region] = end_use_region
#end_use_all.T.plot( kind='box', title= 'Copper to Construction')
ax =  sns.boxplot(data=end_use_all.T,whis=[0, 100], width=.6, palette="vlag")
ax =  sns.swarmplot(data=end_use_all.T, size=3)

# ['Construction', 'Machinery and equipment n.e.c. ',
#        'Office machinery and computers (30)',
#        'Electrical machinery and apparatus n.e.c. (31)',
#        'Radio, television and communication equipment and apparatus (32)',
#        'Medical, precision and optical instruments, watches and clocks (33)',
#        'Motor vehicles, trailers and semi-trailers (34)',
#        'Other transport equipment (35)',
#        'Furniture; other manufactured goods n.e.c. (36)', 'Textiles (17)',
#        'Printed matter and recorded media (22)', 'Food', 'Other raw materials',
#        'Secondary materials', 'Energy carriers', 'Energy carriers.1', 'Other',
#        'Products nec', 'Services']

#Steel TRANSPORT
end_use_all =  pd.DataFrame([])# index=years_exio, columns=regions)
for region in regions:
    end_use_region = pd.DataFrame(region_dict.get(region).get('steel').loc['Motor vehicles, trailers and semi-trailers (34)'] \
        + region_dict.get(region).get('steel').loc['Other transport equipment (35)']).rename(columns = {'Construction':region})
    end_use_all[region] = end_use_region
#end_use_all.T.plot( kind='box', title= 'Copper to Construction')
ax =  sns.boxplot(data=end_use_all.T,whis=[0, 100], width=.6, palette="vlag")
ax =  sns.swarmplot(data=end_use_all.T, size=3)

#ALUTRANSPORT
end_use_all =  pd.DataFrame([])# index=years_exio, columns=regions)
for region in regions:
    end_use_region = pd.DataFrame(region_dict.get(region).get('alumin').loc['Motor vehicles, trailers and semi-trailers (34)'] \
        + region_dict.get(region).get('alumin').loc['Other transport equipment (35)']).rename(columns = {'Construction':region})
    end_use_all[region] = end_use_region
#end_use_all.T.plot( kind='box', title= 'Copper to Construction')
ax =  sns.boxplot(data=end_use_all.T,whis=[0, 100], width=.6, palette="vlag")
ax =  sns.swarmplot(data=end_use_all.T, size=3)

# plot histogram 
ax = sns.distplot(flights[‘passengers’], color=’#9d94ba’, bins=10, kde=False)
ax.set(title=’Distribution of Passengers’)# label each bar in histogram
for p in ax.patches:
 height = p.get_height() # get the height of each bar
 # adding text to each bar
 ax.text(x = p.get_x()+(p.get_width()/2), # x-coordinate position of data label, padded to be in the middle of the bar
 y = height+0.2, # y-coordinate position of data label, padded 0.2 above bar
 s = ‘{:.0f}’.format(height), # data label, formatted to ignore decimals
 ha = ‘center’) # sets horizontal alignment (ha) to center

Histogram showing the frequency of passengers on each flight.
Histogram showing the number of passengers on each flight.

An additional information that might be beneficial to reflect in the graph as well is the mean line of the dataset:

# plot histogram 
# …# adding a vertical line for the average passengers per flight
plt.axvline(flights[‘passengers’].mean(), color=’purple’, label=’mean’)# adding data label to mean line
plt.text(x = flights[‘passengers’].mean()+3, # x-coordinate position of data label, adjusted to be 3 right of the data point
 y = max([h.get_height() for h in ax.patches]), # y-coordinate position of data label, to take max height 
 s = ‘mean: {:.0f}’.format(flights[‘passengers’].mean()), # data label
 color = ‘purple’) # colour of the vertical mean line# label each bar in histogram
# …

Histogram showing the frequency of passengers on each flight with a vertical line indicating the mean.
Histogram showing the number of passengers on each flight and a line indicating the mean.
Bar Plot

Vertical Bar Plot

Plotting the total number of passengers for each year:

# plot vertical barplot
sns.set(rc={‘figure.figsize’:(10,5)})
ax = sns.barplot(x=’year’, y=’passengers’, data=year_flights)
ax.set(title=’Total Number of Passengers Yearly’) # title barplot# label each bar in barplot
for p in ax.patches:
 # get the height of each bar
 height = p.get_height()
 # adding text to each bar
 ax.text(x = p.get_x()+(p.get_width()/2), # x-coordinate position of data label, padded to be in the middle of the bar
 y = height+100, # y-coordinate position of data label, padded 100 above bar
 s = ‘{:.0f}’.format(height), # data label, formatted to ignore decimals
 ha = ‘center’) # sets horizontal alignment (ha) to center

Bar Plot with vertical bars showing the total number of passengers yearly.
Bar plot with vertical bars showing the total number of passengers yearly

Horizontal Bar Plot

Plotting the average number of passengers on flights each month:

# plot horizontal barplot
sns.set(rc={‘figure.figsize’:(10,5)})
ax = sns.barplot(x=’passengers’, y=’month’, data=month_flights, orient=’h’)
ax.set(title=’Average Number of Flight Passengers Monthly’) # title barplot# label each bar in barplot
for p in ax.patches:
 height = p.get_height() # height of each horizontal bar is the same
 width = p.get_width() # width (average number of passengers)
 # adding text to each bar
 ax.text(x = width+3, # x-coordinate position of data label, padded 3 to right of bar
 y = p.get_y()+(height/2), # # y-coordinate position of data label, padded to be in the middle of the bar
 s = ‘{:.0f}’.format(width), # data label, formatted to ignore decimals
 va = ‘center’) # sets vertical alignment (va) to center

Bar plot with horizontal bars showing the average number of passengers for each month.
Bar plot with horizontal bars showing the average number of passengers for each month
Notes on Usage

It might be beneficial to add data labels to some plots (especially bar plots), it would be good to experiment and test out different configurations (such as using labels only for certain meaningful points, instead of labelling everything) and not overdo the labelling, especially if there are many points. A clean and informative graph is usually more preferable than a cluttered one.

# only labelling some points on graph# plot line graph
sns.set(rc={‘figure.figsize’:(10,5)})
ax = sns.lineplot(x=’year’, y=’passengers’, data=year_flights, marker=’*’, color=’#965786')# title the plot
ax.set(title=’Total Number of Passengers Yearly’)mean = year_flights[‘passengers’].mean()# label points on the plot only if they are higher than the mean
for x, y in zip(year_flights[‘year’], year_flights[‘passengers’]):
 if y > mean:
 plt.text(x = x, # x-coordinate position of data label
 y = y-150, # y-coordinate position of data label, adjusted to be 150 below the data point
 s = ‘{:.0f}’.format(y), # data label, formatted to ignore decimals
 color = ‘purple’) # set colour of line

A line plot showing the total number of passengers yearly.
Line plot showing the total number of passengers yearly.

Sign up for Top 10 Stories
By The Startup

Get smarter at building your thing. Subscribe to receive The Startup's top 10 most read stories — delivered straight into your inbox, twice a month. Take a look.

By signing up, you will create a Medium account if you don’t already have one. Review our Privacy Policy for more information about our privacy practices.
More from The Startup

Get smarter at building your thing. Follow to join The Startup’s +8 million monthly readers & +754K followers.
Sayali Charhate

Sayali Charhate

·Aug 9, 2020
Interview Preparation That Helped Me Get Multiple Offers During the Lockdown

Preparing for interviews can be overwhelming, especially when you have a full-time job alongside. While there are plenty of resources available online to prepare for software engineering interviews, it is hard to decide where to begin, how to cover different aspects of interviewing and know whether you are ready to…
Netflix

8 min read
Interview Preparation That Helped Me Get Multiple Offers During the Lockdown

Share your ideas with millions of readers.
Write on Medium
Rajat Sharma

Rajat Sharma

·Aug 9, 2020
Contacts List Screen in React Native

We will be building a simple contacts list screen in React Native. This is how the final version of the app will look like.
React

3 min read
Simple Contacts List in React Native
Michael Beausoleil

Michael Beausoleil

·Aug 9, 2020
The Villainization of Retail Employees

Somewhere along the line, you’ve probably heard the old cliché “ the customer’s always right.” Please, for the sake of yourself or for your customers, disregard this statement. Nobody is always right, but if anyone is right, it’s usually the employee. We’re currently in a time when many of our…
Retail

4 min read
The Villainization of Retail Employees
Black_Raven (James Ng)

Black_Raven (James Ng)

·Aug 9, 2020
Introduction to Airflow in Python

A beginner’s guide to the basic concepts of Apache Airflow — This is a memo to share what I have learnt in Apache Airflow, capturing the learning objectives as well as my personal notes. The course is taught by Mike Metzger from DataCamp. A data engineer’s job includes writing scripts, adding complex CRON tasks, and trying various ways to meet an…
Airflow

2 min read
Introduction to Airflow in Python
Beth Bruno

Beth Bruno

·Aug 9, 2020
The Problem With Writing About Your Life

You have to write a lot of garbage to finally get to the truth — I have begun. I have been meaning to begin for a long time. But there has always been something more important to do. Washing the dishes. Weeding the garden. Washing fly spots off the windows. But when I am gone, who is going to remember that I kept a clean…
Writing

3 min read
The Problem With Writing About Your Life
Read more from The Startup
More from Medium
A Data Model to Generate Keywords List based on Articles
Best Books For Data Science
Wish you all a very happy and prosperous new year 2021.
Using GBIF data and GeoPandas to plot biodiversity trends
A Gentle Introduction to GDAL Part 4: Working with Satellite Data
Neuromancer Blues: Threading vs Processing — Part 2
Garbage Disposal Repair
ARIMA model for forecasting using EViews
EViews from IHS Markit offers academic researchers, corporations, government agencies and students access to powerful statistical…
Find the Difference between Two Angles using Python

Sign In
Kaili Chen
Kaili Chen

Student of tech, working in tech. Also at https://www.linkedin.com/in/chenkaili/
Related
Book Rating Prediction with Python
Use of Linear Regression to predict the rating of a book.
ENEM Data Analysis
In the last weeks, I've dedicated my time looking upon the microdata from Brazilian High School national exam ENEM.
How to convert a string column to title case, lower case, or upper case with Python, Pandas, and…
Mastering Histograms in Matplotlib
Details of Making Histograms

Help

Status

Writers

Blog

Careers

Privacy

Terms

About

Knowable
To make Medium work, we log user data. By using Medium, you agree to our Privacy Policy, including cookie policy.



#'Construction', 'Machinery and equipment n.e.c. ','Office machinery and computers (30)',
# 'Electrical machinery and apparatus n.e.c. (31)','Radio, television and communication equipment and apparatus (32)',
# 'Medical, precision and optical instruments, watches and clocks (33)','Motor vehicles, trailers and semi-trailers (34)',
# 'Other transport equipment (35)','Furniture; other manufactured goods n.e.c. (36)', 'Textiles (17)',
# 'Printed matter and recorded media (22)', 'Food', 'Other raw materials','Secondary materials', 
# 'Energy carriers', 'Energy carriers.1', 'Other','Products nec', 'Services']#

end_uses = ['Construction', 'Machinery and equipment n.e.c. ', 'Electrical machinery and apparatus n.e.c. (31)', \
          'Motor vehicles, trailers and semi-trailers (34)', 'Other transport equipment (35)', 'Furniture; other manufactured goods n.e.c. (36)' ]

for material in materials:
    end_use_all =  pd.DataFrame([])
    for end_use in end_uses:
        for region in regions:
            end_use_region = pd.DataFrame(region_dict.get(region).get(material).loc[end_use ])#.rename(columns = {'Construction':region})
            end_use_all[region] = end_use_region
        ax = sns.boxplot(data=end_use_all.T,whis=[0, 100], width=.6, palette="vlag", fliersize =0)
        ax = sns.swarmplot(data=end_use_all.T)
        ax.set_xticklabels(years_exio,fontsize = 7.5)
        #ax.set_ylim(0,100)
        ax.set(ylabel = "%", title = (material + ' ' + end_use))
        plt.show()
#end_use_all.T.plot( kind='box', title= 'Copper to Construction')



#plt.annotate('BLABLA', (1995,90))
#plt.annotate()
#ax.text(1995, 80, 'lala')


for i, j in enumerate(end_use_all['% of Squad pass']):
    plt.annotate(df['Player'][i],
                xy=(df['% of Squad pass'][i],0),
                xytext=(df['% of Squad pass'][i], random.uniform(0.2,0.4)),
                arrowprops=dict(arrowstyle="->"))

end_use_all.T.max()
ax.plot.show()

#STEEL
end_use_all =  pd.DataFrame([], index=years_exio, columns=regions)
for region in regions:
    end_use_region = pd.DataFrame(region_dict.get(region).get('steel').loc['Construction'])
    end_use_all[region] =end_use_region.values
end_use_all.T.plot( kind='box', title= 'Steel to Construction')
sns.violinplot(data=end_use_all.T)









#region_dict.get('US').get('steel').T.plot(kind='line',marker='o', title= material)
#plt.legend(bbox_to_anchor=(1,1), loc="upper left")
#plt.show()



end_use_all =  pd.DataFrame([], index=years_exio, columns=regions)
for region in regions:
    end_use_region = pd.DataFrame(region_dict.get(region).get('steel').loc['Construction'])
    end_use_all[region] =end_use_region.values
end_use_all.plot( kind='line',marker='o', title= material, linewidth=0, legend=False)
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.show()
end_use_all.T.plot( kind='box', title= 'Steel to Construction')

end_use_all =  pd.DataFrame([], index=years, columns=regions)
for region in regions:
    end_use_region = pd.DataFrame(region_dict.get(region).get('steel').loc['Motor vehicles, trailers and semi-trailers (34)'])
    end_use_all[region] =end_use_region.values
end_use_all.plot( kind='line',marker='o', title= material, linewidth=0, legend=False)
end_use_all.T.plot( kind='box', title= 'Steel to Motor vehicles and trailers')

end_use_all =  pd.DataFrame([], index=years, columns=regions)
for region in regions:
    end_use_region = pd.DataFrame(region_dict.get(region).get('steel').loc['Machinery and equipment n.e.c. '])
    end_use_all[region] =end_use_region.values
end_use_all.plot( kind='box',marker='o', title= material, linewidth=0, legend=False)
end_use_all.T.plot( kind='box', title= material)



#copper
end_use_all =  pd.DataFrame([], index=years_exio, columns=regions)
for region in regions:
    end_use_region = pd.DataFrame(region_dict.get(region).get('Plastic').loc['Construction'])
    end_use_all[region] =end_use_region.values
end_use_all.T.plot( kind='box', title= 'Copper to Construction')
sns.violinplot(data=end_use_all.T)

.T.plot(kind='line',marker='o', title= material)
#for material in materials:
#    material_single = []
#    material_df = pd.DataFrame([], index=Exio_dict.get(year).index.get_level_values(1), columns=years)
#    for year in years:
#        material_single = Exio_dict.get(year).iloc[:,Exio_dict.get(year).columns.get_level_values(0).map(lambda t: (material) in t).to_list()]
#      material_df[year] = material_single.values
#    material_dict[(material)] = material_df
    
    

