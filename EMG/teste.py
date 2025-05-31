import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from copy import deepcopy
from math import prod
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from scipy.signal import stft

data0 = np.load("dataset/s03_1.npy")
data1 = np.load("dataset/s03_2.npy")
data2 = np.load("dataset/s03_3.npy")

data = np.concatenate([data0, data1, data2], axis=0)
print("Shape dos dados combinados:", data.shape)

def butter_bandpass(data, lowcut, highcut, fs=200, order=4):
    nyq = fs * 0.5
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='bandpass')
    return signal.filtfilt(b, a, data)


def butter_lowpass(data, lowcut, fs=200, order=4):
    nyq = fs * 0.5
    low = lowcut / nyq
    b, a = signal.butter(order, low, btype='lowpass')
    return signal.filtfilt(b, a, data, padlen=len(data) // 2 )


def butter_highpass(data, highcut, fs=200, order=4):
    nyq = fs * 0.5
    high = highcut / nyq
    b, a = signal.butter(order, high, btype='highpass')
    return signal.filtfilt(b, a, data, padlen=len(data) // 2)


def butter_notch(data, cutoff, var=1, fs=200, order=4):
    nyq = fs * 0.5
    low = (cutoff - var) / nyq
    high = (cutoff + var) / nyq
    b, a = signal.iirfilter(order, [low, high], btype='bandstop', ftype="butter")
    return signal.filtfilt(b, a, data, padlen=len(data) // 2)

data = data.transpose(0,2,1)
print(data.shape)

data_filtered = butter_bandpass(data, 5, 50)
data_filtered = butter_notch(data_filtered, 60)

# data_filtered = data_filtered.transpose(0,2,1)
data_filtered.shape

data = deepcopy(data_filtered)

step = 103
segment = 256
#data = data_filterded.reshape(60, 2, 20000)
print('', data.shape)

n_win = int((data.shape[-1] - segment) / step) + 1
ids = np.arange(n_win) * step

# Janelas do dado no dominio do tempo
chunks_time = np.array([data[:,:,k:(k + segment)] for k in ids]).transpose(1, 2, 0, 3)

# Janelas do dado no domínio da frequência
_, _, chunks_freq = stft(data, fs=200, nperseg=256, noverlap=128)
chunks_freq = np.swapaxes(chunks_freq, 2, 3)

print('Formato (shape) dos dados depois da divisão de janelas')
print(f'Dominio do tempo: {chunks_time.shape} - (classes+ensaios, canais, janelas, linhas)')
print(f'Dominio da frequência:  {chunks_freq.shape} - (classes+ensaios, canais, janelas, linhas)')

# funções auxiliares
def PSD(w):
    ''' definição da função PSD para o sinal no domínio da frequência '''
    return np.abs(w) ** 2


# funções de extração de características

def var(x):
    return np.sum(x ** 2, axis=-1) / (np.prod(x.shape) - 1)

def rms(x):
    return np.sqrt(np.sum(np.abs(x) ** 2, axis=-1) / (np.prod(x.shape) - 1))

def wl(x):
    return np.sum(np.abs(np.diff(x, axis=-1)), axis=-1)

def zc(x):
    real_part = np.real(x)
    sign_changes = np.diff(np.sign(real_part), axis=-1)
    return np.sum(sign_changes != 0, axis=-1)

# Funções do dominio do Tempo 

def log_det(x):
    from math import e
    return e ** (np.sum(np.log10(np.abs(x)), axis=-1) /  np.prod(x.shape))

def fmd(w):
    return np.sum(PSD(w), axis=-1) / 2

def mmdf(w):
    return np.sum(np.abs(w), axis=-1) / 2

def mf(w):
    return (np.sum(PSD(w), axis=-1) / np.sum(PSD(w), axis=-1)) / 2

final_data = list()
final_data.append(var(chunks_time))
final_data.append(rms(chunks_time))
# final_data.append(log_det(chunks_time))
final_data.append(fmd(chunks_freq))
final_data.append(mmdf(chunks_freq))
final_data.append(mf(chunks_freq))

final = np.array(final_data)
final.shape

X = final.transpose(1, 3, 2, 0)
vis = final.transpose(1, 3, 2, 0)
print('shape para classificação:', X.shape)

np.save('dataset/teste.npy', X)

data = final.transpose(0, 1, 3, 2)
sh = X.shape
data = data.reshape(sh[0] * sh[1], sh[2] *sh[3] )
print('shape para visualização:', data.shape)
X = data

y = list()
for i in range(8):
    l = [i] * 14
    y.append(l)
y = y * 3
y = np.array(y).flatten()
print(y, y.shape)

#Initialize PCA with 2 components
pca = PCA(n_components=2)

feature_names = ['var', 'rms', 'fmd', 'mmdf']

# Iterar sobre as 4 características
for feature_idx in range(4):
    plt.figure(figsize=(8, 6))
    for class_idx in range(8):  # Iterar sobre as 8 classes
        # Selecionar os dados da classe e característica atual
        data = vis[class_idx, :, :, feature_idx]
        # Aplicar PCA para reduzir de 4 para 2 dimensões
        data_pca = pca.fit_transform(data.reshape(-1, 4))
        # Scatter plot para a classe atual
        plt.scatter(data_pca[:, 0], data_pca[:, 1], label=f'Classe {class_idx + 1}', alpha=0.6)

    plt.title(f'Scatter Plot para Característica {feature_names[feature_idx]}')
    plt.xlabel('Componente Principal 1')
    plt.ylabel('Componente Principal 2')
    plt.legend()
    plt.grid(True)
    plt.show()

print(X.shape)
# dividindo as porções de dados em treino e teste (70 e 30% respectivamente)
# com embaralhamento sempre ativo (shuffle=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=True)

# modelo de classificador com os parâmetros padrões

clf = SVC(kernel='rbf', gamma='scale')

# criando o modelo de classificação com os dados de treino
clf.fit(X_train, y_train)

# aplicando o classificador nos dados de teste
res = clf.predict(X_test)

# obtendo e ajustando os resultados 
tot_hit = sum([1 for i in range(len(res)) if res[i] == y_test[i]])
print('Acurácia: {:.2f}%'.format(tot_hit / X_test.shape[0] * 100))
