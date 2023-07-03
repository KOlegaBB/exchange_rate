import aiohttp
import asyncio
from bs4 import BeautifulSoup


async def get_response(request):
    """
    Function to get response from http request
    :param request: string, link of request
    :return: string, html page of response
    """
    try:
        async with aiohttp.ClientSession(headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/95.0.4638.54 Safari/537.36',
        }) as session:
            async with session.get(request) as response:
                return await response.text()
    except aiohttp.ClientConnectorError as e:
        print(f"Connection error: {str(e)}")
        return None


async def parse_html(page, elem_type, classes):
    """
    Get data from element in html page
    :param page: string, html page
    :param elem_type: string, type of element
    :param classes: string, classes of element 'class_1 class_2 ... class_n'
    :return: string, data from element
    """
    soup = BeautifulSoup(page, "html.parser")
    return soup.find(elem_type, class_=classes).text


async def get_rate():
    """
    Get current rate of 1 dollar to hryvnas
    :return: string: exchange rate
    """
    response = await get_response(
        "http://www.google.com/search?q=1+долар+в+грн")
    if not response:
        return None
    rate = await parse_html(response, "span", "DFlfde SwHCTb")
    return rate


async def main():
    """
    Main function to run get_rate function
    """
    rate = await get_rate()
    if rate:
        print(f"Current rate: {rate}")
    else:
        print(f"Can't get current rate")


if __name__ == "__main__":
    asyncio.run(main())
