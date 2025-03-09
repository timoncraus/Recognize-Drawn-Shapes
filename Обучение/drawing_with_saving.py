from os import listdir
import pygame
from time import time
import numpy as np
from joblib import load
from PIL import Image, ImageDraw

pygame.init()
pygame.font.init()

image = Image.open("cash.jpg")
draw_save = ImageDraw.Draw(image)

brain = load('Network.h5')

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, image, w=60, h=60):
        pygame.sprite.Sprite.__init__(self)
        a = pygame.image.load(image)
        self.image = pygame.transform.scale(a, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self, window, opacity):
        self.image.set_alpha(opacity*255)
        window.blit(self.image, self.rect)

def sum_color(m, n):
    g = m+n
    if g>255:
        g=255
    return g

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




saving_shape = 2

saving_path = 'data'
file_list = sorted(listdir(saving_path))
saving_number = 0
for i in file_list:
    if i[0] == str(saving_shape):
        b = i.find('-')
        j = i.find('.')
        num = i[b+1:j]
        if int(num) > saving_number:
            saving_number = int(num)

w = 800
h = 600
screen_size = (w, h)
screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
pygame.display.set_caption('Андромеда (с сохранением)')
pygame.display.set_icon(pygame.image.load("ico.bmp"))

list_table = []
for x in range(40):
    for y in range(40):
        b = 0
        list_table.append([x, y, b])

opacity0 = 1
opacity1 = 1
opacity2 = 1
nerual_timing = time()

running = True
clock = pygame.time.Clock()

