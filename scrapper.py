
import requests as r
import bs4 
import random
import lxml
import re
from headers import headers

# google-bot header : Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/W.X.Y.Z Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)
# Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1
#TODO: use mutiple headers
#TODO: ___ from fake_useragent import UserAgent headers = {"User_Agent":UserAgent().random}
def get_amazon_products(headers):

  base_url = "https://www.amazon.co.za"

  url = "https://www.amazon.co.za/s?k=phone+case"

  headers = random.choice(headers)


  base_response = r.get(base_url , headers=headers)

  if base_response.status_code == 200:

    cookies = base_response.cookies

    product_response = r.get(url , headers=headers , cookies=cookies)
    soup = bs4.BeautifulSoup(product_response.text, features="lxml")

    price_lines = soup.find_all(class_ = "a-price-whole")
    a_tags = soup.find_all('a', class_='a-link-normal s-no-outline')
    image_link =soup.find_all('img', class_ ='s-image')

    #get link for the image
    for img in image_link:
      src = img['src']
      print(src)
      break


    counter = 0

    #regex pattern to extract the part after dp/
    pattern = re.compile(r'/dp/([^/]+)')

    # Extract and print the href attribute for each anchor tag
    for a_tag in a_tags:
        href = a_tag['href']

        match = pattern.search(href)

        if match:
            product_id = match.group(1)
            print(product_id)

        counter +=1
        if counter == 1:
          break

    final_price =str(price_lines[0])

    final_price = final_price.replace('<span class="a-price-whole">', '')
    final_price = final_price.replace('<span class="a-price-decimal">.</span></span>', '')
    print(final_price)
    print("link" , href)

  
get_amazon_products(headers)
#TODO: get three products add tnem to a dict and return them