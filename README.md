# NetworkProject

### Run
<code>
pip3 install -r requirements.txt
</code>
<br>
<code>
docker-compose up mongo
</code>
<br>
<code>
uwsgi --wsgi-file main.py --callable app --http 127.0.0.1:5000
</code>
