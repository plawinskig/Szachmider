import math
import pygame

class Button():
    def __init__(self, pos, text: str, imgNormal, imgHover, r: int,
                 textHoverColor = pygame.Color("#ffffff"), textBasicColor =  pygame.Color("#ffffff"),
                 fontSize = 30, fontOffset=(1, -4), rightDetectionOffset=0):
        self.xPos = pos[0]
        self.yPos = pos[1]

        # Mainly for text fields, 
        # determines how much pixels from the right edge of the button the input detection should end
        self.rightDetectionOffset = rightDetectionOffset

        self.imgNormal = imgNormal
        self.imgHover = imgHover
        self.r = r  # Random number for floating animation

        self.text = text
        self.font = pygame.font.Font("assets/fonts/born2bsporty-fs.otf", size=fontSize)

        self.textBasicColor = textBasicColor
        self.textHoverColor = textHoverColor

        self.currentImage = self.imgNormal
        self.imgRect = self.currentImage.get_rect(center=(self.xPos, self.yPos))

        self.width = self.imgNormal.get_width()
        self.height = self.imgNormal.get_height()
        self.size = 1.0
        self.scale = 1.0

        self.fontXOffset = fontOffset[0]
        self.fontYOffset = fontOffset[1]
        self.fontText = self.font.render(text=self.text, antialias=False, color=self.textBasicColor)
        self.textRect = self.fontText.get_rect(center=(self.width / 2 + self.fontXOffset, self.height / 2 + self.fontYOffset))

        self.alpha = 255
        self.newAlpha = 255

        # Moving logic
        self.xDest = self.xPos
        self.yDest = self.yPos
        self.isMoving = False
        

    def update(self, screen, time, timeDelta):
        # Moving logic
        if self.isMoving:
            self.xPos = pygame.math.lerp(self.xPos, self.xDest, timeDelta * 6, True)
            self.yPos = pygame.math.lerp(self.yPos, self.yDest, timeDelta * 6, True)
        if (self.isMoving and int(self.xPos) in range(int(self.xDest) - 2, int(self.xDest) + 2)
                            and int(self.yPos) in range(int(self.yDest) - 2, int(self.yDest) + 2)):
            self.isMoving = False

        # Float animation
        angle = math.sin(time * 1.2 + self.r * 0.6)
        newYPos = self.yPos + math.sin(time * 1.5 + self.r * 0.8) * 3
        self.currentImage = pygame.transform.rotate(self.currentImage, angle)
        self.currentImage = pygame.transform.scale(self.currentImage,
                                                   (self.currentImage.get_width() * self.scale,
                                                    self.currentImage.get_height() * self.scale))
        self.imgRect = self.currentImage.get_rect(center=(self.xPos, newYPos))


        self.fontText = pygame.transform.rotate(self.fontText, angle)
        self.fontText = pygame.transform.scale(self.fontText,
                                               (self.fontText.get_width() * self.scale,
                                                self.fontText.get_height() * self.scale))
        self.textRect = self.fontText.get_rect(center=(self.width / 2 + self.fontXOffset,
                                                       self.height / 2 + self.fontYOffset))

        # Drawing to screen
        if self.text:
            self.currentImage.blit(self.fontText, self.textRect)
        
        self.alpha = pygame.math.lerp(self.alpha, self.newAlpha, timeDelta * 6, True)
        self.currentImage.set_alpha(self.alpha)

        screen.blit(self.currentImage, self.imgRect)

    def check_for_input(self, position):
        if (position[0] in range(self.imgRect.left, self.imgRect.right - self.rightDetectionOffset)
            and position[1] in range(self.imgRect.top, self.imgRect.bottom)
            and self.alpha > 0):
            return True
        return False

    def hover(self, position):
        if (position[0] in range(self.imgRect.left, self.imgRect.right - self.rightDetectionOffset)
            and position[1] in range(self.imgRect.top, self.imgRect.bottom)):
            self.currentImage = self.imgHover
            self.scale = self.size * 1.05
            self.fontText = self.font.render(text=self.text,
                                             antialias=False,
                                             color=self.textHoverColor)
        else:
            self.currentImage = self.imgNormal
            self.scale = self.size * 1.0
            self.fontText = self.font.render(text=self.text,
                                             antialias=False,
                                             color=self.textBasicColor)

    def move(self, position):
        self.xDest = position[0]
        self.yDest = position[1]
        self.isMoving = True