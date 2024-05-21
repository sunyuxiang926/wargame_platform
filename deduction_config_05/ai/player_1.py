import tensorflow as tf
import numpy as np
import random
# import tensorflow
NAME = '钟山智狼'

np.random.seed(2)
tf.set_random_seed(2)

# GAMMA = 0.9
# LR_A = 0.001
# LR_C = 0.01
# N_A = 6
# N_S = 4

class DeepQNetwork(object):
    def __init__(
            self,sess,
            n_actions,
            n_features,
            learning_rate=0.1,
            reward_decay=1,
            e_greedy=0.8,
            replace_target_iter=300,
            memory_size=500,
            batch_size=32,
            e_greedy_increment=None,
            output_graph=False,
    ):
        self.sess = sess
        self.n_actions = n_actions
        self.n_features = n_features
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon_max = e_greedy
        self.replace_target_iter = replace_target_iter
        self.memory_size = memory_size
        self.batch_size = batch_size
        self.epsilon_increment = e_greedy_increment
        self.epsilon = 0 if e_greedy_increment is not None else self.epsilon_max

        # total learning step
        self.learn_step_counter = 0

        # initialize zero memory [s, a, r, s_]
        self.memory = np.zeros((self.memory_size, n_features * 2 + 2))

        # consist of [target_net, evaluate_net]
        self._build_net()
        t_params = tf.get_collection('target_net_params')
        e_params = tf.get_collection('eval_net_params')
        self.replace_target_op = [tf.assign(t, e) for t, e in zip(t_params, e_params)]

        self.sess = tf.Session()

        if output_graph:
            # $ tensorboard --logdir=logs
            # tf.train.SummaryWriter soon be deprecated, use following
            tf.summary.FileWriter("logs/", self.sess.graph)

        self.sess.run(tf.global_variables_initializer())
        self.cost_his = []

    def _build_net(self):
        # ------------------ build evaluate_net ------------------
        self.s = tf.placeholder(tf.float32, [None, self.n_features], name='s')  # input
        self.q_target = tf.placeholder(tf.float32, [None, self.n_actions], name='Q_target')  # for calculating loss
        with tf.variable_scope('eval_net'):
            # c_names(collections_names) are the collections to store variables
            c_names, n_l1, w_initializer, b_initializer = \
                ['eval_net_params', tf.GraphKeys.GLOBAL_VARIABLES], 10, \
                tf.random_normal_initializer(0., 0.3), tf.constant_initializer(0.1)  # config of layers

            # first layer. collections is used later when assign to target net
            with tf.variable_scope('l1'):
                w1 = tf.get_variable('w1', [self.n_features, n_l1], initializer=w_initializer, collections=c_names)
                b1 = tf.get_variable('b1', [1, n_l1], initializer=b_initializer, collections=c_names)
                l1 = tf.nn.relu(tf.matmul(self.s, w1) + b1)

            # second layer. collections is used later when assign to target net
            with tf.variable_scope('l2'):
                w2 = tf.get_variable('w2', [n_l1, self.n_actions], initializer=w_initializer, collections=c_names)
                b2 = tf.get_variable('b2', [1, self.n_actions], initializer=b_initializer, collections=c_names)
                self.q_eval = tf.matmul(l1, w2) + b2

        with tf.variable_scope('loss'):
            self.loss = tf.reduce_mean(tf.squared_difference(self.q_target, self.q_eval))
        with tf.variable_scope('train'):
            self._train_op = tf.train.RMSPropOptimizer(self.lr).minimize(self.loss)

        # ------------------ build target_net ------------------
        self.s_ = tf.placeholder(tf.float32, [None, self.n_features], name='s_')    # input
        with tf.variable_scope('target_net'):
            # c_names(collections_names) are the collections to store variables
            c_names = ['target_net_params', tf.GraphKeys.GLOBAL_VARIABLES]

            # first layer. collections is used later when assign to target net
            with tf.variable_scope('l1'):
                w1 = tf.get_variable('w1', [self.n_features, n_l1], initializer=w_initializer, collections=c_names)
                b1 = tf.get_variable('b1', [1, n_l1], initializer=b_initializer, collections=c_names)
                l1 = tf.nn.relu(tf.matmul(self.s_, w1) + b1)

            # second layer. collections is used later when assign to target net
            with tf.variable_scope('l2'):
                w2 = tf.get_variable('w2', [n_l1, self.n_actions], initializer=w_initializer, collections=c_names)
                b2 = tf.get_variable('b2', [1, self.n_actions], initializer=b_initializer, collections=c_names)
                self.q_next = tf.matmul(l1, w2) + b2

    def store_transition(self, s, a, r, s_):
        if not hasattr(self, 'memory_counter'):
            self.memory_counter = 0

        transition = np.hstack((s, [a, r], s_))

        # replace the old memory with new memory
        index = self.memory_counter % self.memory_size
        self.memory[index, :] = transition

        self.memory_counter += 1

    def choose_action(self, observation):
        # to have batch dimension when feed into tf placeholder
        observation = observation[np.newaxis, :]

        if np.random.uniform() < self.epsilon:
            # forward feed the observation and get q value for every actions
            actions_value = self.sess.run(self.q_eval, feed_dict={self.s: observation})
            action = np.argmax(actions_value)
        else:
            action = np.random.randint(0, self.n_actions)
        return action

    def learn(self):
        # check to replace target parameters
        if self.learn_step_counter % self.replace_target_iter == 0:
            self.sess.run(self.replace_target_op)
            print('\ntarget_params_replaced\n')

        # sample batch memory from all memory
        if self.memory_counter > self.memory_size:
            sample_index = np.random.choice(self.memory_size, size=self.batch_size)
        else:
            sample_index = np.random.choice(self.memory_counter, size=self.batch_size)
        batch_memory = self.memory[sample_index, :]

        q_next, q_eval = self.sess.run(
            [self.q_next, self.q_eval],
            feed_dict={
                self.s_: batch_memory[:, -self.n_features:],  # fixed params
                self.s: batch_memory[:, :self.n_features],  # newest params
            })

        # change q_target w.r.t q_eval's action
        q_target = q_eval.copy()

        batch_index = np.arange(self.batch_size, dtype=np.int32)
        eval_act_index = batch_memory[:, self.n_features].astype(int)
        reward = batch_memory[:, self.n_features + 1]

        q_target[batch_index, eval_act_index] = reward + self.gamma * np.max(q_next, axis=1)

        """
        For example in this batch I have 2 samples and 3 actions:
        q_eval =
        [[1, 2, 3],
         [4, 5, 6]]
        q_target = q_eval =
        [[1, 2, 3],
         [4, 5, 6]]
        Then change q_target with the real q_target value w.r.t the q_eval's action.
        For example in:
            sample 0, I took action 0, and the max q_target value is -1;
            sample 1, I took action 2, and the max q_target value is -2:
        q_target =
        [[-1, 2, 3],
         [4, 5, -2]]
        So the (q_target - q_eval) becomes:
        [[(-1)-(1), 0, 0],
         [0, 0, (-2)-(6)]]
        We then backpropagate this error w.r.t the corresponding action to network,
        leave other action as error=0 cause we didn't choose it.
        """

        # train eval network
        _, self.cost = self.sess.run([self._train_op, self.loss],
                                     feed_dict={self.s: batch_memory[:, :self.n_features],
                                                self.q_target: q_target})
        self.cost_his.append(self.cost)

        # increasing epsilon
        self.epsilon = self.epsilon + self.epsilon_increment if self.epsilon < self.epsilon_max else self.epsilon_max
        self.learn_step_counter += 1

    def plot_cost(self):
        import matplotlib.pyplot as plt
        plt.plot(np.arange(len(self.cost_his)), self.cost_his)
        plt.ylabel('Cost')
        plt.xlabel('training steps')
        plt.show()



