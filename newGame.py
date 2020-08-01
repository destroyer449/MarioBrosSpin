# improved version of game.py
# 6/20/2019
#
# TODO:
#   images for classes
#   collisions
#
# written in python 3.7

from constants import *


class Player(pygame.sprite.Sprite):
    def __init__(self,
                 name,
                 width,
                 height,
                 image=None,
                 keys=None,
                 jump_height=2.55,
                 move_speed=1.5,
                 pos=(0, 0)):
        super().__init__()
        super().add(objects)
        if keys is None:
            keys = dict(left=pygame.K_a, right=pygame.K_d, up=pygame.K_w, down=pygame.K_s)
        self.name = name
        self.width = width
        self.height = height
        if image is None:
            self.rect = pygame.Rect(pos, (width, height))
        else:
            try:
                self.image, self.rect = load_image(image)
                self.image = pygame.transform.scale(self.image, (width, height))
            except pygame.error:
                self.rect = pygame.Rect(pos, (width, height))
                self.image = pygame.Surface((width, height))
                self.image.fill(image)
        self.keys = keys
        self.pos = list(pos)
        self.jump_height = jump_height
        self.move_speed = move_speed

        self.rect.topleft = pos
        self.start_pos = self.pos
        self.VX = 0
        self.VY = 0
        self.haveJumped = False
        self.wins = 0

    def reset(self):
        self.rect.topleft = self.start_pos
        self.VX = 0
        self.VY = 0
        self.jump_height = self.jump_height
        self.haveJumped = False

    def move(self):
        self.VX = 0.0
        pressed = pygame.key.get_pressed()
        if pressed[self.keys["left"]]:
            self.VX = -self.move_speed
            if self.rect.left > 0:
                self.pos[0] += self.VX

        if pressed[self.keys["right"]]:
            self.VX = self.move_speed
            if self.rect.right < windowWidth:
                self.pos[0] += self.VX

        self.gravity(pressed)

    def gravity(self, pressed):
        if pressed[self.keys["up"]]:
            if not self.haveJumped:
                self.haveJumped = True
                self.VY += self.jump_height

        self.pos[1] -= self.VY

        if self.pos[1] >= windowHeight - self.height:
            self.pos[1] = windowHeight - self.height
            self.VY = 0.0
            self.haveJumped = False
        elif pygame.sprite.spritecollide(self, platforms, False):
            platform = pygame.sprite.spritecollide(self, platforms, False)
            if self.rect.bottom-5 <= platform[0].rect.top:
                self.VY = 0.0
                self.haveJumped = False
        else:
            self.VY -= gravity

        self.rect.topleft = self.pos

    def win(self):
        self.wins += 1
        draw_text(window, "YOU WIN " + self.name, 85, windowWidth // 2, 300)
        draw_text(window, "Press Space To Play Again", 40, windowWidth // 2, 400)
        draw_text(window, str(self.wins) + "-" + str(rounds - self.wins), 40, windowWidth // 2, 450)
        pygame.display.flip()
        ready = False
        while not ready:
            for event in py_event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        ready = True
                    if event.key == pygame.K_ESCAPE:
                        quit_game()

                if event.type == pygame.QUIT:
                    quit_game()
            pygame.time.delay(1)
        self.reset()


class Platform(pygame.sprite.Sprite):
    def __init__(self, start, length, width):
        super().__init__()
        super().add(objects, platforms)
        self.start = start
        self.length = length
        self.width = width
        self.rect = pygame.Rect(self.start, (self.length, self.width))
        self.image = pygame.Surface((abs(self.length), self.width))
        self.image.fill(white, None, 0)


def main():
    global windowHeight, windowWidth
    fps = 180
    clock = pygame.time.Clock()
    pygame.init()

    player1 = Player("Red", 20, 20, (255, 0, 0),
                     jump_height=windowHeight/400+.8,  pos=(windowWidth // 4 - 10, windowHeight - 20))
    movement = dict(left=pygame.K_LEFT, right=pygame.K_RIGHT, up=pygame.K_UP, down=pygame.K_DOWN)
    player2 = Player("Green", 20, 20, (0, 255, 0), movement,
                     jump_height=windowHeight/400+.8, pos=(windowWidth // 4 * 3 - 10, windowHeight - 20))

    length = windowWidth/3.5
    Platform((0, windowHeight/3.5), length, 5)
    Platform((windowWidth-windowWidth/3.5, windowHeight/3.5), length, 5)
    Platform((0, windowHeight/1.4), length, 5)
    Platform((windowWidth/4, windowHeight/2), windowWidth/4*3-windowWidth/4, 5)
    Platform((windowWidth-windowWidth/3.5, windowHeight/1.4), length, 5)
    Platform((0, windowHeight-1), windowWidth, 5)

    while True:
        window.fill((0, 0, 0))
        pygame.draw.line(window, white, (0, 100), (350, 100), 5)
        for event in py_event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause()
                elif event.key == pygame.K_ESCAPE:
                    quit_game()
            if event.type == pygame.VIDEORESIZE:
                # window.fill((0, 0, 0))
                windowWidth, windowHeight = event.size
                length = windowWidth/3.5
                for platform in platforms:
                    platform.kill()
                Platform((0, windowHeight / 3.5), length, 5)
                Platform((windowWidth-length, windowHeight / 3.5), length, 5)
                Platform((windowWidth / 4, windowHeight / 2), windowWidth / 4 * 3 - windowWidth / 4, 5)
                Platform((0, windowHeight / 1.4), length, 5)
                Platform((windowWidth - windowWidth / 3.5, windowHeight / 1.4), length, 5)
                Platform((0, windowHeight - 1), windowWidth, 15)
                player1.jump_height = windowHeight / 400 + .8
                player2.jump_height = windowHeight / 400 + .8

        player1.move()
        player2.move()
        pygame.display.update(objects.draw(window))
        clock.tick(fps)


if __name__ == "__main__":
    main()
