from turtle import Turtle
from game_config import *


class Scoreboard(Turtle):
    def __init__(self, height):
        super().__init__()
        self.color(SCORE_COLOR)
        self.penup()
        self.ht()
        self.score_position_y = height / 2 - 50
        self.lifes = LIFES
        self.aliens = ALIENS_COUNT
        self.shots = 0
        self.update_score(self.lifes, self.aliens)

    def update_score(self, lifes, aliens_num):
        self.clear()
        self.goto(-1 * SKY_WIDTH / 2 + 50, self.score_position_y)
        self.write(f"LIFE: {lifes}", align="left", font=("Arial", 20, "bold"))
        self.goto(-1 * SKY_WIDTH / 2 + 150, self.score_position_y)
        if self.shots == "CHARGING":
            self.color('yellow')
        else:
            self.color(SCORE_COLOR)
        self.write(f"SHOTS: {self.shots}", align="left", font=("Arial", 20, "bold"))
        self.goto(100, self.score_position_y)
        self.write(f"ALIENS: {aliens_num}", align="left", font=("Arial", 20, "bold"))

    def print_game_over(self, message, color):
        self.goto(0, 0)
        self.color(color)
        self.write(f"GAME OVER\nYou {message}", align="center", font=("Courier", 50, "bold"))
