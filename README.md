## About
[中文](./README_CN.md)|[English](./README.md)   
A simple python project that uses open api to crawl and transform data, store it in a database, and then provide an api interface for data query and analysis.

## Tech Stack
[Python](https://www.python.org/) - main programming language is Python.  
[Flask](https://flask.palletsprojects.com/en/2.3.x/) - provides web framework.  
[Flask-SQL](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/) - an extension for Flask that adds support for SQLAlchemy, help binding database records to object. 
[MySQL](https://dev.mysql.com/) - popular database server. 


## How To Run
### Prepare APIKEY 
this project use the free api provided by [AlphaVantage](https://www.alphavantage.co/documentation/) to query time series stock data, so you need to apply for your APIKEY on this page first.


### Preparing the MySQL Server 
The project uses MySQL service to store stock data, if you don't have mysql server, you need to download and install it，see：[MySQL installation](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/)， if you have MySQL service, prepare the `ip，port，username，password，dbname` of MySQL server.

### Configure environment variables 
Project runs need to configure APIKEY and MySQL environment variables on the server
```
    export DB_HOST_PORT = 'database ip and port, eg. 192.168.3.14:3306' 
    export DB_NAME = 'database name' 
    export DB_USER = 'database username' 
    export DB_PASSWORD = 'database user password' 
    export API_KEY = 'APIKEY applied in the first step' 
```

### Crawl data 
```
python get_raw_data.py
```


### Run Web Server 
#### Run In Local 
The ENV variable can be used at startup to specify the environment configuration for service startup
```
ENV=dev python financial/app.py
```

#### Run In Docker 
Change the ENV variable in the docker-compose.yml file
```
docker-compose up --build
```


## How To Maintain The APIKEY 
In principle, it is forbidden to store keys in any form in the code repository, so the database keys used in this project and Alpha Vantage's APIKEY need to be configured in the environment variables before the program starts. A more common practice in the industry is for companies to maintain a KMS key management system, and all keys are obtained by interacting with the KMS key management system
