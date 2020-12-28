#!/usr/bin/env python3
#The lybraries required for this code: The first three are downloaders, the fourth for the file io, 5 & 6 are handleers and sys is for the command line input.
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import shutil
import urllib
import time
import os
import re
import sys
import string
import os.path
import warnings
warnings.filterwarnings("ignore")

#Gets the command line input and turns it into a url.

#In 5.2, I added a UserAgent to hopefully combat the rate limiting.
def getPageSoup(pageurl):
	user_agent = "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36"
	req = urllib.request.Request(pageurl, headers={'User-Agent': user_agent})
	content = urllib.request.urlopen(req).read()
	soup = (BeautifulSoup(content))
	return soup

#From now on, all the values will be stored in arrays. At some point it's going to dump to a log
#file, and this will help.
def getNameNumUrls(soup):
	ltm_a = []
	ltm_b = []
	ltm_c = []
	for link in soup.find_all('p', {'class': 'fileinfo'}):
		ltm_a.append(link.find("span", class_="postfilename").text)
		ltm_c.append(link.a['href'])

	fnn = 000
	for i in ltm_c: 
		result = re.search(r'(\d{13,}.\d)|(\d{13,})',i)
		if result:	
			fn = (result.group())
		elif ("file_store") in i:
			md5 = i.split('/')[-1].split('.')[0][0:16]
			fn = (md5)
		ltm_b.append(str("{} - {}".format(str(fnn).zfill(3), fn)))
		fnn += 1

	return ltm_a, ltm_b, ltm_c

#A filecount function I got from StackOverflow.
def filecount(DIR): return len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])


#The completed fucnction for constructing 4chan folders. 
def makeChanDir(soup):

    nameA = (soup.title.string)
    name = nameA.strip()

    #Some threads like generals ( /sig/, /qtddtot/) have the same name, so the number is necessary.
    idInt = str(soup.findAll("div", {"class":"post op has-file body-not-empty"})[0].get('id')[3:]).zfill(10)

    sInt  = name.count(" - ")
    titleDC = name.split(" - ") 
    if sInt == 1:
       board = titleDC[0] 
       tRw   = titleDC[1]
    if sInt == 2:
       board = titleDC[0] 
       tRw   = ' '.join(titleDC[1:-1])

    print("{} - {}".format(board, tRw) )

    board = board[1:-1].upper()
    alphabet = string.ascii_letters + string.digits + ("'[];()&"",.-_ ")
    thread = ''
    for char in tRw: 
        if char in alphabet:
           thread+=char

    #return ("Site-[ 8chan ] - Board-[" + board + "] - Thread-[ " + thread[:64] +" ]["+idInt+"]")
    return ("Site-[ 8chan ] - Board-[ {} ] - Thread-[ {} ][{}]".format(board,thread[:64],idInt))



def getAllArgs(howOut="return"):
	allArgs = sys.argv
	allArgs = allArgs[1:]


	if howOut == "print": 
		print (len(allArgs))
		for i in allArgs: print (i)
	elif howOut == "return":
		return allArgs

def everything(url):
	global eerr
	eerr = 0
	soup = getPageSoup(url)
	newName = makeChanDir(soup)
	dcwd = ((os.getcwd()) + "/" + newName)
	if os.path.exists(dcwd):
	   fileInt = filecount(dcwd)
	else:
	   fileInt = 0 
	   os.makedirs(dcwd)

	fileName, fileNumber, fileURL = getNameNumUrls(soup)
	#Sets up the numbering, even if the program restarts.
	threadCount = len(fileName)
	if fileInt == 0:
	   loopCount = (fileInt)
	   newStart = True
	elif fileInt > 3:
	   loopCount = (fileInt - 1)
	   newStart = False


	#The Already downloaded Images
	print("Folder Name: " + str(newName))
	print("AD Images:   " + str(fileInt))
	#And the new downloader, as well:
	while loopCount < threadCount:



	      print("Image:                     " + (str(loopCount + 1)) + " of " + (str(threadCount)))


	      fileNameTemp        =  fileName[loopCount]
	      fileNumberTemp      =  fileNumber[loopCount]
	      fileURLTemp         =  fileURL[loopCount]



	      print("File Name:                 " + fileNameTemp)
	      print("File Number:               " + fileNumberTemp)
	      print("File Url:                  " + fileURLTemp[2:])


	      extTR = os.path.splitext(fileNameTemp)[1]
	      fileNameFinal = (fileNumberTemp + " - ON[" + fileNameTemp + "]" + extTR)
	      print ("File to be written:        " + fileNameFinal)


	      try:
	        fileURLTempfix = ("https:" + fileURLTemp) #Workaround for the two slashes
	        #response = requests.get(fileURLTempfix, stream=1)
	        #with open((os.path.join(dcwd, fileNameFinal)), 'wb') as out_file:
	        #  print ("Downloading: " + fileNameFinal)
	        ffpath = (os.path.join(dcwd, fileNameFinal))
	        with urllib.request.urlopen(fileURLTempfix) as response, open(ffpath, 'wb') as out_file:
	          shutil.copyfileobj(response, out_file)
	        del response
	        print ("File Downloaded:           " + fileNameFinal + "\n")
	      except OSError:
	       print ("Error on image: {}\n".format(fileNameFinal))
	       eerr += 1
	      except urllib.error.URLError:
	       print ("Network Error on image: {}\n".format(fileNameFinal))
	       eerr += 1
#	      except Exception:
#	       print ("Exception on image: {}\n".format(fileNameFinal))
#	       eerr += 1


	      
	      loopCount += 1

	return newName, threadCount


def main():
	r = getAllArgs()
	for n, i in enumerate(r):
		print ("Page {}: {}".format(n, i))
		e,t = everything(i)
	if not eerr > 2: print ("{} files in: '{}'".format(t,e))

main()
