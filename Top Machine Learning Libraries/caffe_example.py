import caffe
import numpy as np
import cv2
import sys

model = "examples/mnist/lenet.prototxt"
weights = "examples/mnist/lenet_iter_10000.caffemodel"
net = caffe.Net(model, weights, caffe.TEST)
caffe.set_mode_cpu()

img = cv2.imread(sys.argv[1], 0)
if img.shape != [28, 28]:
    img = cv2.resize(img, (28, 28))
img = img.reshape(28, 28, -1)
img = 1.0 - img / 255.0

out = net.forward_all(data=np.asarray([img.transpose(2, 0, 1)]))

print('The recognized digit is', out["prob"][0].argmax())
