from turtle import Turtle, Screen
from game_config import *
import time
import random
import math


class Rocket(Turtle):
    def __init__(self):
        super().__init__()
        self.screen.register_shape(ROCKET_IMG)
        self.screen.register_shape(EXPLOSION)
        self.screen.getshapes()
        self.penup()
        self.shape(ROCKET_IMG)
        player_xpos = 0
        player_ypos = -1 * SKY_HEIGHT / 2 + 60
        self.goto(player_xpos, player_ypos)
        self.shots = 0
        self.shots_array = []
        self.can_fire = True
        self.health = LIFES
        self.is_alive = True

    def move_right(self):
        '''moves rocket left'''
        # print("User pressed right")
        if self.xcor() < int(SKY_WIDTH / 2 - (ROCKET_STEP * 2)):
            self.goto(self.xcor() + ROCKET_STEP, self.ycor())

    def move_left(self):
        '''moves rocket right '''
        # print("User pressed left")
        if self.xcor() > int(SKY_WIDTH / 2 * -1) + (ROCKET_STEP * 2):
            self.goto(self.xcor() - ROCKET_STEP, self.ycor())

    def user_fire(self):
        '''moves rocket right '''
        # print(f"User pressed space {self.xcor()} {self.ycor()} ")
        self.shots += 1
        self.shots_array.append(Plasma(self.xcor(), self.ycor()))

    def block_fire(self):
        self.goto(self.xcor(), self.ycor())

    def move_reset(self):
        ''' moves rocket to initial position '''
        player_ypos = 0 - int(SKY_WIDTH / 2) + 60
        self.goto(self.xcor(), player_ypos)


class Plasma(Turtle):
    def __init__(self, ship_x, ship_y):
        super().__init__()
        self.shape('square')
        self.shapesize(0.3)
        self.speed(0)
        self.color("orange")
        self.penup()
        self.left(90)
        self.shapesize(stretch_wid=0.1, stretch_len=2)
        self.plasma_x = ship_x
        self.plasma_y = ship_y + 60
        self.shot_active = True
        self.show_plasma(self.plasma_x, self.plasma_y)

    def show_shot(self, shot):
        """ Shows individual plasma shot. takes shot Plasma object """
        # print(f"shot move request for {shot} ")
        shot_y = shot.plasma_y + PLASMA_STEP
        # print(f"Plasma coordinates: {shot.plasma_x} {shot.plasma_y}")
        shot.goto(shot.plasma_x, shot_y)

        # TODO: Update object in array
        self.plasma_x = shot.plasma_x
        self.plasma_y = shot.plasma_y + PLASMA_STEP

        if shot_y >= SKY_HEIGHT / 2 - PLASMA_STEP:
            shot.hideturtle()
            shot.clear()
            shot.shot_active = False

    def show_plasma(self, plasma_x, plasma_y):
        self.goto(plasma_x, plasma_y)

    def check_shot(self, shot, armada):
        """ checks if any of the shots hit close to alien ship """
        for ship in armada.armada_array:
            if ship.distance(shot) < 20:
                print(f"hit ship {ship}. life left {ship.health}")
                ship.health -= 1
                if ship.health < 0:
                    ship.is_alive = False
                    ship.shape(ALIEN_EXPLOSION)
                    self.screen.update()
                if ship.health < 1 :
                    ship.shape(ALIEN_IMG_R)
                elif ship.health < int(ALIEN_MAX_HEALTH / 2):
                    ship.shape(ALIEN_IMG_B)
                # TODO: hide and set to remove plasma shot from array
                shot.hideturtle()
                shot.clear()
                shot.shot_active = False


class AlienShot(Turtle):
    """ individual alien shot class. takes coordinates of the alien ship and attack angle """
    def __init__(self, xpos, ypos, attack_angle):
        super().__init__()
        self.shape("circle")
        self.shapesize(.3)
        self.color("red")
        self.penup()
        self.right(attack_angle)
        self.shot_active = True
        self.alien_shot_x = xpos
        self.alien_shot_y = ypos - 10
        self.angle = attack_angle
        self.goto(xpos, ypos)

    def show_alien_shot(self, alien_shot):
        """ Shows individual alien shot """
        alien_shot.forward(ALIEN_FIRE_STEP)

        # TODO: Update object in array
        self.alien_shot_x = alien_shot.alien_shot_x
        self.alien_shot_y = alien_shot.alien_shot_y

        if self.alien_shot_y <= -1 * SKY_HEIGHT / 2:
            alien_shot.hideturtle()
            alien_shot.clear()
            alien_shot.shot_active = False

    def check_alien_shot(self, alien_shot, myship):
        """ takes alien_shot and myship objects, returns True if hit """
        if alien_shot.distance(myship) < 20:
            print("Hit our ship !!!")
            alien_shot.hideturtle()
            alien_shot.clear()
            alien_shot.shot_active = False
            return True
        else:
            return False


