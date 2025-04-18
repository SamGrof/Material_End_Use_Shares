# -*- coding: utf-8 -*- lol
"""
Created on Tue Mar  8 13:41:20 2022

@author: jstreeck
@Forked by Sam G. Rocket
"""

import os
import sys
import numpy as np
import pandas as pd

main_path = os.getcwd()
module_path = os.path.join(main_path, 'modules')
sys.path.insert(0, module_path)
data_path = os.path.join(main_path, 'input_data/USA/')

from EndUseShares_functions_v1_SGR import calc_CBA,create_WIOMassFilter_plain, create_WIOMassFilter_withServiceRawMatInput,\
     calc_WIO, create_GhoshIoAmcMassFilter_plain, create_GhoshIoAmcMassFilter_delServiceRawMat, calc_GhoshIO_AMC, \
     create_GhoshIoAmcMassFilter_delServiceOutput, create_PartialGhoshIO_filter_plain, create_PartialGhoshIO_filter_noServiceInput, \
     calc_PartialGhoshIO, end_use_transfer, calc_WIO_noYieldCorr, assemble_yield_filter, save_to_excel

# We dont need _ExtAgg? SR
extensions = ['_Base']
#extensions = ['_Base', '_ExtAgg'] # choose scenario out of ['_Base','_ExtAgg']; _Base = Z,A,Y matrices as derived from Information of US BEA, _ExtAgg = in comparison to _Base, some IOT sectors were aggregated  (e.g. paper mills + paperboard mills), filter matrix _Base
# We only need one year to test the code
#years =  ['1963', '1967', '1972', '1977', '1982', '1987', '1992', '1997', '2002','2007', '2012'] # year has to be a string
years =  ['2012'] # year has to be a string


