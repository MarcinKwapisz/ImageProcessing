import math
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image


def otsuHist(img):
    row, col = img.shape
    y = np.zeros(256)
    for i in range(0, row):
        for j in range(0, col):
            y[img[i, j]] += 1
    x = np.arange(0, 256)
    plt.bar(x, y, color='b', width=5, align='center', alpha=0.25)
    plt.show()
    return y

def countPixel(h):
    cnt = 0
    for i in range(0, len(h)):
        if h[i] > 0:
            cnt += h[i]
    return cnt


def weight(s, e):
    w = 0
    for i in range(s, e):
        w += h[i]
    return w


def mean(s, e):
    m = 0
    w = weight(s, e)
    for i in range(s, e):
        m += h[i] * i

    return m / float(w)


def variance(s, e):
    v = 0
    m = mean(s, e)
    w = weight(s, e)
    for i in range(s, e):
        v += ((i - m) ** 2) * h[i]
    v /= w
    return v


def threshold(h):
    cnt = countPixel(h)
    for i in range(1, len(h)):
        vb = variance(0, i)
        wb = weight(0, i) / float(cnt)
        mb = mean(0, i)

        vf = variance(i, len(h))
        wf = weight(i, len(h)) / float(cnt)
        mf = mean(i, len(h))

        V2w = wb * (vb) + wf * (vf)
        V2b = wb * wf * (mb - mf) ** 2

        if not math.isnan(V2w):
            threshold_values[i] = V2w


def get_optimal_threshold():
    min_V2w = min(threshold_values.values())
    optimal_threshold = [k for k, v in threshold_values.items() if v == min_V2w]
    print('optimal threshold', optimal_threshold[0])
    return optimal_threshold[0]

threshold_values = {}
h = [1]
# image = Image.open('image.png').convert("L")
# img = np.asarray(image)
# h = otsuHist(img)
# threshold(h)
# op_thres = get_optimal_threshold()