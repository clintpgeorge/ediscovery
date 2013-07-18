import os
import csv
import shutil
import re
directory_path="E:\\topicModelingDataSet"
csv_map_file="E:\\seed.csv"
#
#file_repo="E:\\temp"
file_repo="E:\\edrmv2txt-v2"
#error_file="E:\\topicModelingDataSet\\error.log"

def check_file_path(file_name):
    if(os.path.isfile(os.path.join(file_repo,file_name))==True):
        return os.path.join(file_repo,file_name)
    
    for root, dirs, _ in os.walk(file_repo):
        for dir in dirs:
            file_path=os.path.join(os.path.join(root,dir,file_name))
            #print file_path 
            if os.path.isfile(file_path)==True:
                return file_path
    return ""

arr=dict()
i=1
for root, dirs, files in os.walk(file_repo):
    for file in files:
        print "walk "+str(i) +" " +file 
        arr[file]=str(os.path.join(root,file))
        i=i+1
    
file=open(csv_map_file,"r")
file_err=open(error_file,"w")
reader = csv.reader(file)
i=1
for row in reader:
    if int(row[2])>=0  and row[0]==row[3]:
        print i
        i=i+1
        if(arr.has_key(row[3]+".txt")==False):
            print "error==>"+row[3]
            file_err.write(unicode(row[3]+"\n"))
            continue
        else:
            output_folder=os.path.join(directory_path,row[1],row[2])
            if os.path.exists(output_folder)==False:
                os.makedirs(output_folder)
            shutil.copy(arr[row[3]+".txt"], output_folder)
   
file.close()
file_err.close()    

for root, dirs, files in os.walk(file_repo):
    for file in files:
        paths=re.split("\.", file)
        if len(paths)==5:
            print os.path.join(root,file)
            os.remove(os.path.join(root,file))   
        