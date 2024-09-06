from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import requests
from saveJson import save_json, load_json
from embed import embed
# Set up Chrome options for headless browsing
chrome_options = Options()
chrome_options.add_argument("--headless")

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Define all possible category names, category ids, descriptions, and schema descriptions
all_categories = {
    'independent study': (['independentstudy'], ""),
    'alternative voices': (['alternative_voices'], ""),
    'buildings grounds': (['buildingsgrounds'], ""),
    'campus closeup': (['campuscloseup'], ""),
    'campus council': (['campuscouncil'], ""),
    'commencement': (['commencement'], ""),
    'compton_family': (['compton_family'], ""),
    'compton_family_correspondence': (['compton_family_correspondence'], ""),
    'compton_family_genealogy': (['compton_family_genealogy'], ""),
    'compton_family_photos': (['compton_family_photos'], ""),
    'coronavirus campus': (['coronavirus_campus'], ""),
    'course catalogs': (['course_catalogs'], ""),
    'directories': (['directories'], ""),
    'galpin takeover': (['galpintakeover'], ""),
    'herbarium sheets': (['herbariumsheets'], ""),
    'lybarger': (['lybarger'], ""),
    'marybehner papers': (['marybehner_papers'], ""),
    'mother home heaven': (['motherhomeheaven'], ""),
    'notestein': (['notestein'], ""),
    'notestein family': (['notestein_family'], ""),
    'presidents': (['presidents'], ""),
    'davis world war II': (['davisworldwarII'], ""),
    'theatre dance': (['theatredance'], ""),
    'lowry addresses': (['lowryaddresses'], ""),
    'index': (['index1870-1920', 'index1920-1970', 'index1970-2017'], ""),
    'voice': (['voice1890-1900', 'voice1901-1910', 'voice1911-1920', 'voice1921-1930', 'voice1931-1940', 'voice1941-1950', 'voice1951-1960', 'voice1961-1970', 'voice1971-1980', 'voice1981-1990', 'voice1991-2000', 'voice2001-2011', 'voice2012-2020'], ""),
    'wooalumnimag': (['wooalumnimag_1981-1990', 'wooalumnimag_1991-2000', 'wooalumnimag_2001-2010', 'wooalumnimag_2011-present'], "")
}

# Define all possible element IDs, split characters, and element names
all_elements = {
    'title': (None, 'title'),
    'authors': (None, 'authors'),
    'abstract': (None, 'abstract'),
    'advisor1': (None, 'advisor'),
    'city': (None, 'city'),
    'coverage': (None, 'coverage'),
    'format': (None, 'format'),
    'subject_area': (';', 'department'),
    'recommended_citation': (None, 'recommended_citation'),
    'bp_categories': ('|', 'disciplines'),
    'keywords': (',', 'keywords'),
    'publication_date': (None, 'publication_date'),
    'degree_granted': (None, 'degree_granted'),
    'document_type': (None, 'document_type'),
    'article-downloads': (None, 'downloads'),
    'subject': (';', 'subject'),
    'source': (None, 'source'),
    'rights': (None, 'rights'),
    'publisher': (None, 'publisher'),
    'relation': (None, 'relation'),
    'identifier': (None, 'identifier'),
    'dc_subject': (';', 'dc_subject'),
    'length': (None, 'length')
}

def extract_page_elements(soup):
    page_elements = {}
    # Get text content for all elements
    for element_id, (split_char, element_name) in all_elements.items():
        element = soup.find(attrs={'id': element_id})
        if element:
            text = element.find('p').text if element.find('p') else element.text
            if split_char:
                page_elements[element_name] = [item.strip() for item in text.split(split_char) if item.strip()]
            else:
                page_elements[element_name] = text.strip()
    return page_elements

def scrape_openworks_page(url):
    driver.get(url)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    result = {'url': url, 'downloads': "0", 'status': '200'}
    if soup.find('div', id='404-error'):
        result['status'] = '404'
        return result

    result.update(extract_page_elements(soup))
    return result

def scrape_independent_study():
    data = load_json('resources/independentstudy.json')
    for i in range(1, 5):
        if i > len(data):
            url = f"https://openworks.wooster.edu/independentstudy/{i}/"
            result = scrape_openworks_page(url)
        else:
            result = data[i-1]
        if i <= len(data):
            data[i-1] = result
        else:
            data.append(result)
    save_json(data, 'resources/independentstudy.json')

# Example usage
if __name__ == "__main__":
    scrape_independent_study()
    driver.quit()