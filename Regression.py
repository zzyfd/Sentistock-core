import datetime
import tensorflow as tf


class Regression:
    b, w1, w2, w3, w4, w5 = [0, 0, 0, 0, 0, 0]
    list = []
    mark = 0
    init = None

    def __init__(self):
        # construct model : stockpremium = b + w1 * marketpremium + w2*SMB + w3*emotion + w4*HIM + w5*turnover

        # create holder
        self.sp = tf.placeholder(tf.float64)
        self.mp = tf.placeholder(tf.float64)
        self.SMB = tf.placeholder(tf.float64)
        self.HIM = tf.placeholder(tf.float64)
        self.turnover = tf.placeholder(tf.float64)
        self.emo = tf.placeholder(tf.float64)

        # sp
        # mp  SMB  HIM  turnover  emo
        # create para
        self.b = tf.Variable(0.0, dtype=tf.float64)
        self.w1 = tf.Variable(0.0, dtype=tf.float64)
        self.w2 = tf.Variable(0.0, dtype=tf.float64)
        self.w3 = tf.Variable(0.0, dtype=tf.float64)
        self.w4 = tf.Variable(0.0, dtype=tf.float64)
        self.w5 = tf.Variable(0.0, dtype=tf.float64)
        # model
        y_model = self.mp * self.w1 + self.SMB * self.w2 + self.w3 * self.emo + self.w4 * self.HIM + self.w5 * self.turnover + self.b
        cost = tf.reduce_mean(tf.square(self.sp - y_model))
        learning_rate = 0.01
        # train
        self.train_op = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)
        print(datetime.datetime.now())
        self.init = tf.initialize_variables([self.b, self.w1, self.w2, self.w3, self.w4, self.w5])

    def LinearR(self, trains):
        with tf.Session() as sess:
            print(datetime.datetime.now())
            sess.run(self.init)
            print(datetime.datetime.now())
            print(len(trains))
            for i in range(0, len(trains)):
                feed = {self.sp: float(trains[i]['sp']), self.mp: float(trains[i]['mp']),
                        self.SMB: float(trains[i]['SMB']),
                        self.HIM: float(trains[i]['HIM']),
                        self.turnover: float(trains[i]['turnover']),
                        self.emo: float(trains[i]['emo'])}
                sess.run(self.train_op, feed_dict=feed)
                print('step: ', i)
                print('b ', sess.run(self.b))
            self.mark = sess.run(self.b)
            sess.close()
