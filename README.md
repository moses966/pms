**Added python-decouple**  
*Installation:*  
`pip install python-decouple`  
1. Create a .env file in the root directory  of your project (Should be at the same level as your manage.py file)
2. Store your important data in this file e.g:
3. `DEBUG=False`  
   `SECRET_KEY='my_secret_key'`
4. Next, import the decouple library into settings.py file:
5. `from decouple import config`
6. Now, we can get our parameters:
7. `DEBUG = config('DEBUG', cast=bool)SECRET_KEY = config('SECRET_KEY')`
