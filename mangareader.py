"""manga reader scrapper"""

#import modules
import multiprocessing as mp
import requests
from bs4 import BeautifulSoup as bs
import os
from tqdm import tqdm

def check_log():
	if os.path.exists("log"):
		return True
	else:
		return False

def log_fetch():
   x = open("log","r")
   y=[]
   for i in x:                                                      #creating a list of all the item in file
      y.append(i)
   z = y[len(y)-1]                                                  #getting the last item form that list
   return z
def update_log(x):
   f=open("log","a")
   f.write("\n")
   f.write(str(x))
   f.close()
#checking if series exist.
def get_name():
   name = False
   while name == False:
   	  x=raw_input("Enter the name of series : ")
   	  url = "http://www.mangareader.net/"+x
   	  print url
   	  check=requests.get(url)
   	  if check.status_code== 200:
   	  	return x
   	  	name = True
   	  else:
   	  	print check.status_code
   	  	print "INVALID NAME, Try Again ..."

#Check for folder
def check_folder(x):
	if os.path.exists(x):
		return True
	else :
		return False
#creating parent directory
def create_folder(x):
	os.mkdir(x)

def worker(url,name):
	x=requests.get(url)
	soup=bs(x.content,"lxml")
	y=soup.find(id="imgholder")
	z=y.img.get("src")
	image=requests.get(z)
	jpg =open(name,"w+")
	jpg.write(image.content)
	jpg.close()

def main():
	print "Welcome ..!"
	print "Enter the series name correctly(as given in mangareader ..!"
	s_name = get_name()
	folder=check_folder(s_name)
	if folder:
		os.chdir(s_name)
	else:
		create_folder(s_name)
		os.chdir(s_name)
	log_check=check_log()
	if log_check:
		ask=raw_input("Use log file(y/n): ")
		if ask == "y":
		   start=log_fetch()
		else:
			start =int(raw_input("Enter the starting chapter number : "))
	else:
		start =(raw_input("Enter the starting chapter number : "))
	start = int(start)
	end=int(raw_input("Enter the last chapter number : "))
	chapters=range(start,end)
	pages=range(1,100)
	for chapter in tqdm(chapters):
		update_log(chapter)
		if os.path.exists(str(chapter)):
			os.chdir(str(chapter))
		else:
			os.mkdir(str(chapter))
			os.chdir(str(chapter))
		print "Working on chapter " + str(chapter)
		for page in pages:
			url="http://www.mangareader.net/"+s_name+"/"+str(chapter)+"/"+str(page)
			print url
			name = s_name+" "+str(chapter)+" "+str(page)
			work = requests.get(url)
			if work.status_code==200:
				print "Working on page " + str(page)
				t=mp.Process(target=worker,args=(url,name))
				t.start()
			else:
				print "Chapter Done..!"
				os.chdir("..")
				break

	print "All Done"
	os.chdir("..")
if __name__ == "__main__":
	main()
