def extractor(address, bed, bath, sqft, price, url, geo, final, parcel_id, year_built):
    from bs4 import BeautifulSoup
    import json
    from parcel import parcel_scraper
    import pytz
    from datetime import datetime
    # with open("page.html", "r") as resource:
    #     soup = BeautifulSoup(resource, "html.parser")
        # address = []
        # bed = []
        # bath = []
        # sqft = []
        # price = []
        # url = []
        #
        # for text in soup.find_all("a"):
        #     address.append(text.text)

        # for link in soup.find_all("a"):
        #     test = link.get("href")
        #     url.append(test)

        # print(url)


    i = 0
    with open("page.html", "r") as resource:
        soup = BeautifulSoup(resource, "html.parser")
        tag = soup.find_all("script")
        script = []
        for text in soup.find_all("span", "bp-Homecard__Stats--baths text-nowrap"):
            bath.append(text.text)

        for test in tag:
            if "startDate" not in test.text:
                script.append(test.text)

        for j in range(len(script) - 1):
            data = json.loads(script[j])
            address.append(data[0]['name'])
            # print(address)
            part = data[0]['name'].split(" ")
            need = f"{part[0]}+{part[1]}+{part[2]}"
            url1 = f"https://psearch.kitsap.gov/pdetails/Default?parcel={need}&type=site"
            # print(url1)
            parcel_scraper(url1, year_built, parcel_id)
            PST = pytz.timezone("US/Pacific")
            datetime_pst = datetime.now(PST)
            current_time = datetime_pst.strftime("%Y-%m-%d %H:%M:%S")
            # print(year_built)
            # print(parcel_id)
            # print(address)
            price.append(data[1]['offers']['price'])
            url.append(data[0]['url'])
            bed.append(data[0]['numberOfRooms'])
            sqft.append(data[0]['floorSize']['value'])
            geo.append(f"latitude {data[0]['geo']['latitude']} longitude {data[0]['geo']['longitude']}")
            if url.count(url[0]) > 1:
                break


        for i in range(len(url)):
            if url.count(url[0]) > 1:
                break
            else:
                final.append((address[i], bed[i], bath[i], sqft[i], geo[i], price[i], url[i], parcel_id[i], year_built[i], current_time))



