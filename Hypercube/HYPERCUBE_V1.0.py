import pygame
import pygame_gui
import os
import math
global resolution
resolution = [1080, 720]

####### GROUP A - COMPLEX MATHEMATICS ####### (Matrix Multiplication) (Rotation Matrices)

def matrix_multiply(a, b): # This mulitplies two matrices together to return a resulting matrix.
    columns_a = len(a[0])
    rows_a = len(a)
    columns_b = len(b[0])
    rows_b = len(b)

    result_matrix = [[j for j in range(columns_b)] for i in range(rows_a)]
    if columns_a == rows_b:
        for x in range(rows_a):
            for y in range(columns_b):
                sum_ = 0
                for k in range(columns_a):
                    sum_ += a[x][k] * b[k][y]
                result_matrix[x][y] = sum_

        return result_matrix

    else:
        print("columns of the first matrix must be equal to the rows of the second matrix")
        return None

def rotation3D_matrices(angle): # Matrix formulas for rotation in 3D.
    x = [
        [1, 0, 0],
        [0, math.cos(angle[0]), -math.sin(angle[0])],
        [0, math.sin(angle[0]), math.cos(angle[0])]
        ]

    y = [
        [math.cos(angle[1]), 0, -math.sin(angle[1])],
        [0, 1, 0],
        [math.sin(angle[1]), 0, math.cos(angle[1])]
        ]

    z = [
        [math.cos(angle[2]), -math.sin(angle[2]), 0],
        [math.sin(angle[2]), math.cos(angle[2]), 0],
        [0, 0, 1]
        ]

    return x, y, z

def rotation4D_matrices(angle): # Matrix formulas for rotation in 4D.
    
    xy = [[math.cos(angle[0]), -math.sin(angle[0]), 0, 0],
          [math.sin(angle[0]), math.cos(angle[0]), 0, 0],
          [0, 0, 1, 0],
          [0, 0, 0, 1]]
    xz = [[math.cos(angle[1]), 0, -math.sin(angle[1]), 0],
          [0, 1, 0, 0],
          [math.sin(angle[1]), 0, math.cos(angle[1]), 0],
          [0, 0, 0, 1]]
    xw = [[math.cos(angle[2]), 0, 0, -math.sin(angle[2])],
          [0, 1, 0, 0],
          [0, 0, 1, 0],
          [math.sin(angle[2]), 0, 0, math.cos(angle[2])]]
    yz = [[1, 0, 0, 0],
          [0, math.cos(angle[3]), -math.sin(angle[3]), 0],
          [0, math.sin(angle[3]), math.cos(angle[3]), 0],
          [0, 0, 0, 1]]
    yw = [[1, 0, 0, 0],
          [0, math.cos(angle[4]), 0, -math.sin(angle[4])],
          [0, 0, 1, 0],
          [0, math.sin(angle[4]), 0, math.cos(angle[4])]]
    zw = [[1, 0, 0, 0],
          [0, 1, 0, 0],
          [0, 0, math.cos(angle[5]), -math.sin(angle[5])],
          [0, 0, math.sin(angle[5]), math.cos(angle[5])]]
    
    return [xy, xz, xw, yz, yw, zw]

def connect_point(x, y, projection, offset): # Connects points in 4D (with offset)
    X = projection[x + offset]
    Y = projection[y + offset]
    pygame.draw.line(screen, black, (X[0], X[1]), (Y[0], Y[1]), 5)

def connect_point3D(x, y, projection):  # Connects points in 3D (without offset)
    X = projection[x]
    Y = projection[y]
    pygame.draw.line(screen, black, (X[0], X[1]), (Y[0], Y[1]), 5)

####### GROUP B - OOP Model #######
    
class Button: # This class is used to create the button from scratch using Pygame for the 4D/3D switch.
    def __init__(self, image, position):
        self.image = image
        self.rect = image.get_rect(topleft=position)

    def clicked(self, event):
        if event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
            else:
                return False

####### GROUP A - OOP Model ####### (Classes + Subclasses + Inheritance)
            
class Shape: # This is the superclass for both shapes in my program.
    def __init__(self, size, angles, position):
        self.angles = angles
        self.position = position
        self.scale = size

