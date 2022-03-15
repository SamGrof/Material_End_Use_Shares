# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 13:41:20 2022

@author: jstreeck
"""

import os
import sys
import numpy as np
import pandas as pd

main_path = os.getcwd()
module_path = os.path.join(main_path, 'modules')
sys.path.insert(0, module_path)
data_path = os.path.join(main_path, 'input_data/')

from EndUseShares_functions_v4 import calc_CBA,create_WIOMassFilter_plain, create_WIOMassFilter_withServiceRawMatInput,\
     calc_WIO, create_GhoshIoAmcMassFilter_plain, create_GhoshIoAmcMassFilter_delServiceRawMat, calc_GhoshIO_AMC, \
     create_GhoshIoAmcMassFilter_delServiceOutput, create_PartialGhoshIO_filter_plain, create_PartialGhoshIO_filter_noServiceInput, \
     calc_PartialGhoshIO, hypothetical_transfer, calc_WIO_noYieldCorr, assemble_yield_filter, save_to_excel


##--> for def create_GhoshIoAmcMassFilter_delServiceRawMat think about whether to delete only outputs of services , raw materials? 


'''

  #1 LOAD DATA AND DERIVE OVERARCHING VARIABLES 

'''

year = '2007' # year has to be a string
extension = '_Base' # choose scenario out of ['_Base','_ExtAgg']; _Base = Z,A,Y matrices as derived from Information of US BEA, _ExtAgg = in comparison to _Base, some IOT sectors were aggregated  (e.g. paper mills + paperboard mills), filter matrix _Base

Z_orig = pd.read_excel(data_path + 'Z_' + year + '_ImpNoExpNoCII' + extension + '.xlsx',index_col=[0,1],header=[0,1]) #commodity x commodity transaction matrix
A_orig = pd.read_excel(data_path + 'A_' + year + '_ImpNoExpNoCII' + extension + '.xlsx',index_col=[0,1],header=[0,1]) # technology matrix: commodity x commodity with industry technology
Y_orig = pd.read_excel(data_path + 'Y_' + year + '_ImpNoExpNoCII' + extension + '.xlsx',index_col=[0,1]) # final demand vector (treatment of imports, exports and CII as specified in file name)
# make sure multiindex and multiindex names of A,Y,Z, filter_matrix are matching (also their formats in Excel files); if code not working and in doubt why, check content overlap and copy multiindex of matrices to filter matrix

filter_matrix = pd.read_excel(data_path + 'Filter_' + year  + extension + '.xlsx',index_col=[0,1],header=[0,1],sheet_name='mass_&_aggreg') # filter and aggregation matrix
raw_yield_df = pd.read_excel(data_path + 'Filter_' + year  + extension + '.xlsx',index_col=[0,1],header=[0],sheet_name='yield')
yield_filter = pd.DataFrame(np.zeros((len(Z_orig),len(Z_orig))), index =Z_orig.index, columns = Z_orig.columns.get_level_values(1))
aggregation_matrix = filter_matrix.iloc[:,6:-2].T # get only the end-use aggregation categories from the filter_matrix 
extension_products = filter_matrix.loc[filter_matrix[('All','Materials')]== 1].index.get_level_values(0).to_list() # the sectors that are considered for distributing material extensions

#assemble yield filter
yield_filter = assemble_yield_filter(aggregation_matrix, raw_yield_df, Z_orig, yield_filter).replace(0,1)
#yield_filter = np.ones_like(Z_orig)

#define the filter settings for different materials/product groups that are used in method functions
raw_materials = filter_matrix.loc[:,(['All'],['Raw_materials'])]
materials  = filter_matrix.loc[:,(['All'],['Materials'])]
intermediates = filter_matrix.loc[:,(['All'],['Intermediates_only'])]
products_p1 = filter_matrix.loc[:,(['All'],['Products_p1'])]
products_p2 = filter_matrix.loc[:,(['All'],['Products_p2'])]
products = pd.DataFrame((products_p1.to_numpy() + products_p2.to_numpy()), index = products_p1.index)
non_service = materials.to_numpy() + intermediates.to_numpy() + products.to_numpy() + raw_materials.to_numpy() 

# set negatives in Y and Z to zero and calculate new x, A, L; negatives are few (e.g. sectors adjustments and secondary goods and few single outliers)
Y_orig.clip(lower=0, inplace=True)
Y = Y_orig.astype(float)
Z_orig.clip(lower=0, inplace=True)
Z = Z_orig.astype(float)
x = Z.sum(axis=1) + Y.sum(axis=1)
x_diag = np.zeros_like(Z)
np.fill_diagonal(x_diag, x)

A = pd.DataFrame(np.dot(Z, np.linalg.pinv(x_diag)),Z.index,Z.columns)
I = np.eye(A.shape[0])
L = pd.DataFrame(np.linalg.pinv(I-A),Z.index,Z.columns)

#check difference of new x,A to original to x,A
print('The sum of x is ' + str(round(x.sum(),4)) + ', the sum of L*Y is ' +str(round(np.dot(L, Y).sum(),4)) + ', the difference is ' +str(abs(x.sum()-np.dot(L, Y).sum())))
print('The sum of A is ' + str(round(A.sum().sum(),4)) + ', the sum of A_orig is ' +str(round(A_orig.sum().sum(),4)) + ', the difference is ' +str(abs(A.sum().sum()-A_orig.sum().sum())))


'''

  #2 IMPLEMENT METHODS TO DATA BY FUNCTIONS IN EndUseSplit_USA_functions_v#

'''

''' # CBA'''
D_cba,D_cba_aggregated,CBA_split,check_cba = calc_CBA(L,Y,filter_matrix,aggregation_matrix,extension_products)

fileName_CBA = 'CBA_' + year + extension
save_to_excel(fileName_CBA,D=D_cba,D_aggregated=D_cba_aggregated,total_split=CBA_split, check = check_cba)

del D_cba,D_cba_aggregated,CBA_split,check_cba


    
''' # WIO-MFA plain'''
filt_Amp, filt_App, filt_Amp_label, filt_App_label = create_WIOMassFilter_plain(A,raw_materials, materials,products,intermediates, non_service)
D_wio,D_wio_aggregated,WIO_split,check_wio = calc_WIO(A, Y, yield_filter, filt_Amp, filt_App,filter_matrix,aggregation_matrix,extension_products)

# save
fileName_WIO = 'WIO_plain_' + year + extension
save_to_excel(fileName_WIO,D=D_wio,D_aggregated=D_wio_aggregated,total_split=WIO_split,\
              yieldFilterName=yield_filter ,filt_Amp=filt_Amp_label,filt_App=filt_App_label, check = check_wio)
   
del filt_Amp, filt_App, filt_Amp_label, filt_App_label, D_wio,D_wio_aggregated,WIO_split,check_wio



''' # WIO-MFA keep raw material and service inputs'''
filt_Amp, filt_App, filt_Amp_label, filt_App_label = create_WIOMassFilter_withServiceRawMatInput(A,raw_materials, materials,products,intermediates, non_service)
D_wio,D_wio_aggregated,WIO_split,check_wio = calc_WIO(A, Y, yield_filter, filt_Amp, filt_App,filter_matrix,aggregation_matrix,extension_products)

# save
fileName_WIO = 'WIO_withServiceInput_' + year + extension
save_to_excel(fileName_WIO,D=D_wio,D_aggregated=D_wio_aggregated,total_split=WIO_split,\
              yieldFilterName=yield_filter ,filt_Amp=filt_Amp_label,filt_App=filt_App_label, check = check_wio)
    
del filt_Amp, filt_App, filt_Amp_label, filt_App_label, D_wio,D_wio_aggregated,WIO_split,check_wio



''' # Ghosh-IO AMC plain'''  
filt_Ghosh_Z,filt_Ghosh_Y, filt_Ghosh_Z_label, filt_Ghosh_Y_label = create_GhoshIoAmcMassFilter_plain(Z, Y, materials, non_service)
D_Ghosh,D_Ghosh_aggregated, QR_check_unity, check_Ghosh  = calc_GhoshIO_AMC(Z, Y, x, filter_matrix, filt_Ghosh_Z, filt_Ghosh_Y,aggregation_matrix,extension_products)

# save
fileName_GhoshIoAmc = 'GhoshAMC_plain_' + year + extension
save_to_excel(fileName_GhoshIoAmc,D=D_Ghosh,D_aggregated=D_Ghosh_aggregated,massFilterName=filter_matrix,\
       GhoshZfilter=filt_Ghosh_Z_label,GhoshYfilter=filt_Ghosh_Y_label, check = check_Ghosh)
    
del filt_Ghosh_Z,filt_Ghosh_Y, filt_Ghosh_Z_label, filt_Ghosh_Y_label, D_Ghosh,D_Ghosh_aggregated, QR_check_unity, \
    check_Ghosh , fileName_GhoshIoAmc



''' # Ghosh-IO no output from service sectors'''  
filt_Ghosh_Z,filt_Ghosh_Y, filt_Ghosh_Z_label, filt_Ghosh_Y_label = create_GhoshIoAmcMassFilter_delServiceOutput(Z, Y, materials, non_service)
D_Ghosh,D_Ghosh_aggregated, QR_check_unity, check_Ghosh  = calc_GhoshIO_AMC(Z, Y, x, filter_matrix, filt_Ghosh_Z, filt_Ghosh_Y,aggregation_matrix,extension_products)

# save
fileName_GhoshIoAmc = 'GhoshAMC_noServOutput_' + year + extension
save_to_excel(fileName_GhoshIoAmc,D=D_Ghosh,D_aggregated=D_Ghosh_aggregated,massFilterName=filter_matrix,\
       GhoshZfilter=filt_Ghosh_Z_label,GhoshYfilter=filt_Ghosh_Y_label, check = check_Ghosh)
    
del filt_Ghosh_Z,filt_Ghosh_Y, filt_Ghosh_Z_label, filt_Ghosh_Y_label, D_Ghosh,D_Ghosh_aggregated, QR_check_unity, \
    check_Ghosh , fileName_GhoshIoAmc



''' # Ghosh-IO no in/output to service and raw material sectors'''  
filt_Ghosh_Z,filt_Ghosh_Y, filt_Ghosh_Z_label, filt_Ghosh_Y_label = create_GhoshIoAmcMassFilter_delServiceRawMat(Z, Y, raw_materials, materials, non_service)
D_Ghosh,D_Ghosh_aggregated, QR_check_unity, check_Ghosh  = calc_GhoshIO_AMC(Z, Y, x, filter_matrix, filt_Ghosh_Z, filt_Ghosh_Y,aggregation_matrix,extension_products)

# save
fileName_GhoshIoAmc = 'GhoshAMC_noTransServRawMat_' + year + extension
save_to_excel(fileName_GhoshIoAmc,D=D_Ghosh,D_aggregated=D_Ghosh_aggregated,massFilterName=filter_matrix,\
       GhoshZfilter=filt_Ghosh_Z_label,GhoshYfilter=filt_Ghosh_Y_label, check = check_Ghosh)
    
del filt_Ghosh_Z,filt_Ghosh_Y, filt_Ghosh_Z_label, filt_Ghosh_Y_label, D_Ghosh,D_Ghosh_aggregated, QR_check_unity, \
    check_Ghosh , fileName_GhoshIoAmc



''' # Partial Ghosh-IO plain'''  
filt_ParGhosh, filt_ParGhosh_label  = create_PartialGhoshIO_filter_plain(Z, materials, intermediates, products_p1)
D_ParGhosh, D_ParGhosh_agg, Q_interm, check_ParGhosh  = calc_PartialGhoshIO(Z, filter_matrix, filt_ParGhosh, filt_ParGhosh_label,aggregation_matrix,extension_products)

# save
fileName_PartialGhosh= 'PartialGhoshIO_plain_' + year + extension
save_to_excel(fileName_PartialGhosh,D=D_ParGhosh,D_aggregated=D_ParGhosh_agg,massFilterName=filter_matrix,\
              MarketShares=Q_interm, filt_ParGhosh=filt_ParGhosh_label, check = check_ParGhosh)
    
del fileName_PartialGhosh, filt_ParGhosh, filt_ParGhosh_label, D_ParGhosh, D_ParGhosh_agg, check_ParGhosh, Q_interm



'''Partial Ghosh-IO no service input'''
filt_ParGhosh, filt_ParGhosh_label  = create_PartialGhoshIO_filter_noServiceInput(Z, materials, intermediates, products_p1, non_service)
D_ParGhosh, D_ParGhosh_agg, Q_interm, check_ParGhosh  = calc_PartialGhoshIO(Z, filter_matrix, filt_ParGhosh, filt_ParGhosh_label,aggregation_matrix,extension_products)

# save
fileName_PartialGhosh= 'PartialGhoshIO_noServiceInput_' + year + extension
save_to_excel(fileName_PartialGhosh,D=D_ParGhosh,D_aggregated=D_ParGhosh_agg,massFilterName=filter_matrix,\
                 MarketShares=Q_interm, filt_ParGhosh=filt_ParGhosh_label, check = check_ParGhosh)

del fileName_PartialGhosh, filt_ParGhosh, filt_ParGhosh_label, D_ParGhosh, D_ParGhosh_agg, check_ParGhosh, Q_interm



'''Hypothetical Transfer WIO-MFA - watch out - now with filter matrix where raw material input is kicked out; default should not have this''' 

# create transfer filter applied to transfer transactions from intermediate demand Z to final demand Y
filt_packaging = filter_matrix.loc[:,(['End-Use Category'],['Packaging'])].iloc[:,0].to_numpy() #packaging as defined in aggregation columns of filter_matrix
filt_prod2service = pd.DataFrame(data=np.ones_like(Z), index= Z.index, columns=Z.columns)
filt_prod2service = (filt_prod2service  * non_service.T).replace(1,2).replace(0,1).replace(2,0) * non_service #non-service are the items not identified as material, intermediate or product in filter_matrix first columns; NOT as defined in aggregation columns
filter_transf = (np.ones_like(Z) * filt_packaging).T
filter_transf = (filter_transf + filt_prod2service).replace(2,1)

Y_transferred, Z_transferred, A_ht = hypothetical_transfer(Z, Y, A, filter_transf, yield_filter)
filt_Amp, filt_App, filt_Amp_label, filt_App_label = create_WIOMassFilter_plain(A,raw_materials, materials,products,intermediates, non_service)
D_ht_WIO,D_ht_WIO_aggregated,HT_WIO_split,check_ht_WIO = calc_WIO_noYieldCorr(A_ht, Y_transferred, filt_Amp, filt_App, filter_matrix,aggregation_matrix,extension_products)

# save
fileName_HTWIOMF= 'HT_WIOMF_' + year + extension
save_to_excel(fileName_HTWIOMF,D=D_ht_WIO,D_aggregated=D_ht_WIO_aggregated,total_split = HT_WIO_split, \
              massFilterName=filter_matrix,   Ztransferred=pd.DataFrame(), Ytransferred=pd.DataFrame(), 
              filter_transf=filter_transf, check = check_ht_WIO)
                
del fileName_HTWIOMF, filt_packaging, filt_prod2service, filter_transf, Y_transferred, Z_transferred, A_ht, filt_Amp, filt_App, filt_Amp_label, filt_App_label,\
    D_ht_WIO,D_ht_WIO_aggregated,HT_WIO_split,check_ht_WIO