# def cal_it1(country1, country2, char, row, aver_gdp=None):
#     # self.country1 = country1
#     # self.country2 = country2
#     # self.char = char
#     gdp_margin = (country1[0] - aver_gdp) / max_gdp
#     print(gdp_margin)
#     k = math.exp(gdp_margin)
#
#     # if self.country1[0] > aver_gdp:
#     #     k =round ((self.country1[0] - aver_gdp) * 10 / max_gdp,1)
#     # elif self.country1[0] == aver_gdp:
#     #     k = 1
#     # elif self.country1[0] < aver_gdp:
#     #     k = round(1 / abs(self.country1[0] - aver_gdp),1)
#     print("k=" + str(k))
#     per_gdp_margin = (country1[1] - aver_per_gdp) * (-1) / max_per_gdp1
#     p = math.exp(per_gdp_margin)
#
#     # if self.country1[1] > aver_per_gdp:
#     #     p = round(1 / (self.country1[1] - aver_per_gdp),1)
#     # elif self.country1[1] == aver_per_gdp:
#     #     p = 1
#     # elif self.country1[1] < aver_per_gdp:
#     #     p = round(abs(self.country1[1] - aver_per_gdp) * 10 / max_per_gdp,1)
#     print("p=" + str(p))
#
#     # right = round(5*(self.country2[2] + self.country2[3]) / (
#     #             self.country1[2] + self.country1[3] + self.country2[2] + self.country2[3]),1)
#     right = round(5 * (country2[2] + country2[3]) / (
#             country1[2] + country1[3] + country2[2] + country2[3]), 1)
#     # right = round((self.country2[2] + self.country2[3]) / (
#     #             self.country1[2] + self.country1[3] ),1)
#     # result = round((k * (self.char[2] + self.char[3]) + p * (self.char[0] + self.char[1])) * right,1)
#     result = round((k * (char[2] + char[3]) + p * (char[0] + char[1])) * right, 1)
#     # print("速度="+str(self.char[2] + self.char[3]))
#     # print("安全="+str(self.char[0] + self.char[1]))
#     # print("right="+str(right)+"\n")
#     # print('result='+ str(result)+"\n")
#     col = 0
#     while col < 5:
#         DM1[row][col] = result
#         col = col + 1
#     # print(DM1)