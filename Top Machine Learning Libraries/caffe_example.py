# 1) install caffe using command `sudo apt install caffe-cpu`
# 2) train network `./examples/mnist/train_lenet.sh`
# 3) build pycaffe (instructions could be taken here - https://github.com/dungba88/caffe-python3-install/blob/master/install-caffe.md), run make pycaffe after make all

# Remarks on step 3:
# The Makefile.config file might reference to older version of python (3.5). If your system has Python 3.6, make appropriate changes (3.5 -> 3.6) in Python 3 section.
# pycaffe module builds will be located in caffe/python directory. To be able to import it you will need to set PYTHONPATH environment variable to caffe/python 
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
