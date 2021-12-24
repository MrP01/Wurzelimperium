import pygame,math
class Superclass(object):
    def __init__(self,pos,image,shapes=[]):
        self.x=pos[0]
        self.y=pos[1]
        self.rotation=0
        self.picture=image
        self.image=pygame.image.load(image)
        self.shapes={}
        for shape in shapes:
            self.shapes[shape]=pygame.image.load(shape)
    def __str__(self):
        return "(%s,%s)"%(self.x,self.y)
    def get_vec(self,pos):
        return pos[0]-self.x,pos[1]-self.y
    def change_shape(self,shape):
        self.image=self.shapes[shape]
        self.picture=shape
    def add_shape(self,shape):
        self.shapes[shape]=pygame.image.load(shape)
    def get_distance(self,pos):
        x=self.get_vec(pos)[0]*self.get_vec(pos)[0]
        y=self.get_vec(pos)[1]*self.get_vec(pos)[1]
        return math.sqrt(x+y)
    def in_range(self,pos,range):
        if self.get_distance(pos) <= range:
            return True
        else:
            return False
    def g2k(self,g):
        r=math.radians(g)
        x=math.sin(r)
        y=math.cos(r)
        return x,y
    def move_to(self,pos,time_passed,pixel=1,pps=100):
        unitx=self.get_vec(pos)[0]/self.get_distance(pos)
        unity=self.get_vec(pos)[1]/self.get_distance(pos)
        self.x=self.x+(unitx*pixel*(time_passed/1000.0)*pps)
        self.y=self.y+(unity*pixel*(time_passed/1000.0)*pps)
        return unitx,unity
    def set_pos(self,pos):
        self.x=pos[0]
        self.y=pos[1]
    def move_in_direction(self,degrees,pixel=10):
        self.x=self.x+self.g2k(degrees)[0]
        self.y=self.y+self.g2k(degrees)[1]
    def get_bounce(self,screensize):
        if self.y + self.image.get_size() >= screensize[1]:
            return True
        elif self.x <= 0 or self.y <= 0:
            return True
        elif self.x + self.image.get_size() >= screensize[0]:
            return True
    def rotate(self,rotation):
        self.rotation+=rotation
    def check_pressed(self):
        mp=pygame.mouse.get_pos()
        size=self.image.get_size()
        if self.x < mp[0] < self.x+size[0]:
            if self.y < mp[1] < self.y+size[1]:
                return True
    def blit(self,screen):
        im=pygame.transform.rotate(self.image,self.rotation)
        screen.blit(im,(self.x,self.y))
