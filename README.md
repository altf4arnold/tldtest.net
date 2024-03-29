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


# When running in debug False :
```
./manage.py collectstatic
./manage.py runserver --insecure
```

# Static files :
The static files need to be hosted outside the gunicorn. So I choose to store them on github pages (for now). Which means that every time the statics get changed, one need to run :
```
./manage.py collectstatic
git add staticfiles/.
```

# CSS : 
To install the CSS bundler : 
```
npm install -D tailwindcss
npx tailwindcss init
```

To update CSS files (they use the tailwinds framework)
```
npx tailwindcss -i ./static/src/input.css -o ./static/src/output.css
```
