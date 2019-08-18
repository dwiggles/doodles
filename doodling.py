#!/usr/local/bin/python3
import tkinter as tk
import random as rnd

class Application(tk.Frame):

    canvas_width=500
    canvas_height=400
    canvas_centre = [canvas_width/2, canvas_height/2]


    slider_dilation_start = 0
    slider_dilation_end = 2
    slider_dilation_length=slider_dilation_end-slider_dilation_start

    slider_dilation_denominator=2

    slider_initital_size_start= 1
    slider_initial_size_end = 100
    slider_initial_size_length=slider_initial_size_end-slider_initital_size_start

    slider_N_triangles_start= 1
    slider_N_triangles_end = 100
    slider_N_triangles_length=slider_N_triangles_end-slider_N_triangles_start

    def __init__(self, master=None):
        super(Application, self).__init__(master)
        self.pack()
        self.createWidgets()
        self.recursive_construction(2, 1, 50)

    def createWidgets(self):
        self.canvas = tk.Canvas(self,width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        # Switching Mac from "Dark Mode" to "Light Mode" "solves" a problem with the Button
        self.quitButton = tk.Button(self, text='Exit', command=self.quit)

        self.slider_dilation = tk.Scale(self, from_=self.slider_dilation_start, to=self.slider_dilation_end, orient="horizontal", length=self.canvas_width/2, label="Growth Rate", resolution=0.001)
        self.slider_dilation.set(1)
        self.slider_dilation.bind("<B1-Motion>", self.response)
        self.slider_dilation.bind("<ButtonRelease-1>", self.response)

        self.slider_dilation_point1 = tk.Scale(self, from_=self.slider_dilation_start, to=self.slider_dilation_end, orient="horizontal", length=self.canvas_width/2, label="Growth Rate step=0.1", resolution=0.1)

        self.slider_initial_size = tk.Scale(self, from_=self.slider_initital_size_start, to=self.slider_initial_size_end, orient="horizontal", length=self.canvas_width/2, label="Starting Size")
        self.slider_initial_size.set(50)
        self.slider_initial_size.bind("<B1-Motion>", self.response)
        self.slider_initial_size.bind("<ButtonRelease-1>", self.response)

        self.slider_N_triangles = tk.Scale(self, from_=self.slider_initital_size_start, to=self.slider_N_triangles_end, orient="horizontal", length=self.canvas_width/2, label="N")
        self.slider_N_triangles.set(2)
        self.slider_N_triangles.bind("<B1-Motion>", self.response)
        self.slider_N_triangles.bind("<ButtonRelease-1>", self.response)

        self.slider_dilation.pack()
        self.slider_initial_size.pack()
        self.slider_N_triangles.pack()
        self.quitButton.pack()

    def render_triangle(self, triangle):
        self.canvas.create_line(triangle[0][0],triangle[0][1],triangle[1][0],triangle[1][1])
        self.canvas.create_line(triangle[1][0],triangle[1][1],triangle[2][0],triangle[2][1])
        self.canvas.create_line(triangle[2][0],triangle[2][1],triangle[0][0],triangle[0][1])

    def translate_triangle(self, triangle, translation=[0,0]):
        return [
            [triangle[0][0] + translation[0], triangle[0][1] + translation[1]],
            [triangle[1][0] + translation[0], triangle[1][1] + translation[1]],
            [triangle[2][0] + translation[0], triangle[2][1] + translation[1]]
            ]

    def dilate_triangle(self, triangle, dilation=[1,1], dilate_origin=[0,0]):
        if dilate_origin == [0,0]:
            return [
                [triangle[0][0] * dilation[0], triangle[0][1] * dilation[1]],
                [triangle[1][0] * dilation[0], triangle[1][1] * dilation[1]],
                [triangle[2][0] * dilation[0], triangle[2][1] * dilation[1]]
                ]
        else:
            return self.translate_triangle(self.dilate_triangle(self.translate_triangle(triangle, [-dilate_origin[0], -dilate_origin[1]]), dilation), dilate_origin)

    def rotate_triangle(self, triangle, rotate=1, rotate_origin=[0,0]):
        # rotate it -- around the origin (Modify this to rotate around any specified point)
        # this will be no "general" rotation, but instead it will be specifically a quarter turn
        # it will be a quarter turn multiplied by 1, 2 or 3.
        # First a single quarter turn
        if rotate_origin == [0,0]:
            if rotate==1:
                return [
                    [triangle[0][1] * -1, triangle[0][0] * 1],
                    [triangle[1][1] * -1, triangle[1][0] * 1],
                    [triangle[2][1] * -1, triangle[2][0] * 1]
                    ]
            elif rotate==2:
                return self.rotate_triangle(self.rotate_triangle(triangle, 1, rotate_origin), 1, rotate_origin)
            elif rotate==3:
                return self.rotate_triangle(self.rotate_triangle(triangle, 1, rotate_origin), 2, rotate_origin)
            else:
                # do nothing; probably this should be flagged in a log
                return triangle
        else:
            # translate the object to the origin by inverting the rotate rotate_origin
            # rotate around the origin
            # translate the object back to it's position by undoing the previous translattion
            return self.translate_triangle(self.rotate_triangle(self.translate_triangle(triangle, [-rotate_origin[0], -rotate_origin[1]]), rotate), rotate_origin)

    def reflect_triangle(self, triangle, offset=0, axis='X'):
        if axis == 'X' or axis == 'x':
            triangle = self.translate_triangle(triangle, [0,-offset])
            triangle = [
                [triangle[0][0], triangle[0][1] * -1],
                [triangle[1][0], triangle[1][1] * -1],
                [triangle[2][0], triangle[2][1] * -1]
                ]
            triangle = self.translate_triangle(triangle, [0,offset])
        else: # Assume "Y" intead
            triangle = self.translate_triangle(triangle, [-offset,0])
            triangle = [
                [triangle[0][0] * -1, triangle[0][1]],
                [triangle[1][0] * -1, triangle[1][1]],
                [triangle[2][0] * -1, triangle[2][1]]
                ]
            triangle = self.translate_triangle(triangle, [offset,0])
        return triangle

    def unit_triangle(self):
       A = [0, 0]
       B = [1, 0]
       C = [0, 1]
       return [ A, B, C ]

    def response_dilation_high_res(self, event):
        size = self.slider_dilation.get()
        self.response(event)

    def response_dilation_point1_res(self, event):
        size = self.slider_dilation_point1.get()
        self.response(event)

    def recursive_construction(self, N, size, initial_size_scalar):
        initial_size = [initial_size_scalar, initial_size_scalar]
        dilation_factor = [(size/(self.slider_dilation_length/self.slider_dilation_denominator)), (size/(self.slider_dilation_length/self.slider_dilation_denominator))]

        if N == 1:
            self.canvas.delete("all")

            T = self.dilate_triangle(self.unit_triangle(), initial_size)
            T = self.translate_triangle(T, [self.canvas_centre[0]*1.5, self.canvas_centre[1]])
            self.render_triangle(T)
        else:
            T=self.recursive_construction(N-1, size, initial_size_scalar)
            if N % 2 == 0:  #even
                T = self.dilate_triangle(T, dilation_factor, T[1])
                T = self.reflect_triangle(T, offset=T[1][1], axis='X')
            else: #odd
                T = self.dilate_triangle(T, dilation_factor, T[2])
                T = self.reflect_triangle(T, offset=T[2][0], axis='Y')
            self.render_triangle(T)
        # Notice that in the base case, the returned value is not processed.
        return T

    def response(self, event):
        size = self.slider_dilation.get()
        initial_size_scalar = self.slider_initial_size.get()
        N_triangles = self.slider_N_triangles.get()
        self.recursive_construction(N_triangles, size, initial_size_scalar)

app=Application()
app.master.title('Doodling')
app.mainloop()
