def save_pygame_path(path):
    import pygame
    import os
    # from pygame.locals import *
    pygame.display.init()
    n = len(path)
    (W, H) = (200*n+50*(n-1), 100)
    surf = pygame.display.set_mode((W, H),32)

    surf = surf.convert_alpha()
    surf.fill((255,255,255,255))
    surf.fill((0,0,0,255), pygame.Rect((0,49),(200*n+50*(n-1),2)))

    for (i,v) in enumerate(path):
        filename = "l-%02d.png" % v
        img = pygame.image.load(os.path.join('imgs', filename))

        surf.blit(img, (200*i+50*(i),0))

    (_, letters) = path_value(path)

    pygame.font.init()
    f = pygame.font.get_default_font()
    font = pygame.font.Font(f, 20)

    for (i,v) in enumerate(letters):
        text = font.render(v, 1, (10, 10, 10))
        textrec = text.get_width()
        #textpos.centerx = surf.get_rect().centerx
        surf.blit(text, (200*(i+1)+50*i+(50-textrec)//2,25))

    str_file = ("from_%02d-to_%02d-long_%d-" % (path[0],path[-1],(len(path)-1))) + "-".join(["%02d" % i for i in path ])
    pygame.display.flip()
    pygame.image.save(surf, "paths/%s-.png" % (str_file,))
    pygame.quit()

def generate_plots():
    t = TowerOfLondon()
    t.show()

    for i in range(36):
        t.set_board_number(i)
        t.save_pygame_letters()
        t.save_pygame()