
import requests as r
import bs4 
import lxml
import random
from urllib.parse import quote_plus
import re

# google-bot header : Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/W.X.Y.Z Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)
# Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1
#TODO: implement an algorithm to group same product together
#TODO: also fetch ratings and how many people rated the product
#TODO: ___ from fake_useragent import UserAgent headers = {"User_Agent":UserAgent().random}

def get_amazon_products(headers , search_query):
    base_url = "https://www.amazon.co.za"
    encoded_query = quote_plus(search_query)
    search_url = f"{base_url}/s?k={encoded_query}"
    
 
    # Choose a random header from the headers list
    chosen_header = random.choice(headers)

    # Make a base request to get initial cookies
    base_response = r.get(base_url, headers=chosen_header)

    if base_response.status_code == 200:
        # Retrieve cookies from the base response
        cookies = base_response.cookies

        # Make a request to the search URL with the retrieved cookies
        product_response = r.get(search_url, headers=chosen_header, cookies=cookies)
        soup = bs4.BeautifulSoup(product_response.text, features="lxml")

        # Find the product list
        product_list = soup.find_all('div', class_='s-main-slot s-result-list s-search-results sg-row')[0].find_all('div', {'data-component-type': 's-search-result'})

        products = []
        pattern = re.compile(r'/dp/([^/]+)')

        for product in product_list[:15]:  # Limit to 15 products
            # Extract product link and Amazon ID
            product_link_tag = product.find('a', class_='a-link-normal s-no-outline')
            if product_link_tag:
                href = product_link_tag['href']
                match = pattern.search(href)
                product_amazon_id = match.group(1) if match else "N/A"
                product_link = f"{base_url}/dp/{product_amazon_id}" if match else "N/A"
            else:
                product_link = "N/A"
                product_amazon_id = "N/A"

            # Extract price
            price_tag = product.find('span', class_='a-price-whole')
            price = price_tag.get_text() if price_tag else "N/A"

            # Extract image link
            image_tag = product.find('img', class_='s-image')
            image_link = image_tag['src'] if image_tag else "N/A"

            # Extract product name
            product_name_tag = product.find('span', class_='a-size-base-plus a-color-base a-text-normal')
            product_name = product_name_tag.get_text() if product_name_tag else "N/A"

            # Extract rating
            rating_tag = product.find('span', class_='a-icon-alt')
            if rating_tag:
                rating = rating_tag.get_text().split(' ')[0]  # Get the first part which is the numerical value
            else:
                rating = "N/A"

            # Extract number of ratings
            number_of_ratings_tag = product.find('span', class_='a-size-base s-underline-text')
            number_of_ratings = number_of_ratings_tag.get_text() if number_of_ratings_tag else "No ratings"

            # Create product data dictionary
            product_data = {
                "product_link": product_link,
                "product_id": product_amazon_id,
                "price": price,
                "image_link": image_link,
                "product_name": product_name,
                "rating": rating,
                "number_of_ratings": number_of_ratings
            }
            products.append(product_data)

        return products

    return None


