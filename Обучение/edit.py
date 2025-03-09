import os
from PIL import Image
path = 'data'
path2 = 'SOMETHING'
file_list = sorted(os.listdir(path))
num_0 = 0
num_1 = 0
num_2 = 0

for i in file_list:
    image = Image.open(path + '/' + i)
    if i[0] == '0':
        kk = '0-' + str(num_0)
        num_0+=1
    elif i[0] == '1':
        kk = '1-' + str(num_1)
        num_1+=1
    elif i[0] == '2':
        kk = '2-' + str(num_2)
        num_2+=1
    image.save(path2 + '/' + kk + '.jpg', 'JPEG')