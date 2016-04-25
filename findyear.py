fileList = open("fileList.txt", "r")
fileName = fileList.readlines()
fileList.close()

startyear = 1900
endyear = 2017

outfile = open("year.txt", "w")

for i in range(len(fileName)): 
    oneFile = open(fileName[i].rstrip(), "r")
    oneFileContent = oneFile.readlines()
    oneFile.close()
    for j in range(len(oneFileContent)):
        yearList = []
        isName = False
        for k in range(len(oneFileContent[j]) - 3):
            if '\"' in oneFileContent[j][k:k+4] or '\'' in oneFileContent[j][k:k+4]:
                isName = not isName
                continue
            if (oneFileContent[j][k:k+4]).isdigit() and (not isName):
                year = int(oneFileContent[j][k:k+4])
                if year <= endyear and year >= startyear:
                    yearList.append(str(year))
        if len(yearList) > 0:
            outfile.write(yearList[len(yearList) - 1] + '\n')
    
outfile.close()                    

            
    
