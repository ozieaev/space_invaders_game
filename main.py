# TODO: create class for screen to show stars
from turtle import Screen, Turtle
from game_config import *
from scoreboard import *
from rocket import *
import time

sky = Screen()
sky.tracer(0)
sky.setup(width=SKY_WIDTH, height=SKY_HEIGHT)
sky.title("SPACE INVADERS GAME")
sky.bgpic("night_sky.png")
sky.bgcolor("black")

myscore = Scoreboard(SKY_HEIGHT)
myship = Rocket()

alienarmada = Armada()

# TODO: setup screen controls
sky.listen()
sky.onkey(myship.move_left, "Left")
sky.onkey(myship.move_right, "Right")
# sky.update()

game_is_on = True
while game_is_on:
    myscore.update_score(myship.health, len(alienarmada.armada_array))

    if myship.can_fire:
        sky.onkey(myship.user_fire, "space")
        myscore.shots = myship.shots
    else:
        sky.onkey(myship.block_fire, "space")
        myscore.shots = "CHARGING"

    active_shots = len(myship.shots_array)
    if active_shots > SHOT_LIMIT - 1:
        myship.can_fire = False
    else:
        myship.can_fire = True

    if active_shots > 0:
        for shot in myship.shots_array:
            # print("call show_shot")
            shot.show_shot(shot)
            # TODO: put check_shot to validate if hit alien
            shot.check_shot(shot, alienarmada)
            if not shot.shot_active:
                myship.shots_array.remove(shot)

    if len(alienarmada.armada_array) > 0:
        alienarmada.move_armada()
        alienarmada.check_armada()
        alienarmada.armada_fire(myship)
        myscore.update_score(myship.health, len(alienarmada.armada_array))
        sky.update()
        print(alienarmada.armada_shots_array)
        for fire in alienarmada.armada_shots_array:
            fire.show_alien_shot(fire)
            # TODO: put check_alien_shot to validate if hit our ship
            hit = fire.check_alien_shot(fire, myship)
            if hit:
                myship.health -= 1
                if myship.health == 0:
                    myship.is_alive = False
                    myship.shape(EXPLOSION)
                    sky.update()
            print(f"fire: {fire.alien_shot_x} {fire.alien_shot_y} {fire.angle}")
            if not fire.shot_active:
                alienarmada.armada_shots_array.remove(fire)
    else:
        myscore.print_game_over("WIN !!!", "yellow")
        sky.update()
        print("Print GAME OVER, WIN!!!")
        game_is_on = False

    # myscore.update_score(myship.health, len(alienarmada.armada_array))

    if not myship.is_alive:
        myscore.update_score(myship.health, len(alienarmada.armada_array))
        myscore.print_game_over("LOST !!!", "red")
        sky.update()
        print("Print GAME OVER, LOST!!!")
        game_is_on = False

sky.exitonclick()
