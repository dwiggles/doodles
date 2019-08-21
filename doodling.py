#!/usr/local/bin/python3
import tkinter as tk
import random as rnd

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
    slider_N_tiles_end = 20
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
        return tile

    def dilate_tile(self, tile, dilation=[1,1], dilate_origin=[0,0]):
        if dilate_origin == [0,0]:
            tile[0::2] = [x*dilation[0] for x in tile[0::2]]
            tile[1::2] = [x*dilation[1] for x in tile[1::2]]
            return tile
        else:
            return self.translate_tile(self.dilate_tile(self.translate_tile(tile, [-dilate_origin[0], -dilate_origin[1]]), dilation), dilate_origin)

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

    def recursive_construction(self, N, size, initial_size_scalar):
        initial_size = [initial_size_scalar, initial_size_scalar]
        dilation_factor = [(size/(self.slider_dilation_length/self.slider_dilation_denominator)), (size/(self.slider_dilation_length/self.slider_dilation_denominator))]

        if N == 1:
            self.canvas.delete("all")
            T = self.dilate_tile(self.unit_tile(4), initial_size)
            T = self.translate_tile(T, [self.canvas_centre[0], self.canvas_centre[1]])
        else:
            T=self.recursive_construction(N-1, size, initial_size_scalar)
            if N % 2 == 0:  #even
                T = self.dilate_tile(T, dilation_factor, [T[2],T[3]])
                T = self.reflect_tile(T, offset=T[3], axis='X')
            else: #odd
                T = self.dilate_tile(T, dilation_factor, [T[-2],T[-1]])
                T = self.reflect_tile(T, offset=T[-2], axis='Y')
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
