import os

cwd = os.getcwd()
isFile = os.getcwd()+'/XMLproses/'
listOfFiles=os.listdir(isFile)

for d_file in listOfFiles:
    try:
        filepath = isFile + d_file
        if not os.path.isfile(filepath):
            print("File "+filepath+" not founds")
        else:
            print("processing file "+filepath)
            os.system("gpt "+filepath)
            print("Complete processing file "+filepath)
            os.remove(filepath)
    except:
        continue
