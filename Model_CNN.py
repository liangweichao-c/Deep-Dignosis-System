import tensorflow as tf
from tensorflow import keras
def Model_CNN_body(input):
    x = keras.layers.Conv2D(filters=32, kernel_size=3,
                            padding='same',
                            activation='selu')(input)
    x = keras.layers.MaxPool2D(pool_size=2)(x)
    x = keras.layers.Conv2D(filters=64, kernel_size=3,
                            padding='same',
                            activation='selu')(x)
    x = keras.layers.MaxPool2D(pool_size=2)(x)
    x = keras.layers.Conv2D(filters=128, kernel_size=3,
                            padding='same',
                            activation='selu')(x)
    x = keras.layers.MaxPool2D(pool_size=2)(x)
    x = keras.layers.Flatten()(x)
    x = keras.layers.Dense(128, activation='selu')(x)
    output = keras.layers.Dense(10, activation="softmax")(x)
    return output

