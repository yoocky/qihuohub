### 按装pip3

	sudo apt-get install python3-pip
    
### 安装依赖

	pip3 install -r requirements.txt

### 安装uwsgi

	pip3 install uwsgi

### 启动app

	uwsgi --http 0.0.0.0:5000 --wsgi-file app.py --callable app --processes 4 --threads 2 --stats 127.0.0.1:9191

	