for extension in extensions:
    for year in years:
        
        '''  #1 LOAD DATA AND DERIVE OVERARCHING VARIABLES '''
        Z_orig = pd.read_excel(data_path + 'Z_' + year + '_ImpNoExpNoCII' + extension + '.xlsx',index_col=[0,1],header=[0,1]) #commodity x commodity transaction matrix
        A_orig = pd.read_excel(data_path + 'A_' + year + '_ImpNoExpNoCII' + extension + '.xlsx',index_col=[0,1],header=[0,1]) # technology matrix: commodity x commodity with industry technology
        Y_orig = pd.read_excel(data_path + 'Y_' + year + '_ImpNoExpNoCII' + extension + '.xlsx',index_col=[0,1]) # final demand vector (treatment of imports, exports and CII as specified in file name)
        # make sure multiindex and multiindex names of A,Y,Z, filter_matrix are matching (also their formats in Excel files); if code not working and in doubt why, check content overlap and copy multiindex of matrices to filter matrix
        
        filter_matrix = pd.read_excel(data_path + 'Filter_' + year  + extension + '.xlsx',index_col=[0,1],header=[0,1],sheet_name='mass_&_aggreg') # filter and aggregation matrix
        
        #Somehow the index of raw_yield_df got messed up. Perhaps because i opened the excel shet with LibreOffice..
        raw_yield_df = pd.read_excel(data_path + 'Filter_' + year  + extension + '.xlsx',index_col=[0,1],header=[0],sheet_name='yield') #header=[0]



        yield_filter = pd.DataFrame(np.zeros((len(Z_orig),len(Z_orig))), index =Z_orig.index, columns = Z_orig.columns.get_level_values(0))
        aggregation_matrix = filter_matrix.iloc[:,6:-2].T # get only the end-use aggregation categories from the filter_matrix 
        extension_products = filter_matrix.loc[filter_matrix[('All','Materials')]== 1].index.get_level_values(0).to_list() # the sectors that are considered for distributing material extensions
        
        #assemble yield filter
        yield_filter = assemble_yield_filter(aggregation_matrix, raw_yield_df, Z_orig, yield_filter).replace(0,1)
        
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
        
        # optional: get direct market shares
        # Q = Z.divide(x.values,axis=0).replace(np.nan,0.0)
        # Q.to_excel('Q_1997_directDeliveryShares.xlsx')
        
        
        ''' 
        
        # End-Use Transfer (EUT) WIO-MFA 
        
        ''' 
        
        # create transfer filter applied to transfer transactions from intermediate demand Z to final demand Y
        filt_packaging = filter_matrix.loc[:,(['End-Use Category'],['Packaging'])].iloc[:,0].to_numpy() #packaging as defined in aggregation columns of filter_matrix
        filt_prod2service = pd.DataFrame(data=np.ones_like(Z), index= Z.index, columns=Z.columns)
        filt_prod2service = (filt_prod2service  * non_service.T).replace(1,2).replace(0,1).replace(2,0) * non_service #non-service are the items not identified as material, intermediate or product in filter_matrix first columns; NOT as defined in aggregation columns
        filter_transf = (np.ones_like(Z) * filt_packaging).T
        filter_transf = (filter_transf + filt_prod2service).replace(2,1)
        
        Y_transferred, Z_transferred, A_eut = end_use_transfer(Z, Y, A, filter_transf, yield_filter)
        filt_Amp, filt_App, filt_Amp_label, filt_App_label = create_WIOMassFilter_plain(A,raw_materials, materials,products,intermediates, non_service)
        D_eut_WIO,D_eut_WIO_aggregated,EUT_WIO_split,check_eut_WIO = calc_WIO_noYieldCorr(A_eut, Y_transferred, filt_Amp, filt_App, filter_matrix,aggregation_matrix,extension_products)
        
        # save
        fileName_EUTWIOMF= 'USA/EUT_WIOMF_' + year + extension
        save_to_excel(fileName_EUTWIOMF,D=D_eut_WIO,D_aggregated=D_eut_WIO_aggregated,total_split = EUT_WIO_split, \
                      massFilterName=filter_matrix,   Ztransferred=pd.DataFrame(), Ytransferred=pd.DataFrame(), 
                      filter_transf=filter_transf, check = check_eut_WIO)
                        
        del fileName_EUTWIOMF, filt_packaging, filt_prod2service, filter_transf, Y_transferred, Z_transferred, A_eut, filt_Amp, filt_App, filt_Amp_label, filt_App_label,\
            D_eut_WIO,D_eut_WIO_aggregated,EUT_WIO_split,check_eut_WIO
                  
            
            
        #'''
        #
        # End-Use Transfer (EUT) WIO-MFA_filtDif
        #
        #''' 
        #
        # create transfer filter applied to transfer transactions from intermediate demand Z to final demand Y
        #filt_packaging = filter_matrix.loc[:,(['End-Use Category'],['Packaging'])].iloc[:,0].to_numpy() #packaging as defined in aggregation columns of filter_matrix
        #filt_prod2service = pd.DataFrame(data=np.ones_like(Z), index= Z.index, columns=Z.columns)
        #filt_prod2service = (filt_prod2service  * non_service.T).replace(1,2).replace(0,1).replace(2,0) * non_service #non-service are the items not identified as material, intermediate or product in filter_matrix first columns; NOT as defined in aggregation columns
        #filter_transf = (np.ones_like(Z) * filt_packaging).T
        #filter_transf = (filter_transf + filt_prod2service).replace(2,1)
        #
        #Y_transferred, Z_transferred, A_eut = end_use_transfer(Z, Y, A, filter_transf, yield_filter)
        #filt_Amp, filt_App, filt_Amp_label, filt_App_label = create_WIOMassFilter_withServiceRawMatInput(A,raw_materials, materials,products,intermediates, non_service)
        #D_eut_WIO,D_eut_WIO_aggregated,EUT_WIO_split,check_eut_WIO = calc_WIO_noYieldCorr(A_eut, Y_transferred, filt_Amp, filt_App, filter_matrix,aggregation_matrix,extension_products)
        #
        ## save
        #fileName_EUTWIOMF= 'USA/EUT_WIOMF_fildDif_' + year + extension
        #save_to_excel(fileName_EUTWIOMF,D=D_eut_WIO,D_aggregated=D_eut_WIO_aggregated,total_split = EUT_WIO_split, \
        #              massFilterName=filter_matrix,   Ztransferred=pd.DataFrame(), Ytransferred=pd.DataFrame(), 
        #              filter_transf=filter_transf, check = check_eut_WIO)
        #                
        #del fileName_EUTWIOMF, filt_packaging, filt_prod2service, filter_transf, Y_transferred, Z_transferred, A_eut, filt_Amp, filt_App, filt_Amp_label, filt_App_label,\
        #    D_eut_WIO,D_eut_WIO_aggregated,EUT_WIO_split,check_eut_WIO
        #
        #del Z_orig, A_orig, Y_orig, filter_matrix, raw_yield_df, yield_filter, aggregation_matrix, extension_products, raw_materials,\
        #    materials, intermediates, products_p1, products_p2, products, non_service, Y, Z, x, A, I, L
        #