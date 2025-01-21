import pygame, sys


class Player(pygame.sprite.Sprite):
    FRAME_DELTA = 0.12

    def __init__(self, color='purple', pos_x=0, pos_y=0):
        super().__init__()
        self.sprite_sheet = pygame.image.load(f'../assets/images/{color}_ghost.png').convert()
        self.image = pygame.Surface((125, 125))
        self.image.blit(self.sprite_sheet, dest=(0, 0), area=(0, 0, 125, 125))

        self.idle, self.left, self.right, self.up, self.down = self.create_loops()
        self.current_sprite_loop = self.idle

        self.pos = (pos_x, pos_y)
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

        self.frame_num = 0
        self.frame_delta = Player.FRAME_DELTA

    def create_loops(self):
        front1 = pygame.Surface((125, 125))
        front1.blit(self.sprite_sheet, dest=(0, 0), area=(0, 0, 125, 125))
        front2 = pygame.Surface((125, 125))
        front2.blit(self.sprite_sheet, dest=(0, 0), area=(125, 0, 250, 125))
        front3 = pygame.Surface((125, 125))
        front3.blit(self.sprite_sheet, dest=(0, 0), area=(250, 0, 375, 375))
        front2.blit(self.sprite_sheet, dest=(0, 0), area=(125, 0, 250, 125))
        front_loop = [front1, front2, front3, front2]

        left1 = pygame.Surface((125, 125))
        left1.blit(self.sprite_sheet, dest=(0, 0), area=(0, 125, 125, 125))
        left2 = pygame.Surface((125, 125))
        left2.blit(self.sprite_sheet, dest=(0, 0), area=(125, 125, 250, 125))
        left3 = pygame.Surface((125, 125))
        left3.blit(self.sprite_sheet, dest=(0, 0), area=(250, 125, 375, 375))
        left2.blit(self.sprite_sheet, dest=(0, 0), area=(125, 125, 250, 125))
        left_loop = [left1, left2, left3, left2]

        right1 = pygame.Surface((125, 125))
        right1.blit(self.sprite_sheet, dest=(0, 0), area=(0, 250, 125, 125))
        right2 = pygame.Surface((125, 125))
        right2.blit(self.sprite_sheet, dest=(0, 0), area=(125, 250, 250, 125))
        right3 = pygame.Surface((125, 125))
        right3.blit(self.sprite_sheet, dest=(0, 0), area=(250, 250, 375, 375))
        right2.blit(self.sprite_sheet, dest=(0, 0), area=(125, 250, 250, 125))
        right_loop = [right1, right2, right3, right2]

        up1 = pygame.Surface((125, 125))
        up1.blit(self.sprite_sheet, dest=(0, 0), area=(0, 375, 125, 125))
        up2 = pygame.Surface((125, 125))
        up2.blit(self.sprite_sheet, dest=(0, 0), area=(125, 375, 250, 125))
        up3 = pygame.Surface((125, 125))
        up3.blit(self.sprite_sheet, dest=(0, 0), area=(250, 375, 375, 375))
        up2.blit(self.sprite_sheet, dest=(0, 0), area=(125, 375, 250, 125))
        up_loop = [up1, up2, up3, up2]

        return front_loop, left_loop, right_loop, up_loop, front_loop

    def update(self):
        """Increase frame_num by the delta and cast that to in(). Use result to pick the
        sprite in the *_loop"""
        self.frame_num += self.frame_delta
        if self.frame_num >= len(self.current_sprite_loop):
            self.frame_num = 0

        self.image = pygame.transform.scale(self.current_sprite_loop[int(self.frame_num)], (125, 125))

    def stop_moving(self):
        self.current_sprite_loop = self.idle
        self.frame_delta = 0.06

    def move_up(self):
        self.frame_delta = Player.FRAME_DELTA
        self.current_sprite_loop = self.up
        self.pos = (self.pos[0], self.pos[1] - 2)
        self.rect.topleft = [self.pos[0], self.pos[1]]

    def move_down(self):
        self.frame_delta = Player.FRAME_DELTA
        self.current_sprite_loop = self.down
        self.pos = (self.pos[0], self.pos[1] + 2)
        self.rect.topleft = [self.pos[0], self.pos[1]]

    def move_left(self):
        self.frame_delta = Player.FRAME_DELTA
        self.current_sprite_loop = self.left
        self.pos = (self.pos[0] - 2, self.pos[1])
        self.rect.topleft = [self.pos[0], self.pos[1]]

    def move_right(self):
        self.frame_delta = Player.FRAME_DELTA
        self.current_sprite_loop = self.right
        self.pos = (self.pos[0] + 2, self.pos[1])
        self.rect.topleft = [self.pos[0], self.pos[1]]

pygame.init()
clock = pygame.time.Clock()

width = 1024
height = 768
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Animation")


moving_sprites = pygame.sprite.Group()
player = Player('purple', 100, 100)
player2 = Player('red', 250, 100)
player3 = Player('blue', 400, 100)
player4 = Player('green', 550, 100)
player5 = Player('slime', 700, 100)
moving_sprites.add(player)
moving_sprites.add(player2)
moving_sprites.add(player3)
moving_sprites.add(player4)
moving_sprites.add(player5)

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        player.move_down()
        player2.move_down()
        player3.move_down()
        player4.move_down()
        player5.move_down()
    elif keys[pygame.K_UP]:
        player.move_up()
        player2.move_up()
        player3.move_up()
        player4.move_up()
        player5.move_up()
    elif keys[pygame.K_LEFT]:
        player.move_left()
        player2.move_left()
        player3.move_left()
        player4.move_left()
        player5.move_left()
    elif keys[pygame.K_RIGHT]:
        player.move_right()
        player2.move_right()
        player3.move_right()
        player4.move_right()
        player5.move_right()
    else:
        player.stop_moving()
        player2.stop_moving()
        player3.stop_moving()
        player4.stop_moving()
        player5.stop_moving()

    # Drawing
    screen.fill((0, 0, 0))
    moving_sprites.update()
    moving_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)
