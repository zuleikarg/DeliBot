# Python program to explain os.mkdir() method  
      
# importing os module  
import os
from datetime import date
    
# Directory 
directory = "GeeksForGeeks"
    
# Parent Directory path 
parent_dir = "C:/Pycharm projects/"
    
# Path 
path = os.path.join(parent_dir, directory) 
    
# Create the directory 
# 'GeeksForGeeks' in 
# '/home / User / Documents'
if not os.path.exists("../demo_vis/"+ str(date.today())):
    os.mkdir("../demo_vis/"+ str(date.today())) 
print("Directory '% s' created" % directory) 
    
# if directory / file that  
# is to be created already 
# exists then 'FileExistsError' 
# will be raised by os.mkdir() method 
    
# Similarly, if the specified path 
# is invalid 'FileNotFoundError' Error 
# will be raised 