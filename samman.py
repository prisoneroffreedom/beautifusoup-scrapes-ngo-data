# A script to get NGO data off BSE Samman website
import requests
import json
import re

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
    outfile.write(columns+",")
outfile.write("\n")
outfile.close() 
print("Name, Program, Location, Cause, Subcause, Beneficiaries,Contact person, Email, Phone")

for state in states_tup:
    url="http://www.bsesammaan.com/searchMain.aspx?stat="+state+"&cty=City&cause=&subcause=&Bef="
    html=urlOpen(url)
    # print ("For state %s opened url %s"% (state,url))
    outer=""
    try:
        soup=BeautifulSoup(html,"lxml")
        # print(soup)
        outer=soup.find_all("a",id = re.compile(".*hlOrganization$"))
       # print( len(outer))

    except Exception as e:
        
        errfile.write("Failed to prepare Soup : "+state+"    :"+e+":URL = "+url+"\n")

    links_list=list();
    ngos={};
   

    for node in outer: 
        # print( node.contents)
        time.sleep(.15)
        orgcontact=""
        orgemail=""
        orgphone=""
        orgname=""
        orgprogram=""
        orgcause=""
        orgsubcause=""
        orgbeneficiaries=""

        orgname=node.get_text().replace("&nbsp",'')
        dadaji=node.parent
        dadaji=dadaji.next_sibling
        orgprogram=dadaji.a.get_text()
        dadaji=dadaji.next_sibling
        orglocation=dadaji.a.get_text()
        dadaji=dadaji.next_sibling
        orgcause=dadaji.a.get_text()
        dadaji=dadaji.next_sibling
        orgsubcause=dadaji.a.get_text()
        dadaji=dadaji.next_sibling
        orgbeneficiaries=dadaji.a.get_text()

        try:
            link="http://www.bsesammaan.com/"+node['href']
            inner=urlOpen(link)
            bowl=BeautifulSoup(inner,'lxml')
            contact_node=bowl.find('span', id=re.compile('^.*lblContactName$'))
            orgcontact=contact_node.get_text()

            landline=bowl.find('span', id=re.compile('^.*lblLandline$'))
            if (landline):
                orgphone += landline.get_text()
            mobile=bowl.find('span',id=re.compile('^.*lblMobile$'))
            if(mobile):
                orgphone+=mobile.get_text()
            
            email_node=bowl.find('a',id=re.compile('^.*orgmail$'))
            orgemail=email_node.get_text()


        except Exception as e:
            errfile.write("Problem in bowl"+link+"\n Exception :"+str(e))
        ngo = ngos.get(orgname)
        if ngo:
            ngo['location'] +="  "+orglocation.replace(state,"")
            print ("duplicate")
        else:
            ngo={}
            ngo['name']=orgname
            ngo['program']=orgprogram
            ngo['location']=orglocation
            ngo['cause'] =orgcause
            ngo['subcause']=orgsubcause
            ngo['beneficiaries']=orgbeneficiaries
            ngo['contact']=orgcontact
            ngo['phone']=orgphone
            ngo['email'] =orgemail
            ngos[orgname]=ngo

    print (len(ngos))
    for name,ngo in ngos.items():
        print(ngo['name'],ngo['program'],ngo['location'],ngo['cause'],ngo['subcause'],ngo['beneficiaries'],ngo['contact'],
        ngo['email'],ngo['phone'], sep=",")
       

errfile.close()




