# A script to scrape NGO data off NGOPortal.org. Uses BS4 and requests.
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
    time.sleep(.2)

    try:
        r = requests.get(url, timeout=7)
        return r.text
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        errfile.write("Timout for URL: " + url + "\n")
        return

        
# NGO Data File. Open the file
filename="redo.csv"
try:
    os.remove(filename)
except:
    pass

redofile=open(filename,"a")
errfilename="Errors.log"
try:
    os.remove(errfilename);
except: 
    pass
errfile=open(errfilename,"a")


#Create outfile header




print("Name,  Location, Phone,Contact person, Email, Website, Activities")
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
for letter in letters:
    url="http://www2.ngoportal.org/ngo_database.html?alpha="+letter +"&key_value=0"
    html=urlOpen(url)
    # print ("For state %s opened url %s"% (state,url))
    candidates=""
    try:
        soup=BeautifulSoup(html,"lxml")
        # print(soup)
        candidates=soup.find_all("h3")
       # print( len(outer))

    except Exception as e:
        
        errfile.write("Failed to prepare Soup : "+state+"    :"+e+":URL = "+url+"\n")

    links_list=list();
    ngos={};
   

    for candidate in candidates: 
        # print( node.contents)
        orgcontact=""
        orgemail=""
        orgphone=""
        orgname=""
        orgprogram=""
        orgcause=""
        orgsubcause=""
        orgbeneficiaries=""
        bowl=""
        a=candidate.find('a')

        if a and re.compile('^ngo-database.*$').match(a.get('href')):

            orgname=candidate.find('a').get_text().replace(","," ").strip()
            orglink="http://www2.ngoportal.org/"+ candidate.find('a')['href']
            #print(orglink)
            orgpage=urlOpen(orglink)
            try:
                bowl=BeautifulSoup(orgpage,'lxml')
                h1s=bowl.find_all('h1')
                for h1 in h1s:
                    if("NGO Management" in h1.get_text() ):
                        # print("Wrong H1")
                        continue
                    #print(orgname)
                    orgname=h1.get_text().replace(","," ").strip()
                    #print(orgname)
                    div=h1.find_next_sibling()
                    p=div.find("p")
                    #print(str(p))
                    details=(str(p)).split("<br/>")

                    contact=details[-1]
                    #print(len(details))
                    for d in details:
                        #print("("+d+")")
                        pass
                    #print( "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                    
                    orglocation=details[1].replace(",", "-").strip()
                    orgphone=details[2].replace(","," ").strip()
                    orgcontact=details[3].replace("Contact:"," ") if "Contact" in details[3] else ""
                    orgcontact=orgcontact.replace(","," ").strip()
                    
                    #contact_list=contact.split("<br/>")
                    # print(len(contact_list))
                    orgemail=details[5].replace("E-mail:","").replace(","," ").strip()
                    orgmobile=details[4].replace("Mobile Number:","").replace(","," ").strip()
                    orgwebsite=details[6].replace("Website:","").replace(",","").strip()
                    orgactivities=p.find_next_sibling().get_text().strip().replace(","," ").replace("\n", " ")
                    print(orgname+","+orglocation+","+orgphone+"/"+orgmobile+","+orgcontact+","+orgemail+","+orgwebsite+","+orgactivities)
                    
                    sys.stdout.flush()
            except Exception as e :
                errfile.write( " Exception occured on page " + orglink +" exception: "+str(e))
                redofile.write(orgname+","+orglink+","+str(e)+"\n")
                redofile.flush()




errfile.close()







