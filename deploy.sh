uwsgi --http 0.0.0.0:5000 --wsgi-file app.py --callable app --processes 4 --threads 2 --stats 127.0.0.1:9191
