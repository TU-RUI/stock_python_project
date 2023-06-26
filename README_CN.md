## 关于[English](./README.md)
一个简单的python项目，使用openapi进行数据抓取和转换，存储到数据库中，再提供数据查询和分析的api接口。


## 技术栈
[Python](https://www.python.org/) - 项目主要开发语言是Python。
[Flask](https://flask.palletsprojects.com/en/2.3.x/) - 提供Web服务框架.
[Flask-SQL](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/) - Flask的扩展插件，用于支持SQLAlchemy框架，帮助维护Python对象和数据库记录之间的映射关系。
[MySQL](https://dev.mysql.com/) - 常见的数据库服务器


## 如何运行
### 准备APIKEY
项目使用[AlphaVantage](https://www.alphavantage.co/documentation/)服务提供的免费api来查询股票数据，因此需要先在此页面申请你的APIKEY

### 准备MySQL服务器
项目使用MySQL服务存储股票数据，如果没有mysql服务器，需要下载安装，安装MySQL见：[MySQL安装教程](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/)，如您已有MySQL服务，准备好MySQL服务器的ip，port，username，password，dbname

### 配置环境变量
项目运行需要在服务器上配置APIKEY和MySQL的环境变量 
```
    export DB_HOST_PORT = '数据库ip和端口号, 例如192.168.3.14:3306'
    export DB_NAME = '数据库名'
    export DB_USER = '数据库用户名'
    export DB_PASSWORD = '数据库用户密码'
    export API_KEY = '第一步申请的APIKEY'
```

### 抓取数据 
```
python get_raw_data.py
```

### 启动api服务 
#### 本地启动 
启动时可以使用ENV变量指定服务启动的环境配置 
```
ENV=dev python financial/app.py
```

#### Docker启动
在docker-compose.yml文件中修改ENV变量 
```
docker-compose up --build
```


## 如何保管密钥
原则上，禁止在代码仓库中以任何形式存储密钥，因此本项目中使用的数据库密钥和Alpha Vantage的APIKEY需要在程序启动前以环境变量的形式配置。在行业内更为常见的做法是公司维护一个KMS密钥管理系统，所有的密钥均通过和KMS密钥管理系统交互得到
