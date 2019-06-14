username ='didok49' 
password = 'sentinel49'
geojson = 'geojson/Lampung_extent_1.geojson'
start_date = '20180401'
end_date='20181230'
platformname = 'Sentinel-1'
producttype='GRD'
orbitdirection='Descending'
url = 'https://scihub.copernicus.eu/apihub/' 
sentineldirpath = "//sentineldata//"

xmlpath="1/xml/Lampung_GRD_Or_Cal_Spk_TC_dB.xml" 
xmlprocesspath='/1/XMLprocess/'
xmlpraprocessresult='/1/Praproses_result/'

xmlpathsubset="/2/subset_xml/Subset_Lampung_test_sitesMedium.xml" 
xmlprocesspathsubset='/2/subset_XMLprocess/'
xmlpraprocessresultsubset='/2/subset_praproses_result/'


xmlpathstack="/3/subset_xml/stack_file_list.xml" 
xmlprocesspathstack='/3/stack_XMLprocess/'
xmlpraprocessresultstack='/3/stack_praproses_result/'

import os, datetime

train_path =os.getcwd()+r'/Validation_of_products_2018/train_mat.mat'
folder = os.getcwd()+r'/Validation_of_products_2018/S1A_timeseries/Lampung_S1A_timeseries_2018Anual_Medium.data'
dateStr = '27Dec2018';

