#/bin/bash

pip install lxml
# Set start and end page
START_PAGE=1
END_PAGE=10
SLEEP_TIME=2
MODE=display
# USE_PROXY=""
# PROXY_PATH=""

# USE_PROXY="--use_proxy"
# PROXY_PATH="--proxy_path 27.107.27.9:80"

# python3 crawling.py --start_page $START_PAGE --end_page $END_PAGE --mode $MODE
python3 crawling.py --start_page $START_PAGE --end_page $END_PAGE \
--mode $MODE --sleep_time $SLEEP_TIME $USE_PROXY $PROXY_PATH
