#/bin/bash

# Set start and end page
START_PAGE=1
END_PAGE=10
SLEEP_TIME=2
MODE=server

python crawling.py --start_page $START_PAGE --end_page $END_PAGE \
--mode $MODE --sleep_time $SLEEP_TIME

