
from amazon_scrapper import get_amazon_products
from takealot_scrapper import get_takealot_products
import asyncio
from headers import headers


def text_search (search):

    async def main():
        result = await asyncio.gather(get_amazon_products(headers, search), get_takealot_products(search))
        return result

    resp = asyncio.run(main())
    
    all_results = []
    all_results.append(resp[0])
    all_results.append(resp[1])

    return all_results