class Cube(Shape): # This is a child of the 'Shape' superclass, it is a Cube (3D) object.
    def __init__(self, size, angles, position):
        super().__init__(size, angles, position) # Inheritance of the superclass's attributes.
        self.projected_vertices = [0,1,2,3,4,5,6,7] ####### GROUP C - Single-dimensional Array #######
        self.c_vertices = [ ####### GROUP B - Multi-dimensional Array #######
            [[-1], [-1], [1]],
            [[1], [-1], [1]],
            [[1], [1], [1]],
            [[-1], [1], [1]],
            [[-1], [-1], [-1]],
            [[1], [-1], [-1]],
            [[1], [1], [-1]],
            [[-1], [1], [-1]]
            ]

    def Draw(self): # This creates an instance of a cube at a specified angle.
        i = 0
        for vertex in self.c_vertices:
            Xrotation, Yrotation, Zrotation = rotation3D_matrices(self.angles)
            rotation = vertex
            rotation = matrix_multiply(Xrotation, rotation)
            rotation = matrix_multiply(Yrotation, rotation)
            rotation = matrix_multiply(Zrotation, rotation)

            z = 1/(12-rotation[2][0]) # This creates the constant for the projection matrix.
            projection_matrix = [[z, 0, 0], # This projects the 3D points into 2D.
                                 [0, z, 0]]

            projection = matrix_multiply(projection_matrix, rotation) # Applying the projection matrix.

            # Getting the x and y coordinates of the new vertex in 2D.
            x = int(projection[0][0] * self.scale) + self.position[0]
            y = int(projection[1][0] * self.scale) + self.position[1]
            self.projected_vertices[i] = [x,y] # Adding them to the array.

            i += 1

        # Connecting all of the points together on the screen to make a cube.
        connect_point3D(0,1,self.projected_vertices)
        connect_point3D(1,2,self.projected_vertices)
        connect_point3D(2,3,self.projected_vertices)
        connect_point3D(3,0,self.projected_vertices)
        connect_point3D(4,5,self.projected_vertices)
        connect_point3D(5,6,self.projected_vertices)
        connect_point3D(6,7,self.projected_vertices)
        connect_point3D(7,4,self.projected_vertices)
        connect_point3D(0,4,self.projected_vertices)
        connect_point3D(1,5,self.projected_vertices)
        connect_point3D(2,6,self.projected_vertices)
        connect_point3D(3,7,self.projected_vertices)

class HyperCube(Shape): # This is a child of the 'Shape' superclass, it is a Hypercube (4D) object.
    def __init__(self, size, angles, position):
        super().__init__(size, angles, position) # Inheritance of the superclass's attributes.
        self.projected_points = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15] ####### GROUP C - Single-dimensional Array #######
        self.vertices = [ ####### GROUP B - Multi-dimensional Array #######
            [[-1], [-1], [1], [1]],
            [[1], [-1], [1], [1]],
            [[1], [1], [1], [1]],
            [[-1], [1], [1], [1]],
            [[-1], [-1], [-1], [1]],
            [[1], [-1], [-1], [1]],
            [[1], [1], [-1], [1]],
            [[-1], [1], [-1], [1]],
            [[-1], [-1], [1], [-1]],
            [[1], [-1], [1], [-1]],
            [[1], [1], [1], [-1]],
            [[-1], [1], [1], [-1]],
            [[-1], [-1], [-1], [-1]],
            [[1], [-1], [-1], [-1]],
            [[1], [1], [-1], [-1]],
            [[-1], [1], [-1], [-1]]
            ]
        self.tesseract_rotation = [[1, 0, 0], ####### GROUP A - COMPLEX MATHEMATICS #######
            [0, math.cos(-math.pi/2), -math.sin(-math.pi/2)],
            [0, math.sin(-math.pi/2), math.cos(-math.pi/2)]]
        
    def Draw(self): # This creates an instance of a hypercube at a specified angle.
        i = 0
        rotations = rotation4D_matrices(self.angles)
        for vertex in self.vertices:
            rotated_3D = vertex
            for n in range(6):
                rotated_3D = matrix_multiply(rotations[n], rotated_3D) # Performs rotations on the vertices from every rotation matrix.
            distance = 5
            width = 1/(distance - rotated_3D[3][0]) # Creating the constant for the projection matrix.
            projection_matrix4Dto3D = [[width, 0, 0, 0],
                                       [0, width, 0, 0],
                                       [0, 0, width, 0]] # This matrix removes the fourth row of the matrix, projecting it from 4D into 3D.
            
            projected_3D = matrix_multiply(projection_matrix4Dto3D, rotated_3D) # Applying the projection matrix.
            rotated_2D = matrix_multiply(self.tesseract_rotation, projected_3D) 
            z = 1/(distance - (rotated_2D[2][0] + rotated_3D[3][0])) # Creating the constant for the projection matrix.
            projection_matrix = [[z, 0, 0], # This matrix removes the third dimension, allowing it to be drawn on a 2D screen.
                                 [0, z, 0]]
            projected_2D = matrix_multiply(projection_matrix, rotated_2D) # Applies the projection matrix.
            
            # Getting the x and y coordinates of the new vertex in 2D.
            x = int(projected_2D[0][0] * self.scale) + self.position[0]
            y = int(projected_2D[1][0] * self.scale) + self.position[1]
            self.projected_points[i] = [x,y] # Adding them to the array.
            i += 1

        # Shortened way of connecting all the points instead of typing them all.
        for m in range(4):
            connect_point(m, (m+1)%4, self.projected_points, 8)
            connect_point(m+4, (m+1)%4 + 4, self.projected_points, 8)
            connect_point(m, m+4, self.projected_points, 8)

        for m in range(4):
            connect_point(m, (m+1)%4, self.projected_points, 0)
            connect_point(m+4, (m+1)%4 + 4, self.projected_points, 0)
            connect_point(m, m+4, self.projected_points, 0)

        for m in range(8):
            connect_point(m,  m+8, self.projected_points, 0)


