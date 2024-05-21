from playwright.sync_api import sync_playwright
from google_lens import run
from amazon_scrapper import get_amazon_products
from takealot_scrapper import get_takealot_products
import asyncio
from headers import headers
import time


start = time.time()

image_url = 'https://user-images.githubusercontent.com/81998012/210290011-c175603d-f319-4620-b886-1eaad5c94d84.jpg'
image_url2 ='https://shop.medindia.com/content/images/thumbs/0001450_morpheme-memocare-plus-for-mental-alertness-500mg-extract-60-veg-capsules-2-bottles_300.jpeg'
with sync_playwright() as playwright:
   name_list , search_word = run(playwright , image_url)

search = search_word
print(f'searching for : {search}')
print(f'spent : {time.time() - start } seconds on google lens')
async def main():
    result = await asyncio.gather(get_amazon_products(headers, search), get_takealot_products(search))
    return result

all_results = asyncio.run(main())

end = time.time()

time_elapsed = end - start

print(all_results)
print(f'time elapsed : {time_elapsed}')