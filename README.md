# This is the main website for tldtest.net

This site has the purpose of testing the response time of TLD nameservers everywhere in the world.

# To run in test environment :
```
virtualenv -p python3.11 venv
source venv/bin/activate
pip install -r requirements.txt
./manage.py migrate
./manage.py runserver
```