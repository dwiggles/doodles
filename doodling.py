
from tkinter import *
from random import *

tk = Tk()

canvas_width=500
canvas_height=canvas_width
canvas = Canvas(tk, width=canvas_width, height=canvas_height)
tk.title("Doodled")
canvas.pack()


def unit_triangle():
   # the_points are A: 0,0, B: 1,0, C: 0,1
   A = [0, 0]
   B = [1, 0]
   C = [0, 1]
   #  return the_points
   return [ A, B, C ]

print(unit_triangle())
print("1:", unit_triangle()[0])
print("2:", unit_triangle()[1])
print("3:", 100*unit_triangle()[2][0], 100*unit_triangle()[2][1])

def render_triangle(triangle=unit_triangle):
    # render a triangle
    canvas.create_line(triangle[0][0],triangle[0][1],triangle[1][0],triangle[1][1])
    canvas.create_line(triangle[1][0],triangle[1][1],triangle[2][0],triangle[2][1])
    canvas.create_line(triangle[2][0],triangle[2][1],triangle[0][0],triangle[0][1])

def translate_triangle(triangle, translation=[0,0]):
    # translate it
        return [
                [triangle[0][0] + translation[0], triangle[0][1] + translation[1]], 
                [triangle[1][0] + translation[0], triangle[1][1] + translation[1]], 
                [triangle[2][0] + translation[0], triangle[2][1] + translation[1]] 
            ]

def dilate_triangle(triangle, dilation=1):
    # dilate it relative to the viewport origin
        return [
                [triangle[0][0] * dilation[0], triangle[0][1] * dilation[1]], 
                [triangle[1][0] * dilation[0], triangle[1][1] * dilation[1]], 
                [triangle[2][0] * dilation[0], triangle[2][1] * dilation[1]] 
            ]
	     
def rotated_triangle(triangle, rotate=0):
    # rotate it
	return triangle

render_triangle([[5,5],[100, 5],[5, 100]])

# I would like to render many random triangles.
seed(1)

# NOTE: randint(0, canvas_width) -- does the "obvious"... right?
def totally_random():
    for i in range(10):
        render_triangle([
            [randint(0, canvas_width), randint(0, canvas_height)], 
            [randint(0, canvas_width), randint(0, canvas_height)], 
            [randint(0, canvas_width), randint(0, canvas_height)]]) 


def arbitrary_xforms():
    render_triangle(translate_triangle(unit_triangle(), [100, 100]))
    render_triangle(translate_triangle(unit_triangle(), [100, 150]))
    render_triangle(translate_triangle(unit_triangle(), [100, 150]))
    render_triangle(translate_triangle(unit_triangle(), [150, 150]))

arbitrary_xforms()
        

# So that's the random triangles. But what about some other triangles. Less random?
# Starting with a single, small right-angle triangle in the middle. 



canvas.mainloop()

