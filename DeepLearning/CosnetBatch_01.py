import numpy as np
import math
import copy

def batch_generator(dataset, group, batch_size, training_prop):

    idx = 0
    training_data_length =  training_prop#int(training_prop * len(dataset))

    if group == 'train':
        data_batch = dataset[0:(training_data_length)]
    else:
        data_batch = dataset[training_data_length:]

    dataset_size = len(data_batch)
    indices = list(range(dataset_size))
    np.random.shuffle(indices)
    while idx < dataset_size:
        chunk = slice(idx, idx + batch_size)
        chunk = indices[chunk]
        chunk = sorted(chunk)
        idx = idx + batch_size
        yield [data_batch[i] for i in chunk]
