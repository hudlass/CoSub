# Imports and packages =========================================================
from CosnetBatch_01 import *
from decimal import Decimal

import tensorflow as tf
import numpy      as np
import math
import csv
import random

# Sort out and formulate data ==================================================
data = list(csv.reader(open('../Data/3x3x3FirstActionsAndLengths002.csv')))
data = data[::2]
data = data[0:300000]
#random.shuffle(data)
data = [[int(j) for j in i] for i in data]

# Paramter simplification ======================================================
node_number = 1024

# Network properties ===========================================================
n_hidden_1 = node_number#1024#64#256#1000
n_hidden_2 = node_number#1024#64#256#1000
n_hidden_3 = node_number#1024#64#128#400
n_hidden_4 = node_number#1024#64#50 # 500
n_hidden_5 = node_number#512#500 # 250
n_hidden_6 = node_number#512#500 # 250
n_hidden_7 = node_number#512#250 # 100
n_hidden_8 = node_number#512#100 # 100
n_hidden_9 = node_number#512#50 # 50
n_hidden_10 = node_number#512 # 20
n_hidden_11 = node_number#512#1000
n_hidden_12 = node_number#512#1000
n_hidden_13 = node_number#512#400
n_hidden_14 = node_number#512#50 # 500
n_hidden_15 = node_number#512#500 # 250
n_hidden_16 = node_number#512#500 # 250
n_hidden_17 = node_number#512#250 # 100
n_hidden_18 = node_number#512#100 # 100
n_hidden_19 = node_number#256#50 # 50
n_hidden_20 = node_number#128 # 20

n_input    = 40
n_classes  = 1

# Network architecture =========================================================
def multilayer_perceptron(x, weights, biases):
    # Layer 1 ==================================================================
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    layer_1 = tf.nn.relu(layer_1)

    # Layer 2 ==================================================================
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    layer_2 = tf.nn.softplus(layer_2)

    # Layer 3 ==================================================================
    layer_3 = tf.add(tf.matmul(layer_2, weights['h3']), biases['b3'])
    layer_3 = tf.nn.softplus(layer_3)

    # Layer 4 ==================================================================
    layer_4 = tf.add(tf.matmul(layer_3, weights['h4']), biases['b4'])
    layer_4 = tf.nn.softplus(layer_4)

    # Layer 5 ==================================================================
    layer_5 = tf.add(tf.matmul(layer_4, weights['h5']), biases['b5'])
    layer_5 = tf.nn.relu(layer_5)

    # Layer 6 ==================================================================
    layer_6 = tf.add(tf.matmul(layer_5, weights['h6']), biases['b6'])
    layer_6 = tf.nn.relu(layer_6)

    # Layer 7 ==================================================================
    layer_7 = tf.add(tf.matmul(layer_6, weights['h7']), biases['b7'])
    layer_7 = tf.nn.relu(layer_7)

    # Layer 8 ==================================================================
    layer_8 = tf.add(tf.matmul(layer_7, weights['h8']), biases['b8'])
    layer_8 = tf.nn.softplus(layer_8)

    # Layer 9 ==================================================================
    layer_9 = tf.add(tf.matmul(layer_8, weights['h9']), biases['b9'])
    layer_9 = tf.nn.softplus(layer_9)

    # Layer 10 ==================================================================
    layer_10 = tf.add(tf.matmul(layer_9, weights['h10']), biases['b10'])
    layer_10 = tf.nn.relu(layer_10)

    # Layer 11 ==================================================================
    layer_11 = tf.add(tf.matmul(layer_10, weights['h11']), biases['b11'])
    layer_11 = tf.nn.relu(layer_11)

    # Layer 12 ==================================================================
    layer_12 = tf.add(tf.matmul(layer_11, weights['h12']), biases['b12'])
    layer_12 = tf.nn.softplus(layer_12)

    # Layer 13 ==================================================================
    layer_13 = tf.add(tf.matmul(layer_12, weights['h13']), biases['b13'])
    layer_13 = tf.nn.softplus(layer_13)

    # Layer 14 ==================================================================
    layer_14 = tf.add(tf.matmul(layer_13, weights['h14']), biases['b14'])
    layer_14 = tf.nn.softplus(layer_14)

    # Layer 15 ==================================================================
    layer_15 = tf.add(tf.matmul(layer_14, weights['h15']), biases['b15'])
    layer_15 = tf.nn.relu(layer_15)

    # Layer 16 ==================================================================
    layer_16 = tf.add(tf.matmul(layer_15, weights['h16']), biases['b16'])
    layer_16 = tf.nn.relu(layer_16)

    # Layer 17 ==================================================================
    layer_17 = tf.add(tf.matmul(layer_16, weights['h17']), biases['b17'])
    layer_17 = tf.nn.relu(layer_17)

    # Layer 18 ==================================================================
    layer_18 = tf.add(tf.matmul(layer_17, weights['h18']), biases['b18'])
    layer_18 = tf.nn.softplus(layer_18)

    # Layer 19 ==================================================================
    layer_19 = tf.add(tf.matmul(layer_18, weights['h19']), biases['b19'])
    layer_19 = tf.nn.softplus(layer_19)

    # Layer 20 ==================================================================
    layer_20 = tf.add(tf.matmul(layer_19, weights['h20']), biases['b20'])
    layer_20 = tf.nn.relu(layer_20)

    # Output layer =============================================================
    out_layer = tf.matmul(layer_10, weights['out']) + biases['out']
    return out_layer

