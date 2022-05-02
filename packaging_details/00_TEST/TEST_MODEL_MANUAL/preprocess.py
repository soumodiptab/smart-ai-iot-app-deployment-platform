from keras.preprocessing.image import img_to_array,load_img
import numpy


def preprocess(data):
    numpy.random.seed(42)
    features = []
    img=load_img(data, color_mode="rgb",target_size=(224, 224))
    features.append(img_to_array(img))
    features = numpy.array(features)
    x_test=features
    x_test /= 255.

    return x_test