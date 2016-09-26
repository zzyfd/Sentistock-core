#! /usr/bin/env python
import tensorflow as tf
import numpy as np
import os
import time
import datetime
import data_helpers as data_helpers
from tensorflow.contrib import learn
from collections import OrderedDict
import jieba
def getCNNDaata(eval_train, checkpoints, sFileName, start, end):
    # Parameters
    # ==================================================

    # Eval Parameters
    tf.flags.DEFINE_integer("batch_size", 64, "Batch Size (default: 64)")
    tf.flags.DEFINE_string("checkpoint_dir", "", "Checkpoint directory from training run")
    tf.flags.DEFINE_boolean("eval_train", False, "Evaluate on all training data")

    # Misc Parameters
    tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
    tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")
    FLAGS = tf.flags.FLAGS
    FLAGS._parse_flags()
    FLAGS.eval_train = eval_train
    FLAGS.checkpoint_dir = "./runs/"+checkpoints+"/checkpoints/"
    print("\nParameters:")
    for attr, value in sorted(FLAGS.__flags.items()):
        print("{}={}".format(attr.upper(), value))
    print("")

    # CHANGE THIS: Load data. Load your own data here
    if FLAGS.eval_train:
        #x_raw, y_test = data_helpers.load_cn_data_and_labels("./data/rt-polaritydata/TestData.txt")
        #y_test = np.argmax(y_test, axis=1)
        examples,y_test = data_helpers.load_cn_data (sFileName, start, end )
        x_raw = []
        for stock in examples:
            for date in examples[stock]:
                for info in examples[stock][date]:
                    x_raw.append(info.strip())
        x_raw = [" ".join(jieba.cut(sent)).strip() for sent in x_raw]
        print("raw loaded");
        y_flag = True
    else:
        x_raw = ["a masterpiece four years in the making", "everything is off."]
        y_test = [1, 0]
        y_flag = False

    # Map data into vocabulary
    vocab_path = os.path.join(FLAGS.checkpoint_dir, "..", "vocab")
    vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_path)
    x_test = np.array(list(vocab_processor.transform(x_raw)))

    print("\nEvaluating...\n")

    # Evaluation
    # ==================================================
    checkpoint_file = tf.train.latest_checkpoint(FLAGS.checkpoint_dir)
    graph = tf.Graph()
    with graph.as_default():
        session_conf = tf.ConfigProto(
          allow_soft_placement=FLAGS.allow_soft_placement,
          log_device_placement=FLAGS.log_device_placement)
        sess = tf.Session(config=session_conf)
        with sess.as_default():
            # Load the saved meta graph and restore variables
            saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
            saver.restore(sess, checkpoint_file)

            # Get the placeholders from the graph by name
            input_x = graph.get_operation_by_name("input_x").outputs[0]
            # input_y = graph.get_operation_by_name("input_y").outputs[0]
            dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

            # Tensors we want to evaluate
            predictions = graph.get_operation_by_name("output/predictions").outputs[0]

            # Generate batches for one epoch
            batches = data_helpers.batch_iter(list(x_test), FLAGS.batch_size, 1, shuffle=False)

            # Collect the predictions here
            all_predictions = []

            for x_test_batch in batches:
                batch_predictions = sess.run(predictions, {input_x: x_test_batch, dropout_keep_prob: 1.0})
                all_predictions = np.concatenate([all_predictions, batch_predictions])
    print("evaluation complete!")
    # Print accuracy if y_test is defined
    if not y_flag:
        error01 = 0
        error10 = 0
        for p in range(0, len(all_predictions)):
            print("Data p {}".format(p))
            print("test {} predict {}".format(y_test[p], all_predictions[p]))
            if y_test[p] != all_predictions[p]:
                if y_test[p] == 0:
                    error01+=1
                else:
                    error10+=1
        correct_predictions = float(sum(all_predictions == y_test))
        print("Total number of test examples: {}".format(len(y_test)))
        print("Accuracy: {:g}".format(correct_predictions/float(len(y_test))))
        print("0-1 ERROR {:g}".format(error01/float(len(y_test))))
        print("1-0 ERROR {:g}".format(error10 / float(len(y_test))))
    else:
        i = 0
        pos = 0
        neg = 0
        posData = OrderedDict()
        negData = OrderedDict()
        for stock in examples:
            for date in examples[stock]:
                for info in examples[stock][date]:
                    info = [info, all_predictions[i]]
                    if all_predictions[i] ==1:
                        pos+=1
                        posData.setdefault(stock, OrderedDict()).setdefault(date, "")
                        posData[stock][date] += info[0]
                    else:
                        neg+=1
                        negData.setdefault(stock, OrderedDict()).setdefault(date, "")
                        negData[stock][date] += info[0]
                    i+=1
        print("pos:",pos);print("neg:",neg)
    return posData, negData