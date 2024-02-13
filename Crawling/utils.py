import logging
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Get an instance of a logger
logger = logging.getLogger(__name__)

# Crawl all hashtags in the page
def get_hashtags(soup):
    item_hashtags = soup.find('div', {'class': 'product-detail__sc-uwu3zm-0 gWytWE'})
    if item_hashtags:
        item_hashtags = item_hashtags.find_all('a')
        item_hashtags = [item_hashtag.get_text().strip() for item_hashtag in item_hashtags]

        # Remove # from the beginning of each hashtag
        item_hashtags = [item_hashtag[1:] for item_hashtag in item_hashtags]
    else:
        item_hashtags = []
    
    return item_hashtags

# Crawl the item info in the page
def get_item_info(driver, soup):
    
    big_category = None
    small_category = None
    item_hashtags = None
    image_url = None
     
    title = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[1]/div[1]/div[1]/div[3]/div[2]/h3').text
    # title = soup.find('div', attrs={'class':'product-detail__sc-1klhlce-1 hMdBOW'}).find('h3').get_text().strip()
    item_category = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[1]/div[1]/div[1]/div[1]').text
    # item_category = soup.find('div', attrs={'class':'product-detail__sc-up77yl-0 htaeEr'})
    if item_category:
        item_category = item_category.replace('\n', '').split(' > ')
        big_category = item_category[0].strip()
        big_category = re.sub(r'\s*\([^)]*\)', '', big_category) 
        try:
            small_category = item_category[1].strip()
            small_category = re.sub(r'\s*\([^)]*\)', '', small_category) 
        except:
            small_category = "none"
    else:
        logging.info(f"Error occured while crawling item_category")

    # Get the hashtags from the page        
    item_hashtags = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]').text
    # product-detail__sc-uwu3zm-0 gWytWE
    # product-detail__sc-uwu3zm-0 gWytWE
    # /html/body/div[3]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div
    # driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div')
    # /html/body/div[3]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div
    # /html/body/div[3]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div/a[1]
    
    if item_hashtags:
        hashtags = item_hashtags.split('\n')
        # item_hashtags = item_hashtags.find_all('a')
        item_hashtags = [item[1:].strip() for item in hashtags]
        # item_hashtags = [item_hashtag.get_text().strip() for item_hashtag in item_hashtags]

        # Remove # from the beginning of each hashtag
        # item_hashtags = [item_hashtag[1:] for item_hashtag in item_hashtags]
    else:
        item_hashtags = []
    
    # Get the image url
    item_imgurl = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div')
    
    if item_imgurl:
        img_element = item_imgurl.find_element(By.TAG_NAME, 'img')
        image_url = img_element.get_attribute('src')
        # img_tag = item_imgurl.find('img')
        # image_url = img_tag['src']
        
        if image_url.startswith('//'):
            image_url = 'https:' + image_url
    else:
        logging.info(f"Error occured while crawling item image_url")

    result_dict = {
        'title': title,
        'big_category': big_category,
        'small_category': small_category,
        'item_hashtags': item_hashtags,
        'image_url': image_url,
    }

    return result_dict
    
# Crawl all urls in the page
def get_item_urls(soup):
    items = soup.find_all('div', attrs={'class':re.compile('^swiper-slide.style_contents_size')})
    logging.info(f"# of items in the page: {len(items)}")
    item_urls = []
    for item in items:
        item_url = item.find('a', {'class': 'styling_img'})['href']
        if item_url.startswith('/app/'):
            item_url = 'https://www.musinsa.com' + item_url
        item_urls.append(item_url)
    
    return item_urls

def remove_popup(driver, soup):
    popup = soup.find('div', {'class': 'n-layer-notice'})
    if popup:
        logging.info(f"\t\tPopup box exist")

        # Wait for the button to be clickable
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "btn-today"))
            )
            # Click the button
            button.click()           
        except:
            logging.info(f"\t\t\tError occured while closing notice box")
        return
    else:
        return

# Take BeautifulSoup object and crawl the detail page
def get_detail_info(soup):
    # Get the title, date, and view count from the soup
    title = soup.find('div', {'id': 'style_info'}).find('h2').get_text().strip()
    styling_date = soup.find('p', {'class': 'styling_date'}).get_text(strip=True).split('|')[0].strip()
    view_num = soup.find('span', {'id': 'view_num'}).get_text(strip=True)[3:]
    view_num = int(view_num.replace(',', ''))

    # styling_txt not always exists
    styling_txt = soup.find('p', attrs={'class':'styling_txt'})
    if styling_txt:
        styling_txt = styling_txt.get_text().strip().replace('\r', ' ')
    else:
        logging.info(f"Error occured while crawling codimap_explain")

    # Get the image url from the soup
    image_url = soup.find('img', attrs={'class':'photo'})
    if image_url:
        image_url = image_url['src']
        if image_url.startswith('//'):
            image_url = 'https:' + image_url
    else:
        logging.info(f"Error occured while crawling codimap_imgurl")

    # Get the item urls from the soup
    item_urls = get_item_urls(soup)
    
    # Get hashtags from the page
    hashtags = get_hashtags(soup)
    
    result_dict = {
        'title': title,
        'styling_date': styling_date,
        'view_num': view_num,
        'styling_txt': styling_txt,
        'image_url': image_url,
        'item_urls': item_urls,
        'hashtags': hashtags
    }

    return result_dict
