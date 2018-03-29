# Imports and packages =========================================================
from CosnetBatch_01 import *
from decimal import Decimal

import tensorflow as tf
import numpy      as np
import math
import csv
import random

# Sort out and formulate data ==================================================
data = list(csv.reader(open('../Data/8PuzzleCosnet_01Data.csv')))
data = data[::2]
data = data[0:120000]
data = [[int(j) for j in i] for i in data]

# Network properties ===========================================================
n_hidden_1 = 1024#64#256#1000
n_hidden_2 = 1024#64#256#1000
n_hidden_3 = 1024#64#128#400
n_hidden_4 = 1024#64#50 # 500
n_hidden_5 = 1024#500 # 250

n_input    = 16
n_classes  = 1

# Network architecture =========================================================
def multilayer_perceptron(x, weights, biases):
    # Layer 1 ==================================================================
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    layer_1 = tf.nn.relu(layer_1)

    # Layer 2 ==================================================================
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    layer_2 = tf.nn.relu(layer_2)

    # Layer 3 ==================================================================
    layer_3 = tf.add(tf.matmul(layer_2, weights['h3']), biases['b3'])
    layer_3 = tf.nn.relu(layer_3)

    # Layer 4 ==================================================================
    layer_4 = tf.add(tf.matmul(layer_3, weights['h4']), biases['b4'])
    layer_4 = tf.nn.relu(layer_4)

    # Layer 5 ==================================================================
    layer_5 = tf.add(tf.matmul(layer_4, weights['h5']), biases['b5'])
    layer_5 = tf.nn.relu(layer_5)

    # Output layer =============================================================
    out_layer = tf.matmul(layer_5, weights['out']) + biases['out']
    return out_layer

# Weights and biases ===========================================================
weights = {
            'h1':  tf.Variable(tf.random_normal([n_input,    n_hidden_1], stddev=0.1)),
            'h2':  tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2], stddev=0.1)),
            'h3':  tf.Variable(tf.random_normal([n_hidden_2, n_hidden_3], stddev=0.1)),
            'h4':  tf.Variable(tf.random_normal([n_hidden_3, n_hidden_4], stddev=0.1)),
            'h5':  tf.Variable(tf.random_normal([n_hidden_4, n_hidden_5], stddev=0.1)),
            'out': tf.Variable(tf.random_normal([n_hidden_5, n_classes],  stddev=0.1))
          }
biases  = {
            'b1':  tf.Variable(tf.random_normal([n_hidden_1], stddev=0.1)),
            'b2':  tf.Variable(tf.random_normal([n_hidden_2], stddev=0.1)),
            'b3':  tf.Variable(tf.random_normal([n_hidden_3], stddev=0.1)),
            'b4':  tf.Variable(tf.random_normal([n_hidden_4], stddev=0.1)),
            'b5':  tf.Variable(tf.random_normal([n_hidden_5], stddev=0.1)),
            'out': tf.Variable(tf.random_normal([n_classes],  stddev=0.1))
          }

# Primary function =============================================================
def main():

    # Basic parameters =========================================================
    monitoring_freq = 200
    epochs          = 50
    learning_rate   = 0.0002
    training_prop   = 100000
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
        sess.run(init_op)
        # saver.restore(sess, "ModelCheckpoints/model002.ckpt")
        # print("Model restored.")

        train_loss_vector = []
        val_loss_vector = []

        print('=============== Training ===============')
        print("Max steps: " + str(max_steps))
        for step in range(max_steps):

            # Getting train batch
            train_batch = next(train_batch_gen)
            if len(train_batch[0]) != batch_size:
                train_batch_gen = batch_generator(data, 'train', batch_size, training_prop)
                train_batch = next(train_batch_gen)

            train_batch = np.asarray(train_batch)
            train_input = train_batch[:, 1:]
            train_label = train_batch[:, 0]



            train_label = train_label.reshape(batch_size, n_classes)

            _ = sess.run(train_step, feed_dict={x: train_input, y: train_label})

            if step % (monitoring_freq) == 0:
                val_batch = next(val_batch_gen)

                if len(val_batch[0]) != batch_size:
                    val_batch_gen = batch_generator(data, 'test', val_batch_size, training_prop)
                    val_batch = next(val_batch_gen)

                val_batch = np.asarray(val_batch)
                val_input = val_batch[:, 1:]
                val_label = val_batch[:, 0]

                val_label = val_label.reshape(val_batch_size, n_classes)

                val_accuracy, val_loss, val_mean_diff, val_input_values = sess.run([accuracy, cost, mean_diff, input_values], feed_dict={x: val_input, y: val_label})
                train_loss = sess.run(cost, feed_dict={x: train_input, y: train_label})

                train_loss_vector.append(train_loss)
                val_loss_vector.append(val_loss)

                #weight_mean, weight_var = tf.nn.moments(weights, axes=[1])

                print("Step: " + str(step))
                #print(weights)#print("Weight mean: " + str(tf.reduce_mean(weights)) + "   Weight variance: " + str(np.std(weights)))
                print("Training loss: %.3f   Validation accuracy: %.2f%%   Validation loss: %.3f   Validation mean difference: %.3f" % (math.sqrt(train_loss * batch_size), val_accuracy, math.sqrt(val_loss * batch_size), val_mean_diff))
                print()

        # Testing model ========================================================
        print('=============== Testing ===============')

        testing_size = len(data) - training_prop#int((1 - training_prop) * len(data))
        num_test_iter = int(testing_size/val_batch_size)
        accuracy_sum = 0

        for i in range(num_test_iter):

            # Processing data ==================================================
            test_batch = next(test_batch_gen)
            test_batch = np.asarray(test_batch)
            test_input = test_batch[:, 1:]
            test_label = test_batch[:, 0]
            test_label = test_label.reshape(val_batch_size, n_classes)

            accuracy_sum += sess.run(accuracy, feed_dict={x: test_input, y: test_label})

        accuracy_sum /= num_test_iter
        print('Final Accuracy : %.2f%%' % (accuracy_sum))

        save_path = saver.save(sess, "ModelCheckpoints/8PuzzleFirstActionAndLengthsModel001.ckpt")
        print("Model saved in path: %s" % save_path)





main()
