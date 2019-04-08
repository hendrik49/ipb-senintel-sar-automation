import os
import config

cwd = os.getcwd()
isFile = os.getcwd()+config.xmlprocesspathsubset
listOfFiles=os.listdir(isFile)

for d_file in listOfFiles:
    try:
        filepath = isFile + d_file
        if not os.path.isfile(filepath):
            print("File "+filepath+" not founds")
        else:
            print("processing subset file "+filepath)
            os.system("gpt "+filepath)
            print("Complete processing subset file "+filepath)
            #os.remove(filepath)
    except:
        continue
