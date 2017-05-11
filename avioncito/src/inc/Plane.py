# -*- coding: utf-8 -*-
#!/usr/bin/python

import pygame

class Plane(pygame.sprite.DirtySprite):    
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.rect = self.image.get_rect()
        
    def plane_left(self):
        pass

    def plane_right(self):
        pass

class ForwardPlaneLeft(Plane):
    def __init__(self):
        self.image = pygame.image.load("./images/forward_left.png").convert_alpha()
        Plane.__init__(self)
        self.kind = "ForwardPlaneLeft"

    def plane_left(self):
        super(ForwardPlaneLeft, self).plane_left()
        return True

    def plane_right(self):
        super(ForwardPlaneLeft, self).plane_right()
        return False

class ForwardPlaneRight(Plane):
    def __init__(self):
        self.image = pygame.image.load("./images/forward_right.png").convert_alpha()
        Plane.__init__(self)
        self.kind = "ForwardPlaneRight"

    def plane_left(self):
        super(ForwardPlaneRight, self).plane_left()
        return False

    def plane_right(self):
        super(ForwardPlaneRight, self).plane_right()
        return True

class InversePlaneLeft(Plane):
    def __init__(self):
        self.image = pygame.image.load("./images/inverse_left.png").convert_alpha()
        Plane.__init__(self)
        self.kind = "InversePlaneLeft"

    def plane_left(self):
        super(InversePlaneLeft, self).plane_left()
        return False

    def plane_right(self):
        super(InversePlaneLeft, self).plane_right()
        return True

class InversePlaneRight(Plane):
    def __init__(self):
        self.image = pygame.image.load("./images/inverse_right.png").convert_alpha()
        Plane.__init__(self)
        self.kind = "InversePlaneRight"

    def plane_left(self):
        super(InversePlaneRight, self).plane_left()
        return True

    def plane_right(self):
        super(InversePlaneRight, self).plane_right()
        return False

class ReverseForwardPlaneLeft(Plane):
    def __init__(self):
        self.image = pygame.image.load("./images/reverse_forward_left.png").convert_alpha()
        Plane.__init__(self)
        self.kind = "ReverseForwardPlaneLeft"

    def plane_left(self):
        super(ReverseForwardPlaneLeft, self).plane_left()
        return True

    def plane_right(self):
        super(ReverseForwardPlaneLeft, self).plane_right()
        return False

class ReverseForwardPlaneRight(Plane):
    def __init__(self):
        self.image = pygame.image.load("./images/reverse_forward_right.png").convert_alpha()
        Plane.__init__(self)
        self.kind = "ReverseForwardPlaneRight"

    def plane_left(self):
        super(ReverseForwardPlaneRight, self).plane_left()
        return False

    def plane_right(self):
        super(ReverseForwardPlaneRight, self).plane_right()
        return True

class ReverseInversePlaneLeft(Plane):
    def __init__(self):
        self.image = pygame.image.load("./images/reverse_inverse_left.png").convert_alpha()
        Plane.__init__(self)
        self.kind = "ReverseInversePlaneLeft"

    def plane_left(self):
        super(ReverseInversePlaneLeft, self).plane_left()
        return False

    def plane_right(self):
        super(ReverseInversePlaneLeft, self).plane_right()
        return True

class ReverseInversePlaneRight(Plane):
    def __init__(self):
        self.image = pygame.image.load("./images/reverse_inverse_right.png").convert_alpha()
        Plane.__init__(self)
        self.kind = "ReverseInversePlaneRight"

    def plane_left(self):
        super(ReverseInversePlaneRight, self).plane_left()
        return True

    def plane_right(self):
        super(ReverseInversePlaneRight, self).plane_right()
        return False
