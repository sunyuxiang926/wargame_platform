# Author: Tao Zhang
# CreateTime: 2020/8
# FileName: ResultVisualization
# Description: 结果可视化
import matplotlib.pyplot as plt
import pandas as pd

class ResultVisualization:
    def __init__(self, _first_half_episodes, _second_half_episodes):
        """
        初始化
        """
        # 推演信息
        self.first_half_episodes = _first_half_episodes  # 上半场推演回合数
        self.second_half_episodes = _second_half_episodes  # 下半场推演回合数
        # 红方信息
        self.red_kill_score = []  # 远程打击得分
        self.red_get_goal_score = []  # 夺控分
        self.red_survive_score = []  # 剩余兵力
        self.red_win_times = []  # 获胜次数
        self.red_point_attack_score = []
        self.red_point_defense_score = []
        # 蓝方信息
        self.blue_kill_score = []
        self.blue_get_goal_score = []
        self.blue_survive_score = []
        self.blue_win_times = []
        self.blue_point_attack_score = []
        self.blue_point_defense_score = []

    def data_update(self, wargame_town):
        """
        更新数据
        :param isRed: 是否为红方，布尔类型
        :param wargame_town: 推演环境的信息，环境env类型
        :return: void
        """
        self.red_kill_score.append(wargame_town.red_kill_score)
        self.red_get_goal_score.append(wargame_town.red_get_goal_score)
        self.red_survive_score.append(wargame_town.red_survive_score)
        self.red_win_times.append(wargame_town.red_win_times)
        self.red_point_attack_score.append(wargame_town.red_pointattack_score)
        self.red_point_defense_score.append(wargame_town.red_pointdefense_score)

        self.blue_kill_score.append(wargame_town.blue_kill_score)
        self.blue_get_goal_score.append(wargame_town.blue_get_goal_score)
        self.blue_survive_score.append(wargame_town.blue_survive_score)
        self.blue_win_times.append(wargame_town.blue_win_times)
        self.blue_point_attack_score.append(wargame_town.blue_pointattack_score)
        self.blue_point_defense_score.append(wargame_town.blue_pointdefense_score)

    def output(self):
        """
        输出图片
        :return: 保存至项目的根目录中
        """
        print("----------")
        print("画图所用的数据：")

        print("red_kill_score:")
        print(self.red_kill_score)
        print("red_get_goal_score:")
        print(self.red_get_goal_score)
        print("red_survive_score:")
        print(self.red_survive_score)
        print("red_win_times:")
        print(self.red_win_times)
        print("red_point_attack_score")
        print(self.red_point_attack_score)
        print("red_point_defense_score")
        print(self.red_point_defense_score)

        print("blue_kill_score:")
        print(self.blue_kill_score)
        print("blue_get_goal_score:")
        print(self.blue_get_goal_score)
        print("blue_survive_score:")
        print(self.blue_survive_score)
        print("blue_win_times:")
        print(self.blue_win_times)
        print("blue_point_attack_score")
        print(self.blue_point_attack_score)
        print("blue_point_defense_score")
        print(self.blue_point_defense_score)

        print("----------")

        plt.rcParams['font.family'] = ['sans-serif']
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.style.use('ggplot')

        # 绘图1：双方歼敌得分
        fig1 = plt.figure()
        fig1.suptitle("The kill score of both sides")
        # ax1 = plt.subplot(121)
        ax1 = plt.subplot(111)
        # ax1.set_title("上半场")
        ax1.plot(range(self.first_half_episodes), self.red_kill_score[0:self.first_half_episodes], 'r', label='red')
        ax1.plot(range(self.first_half_episodes), self.blue_kill_score[0:self.first_half_episodes], '--b', label='blue')
        plt.legend()
        # ax2 = plt.subplot(122)
        # ax2.set_title("下半场")
        # ax2.plot(self.red_kill_score[self.first_half_episodes:], 'r', label='red')
        # ax2.plot(self.blue_kill_score[self.first_half_episodes:], '--', 'b', label='blue')
        plt.xlabel("Episodes")
        plt.ylabel("Score")
        plt.savefig('kill_score.jpg', dpi=300)
        # 将数据保存到DataFrame对象中
        data = {
            'red_kill_score': self.red_kill_score[self.first_half_episodes:],
            'blue_kill_score': self.blue_kill_score[self.first_half_episodes:]
        }
        df = pd.DataFrame(data)
        # 保存DataFrame到Excel文件
        # df.to_excel('kill_score.xlsx', index=False)

        # 绘图2：双方夺控得分
        fig2 = plt.figure()
        fig2.suptitle("The get goal score of both sides")
        # ax1 = plt.subplot(121)
        ax1 = plt.subplot(111)
        # ax1.set_title("上半场")
        ax1.plot(range(self.first_half_episodes), self.red_get_goal_score[0:self.first_half_episodes], 'r', label='red')
        ax1.plot(range(self.first_half_episodes), self.blue_get_goal_score[0:self.first_half_episodes], '--b', label='blue')
        plt.legend()
        # ax2 = plt.subplot(122)
        # ax2.set_title("下半场")
        # ax2.plot(self.red_get_goal_score[self.first_half_episodes:], 'r', label='red')
        # ax2.plot(self.blue_get_goal_score[self.first_half_episodes:], '--', 'b', label='blue')
        plt.xlabel("Episodes")
        plt.ylabel("Score")
        plt.savefig('get_goal_score.jpg', dpi=300)

        # 绘图3：双方存活得分
        fig3 = plt.figure()
        fig3.suptitle("The survive score of both sides")
        # ax1 = plt.subplot(121)
        ax1 = plt.subplot(111)
        # ax1.set_title("上半场")
        ax1.plot(range(self.first_half_episodes), self.red_survive_score[0:self.first_half_episodes], 'r', label='red')
        ax1.plot(range(self.first_half_episodes), self.blue_survive_score[0:self.first_half_episodes], '--b',
                 label='blue')
        plt.legend()
        # ax2 = plt.subplot(122)
        # ax2.set_title("下半场")
        # ax2.plot(self.red_survive_score[self.first_half_episodes:], 'r', label='red')
        # ax2.plot(self.blue_survive_score[self.first_half_episodes:], '--', 'b', label='blue')
        plt.xlabel("Episodes")
        plt.ylabel("Score")
        plt.savefig('survive_score.jpg', dpi=300)

        # 绘图4：双方胜场次数
        fig4 = plt.figure()
        fig4.suptitle("The winning times of both sides")
        # ax1 = plt.subplot(121)
        ax1 = plt.subplot(111)
        # ax1.set_title("上半场")
        ax1.plot(range(self.first_half_episodes), self.red_win_times[0:self.first_half_episodes], 'r', label='red')
        ax1.plot(range(self.first_half_episodes), self.blue_win_times[0:self.first_half_episodes], '--b', label='blue')
        plt.legend()
        # ax2 = plt.subplot(122)
        # ax2.set_title("下半场")
        # ax2.plot(self.red_win_times[self.first_half_episodes:], 'r', label='red')
        # ax2.plot(self.blue_win_times[self.first_half_episodes:], '--', 'b', label='blue')
        plt.xlabel("Episodes")
        plt.ylabel("Win times")
        plt.savefig('win_times.jpg', dpi=300)

        # 绘图5：双方胜率
        red_win_rate = []
        blue_win_rate = []
        for i in range(len(self.red_win_times)):
            red_win_rate.append(self.red_win_times[i] / (self.red_win_times[i] + self.blue_win_times[i])*100)
            blue_win_rate.append(self.blue_win_times[i] / (self.red_win_times[i] + self.blue_win_times[i])*100)
        fig5 = plt.figure()
        fig5.suptitle("The winning rate of both sides")
        # ax1 = plt.subplot(121)
        ax1 = plt.subplot(111)
        # ax1.set_title("上半场")
        ax1.plot(range(self.first_half_episodes), red_win_rate[0:self.first_half_episodes], 'r', label='red')
        ax1.plot(range(self.first_half_episodes), blue_win_rate[0:self.first_half_episodes], '--b', label='blue')
        plt.legend()
        # ax2 = plt.subplot(122)
        # ax2.set_title("下半场")
        # ax2.plot(self.red_win_rate[self.first_half_episodes:], 'r', label='red')
        # ax2.plot(self.blue_win_rate[self.first_half_episodes:], '--', 'b', label='blue')
        plt.xlabel("Episodes")
        plt.ylabel("Percentage")
        plt.savefig('win_rate.jpg', dpi=300)
        # 将字典转换为数据帧
        df = pd.DataFrame(red_win_rate[0:self.first_half_episodes])
        # 将数据帧保存到Excel文件
        # df.to_excel('win_rate.xlsx', index=False)

        # 绘图6：双方抢攻得分
        fig6 = plt.figure()
        fig6.suptitle("The sound attack score of both sides")
        ax1 = plt.subplot(111)
        ax1.plot(range(self.first_half_episodes), self.red_point_attack_score[0:self.first_half_episodes], 'r', label='red')
        ax1.plot(range(self.first_half_episodes), self.blue_point_attack_score[0:self.first_half_episodes], '--b', label='blue')
        plt.legend()
        plt.xlabel("Episodes")
        plt.ylabel("Sound Attack Score")
        plt.savefig('sound_attack.jpg', dpi=300)

        # 绘图7：双方据守得分
        fig7 = plt.figure()
        fig7.suptitle("The guard score of both sides")
        ax1 = plt.subplot(111)
        ax1.plot(range(self.first_half_episodes), self.red_point_defense_score[0:self.first_half_episodes], 'r', label='red')
        ax1.plot(range(self.first_half_episodes), self.blue_point_defense_score[0:self.first_half_episodes], '--b', label='blue')
        plt.legend()
        plt.xlabel("Episodes")
        plt.ylabel("Guard Score")
        plt.savefig('Guard_Score.jpg', dpi=300)

    def output1(self):
        """
        输出图片
        :return: 保存至项目的根目录中
        """
        print("----------")
        print("画图所用的数据：")
        print("red_kill_score")
        print(self.red_kill_score)
        print("red_get_goal_score")
        print(self.red_get_goal_score)
        print("red_survive_score")
        print(self.red_survive_score)
        print("red_win_times")
        print(self.red_win_times)
        print("blue_kill_score")
        print(self.blue_kill_score)
        print("blue_get_goal_score")
        print(self.blue_get_goal_score)
        print("blue_survive_score")
        print(self.blue_survive_score)
        print("blue_win_times")
        print(self.blue_win_times)
        print("----------")

        plt.rcParams['font.family'] = ['sans-serif']
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.style.use('ggplot')

        fig1 = plt.figure()
        fig1.suptitle("The kill score of both sides(mhs)")
        # ax1 = plt.subplot(121)
        ax1 = plt.subplot(111)
        # ax1.set_title("上半场")
        ax1.plot(range(self.first_half_episodes), self.red_kill_score[0:self.first_half_episodes], 'r', label='red')
        ax1.plot(range(self.first_half_episodes), self.blue_kill_score[0:self.first_half_episodes], '--b', label='blue')
        plt.legend()
        # ax2 = plt.subplot(122)
        # ax2.set_title("下半场")
        # ax2.plot(self.red_kill_score[self.first_half_episodes:], 'r', label='red')
        # ax2.plot(self.blue_kill_score[self.first_half_episodes:], '--', 'b', label='blue')
        plt.xlabel("Episodes")
        plt.ylabel("Score")
        plt.savefig('mhs_kill_score.jpg', dpi=300)

        fig2 = plt.figure()
        fig2.suptitle("The get goal score of both sides(mhs)")
        # ax1 = plt.subplot(121)
        ax1 = plt.subplot(111)
        # ax1.set_title("上半场")
        ax1.plot(range(self.first_half_episodes), self.red_get_goal_score[0:self.first_half_episodes], 'r', label='red')
        ax1.plot(range(self.first_half_episodes), self.blue_get_goal_score[0:self.first_half_episodes], '--b',
                 label='blue')
        plt.legend()
        # ax2 = plt.subplot(122)
        # ax2.set_title("下半场")
        # ax2.plot(self.red_get_goal_score[self.first_half_episodes:], 'r', label='red')
        # ax2.plot(self.blue_get_goal_score[self.first_half_episodes:], '--', 'b', label='blue')
        plt.xlabel("Episodes")
        plt.ylabel("Score")
        plt.savefig('mhs_get_goal_score.jpg', dpi=300)

        fig3 = plt.figure()
        fig3.suptitle("The survive score of both sides(mhs)")
        # ax1 = plt.subplot(121)
        ax1 = plt.subplot(111)
        # ax1.set_title("上半场")
        ax1.plot(range(self.first_half_episodes), self.red_survive_score[0:self.first_half_episodes], 'r', label='red')
        ax1.plot(range(self.first_half_episodes), self.blue_survive_score[0:self.first_half_episodes], '--b',
                 label='blue')
        plt.legend()
        # ax2 = plt.subplot(122)
        # ax2.set_title("下半场")
        # ax2.plot(self.red_survive_score[self.first_half_episodes:], 'r', label='red')
        # ax2.plot(self.blue_survive_score[self.first_half_episodes:], '--', 'b', label='blue')
        plt.xlabel("Episodes")
        plt.ylabel("Score")
        plt.savefig('mhs_survive_score.jpg', dpi=300)

        fig4 = plt.figure()
        fig4.suptitle("The win times of both sides(mhs)")
        # ax1 = plt.subplot(121)
        ax1 = plt.subplot(111)
        # ax1.set_title("上半场")
        ax1.plot(range(self.first_half_episodes), self.red_win_times[0:self.first_half_episodes], 'r', label='red')
        ax1.plot(range(self.first_half_episodes), self.blue_win_times[0:self.first_half_episodes], '--b', label='blue')
        plt.legend()
        # ax2 = plt.subplot(122)
        # ax2.set_title("下半场")
        # ax2.plot(self.red_win_times[self.first_half_episodes:], 'r', label='red')
        # ax2.plot(self.blue_win_times[self.first_half_episodes:], '--', 'b', label='blue')
        plt.xlabel("Episodes")
        plt.ylabel("Win times")
        plt.savefig('mhs_win_times.jpg', dpi=300)

        # 计算胜率
        red_win_rate = []
        blue_win_rate = []
        for i in range(len(self.red_win_times)):
            red_win_rate.append(self.red_win_times[i] / (self.red_win_times[i] + self.blue_win_times[i])*100)
            blue_win_rate.append(self.blue_win_times[i] / (self.red_win_times[i] + self.blue_win_times[i])*100)
        fig5 = plt.figure()
        fig5.suptitle("The win rate of both sides(mhs)")
        # ax1 = plt.subplot(121)
        ax1 = plt.subplot(111)
        # ax1.set_title("上半场")
        ax1.plot(range(self.first_half_episodes), red_win_rate[0:self.first_half_episodes], 'r', label='red')
        ax1.plot(range(self.first_half_episodes), blue_win_rate[0:self.first_half_episodes], '--b', label='blue')
        plt.legend()
        # ax2 = plt.subplot(122)
        # ax2.set_title("下半场")
        # ax2.plot(self.red_win_rate[self.first_half_episodes:], 'r', label='red')
        # ax2.plot(self.blue_win_rate[self.first_half_episodes:], '--', 'b', label='blue')
        plt.xlabel("Episodes")
        plt.ylabel("Percentage")
        plt.savefig('mhs_win_rate.jpg', dpi=300)

    def output2(self):
        """
        输出图片
        :return: 保存至项目的根目录中
        """
        print("----------")
        print("画图所用的数据：")
        print("red_kill_score")
        print(self.red_kill_score)
        print("red_get_goal_score")
        print(self.red_get_goal_score)
        print("red_survive_score")
        print(self.red_survive_score)
        print("red_win_times")
        print(self.red_win_times)
        print("blue_kill_score")
        print(self.blue_kill_score)
        print("blue_get_goal_score")
        print(self.blue_get_goal_score)
        print("blue_survive_score")
        print(self.blue_survive_score)
        print("blue_win_times")
        print(self.blue_win_times)
        print("----------")

        plt.rcParams['font.family'] = ['sans-serif']
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.style.use('ggplot')

        fig1 = plt.figure()
        fig1.suptitle("The kill score of both sides(ss)")
        # ax1 = plt.subplot(121)
        ax1 = plt.subplot(111)
        # ax1.set_title("上半场")
        ax1.plot(range(self.first_half_episodes), self.red_kill_score[0:self.first_half_episodes], 'r', label='red')
        ax1.plot(range(self.first_half_episodes), self.blue_kill_score[0:self.first_half_episodes], '--b', label='blue')
        plt.legend()
        # ax2 = plt.subplot(122)
        # ax2.set_title("下半场")
        # ax2.plot(self.red_kill_score[self.first_half_episodes:], 'r', label='red')
        # ax2.plot(self.blue_kill_score[self.first_half_episodes:], '--', 'b', label='blue')
        plt.xlabel("Episodes")
        plt.ylabel("Score")
        plt.savefig('ss_kill_score.jpg', dpi=300)

        fig2 = plt.figure()
        fig2.suptitle("The get goal score of both sides(ss)")
        # ax1 = plt.subplot(121)
        ax1 = plt.subplot(111)
        # ax1.set_title("上半场")
        ax1.plot(range(self.first_half_episodes), self.red_get_goal_score[0:self.first_half_episodes], 'r', label='red')
        ax1.plot(range(self.first_half_episodes), self.blue_get_goal_score[0:self.first_half_episodes], '--b',
                 label='blue')
        plt.legend()
        # ax2 = plt.subplot(122)
        # ax2.set_title("下半场")
        # ax2.plot(self.red_get_goal_score[self.first_half_episodes:], 'r', label='red')
        # ax2.plot(self.blue_get_goal_score[self.first_half_episodes:], '--', 'b', label='blue')
        plt.xlabel("Episodes")
        plt.ylabel("Score")
        plt.savefig('ss_get_goal_score.jpg', dpi=300)

        fig3 = plt.figure()
        fig3.suptitle("The survive score of both sides(ss)")
        # ax1 = plt.subplot(121)
        ax1 = plt.subplot(111)
        # ax1.set_title("上半场")
        ax1.plot(range(self.first_half_episodes), self.red_survive_score[0:self.first_half_episodes], 'r', label='red')
        ax1.plot(range(self.first_half_episodes), self.blue_survive_score[0:self.first_half_episodes], '--b',
                 label='blue')
        plt.legend()
        # ax2 = plt.subplot(122)
        # ax2.set_title("下半场")
        # ax2.plot(self.red_survive_score[self.first_half_episodes:], 'r', label='red')
        # ax2.plot(self.blue_survive_score[self.first_half_episodes:], '--', 'b', label='blue')
        plt.xlabel("Episodes")
        plt.ylabel("Score")
        plt.savefig('ss_survive_score.jpg', dpi=300)

        fig4 = plt.figure()
        fig4.suptitle("The win times of both sides(ss)")
        # ax1 = plt.subplot(121)
        ax1 = plt.subplot(111)
        # ax1.set_title("上半场")
        ax1.plot(range(self.first_half_episodes), self.red_win_times[0:self.first_half_episodes], 'r', label='red')
        ax1.plot(range(self.first_half_episodes), self.blue_win_times[0:self.first_half_episodes], '--b', label='blue')
        plt.legend()
        # ax2 = plt.subplot(122)
        # ax2.set_title("下半场")
        # ax2.plot(self.red_win_times[self.first_half_episodes:], 'r', label='red')
        # ax2.plot(self.blue_win_times[self.first_half_episodes:], '--', 'b', label='blue')
        plt.xlabel("Episodes")
        plt.ylabel("Win times")
        plt.savefig('ss_win_times.jpg', dpi=300)

        # 计算胜率
        red_win_rate = []
        blue_win_rate = []
        for i in range(len(self.red_win_times)):
            red_win_rate.append(self.red_win_times[i] / (self.red_win_times[i] + self.blue_win_times[i])*100)
            blue_win_rate.append(self.blue_win_times[i] / (self.red_win_times[i] + self.blue_win_times[i])*100)
        fig5 = plt.figure()
        fig5.suptitle("The win rate of both sides(ss)")
        # ax1 = plt.subplot(121)
        ax1 = plt.subplot(111)
        # ax1.set_title("上半场")
        ax1.plot(range(self.first_half_episodes), red_win_rate[0:self.first_half_episodes], 'r', label='red')
        ax1.plot(range(self.first_half_episodes), blue_win_rate[0:self.first_half_episodes], '--b', label='blue')
        plt.legend()
        # ax2 = plt.subplot(122)
        # ax2.set_title("下半场")
        # ax2.plot(self.red_win_rate[self.first_half_episodes:], 'r', label='red')
        # ax2.plot(self.blue_win_rate[self.first_half_episodes:], '--', 'b', label='blue')
        plt.xlabel("Episodes")
        plt.ylabel("Percentage")
        plt.savefig('ss_win_rate.jpg', dpi=300)

    def output3(self):
        """
        输出图片
        :return: 保存至项目的根目录中
        """
        print("----------")
        print("画图所用的数据：")
        print("red_kill_score")
        print(self.red_kill_score)
        print("red_get_goal_score")
        print(self.red_get_goal_score)
        print("red_survive_score")
        print(self.red_survive_score)
        print("red_win_times")
        print(self.red_win_times)
        print("blue_kill_score")
        print(self.blue_kill_score)
        print("blue_get_goal_score")
        print(self.blue_get_goal_score)
        print("blue_survive_score")
        print(self.blue_survive_score)
        print("blue_win_times")
        print(self.blue_win_times)
        print("----------")

        plt.rcParams['font.family'] = ['sans-serif']
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.style.use('ggplot')

        fig1 = plt.figure()
        fig1.suptitle("The kill score of both sides(ss)")
        # ax1 = plt.subplot(121)
        ax1 = plt.subplot(111)
        # ax1.set_title("上半场")
        ax1.plot(range(self.first_half_episodes), self.red_kill_score[0:self.first_half_episodes], 'r', label='red')
        ax1.plot(range(self.first_half_episodes), self.blue_kill_score[0:self.first_half_episodes], '--b', label='blue')
        plt.legend()
        # ax2 = plt.subplot(122)
        # ax2.set_title("下半场")
        # ax2.plot(self.red_kill_score[self.first_half_episodes:], 'r', label='red')
        # ax2.plot(self.blue_kill_score[self.first_half_episodes:], '--', 'b', label='blue')
        plt.xlabel("Episodes")
        plt.ylabel("Score")
        plt.savefig('ss_kill_score.jpg', dpi=300)

        fig2 = plt.figure()
        fig2.suptitle("The get goal score of both sides(ss)")
        # ax1 = plt.subplot(121)
        ax1 = plt.subplot(111)
        # ax1.set_title("上半场")
        ax1.plot(range(self.first_half_episodes), self.red_get_goal_score[0:self.first_half_episodes], 'r', label='red')
        ax1.plot(range(self.first_half_episodes), self.blue_get_goal_score[0:self.first_half_episodes], '--b',
                 label='blue')
        plt.legend()
        # ax2 = plt.subplot(122)
        # ax2.set_title("下半场")
        # ax2.plot(self.red_get_goal_score[self.first_half_episodes:], 'r', label='red')
        # ax2.plot(self.blue_get_goal_score[self.first_half_episodes:], '--', 'b', label='blue')
        plt.xlabel("Episodes")
        plt.ylabel("Score")
        plt.savefig('szjc_get_goal_score.jpg', dpi=300)

        fig3 = plt.figure()
        fig3.suptitle("The survive score of both sides(szjc)")
        # ax1 = plt.subplot(121)
        ax1 = plt.subplot(111)
        # ax1.set_title("上半场")
        ax1.plot(range(self.first_half_episodes), self.red_survive_score[0:self.first_half_episodes], 'r', label='red')
        ax1.plot(range(self.first_half_episodes), self.blue_survive_score[0:self.first_half_episodes], '--b',
                 label='blue')
        plt.legend()
        # ax2 = plt.subplot(122)
        # ax2.set_title("下半场")
        # ax2.plot(self.red_survive_score[self.first_half_episodes:], 'r', label='red')
        # ax2.plot(self.blue_survive_score[self.first_half_episodes:], '--', 'b', label='blue')
        plt.xlabel("Episodes")
        plt.ylabel("Score")
        plt.savefig('szjc_survive_score.jpg', dpi=300)

        fig4 = plt.figure()
        fig4.suptitle("The win times of both sides(szjc)")
        # ax1 = plt.subplot(121)
        ax1 = plt.subplot(111)
        # ax1.set_title("上半场")
        ax1.plot(range(self.first_half_episodes), self.red_win_times[0:self.first_half_episodes], 'r', label='red')
        ax1.plot(range(self.first_half_episodes), self.blue_win_times[0:self.first_half_episodes], '--b', label='blue')
        plt.legend()
        # ax2 = plt.subplot(122)
        # ax2.set_title("下半场")
        # ax2.plot(self.red_win_times[self.first_half_episodes:], 'r', label='red')
        # ax2.plot(self.blue_win_times[self.first_half_episodes:], '--', 'b', label='blue')
        plt.xlabel("Episodes")
        plt.ylabel("Win times")
        plt.savefig('szjc_win_times.jpg', dpi=300)

        # 计算胜率
        red_win_rate = []
        blue_win_rate = []
        for i in range(len(self.red_win_times)):
            red_win_rate.append(self.red_win_times[i] / (self.red_win_times[i] + self.blue_win_times[i])*100)
            blue_win_rate.append(self.blue_win_times[i] / (self.red_win_times[i] + self.blue_win_times[i])*100)
        fig5 = plt.figure()
        fig5.suptitle("The win rate of both sides(szjc)")
        # ax1 = plt.subplot(121)
        ax1 = plt.subplot(111)
        # ax1.set_title("上半场")
        ax1.plot(range(self.first_half_episodes), red_win_rate[0:self.first_half_episodes], 'r', label='red')
        ax1.plot(range(self.first_half_episodes), blue_win_rate[0:self.first_half_episodes], '--b', label='blue')
        plt.legend()
        # ax2 = plt.subplot(122)
        # ax2.set_title("下半场")
        # ax2.plot(self.red_win_rate[self.first_half_episodes:], 'r', label='red')
        # ax2.plot(self.blue_win_rate[self.first_half_episodes:], '--', 'b', label='blue')
        plt.xlabel("Episodes")
        plt.ylabel("Percentage")
        plt.savefig('szjc_win_rate.jpg', dpi=300)

    def output_HCI(self):
        print()
        # """
        # 输出图片
        # :return: 保存至项目的根目录中
        # """
        # print("----------")
        # print("画图所用的数据：")
        # print("red_kill_score")
        # print(self.red_kill_score)
        # print("red_get_goal_score")
        # print(self.red_get_goal_score)
        # print("red_survive_score")
        # print(self.red_survive_score)
        # print("red_win_times")
        # print(self.red_win_times)
        # print("blue_kill_score")
        # print(self.blue_kill_score)
        # print("blue_get_goal_score")
        # print(self.blue_get_goal_score)
        # print("blue_survive_score")
        # print(self.blue_survive_score)
        # print("blue_win_times")
        # print(self.blue_win_times)
        # print("----------")
        #
        # plt.rcParams['font.family'] = ['sans-serif']
        # plt.rcParams['font.sans-serif'] = ['SimHei']
        # plt.style.use('ggplot')
        #
        # fig1 = plt.figure()
        # fig1.suptitle("The kill score of both sides")
        #
        # ax1 = plt.subplot(111)
        #
        # ax1.plot(range(self.first_half_episodes), self.red_kill_score[0:self.first_half_episodes], 'r', label='red')
        # ax1.plot(range(self.first_half_episodes), self.blue_kill_score[0:self.first_half_episodes], '--b', label='blue')
        # plt.legend()
        #
        # plt.xlabel("Episodes")
        # plt.ylabel("Score")
        # plt.savefig('kill_score.jpg', dpi=300)
        # # 将数据保存到DataFrame对象中
        # data = {
        #     'red_kill_score': self.red_kill_score[self.first_half_episodes:],
        #     'blue_kill_score': self.blue_kill_score[self.first_half_episodes:]
        # }
        # df = pd.DataFrame(data)
        # # 保存DataFrame到Excel文件
        # df.to_excel('kill_score.xlsx', index=False)
        #
        # fig2 = plt.figure()
        # fig2.suptitle("The get goal score of both sides")
        #
        # ax1 = plt.subplot(111)
        #
        # ax1.plot(range(self.first_half_episodes), self.red_get_goal_score[0:self.first_half_episodes], 'r', label='red')
        # ax1.plot(range(self.first_half_episodes), self.blue_get_goal_score[0:self.first_half_episodes], '--b', label='blue')
        # plt.legend()
        #
        # plt.xlabel("Episodes")
        # plt.ylabel("Score")
        # plt.savefig('get_goal_score.jpg', dpi=300)
        #
        # fig3 = plt.figure()
        # fig3.suptitle("The survive score of both sides")
        #
        # ax1 = plt.subplot(111)
        #
        # ax1.plot(range(self.first_half_episodes), self.red_survive_score[0:self.first_half_episodes], 'r', label='red')
        # ax1.plot(range(self.first_half_episodes), self.blue_survive_score[0:self.first_half_episodes], '--b',
        #          label='blue')
        # plt.legend()
        #
        # plt.xlabel("Episodes")
        # plt.ylabel("Score")
        # plt.savefig('survive_score.jpg', dpi=300)
        #
        # fig4 = plt.figure()
        # fig4.suptitle("The win times of both sides")
        #
        # ax1 = plt.subplot(111)
        #
        # ax1.plot(range(self.first_half_episodes), self.red_win_times[0:self.first_half_episodes], 'r', label='red')
        # ax1.plot(range(self.first_half_episodes), self.blue_win_times[0:self.first_half_episodes], '--b', label='blue')
        # plt.legend()
        #
        # plt.xlabel("Episodes")
        # plt.ylabel("Win times")
        # plt.savefig('win_times.jpg', dpi=300)
        #
        # # 计算胜率
        # red_win_rate = []
        # blue_win_rate = []
        # for i in range(len(self.red_win_times)):
        #     red_win_rate.append(self.red_win_times[i] / (self.red_win_times[i] + self.blue_win_times[i])*100)
        #     blue_win_rate.append(self.blue_win_times[i] / (self.red_win_times[i] + self.blue_win_times[i])*100)
        # fig5 = plt.figure()
        # fig5.suptitle("The win rate of both sides")
        #
        # ax1 = plt.subplot(111)
        #
        # ax1.plot(range(self.first_half_episodes), red_win_rate[0:self.first_half_episodes], 'r', label='red')
        # ax1.plot(range(self.first_half_episodes), blue_win_rate[0:self.first_half_episodes], '--b', label='blue')
        # plt.legend()
        #
        # plt.xlabel("Episodes")
        # plt.ylabel("Percentage")
        # plt.savefig('win_rate.jpg', dpi=300)
        # # 将字典转换为数据帧
        # df = pd.DataFrame(red_win_rate[0:self.first_half_episodes])
        # # 将数据帧保存到Excel文件
        # df.to_excel('win_rate.xlsx', index=False)

if __name__ == '__main__':
    test = ResultVisualization(10, 10)
    test.output()
