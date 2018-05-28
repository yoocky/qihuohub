# qihuohub-quotation
Provide real time quotation service for stock and Futures
***
## Requirement
* python3.5+

## Package management

	sudo apt-get install python3-pip
    
## Install dependency

	pip3 install -r requirements.txt

## Install server container

	pip3 install uwsgi

## Deploy

	uwsgi --http 0.0.0.0:5000 --wsgi-file app.py --callable app --processes 4 --threads 2 --stats 127.0.0.1:9191

	

