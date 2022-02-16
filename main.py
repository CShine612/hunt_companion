import gc
import math
from tkinter import *
import turtle

state = None
in_play = False
all_overlays = []
hunter_turtles = []
noise_turtles = []
darksight_turtles = []


# ToDo Implement the fading function on the noise turtles

# ---------------------------- Button Functions ------------------------------- #
# -------- Menu display function ---------- #

def menu_display():
    stop()
    root.geometry("1200x650")
    menu_background_label.place(x=0, y=0, relwidth=1, relheight=1)
    choose_text.grid(column=0, row=0, columnspan=3, sticky="EW")
    bayou_select.grid(column=0, row=1)
    lawson_select.grid(column=1, row=1)
    desalle_select.grid(column=2, row=1)


# -------- Map display function ---------- #

def map_display(game_map):
    start(3600, game_map)
    timer_label.grid(column=0, row=0, columnspan=2, sticky="W")
    dead_hunter_label.grid(column=2, row=0, columnspan=2, sticky="E")
    root.geometry("805x890")
    map_turtle.shape(game_map["spawns"])
    map_frame.grid(column=0, row=1, columnspan=4)
    canvas.pack()
    noise_button.grid(column=0, row=2, sticky="NSEW")
    noise_clear_button.grid(column=0, row=3, sticky="NSEW")
    dead_hunter_button.grid(column=1, row=2, sticky="NSEW")
    dead_hunter_clear_button.grid(column=1, row=3, sticky="NSEW")
    dark_sight_range_button.grid(column=2, row=2, sticky="NSEW")
    dark_sight_range_clear_button.grid(column=2, row=3, sticky="NSEW")
    undo_button.grid(column=3, row=2, sticky="NSEW")
    reset_button.grid(column=3, row=3, sticky="NSEW")
    screen.update()


def countdown(count, game_map):
    global in_play
    if not in_play:
        return
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    timer_label.config(text=f"Estimated time remaining: {count_min}:{count_sec}")
    root.after(1000, countdown, count - 1, game_map)
    if count_min == 49:
        map_turtle.shape(game_map["clear"])
        screen.update()


def start(count, game_map):
    global in_play
    in_play = True
    countdown(count, game_map)


def stop():
    global in_play
    in_play = False


# -------- Clear Screen ---------- #

def clear_menu_screen():
    for item in root.grid_slaves():
        item.grid_forget()


def clear_map_screen():
    clear_darksight()
    clear_hunter()
    clear_noise()
    for item in root.grid_slaves():
        item.grid_forget()

    noise_button.config(background="SystemButtonFace")
    dead_hunter_button.config(background="SystemButtonFace")
    dark_sight_range_button.config(background="SystemButtonFace")


# -------- Menu Buttons ---------- #

def bayou_display():
    clear_menu_screen()
    map_display(bayou)


def lawson_display():
    clear_menu_screen()
    map_display(lawson)


def desalle_display():
    clear_menu_screen()
    map_display(desalle)


# -------- Map Buttons ---------- #
# -------- Place Buttons ---------- #

def place_hunter():
    global state
    dark_sight_range_button.config(background="SystemButtonFace")
    noise_button.config(background="SystemButtonFace")
    dead_hunter_button.config(background="green")
    state = "hunter"


def place_darksight():
    global state
    dark_sight_range_button.config(background="green")
    noise_button.config(background="SystemButtonFace")
    dead_hunter_button.config(background="SystemButtonFace")
    state = "darksight"


def place_noise():
    global state
    dark_sight_range_button.config(background="SystemButtonFace")
    noise_button.config(background="green")
    dead_hunter_button.config(background="SystemButtonFace")
    state = "noise"


# -------- Clear Buttons ---------- #

def clear_hunter():
    while len(hunter_turtles) > 0:
        hunter_turtles[-1].hideturtle()
        hunter_turtles.pop()
    dead_hunter_label.config(text=f"Known Dead hunters: {len(hunter_turtles)}")
    screen.update()


def clear_darksight():
    for item in darksight_turtles:
        item.clear()
    screen.update()


def clear_noise():
    while len(noise_turtles) > 0:
        noise_turtles[-1].hideturtle()
        noise_turtles.pop()
    screen.update()


# -------- Undo/Reset Buttons ---------- #

