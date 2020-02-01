#!/usr/local/bin/python3
import tkinter as tk
from math import sin, cos, pi
import numpy as np

class Application(tk.Frame):

    canvas_width=900
    canvas_height=400
    canvas_centre = [canvas_width/2, canvas_height/2]

    slider_dilation_start = 0
    slider_dilation_end = 3
    slider_dilation_length=slider_dilation_end-slider_dilation_start

    slider_rotation_start = 0
    slider_rotation_end = 2*pi
    slider_rotation_length=slider_rotation_end-slider_rotation_start

    slider_dilation_denominator=3

    slider_initital_size_start= 1
    slider_initial_size_end = 300
    slider_initial_size_length=slider_initial_size_end-slider_initital_size_start

    slider_tile_type_start=2
    slider_tile_type_end=7

    slider_N_tiles_start= 1
    slider_N_tiles_end = 90
    slider_N_tiles_length=slider_N_tiles_end-slider_N_tiles_start

    def __init__(self, master=None):
        super(Application, self).__init__(master)
        self.pack()
        self.createWidgets()
        self.recursive_construction(N=2, size=1, rotate=pi, initial_size_scalar=50, tile_type=4)

    def createWidgets(self):
        self.canvas = tk.Canvas(self,width=self.canvas_width, height=self.canvas_height)
        # Switching Mac from "Dark Mode" to "Light Mode" "solves" a problem with the Button
        self.quitButton = tk.Button(self, text='Exit', command=self.quit)

        self.slider_dilation = tk.Scale(self, from_=self.slider_dilation_start, to=self.slider_dilation_end, orient="horizontal", length=self.canvas_width*0.9, label="Growth Rate", resolution=0.001)
        self.slider_dilation.set(1)
        self.slider_dilation.bind("<B1-Motion>", self.response)
        self.slider_dilation.bind("<ButtonRelease-1>", self.response)

        self.slider_dilation_point1 = tk.Scale(self, from_=self.slider_dilation_start, to=self.slider_dilation_end, orient="horizontal", length=self.canvas_width*0.5, label="Growth Rate step=0.1", resolution=0.1)

        self.slider_rotation = tk.Scale(self, from_=self.slider_rotation_start, to=self.slider_rotation_end, orient="horizontal", length=self.canvas_width*0.9, label="Rotation", resolution=0.0001)
        self.slider_rotation.set(pi)
        self.slider_rotation.bind("<B1-Motion>", self.response)
        self.slider_rotation.bind("<ButtonRelease-1>", self.response)

        self.slider_initial_size = tk.Scale(self, from_=self.slider_initital_size_start, to=self.slider_initial_size_end, orient="horizontal", length=self.canvas_width*0.5, label="Starting Size")
        self.slider_initial_size.set(50)
        self.slider_initial_size.bind("<B1-Motion>", self.response)
        self.slider_initial_size.bind("<ButtonRelease-1>", self.response)

        self.slider_tile_type= tk.Scale(self, from_=self.slider_tile_type_start, to=self.slider_tile_type_end, orient="vertical", length=self.canvas_width*0.5, label="Polygon")
        self.slider_tile_type.set(4)
        self.slider_tile_type.bind("<B1-Motion>", self.response)
        self.slider_tile_type.bind("<ButtonRelease-1>", self.response)

        self.slider_N_tiles = tk.Scale(self, from_=self.slider_initital_size_start, to=self.slider_N_tiles_end, orient="horizontal", length=self.canvas_width*0.5, label="N")
        self.slider_N_tiles.set(2)
        self.slider_N_tiles.bind("<B1-Motion>", self.response)
        self.slider_N_tiles.bind("<ButtonRelease-1>", self.response)

        self.quitButton.pack()
        self.slider_tile_type.pack(side="left")
        self.canvas.pack()
        self.slider_dilation.pack()
        self.slider_rotation.pack()
        self.slider_initial_size.pack()
        self.slider_N_tiles.pack()

    def render_tile(self, tile, skin):
        self.canvas.create_polygon(tile, outline='#000', fill=skin, width=1)
        #self.canvas.create_polygon(tile, outline='#000', fill="", width=1)

    def translate_tile(self, tile, translation=[0,0]):
        tile[0::2] = [x + translation[0] for x in tile[0::2]]
        tile[1::2] = [x + translation[1] for x in tile[1::2]]
        return tile

    def dilate_tile(self, tile, dilation=[1,1], dilate_origin=[0,0]):
        if dilate_origin == [0,0]:
            tile[0::2] = [x*dilation[0] for x in tile[0::2]]
            tile[1::2] = [x*dilation[1] for x in tile[1::2]]
            return tile
        else:
            return self.translate_tile(self.dilate_tile(self.translate_tile(tile, [-dilate_origin[0], -dilate_origin[1]]), dilation), dilate_origin)

    def rotate_tile(self, tile, rotate=0, rotate_origin=[0,0]):
        # Recall the generalized rotation,
        # R = | cos(t) -sin(t) |
        #     | sin(t)  cos(t) |
        c=cos(rotate)
        s=sin(rotate)
        R = np.array([[c, -s], [s, c]])
        T=tile
        if rotate_origin == [0,0]:
            # rotate each point -- but to execute matmul, the data must be structred into x,y arrays.
            T = [[np.matmul(t,R)  for t in [T[x:x+2] for x in range(0,len(T),2)]][i] for i in range(int(len(T)/2))]
            # Now undo the work of structuring the data into x,y arrays... convert back to a staight up list
            T = [T[i][j].tolist() for i in range(len(T)) for j in range(len(T[0]))]
            return T
        else:
            # translate the object to the origin by inverting the rotate rotate_origin
            # rotate around the origin
            # translate the object back to it's position by undoing the previous translation
            return self.translate_tile(self.rotate_tile(self.translate_tile(tile, [-rotate_origin[0], -rotate_origin[1]]), rotate), rotate_origin)

    def reflect_tile(self, tile, offset=0, axis='X'):
        if axis == 'X' or axis == 'x':
            tile = self.translate_tile(tile, [0,-offset])
            tile[1::2] = [x * -1 for x in tile[1::2]]
            tile = self.translate_tile(tile, [0,offset])
        else: # Assume "Y" intead
            tile = self.translate_tile(tile, [-offset,0])
            tile[0::2] = [x * -1 for x in tile[0::2]]
            tile = self.translate_tile(tile, [offset,0])
        return tile

    def unit_tile(self,V):
        # V is the number of vertices, an int
        # Kind of assumes tile are regular polygons -- but not really
        # Equilateral triangle
        if V == 3:
            A = [0, 0]
            B = [1, 0]
            # The angle is 60
            dx = cos(pi*60/180)
            dy = sin(pi*60/180)
            C = [B[0] - dx , B[1] + dy]
            return  A + B + C

        if V == 4:
            A = [0, 0]
            B = [1, 0]
            C = [1, 1]
            D = [0, 1]
            return  A + B + C + D

        if V == 9:
            A = [0, 0]
            B = [1, 0]
            # The angle is 180 less 108, ie 72
            dx = cos(pi*(180-108)/180)
            dy = sin(pi*(180-108)/180)
            C = [1 + dx , 0 + dy]
            E = [0 - dx, 0 + dy]
            dx = cos(pi*(180-2*108)/180)
            dy = sin(pi*(180-2*108)/180)
            D = [E[0] + dx, E[1] - dy]
            return  A + B + C + D + E

        if V == 6:
            A = [0, 0]
            B = [1, 0]
            # The angle is 180 less 60, 360/6
            dx = cos(pi*(180-60)/180)
            dy = sin(pi*(180-60)/180)
            C = [1 - dx , 0 + dy]
            F = [0 + dx, 0 + dy]
            dx = cos(pi*(180-2*60)/180)
            dy = sin(pi*(180-2*60)/180)
            D = [C[0] - dx, C[1] + dy]
            E = [F[0] + dx, F[1] + dy]
            return A + B + C + D + E  + F

        if V == 7:
            A = [0, 0]
            B = [1, 0]
            # The angle is 180 less 900/7
            dx = cos(pi*(180-900/7)/180)
            dy = sin(pi*(180-900/7)/180)
            C = [1 + dx , 0 + dy]
            G = [0 - dx, 0 + dy]
            dx = cos(pi*(180-2*900/7)/180)
            dy = sin(pi*(180-2*900/7)/180)
            D = [C[0] - dx, C[1] - dy]
            F = [G[0] + dx, G[1] - dy]
            dx = cos(pi*(180-3*900/7)/180)
            dy = sin(pi*(180-3*900/7)/180)
            E = [D[0] + dx, D[1] + dy]
            return A + B + C + D + E + F + G

        #if V == 20:
        if V == 5:
            A = [0, 0]
            B = [1, 0]
            # The angle is 180 less 108, ie 72
            dx = cos(pi*(180-108)/180)
            dy = sin(pi*(180-108)/180)
            C = [1 + dx , 0 + dy]
            E = [0 - dx, 0 + dy]
            dx = cos(pi*(180-2*108)/180)
            dy = sin(pi*(180-2*108)/180)
            D = [E[0] + dx, E[1] - dy]

            return A + C + E + B + D
            """
                A + B + C + D +
                E + F + G + H +
                I + J + K + L +
                M + N + O + P +
                Q + S + T + U
            """
        # Could return any old shape, really. Like this one:
        if V == 2:
                A = [0, 0]
                B = [1, 0]
                C = [1, 1]
                D = [0, 1]
                # The angle is 60
                dx = cos(pi*60/180)
                dy = sin(pi*60/180)
                E = [B[0] - dx , B[1] - dy]
                return  A + E + B + C + D

    def recursive_construction(self, N, size, rotate, initial_size_scalar, tile_type):
        initial_size = [initial_size_scalar, initial_size_scalar]
        dilation_factor = [(size/(self.slider_dilation_length/self.slider_dilation_denominator)), (size/(self.slider_dilation_length/self.slider_dilation_denominator))]
        if N == 1:
            self.canvas.delete("all")
            T = self.dilate_tile(self.unit_tile(tile_type), initial_size)
            T = self.translate_tile(T, [self.canvas_centre[0], self.canvas_centre[1]])
            # render a red tile (ie skin = '#F00')
            self.render_tile(T, skin='#F00')
        else:
            T = self.recursive_construction(N-1, size, rotate, initial_size_scalar, tile_type)
            T = self.rotate_tile(T[4::]+T[0:4], rotate=rotate, rotate_origin=[T[4],T[5]])
            T = self.dilate_tile(T, dilation_factor, [T[0],T[1]])
            # render a blue tile (ie skin = '#F00')
            self.render_tile(T, skin='#00F')
        return T

    def response(self, event):
        size = self.slider_dilation.get()
        rotate = self.slider_rotation.get()
        initial_size_scalar = self.slider_initial_size.get()
        tile_type = self.slider_tile_type.get()
        N_tiles = self.slider_N_tiles.get()
        self.recursive_construction(N_tiles, size, rotate, initial_size_scalar, tile_type)

app=Application()
app.master.title('Doodling')
app.mainloop()