def get_state(wargame):
    state = np.array([wargame.scenario.red_tank_1.co_x,
                     wargame.scenario.red_tank_1.co_y,
                     wargame.scenario.red_tank_1.goal[0],
                     wargame.scenario.red_tank_1.goal[1]
                        ])

    return state

def replace_action(num, wargame):
    s_x = wargame.scenario.red_tank_1.co_x
    s_y = wargame.scenario.red_tank_1.co_y
    s_x_ = wargame.scenario.red_tank_2.co_x
    s_y_ = wargame.scenario.red_tank_2.co_y
    e_x = wargame.scenario.blue_tank_1.co_x
    e_y = wargame.scenario.blue_tank_1.co_y
    e_x_ = wargame.scenario.blue_tank_2.co_x
    e_y_ = wargame.scenario.blue_tank_2.co_y

    site_neighbour_1 = wargame.game_map.get_neighbour(s_x, s_y)
    site_neighbour_2 = wargame.game_map.get_neighbour(s_x_, s_y_)
    tank1 = wargame.scenario.red_tank_1
    tank2 = wargame.scenario.red_tank_2
    enermy1 = wargame.scenario.blue_tank_1
    enermy2 = wargame.scenario.blue_tank_2

    if wargame.game_map.visibility_estimation(s_x,s_y,e_x,e_y) or wargame.game_map.visibility_estimation(s_x_,s_y_,e_x,e_y):
        tank1.direct_fire(enermy1)
        tank2.direct_fire(enermy1)
    elif wargame.game_map.visibility_estimation(s_x,s_y,e_x_,e_y_) or wargame.game_map.visibility_estimation(s_x_,s_y_,e_x_,e_y_):
        tank1.direct_fire(enermy2)
        tank2.direct_fire(enermy2)
    elif s_y >= 7 and s_y <= 17:
        tank1.move_one_step(site_neighbour_1[1][0], site_neighbour_1[1][1])
        tank2.move_one_step(site_neighbour_2[1][0], site_neighbour_2[1][1])
    elif num == 0 and 11 <= site_neighbour_1[0][0] <= 25 and 5 <= site_neighbour_1[0][1] <= 43:
        tank1.move_one_step(site_neighbour_1[0][0], site_neighbour_1[0][1])
        tank2.move_one_step(site_neighbour_2[0][0], site_neighbour_2[0][1])
    elif num == 1 and 11 <= site_neighbour_1[1][0] <= 25 and 5 <= site_neighbour_1[1][1] <= 43:
        tank1.move_one_step(site_neighbour_1[1][0], site_neighbour_1[1][1])
        tank2.move_one_step(site_neighbour_2[1][0], site_neighbour_2[1][1])
    elif num == 2 and 11 <= site_neighbour_1[2][0] <= 25 and 5 <= site_neighbour_1[2][1] <= 43:
        tank1.move_one_step(site_neighbour_1[2][0], site_neighbour_1[2][1])
        tank2.move_one_step(site_neighbour_2[2][0], site_neighbour_2[2][1])
    elif num == 3 and 11 <= site_neighbour_1[3][0] <= 25 and 5 <= site_neighbour_1[3][1] <= 43:
        tank1.move_one_step(site_neighbour_1[3][0], site_neighbour_1[3][1])
        tank2.move_one_step(site_neighbour_2[3][0], site_neighbour_2[3][1])
    elif num == 4 and 11 <= site_neighbour_1[4][0] <= 25 and 5 <= site_neighbour_1[4][1] <= 43:
        tank1.move_one_step(site_neighbour_1[4][0], site_neighbour_1[4][1])
        tank2.move_one_step(site_neighbour_2[4][0], site_neighbour_2[4][1])
    elif num == 5 and 11 <= site_neighbour_1[5][0] <= 25 and 5 <= site_neighbour_1[5][1] <= 43:
        tank1.move_one_step(site_neighbour_1[5][0], site_neighbour_1[5][1])
        tank2.move_one_step(site_neighbour_2[5][0], site_neighbour_2[5][1])

