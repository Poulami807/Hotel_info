
import requests
from bs4 import BeautifulSoup
import pandas
import sys
import sql


max_pg = int(sys.argv[1])
url="https://www.oyorooms.com/hotels-in-bangalore/?page=1"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
scraped_info_list=[]
database=sys.argv[2]
sql.create(database) #passing dbname as a parameter


for page in range(1,max_pg):
    req=requests.get(url+str(page),headers=headers)
    content=req.content
    soup=BeautifulSoup(content,"html.parser")
    hotels=soup.find_all("div",{"class":"hotelCardListing"})
    for hotel in hotels:
         
         hotel_dict={}
         hotel_dict["name"]=hotel.find("h3",{"class":"listingHotelDescription__hotelName"}).text

         hotel_dict["address"]=hotel.find("span",{"itemprop":"streetAddress"}).text
                  

         try:
            hotel_dict["price"]=hotel.find("span",{"class":"listingPrice__finalPrice"}).text
            hotel_dict["rating"]=hotel.find("span",{"class":"hotelRating__rating"}).text
            

         except AttributeError:
            hotel_dict["price"]=None
            hotel_dict["rating"]=None
    
         parent_amenities_element=hotel.find("div",{"class":"amenityWrapper"})
         amenities_list=[]
         for amenity in parent_amenities_element.find_all("div",{"class":"amenityWrapper__amenity"}):
                 amenities_list.append(amenity.find("span",{"class":"d-body-sm"}).text.strip())
         hotel_dict["amenities"]=', '.join(amenities_list[:-1])
         scraped_info_list.append(hotel_dict)
         
         sql.insert(database,tuple(hotel_dict.values()))
          



dataframe=pandas.DataFrame(scraped_info_list)
dataframe.to_csv(url.split('/')[3]+'.csv')

sql.get_info(database)
        
         