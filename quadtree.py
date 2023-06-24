'''Defines the QuadTree class used to group data into QuadTree Tree data structure'''
#Implemented with the aid of: https://www.youtube.com/watch?v=RKODYaueSvw
import numpy as np

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Rectangle:
    def __init__(self, corner, width, height): #defines a rectangle given its bottom left corner, his width and his height
        self.corner = corner #a Point class object
        self.width = width
        self.height = height

        #defines boundaries of the Rectangle
        self.left = corner.x
        self.top = corner.y + height
        self.right = corner.x + width
        self.bottom = corner.y

    def ContainsData(self, data):
        '''checks for the data properties x and y return the binary value of the condition involving Rectangle class
        parameters'''
        return (self.left <= data.x < self.right and self.bottom <= data.y < self.top) 

    def draw(self, ax, c = 'k', lw = 1, alpha = 1, **kwargs):
        x1, y1 = self.left, self.bottom
        x2, y2 = self.right, self.top
        ax.plot([x1, x1, x2, x2, x1],[y1, y2, y2, y1, y1], c = c, lw = lw, **kwargs)

class TreeNode:
    def __init__(self, boundaries, capacity = 1): #capacity argument is just for testing
        self.boundaries = boundaries
        self.capacity = capacity

        self.StoredData = []
        self.divided = False #checks if the current node has been already divided

    def insert(self, data):
        #checks if the data is in the boundaries (rectangle of given width and height from its corner), all the 
        #binary values are assigned to know which QuadTree the given data below
        if not self.boundaries.ContainsData(data):
            return False
        
        #checks if the Node is avaliable for storing data
        if len(self.StoredData) < self.capacity:
            #Adds data to the StoredData list and sets the square s parameter of the particle to use it with MAC
            self.StoredData.append(data)
            data.s = np.sqrt(self.boundaries.width**2 + self.boundaries.height**2)
            return True
    
        if not self.divided:
            self.divide()

        if self.nw.insert(data):
            return True
        elif self.ne.insert(data):
            return True
        elif self.se.insert(data):
            return True
        elif self.sw.insert(data):
            return True
        
        #if for any reason the point is not added to any QuadTree
        return False

    def divide(self):
        x_corner = self.boundaries.corner.x
        y_corner = self.boundaries.corner.y
        new_width = 0.5*self.boundaries.width
        new_height = 0.5*self.boundaries.height

        #define childs
        nw = Rectangle(Point(x_corner, y_corner + new_height), new_width, new_height)
        self.nw = TreeNode(nw)
        
        ne = Rectangle(Point(x_corner + new_width, y_corner + new_height), new_width, new_height)
        self.ne = TreeNode(ne)
        
        se = Rectangle(Point(x_corner + new_width, y_corner), new_width, new_height)
        self.se = TreeNode(se)
        
        sw = Rectangle(Point(x_corner, y_corner), new_width, new_height)
        self.sw = TreeNode(sw)
        
        self.divided = True

    def __len__(self):
        count = len(self.StoredData)
        if self.divided:
            count += len(self.nw) + len(self.ne) + len(self.se) + len(self.sw)

        return count
    
    def draw(self, ax, c = 'k', lw = 1, alpha = 1):
        self.boundaries.draw(ax, c = c, lw = lw, alpha = alpha)

        if self.divided:
            self.nw.draw(ax, c = c, lw = lw, alpha = alpha)
            self.ne.draw(ax, c = c, lw = lw, alpha = alpha)
            self.se.draw(ax, c = c, lw = lw, alpha = alpha)
            self.sw.draw(ax, c = c, lw = lw, alpha = alpha)

    def SweepRegion(self):
        data_in_region = []

        for data in self.StoredData:
            data_in_region.append(data)

        if self.divided:
            data_in_region.extend(self.nw.SweepRegion())
            data_in_region.extend(self.ne.SweepRegion())
            data_in_region.extend(self.se.SweepRegion())
            data_in_region.extend(self.sw.SweepRegion())

        return data_in_region

    def CenterOfMass(self):

        TotalMass = 0
        XPonderate = 0
        YPonderate = 0        
        
        sample = self.SweepRegion()

        for data in sample:
            TotalMass += data.mass
            XPonderate += data.mass*data.x
            YPonderate += data.mass*data.y

        X_cm = XPonderate/TotalMass
        Y_cm = YPonderate/TotalMass

        return Point(X_cm, Y_cm), TotalMass

    def ParticleInteraction(self, particle, G=1, theta = 0.5):
        '''calculte all the interactions over the particle having on count the theta criterion, and returns acceleration components
        to later use it with leapfrog integration'''
        
        #initial acceleration
        ax = 0
        ay = 0

        for data in self.StoredData:
            if data.x == particle.x and data.y == particle.y:#particle does not interact with itself
                ax += 0
                ay += 0 
            
            else:
                dx = data.x - particle.x
                dy = data.y - particle.y
                aux_y = abs(dx)/dx
                aux_x = abs(dy)/dy
                ax += aux_x*G*data.mass/dx**2
                ay += aux_y*G*data.mass/dy**2

        if self.divided:
            CM, TotalMass = self.CenterOfMass()
            d = np.sqrt((CM.x-particle.x)**2+(CM.y-particle.y)**2)

            if particle.s/d < theta: #multipole acceptance criterion (MAC)
                dx = CM.x - particle.x
                dy = CM.y - particle.y
                aux_x = abs(dx)/dx
                aux_y = abs(dy)/dy
                ax += aux_x*G*TotalMass/dx**2
                ay += aux_y*G*TotalMass/dy**2

            else:
                if len(self.StoredData) > 0:
                    ax1, ay1 = self.nw.ParticleInteraction(particle)
                    ax += ax1
                    ay += ay1
                    ax2, ay2 = self.ne.ParticleInteraction(particle)
                    ax += ax2
                    ay += ay2
                    ax3, ay3 = self.se.ParticleInteraction(particle)
                    ax += ax3
                    ay += ay3
                    ax4, ay4 = self.sw.ParticleInteraction(particle)
                    ax += ax4
                    ay += ay4
                
                else:
                    ax += 0
                    qy+= 0

            return ax, ay

        # This below is a kind of brute force algorithm I wrote first, it could be addapted by replacing the sample parameter
        # and we could have a way to measure runtime, but I am not doing it yet

        # for data in sample:

        #     if data.x != particle.x and data.y != particle.y:#particle does not interact with itself
        #         dx = data.x - particle.x
        #         dy = data.y - particle.y
        #         aux_y = abs(dx)/dx
        #         aux_x = abs(dy)/dy
        #         a.x += aux_x*G*data.mass/dx**2
        #         a.y += aux_y*G*data.mass/dy**2

        #     else:
        #         a.x += 0
        #         a.y += 0