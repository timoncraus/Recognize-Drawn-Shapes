from sklearn import svm, metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from PIL import Image
from os import listdir
import numpy as np
from joblib import dump, load

def get_pixels(full_filename):

    im = Image.open(full_filename)
    im_arr = np.asarray(im)
    list_pix = []
    for i in im_arr:
        for k in i:
            sum_pix = 0
            for l in k:
                sum_pix += l
            list_pix.append(sum_pix/255)
    return list_pix    
def get_dataset(path):

    list_files = sorted(listdir(path))
    
    dataset = []
    x = []
    y = []
    for filename in list_files:
        list_pix = get_pixels(path + '/' + filename)
        x.append(list_pix)
        answer = int(filename[0])

        y.append(answer)


    return x, y

#Открыть существующую:
#brain = load('shape_network.h5')

#Обучить с нуля:
#
X, y = get_dataset('data')

brain = svm.SVC(gamma=0.001, probability=True)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.18, shuffle=True)

brain.fit(X_train, y_train)

y_pred = brain.predict(X_test)

score = accuracy_score(y_test, y_pred)*100 # смотрим сколько угадало в процентах

print('Точность: ' + str(score)[:5] + '%')

#Тест:
print('Тест')
x = get_pixels('test_shape.jpg')

#y = brain.predict([x])
#print(list[y[0]])

y = brain.predict_proba([x])
np.set_printoptions(suppress=True)
list = ['Круг', 'Треугольник', 'Квадрат']

mm = np.argmax(y)
print(list[mm])
print('(' + str(y[0][mm]*100)[:5] + '%)')

#Сохранить нейросеть:
dump(brain, 'Network.h5')