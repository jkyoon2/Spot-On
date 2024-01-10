import logging
import re

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Crawl all hashtags in the page
def get_hashtags(soup):
    # div class="ui-tag-list"
    hashtags = soup.find('div', {'class': 'ui-tag-list'})
    if hashtags:
        hashtags = hashtags.find_all('a')
        hashtags = [hashtag.get_text().strip() for hashtag in hashtags]

        # Remove # from the beginning of each hashtag
        hashtags = [hashtag[1:] for hashtag in hashtags]
    
    else:
        hashtags = []
    
    return hashtags

# Crawl the item info in the page
def get_item_info(soup):
    big_category = None
    small_category = None
    item_hashtags = []
    image_url = None
    title = soup.find('span', attrs={'class':'product_title'}).find('em').get_text().strip()
    item_category = soup.find('p', attrs={'class':'item_categories'})
    if item_category:
        big_category = item_category.find_all('a')[0].get_text().strip()
        try:
            small_category = item_category.find_all('a')[1].get_text().strip()
        except:
            small_category = "none"
    else:
        logging.info(f"Error occured while crawling item_category")

    item_hashtags = soup.find_all('a', attrs={'class':'listItem'})
    if item_hashtags:
        item_hashtags = [item_hashtag.get_text().strip() for item_hashtag in item_hashtags]

        # Remove # from the beginning of each hashtag
        item_hashtags = [item_hashtag[1:] for item_hashtag in item_hashtags]

    else:
        item_hashtags = []
    
    # Get the image url
    item_imgurl = soup.find('img', attrs={'class':'plus_cursor'})
    if item_imgurl:
        image_url = item_imgurl['src']
        if image_url.startswith('//'):
            image_url = 'https:' + image_url
    else:
        logging.info(f"Error occured while crawling item image_url")

    result_dict = {
        'title': title,
        'big_category': big_category,
        'small_category': small_category,
        'item_hashtags': item_hashtags,
        'image_url': image_url
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