# coding: utf-8
# Date ：2021/7/22 18:48
# Tool ：PyCharm
import matplotlib.pyplot as plt
import pandas as pd
import xlrd


data_dqn = pd.read_excel(r'C:\Users\Zhou\Desktop\兵棋推演平台v6.0\results\PPO胜率提取测试.xlsx')
data_pkdqn = pd.read_excel(r'C:\Users\Zhou\Desktop\兵棋推演平台v6.0\results\PK-PPO胜率提取测试.xlsx')
data_rnmdqn = pd.read_excel(r'C:\Users\Zhou\Desktop\兵棋推演平台v6.0\results\RNM-PPO胜率提取测试.xlsx')
data_ifnmdqn = pd.read_excel(r'C:\Users\Zhou\Desktop\兵棋推演平台v6.0\results\IFNM-PPO胜率提取测试.xlsx')
dqn = data_dqn[0:100]
pkdqn = data_pkdqn[0:100]
rnmdqn = data_rnmdqn[0:100]
ifnmdqn = data_ifnmdqn[0:100]
fig = plt.subplot()
# ax1.set_title("上半场")
fig.plot(range(100), dqn, 'r', label='PPO')
fig.plot(range(100), pkdqn, 'g', label='PK-PPO')
fig.plot(range(100), rnmdqn, 'b', label='Real Number M-PPO')
fig.plot(range(100), ifnmdqn, 'y', label='Intuitionistic Fuzzy Numbers M-PPO')
plt.legend()
plt.xlabel("Episodes")
plt.ylabel("Percentage")
plt.show()