import math
from scipy.optimize import minimize
# Light up lights in sequential order, then take a photo of each one
# Do this 3 times 120 deg apart

# For each point:
    # Take the y pos from one image as the final 3d coord y pos
    # Rotate the second coord 120 deg and 3rd 240 deg then find the equation of the line from (0,-1) 
    # Then find the closest point to all 3 lines, this will give the x and z coord.

# Equations are stored in the form aX+bY+c=0 where (a,b,c)

class Light:
    def __init__(self) -> None:
        self.fin_x_coord = None
        self.fin_y_coord = None
        self.fin_z_coord = None

    def calc_final(self, first_coord, second_coord, third_coord):
        self.fin_y_coord = first_coord[1]
        # Rotate the coords
        second_coord = rotate_coord((second_coord[0],0), math.radians(120))
        second_coord_point = rotate_coord((0,-1), math.radians(120))
        third_coord = rotate_coord((third_coord[0],0), math.radians(240))
        third_coord_point = rotate_coord((0,-1), math.radians(240))

        # Find the 3 equations of the lines
        first_equ = calc_equ_line((first_coord[0],0), (0,-1))
        second_equ = calc_equ_line(second_coord, second_coord_point)
        third_equ = calc_equ_line (third_coord, third_coord_point)


        print("Line Equations:")
        print(f"1st Line: {first_equ}")
        print(f"2nd Line: {second_equ}")
        print(f"3rd Line: {third_equ}")

        # Find the closest point
        closest_point = find_closest_point([first_equ, second_equ, third_equ])
        self.fin_x_coord, self.fin_z_coord = closest_point
        print(f"Closest Point: {closest_point}")
   

def calc_equ_line(coord1, coord2):
    m = (coord2[1]-coord1[1])/(coord2[0]-coord1[0])
    return (-m, 1, m*coord1[0]-coord1[1])

def rotate_coord(coord, angle):
    new_x = (coord[0]*math.cos(angle)) - (coord[1]*math.sin(angle))
    new_y = (coord[0]*math.sin(angle)) + (coord[1]*math.cos(angle))
    return (new_x, new_y)

def find_closest_point(lines):
    """Find the point closest to all three lines."""
    def distance_squared(point, line):
        x, z = point
        a, b, c = line
        return ((a * x + b * z + c) ** 2) / (a**2 + b**2)

    def objective(point):
        return sum(distance_squared(point, line) for line in lines)

    # Initial guess for the minimizer
    initial_guess = (0, 0)
    result = minimize(objective, initial_guess, method='BFGS')
    return result.x

temp_light = Light()
temp_light.calc_final((10,100),(30,101),(80,100))