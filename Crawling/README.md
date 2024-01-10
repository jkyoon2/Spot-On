# 무신사 코디맵 크롤링 코드

**멀티프로세싱 기능 추가하였습니다**

병주가 작성한 코드를 기반으로 모듈화하고 성능을 개선해 두었습니다. Argument parser를 추가해 두어서 GUI / headless / server에서 모두 실행할 수 있게 해두었으며, argument로 페이지 번호를 전달할 수 있습니다. Output data는 **JSON** 형태이며 코디맵과 해당 코디맵에 속한 아이템 정보까지 모두 포함하게 됩니다.

## Getting Started

## Usage

The script can be run from the command line with the following syntax:

```bash
python3 crawling.py --start_page 1 --end_page 5 --output_dir output --num_workers 4
```

### Prerequisites
- Python >= 3.9
- pip (Python package installer)
- Chrome browser (for Selenium web driver)
- Selenium, bs4 with chrome engine
- tqdm

### Installing

Install the necessary Python packages with the following command:

<pre>
pip install -r requirements.txt
</pre>

This command installs all the Python packages necessary to run this project, such as `beautifulsoup4`, `selenium`, `pandas`, `numpy`, `tqdm`, and `webdriver_manager`.

If you encounter an error related to the Python interpreter while installing the packages, try running the installation command as a Python module. This will ensure that the packages are installed in the correct environment. You can use either `python` or `python3` at the start of the command, depending on your Python setup:

<pre>
python -m pip install -r requirements.txt
</pre>

or

<pre>
python3 -m pip install -r requirements.txt
</pre>

### Project Structure
Here is the file structure of this project:

- `crawling.py`: The main script for the web crawler.
- `utils.py`: Contains helper functions to extract detailed information from each webpage.
- `README.md`: Documentation for this project.

The main script, `crawling.py`, can be run from the command line and accepts several command-line arguments.

## Running the Script

You can run the script using the following command:
<pre>
python crawling.py --start_page START_PAGE --end_page END_PAGE --mode MODE --save_path SAVE_PATH --log_path LOG_PATH --num_workers NUM_WORKERS
</pre>


Replace `START_PAGE`, `END_PAGE`, `MODE`, `SAVE_PATH`, `LOG_PATH` and `NUM_WORKERS` with the desired values. Here is the explanation of each argument:

- `--start_page`: (Default: 1) The starting page number to start crawling.
- `--end_page`: (Default: 2) The ending page number to stop crawling.
- `--mode`: (Default: 'display') The mode of operation. Available options are 'display', 'headless', and 'server'.
- `--save_path`: (Default: './outputs/') The path where the data will be saved.
- `--log_path`: (Default: './') The path where the log will be saved.
- `--debug` : Debugging purpose. If it is set, the program will only crawl the first 3 codimaps in each page for faster debugging.
- `--num_workers` : Number of worker processes for multiprocessing. Each page will be assigned to a single process. If set to 1, the script will run with a single process.


## Output

The output of this script is a series of JSON files, each corresponding to a page on the Musinsa codimap. Each JSON file contains information about each codimap on the page, including:

- Codimap title, view count, styling text, image URL, and styling date
- List of associated items, with details such as title, category, hashtags, and image URL


## Output Example

The output of the script is a series of JSON files, each corresponding to a page on the Musinsa codimap. Each JSON file contains a list of data, where each element represents a codimap with various information as shown below:

```json
{
    "title": "언제나 귀여워",
    "styling_date": "2021.08.20",
    "view_num": 3236,
    "styling_txt": "퍼프소매가 돋보이는 미디 원피스에 카디건을 더하고, 플랫 슈즈로 완성한 걸리시 룩",
    "image_url": "https://image.msscdn.net/images/codimap/detail/5782/detail_5782_1_500.jpg?202306120506",
    "item_urls": [
        "https://www.musinsa.com/app/goods/1484418/0"
    ],
    "hashtags": [
        "피크닉",
        "화사한",
        "체크",
    ],
    "style_tag": "걸리시",
    "item_list": [
        {
            "title": "Im Happy Pearl Choker",
            "big_category": "주얼리",
            "small_category": "목걸이/펜던트",
            "item_hashtags": [
                "진주"
            ],
            "image_url": "https://image.msscdn.net/images/goods_img/20200614/1484418/1484418_1_500.jpg"
        }
    ]
}