sess = tf.Session()
actor = DeepQNetwork(sess, 6, 4,)
saver = tf.train.Saver()
# saver.restore(sess, 'model/train-15000')

def red_choose_action(wargame):
    s = get_state(wargame)
    num = actor.choose_action(s)
    replace_action(num, wargame)


# def red_choose_action(wargame):
#     tank_1 = wargame.scenario.red_tank_1
#     tank_2 = wargame.scenario.red_tank_2
#     e_tank_1 = wargame.scenario.blue_tank_1
#     e_tank_2 = wargame.scenario.blue_tank_2
#     neighbours1 = wargame.game_map.get_neighbour(tank_1.co_x, tank_1.co_y)
#     neighbours2 = wargame.game_map.get_neighbour(tank_2.co_x, tank_2.co_y)
#
#     # -------Tank1 AI-------
#     d1 = {}
#     for neighbour in neighbours1:
#         if neighbour not in tank_1.move_history:
#
#             d1[neighbour] = tank_1.wargame_env.game_map.get_distance_between_hex(tank_1.goal[0], tank_1.goal[1],neighbour[0], neighbour[1])
#     d_neighbour1 = min(d1, key=d1.get)
#
#     n = random.random()
#     print('A1 n=',n)
#     if n < 0.2:
#         action = tank_1.actions[7]
#         tank_1.change_to_fire_state()
#         fire_result = tank_1.direct_fire(e_tank_1)
#     elif n < 0.4:
#         action = tank_1.actions[8]
#         tank_1.indirect_fire(15,35)
#     elif n < 0.9:
#         action = tank_1.actions[6]
#         tank_1.change_to_hide_state()
#
#     else:
#         tank_1.move_one_step(d_neighbour1[0], d_neighbour1[1])
#         print('B1 dMove_to:', d_neighbour1[0], d_neighbour1[1])
#
#     # -------Tank2 AI-------
#
#     d2 = {}
#     for neighbour in neighbours2:
#         if neighbour not in tank_2.move_history:
#             d2[neighbour] = tank_2.wargame_env.game_map.get_distance_between_hex(tank_2.goal[0], tank_2.goal[1],
#                                                                                  neighbour[0], neighbour[1])
#     d_neighbour2 = min(d2, key=d2.get)
#
#     n = random.random()
#     print('A2 n=', n)
#     if n < 0.5:
#         action = tank_2.actions[7]
#         fire_result = tank_2.direct_fire(e_tank_2)
#     elif n < 0.7:
#         action = tank_2.actions[8]
#         tank_2.indirect_fire(15,33)
#     elif n < 0.8:
#         action = tank_2.actions[6]
#         tank_2.change_to_hide_state()
#
#     else:
#         tank_2.move_one_step(d_neighbour2[0], d_neighbour2[1])
#         print('B2 Move_to:', d_neighbour2[0], d_neighbour2[1])
#
#     return
#
# def blue_choose_action(wargame):
#     tank_1 = wargame.scenario.blue_tank_1
#     tank_2 = wargame.scenario.blue_tank_2
#     e_tank_1 = wargame.scenario.red_tank_1
#     e_tank_2 = wargame.scenario.red_tank_2
#     neighbours1 = wargame.game_map.get_neighbour(tank_1.co_x, tank_1.co_y)
#     neighbours2 = wargame.game_map.get_neighbour(tank_2.co_x, tank_2.co_y)
#
#     # -------Tank1 AI-------
#     d1 = {}
#     for neighbour in neighbours1:
#         if neighbour not in tank_1.move_history:
#             d1[neighbour] = tank_1.wargame_env.game_map.get_distance_between_hex(tank_1.goal[0], tank_1.goal[1],
#                                                                                  neighbour[0], neighbour[1])
#     d_neighbour1 = min(d1, key=d1.get)
#
#     n = random.random()
#     print('B1 n=', n)
#     if n < 0.2:
#         action = tank_1.actions[7]
#         tank_1.change_to_fire_state()
#         fire_result = tank_1.direct_fire(e_tank_1)
#     elif n < 0.4:
#         action = tank_1.actions[8]
#         tank_1.indirect_fire(17, 7)
#     elif n < 0.9:
#         action = tank_1.actions[6]
#         tank_1.change_to_hide_state()
#
#     else:
#         tank_1.move_one_step(d_neighbour1[0], d_neighbour1[1])
#         print('B1 dMove_to:', d_neighbour1[0], d_neighbour1[1])
#
#     # -------Tank2 AI-------
#
#     d2 = {}
#     for neighbour in neighbours2:
#         if neighbour not in tank_2.move_history:
#             d2[neighbour] = tank_2.wargame_env.game_map.get_distance_between_hex(tank_2.goal[0], tank_2.goal[1],
#                                                                                  neighbour[0], neighbour[1])
#     d_neighbour2 = min(d2, key=d2.get)
#
#     n = random.random()
#     print('B2 n=', n)
#     if n < 0.5:
#         action = tank_2.actions[7]
#         fire_result = tank_2.direct_fire(e_tank_2)
#     elif n < 0.7:
#         action = tank_2.actions[8]
#         tank_2.indirect_fire(17, 7)
#     elif n < 0.8:
#         action = tank_2.actions[6]
#         tank_2.change_to_hide_state()
#
#     else:
#         tank_2.move_one_step(d_neighbour2[0], d_neighbour2[1])
#         print('B2 Move_to:', d_neighbour2[0], d_neighbour2[1])
#
#     return

