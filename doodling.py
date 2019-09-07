#!/usr/local/bin/python3
import tkinter as tk
from math import sin, cos, pi
import numpy as np

class Application(tk.Frame):

    canvas_width=900
    canvas_height=500
    canvas_centre = [canvas_width/2, canvas_height/2]

    slider_dilation_start = 0
    slider_dilation_end = 2
    slider_dilation_length=slider_dilation_end-slider_dilation_start

    slider_dilation_denominator=2

    slider_initital_size_start= 1
    slider_initial_size_end = 300
    slider_initial_size_length=slider_initial_size_end-slider_initital_size_start

    slider_N_tiles_start= 1
    slider_N_tiles_end = 90
    slider_N_tiles_length=slider_N_tiles_end-slider_N_tiles_start

    def __init__(self, master=None):
        super(Application, self).__init__(master)
        self.pack()
        self.createWidgets()
        self.recursive_construction(2, 1, 50)

    def createWidgets(self):
        self.canvas = tk.Canvas(self,width=self.canvas_width, height=self.canvas_height)
        # Switching Mac from "Dark Mode" to "Light Mode" "solves" a problem with the Button
        self.quitButton = tk.Button(self, text='Exit', command=self.quit)

        self.slider_dilation = tk.Scale(self, from_=self.slider_dilation_start, to=self.slider_dilation_end, orient="horizontal", length=self.canvas_width*0.9, label="Growth Rate", resolution=0.001)
        self.slider_dilation.set(1)
        self.slider_dilation.bind("<B1-Motion>", self.response)
        self.slider_dilation.bind("<ButtonRelease-1>", self.response)

        self.slider_dilation_point1 = tk.Scale(self, from_=self.slider_dilation_start, to=self.slider_dilation_end, orient="horizontal", length=self.canvas_width*0.5, label="Growth Rate step=0.1", resolution=0.1)

        self.slider_initial_size = tk.Scale(self, from_=self.slider_initital_size_start, to=self.slider_initial_size_end, orient="horizontal", length=self.canvas_width*0.5, label="Starting Size")
        self.slider_initial_size.set(50)
        self.slider_initial_size.bind("<B1-Motion>", self.response)
        self.slider_initial_size.bind("<ButtonRelease-1>", self.response)

        self.slider_N_tiles = tk.Scale(self, from_=self.slider_initital_size_start, to=self.slider_N_tiles_end, orient="horizontal", length=self.canvas_width*0.5, label="N")
        self.slider_N_tiles.set(2)
        self.slider_N_tiles.bind("<B1-Motion>", self.response)
        self.slider_N_tiles.bind("<ButtonRelease-1>", self.response)

        self.quitButton.pack()
        self.canvas.pack()
        self.slider_dilation.pack()
        self.slider_initial_size.pack()
        self.slider_N_tiles.pack()

    def render_tile(self, tile):
        self.canvas.create_polygon(tile, outline='#000', fill='#888', width=1)

    def translate_tile(self, tile, translation=[0,0]):
        tile[0::2] = [x + translation[0] for x in tile[0::2]]
        tile[1::2] = [x + translation[1] for x in tile[1::2]]
        #tile[0::2] = [x + translation[0] for x in tile[0::2]]
        #tile[1::2] = [x + translation[1] for x in tile[1::2]]
        return tile

    def dilate_tile(self, tile, dilation=[1,1], dilate_origin=[0,0]):
        if dilate_origin == [0,0]:
            tile[0::2] = [x*dilation[0] for x in tile[0::2]]
            tile[1::2] = [x*dilation[1] for x in tile[1::2]]
            return tile
        else:
            return self.translate_tile(self.dilate_tile(self.translate_tile(tile, [-dilate_origin[0], -dilate_origin[1]]), dilation), dilate_origin)

    def rotate_tile(self, tile, rotate=0, rotate_origin=[0,0]):
        # rotate it -- around the origin (Modify this to rotate around any specified point)
        # this will be no "general" rotation, but instead it will be specifically a quarter turn
        # it will be a quarter turn multiplied by 1, 2 or 3.
        # First a single quarter turn
        # Recall the generalized rotation,
        # R = | cos(t) -sin(t) |
        #     | sin(t)  cos(t) |
        c=cos(rotate)
        s=sin(rotate)
        R = np.array([[c, -s], [s, c]])
        #T = np.transpose(np.array([tile[0::2], tile[1::2]]))
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
            # translate the object back to it's position by undoing the previous translattion
            return self.translate_tile(self.rotate_tile(self.translate_tile(tile, [-rotate_origin[0], -rotate_origin[1]]), rotate), rotate_origin)

    def reflect_tile(self, tile, offset=0, axis='X'):
        if axis == 'X' or axis == 'x':
            tile = self.translate_tile(tile, [0,-offset])
            #tile = self.dilate_tile(tile, [1,-1], dilate_origin=[0,-offset])
            tile[1::2] = [x * -1 for x in tile[1::2]]
            tile = self.translate_tile(tile, [0,offset])
        else: # Assume "Y" intead
            tile = self.translate_tile(tile, [-offset,0])
            #tile = self.dilate_tile(tile, [-1,1], dilate_origin=[-offset,0])
            tile[0::2] = [x * -1 for x in tile[0::2]]
            tile = self.translate_tile(tile, [offset,0])
        return tile

    def unit_tile(self,V):
        # V is the number of vertices, an int
        # Kind of assumes tile are regular polygons -- but not really
        if V == 3:
            A = [0, 0]
            B = [1, 0]
            C = [0, 1]
            return A + B + C
        if V == 4:
            A = [0, 0]
            B = [1, 0]
            C = [1, 1]
            D = [0, 1]
            return  A + B + C + D
        if V == 5:
            A = [0, 0]
            B = [1, 0]
            # The angle is 180 less 108, ie 72
            dx = cos(pi*72/180)
            dy = sin(pi*72/180)
            C = [1 + dx , 0 + dy]
            E = [0 - dx, 0 + dy]
            dx = cos(pi*36/180)
            dy = sin(pi*36/180)
            D = [E[0] + dx, E[1] + dy]
            return  A + B + C + D + E

    def recursive_construction(self, N, size, initial_size_scalar):
        initial_size = [initial_size_scalar, initial_size_scalar]
        dilation_factor = [(size/(self.slider_dilation_length/self.slider_dilation_denominator)), (size/(self.slider_dilation_length/self.slider_dilation_denominator))]
        if N == 1:
            self.canvas.delete("all")
            T = self.dilate_tile(self.unit_tile(5), initial_size)
            T = self.translate_tile(T, [self.canvas_centre[0], self.canvas_centre[1]])
            T = self.rotate_tile(T, rotate=2*3.1415926838/len(T), rotate_origin=[sum(T[0::2])/len(T)*2,sum(T[1::2])/len(T)*2])
        else:
            T=self.recursive_construction(N-1, size, initial_size_scalar)
            T = self.rotate_tile(T[2::]+T[0:2], rotate=2*3.1415926838/len(T), rotate_origin=[T[0],T[1]])
            T = self.dilate_tile(T,dilation_factor, [T[0],T[1]])
        self.render_tile(T)
        return T

    def response(self, event):
        size = self.slider_dilation.get()
        initial_size_scalar = self.slider_initial_size.get()
        N_tiles = self.slider_N_tiles.get()
        self.recursive_construction(N_tiles, size, initial_size_scalar)

app=Application()
app.master.title('Doodling')
app.mainloop()
