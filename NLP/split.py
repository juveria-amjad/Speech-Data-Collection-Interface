textfile= "input15.txt"
outputfile = "inputc15.txt"
OutFile = open(outputfile, 'w',encoding='utf-8')

with open(textfile, 'r', encoding = 'utf-8') as f:
    for line in f:
        a = line.split()
        if len(a) > 10:
            s1=a[:10]
            s2=a[10:]
            OutFile.write(" ".join(s1) + '\n')
            OutFile.write(" ".join(s2)+ '\n')
            
        else:
            OutFile.write(line)

OutFile.close()
            
        