class AlienShip(Turtle):
    """ Alien Ship object """
    def __init__(self, xpos, ypos):
        super().__init__()
        self.screen.register_shape(ALIEN_IMG_G)
        self.screen.register_shape(ALIEN_IMG_B)
        self.screen.register_shape(ALIEN_IMG_R)
        self.screen.register_shape(ALIEN_EXPLOSION)
        self.screen.getshapes()
        self.penup()
        self.shape(ALIEN_IMG_G)
        self.goto(xpos, ypos)
        self.health = ALIEN_MAX_HEALTH
        self.can_fire = True
        self.is_alive = True


class Armada():
    """ Alien Ships Armada Class: controls all alien ships """
    def __init__(self):
        self.armada_array = []
        start_x = -1 * SKY_WIDTH / 2 + 60
        start_y = SKY_HEIGHT / 2 - 100
        for x in range(0, ALIENS_PER_LINE):
            for y in range(0, ALIENS_ROWS):
                alien_x = start_x + x * ALIEN_INTERVAL_X
                alien_y = start_y - y * ALIEN_INTERVAL_Y
                self.armada_array.append(AlienShip(alien_x, alien_y))
                print(f"adding alien at {alien_x} {alien_y}")
        self.armada_count = len(self.armada_array)
        self.armada_direction = 1  # left; -1 = right
        self.armada_adv_count = 0
        self.armada_down_step = 0
        self.armada_shots_array = []

    def move_armada(self):
        """ Move armada left, right and advance down """
        for alien in self.armada_array:
            alien.goto(alien.xcor() + self.armada_direction, alien.ycor() - self.armada_down_step)

        # TODO: change directions if reaching borders
        if self.armada_array[0].xcor() > 0 - SKY_WIDTH / 2 + int(ALIEN_INTERVAL_X * 1.5):
            self.armada_direction = -1
            # TODO: increment side move count and advance down
            self.armada_adv_count += 1
            # print(f"armada count is {self.armada_adv_count}")
        if self.armada_array[0].xcor() < 0 - SKY_WIDTH / 2 + int(ALIEN_INTERVAL_X * 0.5):
            self.armada_direction = 1

        if self.armada_adv_count >= ALIEN_ADVANCE_THRESHOLD:
            print(f"Moving armada down. count is {self.armada_adv_count}")
            # move one line closer
            self.armada_down_step = ALIEN_DOWN_STEP
            self.armada_adv_count = 0
        else:
            self.armada_down_step = 0

    def show_armada(self):
        print(self.armada_array)
        for alien_ship in self.armada_array:
            alien_ship.goto(alien_ship.xcor(), alien_ship.ycor())

    def check_armada(self):
        for alien in self.armada_array:
            if not alien.is_alive:
                alien.ht()
                self.armada_array.remove(alien)

    def armada_fire(self, myship):
        # TODO: get random ship from remaining ships at random time
        if len(self.armada_array) > 0:
            if random.randrange(0, len(self.armada_array) * ALIEN_RANDOMIZER + 10) == len(self.armada_array):
                ship_to_fire = random.choice(self.armada_array)
                print(f"Random ship selected to fire: {ship_to_fire}")
                distance_y = ship_to_fire.ycor() - myship.ycor()
                print(f"alien: {ship_to_fire.xcor()}, myship: {myship.xcor()}")

                if ship_to_fire.xcor() <= myship.xcor():
                    distance_x = myship.xcor() - ship_to_fire.xcor()
                else:
                    distance_x = ship_to_fire.xcor() - myship.xcor()

                # median = math.sqrt(distance_x ** 2 + distance_y ** 2)
                myradians = math.atan2(myship.ycor() - ship_to_fire.ycor(), myship.xcor() - ship_to_fire.xcor())
                mydegrees = int(abs(math.degrees(myradians)))
                print(f"vertical distance: {distance_y}, horizontal distance: {distance_x}, Right angle: {mydegrees}")

                self.armada_shots_array.append(AlienShot(ship_to_fire.xcor(), ship_to_fire.ycor(), mydegrees))