def Main():
    width, height = 1080, 720
    xy = 0
    xz = 0
    xw = 0
    yz = 0
    yw = 0
    zw = 0
    scale = 2400
    position = [resolution[0]//4*3, resolution[1]//2]
    font = pygame.font.SysFont('cour.ttf', 80)
    font2 = pygame.font.SysFont('cour.ttf',25)
    menu = True
    viewer = False

    # This loops allows the user to go back and forth from menu to viewer.
    while True:
        
        if menu == True:
            # Creating the two menu buttons.
            viewer_button = pygame_gui.elements.ui_button.UIButton(relative_rect=pygame.Rect((int(width/2 - 250), height//2+60),(int(500), int(100))), text="HYPERCUBE VIEWER", manager=manager)
            quit_button = pygame_gui.elements.ui_button.UIButton(relative_rect=pygame.Rect((int(width/2 - 125), height//4*3),(int(250), int(75))), text="QUIT", manager=manager)
            
            while menu:
                clock.tick(fps)
                time_delta = clock.tick(fps)/1000
                screen.fill(white)

                for event in pygame.event.get():
                    manager.process_events(event)



                # This part is for the rotating hypercube on the menu screen.
                angles_4D = [xy,xz,xw,yz,yw,zw]

                if xy >= math.pi*2:
                    xy = 0
                if xz >= math.pi*2:
                    xz = 0
                if xw >= math.pi*2:
                    xw = 0
                if yz >= math.pi*2:
                    yz = 0
                if yw >= math.pi*2:
                    yw = 0
                if zw >= math.pi*2:
                    zw = 0
                
                Menu_Tesseract = HyperCube(1800, angles_4D, [width//2, height//3-30])
                Menu_Tesseract.Draw()
                xy += 0.01
                xz += 0.01
                xw += 0.01
                yz += 0.01
                yw += 0.01
                zw += 0.01
                
                if viewer_button.check_pressed():
                    menu = False
                    viewer = True
                    viewer_button.hide()
                    quit_button.hide()

                if quit_button.check_pressed():
                    quit()

                # Render GUI and Draw pygame objects.
                manager.update(time_delta)
                manager.draw_ui(screen)
                pygame.display.update()

                
        elif viewer == True:
            
            # Setting up all the GUI elements: Title, Sliders, Textboxes, Buttons.
            
            img = font.render('HYPERCUBE VIEWER', True, (20,20,20))
            img_pos = img.get_rect(center=(width//2,50))

            XY_label = font2.render('XY', True, (20,20,20))
            XY_label_pos = XY_label.get_rect(center=(width//2-70,height/20*8+12))
            XZ_label = font2.render('XZ', True, (20,20,20))
            XZ_label_pos = XZ_label.get_rect(center=(width//2-72,height/20*9+12))
            YZ_label = font2.render('YZ', True, (20,20,20))
            YZ_label_pos = YZ_label.get_rect(center=(width//2-72,height/20*7+12))
            XW_label = font2.render('XW', True, (20,20,20))
            XW_label_pos = XW_label.get_rect(center=(width//2-67,height/20*10+12))
            YW_label = font2.render('YW', True, (20,20,20))
            YW_label_pos = YW_label.get_rect(center=(width//2-69,height/20*11+12))
            ZW_label = font2.render('ZW', True, (20,20,20))
            ZW_label_pos = ZW_label.get_rect(center=(width//2-67,height/20*12+12))

            Y_label = font2.render('Y', True, (20,20,20))
            Y_label_pos = Y_label.get_rect(center=(width//2-76,height/20*8+12))
            Z_label = font2.render('Z', True, (20,20,20))
            Z_label_pos = Z_label.get_rect(center=(width//2-76,height/20*9+12))
            X_label = font2.render('X', True, (20,20,20))
            X_label_pos = X_label.get_rect(center=(width//2-76,height/20*7+12))
            
            XY_slider = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(relative_rect=pygame.Rect((int(width/20), height-int(height/20*12)),(int(width/8*3), int(height/30))), start_value=xy, value_range=(0,math.pi*2),manager=manager)
            XZ_slider = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(relative_rect=pygame.Rect((int(width/20), height-int(height/20*11)),(int(width/8*3), int(height/30))), start_value=xz, value_range=(0,math.pi*2),manager=manager)
            XW_slider = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(relative_rect=pygame.Rect((int(width/20), height-int(height/20*10)),(int(width/8*3), int(height/30))), start_value=xw, value_range=(0,math.pi*2),manager=manager)
            YZ_slider = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(relative_rect=pygame.Rect((int(width/20), height-int(height/20*13)),(int(width/8*3), int(height/30))), start_value=yz, value_range=(0,math.pi*2),manager=manager)
            YW_slider = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(relative_rect=pygame.Rect((int(width/20), height-int(height/20*9)),(int(width/8*3), int(height/30))), start_value=yw, value_range=(0,math.pi*2),manager=manager)
            ZW_slider = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(relative_rect=pygame.Rect((int(width/20), height-int(height/20*8)),(int(width/8*3), int(height/30))), start_value=zw, value_range=(0,math.pi*2),manager=manager)

            XY_textbox = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((int(width/100), height - int(height/20*12)),(int(width/28), int(height/30))), manager=manager)
            XY_textbox.set_text(str(int(xy*57.2958)))
            XZ_textbox = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((int(width/100), height - int(height/20*11)),(int(width/28), int(height/30))), manager=manager)
            XZ_textbox.set_text(str(int(xz*57.2958)))
            XW_textbox = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((int(width/100), height - int(height/20*10)),(int(width/28), int(height/30))), manager=manager)
            XW_textbox.set_text(str(int(xw*57.2958)))
            YZ_textbox = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((int(width/100), height - int(height/20*13)),(int(width/28), int(height/30))), manager=manager)
            YZ_textbox.set_text(str(int(yz*57.2958)))
            YW_textbox = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((int(width/100), height - int(height/20*9)),(int(width/28), int(height/30))), manager=manager)
            YW_textbox.set_text(str(int(yw*57.2958)))
            ZW_textbox = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((int(width/100), height - int(height/20*8)),(int(width/28), int(height/30))), manager=manager)
            ZW_textbox.set_text(str(int(zw*57.2958)))
            
            reset_values = pygame_gui.elements.ui_button.UIButton(relative_rect=pygame.Rect((int(width/20), height/3*2),(int(250), int(50))), text="Reset Values", manager=manager)
            back_button = pygame_gui.elements.ui_button.UIButton(relative_rect=pygame.Rect((int(width/30), height/10*9),(int(150), int(50))), text="Back to Menu", manager=manager)
            
            switch_image = pygame.image.load('switch.png')
            switch_image1= pygame.image.load('switch2.png')
            dimension_switch = Button(switch_image, (10, 10))
            
            hypercube_ = True

            # The following loop is where everything is rendered in the hypercube viewer.
            while viewer:
                clock.tick(fps)
                time_delta = clock.tick(fps)/1000
                screen.fill(white)

                for event in pygame.event.get(): # Takes all the user inputs.
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        hyper = dimension_switch.clicked(event)
                        if hyper: # Switches between hypercube and cube.
                            if hypercube_:
                                hypercube_ = False
                                XW_slider.hide()
                                YW_slider.hide()
                                ZW_slider.hide()
                                XW_textbox.hide()
                                YW_textbox.hide()
                                ZW_textbox.hide()
                            else:
                                hypercube_ = True
                                XW_slider.show()
                                YW_slider.show()
                                ZW_slider.show()
                                XW_textbox.show()
                                YW_textbox.show()
                                ZW_textbox.show()
                            print(hypercube_)
                    
                    manager.process_events(event)

                
                screen.blit(dimension_switch.image, dimension_switch.rect) # render switch

                if hypercube_:
                    screen.blit(switch_image1, (10,10))
                  
                screen.blit(img, img_pos)  # render text

                # Getting slider values for the rotation

                xy = XY_slider.get_current_value() ; XY_textbox.set_text(str(int(xy*57.2958)))     
                xz = XZ_slider.get_current_value() ; XZ_textbox.set_text(str(int(xz*57.2958)))
                xw = XW_slider.get_current_value() ; XW_textbox.set_text(str(int(xw*57.2958)))
                yz = YZ_slider.get_current_value() ; YZ_textbox.set_text(str(int(yz*57.2958)))
                yw = YW_slider.get_current_value() ; YW_textbox.set_text(str(int(yw*57.2958)))
                zw = ZW_slider.get_current_value() ; ZW_textbox.set_text(str(int(zw*57.2958)))
                
                angles_4D = [xy,xz,xw,yz,yw,zw]

                angles_3D = [yz,math.pi * 2 - xy,xz]

                # Reset rotation if button is pressed
                if reset_values.check_pressed():
                    angles_4D = [0, 0, 0, 0, 0, 0]
                    XY_slider.set_current_value(0)
                    XZ_slider.set_current_value(0)
                    XW_slider.set_current_value(0)
                    YZ_slider.set_current_value(0)
                    YW_slider.set_current_value(0)
                    ZW_slider.set_current_value(0)
                    angles_3D = [0, 0, 0]
                    
                if hypercube_: # If switch is set to 4D, draw hypercube, else, draw cube.
                    Tesseract = HyperCube(scale, angles_4D, position)
                    Tesseract.Draw()
                    screen.blit(XY_label, XY_label_pos)
                    screen.blit(XZ_label, XZ_label_pos)
                    screen.blit(YZ_label, YZ_label_pos)
                    screen.blit(XW_label, XW_label_pos)
                    screen.blit(YW_label, YW_label_pos)
                    screen.blit(ZW_label, ZW_label_pos)
                else:
                    Cube_ = Cube(1800, angles_3D, position)
                    Cube_.Draw()
                    screen.blit(X_label, X_label_pos)
                    screen.blit(Y_label, Y_label_pos)
                    screen.blit(Z_label, Z_label_pos)

                if back_button.check_pressed(): # Back to menu, hide current GUI.
                    menu = True
                    viewer = False
                    back_button.hide()
                    reset_values.hide()

                    XW_slider.hide()
                    YW_slider.hide()
                    ZW_slider.hide()
                    XY_slider.hide()
                    YZ_slider.hide()
                    XZ_slider.hide()
                    
                    XW_textbox.hide()
                    YW_textbox.hide()
                    ZW_textbox.hide()
                    XY_textbox.hide()
                    YZ_textbox.hide()
                    XZ_textbox.hide()
                
            
                manager.update(time_delta)
                manager.draw_ui(screen)
                pygame.display.update()
            

# Initialising everything for Pygame window + program.

os.environ["SDL_VIDEO_CENTERED"]='1'
black, white = (20, 20, 20), (230, 230, 230)
pygame.init()
pygame.display.set_caption("Hypercube Viewer by Connor Groom")
width, height = resolution[0], resolution[1]
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

fps = 60
manager = pygame_gui.UIManager((width, height))

Main()

            




















            
            
        
        
        
