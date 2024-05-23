import asyncio
from playwright.async_api import async_playwright
import requests as r
import bs4 
import lxml
import random
from urllib.parse import quote_plus
from urllib.parse import urlparse, unquote
from headers import headers
import re
import time

# google-bot header : Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/W.X.Y.Z Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)
# Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1
#TODO: implement an algorithm to group same product together
#TODO: also fetch ratings and how many people rated the product
#TODO: ___ from fake_useragent import UserAgent headers = {"User_Agent":UserAgent().random}

async def get_takealot_products( search_query):
    async with async_playwright() as playwright:

        base_url = "https://www.takealot.com/"
        base_for_product_url = "https://www.takealot.com"
        encoded_query = quote_plus(search_query)
        search_url = f"{base_url}all?_sb=1&_r=1&_si=0042de8ba5dd00715c1d7950eea9c2f7&qsearch={encoded_query}"
        
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        #page.goto('https://www.takealot.com/all?_sb=1&_r=1&qsearch=phone%20cases%20s23&via=suggestions&_si=55813baf4a814d46e51fc7b502fa7bf6')
        await page.goto(search_url)
        print(search_url)
        #time.sleep(15)
        # Waiting for the content to load
        #page.wait_for_selector('.product-card product-card-module_product-card_fdqa8', timeout=60000)

        content = await page.content()
        soup = bs4.BeautifulSoup(content, 'html.parser')
        await page.close()
        await browser.close()
        #print(soup)

        # Make a base request to get initial cookies
        #base_response = r.get(base_url, headers=chosen_header)

        # Find the product list
        product_list = soup.find_all( class_ ="product-card")
        #print(product_list[:1])
        products = []

        for product in product_list[:15]:  # Limit to 15 products
            # Extract product title
            title_tag = product.find('h4', class_="product-title")
            product_title = title_tag.text if title_tag else "N/A"

            # Extract product price
            price_tag = product.find('li', class_="price")
            if price_tag:
                price_text = price_tag.text.strip()
                product_price = float(re.sub(r'[^\d.]', '', price_text))  # Remove non-numeric characters
            else:
                product_price = 'N/A'

            # Extract the product URL
            url_tag = product.find('a', class_="product-anchor")
            if url_tag:
                url = url_tag['href'] 
                product_url = f'{base_for_product_url}{url}'
            else: 
                "N/A"

            # Extract product image URL
            img_tag = product.find('img', {'data-ref': 'product-thumb'})
            product_img_url = img_tag['src'] if img_tag else "N/A"

            # Extract rating if available (convert to float)
            rating_tag = product.find('div', class_="rating-module_rating-wrapper_3Cogb")
            if rating_tag:
                rating_text = rating_tag.text.strip()
                product_rating = float(re.search(r'\d+(\.\d+)?', rating_text).group())  # Extract the numeric part
            else:
                product_rating = 'N/A'

            # Extract number of ratings (convert to int)
            num_ratings_tag = product.find('span', class_="rating-module_review-count_3g6zO")
            if num_ratings_tag:
                num_ratings_text = num_ratings_tag.text.strip()
                num_ratings = int(re.search(r'\d+', num_ratings_text).group())  # Extract the numeric part
            else:
                num_ratings ='N/A'

            # Extract product ID from URL
            if product_url != "N/A":
                product_id = unquote(urlparse(product_url).path.split('/')[-1])
            else:
                product_id = "N/A"

            products.append({
                'product_name': product_title,
                'price': product_price,
                'product_url': product_url,
                'image_url': product_img_url,
                'rating': product_rating,
                'num_ratings': num_ratings,
                'product_id': product_id,
                "store":"takealot"
            })

        return products



#products =  asyncio.run(get_takealot_products( "iphone case s23"))
#print(products)