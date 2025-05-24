def parcel_scraper(url1, year_built, parcel_id):
    import requests
    from bs4 import BeautifulSoup

    response1 = requests.get(url1)

    soup = BeautifulSoup(response1.text, "html.parser")
    data = soup.find("ul", "dropdown-menu")
    try:
        data_parc = soup.find("div", "panel-body").h4.text.split(" ")
        parcel = data_parc[18].strip("\n").strip("\r")
        parcel_id.append(parcel)
        data_year = soup.find("table", "table table-striped table-bordered table-hover").tbody
        for prop_class in data_year.find_all("tr"):
            if prop_class.td.text.strip("\n") == "Property Class":
                condition = prop_class.td.next_sibling.next_sibling.text
                if "910" in condition:
                    year_built.append(condition)
                else:
                    for link in data.find_all("a"):
                        if "Buildings & Improvements" in link.text:
                            url2 = f"https://psearch.kitsap.gov{link.get("href")}"
                            # parcel_id.append(url2)
                            response2 = requests.get(url2)
                            soup = BeautifulSoup(response2.text, "html.parser")
                            data = soup.find("table", "table table-striped table-bordered table-hover")
                            for year in data.find_all("tr"):
                                if year.td.text == "Year Built":
                                    year_ = year.td.next_sibling.text
                                    year_built.append(year_)
    except AttributeError:
        year_built.append("None")
        parcel_id.append("None")