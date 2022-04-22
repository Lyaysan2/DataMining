import numpy as np


matrix = [[0, 1, 0, 0, 0, 0],
          [0, 0, 1, 0, 0, 0],
          [0, 0, 0, 0, 0, 0],
          [0, 0, 1, 0, 1, 0],
          [1, 1, 0, 0, 0, 0],
          [0, 0, 0, 1, 0, 0]]

mtx = np.array(matrix)
mtx_trn = mtx.transpose()

vector = []
for j in range(len(mtx)):
    vector.append(1.0)

vector = np.array(vector)


def scaling_vector():
    max_el = np.max(vector, 0)
    for i in range(np.size(vector)):
        vector[i] = vector[i] / max_el


for k in range(5):
    vector = mtx_trn.dot(vector)  # L^T * h

    scaling_vector()

    if k == 4:
        print("authorities pages: ", vector)  # a

    vector = mtx.dot(vector)  # L * a

    scaling_vector()

    if k == 4:
        print("hubs pages: ", vector)  # h






