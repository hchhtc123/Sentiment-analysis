import paddlehub as hub
import interface
import sys
import xlrd
import csv
import re
import pandas as pd
import numpy as np
from functools import partial
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from time import time

# 单条文本情感分类
def Single_classification(ui):
    content = ui.textEdit.toPlainText()  # 获取输入的要进行情感分类的文本
    # 要进行情感分类的文本内容不能为空
    if content == '':
        ui.label_3.setVisible(False)     # 隐藏结果
        ui.lineEdit_5.setVisible(False)
        ui.warn1()   # 提示补全文本内容
    else:
        # 格式处理：
        data = []
        list = []
        list.append(content)
        data.append(list)
        t1 = time()
        # 对单条文本进行预测
        label = model.predict(data, max_seq_len=128, batch_size=16, use_gpu=False)  # 若下载了GPU的paddle，可以将此处use_gpu设置为True
        t2 = time()
        # 单条预测时间检测
        print('单条文本分类CPU环境下预测耗时（毫秒）：%.3f' % ((t2 - t1) * 1000.0))
        ui.lineEdit_5.setText(label[0])   # 完成预测后在界面显示预测的情感类别
        ui.label_3.setVisible(True)
        ui.lineEdit_5.setVisible(True)

# 批量文本情感分类
def Batch_classification(ui):
    excel_path = ui.lineEdit_2.text()   # 获取输入文件路径
    output_path = ui.lineEdit_4.text()  # 获取输出文件路径
    # 路径不能为空
    if excel_path == '':
        ui.warn2()  # 提示未选择要进行批量情感分类的excel文件
    elif output_path == '':
        ui.warn3()  # 提示未选择生成结果文件输出路径
    else:
        # ui.showloading()   # 显示加载中
        # 读取导入的excel文件
        df = pd.read_excel(excel_path)
        # 格式处理：
        news = pd.DataFrame(columns=['content'])
        news['content'] = df["content"]
        # 首先将pandas读取的数据转化为array
        data_array = np.array(news)
        # 然后转化为list形式
        data_list =data_array.tolist()

        # 批量文本预测
        results = model.predict(data_list, max_seq_len=128, batch_size=16, use_gpu=False) # 若下载了GPU的paddle，可以将此处use_gpu设置为True

        df['label'] = results # 将结果填充到label列上
        # 保存结果文件为excel文件
        df.to_excel(output_path, sheet_name='预测结果', index=False, header=True)
        # ui.cancelloading() # 完成预测后取消显示加载中
        ui.success()  # 提示分类完成

if __name__ == '__main__':

    # 定义要进行情感分类的7个类别
    label_list=['难过', '愉快', '喜欢', '愤怒', '害怕', '惊讶', '厌恶']
    label_map = { 
        idx: label_text for idx, label_text in enumerate(label_list)
    }

    # 加载训练好的模型
    model = hub.Module(
        name='ernie_tiny',
        version='2.0.2',  # 与训练时统一好，若未指定版本将自动下载最新的版本
        task='seq-cls',
        num_classes=7,
        load_checkpoint='../Ernie-model/model.pdparams',   # 注意模型参数一定要加载对！
        label_map=label_map
    )

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = interface.Ui_Form()
    ui.setupUi(MainWindow)
    MainWindow.show()
    
    # 为按钮绑定相关功能函数完成功能添加：
    # 单条文本情感分类
    ui.pushButton.clicked.connect(partial(Single_classification, ui))
    # 批量文本情感分类
    ui.pushButton_4.clicked.connect(partial(Batch_classification, ui))

    sys.exit(app.exec_())