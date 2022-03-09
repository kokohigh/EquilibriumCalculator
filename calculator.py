import sys
import math
from PyQt5.QtWidgets import QApplication
from PyQt5 import uic
import numpy as np
from PyQt5.QtGui import QIcon
from sympy import *

class Calculator():

    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = uic.loadUi('equilibrium0.ui')
        self.ui.comboBox_3.currentIndexChanged.connect(self.combo_set)
        self.ui.comboBox_4.currentIndexChanged.connect(self.combo_set)
        self.ui.button.clicked.connect(self.handleCalc)


    def combo_set(self):
        country1 = self.ui.comboBox_3.currentText()
        country2 = self.ui.comboBox_4.currentText()
        return country1,country2


    def handleCalc(self):
        game_dm1,game_dm2 = self.combo_set()
        #用于储存国家数据的字典
        countries = {
        # 发达国家
        'アメリカ':[20580250,62869,2568407,1645626],
        '日本' : [4971767,39304,720738,705528],
        'ドイツ' : [3951340,47662,1234222,1489158],
        'イギリス' : [2828833,42580,591801,468817],
        'シンガポール' : [364139,64579,359266,390763],
        'スイス' : [705546,83162,277001,313866],
        'スウェーデン' : [556073,54356,158690,160543],
        'フランス' : [2780152,42953,651179,569732],
        #发展中国家
        '中国' : [13368073,9580,2077097,2499029],
        'アラブ首長国連邦' : [414179,39709,261905,280136],
        'サウジアラビア' : [786522,23539,141891,268590],
        'インド' : [2718732,2038,483864,324163],
        'ロシア' : [1657290,11289,254052,418796],
        'ブラジル' : [1867818,8959,184104,222644],
        'インドネシア' : [1022454,3871,170727,167497],
        'エジプト' : [249559,2573,70919,28993],
        #欠发达国家
        'ルワンダ' : [9510,787,2703,1166],
        'ブータン' : [2582,3160,960,590],
        'ミャンマー' : [68668,1300,18000,17440],
        'ガンビア' : [1625,713,619,111],
        '中央アフリカ' : [2280,449,460,180],
        'ギニア' : [12099,910,3370,3337],
        'ザンビア' : [26720,1503,7221,7303],
        'ウガンダ' : [28116,724,7476,3455],
        }
        aver_gdp = 440049  # 平均GDP
        aver_per_gdp = 20000  # 发达国家标准
        max_gdp = 20580250-440049 #最高的GDP与平均GDP的差
        # max_per_gdp = 115536-20000 #最高的人均GDP与平均人均GDP的差
        max_per_gdp1 = 20000 - 307

        #正常的评分
        char_dol = [3, 4, -2, -2]
        char_SDR = [2, 3, -3, -3]
        char_lib = [1, 1, 3, 3]
        char_CBDC = [2, 2, 4, 2]
        char_bit = [4, -4, 2, 3]

        #swift变好的评分
        # char_dol = [3, 4, 4, 2 ,0]
        # char_SDR = [2, 3, 3, 1,1]
        # char_lib = [1, 1, 3, 3,2]
        # char_CBDC = [2, 2, 4, 2,3]
        # char_bit = [4, -4, 2, 3,4]

        #libra变坏的评分
        # char_dol = [3, 4, -2, -2,0]
        # char_SDR = [2, 3, -3, -3,1]
        # char_lib = [-2, -2, 3, 3,2]
        # char_CBDC = [2, 2, 4, 2,3]
        # char_bit = [4, -4, 2, 3,4]

        # #+1的评分
        # char_dol = [4, 5, -1, -1, 0]
        # char_SDR = [3, 4, -2, -2, 1]
        # char_lib = [2, 2, 4, 4, 2]
        # char_CBDC = [3, 3, 5, 3, 3]
        # char_bit = [5, -3, 3, 4, 4]

        #+5的评分
        # char_dol = [8, 9, 3, 3, 0]
        # char_SDR = [7, 8, 2, 2, 1]
        # char_lib = [6, 6, 8, 8, 2]
        # char_CBDC = [7, 7, 9, 7, 3]
        # char_bit = [9, 1, 7, 8, 4]

        # #-1的评分
        # char_dol = [2, 3, -3, -3, 0]
        # char_SDR = [1, 2, -4, -4, 1]
        # char_lib = [0, 0, 2, 2, 2]
        # char_CBDC = [1, 1, 3, 1, 3]
        # char_bit = [3, -5, 1, 2, 4]

        #-5的评分
        # char_dol = [-2, -1, -7, -7, 0]
        # char_SDR = [-3, -2, -8, -8, 1]
        # char_lib = [-4, -4, -2, -2, 2]
        # char_CBDC = [-3, -3, -1, -3, 3]
        # char_bit = [-1, -9, -3, -2, 4]

        # 5倍的评分
        # char_dol = [15, 20, -10, -10, 0]
        # char_SDR = [10, 15, -15, -15, 5]
        # char_lib = [5, 5, 15, 15, 10]
        # char_CBDC = [10, 10, 20, 10, 15]
        # char_bit = [20, -20, 10, 15, 20]

        # #2倍的评分
        # char_dol = [6, 8, -4, -4, 0]
        # char_SDR = [4, 6, -6, -6, 2]
        # char_lib = [2, 2, 6, 6, 4]
        # char_CBDC = [4, 4, 8, 4, 6]
        # char_bit = [8, -8, 4, 6, 8]
        #
        # #0.5倍的评分
        # char_dol = [1.5, 2, -1, -1, 0]
        # char_SDR = [1, 1.5, -1.5, -1.5, 0.5]
        # char_lib = [0.5, 0.5, 1.5, 1.5, 1]
        # char_CBDC = [1, 1, 2, 1, 1.5]
        # char_bit = [2, -2, 1, 1.5, 2]

        DM1 = np.around([[0.0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0], ],decimals=1)
        DM2 = np.around([[0.0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0], ],decimals=1)

        #标准值
        delta = np.array([[1, 0, 1, -1, -1],
                          [0, 1, 1, -1, -1],
                          [1, 1, 2, -1, -1],
                          [-1, -1, -1, 3, -2],
                          [-1, -1, -1, -2, 1], ])

        # +1的数值
        # delta = np.array([[2, 1, 2, 0, 0],
        #                   [1, 2, 2, 0, 0],
        #                   [2, 2, 3, 0, 0],
        #                   [0, 0, 0, 4, -1],
        #                   [0, 0, 0, -1, 2], ])

        # +5的数值
        # delta = np.array([[6, 5, 6, 4, 4],
        #                   [5, 6, 6, 4, 4],
        #                   [6, 6, 7, 4, 4],
        #                   [4, 4, 4, 8, 3],
        #                   [4, 4, 4, 3, 6], ])

        # -1的数值
        # delta = np.array([[0, -1, 0, -2, -2],
        #                   [-1, 0, 0, -2, -2],
        #                   [0, 0, 1, -2, -2],
        #                   [-2, -2, -2, 2, -3],
        #                   [-2, -2, -2, -3, 0], ])

        # -5的数值
        # delta = np.array([[-4, -5, -4, -6, -6],
        #                   [-5, -4, -4, -6, -6],
        #                   [-4, -4, -3, -6, -6],
        #                   [-6, -6, -6, -2, -7],
        #                   [-6, -6, -6, -7, -4], ])

        # 0.5倍的值
        # delta = np.array([[0.5, 0, 0.5, -0.5, -0.5],
        #                   [0, 0.5, 0.5, -0.5, -0.5],
        #                   [0.5, 0.5, 1, -0.5, -0.5],
        #                   [-0.5, -0.5, -0.5, 1.5, -1],
        #                   [-0.5, -0.5, -0.5, -1, 0.5], ])

        # 2倍的值
        # delta = np.array([[2, 0, 2, -2, -2],
        #                   [0, 2, 2, -2, -2],
        #                   [2, 2, 4, -2, -2],
        #                   [-2, -2, -2, 6, -2],
        #                   [-2, -2, -2, -4, 2], ])

        # 5倍的值
        # delta = np.array([[5, 0, 5, -5, -5],
        #                   [0, 5, 5, -5, -5],
        #                   [5, 5, 10, -5, -5],
        #                   [-5, -5, -5, 15, -10],
        #                   [-5, -5, -5, -10, 5], ])


        #DM1的利得表的计算函数
        def cal_it1(country1,country2,char,row):
            gdp_margin = (country1[0] - aver_gdp)/max_gdp
            k = math.exp(gdp_margin)


            # if self.country1[0] > aver_gdp:
            #     k =round ((self.country1[0] - aver_gdp) * 10 / max_gdp,1)
            # elif self.country1[0] == aver_gdp:
            #     k = 1
            # elif self.country1[0] < aver_gdp:
            #     k = round(1 / abs(self.country1[0] - aver_gdp),1)
            per_gdp_margin = (country1[1] - aver_per_gdp )*(-1)/max_per_gdp1
            p = math.exp(per_gdp_margin)

            # if self.country1[1] > aver_per_gdp:
            #     p = round(1 / (self.country1[1] - aver_per_gdp),1)
            # elif self.country1[1] == aver_per_gdp:
            #     p = 1
            # elif self.country1[1] < aver_per_gdp:
            #     p = round(abs(self.country1[1] - aver_per_gdp) * 10 / max_per_gdp,1)
            # right = round(5*(self.country2[2] + self.country2[3]) / (
            #             self.country1[2] + self.country1[3] + self.country2[2] + self.country2[3]),1)
            # right = round((self.country2[2] + self.country2[3]) / (
            #             self.country1[2] + self.country1[3] ),1)
            # result = round((k * (self.char[2] + self.char[3]) + p * (self.char[0] + self.char[1])) * right,1)
            right = round(5*(country2[2] + country2[3]) / (
                        country1[2] + country1[3] + country2[2] + country2[3]),1)
            result = round((k * (char[2] + char[3]) + p * (char[0] + char[1])) * right,1)

            #将DM1的利得表结果写入矩阵
            col = 0
            while col < 5:
                DM1[row][col] = result
                col = col + 1

        #DM2的利得表的计算函数
        def cal_it2(country1,country2,char,row):
            # self.country1 = country1
            # self.country2 = country2
            # self.char = char

            gdp_margin = (country1[0] - aver_gdp)/max_gdp
            m = math.exp(gdp_margin)
            # if self.country1[0] > aver_gdp:
            #     m =round ((self.country1[0] - aver_gdp) * 10 / max_gdp,1)
            # elif self.country1[0] == aver_gdp:
            #     m = 1
            # elif self.country1[0] < aver_gdp:
            #     m = round(1 / abs(self.country1[0] - aver_gdp),1)
            # print("m=" + str(m))

            per_gdp_margin = (country1[1] - aver_per_gdp)*(-1)/max_per_gdp1
            n = math.exp(per_gdp_margin)
            # if self.country1[1] > aver_per_gdp:
            #     n = round(1 / (self.country1[1] - aver_per_gdp),1)
            # elif self.country1[1] == aver_per_gdp:
            #     n = 1
            # elif self.country1[1] < aver_per_gdp:
            #     n = round(abs(self.country1[1] - aver_per_gdp) * 10 / max_per_gdp,1)
            # print("n=" + str(n))

            #方案1
            right = round(5*(country2[2] + country2[3]) / (
                        country1[2] + country1[3] + country2[2] + country2[3]),1)
            #方案2
            # right = round((self.country2[2] + self.country2[3]) / (
            #         self.country1[2] + self.country1[3] ), 1)
            result = round((m * (char[2] + char[3]) + n * (char[0] + char[1])) * right,1)

            #将DM2的利得表结果写入矩阵
            col = 0
            while col < 5:
                DM2[row][col] = result
                col = col + 1

        #打印利得表
        def print_benefit(dm1,dm2):

            cal_it1(dm1, dm2, char_dol, 0)
            cal_it1(dm1, dm2, char_SDR, 1)
            cal_it1(dm1, dm2, char_lib, 2)
            cal_it1(dm1, dm2, char_CBDC, 3)
            cal_it1(dm1, dm2, char_bit, 4)
            # 计算DM2的利得表
            cal_it2(dm2, dm1, char_dol, 0)
            cal_it2(dm2, dm1, char_SDR, 1)
            cal_it2(dm2, dm1, char_lib, 2)
            cal_it2(dm2, dm1, char_CBDC, 3)
            cal_it2(dm2, dm1, char_bit, 4)

            DM1_res = DM1 + delta
            DM2_res = DM2 + delta
            self.ui.textBrowser_1.clear()
            self.ui.textBrowser_1.append(" DM1=\n"+str(DM1_res)+"\n"+"DM2=\n"+str(DM2_res))
            # self.ui.textBrowser_1.append("利得表=\n"+"(" + str(DM1_res) + "\n" + str(DM2_res.T) + ")")
            # self.ui.textBrowser_1.append("利得表=\n" )
            # i,j = 0,0
            # while i < 5:
            #     np.set_printoptions(precision=3)   #小数点后三位的设置
            #     while j < 5:
            #         self.ui.textBrowser_1.append("("+str(DM1_res[i][j]) + "\n" + str(DM2_res.T[i][j])+")")
            #         if j == 4:
            #             self.ui.textBrowser_1.append("\n")
            #         j = j+1
            #     i = i+1

            return DM1_res,DM2_res

        #打印nash均衡
        def nash():
            self.ui.textBrowser_2.clear()
            self.ui.textBrowser_3.clear()
            list_nash = []

            DM1_res,DM2_res = print_benefit(dm1=countries[game_dm1],dm2=countries[game_dm2])
            DM2_res = DM2_res.T

            rig = np.array([100, 100, 100, 100, 100])
            res1 = np.linalg.solve(DM1_res, rig)
            res2 = np.linalg.solve(DM2_res, rig)
            res1 = res1/np.sum(res1)
            res2 = res2/np.sum(res2)


            # def inner_nash(res):
            #     x1=Symbol("x1")
            #     x2 = Symbol("x2")
            #     x3 = Symbol("x3")
            #     x4 = Symbol("x4")
            #     x5 = Symbol("x5")
            #     innerResult=solve([(res[0][0]*x1+res[0][1]*x2+res[0][2]*x3+res[0][3]*x4+res[0][4]*x5)-(res[1][0]*x1+res[1][1]*x2+res[1][2]*x3+res[1][3]*x4+res[1][4]*x5),
            #                       (res[0][0]*x1+res[0][1]*x2+res[0][2]*x3+res[0][3]*x4+res[0][4]*x5)-(res[2][0]*x1+res[2][1]*x2+res[2][2]*x3+res[2][3]*x4+res[2][4]*x5),
            #                       (res[0][0]*x1+res[0][1]*x2+res[0][2]*x3+res[0][3]*x4+res[0][4]*x5)-(res[3][0]*x1+res[3][1]*x2+res[3][2]*x3+res[3][3]*x4+res[3][4]*x5),
            #                       (res[0][0]*x1+res[0][1]*x2+res[0][2]*x3+res[0][3]*x4+res[0][4]*x5)-(res[4][0]*x1+res[4][1]*x2+res[4][2]*x3+res[4][3]*x4+res[4][4]*x5),
            #                       x1+x2+x3+x4+x5-1],[x1,x2,x3,x4,x5])
            #     print(innerResult)
            #     return innerResult
            # res1 = inner_nash(DM1_res)
            # res2 = inner_nash(DM2_res)
            j = 0
            key = True
            while j < 5:
                if res1[j]<=1 and res1[j]>=0 and res2[j]<=1 and res2[j]>=0:
                    key = True
                    j = j+1
                else:
                    key = False
                    break

            if key == True:
                list_nash.append((res1, res2))
                print("list_nash="+str(list_nash))
                self.ui.textBrowser_2.append("nash均衡：\n" + "(" + str(res1) + "," + str(res2) + ")\n")
            else:
                self.ui.textBrowser_2.append("非nash均衡：\n" + "(" + str(res1) + "," + str(res2) + ")\n")
                list_nash.append('不是nash均衡')
            #---------------------判断顶点是不是Nash均衡-------------------------
            i = 0
            while i<5:
                j = 0
                while j<5:
                    row = [0, 1, 2, 3, 4]
                    col = [0, 1, 2, 3, 4]
                    row.remove(i)
                    col.remove(j)
                    # print(row,row[0],row[1],row[2],row[3])
                    # print(col,col[0],col[1],col[2],col[3])
                    # print("\n")
                    # if DM1_res[i][j] > DM1_res[row[0]][j] and DM1_res[i][j] > DM1_res[row[1]][j] and DM1_res[i][j] > \
                    #         DM1_res[row[2]][j] and DM1_res[i][j] > DM1_res[row[3]][j] and DM2_res[i][j] > DM2_res[i][
                    #     col[0]] and DM2_res[i][j] > DM2_res[i][col[1]] and DM2_res[i][j] > DM2_res[i][col[2]] and \
                    #         DM2_res[i][j] > DM2_res[i][col[3]]:
                    if DM1_res[i][j] > DM1_res[row[0]][j] and DM1_res[i][j] > DM1_res[row[1]][j] and DM1_res[i][j] > \
                            DM1_res[row[2]][j] and DM1_res[i][j] > DM1_res[row[3]][j] and DM2_res[i][j] > DM2_res[i][
                        col[0]] and DM2_res[i][j] > DM2_res[i][col[1]] and DM2_res[i][j] > DM2_res[i][col[2]] and \
                            DM2_res[i][j] > DM2_res[i][col[3]]:
                        e_fir = [0, 0, 0, 0, 0]
                        e_sec = [0, 0, 0, 0, 0]
                        e_fir[i] = 1
                        e_sec[j] = 1
                        self.ui.textBrowser_3.append('('+str(e_fir)+str(e_sec)+')')
                        list_nash.append((e_fir, e_sec))
                    j = j + 1
                i = i + 1

            return list_nash

        #动态均衡检验函数
        def check_x(res1,res2,DM1_res):
            e = np.identity(5)
            i = 0
            list_dx = []
            while i < 5:
                for x in res1:
                    dx = (np.dot(e[i],DM1_res,res2)-np.dot(res1,DM1_res,res2))*x
                    list_dx.append(dx)
                i = i+1
            return list_dx

        def check_y(res1,res2,DM2_res):
            e = np.identity(5)
            i = 0
            list_dy = []
            while i < 5:
                for y in res2:
                    dy = (np.dot(res1,DM2_res,e[i])-np.dot(res1,DM2_res,res2))*y
                    list_dy.append(dy)
                i = i+1
            return list_dy
        #打印动态均衡
        def dynamics():
            #list_nash[0]带入进行验算，其余直接打印
            list_nash = nash()
            self.ui.textBrowser_4.clear()
            for ne in list_nash[1:]:
                self.ui.textBrowser_4.append("動学的均衡:\n"+str(ne)+'\n')
            #-----------验算list_nash[0]是否为动态均衡------------(怎么感觉不太对？？？？)
            try:
                list_dx = check_x(nash()[0][0],nash()[0][1],print_benefit(countries[game_dm1],countries[game_dm2])[0])
                list_dy = check_y(nash()[0][0],nash()[0][1],print_benefit(countries[game_dm1],countries[game_dm2])[1])
                if (np.array(list_dx) == 0).any() and (np.array(list_dy) == 0).any():
                    self.ui.textBrowser_4.append("動学的均衡:\n" + str(list_nash[0]) + '\n')
            except:
                print("不是动态均衡")



        print_benefit(countries[game_dm1],countries[game_dm2])
        nash()
        dynamics()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('bitcoin.png'))
    calcu = Calculator()
    calcu.ui.show()
    app.exec_()
