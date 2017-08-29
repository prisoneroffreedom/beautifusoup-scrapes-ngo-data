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
'''

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

"""

//////////////////////////////////////////////////////////////////////////////////////

        name=node
    for link in links:  #  List of States
        #print ("Parsing "+link['href'])
        #print ()
        links_list.append(link['href'])

    output=list()
    for link in links_list:  #  List of States 
        #print( link)
        jsont=urlOpen(link+"/wp-json/wp/v2/pages")
        state_pages=list()
        try:
        
            decoder=json.JSONDecoder()
            json_data= decoder.decode(s=jsont)
        except :
            errfile.write("JSON Error in reading: "+link+"\n")
            continue
        for data in json_data:
        if isinstance(data, dict):
            url=data["guid"]["rendered"]
            if url.find("page_id=")!= -1:
                #print( url)
                state_pages.append(url)
    #raw_input("Press Enter to continue...")
    for page in state_pages:
        end=page.find("ngosindia.com")
        state=page[7:end]
        print state
        html=urlOpen(page)
        soup=""
        article=""
        try:
            soup=BeautifulSoup(html,'lxml')
            article=soup.find("article")
        except:
            errfile.write("BS4 Error in reading: "+page+"\n")
            continue
      
        rows=article.find_all("li");
        for row in rows:
            try:          
                link=row.find("a")    
                name=link['title']
                scrapeUrl=link['href'] 
            except:
                errfile.write("Can't find scrape URL: "+ str(row)    + "\n")
                continue
                
            out={"Name" : name,"ScrapeUrl" : scrapeUrl,"State":state[:-1]}
            #print("opening-> "+scrapeUrl)
            time.sleep(.1)
            html2=urlOpen(scrapeUrl)
            content=""  
            info=""
            try:
                soup=BeautifulSoup(html2,'lxml')
                content=soup.h1.parent
            except:
                errfile.write("BS4 Error in reading: "+scrapeUrl+"\n")
                continue

                
            if content!="":
                info=content.text.replace("\n","    ")
            #print(info)
            headings=("Add","Pin","Phone","Mobile","Email","Website","Contact Person","Purpose",  "Purpose",  "Aims/Objectives/Mission ",)
            delim="**DELIMITER**"
            info=info.replace("Tel:","Phone:")
            info=info.replace("Aim/Objective/Mission","Aims/Objectives/Mission")
            for item in headings:
                pos=info.find(item)
                if pos>-1 :
                    info=info[:pos]+delim+info[pos:]
            info+=delim
            for item in headings:
                pos=info.find(item)
                if pos>-1 :
                    sub=info[pos:]
                    end=sub.find(delim)
                    value=sub[len(item)+1:end]
                    #value=info[pos:info.find("<br/>",beg=pos)]
                    out[item]=value
                else:
                    print(item + " not found  ")
                    continue

            outfile=open(filename,"a")
            
            for columns in top:
                if out.get(columns):
                    outfile.write(','+out.get(columns).replace(",","").encode("utf8"))
                else:
                    outfile.write(',')
            outfile.write("\n")
            outfile.close()
        errfile.close()
        errfile=open(errfilename,"a")

outfile.close()
errfile.close()
       
"""
'''
                

            


        

  

        
    
        
   

                          





