#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 01:34:13 2022

@author: Roberto
"""

import glob
import os
from lxml import etree as ET
import subprocess
import sys



#In order to assure the correct execution of the program you have to start the program before starting the conversion


##YOU HAVE TO RN THE PROGRAM IN A DIRECTORY CONTAINING THE FOLLOWING SUB-DIRECTORY PATTERN: 
    #ARTIST/ALBUM/SONG
    
##OTHERWISE THE PROGRAM WILL CRASH
    
    
    
# /Users/Roberto/Desktop/Programmazione Applicata/Python/DRMConverter_fix/Musica

#conversion_path = "/Users/Roberto/Desktop/Programmazione Applicata/Python/DRMConverter_fix/Musica/R&B"

conversion_path = "/Users/Roberto/Music/MacSoft"

XMLPath = []
#XMLPath.append('/Users/Roberto/Desktop/Programmazione Applicata/Python/DRMConverter_fix/ConvertedSongs.xml')


ar = " "
al = " "
song = " "


lalbum = ""
lartist = ""
lf = ""

b = True

while(b == True):
    print("Add xml? [y/n]")
    b = str(input())[0].lower() == "y"
    if(b):
        print("\nPath:")
        inp = input()
        if(os.path.isfile(inp)):
            XMLPath.append(inp)
        else:
            print("Path non valido")
        print(XMLPath)

    
if(len(XMLPath) == 0): 
    sys.exit("No path specified for xml, quitting...")

print("Daemon started...")

totalSongs = 0

for el in XMLPath:
    root = ET.XML(ET.tostring(ET.parse(el)))
    totalSongs = totalSongs + len(root.xpath('.//Song'))

print("Already converted songs : " + str(totalSongs))

while(True):
    


    try:

        
        list_of_dirs = glob.glob(conversion_path+"/*/*")

        ldir_prev = max(list_of_dirs, key=os.path.getctime)



        lalbum_orig = os.path.split(ldir_prev)[1] 
        lalbum = os.path.split(ldir_prev)[1].strip()
        
        lartist = os.path.split(os.path.split(ldir_prev)[0])[1].strip()
        lartist_orig = os.path.split(os.path.split(ldir_prev)[0])[1]


        lfile = glob.glob(ldir_prev+"/*", recursive=True)
        lf_prev = max(lfile, key=os.path.getctime)

        lf = os.path.split(lf_prev)[1].strip()
        lf_orig = os.path.split(lf_prev)[1]
        
        
        
        if(lf != song): 
            
            #print("Last modified artist: " + lartist)
            #print("----------")
            #print("Last modified album: " + lalbum)
            #print("----------")
            #print("Last modified file: " + lf)
            #print("----------\n")
        
            ar = lartist 
            al = lalbum 
            song = lf
            
        for el in XMLPath:

            root = ET.XML(ET.tostring(ET.parse(el)))

            val = False
            
            
            

            search = root.xpath('.//Artist[text()="' +lartist + '"]/Album[text()="' +lalbum + '"]/Song[text()="' +lf + '"]')

            if(len(search) > 0):
                print("File found in " + os.path.basename(el) + " already converted song: " + lf)
                try:
                    print("\nRemoving: " + conversion_path + "/"+lartist+"/"+lalbum+"/"+lf)
                    os.remove(conversion_path+"/"+lartist_orig+"/"+lalbum_orig+"/"+lf_orig)
                    print("File removed")
                    print("---------\n\n")

                    subprocess.call(['osascript', '-e', 'tell application "Musica" to quit'])
                except Exception as e:
                    print("Exception in removing file")
                    print(str(e))



    except Exception as e:
            continue
            # print("-----EXCEPTION PRINT-----")
            # print("Last modified artist: " + lartist)
            # print("----------")
            # print("Last modified album: " + lalbum)
            # print("----------")
            # print("Last modified file: " + lf)
            # print("----------\n\n")






#%%



###################################
#     WORKING                     #
#       VERSION                   #
###################################




#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# """
# Created on Fri Sep  2 01:34:13 2022

# @author: Roberto
# """

# import glob
# import os
# from lxml import etree as ET
# import subprocess




# #In order to assure the correct execution of the program you have to start the program before starting the conversion


# ##YOU HAVE TO RN THE PROGRAM IN A DIRECTORY CONTAINING THE FOLLOWING SUB-DIRECTORY PATTERN: 
#     #ARTIST/ALBUM/SONG
    
# ##OTHERWISE THE PROGRAM WILL CRASH
    
    
    
# # /Users/Roberto/Desktop/Programmazione Applicata/Python/DRMConverter_fix/Musica

