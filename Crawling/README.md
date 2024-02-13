# Mushinsa Crawling code

**Fixed the Vessl environment issue (02/13)**

## Getting Started
### Prerequisites
This code is tested in the Vessl environment, and you can install the required packages by running the following command:

```sh
./setup.sh
```

**Note**: You DO NOT need to manually install the chromedriver. Latest Selenium package will automatically download the compatible chromedriver for you.


# How to run the code
## 1. If you want to manally pass the arguments
```python
python crawling.py --start_page 1 --end_page 5 --mode server
```

## 2. If you want to run the code using the bash script
```sh
# After modifying the arguments (e.g., start_page, end_page, mode, etc.) in the run.sh file,
./run.sh
```

## 3. Recommended command for running the file (running free from any interruption)
```sh
# After modifying the arguments,
mkdir logs
nohup ./run.sh > logs/crawling.log 2>&1 &
```
**This will run the code in the background (even if you close the terminal) and save the logs in the logs/crawling.log file.**

## 4. If you want to stop the code
```sh
ps -ef | grep crawling.py
kill -9 <PID>
```
