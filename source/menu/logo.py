from source.gui.button import Button
import pygame

class Logo():
    def __init__(self, pos):
        self.x_pos = pos[0]
        self.y_pos = pos[1]

        self.letter_bg_s = Button(pos=(self.x_pos - 217, self.y_pos), text="",
                                img_normal=pygame.image.load("assets/logo/LTR_bg_s.png").convert_alpha(),
                                img_hover=pygame.image.load("assets/logo/LTR_bg_s.png").convert_alpha(), r = 1)

        self.letter_bg_z = Button(pos=(self.x_pos - 172, self.y_pos + 12), text="",
                                img_normal=pygame.image.load("assets/logo/LTR_bg_z.png").convert_alpha(),
                                img_hover=pygame.image.load("assets/logo/LTR_bg_z.png").convert_alpha(), r = 2)

        self.letter_bg_a = Button(pos=(self.x_pos - 127, self.y_pos + 12), text="",
                                img_normal=pygame.image.load("assets/logo/LTR_bg_a.png").convert_alpha(),
                                img_hover=pygame.image.load("assets/logo/LTR_bg_a.png").convert_alpha(), r = 3)

        self.letter_bg_c = Button(pos=(self.x_pos - 83, self.y_pos + 12), text="",
                                img_normal=pygame.image.load("assets/logo/LTR_bg_c.png").convert_alpha(),
                                img_hover=pygame.image.load("assets/logo/LTR_bg_c.png").convert_alpha(), r = 4)

        self.letter_bg_h = Button(pos=(self.x_pos - 36, self.y_pos + 9), text="",
                                  img_normal=pygame.image.load("assets/logo/LTR_bg_h.png").convert_alpha(),
                                  img_hover=pygame.image.load("assets/logo/LTR_bg_h.png").convert_alpha(), r=5)

        self.letter_bg_m = Button(pos=(self.x_pos + 27, self.y_pos + 9), text="",
                                  img_normal=pygame.image.load("assets/logo/LTR_bg_m.png").convert_alpha(),
                                  img_hover=pygame.image.load("assets/logo/LTR_bg_m.png").convert_alpha(), r=6)

        self.letter_bg_i = Button(pos=(self.x_pos + 86, self.y_pos), text="",
                                  img_normal=pygame.image.load("assets/logo/LTR_bg_i.png").convert_alpha(),
                                  img_hover=pygame.image.load("assets/logo/LTR_bg_i.png").convert_alpha(), r=7)

        self.letter_bg_d = Button(pos=(self.x_pos + 136, self.y_pos), text="",
                                  img_normal=pygame.image.load("assets/logo/LTR_bg_d.png").convert_alpha(),
                                  img_hover=pygame.image.load("assets/logo/LTR_bg_d.png").convert_alpha(), r=8)

        self.letter_bg_e = Button(pos=(self.x_pos + 180, self.y_pos + 9), text="",
                                  img_normal=pygame.image.load("assets/logo/LTR_bg_e.png").convert_alpha(),
                                  img_hover=pygame.image.load("assets/logo/LTR_bg_e.png").convert_alpha(), r=9)

        self.letter_bg_r = Button(pos=(self.x_pos + 223, self.y_pos + 12), text="",
                                  img_normal=pygame.image.load("assets/logo/LTR_bg_r.png").convert_alpha(),
                                  img_hover=pygame.image.load("assets/logo/LTR_bg_r.png").convert_alpha(), r=10)

        self.letter_front_s = Button(pos=(self.x_pos - 217, self.y_pos), text="",
                                  img_normal=pygame.image.load("assets/logo/LTR_front_s.png").convert_alpha(),
                                  img_hover=pygame.image.load("assets/logo/LTR_front_s.png").convert_alpha(), r=1)

        self.letter_front_z = Button(pos=(self.x_pos - 172, self.y_pos + 12), text="",
                                  img_normal=pygame.image.load("assets/logo/LTR_front_z.png").convert_alpha(),
                                  img_hover=pygame.image.load("assets/logo/LTR_front_z.png").convert_alpha(), r=2)

        self.letter_front_a = Button(pos=(self.x_pos - 127, self.y_pos + 12), text="",
                                  img_normal=pygame.image.load("assets/logo/LTR_front_a.png").convert_alpha(),
                                  img_hover=pygame.image.load("assets/logo/LTR_front_a.png").convert_alpha(), r=3)

        self.letter_front_c = Button(pos=(self.x_pos - 83, self.y_pos + 12), text="",
                                  img_normal=pygame.image.load("assets/logo/LTR_front_c.png").convert_alpha(),
                                  img_hover=pygame.image.load("assets/logo/LTR_front_c.png").convert_alpha(), r=4)

        self.letter_front_h = Button(pos=(self.x_pos - 36, self.y_pos + 9), text="",
                                  img_normal=pygame.image.load("assets/logo/LTR_front_h.png").convert_alpha(),
                                  img_hover=pygame.image.load("assets/logo/LTR_front_h.png").convert_alpha(), r=5)

        self.letter_front_m = Button(pos=(self.x_pos + 27, self.y_pos + 9), text="",
                                  img_normal=pygame.image.load("assets/logo/LTR_front_m.png").convert_alpha(),
                                  img_hover=pygame.image.load("assets/logo/LTR_front_m.png").convert_alpha(), r=6)

        self.letter_front_i = Button(pos=(self.x_pos + 86, self.y_pos), text="",
                                  img_normal=pygame.image.load("assets/logo/LTR_front_i.png").convert_alpha(),
                                  img_hover=pygame.image.load("assets/logo/LTR_front_i.png").convert_alpha(), r=7)

        self.letter_front_d = Button(pos=(self.x_pos + 136, self.y_pos), text="",
                                  img_normal=pygame.image.load("assets/logo/LTR_front_d.png").convert_alpha(),
                                  img_hover=pygame.image.load("assets/logo/LTR_front_d.png").convert_alpha(), r=8)

        self.letter_front_e = Button(pos=(self.x_pos + 180, self.y_pos + 9), text="",
                                  img_normal=pygame.image.load("assets/logo/LTR_front_e.png").convert_alpha(),
                                  img_hover=pygame.image.load("assets/logo/LTR_front_e.png").convert_alpha(), r=9)

        self.letter_front_r = Button(pos=(self.x_pos + 223, self.y_pos + 12), text="",
                                  img_normal=pygame.image.load("assets/logo/LTR_front_r.png").convert_alpha(),
                                  img_hover=pygame.image.load("assets/logo/LTR_front_r.png").convert_alpha(), r=10)

    def update(self, screen, time, position):
        for bg in [self.letter_bg_s, self.letter_bg_z, self.letter_bg_a, self.letter_bg_c, self.letter_bg_h,
                    self.letter_bg_m, self.letter_bg_i, self.letter_bg_d, self.letter_bg_e, self.letter_bg_r]:
            bg.hover(position)
            bg.update(screen, time, 0)

        for front in [self.letter_front_s, self.letter_front_z, self.letter_front_a, self.letter_front_c, self.letter_front_h,
                    self.letter_front_m, self.letter_front_i, self.letter_front_d, self.letter_front_e, self.letter_front_r]:
            front.hover(position)
            front.update(screen, time, 0)
