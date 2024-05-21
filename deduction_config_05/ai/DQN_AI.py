import gym
import tensorflow as tf
import numpy as np
import random
from collections import deque

# Hyper Parameters

ENV_NAME = 'Wargame_想定一'
EPISODE = 10000 # Episode limitation
STEP = 300 # Step limitation in an episode
TEST = 10 # The number of experiment test every 100 episode

def main():
  # initialize OpenAI Gym env and dqn agent
  env = gym.make(ENV_NAME)
  agent = DQN(env)

  for episode in range(EPISODE):
    # initialize task
    state = env.reset()
    # Train
    for step in range(STEP):
      action = agent.egreedy_action(state) # e-greedy action for train
      next_state,reward,done,_ = env.step(action)
      # Define reward for agent
      reward_agent = -1 if done else 0.1
      agent.perceive(state,action,reward,next_state,done)
      state = next_state
      if done:
        break

# Test every 100 episodes
    if episode % 100 == 0:#第100、200、300...
      total_reward = 0
      for i in range(TEST):#每10个episodes，进行一次平均奖赏值的计算
        state = env.reset()
        for j in range(STEP):#一个episodes中内部step:300步
          env.render()#更新环境中的Agent内部神经网络结构
          action = agent.action(state) # direct action for test，直接依据训训的Agent来选择动作
          state,reward,done,_ = env.step(action)#切换下一个动作
          total_reward += reward
          if done:
            break
      ave_reward = total_reward/TEST
      print("episode:%s,Evaluation Average Reward:%s"%(episode,ave_reward))

      #如果平均奖赏足够大，就不需要训练
      if ave_reward >= 200:
        break

if __name__ == '__main__':
    main()

# Hyper Parameters for DQN（DQN算法的“超参数”）
GAMMA = 0.9 # discount factor for target Q
INITIAL_EPSILON = 0.5 # starting value of epsilon
FINAL_EPSILON = 0.01 # final value of epsilon
REPLAY_SIZE = 10000 # experience replay buffer size
BATCH_SIZE = 32 # size of minibatch

class DQN():
  # DQN Agent
  def __init__(self, env): #初始化，每次执行对象实例时，实例该函数一次
      # init experience replay
      self.replay_buffer = deque()#类似于list列表数组，支持两端操作
      # init some parameters
      self.time_step = 0
      self.epsilon = INITIAL_EPSILON
      self.state_dim = env.observation_space.shape[0]#输入的多维状态向量
      self.action_dim = env.action_space.n #动作空间的维度

      self.create_Q_network() #初始化时，创建Q网
      self.create_training_method()

      # Init session,相当于一个主对象
      self.session = tf.InteractiveSession()
      self.session.run(tf.initialize_all_variables())#添加一个操作，对变量做初始化

  def create_Q_network(self): #创建Q网络
      # network weights
      W1 = self.weight_variable([self.state_dim, 20])#调用内置函数
      b1 = self.bias_variable([20])
      W2 = self.weight_variable([20, self.action_dim])
      b2 = self.bias_variable([self.action_dim])
      # input layer
      self.state_input = tf.placeholder("float", [None, self.state_dim])
      # hidden layers
      h_layer = tf.nn.relu(tf.matmul(self.state_input, W1) + b1)
      # Q Value layer，output layer,输出层
      self.Q_value = tf.matmul(h_layer, W2) + b2   # 拟合的输出值：f(x) = W2x + b2

  # 定义一个函数，用于初始化所有的权值 W
  def weight_variable(self, shape):
      initial = tf.truncated_normal(shape)
      return tf.Variable(initial)

  # 定义一个函数，用于初始化所有的偏置项 b
  def bias_variable(self, shape):
      initial = tf.constant(0.01, shape=shape)
      return tf.Variable(initial)

  def create_training_method(self): #创建训练方法
      self.action_input = tf.placeholder("float", [None, self.action_dim])  # one hot presentation
      self.y_input = tf.placeholder("float", [None]) #实际环境产生的数据
      #沿着的tensor维度求和
      #tf里面的tensor就是一个多维数组，所以reduce sum就是压缩这个数组，这就像把一个立方体压成平
      #这些操作的本质就是降维，以xxx的手段降维
      Q_action = tf.reduce_sum(tf.mul(self.Q_value, self.action_input), reduction_indices=1)
      #Computes the mean of elements across dimensions of a tensor.
      #计算列表各元素的平方和的均值
      self.cost = tf.reduce_mean(tf.square(self.y_input - Q_action)) #成本函数或称损失函数
      #此函数是Adam优化算法：是一个寻找全局最优点的优化算法，引入了二次方梯度校正
      self.optimizer = tf.train.AdamOptimizer(0.0001).minimize(self.cost)

  def perceive(self,state,action,reward,next_state,done): #感知存储信息
      one_hot_action = np.zeros(self.action_dim) #返回来一个给定形状和类型的用0填充的数组
      one_hot_action[action] = 1
      self.replay_buffer.append((state, one_hot_action, reward, next_state, done))

      if len(self.replay_buffer) > REPLAY_SIZE:
          self.replay_buffer.popleft()

      if len(self.replay_buffer) > BATCH_SIZE:
          self.train_Q_network() #取相应样例数据，进行DQN训练

  def train_Q_network(self): #训练网络
      self.time_step += 1
      # Step 1: obtain random minibatch from replay memory
        #从指定的序列中，随机的截取指定长度的片断，不作原地修改
      minibatch = random.sample(self.replay_buffer, BATCH_SIZE)
      #data是一个由4列元素组成的多行二维列表数组，序列[[data[0],[data[1],[data[2],[data[3]],.....]
      state_batch = [data[0] for data in minibatch]
      action_batch = [data[1] for data in minibatch]
      reward_batch = [data[2] for data in minibatch]
      next_state_batch = [data[3] for data in minibatch]

      # Step 2: calculate y
      y_batch = []
      Q_value_batch = self.Q_value.eval(feed_dict={self.state_input: next_state_batch})
      for i in range(0, BATCH_SIZE):
          done = minibatch[i][4]
          if done:
              y_batch.append(reward_batch[i])
          else:
              y_batch.append(reward_batch[i] + GAMMA * np.max(Q_value_batch[i]))

      self.optimizer.run(feed_dict={
          self.y_input: y_batch,
          self.action_input: action_batch,
          self.state_input: state_batch
      })

  def egreedy_action(self, state):  # 输出带随机的动作
      Q_value = self.Q_value.eval(feed_dict={
          self.state_input: [state]
      })[0]
      if random.random() <= self.epsilon:
          return random.randint(0, self.action_dim - 1)
      else:
          return np.argmax(Q_value)
      self.epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / 10000


  def action(self,state): #输出动作
      return np.argmax(self.Q_value.eval
                           (feed_dict={self.state_input: [state]})[0])