# ==============================================================================
# ==============================================================================
# Multilayer Perceptron - Version 001 ==========================================
# Luke Hudlass-Galley ==========================================================
# ==============================================================================
# ==============================================================================

# Imports and packages =========================================================
from BatchGenerator import *

import tensorflow as tf
import numpy      as np
import math
import csv
import random

# Sort out and formulate data ==================================================
data = list(csv.reader(open('../FormattedData/8PuzzleLengthsUniform.csv')))
data = data[::2]
#random.shuffle(data)

node_number = 512

# Network properties ===========================================================
n_hidden_1 = node_number
n_hidden_2 = node_number
n_hidden_3 = node_number
n_hidden_4 = node_number
n_hidden_5 = node_number
n_hidden_6 = node_number
n_hidden_7 = node_number

n_input    = 8
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

    # Layer 6 ==================================================================
    layer_6 = tf.add(tf.matmul(layer_5, weights['h6']), biases['b6'])
    layer_6 = tf.nn.relu(layer_6)

    # Layer 7 ==================================================================
    layer_7 = tf.add(tf.matmul(layer_6, weights['h7']), biases['b7'])
    layer_7 = tf.nn.relu(layer_7)

    # Output layer =============================================================
    out_layer = tf.matmul(layer_7, weights['out']) + biases['out']
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
            'out': tf.Variable(tf.random_normal([n_hidden_7, n_classes],  stddev=0.1))
          }
biases  = {
            'b1':  tf.Variable(tf.random_normal([n_hidden_1], stddev=0.1)),
            'b2':  tf.Variable(tf.random_normal([n_hidden_2], stddev=0.1)),
            'b3':  tf.Variable(tf.random_normal([n_hidden_3], stddev=0.1)),
            'b4':  tf.Variable(tf.random_normal([n_hidden_4], stddev=0.1)),
            'b5':  tf.Variable(tf.random_normal([n_hidden_5], stddev=0.1)),
            'b6':  tf.Variable(tf.random_normal([n_hidden_6], stddev=0.1)),
            'b7':  tf.Variable(tf.random_normal([n_hidden_7], stddev=0.1)),
            'out': tf.Variable(tf.random_normal([n_classes],  stddev=0.1))
          }