def undo(*args):
    if len(all_overlays) > 0:
        all_overlays[-1].hideturtle()
        dead_turtle = all_overlays.pop()
        if dead_turtle in hunter_turtles:
            hunter_turtles.remove(dead_turtle)
        elif dead_turtle in darksight_turtles:
            dead_turtle.clear()
            darksight_turtles.remove(dead_turtle)
        if dead_turtle in noise_turtles:
            noise_turtles.remove(dead_turtle)
        screen.update()
    dead_hunter_label.config(text=f"Known Dead hunters: {len(hunter_turtles)}")


def reset():
    while len(all_overlays) > 0:
        del all_overlays[-1]
        gc.collect()
    clear_map_screen()
    menu_display()


# -------- Map on click functions ---------- #


def on_click(x, y):
    if state == "hunter":
        hunter_turtles.append(turtle.RawTurtle(screen))
        hunter_turtles[-1].penup()
        hunter_turtles[-1].shape(hunter_image)
        hunter_turtles[-1].setposition(x, y)
        all_overlays.append(hunter_turtles[-1])
        dead_hunter_label.config(text=f"Known Dead hunters: {len(hunter_turtles)}")
        screen.update()
    elif state == "darksight":
        darksight_turtles.append(turtle.RawTurtle(screen))
        darksight_turtles[-1].penup()
        darksight_turtles[-1].setposition(x, y - 120)
        darksight_turtles[-1].pendown()
        darksight_turtles[-1].pensize(2)
        darksight_turtles[-1].color("red")
        darksight_turtles[-1].circle(120)
        darksight_turtles[-1].hideturtle()
        all_overlays.append(darksight_turtles[-1])
        screen.update()
    elif state == "noise":
        noise_turtles.append(turtle.RawTurtle(screen))
        noise_turtles[-1].penup()
        noise_turtles[-1].shape(noise_image)
        noise_turtles[-1].setposition(x, y)
        all_overlays.append(noise_turtles[-1])
        screen.update()


# ---------------------------- UI SETUP ------------------------------- #

# Window

root = Tk()
root.title("Hunt Companion")
root.resizable(height=False, width=False)
root.iconbitmap("images/icon.ico")

# -------- Main Menu ---------- #

# Background

menu_background = PhotoImage(file="images/png/menu_background.png")
menu_background_label = Label(root, image=menu_background)

# Label

choose_text = Label(text="What map are you playing on?", font=("Arial", 15))

# Buttons

bayou_select = Button(text="Stillwater Bayou", command=bayou_display)
bayou_select.config(width=20, font=("Arial", 15))

lawson_select = Button(text="Lawson Delta", command=lawson_display)
lawson_select.config(width=20, font=("Arial", 15))

desalle_select = Button(text="Desalle", command=desalle_display)
desalle_select.config(width=20, font=("Arial", 15))

# -------- Map Page ---------- #

# Header

timer_label = Label(root, font=("Arial", 15))

dead_hunter_label = Label(root, text=f"Known Dead hunters: {len(hunter_turtles)}", font=("Arial", 15))

# Map

map_frame = Frame(root, height=800, width=800)
canvas = Canvas(map_frame, height=800, width=800)
screen = turtle.TurtleScreen(canvas)
map_turtle = turtle.RawTurtle(screen)

bayou = {"clear": "images/bayou.gif", "spawns": "images/bayou_spawns.gif"}
screen.addshape(bayou["clear"])
screen.addshape(bayou["spawns"])
lawson = {"clear": "images/lawson_delta.gif", "spawns": "images/lawson_delta_spawns.gif"}
screen.addshape(lawson["clear"])
screen.addshape(lawson["spawns"])
desalle = {"clear": "images/desalle.gif", "spawns": "images/desalle_spawns.gif"}
screen.addshape(desalle["clear"])
screen.addshape(desalle["spawns"])

hunter_image = "markers/dead.gif"
screen.addshape(hunter_image)

noise_image = "markers/ear.gif"
screen.addshape(noise_image)

# Buttons

noise_button = Button(text="Noise marker", command=place_noise)

noise_clear_button = Button(text="Clear Noise Markers", command=clear_noise)

dead_hunter_button = Button(text="Dead Hunter", command=place_hunter)

dead_hunter_clear_button = Button(text="Clear Hunters", command=clear_hunter)

dark_sight_range_button = Button(text="Dark Sight Range", command=place_darksight)

dark_sight_range_clear_button = Button(text="Clear DS Range", command=clear_darksight)

undo_button = Button(text="Undo", command=undo)

reset_button = Button(text="Reset", command=reset)

# ---------------------------- Main Loop ------------------------------- #
menu_display()
screen.tracer(0)

screen.listen()
screen.onscreenclick(on_click, 1)
screen.onscreenclick(undo, 3)

root.mainloop()
