#!/usr/bin/env python
# coding: utf-8

import os
import xml.etree.ElementTree as etree
cwd = os.getcwd()
isFile = os.getcwd()+'/sentineldata/'
indx = 1
tree = etree.parse(cwd+'/'+'Lampung_GRD_Or_Cal_Spk_TC_dB.xml')
elem = tree.findall(".//node")
a=[]
for prnt in elem:
    if (prnt.attrib["id"]!="Read"):
        if (prnt.attrib["id"]=="Write"):
            break
        else:
            a.append(prnt.attrib['id'][:3])

gabs='_'.join(a)

##checkdir
listOfFiles=os.listdir(isFile)
xml_dir = cwd+'/XMLproses/'
if not os.path.exists(xml_dir):
    os.makedirs(xml_dir)

dim_dir = cwd+'/Praproses Result/'
if not os.path.exists(dim_dir):
    os.makedirs(dim_dir)
    
for d_file in listOfFiles:
    (sarfileshortname, extension)  = os.path.splitext(d_file)
    read_data = isFile+d_file
    write_data = dim_dir+sarfileshortname+'_'+gabs+'.dim'
    for entry in elem:
        try:
            if (entry.attrib["id"]=="Read"):
                entry[2][0].text = read_data
            if (entry.attrib["id"]=="Write"):
                entry[2][0].text = write_data
        except:
            continue
    tree.write(xml_dir+'sar_praproses_'+str(indx)+'.xml')
    indx = indx + 1