# Primary function =============================================================
def main():

    # Basic parameters =========================================================
    monitoring_freq = 500
    epochs          = 100
    learning_rate   = 0.00015
    training_prop   = 100000
    batch_size      = 50
    val_batch_size  = 500
    test_batch_size = len(data) - training_prop#int((1 - training_prop) * len(data))
    max_steps       = int(epochs * training_prop / batch_size)
    print("Max steps: " + str(max_steps))

    # Initialise input and outputs for the network =============================
    x = tf.placeholder("float", [None, n_input])
    y = tf.placeholder("float", [None, n_classes])

    # Generate batches of data =================================================
    train_batch_gen = batch_generator(data, 'train', batch_size, training_prop)
    val_batch_gen   = batch_generator(data, 'test',  val_batch_size, training_prop)
    test_batch_gen  = batch_generator(data, 'test',  test_batch_size, training_prop)

    # Import network model =====================================================
    output     = multilayer_perceptron(x, weights, biases)
    cost       = tf.losses.mean_squared_error(y, output)

    input_parity = tf.transpose([x[:,0]])# for item in range(0, 10000)]

    pred = (abs(tf.floor(output) - input_parity) % 2) + tf.floor(output)

    train_step = tf.train.AdamOptimizer(learning_rate).minimize(cost)

    # Features to retrieve from the session ====================================
    correct    = tf.equal(tf.round(y), tf.round(pred))
    accuracy   = tf.reduce_mean(tf.cast(correct, 'float')) * 100
    mean_diff  = tf.reduce_mean(tf.cast(tf.abs(tf.round(y) - tf.round(pred)), 'float'))

    # Initialise variables for the model =======================================
    init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())

    saver = tf.train.Saver()

    with tf.Session() as sess:
        sess.run(init_op)

        print()
        print("=================================================")
        print("Training Mode ===================================")
        print("=================================================")
        print()
        print("Max steps: " + str(max_steps))
        print()

        inconsistency_results = []

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

                val_label            = val_label.reshape(val_batch_size, n_classes)
                val_labels_formatted = [int(item[0]) for item in val_label]
                val_predictions      = sess.run(pred, feed_dict={x: val_input, y: val_label})

                train_loss = sess.run(cost, feed_dict={x: train_input, y: train_label})

                print("Step " + str(step) + ":")
                print()
                print("Validation test:")
                # for i in range(len(val_predictions)):
                #     if int(val_predictions[i][0]) == int(val_label[i][0]):
                #         print("Prediction: " + str(int(val_predictions[i][0])) + "  Ground truth: " + str(int(val_label[i][0])) + "    Correctly predicted")
                #     else:
                #         print("Prediction: " + str(int(val_predictions[i][0])) + "  Ground truth: " + str(int(val_label[i][0])))

                error_difference = np.transpose(val_predictions) - val_labels_formatted

                #print()
                print("Statistics for step " + str(step) + ":")
                accuracy = int((np.count_nonzero(error_difference == 0)/len(error_difference[0])) * 100)
                print("Accuracy:              " + str(accuracy) + "% (" + str(int(np.count_nonzero(error_difference == 0))) + "/" + str(len(error_difference[0])) + ")")
                mean_square_error = (error_difference ** 2).mean(axis = None)
                print("Mean square error:     " + str(mean_square_error))
                absolute_dev = np.sum(np.abs(error_difference))/len(error_difference[0])
                print("Absolute deviation:    " + str(absolute_dev))
                average_dev = np.abs(np.sum(error_difference))/len(error_difference[0])
                print("Average deviation:     " + str(average_dev))
                inconsistency = np.abs(absolute_dev - average_dev)
                inconsistency_results.append(inconsistency)
                print("Inconsistency:         " + str(inconsistency))
                standard_dev = np.std(error_difference)
                print("Standard deviation:    " + str(standard_dev))
                print()





        # Testing model ========================================================
        print('=============== Testing ===============')

        test_batch = next(test_batch_gen)

        test_batch = np.asarray(test_batch)
        test_input = test_batch[:, 1:]
        test_label = test_batch[:, 0]

        test_label            = test_label.reshape(test_batch_size, n_classes)
        test_labels_formatted = [int(item[0]) for item in test_label]
        test_predictions      = sess.run(pred, feed_dict={x: test_input, y: test_label})

        print()
        print("Test results:")
        for i in range(len(test_predictions)):
            if int(test_predictions[i][0]) == int(test_label[i][0]):
                print("Prediction: " + str(int(test_predictions[i][0])) + "  Ground truth: " + str(int(test_label[i][0])) + "    Correctly predicted")
            else:
                print("Prediction: " + str(int(test_predictions[i][0])) + "  Ground truth: " + str(int(test_label[i][0])))

        error_difference = np.transpose(test_predictions) - test_labels_formatted

        print()
        print("Inconsistency results")
        print(inconsistency_results)
        print("Statistics:")
        accuracy = int((np.count_nonzero(error_difference == 0)/len(error_difference[0])) * 100)
        print("Accuracy:              " + str(accuracy) + "% (" + str(int(np.count_nonzero(error_difference == 0))) + "/" + str(len(error_difference[0])) + ")")
        mean_square_error = (error_difference ** 2).mean(axis = None)
        print("Mean square error:     " + str(mean_square_error))
        absolute_dev = np.sum(np.abs(error_difference))/len(error_difference[0])
        print("Absolute deviation:    " + str(absolute_dev))
        average_dev = np.abs(np.sum(error_difference))/len(error_difference[0])
        print("Average deviation:     " + str(average_dev))
        inconsistency = np.abs(absolute_dev - average_dev)
        print("Inconsistency:         " + str(inconsistency))
        standard_dev = np.std(error_difference)
        print("Standard deviation:    " + str(standard_dev))
        print()

        save_path = saver.save(sess, "ModelCheckpoints/8PuzzleJustLengthsModel001.ckpt")
        print("Model saved in path: %s" % save_path)



main()
