import keras

class PrintLogs(keras.callbacks.Callback):
    def on_train_begin(self, logs=None):
        print('欢迎你，张家盛')

    def on_epoch_begin(self, epoch, logs={}):
        self.epochs = self.params.get('epochs')
        with open('log.txt', 'w') as f:
            f.write('1')
        print('Epoch %d/%d' % (epoch + 1, self.epochs))

    def on_batch_end(self, batch, logs={}):
        self.batch_size = self.params.get('batch_size')
        self.samples = self.params.get('samples')
        percent = min(batch + 1, self.samples) * self.batch_size / self.samples * 100
        tiao = '[{}>{}]'.format('=' * int(percent // 2.5), '.' * int(40 - percent // 2.5))

        print('{}/{} {} - loss:{}'.format(min((batch + 1) * self.batch_size, self.samples), self.samples, tiao, logs.get('loss')))
    
    def on_train_end(self, logs=None):
        print('再见，张家盛')