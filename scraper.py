def scraper(url):
        from bs4 import BeautifulSoup
        import requests

        headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Language": "en",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
                "Sec-Ch-Ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Windows"',
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            }

        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        wanted = soup.find("div", "HomeCardsContainer flex flex-wrap reversePosition")
        wanted = str(wanted)
        with open("page.html", "w") as html:
            html.write(wanted)
#
# import requests
# import urllib.parse
#
# address = '7166 McCormick Woods Dr SW, Port Orchard, WA 98367'
# url = 'https://nominatim.openstreetmap.org/search?' + urllib.parse.quote(address) +'&format=json'
#
# response = requests.get(url)
# print(response.content)
