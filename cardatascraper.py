# import libraries
from bs4 import BeautifulSoup
import requests
import csv

def getCarData(page = 1):
    cars = []
    url = f'https://www.marutisuzukitruevalue.com/used-cars-in-bengaluru/{page}#page={page}'
    # get html content
    content = requests.get(url)._content
    soup = BeautifulSoup(content, 'html.parser')

    # get total cars
    # total_cars = soup.find(class_="total_car").text.split()[0]
    # print("Total available cars: {}\n".format(total_cars))
    print("Page", page)

    # get the cards of cars
    car_boxes = soup.find_all(class_="carBox")
    for car_box in car_boxes:
        # get name of car
        name = car_box.h5.a.text
        # print(name)
        # get details of car
        # year, fuel type, kms driven
        details = car_box.find(class_ = "details").text.strip()
        year, fuel, kms = details.split('\n')
        # remove spaces and km
        kms = kms.replace(' ','')[:-2]
        # print("Details: {} | {} | {}s driven".format(*x))
        # get the price
        price = car_box.find(class_ = "priceSection").span.text.replace(' ','')[1:]
        # print("Price: ₹{}\n".format(price))
        cars.append([name, year, fuel, kms, price])
    return cars

def getNumberOfPages():
    url = "https://www.marutisuzukitruevalue.com/used-cars-in-bengaluru"
    # get html content
    content = requests.get(url)._content
    soup = BeautifulSoup(content, 'html.parser')
    # get the pagination element
    pagination = soup.find(class_ = "paginationonCarListing").ul.text
    # get last second element => last page number
    pgs = int(pagination.split()[-2])
    return pgs

# get data from all pages
ncars = []
pgs = getNumberOfPages()
# print(pgs)
for i in range(1,pgs+1):
    cars = getCarData(page=i)
    ncars.extend(cars)
print("Web Scraping Done!!")
# print(ncars)

# write data to csv
with open ('cardata.csv','w', newline='') as file:
    writer=csv.writer(file)
    writer.writerow(['Name','Year','Fuel','Kilometers driven','Price'])
    for row in ncars:
        writer.writerow(row)
print("Writing to csv done")

# TODO
# 1. Handle pagination - DONE
# 2. Save results to csv file