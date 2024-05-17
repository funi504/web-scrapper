from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def run(playwright , image_url):
   
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(f'https://lens.google.com/uploadbyurl?url={image_url}&hl=en')

    # Waiting for the content to load
    page.wait_for_selector('.kuwdsf .VfPpkd-RLmnJb', timeout=15000)

    content = page.content()
    soup = BeautifulSoup(content, 'html.parser')
    page.close()
    browser.close()

    # Parsing the reverse image search link
    #print(soup)
    reverse_image_search_element = soup.select_one('.DeMn2d')
    # Finding all elements with class 'xQ4tVe'
    all_results = soup.find_all(class_='xQ4tVe')

   
    if reverse_image_search_element is None or all_results is None:
        # if theres no title in results for reverse image search use the desc
        reverse_image_search_element_desc = soup.select_one('.UAiK1e')
        #if reverse image search element desc is also none
        if reverse_image_search_element_desc is None:
            return None , None
        
        desc = [result.get_text() for result in reverse_image_search_element_desc]
        return desc, desc[0]

    else:
        all_results_name = []
        # Printing the text content of the selected elements
        estimated_element = reverse_image_search_element.get_text()
        all_results_texts = [result.get_text() for result in all_results]

        for text in all_results_texts:
            #print(text)
            all_results_name.append(text)
        
        return all_results_name , estimated_element