# #conversion_path = "/Users/Roberto/Desktop/Programmazione Applicata/Python/DRMConverter_fix/Musica/R&B"

# conversion_path = "/Users/Roberto/Documents/AppleMacSoft/AppleMacSoft DRM Converter"

# XMLPath = []
# XMLPath.append('/Users/Roberto/Desktop/Programmazione Applicata/Python/DRMConverter_fix/ConvertedSongs.xml')


# ar = " "
# al = " "
# song = " "


# lalbum = ""
# lartist = ""
# lf = ""

# b = True

# while(b == True):
#     print("You want to add more xml? [y/n]")
#     b = str(input())[0].lower() == "y"
#     if(b):
#         print("Path:")
#         inp = input()
#         if(os.path.isfile(inp)):
#             XMLPath.append(inp)
#         else:
#             print("Path non valido")
#         print(XMLPath)
#         print("Vuoi Continuare?:")
    


# while(True):
    

#     try:

        
#         list_of_dirs = glob.glob(conversion_path+"/*/*")

#         ldir_prev = max(list_of_dirs, key=os.path.getctime)




#         lalbum = os.path.split(ldir_prev)[1]
#         lartist = os.path.split(os.path.split(ldir_prev)[0])[1]


#         lfile = glob.glob(ldir_prev+"/*", recursive=True)
#         lf_prev = max(lfile, key=os.path.getctime)

#         lf = os.path.split(lf_prev)[1]

        
        
        
#         if(lf != song): 
            
#             #print("Last modified artist: " + lartist)
#             #print("----------")
#             #print("Last modified album: " + lalbum)
#             #print("----------")
#             #print("Last modified file: " + lf)
#             #print("----------\n")
        
#             ar = lartist 
#             al = lalbum 
#             song = lf
            
#         for el in XMLPath:

#             root = ET.XML(ET.tostring(ET.parse(el)))

#             val = False
            
#             #for ar in root.iter():
                

#             search = root.xpath('.//Song[text()="' + lf + '"]')

#             if(len(search) > 0):
#                 print("File found in " + os.path.basename(el) + " already converted song: " + lf)
#                 try:
#                     print("\nRemoving: " + conversion_path + "/"+lartist+"/"+lalbum+"/"+lf)
#                     os.remove(conversion_path+"/"+lartist+"/"+lalbum+"/"+lf)
#                     print("File removed")
#                     print("---------\n\n")

#                     subprocess.call(['osascript', '-e', 'tell application "Musica" to quit'])
#                 except:
#                     print("Exception in removing file")



#     except:
#             continue
#             # print("-----EXCEPTION PRINT-----")
#             # print("Last modified artist: " + lartist)
#             # print("----------")
#             # print("Last modified album: " + lalbum)
#             # print("----------")
#             # print("Last modified file: " + lf)
#             # print("----------\n\n")







#%%

# import glob
# import os
# from lxml import etree as ET


# #In order to assure the correct execution of the program you have to start the program before starting the conversion

# # /Users/Roberto/Desktop/Programmazione Applicata/Python/DRMConverter_fix/Musica

# conversion_path = "/Users/Roberto/Desktop/Programmazione Applicata/Python/DRMConverter_fix/Musica/R&B"

# XMLPath = '/Users/Roberto/Desktop/Programmazione Applicata/Python/DRMConverter_fix/ConvertedSongs.xml'

# list_of_dirs = glob.glob(conversion_path+"/*/*")  

# ldir_prev = max(list_of_dirs, key=os.path.getctime)

# # print(ldir_prev)


# lalbum = os.path.split(ldir_prev)[1]
# lartist = os.path.split(os.path.split(ldir_prev)[0])[1]
# print("----------")
# print("Last modified artist: " + lartist)
# print("----------")
# print("Last modified album: " + lalbum)
# print("----------")

# lfile = glob.glob(ldir_prev+"/*", recursive=True)
# lf_prev = max(lfile, key=os.path.getctime)

# lf = os.path.split(lf_prev)[1]

# print("Last modified file: " + lf)
# print("----------")




# root = ET.XML(ET.tostring(ET.parse(XMLPath)))

# val = False 

# # print(root.xpath('.//Song[starts-with(text(),"' + lf+ '")]'))
# search = root.xpath('.//Song[text()="' + lf+ '"]')
# print(len(search))


# if(len(search)>0): 
    
#     try:
#         os.remove(conversion_path+"/"+lartist+"/"+lalbum+"/"+lf)
#         print("File removed")
#     except:
        # print("exception in removing file")
    

# for i in search: 
#     print(str(ET.tostring(i).decode("utf-8")))






