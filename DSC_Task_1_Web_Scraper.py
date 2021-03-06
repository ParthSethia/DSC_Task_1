import requests
import time
import csv
import re
from bs4 import BeautifulSoup
import os

os.mkdir('book_images')

csv_file = open('bookscrape.csv','w') #creation of csv file
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Serial No.','Category','Title','Rating','Price','Availability'])

URL="https://books.toscrape.com/"
page=requests.get("https://books.toscrape.com/index.html").text

cat_num=1; #the index of category
j=0;       #for the count of books
sno=0;     #for serial numbering in csv file

soup = BeautifulSoup(page,'lxml')

temp=soup.find('ul',class_='nav nav-list')

for temp2 in temp.li.ul.find_all('li'):
	cat_num = int(((temp2.find('a')['href']).split('/')[3]).split('_')[1])
	if cat_num>11:
		break;
	if cat_num!=1:
		cat_url = (temp2.find('a')['href']) #getting url segment specific to a category
		
		cat=(temp2.find('a').text).split()[0] #getting name of the category
		print(cat)
		URL= URL+cat_url #complete url of the respective category (base URL + Category URL Segment)
		
		soup=BeautifulSoup(requests.get(URL).text,'lxml') #updating html according to specific category

		os.makedirs(os.path.join('book_images',cat))

		for book in soup.find_all('li',class_='col-xs-6 col-sm-4 col-md-3 col-lg-3'): #loop for page 1 where number of books is 20
			book_title = book.h3.find('a')['title']
			book_rating = (book.find('p')['class'])[1]
			book_price = book.find('p',class_='price_color').text
			book_availability = book.find('p',class_='instock availability').text
			#getting thumbnails from website and storing them
			x=(book.find('img',class_='thumbnail')['src'])
			img_link = "https://books.toscrape.com/"+x.split('/')[4]+'/'+x.split('/')[5]+'/'+x.split('/')[6]+'/'+x.split('/')[7]+'/'+x.split('/')[8]
			img_data = requests.get(img_link).content
			with open('book_images'+'/'+cat+'/'+book_title+'.jpg','wb+') as f:
				f.write(img_data)

			sno=sno+1 #serial number updation for csv
			csv_writer.writerow([sno,cat,book_title,book_rating,book_price,book_availability])
			j=j+1
			
		if (soup.find('li',class_='next') != None) : #loop for the page 2 if number of books greater than 20
			URL="https://books.toscrape.com/"
			URL=URL+cat_url.split('/')[0]+'/'+cat_url.split('/')[1]+'/'+cat_url.split('/')[2]+'/'+cat_url.split('/')[3]+'/'+soup.find('li',class_='next').find('a')['href'] #updating URL for page 2
			soup=BeautifulSoup(requests.get(URL).text,'lxml')
			for book in soup.find_all('li',class_='col-xs-6 col-sm-4 col-md-3 col-lg-3'): #loop for page 2 books.
				book_title = book.h3.find('a')['title']
				book_rating = (book.find('p')['class'])[1]
				book_price = book.find('p',class_='price_color').text
				book_availability = book.find('p',class_='instock availability').text	
				#getting thumbnails from website and storing them
				x=(book.find('img',class_='thumbnail')['src'])
				img_link = "https://books.toscrape.com/"+x.split('/')[4]+'/'+x.split('/')[5]+'/'+x.split('/')[6]+'/'+x.split('/')[7]+'/'+x.split('/')[8]
				img_data = requests.get(img_link).content
				with open('book_images'+'/'+cat+'/'+book_title+'.jpg','wb+') as f:
					f.write(img_data)

				j=j+1
				sno=sno+1
				csv_writer.writerow([sno,cat,book_title,book_rating,book_price,book_availability]) #writing data to csv file.
				if(j>29):
					break
		f.close()
		j=0

	URL="https://books.toscrape.com/"
csv_file.close()
