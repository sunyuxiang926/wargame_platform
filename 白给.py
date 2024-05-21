import tensorflow as tf
import numpy as np

NAME = '白给'

GAMMA = 0.8
A_LR = 0.0003
C_LR = 0.0009
BATCH = 32
A_UPDATE_STEPS = 10
UPDATE_STEPS = 10
S_DIM = 4
A_DIM = 6

METHOD = [
    dict(name='kl_pen', kl_target=0.01, lam=0.5),   # KL penalty
    dict(name='clip', epsilon=0.2),                 # Clipped surrogate objective, find this is better
][1]        # choose the method for optimization

def get_state(wargame, tank):
    state = []
    # red_tank1 = wargame.scenario.red_tank_1
    state.append(tank.co_x)
    state.append(tank.co_y)
    state.append(tank.goal[0])
    state.append(tank.goal[1])
    return np.array(state)


def get_war_state(wargame):
    state = {}
    red_tank1 = wargame.scenario.red_tank_1
    red_tank2 = wargame.scenario.red_tank_2
    blue_tank1 = wargame.scenario.blue_tank_1
    blue_tank2 = wargame.scenario.blue_tank_2
    # state.append(wargame.rounds)                        # 回合数
    state['r1x'] = red_tank1.co_x  # 当前坦克坐标
    state['r1y'] = red_tank1.co_y  #
    state['r1n'] = red_tank1.get_piece_state()[2]  # 当前坦克血量
    state['r1gx'] = red_tank1.goal[0]  # 当前坦克目标点
    state['r1gy'] = red_tank1.goal[1]
    state['r2x'] = red_tank2.co_x
    state['r2y'] = red_tank2.co_y
    state['r2n'] = red_tank2.get_piece_state()[2]
    state['r2gx'] = red_tank2.goal[0]
    state['r2gy'] = red_tank2.goal[1]
    state['e1x'] = blue_tank1.co_x  # 敌方坦克1坐标
    state['e1y'] = blue_tank1.co_y
    state['e1n'] = blue_tank1.get_piece_state()[2]  # 敌方坦克1血量
    state['r1see1'] = red_tank1.check_watch(blue_tank1)  # 是否可以看到敌方坦克1
    state['r2see1'] = red_tank2.check_watch(blue_tank1)
    state['e2x'] = blue_tank2.co_x  # 敌方坦克2坐标
    state['e2y'] = blue_tank2.co_y
    state['e2n'] = blue_tank2.get_piece_state()[2]  # 敌方坦克2血量
    state['r1see2'] = red_tank1.check_watch(blue_tank2)  # 是否可以看到敌方坦克2
    state['r2see2'] = red_tank2.check_watch(blue_tank2)

    return state

def get_war_stateb(wargame):
    state = {}
    red_tank1 = wargame.scenario.red_tank_1
    red_tank2 = wargame.scenario.red_tank_2
    blue_tank1 = wargame.scenario.blue_tank_1
    blue_tank2 = wargame.scenario.blue_tank_2
    # state.append(wargame.rounds)                        # 回合数
    # state['r1x'] = red_tank1.co_x  # 当前坦克坐标
    # state['r1y'] = red_tank1.co_y  #
    state['b1n'] = blue_tank1.get_piece_state()[2]  # 当前坦克血量
    # state['r1gx'] = red_tank1.goal[0]  # 当前坦克目标点
    # state['r1gy'] = red_tank1.goal[1]
    # state['r2x'] = red_tank2.co_x
    # state['r2y'] = red_tank2.co_y
    state['b2n'] = blue_tank2.get_piece_state()[2]
    # state['r2gx'] = red_tank2.goal[0]
    # state['r2gy'] = red_tank2.goal[1]
    # state['e1x'] = blue_tank1.co_x  # 敌方坦克1坐标
    # state['e1y'] = blue_tank1.co_y
    state['e1n'] = red_tank1.get_piece_state()[2]  # 敌方坦克1血量
    state['b1see1'] = blue_tank1.check_watch(red_tank1)  # 是否可以看到敌方坦克1
    state['b2see1'] = blue_tank2.check_watch(red_tank1)
    state['e2n'] = red_tank2.get_piece_state()[2]  # 敌方坦克2血量
    state['b1see2'] = blue_tank1.check_watch(red_tank2)  # 是否可以看到敌方坦克2
    state['b2see2'] = blue_tank2.check_watch(red_tank2)

    return state

