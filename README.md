# 缺陷产品识别系统 IPRS(Injury Products Recognize System)

powered by Django


## Setup

#### Download Dependencies

```shell script
pip install -r requirements.txt
```

#### Startup
*You can directly start the service by clicking run button in you Pycharm*

Or use Django startup command:
```shell script
cd ./src/service
python manage.py runserver
```

### Overview

这个项目是整个IPRS的数据分析部分，他以Django Service的形式对外暴露一个接口([here](./src/service/iprs/urls.py))

这个接口接受一个post请求，请求中带着一个csv文件，文件是从裁判文书网爬取的数据

他将接收到的数据进行分析，并且识别出其中的伤害事件和伤害产品，将分析结果通过HTTP POST请求的形式传给后端进行存储和展示

数据分析分为两部分：

1. 伤害事件识别:
    1. 使用训练好的CNN网络进行识别([here](./src/doc_classification/__init__.py))
    2. 网络保存在[这里](./src/doc_classification/court/data)
    3. 输入文书的是上面提到的csv文件
2. 伤害产品识别:
    1. 使用正则匹配的方式进行识别
    2. 输入是1中被判定为伤害事件的文书
    
上面两步进行完之后，会向存储后台发送存储请求([here](./src/request/__init__.py))，将数据存进数据库，以供展示
