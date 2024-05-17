from playwright.sync_api import sync_playwright
from google_lens import run
import time

# Start the timer
start_time = time.time()
image_url = 'https://user-images.githubusercontent.com/81998012/210290011-c175603d-f319-4620-b886-1eaad5c94d84.jpg'
image_url2 ='https://shop.medindia.com/content/images/thumbs/0001450_morpheme-memocare-plus-for-mental-alertness-500mg-extract-60-veg-capsules-2-bottles_300.jpeg'
with sync_playwright() as playwright:
   name_list , name = run(playwright , image_url)

# Calculate the elapsed time
elapsed_time = time.time() - start_time

# Print the results and the elapsed time
print("Name list:", name_list)
print("Name:", name)
print("Elapsed time:", elapsed_time, "seconds")