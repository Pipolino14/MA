import math

#please dont break

class Animal:
    def __init__(self, max_vel, rotation_vel, id):
        self.img = self.IMG
        self.mask = self.MASK
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1
        self.id = id

    
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel
    
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()


    def move(self):
        #converting the current facing angle to RAD
        radians = math.radians(self.angle)
        #cos(RichtungsWinkel) * Hypothenuse{velocity vector} = Gegenkatethe --> Y movement
        vertical = math.cos(radians) * self.vel
        #sin(RichtungsWinkel) * Hypothenuse{velocity vector} = Ankatethe --> X movement
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal
    
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()


    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), (self.angle+90))

    def collision(self, mask, x=0, y=0):
        animal_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        touch = mask.overlap(animal_mask, offset)
        return touch
    
    def bounce(self):
        self.vel = -self.vel


class Environment:
    Hanimals = {}
    Panimals = {}

    def AddHunter(self):
        id = str(uuid.uuid4())
        print(id)
        hunterAnimal = HunterAnimal(4,4, id)
        hunterAnimal.x = random.randint(100, 1600)
        hunterAnimal.y = random.randint(100, 900)
        self.Hanimals.update({id:hunterAnimal})



class HunterAnimal(Animal):
    IMG = HUNTER_IMG
    MASK = HUNTER_MASK
    START_POS = (300, 300)

class PreyAnimal(Animal):
    IMG = PREY_IMG
    START_POS = (500, 500)


def check_border(self):
#Version on Check_border, where Sprites get teleported to other screen side
        HEI = (self.IMG.get_height()/2)
        WID = (self.IMGWID/2)
        if self.y > HEIGHT - HEI:
            self.y = 0 + HEI + 1
        if self.y < HEI:
            self.y = HEIGHT - HEI - 1
        if self.x > WIDTH - WID:
            self.x = 0 + WID + 1
        if self.x < WID:
            self.x = WIDTH - WID - 1

#-----------------------------
