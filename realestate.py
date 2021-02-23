import requests #for sending requests to our URL
from bs4 import BeautifulSoup # to parse our request URL's html into something we can read
import pandas # for rendering our data as a data frame, then as an excel/csv file

#defining headers
headers = {
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}



r = requests.get("http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/",
headers= headers)

#append to url to go thorugh pages
#t=0&s=0
#t=0&s=10
#t=0&s=20
#t=0&s=30 etc



c=r.content

soup = BeautifulSoup(c,"html.parser")

all = soup.find_all("div", {"class":"propertyRow"})

#finding page count
page_nr=soup.find_all("a", {"class": "Page"})[-1].text


l= []
#base url for pagination
base_url = "http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
#because the pagination url goes 10, 20, 30 etc, we need to multiply page count by 10
for page in range(0,int(page_nr)*10, 10):
    
    r= requests.get(base_url +str(page)+".html", headers = headers)
    c= r.content
    soup= BeautifulSoup(c,"html.parser")
    all = soup.find_all("div", {"class":"propertyRow"})
    #creating library for each listing to store all our dataframe fields
    for item in all:
        d={}
        try:
            d["Address"]=item.find_all("span",{"class": "propAddressCollapse"})[0].text
        except:
            d["Address"]=None
        try:
            d["State"]=item.find_all("span",{"class": "propAddressCollapse"})[1].text
        except:
            d["State"]=None
        d["Price"]=item.find("h4",{"class":"propPrice"}).text.replace("\n","").replace(" ","")
        try:
            d["Beds"]=item.find("span" ,{"class": "infoBed"}).find("b").text
        except:
            d["Beds"]=None
        try:
            d["Sq Ft"] = item.find("span" ,{"class": "infoSqFt"}).find("b").text
        except:
            d["Sq Ft"] =None

        try:
            d["Full Baths"]=item.find("span" ,{"class": "infoValueFullBath"}).find("b").text
        except:
            d["Full Baths"] = None

        try:
            d["Half Baths"] = item.find("span" ,{"class": "infoValueHalfBath"}).find("b").text
        except:
            d["Half Baths"] = None
        
        for column_group in item.find_all("div", {"class":"columnGroup"}):
        
            for feature_group, feature_name in zip(column_group.find_all("span", {"class": "featureGroup"}), column_group.find_all("span", {"class": "featureName"})):
                if "Lot Size" in feature_group.text:
                    d["Lot Size"] = feature_name.text
        #appending to our list
        l.append(d)

#exporting to a dataframe
df= pandas.DataFrame(l)
#rendering csv
df.to_csv("Output.csv")
   