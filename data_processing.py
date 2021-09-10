import re
import numpy as np
import pywt
import os
import matplotlib.pyplot as plt

sampling_rate_ago, Rotating_speed, sampling_rate = 6400, 3000, 800

def read_file(path):
    with open(path, errors='ignore') as f:
        datas = f.read().split("\n")
    try:
        pattern = re.compile(r'\|.*')
        d = [float(pattern.findall(data)[0][1:].replace('\x00', '')) for data in datas if
             len(data) > 1 and 'm' not in data]
    except:
        d = [data.replace('\x00', '') for data in datas if
             len(data) > 1 and 'm' not in data]
    return np.array(d).flatten()

def cut_data(data):    #拆分数据
    da = []
    for i in range(data.shape[0] // 128 - 1):
        da.append(data[128*i:128*i+256])
    da.append(data[-256:])
    return np.array(da)

def get_data(data, time):  # 分离采集样本
    Data = []
    for i in range(len(data) // time):
        Data.append(data[time * i])
    return np.array(Data)

def direct_data(data):   #峰峰值
    dat = []
    for i in range(data.shape[0]):
        dat.append(max(data[i])-min(data[i]))
    return np.array(dat)

def process(data,long):     #滑动
    A = []
    for i in range(np.array(data).shape[0]-long):
        A.append(data[i:i+long])
    return np.array(A)

def morl_change(Data, totalscal, sampling_rate):  # 连续小波变换
    Ts = 1 / sampling_rate
    t = Ts * np.array(range(Data.shape[0]))
    # wavename = "cgau8"
    wavename = "morl"
    totalscal = 129
    fc = pywt.central_frequency(wavename)  # 中心频率
    cparam = 2 * fc * totalscal
    scales = cparam / np.arange(totalscal, 1, -1)
    [cwtmatr, frequencies] = pywt.cwt(Data, scales, wavename, 1.0 / sampling_rate)
    return [cwtmatr, frequencies]


def hua_fft(y, fs, style, *args):
    '''
    当style=1,画幅值谱；当style=2,画功率谱;当style=其他的，那么花幅值谱和功率谱
    当style=1时，还可以多输入2个可选参数
    可选输入参数是用来控制需要查看的频率段的
    第一个是需要查看的频率段起点
    第二个是需要查看的频率段的终点
    其他style不具备可选输入参数，如果输入发生位置错误
    '''
    nfft = len(y)
    y = y - np.mean(y)  # 去除直流分量
    y_ft = np.fft.fft(y, nfft)  # 对y信号进行DFT，得到频率的幅值分布
    y_p = y_ft * y_ft.conjugate() / nfft  # conjugate()函数是求y函数的共轭复数，实数的共轭复数是他本身。
    y_f = fs * np.arange(0, nfft / 2 + 1) / nfft  # T变换后对应的频率的序列
    yy = 4 * abs(y_ft[0: nfft // 2 + 1]) / len(y)
    if style == 1:
        if len(args) == 0:
            plt.plot(y_f, yy, linewidth=5)  # matlab的帮助里画FFT的方法
            plt.scatter(50, max(yy), color='', marker='o', edgecolors='r', s=3000)
            plt.xticks([50 * i for i in range(1, 9)], ['{}阶次'.format(i) for i in range(1, 9)])
            plt.ylim(0, max(yy) * 1.1)

        else:
            f1 = args[0]
            fn = args[1]
            ni = round(f1 * nfft / fs + 1)
            na = round(fn * nfft / fs + 1)
            plt.plot(y_f[ni - 1: na + 1], abs(y_ft[ni - 1: na + 1] * 2 / nfft))
    else:
        if style == 2:
            plt.plot(y_f, y_p[0:nfft / 2 + 1])
        else:
            plt.subplot(211)
            plt.plot(y_f, 2 * abs(y_ft[0: nfft / 2 + 1]) / len(y))
            plt.ylabel('幅值')
            plt.xlabel('频率')
            plt.title('信号幅值谱')
            plt.subplot(212)
            plt.plot(y_f, y_p[0: nfft / 2 + 1])
            plt.ylabel('功率谱密度')
            plt.xlabel('频率')
            plt.title('信号功率谱')


def X1_data(data, fs):  # 工频值   fs = 6400 采样频率
    from scipy import signal
    C, D = [], []
    for i in range(data.shape[0]):
        nfft = len(data[i])
        data[i] = data[i] - np.mean(data[i])  # 去除直流分量
        x_ft = np.fft.fft(data[i], nfft)  # 对y信号进行DFT，得到频率的幅值分布
        y = 2 * abs(x_ft[0: nfft // 2 + 1]) / len(data[i])
        num_peak = signal.find_peaks((2 * abs(x_ft[0: nfft // 2 + 1])), distance=4)
        C.append(2 * y[num_peak[0][0]])
        # D.append(2 * y[num_peak[0][1]])
    return C

def data_processing1(path):  # 处理深度训练数据函数
    data_dic, num_dic = {}, {}
    x_train, y_train = [], []  # the data of deep
    for root, dirs, _ in os.walk(path):
        for d in dirs:
            data_dic[int(d.split('-')[0])] = os.path.join(root, d)  # 增加根目录的文件名

    for key, item in data_dic.items():
        for file in os.listdir(item):
            d = read_file(os.path.join(data_dic[key], file))  # 读数据
            for i in range((d.shape[0] - 8 * 128) // 256):  # 滑动取时序数据
                da = d[256 * i:8 * 128 + 256 * i]  # 每次8*128个点提取出来
                data = get_data(da, sampling_rate_ago // sampling_rate)
                [cwtmatr, frequencies] = morl_change(data, 129,sampling_rate)
                x_train.append(abs(cwtmatr))
            y_train.extend(key * np.ones((d.shape[0] - 8 * 128)// 256))

        num_dic[key] = len(y_train)

    x_train = np.array(x_train).astype(np.float32).reshape(-1, 1).reshape(-1, 128, 128, 1)
    y_train = np.array(y_train)
    return x_train, y_train, num_dic


def data_processing2(path):# 处理深度诊断数据函数
    d = read_file(path)
    # 先画图，展示波形和数据情况
    fs = 6400  # 采样频率；
    nfft = 3200  # 采样点数
    x = d[:nfft]
    xx = d[:int(nfft / 4)]
    print(xx.shape, d.shape)

    da = cut_data(d)  # 拆分数据
    dat = direct_data(da)  # 峰峰值
    data_X1 = X1_data(da, 6400)  # 一倍频
    index = data_X1.index(max(data_X1))
    data_str = [da[index], xx, fs, hua_fft, data_X1,dat]

    x_test = []
    for i in range((d.shape[0] - 8 * 128) // 256):  # 滑动取时序数据
        da = d[256 * i:8 * 128 + 256 * i]  # 每次128*128个点提取出来
        data = get_data(da, sampling_rate_ago // sampling_rate)
        [cwtmatr, frequencies] = morl_change(data, 129,sampling_rate)
        x_test.append(abs(cwtmatr))

    x_test = np.array(x_test).astype(np.float32).reshape(-1, 1).reshape(-1, 128, 128, 1)
    return x_test, data_str


def data_processing3(path):  # 处理时序深度训练数据函数
    data_dic, num_dic = {}, {}
    x_train_time, x_train_deep, y_train = [], [], []    #the data of time&deep
    for root, dirs, _ in os.walk(path):
        for d in dirs:
            data_dic[int(d.split('-')[0])] = os.path.join(root, d)  # 增加根目录的文件名

    for key, item in data_dic.items():
        for file in os.listdir(item):
            d = read_file(os.path.join(data_dic[key], file))  # 读数据
            for i in range((d.shape[0] - 128 * 128) // 128):  # 滑动取时序数据
                da = d[128 * i:128 * 128 + 128 * i]  # 每次128*128个点提取出来
                dat = da[len(da) - 8 * 128:len(da)]
                data = get_data(dat, sampling_rate_ago // sampling_rate)
                [cwtmatr, frequencies] = morl_change(data, 129,sampling_rate)
                x_train_deep.append(abs(cwtmatr))
            da = cut_data(d)  # 拆分数据
            dat = direct_data(da)  # 峰峰值
            data_X1 = X1_data(da, 6400)  # 一倍频
            data = process(data_X1, 128)  # 滑动
            x_train_time.extend(data)
            y_train.extend(key * np.ones(data.shape[0]))
        num_dic[key] = len(y_train)

    x_train_time, y_train = np.array(x_train_time), np.array(y_train)
    x_train_time = x_train_time.reshape(x_train_time.shape[0], x_train_time.shape[1], 1)
    x_train_deep = np.array(x_train_deep).astype(np.float32).reshape(-1, 1).reshape(-1, 128, 128, 1)
    return x_train_time, x_train_deep, y_train, num_dic


def data_processing4(path):# 处理时序深度诊断数据函数
    d = read_file(path)
    # 先画图，展示波形和数据情况
    fs = 6400  # 采样频率；
    nfft = 3200  # 采样点数
    x = d[:nfft]
    xx = d[:int(nfft / 4)]
    print(xx.shape, d.shape)

    if not os.path.exists(os.path.join("bin")):
        os.mkdir(os.path.join("bin"))

    da = cut_data(d)  # 拆分数据
    dat = direct_data(da)  # 峰峰值
    data_X1 = X1_data(da, 6400)  # 一倍频
    index = data_X1.index(max(data_X1))
    data_str = [da[index], xx, fs, hua_fft, data_X1,dat]

    x_test_deep,x_test_time = [],[]
    for i in range((d.shape[0] - 128 * 128) // 128):  # 滑动取时序数据
        da = d[128 * i:128 * 128 + 128 * i]  # 每次128*128个点提取出来
        dat = da[len(da) - 8 * 128:len(da)]
        data = get_data(dat, sampling_rate_ago // sampling_rate)
        [cwtmatr, frequencies] = morl_change(data, 129,sampling_rate)
        x_test_deep.append(abs(cwtmatr))

    x_test_time = np.array(process(data_X1, 128))  # 滑动
    x_test_time = x_test_time.astype(np.float32).reshape(x_test_time.shape[0], x_test_time.shape[1], 1)
    x_test_deep = np.array(x_test_deep).astype(np.float32).reshape(-1, 1).reshape(-1, 128, 128, 1)

    return x_test_time, x_test_deep, data_str

def data_processing(path, net, is_train):
    if net == '时序深度融合网络' and is_train:
        return data_processing3(path)
    elif net == '时序深度融合网络' and not is_train:
        return data_processing4(path)
    elif not is_train:
        return data_processing2(path)
    else:
        return data_processing1(path)