def replace_action(wargame, tank, num):
    # tank = wargame.scenario.red_tank_1
    neighbor = wargame.game_map.get_neighbour(tank.co_x, tank.co_y)
    if num == 0:
        tank.move_one_step(neighbor[0][0], neighbor[0][1])
    elif num == 1:
        tank.move_one_step(neighbor[1][0], neighbor[1][1])
    elif num == 2:
        tank.move_one_step(neighbor[2][0], neighbor[2][1])
    elif num == 3:
        tank.move_one_step(neighbor[3][0], neighbor[3][1])
    elif num == 4:
        tank.move_one_step(neighbor[4][0], neighbor[4][1])
    elif num == 5:
        tank.move_one_step(neighbor[5][0], neighbor[5][1])
    elif num == 6:
        tank.direct_fire(wargame.scenario.blue_tank_1)
    elif num == 7:
        tank.direct_fire(wargame.scenario.blue_tank_2)

def replace_actionb(wargame, tank, num):
    # tank = wargame.scenario.red_tank_1
    neighbor = wargame.game_map.get_neighbour(tank.co_x, tank.co_y)
    if num == 0:
        tank.move_one_step(neighbor[0][0], neighbor[0][1])
    elif num == 1:
        tank.move_one_step(neighbor[1][0], neighbor[1][1])
    elif num == 2:
        tank.move_one_step(neighbor[2][0], neighbor[2][1])
    elif num == 3:
        tank.move_one_step(neighbor[3][0], neighbor[3][1])
    elif num == 4:
        tank.move_one_step(neighbor[4][0], neighbor[4][1])
    elif num == 5:
        tank.move_one_step(neighbor[5][0], neighbor[5][1])
    elif num == 6:
        tank.direct_fire(wargame.scenario.red_tank_1)
    elif num == 7:
        tank.direct_fire(wargame.scenario.red_tank_2)

class PPO(object):
    def __init__(self):
        self.sess = tf.Session()
        self.tfs = tf.placeholder(tf.float32, [None, S_DIM], 'state')

        # critic
        # with tf.variable_scope('critic'):
        w_init = tf.random_normal_initializer(0., .1)
        l1 = tf.layers.dense(self.tfs, 100, tf.nn.relu, kernel_initializer=w_init, name='lc')
        # l2 = tf.layers.dense(l1, 50, tf.nn.relu)
        self.v = tf.layers.dense(l1, 1)
        self.tfdc_r = tf.placeholder(tf.float32, [None, 1], name='discounted_r')
        self.advantage = self.tfdc_r - self.v
        closs = tf.reduce_mean(tf.square(self.advantage))
        self.ctrain = tf.train.AdamOptimizer(C_LR, epsilon=1e-5).minimize(closs)

        # actor
        self.pi, pi_params = self._build_anet('pi', trainable=True)
        oldpi, oldpi_params = self._build_anet('oldpi', trainable=False)
        self.update_oldpi_op = [oldp.assign(p) for p, oldp in zip(pi_params, oldpi_params)]

        # loss
        self.tfa = tf.placeholder(tf.int32, [None, ], 'action')
        self.tfadv = tf.placeholder(tf.float32, [None, 1], 'advantage')
        # with tf.variable_scope('loss'):
        a_indices = tf.stack([tf.range(tf.shape(self.tfa)[0], dtype=tf.int32), self.tfa], axis=1)
        pi_prob = tf.gather_nd(params=self.pi, indices=a_indices)   # shape=(None, )
        oldpi_prob = tf.gather_nd(params=oldpi, indices=a_indices)  # shape=(None, )
        with tf.variable_scope('surrogate'):
            # ratio = tf.divide(pi.prob(self.tfa), tf.maximum(oldpi.prob(self.tfa), 1e-5))
            # ratio = pi.prob(self.tfa) / oldpi.prob(self.tfa)
            ratio = tf.divide(pi_prob, tf.maximum(oldpi_prob, 1e-5))
            surr = ratio * self.tfadv                       # surrogate loss
            # if METHOD['name'] == 'kl_pen':
            #     self.tflam = tf.placeholder(tf.float32, None, 'lambda')
            #     kl = tf.distributions.kl_divergence(oldpi, self.pi)
            #     self.kl_mean = tf.reduce_mean(kl)
            #     self.aloss = -(tf.reduce_mean(surr - self.tflam * kl))
            # else:
            self.aloss = -tf.reduce_mean(tf.minimum(
                surr,
                tf.clip_by_value(ratio, 1.-METHOD['epsilon'], 1.+METHOD['epsilon'])*self.tfadv))

        # actor train
        # with tf.variable_scope('atrain'):
        self.atrain_op = tf.train.AdamOptimizer(A_LR, epsilon=1e-5).minimize(self.aloss)

        self.saver = tf.train.Saver()
        # tf.summary.FileWriter("log/", self.sess.graph)
        self.sess.run(tf.global_variables_initializer())

    def _build_anet(self, name, trainable):
        with tf.variable_scope(name):
            l_a = tf.layers.dense(self.tfs, 200, tf.nn.relu, kernel_initializer=tf.random_normal_initializer(0., .1),
                                  trainable=trainable)
            # l_b = tf.layers.dense(l_a, 100, tf.nn.relu, kernel_initializer=tf.random_normal_initializer(0., .1),
            #                       trainable=trainable)
            a_prob = tf.layers.dense(l_a, A_DIM, tf.nn.softmax, trainable=trainable)
        params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope=name)
        return a_prob, params

    def choose_action(self, s):
        prob_weights = self.sess.run(self.pi, feed_dict={self.tfs: s[None, :]})
        action = np.random.choice(range(prob_weights.shape[1]),
                                      p=prob_weights.ravel())  # select action w.r.t the actions prob
        return action

    def load_model(self, path):
        self.saver.restore(self.sess, path)

