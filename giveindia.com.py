# A script to get NGO data off Giveindia.org. Requires Beautiful Soup 4 and requests.

import requests
import json
import re
import sys
import time
import os
from bs4 import BeautifulSoup

# Function to open webpage and return contents


def urlOpen(url):
    # urlOpen URL return HTML
    try:
        r = requests.get(url, timeout=7)
        return r.text
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        errfile.write("Timout for URL: " + url + "\n")
        return

        
# NGO Data File. Open the file
filename="NGO_DATA.csv"
try:
    os.remove(filename)
except:
    pass

outfile=open(filename,"a")
errfilename="Errors.log"
try:
    os.remove(errfilename);
except: 
    pass
errfile=open(errfilename,"a")

#Create outfile header

states_tup = (  "Andaman and Nicobar Islands",
                "Andhra Pradesh",
                "Arunachal Pradesh",
                "Assam",
                "Bihar",
                "Chandigarh",
                "Chhattisgarh",
                "Dadra and Nagar Haveli",
                "Daman and Diu",
                "National Capital Territory of Delhi",
                "Goa",
                "Gujarat",
                "Haryana",
                "Himachal Pradesh",
                "Jammu and Kashmir",
                "Jharkhand",
                "Karnataka",
                "Kerala",
                "Lakshadweep",
                "Madhya Pradesh",
                "Maharashtra",
                "Manipur",
                "Meghalaya",
                "Mizoram",
                "Nagaland",
                "Orissa",
                "Puducherry",
                "Punjab",
                "Rajasthan",
                "Sikkim",
                "Tamil Nadu",
                "Telangana",
                "Tripura",
                "Uttar Pradesh",
                "Uttarakhand",
                "West Bengal",)

top=("State","Name","Add","Pin","Phone","Mobile","Email","Website","Contact Person","Purpose",   "Aims/Objectives/Mission ",)
for columns in top:
    pass
    #outfile.write(columns+",")
#outfile.write("\n")
outfile.close() 
print("Name, State, Location, Contact person, Phone,Email , Website, Mission")


   
for state in (1,):
   

    # print("Name, State, Location, Contact person, Email, Phone")
    url="http://www.giveindia.org/certified-indian-ngos.aspx"
    html=urlOpen(url)
    # print ("For state %s opened url %s"% (state,url))
    soup=BeautifulSoup(html,"lxml")
        # print(soup)
    tr=soup.find_all("td",class_="column col-sm-8")

    

    for outer in tr:
        # print(type(outer))
        # print(str(outer))
        ngoname = None
        link = None
        ngostate = None
        location = None
        inner = None
        contact = None
        contact_person = None
        phone = None
        email = None
        website = None
        mission = None
        ngoname = (outer.find("a")).get_text().replace(","," ").replace("\n"," ").strip()
        link = outer.find("a")['href']
        ngost=outer.find_next_sibling()
        #print(type(ngostate))
        ngostate=ngost.get_text().replace(","," ").replace("\n"," ").strip()
        location=ngost.find_next_sibling()
        # print( type(location))
        location=location.get_text().replace(","," ").replace("\n"," ").strip()
        innerhtml=""
        bowl=""
        inner="http://www.giveindia.org"+link

        try:
            # print("Fetching :"+ inner)
            innerhtml=urlOpen(inner)
            bowl=BeautifulSoup(innerhtml,'lxml')
        except Exception as e:
            print("Failed to prepare Soup : "+inner+"\n"+str(e))
            continue
        contact=bowl.find('div',id="contact")
        
        contact_person=contact.find('span', id=re.compile("^.*lbcontactname$")).get_text().replace(","," ").replace("\n"," ")
        # print(contact_person)
        phone=contact.find('span',id=re.compile("^.*lbPhone$")).get_text().replace(","," ").replace("\n"," ")
        email=contact.find('span',id=re.compile("^.*lbEmail$")).get_text().replace(","," ").replace("\n"," ")
        website=contact.find('span',id=re.compile('^.*lbwebsite$')).get_text().replace(","," ").replace("\n"," ")
        mission=bowl.find('div',id="profile").find_all('tr')[3].get_text().replace(","," ").replace("\n"," ")
        

        print(ngoname+","+ngostate+","+location+","+contact_person+","+phone+","+email+","+website+","+mission)
        sys.stdout.flush()



