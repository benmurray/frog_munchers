import pygame, sys


class Player(pygame.sprite.Sprite):
    FRAME_DELTA = 0.06

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprite_sheet = pygame.image.load('../assets/images/purple_ghost.png').convert()
        self.image = pygame.Surface((125, 125))
        self.image.blit(self.sprite_sheet, dest=(0, 0), area=(0, 0, 125, 125))

        self.idle, self.left, self.right, self.up, self.down = self.create_loops()
        self.current_sprite_loop = self.idle

        self.pos = (pos_x, pos_y)
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

        self.frame_num = 0

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
        self.frame_num += Player.FRAME_DELTA
        if self.frame_num >= len(self.current_sprite_loop):
            self.frame_num = 0

        self.image = pygame.transform.scale(self.current_sprite_loop[int(self.frame_num)], (125, 125))

    def stop_moving(self):
        self.current_sprite_loop = self.idle

    def move_up(self):
        self.current_sprite_loop = self.up
        self.pos = (self.pos[0], self.pos[1] - 2)
        self.rect.topleft = [self.pos[0], self.pos[1]]

    def move_down(self):
        self.current_sprite_loop = self.down
        self.pos = (self.pos[0], self.pos[1] + 2)
        self.rect.topleft = [self.pos[0], self.pos[1]]

    def move_left(self):
        self.current_sprite_loop = self.left
        self.pos = (self.pos[0] - 2, self.pos[1])
        self.rect.topleft = [self.pos[0], self.pos[1]]

    def move_right(self):
        self.current_sprite_loop = self.right
        self.pos = (self.pos[0] + 2, self.pos[1])
        self.rect.topleft = [self.pos[0], self.pos[1]]

pygame.init()
clock = pygame.time.Clock()

width = 1024
height = 768
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Animation")


moving_sprintes = pygame.sprite.Group()
player = Player(100, 100)
moving_sprintes.add(player)

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        player.move_down()
    elif keys[pygame.K_UP]:
        player.move_up()
    elif keys[pygame.K_LEFT]:
        player.move_left()
    elif keys[pygame.K_RIGHT]:
        player.move_right()
    else:
        player.stop_moving()

    # Drawing
    screen.fill((0, 0, 0))
    moving_sprintes.update()
    moving_sprintes.draw(screen)
    pygame.display.flip()
    clock.tick(60)