while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # нажатие на крестик: выход
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                for i in list_table:
                    color_pix = abs(i[2]-255)

                    draw_save.point( ( (i[0]-x_table)//block, (i[1]-y_table)//block ), (color_pix, color_pix, color_pix) )
                image.save(str(saving_path) + '/' + str(saving_shape) + '-' + str(saving_number+1) + '.jpg', 'JPEG')
                print(str(saving_shape) + '-' + str(saving_number+1))
                saving_number+=1

                for i in list_table:
                    i[2] = 0

            mouse_t = pygame.mouse.get_pressed()[0]

        x_table, y_table = w//7, h//10
        block = w*0.5//40
        if block > 14:
            block = 14

        screen.fill((255, 255, 255))



        
        clear_block = [x_table+40*block//2-block*9//2, y_table+40*block+block*2, block*9, block*3]
        pygame.draw.rect(screen, (100, 100, 100), clear_block)
        #
        clear_font = pygame.font.SysFont('Arial', int(block*2.5))
        textsurface = clear_font.render('Стереть', False, (255, 255, 255))
        screen.blit(textsurface,(x_table+40*block//2+block*0.6-block*9//2, y_table+40*block+block*2, block*9, block*3))


        save_block = [x_table+40*block//2-block*9//2, y_table+40*block+block*6, block*9, block*3]
        pygame.draw.rect(screen, (90, 90, 140), save_block)
        #
        save_font = pygame.font.SysFont('Arial', int(block*2.1))
        textsurface = save_font.render('Сохранить', False, (255, 255, 255))
        screen.blit(textsurface,(x_table+40*block//2+block*0.2-block*9//2, y_table+40*block+block*6, block*9, block*3))


        bg_block = [x_table, y_table, 40*block+block, 40*block+block]
        pygame.draw.rect(screen, (162, 115, 61), bg_block)


        w1 = block*6

        myfont = pygame.font.SysFont('Arial', int(block*3))

        p_circle = GameSprite(x=40*block+x_table+block*4, y=y_table+10, image='p_circle.png', w=w1, h=w1)
        p_circle.reset(screen, opacity0)
        #
        textsurface = myfont.render(str(opacity0*100)[:4] + '%', False, (0, 0, 0))
        screen.blit(textsurface,(40*block+x_table+block*4+block*9, y_table+15))

        p_triangle = GameSprite(x=40*block+x_table+block*4, y=y_table+w1+25, image='p_triangle.png', w=w1, h=w1)
        p_triangle.reset(screen, opacity1)
        #
        textsurface = myfont.render(str(opacity1*100)[:4] + '%', False, (0, 0, 0))
        screen.blit(textsurface,(40*block+x_table+block*4+block*9, y_table+w1+30))


        p_square = GameSprite(x=40*block+x_table+block*4, y=y_table+w1*2+55, image='p_square.png', w=w1, h=w1)
        p_square.reset(screen, opacity2)
        #
        textsurface = myfont.render(str(opacity2*100)[:4] + '%', False, (0, 0, 0))
        screen.blit(textsurface,(40*block+x_table+block*4+block*9, y_table+w1*2+55))

        x_mouse, y_mouse = pygame.mouse.get_pos()
        for i in range(len(list_table)):
            #pygame.draw.rect(screen, (0,0,0,list_table[i][2]), [list_table[i][0], list_table[i][1], block, block])
            rect = [list_table[i][0]*block+x_table, list_table[i][1]*block+y_table, block, block]
            shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
            pygame.draw.rect(shape_surf, (0,0,0,list_table[i][2]), shape_surf.get_rect())
            screen.blit(shape_surf, rect)
            
            if mouse_t:
                if x_mouse >= list_table[i][0]*block+x_table and x_mouse <= list_table[i][0]*block+x_table + block and y_mouse >= list_table[i][1]*block+y_table and y_mouse <= list_table[i][1]*block+y_table + block:
                    list_table[i][2] = sum_color(list_table[i][2], 255)
                    try:
                        list_table[i-1][2] = sum_color(list_table[i+1][2], 255)
                        list_table[i+1][2] = sum_color(list_table[i+1][2], 255)
                        list_table[i+40][2] = sum_color(list_table[i+40][2], 255)
                        list_table[i-40][2] = sum_color(list_table[i+40][2], 225)
                        #
                        list_table[i-39][2] = sum_color(list_table[i-39][2], 75)
                        list_table[i+39][2] = sum_color(list_table[i+39][2], 75)
                        list_table[i-41][2] = sum_color(list_table[i-41][2], 75)
                        list_table[i+41][2] = sum_color(list_table[i+41][2], 75)
                    except:
                        pass

        if mouse_t:
            if x_mouse >= clear_block[0] and x_mouse <= clear_block[0]+clear_block[2] and y_mouse >= clear_block[1] and y_mouse <= clear_block[1]+clear_block[3]:
                for i in list_table:
                    i[2] = 0

                opacity0 = 0
                opacity1 = 0
                opacity2 = 0

        surface = pygame.display.get_surface()
        w, h = surface.get_width(), surface.get_height()

        if mouse_t:
            if x_mouse >= save_block[0] and x_mouse <= save_block[0]+save_block[2] and y_mouse >= save_block[1] and y_mouse <= save_block[1]+save_block[3] and need_to:
                saving_mode = True

                for i in list_table:
                    color_pix = abs(i[2]-255)

                    draw_save.point( ( (i[0]-x_table)//block, (i[1]-y_table)//block ), (color_pix, color_pix, color_pix) )
                image.save(str(saving_path) + '/' + str(saving_shape) + '-' + str(saving_number+1) + '.jpg', 'JPEG')
                print(str(saving_shape) + '-' + str(saving_number+1))
                saving_number+=1
                need_to = False

                for i in list_table:
                    i[2] = 0
        else:
            need_to = True
        



        clock.tick(150)


        if time() - nerual_timing > 1:
            
            nerual_timing = time()

            for i in list_table:
                    color_pix = abs(i[2]-255)

                    draw_save.point( ( i[0], i[1] ), (color_pix, color_pix, color_pix) )
            image.save('cash.jpg', 'JPEG')

            x = get_pixels('cash.jpg')

            y = np.array(brain.predict_proba([x]))
            np.set_printoptions(suppress=True)

            opacity0 = y[0][0]
            opacity1 = y[0][1]
            opacity2 = y[0][2]

        pygame.display.update()

pygame.quit()