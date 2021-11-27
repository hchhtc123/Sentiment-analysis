#-*- coding:utf-8 -*-
# __init__.py 有两个作用：一是包含应用工厂；二 是告诉 Python flaskr 文件夹应当视作为一个包。

# 启动步骤：首先移动到文件夹flaskr所在目录
# set FLASK_APP=flaskr
# set FLASK_ENV=development   # 设置生产或开发环境
# flask run

# 注意导入项目所需使用的包名
import os
from flask import Flask
from flask import request, jsonify, make_response
from flask_cors import CORS
import json
import paddlehub as hub


def process(content):
    # 对文本格式的处理：
    data = []
    list = []
    list.append(content)
    data.append(list)
    return data

# 工厂模式创建flask的app
def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, supports_credentials=True)

    # 加载模型参数
    # 定义要进行情感分类的7个类别
    label_list=['难过', '愉快', '喜欢', '愤怒', '害怕', '惊讶', '厌恶']
    label_map = { 
        idx: label_text for idx, label_text in enumerate(label_list)
    }

    # 加载训练好的模型
    model = hub.Module(
        name='ernie_tiny',
        task='seq-cls',
        num_classes=7,
        load_checkpoint='../../Ernie-model/model.pdparams',  # 加载训练好的模型参数
        label_map=label_map
    )
    print('Model load success!')

    # 解决跨域问题：
    # r'/*' 是通配符，让本服务器所有的URL 都允许跨域请求
    CORS(app, resources=r'/*')
    @app.after_request
    def af_request(resp):     
        """
        #请求钩子，在所有的请求发生后执行，加入headers。
        :param resp:
        :return:
        """
        resp = make_response(resp)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
        return resp

    # 主页返回页面数据测试
    @app.route('/')
    def hello():
        return 'Hello, World!'
    
    # 定义服务接口API
    @app.route('/emoAnalysis', methods=["GET","POST"])
    def emotion_analyse():
        if request.method == 'GET':
            # 获取get方法传的param参数'text'数据
            text =  request.args.get('text','')
            if text=='':
                response = make_response(json.dumps(dict(success=False, message="text文本内容为空！"), ensure_ascii=False))
                return response
            else:
                try:
                    data = process(text)
                    label = model.predict(data, max_seq_len=128, batch_size=1, use_gpu=False)
                    # 若下载了GPU版本的paddle，可以将此处use_gpu设置为True
                    review = {
                        'success': True,
                        'text': text,
                        'label':label[0],
                    }
                    response = make_response(json.dumps(review, ensure_ascii=False))
                    return response
                except Exception as e:
                    print(e)  # 打印发生的异常到控制台
                    response = make_response(json.dumps(dict(success=False, message="请求失败！", error=e), ensure_ascii=False))
                    return response
  
        elif request.method == 'POST':
            # 获取post方法传的body字段'text'数据
            if request.json is None:
                response = make_response(json.dumps(dict(success=False, message="发送数据格式需要json格式！"), ensure_ascii=False))
                return response
            else:
                print(request.json)
                text = request.json.get('text')
                if text is None:
                    response = make_response(json.dumps(dict(success=False, message="text文本内容为空！"), ensure_ascii=False))
                    return response
                else:
                    try:
                        data = process(text)
                        label = model.predict(data, max_seq_len=128, batch_size=1, use_gpu=False)
                        review = {
                            'success': True,
                            'text': text,
                            'label':label[0],
                        }
                        response = make_response(json.dumps(review, ensure_ascii=False))
                        return response
                    except Exception as e:
                        print(e) # 打印发生的异常到控制台
                        response = make_response(json.dumps(dict(success=False, message="请求失败！",  error=e), ensure_ascii=False))
                        return response
            
    return app
    