# Weights and biases ===========================================================
weights = {
            'h1':  tf.Variable(tf.random_normal([n_input,    n_hidden_1], stddev=0.1)),
            'h2':  tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2], stddev=0.1)),
            'h3':  tf.Variable(tf.random_normal([n_hidden_2, n_hidden_3], stddev=0.1)),
            'h4':  tf.Variable(tf.random_normal([n_hidden_3, n_hidden_4], stddev=0.1)),
            'h5':  tf.Variable(tf.random_normal([n_hidden_4, n_hidden_5], stddev=0.1)),
            'h6':  tf.Variable(tf.random_normal([n_hidden_5, n_hidden_6], stddev=0.1)),
            'h7':  tf.Variable(tf.random_normal([n_hidden_6, n_hidden_7], stddev=0.1)),
            'h8':  tf.Variable(tf.random_normal([n_hidden_7, n_hidden_8], stddev=0.1)),
            'h9':  tf.Variable(tf.random_normal([n_hidden_8, n_hidden_9], stddev=0.1)),
            'h10': tf.Variable(tf.random_normal([n_hidden_9, n_hidden_10], stddev=0.1)),
            'h11':  tf.Variable(tf.random_normal([n_hidden_10, n_hidden_11], stddev=0.1)),
            'h12':  tf.Variable(tf.random_normal([n_hidden_11, n_hidden_12], stddev=0.1)),
            'h13':  tf.Variable(tf.random_normal([n_hidden_12, n_hidden_13], stddev=0.1)),
            'h14':  tf.Variable(tf.random_normal([n_hidden_13, n_hidden_14], stddev=0.1)),
            'h15':  tf.Variable(tf.random_normal([n_hidden_14, n_hidden_15], stddev=0.1)),
            'h16':  tf.Variable(tf.random_normal([n_hidden_15, n_hidden_16], stddev=0.1)),
            'h17':  tf.Variable(tf.random_normal([n_hidden_16, n_hidden_17], stddev=0.1)),
            'h18':  tf.Variable(tf.random_normal([n_hidden_17, n_hidden_18], stddev=0.1)),
            'h19': tf.Variable(tf.random_normal([n_hidden_18, n_hidden_19], stddev=0.1)),
            'h20': tf.Variable(tf.random_normal([n_hidden_10, n_hidden_20], stddev=0.1)),
            'out': tf.Variable(tf.random_normal([n_hidden_5, n_classes],  stddev=0.1))
          }
biases  = {
            'b1':  tf.Variable(tf.random_normal([n_hidden_1], stddev=0.1)),
            'b2':  tf.Variable(tf.random_normal([n_hidden_2], stddev=0.1)),
            'b3':  tf.Variable(tf.random_normal([n_hidden_3], stddev=0.1)),
            'b4':  tf.Variable(tf.random_normal([n_hidden_4], stddev=0.1)),
            'b5':  tf.Variable(tf.random_normal([n_hidden_5], stddev=0.1)),
            'b6':  tf.Variable(tf.random_normal([n_hidden_6], stddev=0.1)),
            'b7':  tf.Variable(tf.random_normal([n_hidden_7], stddev=0.1)),
            'b8':  tf.Variable(tf.random_normal([n_hidden_8], stddev=0.1)),
            'b9':  tf.Variable(tf.random_normal([n_hidden_9], stddev=0.1)),
            'b10': tf.Variable(tf.random_normal([n_hidden_10], stddev=0.1)),
            'b11':  tf.Variable(tf.random_normal([n_hidden_11], stddev=0.1)),
            'b12':  tf.Variable(tf.random_normal([n_hidden_12], stddev=0.1)),
            'b13':  tf.Variable(tf.random_normal([n_hidden_13], stddev=0.1)),
            'b14':  tf.Variable(tf.random_normal([n_hidden_14], stddev=0.1)),
            'b15':  tf.Variable(tf.random_normal([n_hidden_15], stddev=0.1)),
            'b16':  tf.Variable(tf.random_normal([n_hidden_16], stddev=0.1)),
            'b17':  tf.Variable(tf.random_normal([n_hidden_17], stddev=0.1)),
            'b18':  tf.Variable(tf.random_normal([n_hidden_18], stddev=0.1)),
            'b19':  tf.Variable(tf.random_normal([n_hidden_19], stddev=0.1)),
            'b20': tf.Variable(tf.random_normal([n_hidden_20], stddev=0.1)),
            'out': tf.Variable(tf.random_normal([n_classes],  stddev=0.1))
          }

