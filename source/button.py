class Button():
    def __init__(self, pos, img_normal, img_hover):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.img_normal = img_normal
        self.img_hover = img_hover
        self.current_image = self.img_normal
        self.rect = self.current_image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        screen.blit(self.current_image, self.rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def hover(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.current_image = self.img_hover
        else:
            self.current_image = self.img_normal