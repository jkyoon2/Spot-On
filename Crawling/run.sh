#/bin/bash

# install pip library
pip install lxml

# Set start and end page
START_PAGE=358
END_PAGE=389
SLEEP_TIME=2
MODE=server

# USE_PROXY="--use_proxy"
# PROXY_PATH="--proxy_path 27.107.27.9:80"


python crawling.py --start_page $START_PAGE --end_page $END_PAGE --mode $MODE