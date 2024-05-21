import pandas as pd
class data_rule():
    '''
    scenario:想定
    terrain:地形
    数据知识判断的方法：
    1.在推演前开始调用data_pre_processing处理数据（前提是要提前获得数据）evaluation_decision产生序贯路径决策
    2.在推演中，每回合调用rule系列函数判断，返回决策（优先使用规则路径）
    '''
    def __init__(self, scenario,terrain):
        self.scenario=scenario
        self.terrain=terrain
    '''
    获取六角格的ID号，如果每个六角格有ID号,需要此功能函数找到每次移动后的ID
    init_position:初始的ID
    oddeven：奇数偶数标志位。1：奇数。-1：偶数
    move：移动方向。（0-6），1为东边六角格方向，而后逆时针旋转依次为2-6，0不动
    '''
    def get_positionID(self,init_position,oddeven,move):
        init_po = init_position
        #不跨行移动
        if move == 1:
            init_po = init_po + 1
        elif move == 4:
            init_po = init_po - 1
        #跨行移动分奇偶，具体每跨一行的ID变化多少依据实际情况，下面代码只是示例
        else:
            if oddeven == 1:
                if move == 2:
                    init_po = init_po + 100
                if move == 3:
                    init_po = init_po + 99
                if move == 5:
                    init_po = init_po - 101
                if move == 6:
                    init_po = init_po - 100
            if oddeven == -1:
                if move == 2:
                    init_po = init_po + 101
                if move == 3:
                    init_po = init_po + 100
                if move == 5:
                    init_po = init_po - 100
                if move == 6:
                    init_po = init_po - 99
        #返回移动后的ID
        return init_po


    '''
    对输入的数据源进行数据处理,注意这里是针对两个算子，而且是已设计的移动数据存储的格式 算子1移动/算子2移动 （523/46）
    如果想定环境和数据改变，如存储移动格式等，代码要相应改变，所以在设计此函数需要自行更改下部分从excel中获取移动数据list（#号标注范围）
    data_source：源数据
    table_name：存在excel表名，函数调用的格式
    final_result:excel中最终推演的胜负结果列名
    total_game:excel局数列名
    red_move：红方移动列名
    init_ID:算子初始位置ID
    oddeven：奇偶标志位传入
    '''
    def data_pre_processing(self,data_source,table_name,final_result,total_game,red_move,init_ID,oddeven):
        frame = pd.read_excel(data_source, sheet_name=table_name)
        s = frame[final_result].tolist()
        num_id = 0
        red_patch_list = []
        blue_patch_list = []
        #统计有多少,蓝方获胜和红方获胜局，并分别统计他们的ID号记录在各自的list中
        for i in s:
            if i=='red win!':
                num_id = num_id + 1
                red_patch_list.append(num_id)
            if i =='blue win':
                num_id = num_id + 1
                blue_patch_list.append(num_id)
        for i in red_patch_list:
            # 取局数为i的推演数据
            patch = frame.loc[frame[total_game] == i]
            # 将移动列转为列表
            move_list = patch[red_move].tolist()
            #--------------------------#
            #需要完善如何精准找到移动列表
            move1=[]
            #--------------------------#
            pass


        red_win_list_0 = []
        red_dict_0 = {}
        init_pos_0 = init_ID
        oddeven_0 = oddeven
        for i in red_patch_list:
            #每一组提取出来的移动列表
            newl1=move1[i]
            for i in newl1:
                red_dict_0[init_pos_0]=i
                init_pos_0=self.self.get_positionID(init_pos_0,oddeven_0,i)
                if i in [2,3,5,6]:
                    oddeven_0=-oddeven_0
            red_win_list_0.append(red_dict_0)
            init_pos_0=init_ID
            red_dict_0 = {}

        #蓝方获胜的操作是一样的
        for i in blue_patch_list:
            # 取局数为i的推演数据
            patch = frame.loc[frame[total_game] == i]
            # 将移动列转为列表
            move_list = patch[red_move].tolist()
            # --------------------------#
            # 需要完善如何精准找到移动列表
            move2 = []
            # --------------------------#
            pass

        blue_win_list_0 = []
        blue_dict_0 = {}
        for i in blue_patch_list:
            #每一组提取出来的移动列表
            newl2 = move2[i]
            for i in newl2:
                blue_dict_0[init_pos_0]=i
                init_pos_0=self.self.get_positionID(init_pos_0,oddeven_0,i)
                if i in [2,3,5,6]:
                    oddeven_0=-oddeven_0
            blue_win_list_0.append(blue_dict_0)
            init_pos_0=init_ID
            blue_dict_0 = {}
        #数据格式：[{1940:4,1840:3,....},{...},{}.......]
        return red_win_list_0,blue_win_list_0

    '''
    评价路径决策函数
    环境是按照初始火力战的环境构建的,所以需要传入想定的数据，在初始化函数中声明了
    lowest_point:地图最低高程
    key_init:算子初始位置
    k_oddeven_0：奇偶标志位，同上
    red_win_list_0：红色方获胜数据信息
    blue_win_list_0:蓝色方获胜数据信息（需要调用上面一个函数实例化后传入）
    '''
    def evaluation_decision(self,lowest_point,key_init,k_oddeven_0,red_win_list_0,blue_win_list_0):
        #阿尔法参数调参过程0.1-0.9
        for g in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
            #势能价值，此处以高程势能作为例子，如果要计算其他高程，则直接加入字典，格式{六角格ID：势能值}
            E_dict = {}
            #获取想定中的六角格信息
            hexagon_group = self.scenario.hex_group
            for i in hexagon_group:
                E_dict[int(i.ID)] = (int(i.elevation) - lowest_point) / 300
            #数据统计，贪心决策
            move_list = []
            result_list_0=[]
            while True:
                num_3=num_4=num_5=num_6== 0
                num_3_lose =num_4_lose =num_5_lose =num_6_lose =0
                #此处未统计未移动的情况，因为没有意义
                for i in red_win_list_0:
                    for key in i:
                        if key == key_init:
                            if i[key]==1:
                                num_1=num_1+1
                            if i[key]==2:
                                num_2=num_2+1
                            if i[key] == 3:
                                num_3 = num_3 + 1
                            if i[key] == 4:
                                num_4 = num_4 + 1
                            if i[key] == 5:
                                num_5 = num_5 + 1
                            if i[key] == 6:
                                num_6 = num_6 + 1
                for i in blue_win_list_0:
                    for key in i:
                        if key == key_init:
                            if i[key]==1:
                                num_1_lose=num_1_lose+1
                            if i[key]==2:
                                num_2_lose=num_2_lose+1
                            if i[key] == 3:
                                num_3_lose = num_3_lose + 1
                            if i[key] == 4:
                                num_4_lose = num_4_lose + 1
                            if i[key] == 5:
                                num_5_lose = num_5_lose + 1
                            if i[key] == 6:
                                num_6_lose = num_6_lose + 1
                total_num = num_3 + num_4 + num_5 + num_6 + num_3_lose + num_4_lose + num_5_lose + num_6_lose
                win_rate_3 =win_rate_4 =win_rate_5 =win_rate_6 = 0
                if num_3 != 0:
                    win_rate_3 = num_3 / (num_3 + num_3_lose)
                if num_4 != 0:
                    win_rate_4 = num_4 / (num_4 + num_4_lose)
                if num_5 != 0:
                    win_rate_5 = num_5 / (num_5 + num_5_lose)
                if num_6 != 0:
                    win_rate_6 = num_6 / (num_6 + num_6_lose)
                #这段不确定是否有用
                key_next = self.self.get_positionID(key_init, k_oddeven_0, 3)
                #定义一个胜率的集合
                rate_dict = {}
                '''
                得分=概率a*(该方向的胜率+节点势能)+(1-概率a)*(该方向的胜率+节点势能)*场数/整场数
                '''
                if E_dict.get(self.self.get_positionID(key_init, k_oddeven_0, 3)) is None:
                    E_dict[self.get_positionID(key_init, k_oddeven_0, 3)] = 0
                rate_dict[3] = g * (win_rate_3 + E_dict[self.get_positionID(key_init, k_oddeven_0, 3)]) * (
                (num_3 + num_3_lose) / total_num) + (1 - g) * (win_rate_3 +E_dict[self.get_positionID(key_init,k_oddeven_0,3)])
                if E_dict.get(self.get_positionID(key_init, k_oddeven_0, 4)) is None:
                    E_dict[self.get_positionID(key_init, k_oddeven_0, 4)] = 0
                rate_dict[4] = g * (win_rate_4 + E_dict[self.get_positionID(key_init, k_oddeven_0, 4)]) * (
                (num_4 + num_4_lose) / total_num) + (1 - g) * (win_rate_4 + E_dict[self.get_positionID(key_init,k_oddeven_0,4)])
                if E_dict.get(self.get_positionID(key_init, k_oddeven_0, 5)) is None:
                    E_dict[self.get_positionID(key_init, k_oddeven_0, 5)] = 0
                rate_dict[5] = g * (win_rate_5 + E_dict[self.get_positionID(key_init, k_oddeven_0, 5)]) * (
                (num_5 + num_5_lose) / total_num) + (1 - g) * (win_rate_5 +E_dict[self.get_positionID(key_init,k_oddeven_0,5)])
                if E_dict.get(self.get_positionID(key_init, k_oddeven_0, 6)) is None:
                    E_dict[self.get_positionID(key_init, k_oddeven_0, 6)] = 0
                rate_dict[6] = g * (win_rate_6 + E_dict[self.get_positionID(key_init, k_oddeven_0, 6)]) * (
                (num_6 + num_6_lose) / total_num) + (1 - g) * (win_rate_6 +E_dict[self.get_positionID(key_init,k_oddeven_0,6)])
                #找到每个节点最优的下一个节点
                move = max(rate_dict, key=rate_dict.get)
                #防止两个位置的得分最高方向互为对方，成为死循环，无法移动。
                if len(move_list) >= 1:
                    if (move_list[-1] == 3 and move == 6) or (move_list[-1] == 6 and move == 3):
                        del rate_dict[move]
                        move = max(rate_dict, key=rate_dict.get)
                #防止出现越界操作，算法无法进行
                if move == 3 and key_init > 1900:
                    del rate_dict[3]
                    move = max(rate_dict, key=rate_dict.get)
                move_list.append(move)
                key_init = self.get_positionID(key_init, k_oddeven_0, move)
                if move in [2, 3, 5, 6]:
                    k_oddeven_0 = -k_oddeven_0
                # 如果到了一个总局数小于10的点，跳出循环，这个值可以改变      1500:35 464:20
                if total_num < 10:
                    break
            #产生一个嵌套列表[[],[],....]内层列表对应相应阿尔法参数的序贯路径决策结果
            result_list_0.append(move_list)

    '''
    规则决策要传入实时的算子状态，依据具体地形，结合实际推演知识编写
    例如：射击规则。自身和敌方算子被压制后等，如何移动。或者更复杂，当敌方算子出现在什么位置，我方算子如何移动。
    此规则模块编写很简单，IF语句是主导，没有循环，关键在认为设计的如何
    pieces_state_group：算子组，每个算子，经过算子类实例化后加入算子组
    '''
    def rule_move(self,pieces_state_group):
        # rule1:移动
        return
        pass
    '''
    :return
    attack_pieces:攻击算子
    defend_pieces被攻击算子
    weapon：武器选择
    （如果多算子，就要返回字典）
    '''
    def rule_shoot(self,pieces_state_group):
        # rule2:射击
        return
        pass
    def rule_position(self,pieces_state_group):
        # rule3:特殊地形规则
        return
        pass







