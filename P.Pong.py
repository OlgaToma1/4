from tkinter import *

WIDTH = 1000
HEIGHT = 600

PAD_W = 10
PAD_H = 100

BALL_RADIUS = 40

root = Tk()
root.title ("Ping Pong")

c = Canvas(root, width=WIDTH, height=HEIGHT, background="#483D8B")
c.pack()

c.create_line(PAD_W, 0, PAD_W, HEIGHT, fill="white")
c.create_line(WIDTH - PAD_W, 0, WIDTH - PAD_W, HEIGHT, fill="white")
c.create_line(WIDTH / 2, 0, WIDTH / 2, HEIGHT, fill="white")

BALL = c.create_oval(WIDTH/2-BALL_RADIUS/2,
                    HEIGHT/2-BALL_RADIUS/2,
                    WIDTH/2+BALL_RADIUS/2,
                    HEIGHT/2+BALL_RADIUS/2, fill="#DEB887")

LEFT_PAD = c.create_line(PAD_W/2, 0, PAD_W/2, PAD_H, width=PAD_W, fill="#FFF8DC")
RIGHT_PAD = c.create_line(WIDTH-PAD_W/2, 0, WIDTH-PAD_W/2,
                          PAD_H, width=PAD_W, fill="#FFF8DC")

BALL_X_CHANGE = 20
BALL_Y_CHANGE = 0

def move_ball():
    c.move(BALL, BALL_X_CHANGE, BALL_Y_CHANGE)
def move_main():
    move_ball()
    root.after(30, main)

PAD_SPEED = 10
LEFT_PAD_SPEED = 0
RIGHT_PAD_SPEED = 0

def move_pads():
    PADS = {LEFT_PAD: LEFT_PAD_SPEED,
            RIGHT_PAD: RIGHT_PAD_SPEED}
    for pad in PADS:
       c.move(pad, 0, PADS[pad])
       if c.coords(pad)[1] < 0:
        c.move(pad, 0, -c.coords(pad)[1])
       elif c.coords(pad)[3] > HEIGHT:
        c.move(pad, 0, HEIGHT - c.coords(pad)[3])

def main():
    move_ball()
    move_pads()
    root.after(30, main)

c.focus_set()

def movement_handler(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym == "w":
        LEFT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "s":
        LEFT_PAD_SPEED = PAD_SPEED
    elif event.keysym == "o":
        RIGHT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "l":
        RIGHT_PAD_SPEED = PAD_SPEED


c.bind("<KeyPress>", movement_handler)

import random


BALL_SPEED_UP = 1.05
BALL_MAX_SPEED = 16
BALL_X_SPEED = 8
BALL_Y_SPEED = 8
right_line_distance = WIDTH - PAD_W


def bounce(action):
    global BALL_X_SPEED, BALL_Y_SPEED
    if action == "strike":
        BALL_Y_SPEED = random.randrange(-8, 8)
        if abs(BALL_X_SPEED) < BALL_MAX_SPEED:
            BALL_X_SPEED *= -BALL_SPEED_UP
        else:
            BALL_X_SPEED = -BALL_X_SPEED
    else:
        BALL_Y_SPEED = -BALL_Y_SPEED


def move_ball():
    ball_left, ball_top, ball_right, ball_bot = c.coords(BALL)
    ball_center = (ball_top + ball_bot) / 2

    if ball_right + BALL_X_SPEED < right_line_distance and \
            ball_left + BALL_X_SPEED > PAD_W:
        c.move(BALL, BALL_X_SPEED, BALL_Y_SPEED)
    elif ball_right == right_line_distance or ball_left == PAD_W:
        if ball_right > WIDTH / 2:
            if c.coords(RIGHT_PAD)[1] < ball_center < c.coords(RIGHT_PAD)[3]:
                bounce("strike")
            else:
                update_score("left")
                spawn_ball()
        else:
            if c.coords(LEFT_PAD)[1] < ball_center < c.coords(LEFT_PAD)[3]:
               bounce("strike")
            else:
                update_score("right")
                spawn_ball()
    else:
        if ball_right > WIDTH / 2:
            c.move(BALL, right_line_distance - ball_right, BALL_Y_SPEED)
        else:
            c.move(BALL, -ball_left + PAD_W, BALL_Y_SPEED)
    if ball_top + BALL_Y_SPEED < 0 or ball_bot + BALL_Y_SPEED > HEIGHT:
        bounce("ricochet")

PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0

p_1_text = c.create_text(WIDTH-WIDTH/6, PAD_H/4,
text=PLAYER_1_SCORE,
font="Arial 20",
fill="white")
p_2_text = c.create_text(WIDTH/6, PAD_H/4,
text=PLAYER_2_SCORE,
font="Arial 20",
fill="white")

INITIAL_SPEED = 20


def update_score(player):
    global PLAYER_1_SCORE, PLAYER_2_SCORE
    if player == "right":
        PLAYER_1_SCORE += 1
        c.itemconfig(p_1_text, text=PLAYER_1_SCORE)
    else:
        PLAYER_2_SCORE += 1
        c.itemconfig(p_2_text, text=PLAYER_2_SCORE)


def spawn_ball():
    global BALL_X_SPEED
    c.coords(BALL, WIDTH / 2 - BALL_RADIUS / 2,
             HEIGHT / 2 - BALL_RADIUS / 2,
             WIDTH / 2 + BALL_RADIUS / 2,
             HEIGHT / 2 + BALL_RADIUS / 2)
    BALL_X_SPEED = -(BALL_X_SPEED * -INITIAL_SPEED) / abs(BALL_X_SPEED)



main()

root.mainloop()
