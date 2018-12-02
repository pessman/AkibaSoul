# AkibaSoul
Various python scripts to interact with myfigurecollection for AkibaSoul

## Setup
### Python
> requires python 3.6.x

### Virtual Environment
> python(3) -m venv venv
> source venv/bin/activate (linux)
> pip install -r requirements.txt

### Add constants file to Scripts folder with following variables
> ITEM_DB_MYSQL_USER = '<user>'
> ITEM_DB_MYSQL_PASSWORD = '<password>'
> ITEM_DB_URL = 'http://myfigurecollection.net/api_v2.php?type=json&access=read&object=items&request=search&keywords='