from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
# Set up Chrome options for headless browsing
chrome_options = Options()
chrome_options.add_argument("--headless")

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Define all possible element IDs, split characters, and element names
all_elements = {
    'title': None,
    'authors': None,
    'abstract': None,
    'advisor1': None,
    'city': None,
    'coverage': None,
    'format': None,
    'subject_area': ';',
    'recommended_citation': None,
    'bp_categories': '|',
    'keywords': ',',
    'publication_date': None,
    'degree_granted': None,
    'document_type': None,
    'article-downloads': None,
    'subject': ';',
    'source': None,
    'rights': None,
    'publisher': None,
    'relation': None,
    'identifier': None,
    'dc_subject': ';',
    'length': None
}

def extract_page_elements(soup):
    page_elements = {}
    # Get text content for all elements
    for element_id, split_char in all_elements.items():
        element = soup.find(attrs={'id': element_id})
        if element:
            text = element.find('p').text if element.find('p') else element.text
            if split_char:
                page_elements[element_id] = [item.strip() for item in text.split(split_char) if item.strip()]
            else:
                page_elements[element_id] = text.strip()
    return page_elements

def extract_download_link(soup):
    element = soup.find('div', class_='aside download-button')
    if element:
        link = element.find('a', id='pdf')
        if link:
            return link['href']
    return None

def scrape_openworks_page(url):
    driver.get(url)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    result = {'url': url, 'article-downloads': '0', 'status': '200'}
    if soup.find('div', id='404-error'):
        result['status'] = '404'
        return result

    result.update(extract_page_elements(soup))
    result['article-downloads'] = int(result['article-downloads'].replace(',', '') or '0')
    result['downloads'] = result['article-downloads']
    del result['article-downloads']
    result['downloadLink'] = extract_download_link(soup)
    return result

# Example usage
if __name__ == "__main__":
    url = 'https://openworks.wooster.edu/independentstudy/1/'
    data = scrape_openworks_page(url)
    print(data)
    driver.quit()
