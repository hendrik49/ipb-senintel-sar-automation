import os
import config

cwd = os.getcwd()
isFile = os.getcwd()+config.xmlprocesspathstack
listOfFiles=os.listdir(isFile)

for d_file in listOfFiles:
    try:
        filepath = isFile + d_file
        if not os.path.isfile(filepath):
            print("File "+filepath+" not founds")
        else:
            print("processing stack file "+filepath)
            os.system("gpt "+filepath)
            print("Complete processing stack file "+filepath)
            #os.remove(filepath)
    except:
        continue