def red_choose_action(wargame):
    tf.reset_default_graph()
    ppor = PPO()
    last_ckpt = tf.train.latest_checkpoint('./models/r/')
    ppor.load_model(last_ckpt)
    war_state = get_war_stateb(wargame)
    # tank 1 主要往目标点进行移动
    tank1 = wargame.scenario.red_tank_1
    state = get_state(wargame, tank1)
    if war_state['b1see1'] and war_state['b1n'] != 0:
        num = 6
        tank1.change_to_fire_state()
    elif war_state['b2see1'] and war_state['b2n'] != 0:
        num = 7
        tank1.change_to_fire_state()
    else:
        num = ppor.choose_action(state)
    replace_action(wargame, tank1, num)

    # tank 2 主要做攻击掩护动作r
    tank2 = wargame.scenario.red_tank_2
    state = get_state(wargame, tank2)
    # if war_state['b1see2'] and war_state['b1n'] != 0:
    #     num = 6
    #     tank2.change_to_fire_state()
    # elif war_state['b2see2'] and war_state['b2n'] != 0:
    #     num = 7
    #     tank2.change_to_fire_state()
    # else:
    #     num = ppor.choose_action(state)
    num = ppor.choose_action(state)
    replace_action(wargame, tank2, num)
    # pass


def blue_choose_action(wargame):
    tf.reset_default_graph()
    ppob = PPO()
    last_ckpt1 = tf.train.latest_checkpoint('./models/b/')
    ppob.load_model(last_ckpt1)
    war_state = get_war_stateb(wargame)
    # tank 1 主要往目标点进行移动
    tank1 = wargame.scenario.blue_tank_1
    state = get_state(wargame, tank1)
    if war_state['b1see1'] and war_state['e1n'] != 0:
        num = 6
        tank1.change_to_fire_state()
    elif war_state['b1see2'] and war_state['e2n'] != 0:
        num = 7
        tank1.change_to_fire_state()
    else:
        num = ppob.choose_action(state)
    # num = ppob.choose_action(state)
    replace_actionb(wargame, tank1, num)

    # tank 2 主要做攻击掩护动作
    tank2 = wargame.scenario.blue_tank_2
    state = get_state(wargame, tank2)
    if war_state['b2see1'] and war_state['e1n'] != 0:
        num = 6
        tank2.change_to_fire_state()
    elif war_state['b2see2'] and war_state['e2n'] != 0:
        num = 7
        tank2.change_to_fire_state()
    else:
        num = ppob.choose_action(state)
    # num = ppob.choose_action(state)
    replace_actionb(wargame, tank2, num)
    # pass
