from random import randint
import struct
from typing import KeysView

''' 
Se crea una clase que deje escribir en byte. La clase struct permite que se pueda pasar cosas y que se interprete en data binaria.
La información se puede guardar en un formato especifico. 
En la funcion word va un "h" ya que se necesita dos bits.
'''

def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    # short
    return struct.pack('=h', w)

def dword(w):
    # long
    return struct.pack('=l', w)

'''
Aqui se crea una función de color (r,g,b) que regresa bytes que se tienen que escribir en memoria.
La manera mas simple para convertir en bytes algo es casting. En py hay una funcion que hace eso llamada bytes().
'''

def color(r, g, b):
    return bytes([b, g, r])

BLACK =  color(0, 0, 0)
WHITE =  color(255, 255, 255)

'''

Se creara algo bien básico, que se pueda escribir en una pantalla. 
En el constructor se tienen que recibir dos parametros; el ancho de la pantalla (sirve para inicializar la raiz), y el alto.
Object es la clase padre de la que se hereda de forma generica. El constructor se crea primero con self 

'''



class Renderer(object):
    def glinit():
        r =  Renderer(1024, 768)
    

    def __init__(self, width, height):
        self.width = 1024 
        self.height = 768
        # Esta variable le da color al punto
        self.current_color = WHITE
        self.clear_color = BLACK

        self.clear()

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height

    def glViewPort(self, x, y, width, height):
        self.viewport_x = x
        self.viewport_y = y
        self.viewport_width = width
        self.viewport_height = height

    def glClear(self):
        self.clear()

    def glClearColor(self, r, g, b):
        self.r = int(r*255)
        self.g = int(g*255)
        self.b = int(b*255)
        self.clear_color = color(r, g, b)

    def glVertex(self, x, y):
        self.x = round((x + 1)* (self.viewport_width/2) + self.viewport_x)
        self.y = round((y + 1)* (self.viewport_height/2) + self.viewport_y)
        self.point(x, y)
    def glColor(self, r, g, b):
        self.r = int(r*255)
        self.g = int(g*255)
        self.b = int(b*255)
        self.current_color = color(r, g, b)


    '''
    Aqui se inicializa el framebuffer, que es una red de arrays que tienen los canales verde, rojo y azul.
    Ahora se dice que retorna BLACK para cada valor en un rango, y el rango va ser el ancho completo de la pantalla.
    Se quiere que haga eso en un rango que es el alto completo de la pantalla.
    Clear es una función que regresa todo a negro.
    '''

    def clear(self):
        self.framebuffer = [
            [BLACK for x in range(self.width)]
            for y in range(self.height)
        ]

    '''
    Eset es un metodo que sirve para escribir un archivo y que reciba el nombre del archivo que escribira.
    '''

    def write(self, filename):
        f = open(filename, 'bw')

        # File header (14)
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + 3*(self.width*self.height)))
        f.write(dword(0))
        f.write(dword(14 + 40))

        # Info header (40)
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(3*(self.width*self.height)))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        # Bitmap (se recorre el framebuffer completo, para meter los bytes en un array de 4)
        for y in range(self.height):
            for x in range(self.width):
                f.write(self.framebuffer[y][x])

        f.close()
        

    def render(self):
        self.write('a.bmp')

    # Se agregara un punto 
    def point(self, x, y, color = None):
        self.framebuffer[y][x] = color or self.current_color

'''

El objetivo es que se crea un nuevo render que contenga el tamño de la pantalla.
Despues se llama algo para que lo rendirice, y que el render este en un a.bmp

'''
r =  Renderer(80, 80)
r.current_color = color(255, 255, 255)

r.point(10, 10)
r.point(11, 10)
r.point(10, 11)
r.point(11, 11)

r.render()

