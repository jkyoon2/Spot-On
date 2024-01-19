#/bin/bash

# Set start and end page
START_PAGE=358
END_PAGE=389
SLEEP_TIME=2
MODE=headless
USE_PROXY=""
PROXY_PATH=""

# USE_PROXY="--use_proxy"
# PROXY_PATH="--proxy_path 27.107.27.9:80"


python3 crawling.py --start_page $START_PAGE --end_page $END_PAGE \
--mode $MODE --num_workers 1 --sleep_time $SLEEP_TIME $USE_PROXY $PROXY_PATH
