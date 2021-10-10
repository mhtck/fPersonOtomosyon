from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_palette('husl')
import matplotlib.pyplot as plt

from mlxtend.preprocessing import minmax_scaling
from scipy import stats
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


def predict(a: int, b: int, c: int, d: int):
    datas = pd.read_csv('utilities/Staff.csv', encoding='cp1254')

    # Veri Önizlemesi

    # print(datas.head(), "\n", "\n")  # verinin ilk n satırını döndürür
    # datas.info(), "\n", "\n"  # dizin türü,sütun türleri,boş olmayan değerler,bellek kullanımı vb DataFrame hakkında bilgi yazdırır
    # print(datas.describe(), "\n",
    #       "\n")  # bir veri çerçevesinin yüzdelik oranı, ortalama, standart vb. gibi bazı temel istatistiksel ayrıntılarını görüntüler
    # print(datas['unvan'].value_counts())  # değişkenlerin kaç kez göründüğünü hesaplar

    # Veri goruntuleme

    Id = len('isim')

    tmp = datas.drop('isim', axis=1)

    # scikit-learn ile modelleme

    # articleinternational
    # articlenational
    # paper
    # books

    #X = datas.drop(['articleinternational', 'articlenational','paper','books'], axis=1)
    X = datas.drop(['isim', 'unvan'], axis=1)
    y = datas['unvan']


    # Aynı veri kümesi üzerinde eğitim ve test

    k_range = list(range(1, 6))
    scores = []

    for k in k_range:
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X, y)
        y_pred = knn.predict(X)
        scores.append(metrics.accuracy_score(y, y_pred))

    # plt.plot(k_range, scores)
    # plt.xlabel('KNN için k değeri')
    # plt.ylabel('Doğruluk Puanı')
    # plt.title('Komşuların k Değerlerinin Doğruluk Puanları')
    # plt.figure()
    # plt.show()


    logreg = LogisticRegression(max_iter=500)
    logreg.fit(X, y)  # sonucu belirleyen bağımsız değişkenli veri kümesini analiz etmek için kullanılır
    y_pred = logreg.predict(X)
    # print(metrics.accuracy_score(y, y_pred))

    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=5)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    # print(X_train.shape)
    # print(y_train.shape)
    # print(X_test.shape)
    # print(y_test.shape)


    k_range = list(range(1, 26))
    scores = []
    for k in k_range:
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train, y_train)
        y_pred = knn.predict(X_test)
        scores.append(metrics.accuracy_score(y_test, y_pred))
    # plt.plot(k_range, scores)
    # plt.xlabel('KNN için k değeri')
    # plt.ylabel('Doğruluk Puanı')
    # plt.title('Komşuların k Değerlerinin Doğruluk Puanları')
    # plt.show()

    k_range = list(range(1, 26))
    scores = []
    for k in k_range:
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X, y)
        y_pred = knn.predict(X)
        scores.append(metrics.accuracy_score(y, y_pred))

    logreg = LogisticRegression()
    logreg.fit(X_train, y_train)
    y_pred = logreg.predict(X_test)
    # print(metrics.accuracy_score(y_test, y_pred))

    knn = KNeighborsClassifier(n_neighbors=12)
    knn.fit(X, y)

    # örnek dışı gözlem örneği için bir tahmin yapın
    return knn.predict([[0, 1, 2, 3]]), metrics.accuracy_score(y_test, y_pred)

predict(1,2,3,4)