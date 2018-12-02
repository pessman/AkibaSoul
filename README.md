# AkibaSoul
Various python scripts to interact with myfigurecollection for AkibaSoul

## Setup
### Python
> requires python 3.6.x

### Virtual Environment
1. python(3) -m venv venv
2. source venv/bin/activate (linux)
3. pip install -r requirements.txt

### Add constants file to Scripts folder with following variables
1. ITEM_DB_MYSQL_USER = 'user_name'
2. ITEM_DB_MYSQL_PASSWORD = 'password'
3. ITEM_DB_URL = 'http://myfigurecollection.net/api_v2.php?type=json&access=read&object=items&request=search&keywords='