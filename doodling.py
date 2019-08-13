#!/usr/local/bin/python3
import tkinter as tk
import random as rnd

# Borrowing the oo approach from the Wikipedia example
class Application(tk.Frame):

    canvas_width=500
    canvas_height=canvas_width
    canvas_centre = [canvas_width/2, canvas_height/2]
    initial_size = 100
    def __init__(self, master=None):
        super(Application, self).__init__(master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.canvas = tk.Canvas(self,width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        self.quitButton = tk.Button(self, text='Exit', command=self.quit)
        self.quitButton.pack()
        self.slider = tk.Scale(self, from_=self.initial_size, to=self.initial_size+100, orient="horizontal", length=490)
        self.slider.bind("<ButtonRelease-1>", self.response)
        self.slider.pack()

    def render_triangle(self, triangle):
        # render a triangle
        self.canvas.create_line(triangle[0][0],triangle[0][1],triangle[1][0],triangle[1][1])
        self.canvas.create_line(triangle[1][0],triangle[1][1],triangle[2][0],triangle[2][1])
        self.canvas.create_line(triangle[2][0],triangle[2][1],triangle[0][0],triangle[0][1])

    def translate_triangle(self, triangle, translation=[0,0]):
        # translate it
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
                # do nothing to the input triangle; probably this should be flagged in a log
                return triangle
        else:
            # translate the object to the origin by inverting the rotate rotate_origin
            # rotate around the origin
            # translate the object back to it's position by undoing the previous translattion
            return self.translate_triangle(self.rotate_triangle(self.translate_triangle(triangle, [-rotate_origin[0], -rotate_origin[1]]), rotate), rotate_origin)

    def reflect_x_triangle(self, triangle):
        # Reflect in the x-axis
        return [
            [triangle[0][0], triangle[0][1] * -1],
            [triangle[1][0], triangle[1][1] * -1],
            [triangle[2][0], triangle[2][1] * -1]
            ]

    def reflect_y_triangle(self, triangle):
        # Reflect in the x-axis
        return [
            [triangle[0][0] * -1, triangle[0][1]],
            [triangle[1][0] * -1, triangle[1][1]],
            [triangle[2][0] * -1, triangle[2][1]]
            ]

    def unit_triangle(self):
       # the_points are A: 0,0, B: 1,0, C: 0,1
       A = [0, 0]
       B = [1, 0]
       C = [0, 1]
       #  return the_points
       return [ A, B, C ]

    def response(self, event):

        size = self.slider.get()
        if size < self.initial_size :
            size = self.initial_size
        # Create T1 and place it at the centre of the canvas with fixed size, initial_size
        T1 = self.translate_triangle(
            self.dilate_triangle( self.unit_triangle(),
                [self.initial_size, self.initial_size]), [self.canvas_centre[0]*1.5, self.canvas_centre[1]])

        # Now, for T2, use a dilate origin set to the lower right corner (?really)
        T2 = T1
        T2 = self.dilate_triangle(T2, [size/self.initial_size, size/self.initial_size], T2[1])
        T2 = self.translate_triangle(self.reflect_x_triangle(self.translate_triangle(T2, [0,-T2[1][1]])), [0,T2[1][1]])

        T3 = T2
        T3 = self.dilate_triangle(T3, [size/self.initial_size, size/self.initial_size], T3[2])
        T3 = self.translate_triangle(self.reflect_y_triangle(self.translate_triangle(T3, [-T3[2][0],0])), [T3[2][0],0])

        T4 = T3
        T4 = self.dilate_triangle(T4, [size/self.initial_size, size/self.initial_size], T4[1])
        T4 = self.translate_triangle(self.reflect_x_triangle(self.translate_triangle(T4, [0,-T4[1][1]])), [0,T4[1][1]])

        self.canvas.delete("all")
        self.render_triangle(T1)
        self.render_triangle(T2)
        self.render_triangle(T3)
        self.render_triangle(T4)

app=Application()
app.master.title('Doodling')
app.mainloop()
