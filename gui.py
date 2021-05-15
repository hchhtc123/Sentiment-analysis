from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
import paddlehub as hub
import interface
from functools import partial
import sys
import xlrd
import csv

# 单条新闻文本分类
def Single_classification(ui):
    content = ui.textEdit.toPlainText()  # 获取输入的新闻内容
    # 新闻正文内容不能为空
    if content == '':
        # 清空显示
        ui.label_3.setVisible(False)
        ui.lineEdit.setVisible(False)
        # 提示补全新闻内容
        ui.warn1()
    else:
        # 创建空列表
        data = []
        list = []
        # 使用 append() 添加元素
        list.append(content)
        data.append(list)
        label = model.predict(data, max_seq_len=128, batch_size=1, use_gpu=False)
        # 显示输出预测结果
        ui.lineEdit.setText(label[0])
        ui.label_3.setVisible(True)
        ui.lineEdit.setVisible(True)

# 批量新闻文本分类
def Batch_classification(ui):
    excel_path = ui.lineEdit_2.text()
    output_path = ui.lineEdit_4.text()
    if excel_path == '':
        ui.warn2()  # 提示未选择excel新闻文件
    elif output_path == '':
        ui.warn3()  # 提示未选择分类结果文件输出路径
    else:
        ui.showloading()   # 显示加载中
        workbook = xlrd.open_workbook(excel_path)
        Data_sheet = workbook.sheets()[0]  # 通过索引获取
        rowNum = Data_sheet.nrows  # sheet行数
        colNum = Data_sheet.ncols  # sheet列数
        list = []
        for i in range(1, rowNum):
            rowlist = []
            for j in range(colNum):
                rowlist.append(Data_sheet.cell_value(i, j))
            list.append(rowlist)
        print(list)
        results = model.predict(list, max_seq_len=128, batch_size=1, use_gpu=False)
        print(results)
        # 保存结果文件
        # 1. 创建文件对象
        f = open(output_path, 'w', encoding='utf-8')
        # 2. 基于文件对象构建 csv写入对象
        csv_writer = csv.writer(f)
        # 3. 构建列表头
        csv_writer.writerow(["情感类别"])
        # 4. 写入csv文件内容
        for label in results:
            csv_writer.writerow([label])
        # for idx in enumerate(list):
        #     csv_writer.writerow([idx, results[idx]])
        # 5. 关闭文件
        f.close()
        # 取消显示加载中
        ui.cancelloading()
        # 提示分类完成
        ui.success()


if __name__ == '__main__':
    # 定义模型输出标签
    label_list = ['喜悦', '愤怒', '厌恶', '低落']
    label_map = {
        idx: label_text for idx, label_text in enumerate(label_list)
    }
    # 加载模型
    model = hub.Module(
        name='ernie',
        task='seq-cls',
        load_checkpoint='ckpt/best_model/model.pdparams',
        label_map=label_map
    )

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = interface.Ui_Form()
    ui.setupUi(MainWindow)
    MainWindow.show()
    # 为按钮绑定功能函数
    # 单条文本情感分类预测
    ui.pushButton.clicked.connect(partial(Single_classification, ui))
    # 批量导入文本并进行情感分类预测
    ui.pushButton_4.clicked.connect(partial(Batch_classification, ui))
    sys.exit(app.exec_())