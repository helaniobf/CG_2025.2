#pip install pygame
#pip install PyOpenGL PyOpenGL_accelerate

import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

pg.init()
info = pg.display.Info()

# Definindo altura e largura da janela
height = info.current_h - 100
width = info.current_w - 100
display = (width, height)
screen = pg.display.set_mode(display, DOUBLEBUF | OPENGL)

# Input(mundo) -> NDC
def inp_to_ndc(x, y, x_min, x_max, y_min, y_max, ndc_min=0, ndc_max=1):
    ndc_x = ndc_min + (x - x_min) * (ndc_max - ndc_min) / (x_max - x_min)
    ndc_y = ndc_min + (y - y_min) * (ndc_max - ndc_min) / (y_max - y_min)
    return ndc_x, ndc_y

# NDC -> coordenadas do mundo
def ndc_to_user(ndc_x, ndc_y, x_min, x_max, y_min, y_max, ndc_min=0, ndc_max=1):
    x = x_min + (ndc_x - ndc_min) * (x_max - x_min) / (ndc_max - ndc_min)
    y = y_min + (ndc_y - ndc_min) * (y_max - y_min) / (ndc_max - ndc_min)
    return x, y

# coordenadas do mundo -> NDC 
def user_to_ndc(x, y, x_min, x_max, y_min, y_max, ndc_min=0, ndc_max=1):
    return inp_to_ndc(x, y, x_min, x_max, y_min, y_max, ndc_min, ndc_max)

# NDC -> DC
def ndc_to_dc(ndc_x, ndc_y, ndh, ndv, ndc_min=0, ndc_max=1):
    dc_x = round((ndc_x - ndc_min) / (ndc_max - ndc_min) * (ndh - 1))
    dc_y = round((ndc_y - ndc_min) / (ndc_max - ndc_min) * (ndv - 1))
    return dc_x, dc_y

def draw_pixel(dc_x, dc_y):
    glPointSize(1)
    glBegin(GL_POINTS)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(dc_x, dc_y) 
    glEnd()

def main():    
    ndh = info.current_w # Largura do dispositivo
    ndv = info.current_h # Altura do dispositivo
    
    # WC coordenadas (Coordenadas do usuário)
    wc_x_min = float(input("Digite o X mínimo: "))
    wc_x_max = float(input("Digite o X máximo: "))
    wc_y_min = float(input("Digite o Y mínimo: "))
    wc_y_max = float(input("Digite o Y máximo: "))
    wc_x = float(input("Digite a coordenada X: "))
    wc_y = float(input("Digite a coordenada Y: "))
    
    # Configurar a matriz de projeção
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)  # Mapeia coordenadas ao tamanho da janela
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Teste com NDC no intervalo [-1, +1]
    coordenadas_ndc = inp_to_ndc(wc_x, wc_y, wc_x_min, wc_x_max, wc_y_min, wc_y_max, -1, 1)
    coordenadas_dc = ndc_to_dc(coordenadas_ndc[0], coordenadas_ndc[1], ndh, ndv, -1, 1)

    print("------------------- RESULTADOS -------------------")
    print(f"Resolução do Dispositivo: {info.current_w} x {info.current_h}")
    print(f"Coordenadas WC: X = {wc_x}, Y = {wc_y}")
    print(f"Coordenadas NDC: X = {round(coordenadas_ndc[0], 3)}, Y = {round(coordenadas_ndc[1], 3)}")
    print(f"Coordenadas DC: X = {coordenadas_dc[0]}, Y = {coordenadas_dc[1]}")

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_pixel(coordenadas_dc[0], coordenadas_dc[1])
        pg.display.flip()

if __name__ == "__main__":
    main()