#This script scrapes NGO data from www.ngosindia.com
# Uses BeautifulSoup4 and requests libraries
import requests
import json
import pprint
import time
import os
from bs4 import BeautifulSoup

#Function to open webpage and return contents
def urlOpen(url):
    # urlOpen URL return HTML
    try:
        r=requests.get(url, timeout=4)
        return r.text
    except (requests.exceptions.Timeout,requests.exceptions.ConnectionError):
        errfile.write("Timout for URL: "+url+"\n")
        return
#NGO Data File. Open the file
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
top=("State","Name","Add","Pin","Phone","Mobile","Email","Website","Contact Person","Purpose",   "Aims/Objectives/Mission ",)
for columns in top:
    outfile.write(columns+",")
outfile.write("\n")
outfile.close() 

html=urlOpen("http://www.ngosindia.com/ngos-of-india/")
active=""
try:
    soup=BeautifulSoup(html,"lxml")
    active=soup.find_all("ul",{"class" : "active"})
except:
    errfile.write("Failed to create Soup : http://www.ngosindia.com/ngos-of-india/"+"\n")
links_list=list();
for act in active: 

    links=act.find_all("a")
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
       
                
                

            


        

  

        
    
        
   

                          





