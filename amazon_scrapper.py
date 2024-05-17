
import requests as r
import bs4 
import random
import lxml
import re
from headers import headers

# google-bot header : Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/W.X.Y.Z Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)
# Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1
#TODO: implement an algorithm to group same product together
#TODO: also fetch ratings and how many people rated the product and product name
#TODO: ___ from fake_useragent import UserAgent headers = {"User_Agent":UserAgent().random}
def get_amazon_products(headers):
  
    base_url = "https://www.amazon.co.za"
    url = "https://www.amazon.co.za/s?k=phone+case"

    headers = random.choice(headers)

    base_response = r.get(base_url, headers=headers)

    if base_response.status_code == 200:
        cookies = base_response.cookies
        product_response = r.get(url, headers=headers, cookies=cookies)
        soup = bs4.BeautifulSoup(product_response.text, features="lxml")

        price_lines = soup.find_all(class_="a-price-whole")
        a_tags = soup.find_all('a', class_='a-link-normal s-no-outline')
        image_link = soup.find_all('img', class_='s-image')

        image_src = [img['src'] for img in image_link[:3]]  # Limit to 3 images

        pattern = re.compile(r'/dp/([^/]+)')
        product_links = [pattern.search(a_tag['href']).group(1) for a_tag in a_tags[:3]]

        prices = [str(price).replace('<span class="a-price-whole">', '').replace(
            '<span class="a-price-decimal">.</span></span>', '') for price in price_lines[:3]]

        # Creating a dictionary for each product with its details
        products = []
        for i in range(3):
            product = {
                "product_link": f"{base_url}/dp/{product_links[i]}",
                "price": prices[i],
                "image_link": image_src[i]
            }
            products.append(product)

        return products

    return None

# Calling the function to get the products
products = get_amazon_products(headers)

if products:
    for product in products:
        print(product)
else:
    print("Failed to retrieve product information.")
