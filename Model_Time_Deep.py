from tensorflow import keras
def Model_Time_Deep_body(input_time,input_deep):
    hidden11 = keras.layers.LSTM(units=128)(input_time)
    hidden12 = keras.layers.Dense(32, activation="relu")(hidden11)
    hidden21 = keras.layers.SeparableConv2D(filters=4, kernel_size=3,
                                            padding='same',
                                            activation='selu')(input_deep)
    hidden22 = keras.layers.MaxPool2D(pool_size=2)(hidden21)
    hidden23 = keras.layers.SeparableConv2D(filters=8, kernel_size=3,
                                            padding='same',
                                            activation='relu')(hidden22)
    hidden24 = keras.layers.MaxPool2D(pool_size=2)(hidden23)
    hidden25 = keras.layers.SeparableConv2D(filters=16, kernel_size=3,
                                            padding='same',
                                            activation='relu')(hidden24)

    hidden26 = keras.layers.MaxPool2D(pool_size=2)(hidden25)
    hidden27 = keras.layers.Flatten()(hidden26)
    hidden28 = keras.layers.Dense(16, activation="relu")(hidden27)
    hidden29 = keras.layers.AlphaDropout(rate=0.5)(hidden28)
    concat = keras.layers.concatenate([hidden12, hidden29])
    hidden1 = keras.layers.Dense(32, activation="relu")(concat)
    output = keras.layers.Dense(10, activation="softmax")(hidden1)
    return output
