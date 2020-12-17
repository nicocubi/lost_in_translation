# Script to remove the books which contain english words mixed to Spanish language
import os,sys

txtDir= "/home/nicolas/CODE/lostInTranslation/data/txt"
jsonDir="/home/nicolas/CODE/lostInTranslation/data/metadata"

toParse= "ENGLISH2.log"

if not os.path.exists(toParse):
    print("File", toParse, "doesn't exist, quitting.")
    sys.exit(1)

filesTodel=[]
with open(toParse) as f:
    for l in f.readlines():
        txtfile= l.split()[1].split('-->')[0].split('.')[0]
        filesTodel.append(txtfile)

for fi in filesTodel:
    txtfi=os.path.join(txtDir,fi+'.txt')
    jsonfi=os.path.join(jsonDir,fi+'.json')

    for fifi in (txtfi,jsonfi):
        if os.path.exists(fifi):
            os.remove(fifi)
        else:
            print(fifi, "does not exist,skipping")
