import os, logging, argparse
import multiprocessing
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm

import pandas as pd
import numpy as np
import time, json, re
from utils import get_detail_info, get_item_info

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--start_page', type=int, default=1, help='Start page number')
parser.add_argument('--end_page', type=int, default=2, help='End page number')
parser.add_argument('--mode', type=str, default='headless', help='Mode of crawling (display, headless, server)')
parser.add_argument('--save_path', type=str, default='./outputs/', help='Path to save the data')
parser.add_argument('--log_path', type=str, default='./', help='Path to save the log')
parser.add_argument('--num_workers', type=int, default=1, help='Number of workers')
parser.add_argument('--debug', action='store_true', help='Debugging purpose')
parser.add_argument('--use_proxy', action='store_true', help='Use proxy')
parser.add_argument('--sleep_time', type=int, default=2, help='Sleep time for each page')
parser.add_argument('--proxy_path', type=str, default='117.1.16.131:8080', help='Proxy IP and port number')
parser.add_argument('--continue', action='store_true', help='Crawl missing pages')

args = parser.parse_args()

# Set options for chrome driver
options = webdriver.ChromeOptions()
options.add_argument('--disable-dev-shm-usage') # To prevent memory leak
options.add_argument("--disable-notifications") # To prevent notification
options.add_experimental_option('excludeSwitches', ['disable-popup-blocking']) # To prevent popup blocking

# Set mode of chrome driver
if args.mode == 'display':
    pass
elif args.mode == 'headless':
    options.add_argument("--headless")
elif args.mode == 'server':
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
else:
    logging.info("Invalid mode. Please check the mode again. (display, headless, server))")
    exit()

# Set proxy for chrome driver
if args.use_proxy:
    options.add_argument(f"--proxy-server={args.proxy_path}")

# Logging setting
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Print log message to console
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# Print log message to file
if not os.path.exists(args.log_path):
    os.makedirs(args.log_path)
file_handler = logging.FileHandler(os.path.join(args.log_path, f"codimap_crawling_{args.start_page}_{args.end_page}.log"))
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Crawl all codimaps in the page_num page
def crawl(page_num, save_path='./', **kwargs):
    """
        Crawl all codimaps in the page_num page.
        :param page_num: page number

        :return: codimap_list
    """
    # Set driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(3)

    codimap_list = []
    url = f"https://www.musinsa.com/app/codimap/lists?style_type=&tag_no=&brand=&display_cnt=60&list_kind=big&sort=comment_cnt&page={page_num}"
    driver.get(url)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'address')))

    soup = BeautifulSoup(driver.page_source, 'lxml')
    data_rows = soup.find_all('li', attrs={'class':'style-list-item'})  # Get all codimaps in the page

    # Get informations from each codimap
    if args.debug:
        data_rows = data_rows[:3]

    for i in tqdm(range(len(data_rows)), desc=f"Page {page_num}"):
        driver.get(url)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'address')))

        logging.info(f"#{i+1} codimap crawling started")

        # First get the style tag of the codimap (This dissapears when you click the codimap)
        style_tag = data_rows[i].find('span', attrs={'class':'style-list-information__text'})
        codi_element_xpath = driver.find_element(By.XPATH, f"/html/body/div[3]/div[3]/form/div[4]/div/ul/li[{i+1}]/div[1]/a/div/img")
        codi_element_xpath.click() # Click the codi map and go to the detail page.

        # Wait until the page is loaded
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'styling_txt')))

        # Get the codimap information
        soup = BeautifulSoup(driver.page_source, 'lxml')
        detail_info = get_detail_info(soup)
        detail_info['style_tag'] = style_tag.text
        
        # Get items from codi map
        item_list = []
        
        for item_url in detail_info['item_urls']:
            time.sleep(args.sleep_time)
            driver.get(item_url)
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "plus_cursor"))
            )

            soup = BeautifulSoup(driver.page_source, 'lxml')
        
            item_info = get_item_info(soup)
            item_list.append(item_info)
        
        # Add codimap information to codimap_list
        detail_info['item_list'] = item_list
        codimap_list.append(detail_info)

        logger.info(f"Page {page_num}, #{i+1} codimap crawling finished")

        # Show detail info if num_workers is 1
        if args.num_workers == 1:
            logger.info(f"Detail info: {detail_info}")

    # Save the data in json format
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    with open(os.path.join(save_path, f"codimap_list_{page_num}.json"), 'w', encoding='utf-8') as json_file:
        json.dump(codimap_list, json_file, ensure_ascii=False, indent=4)

    driver.close()
    return codimap_list

def safe_crawl(page, save_path, error_pages):
    # For error handling in multiprocessing
    try:
        crawl(page, save_path)
    except Exception as e:
        logger.error(f"{page} page crawling failed")
        logger.error(e)
        error_pages.append(page)


# main function
if __name__ == "__main__":
    # Show the arguments
    logger.info(f"Start page: {args.start_page}")
    logger.info(f"End page: {args.end_page}")
    logger.info(f"Mode: {args.mode}")
    logger.info(f"Save path: {args.save_path}")
    logger.info(f"Log path: {args.log_path}")
    logger.info(f"Debug mode: {args.debug}")
    logger.info(f"Number of workers: {args.num_workers}")

    # List containing error pages - for multiprocessing (shared memory)
    error_pages_single = []
    manager = multiprocessing.Manager()
    error_pages = manager.list()

    # Multiprocessing feature for 4 processes
    page_list = []
    for i in range(args.start_page, args.end_page+1, args.num_workers):
        page_list.append((i, min(i+args.num_workers-1, args.end_page)))
    
    if args.num_workers > 1:
        # Multiprocessing
        for pages in page_list:
            logger.info(f"{pages[0]}-{pages[1]} page crawling started")
            logger.info(f"Each page will be assigned to a single process")

            # Assign each page to a process
            processes = []
            for page in range(pages[0], pages[1]+1):
                logger.info(f"Process for {page} page started")
                p = multiprocessing.Process(target=safe_crawl, args=(page, args.save_path, error_pages))
                p.start()
                processes.append(p)
            
            for p in processes:
                p.join()
            
            logger.info(f"{pages[0]}-{pages[1]} page crawling finished")
    else:
        # Single process
        # First get all file names in the save path
        file_names = os.listdir(args.save_path)
        file_names = [int(file_name.split('_')[-1].split('.')[0]) for file_name in file_names]
        
        # Get pages that are not crawled yet
        page_list = [page for page in range(args.start_page, args.end_page+1) if page not in file_names]

        # Show pages that are not crawled yet
        logger.info(f"Pages that are not crawled yet: {page_list}")

        for page in page_list:
            logger.info(f"{page} page crawling started")
            try:
                crawl(page, args.save_path)
            except Exception as e:
                logger.error(f"{page} page crawling failed")
                logger.error(e)
                error_pages_single.append(page)
                
            logger.info(f"{page} page crawling finished")
    
    # Print error pages
    logger.info(f"Error pages: {error_pages}")