# Primary function =============================================================
def main():

    # Basic parameters =========================================================
    monitoring_freq = 100
    epochs          = 50
    learning_rate   = 0.0002
    training_prop   = 200000
    batch_size      = 50
    val_batch_size  = 500
    max_steps       = int(epochs * training_prop / batch_size)


    # Initialise input and outputs for the network =============================
    x = tf.placeholder("float", [None, n_input])
    y = tf.placeholder("float", [None, n_classes])

    # Generate batches of data =================================================
    train_batch_gen = batch_generator(data, 'train', batch_size, training_prop)
    val_batch_gen   = batch_generator(data, 'test',  val_batch_size, training_prop)
    test_batch_gen  = batch_generator(data, 'test',  val_batch_size, training_prop)

    # Import network model =====================================================
    pred = multilayer_perceptron(x, weights, biases)
    input_values = x

    cost = tf.losses.absolute_difference(y, pred)
    train_step = tf.train.AdamOptimizer(learning_rate).minimize(cost)
    # train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

    correct    = tf.equal(tf.round(y), tf.round(pred))
    accuracy   = tf.reduce_mean(tf.cast(correct, 'float')) * 100
    difference = tf.abs(tf.round(y) - tf.round(pred))
    mean_diff  = tf.reduce_mean(tf.cast(difference, 'float'))

    init_op = tf.group(tf.global_variables_initializer(),
              tf.local_variables_initializer())

    saver = tf.train.Saver()


    with tf.Session() as sess:
        #sess.run(init_op)
        saver.restore(sess, "ModelCheckpoints/3x3x3FirstActionAndLengthsModel001.ckpt")
        print("Model restored.")

        # print('=============== Training ===============')
        # print("Max steps: " + str(max_steps))
        # for step in range(max_steps):
        #
        #     # Getting train batch
        #     train_batch = next(train_batch_gen)
        #     if len(train_batch[0]) != batch_size:
        #         train_batch_gen = batch_generator(data, 'train', batch_size, training_prop)
        #         train_batch = next(train_batch_gen)
        #
        #     train_batch = np.asarray(train_batch)
        #     train_input = train_batch[:, 2:]
        #     train_label = train_batch[:, 0]
        #
        #
        #
        #     train_label = train_label.reshape(batch_size, n_classes)
        #
        #     _ = sess.run(train_step, feed_dict={x: train_input, y: train_label})
        #
        #     if step % (monitoring_freq) == 0:
        #         val_batch = next(val_batch_gen)
        #
        #         if len(val_batch[0]) != batch_size:
        #             val_batch_gen = batch_generator(data, 'test', val_batch_size, training_prop)
        #             val_batch = next(val_batch_gen)
        #
        #         val_batch = np.asarray(val_batch)
        #         val_input = val_batch[:, 2:]
        #         val_label = val_batch[:, 0]
        #
        #         val_label = val_label.reshape(val_batch_size, n_classes)
        #
        #         val_accuracy, val_loss, val_mean_diff, val_input_values = sess.run([accuracy, cost, mean_diff, input_values], feed_dict={x: val_input, y: val_label})
        #         train_loss = sess.run(cost, feed_dict={x: train_input, y: train_label})
        #
        #         #weight_mean, weight_var = tf.nn.moments(weights, axes=[1])
        #
        #         print("Step: " + str(step))
        #         #print(weights)#print("Weight mean: " + str(tf.reduce_mean(weights)) + "   Weight variance: " + str(np.std(weights)))
        #         print("Training loss: %.3f   Validation accuracy: %.2f%%   Validation loss: %.3f   Validation mean difference: %.3f" % (math.sqrt(train_loss * batch_size), val_accuracy, math.sqrt(val_loss * batch_size), val_mean_diff))
        #         print()

        # Testing model ========================================================
        print('=============== Testing ===============')

        testing_size = len(data) - training_prop#int((1 - training_prop) * len(data))
        num_test_iter = int(testing_size/val_batch_size)
        accuracy_sum = 0

        for i in range(num_test_iter):

            # Processing data ==================================================
            test_batch = next(test_batch_gen)
            test_batch = np.asarray(test_batch)
            test_input = test_batch[:, 2:]
            test_label = test_batch[:, 0]
            test_label = test_label.reshape(val_batch_size, n_classes)

            accuracy_sum += sess.run(accuracy, feed_dict={x: test_input, y: test_label})

        accuracy_sum /= num_test_iter
        print('Final Accuracy : %.2f%%' % (accuracy_sum))

        # save_path = saver.save(sess, "ModelCheckpoints/3x3x3FirstActionAndLengthsModel001.ckpt")
        # print("Model saved in path: %s" % save_path)




main()
