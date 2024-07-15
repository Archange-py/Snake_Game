from ion import keydown,KEY_UP,KEY_DOWN,KEY_LEFT,KEY_RIGHT,KEY_BACKSPACE,KEY_OK
from kandinsky import get_pixel,draw_string,fill_rect,color
from time import sleep, monotonic
from random import randint

class Screen: palette = {"Background":(255,255,255),"PrimaryColor":(0,0,0),"PrimaryText":(0,200,200),"SecondaryText":(255,255,255),"SnakeColor":(0,255,0),"FoodColor":(255,0,0)}

class Curseur:
    def __init__(self, *args, default=""): self.args, self.sens, self.default = args, "R", default
    def __next__(self): self.N += 1 if self.sens == "R" else -1 ; self.check() ; self.curs = self.args[self.N] ; return self.curs
    def __iter__(self): self.curs, self.N = self.default if self.default != ""  else self.args[-1], self.args.index(self.default) if self.default != ""  else -1 ; return self
    def check(self):
        if self.N > len(self.args)-1: self.N = 0
        elif self.N < 0: self.N = len(self.args)-1

class GUI:
    speed,bot,color_mode = 0.1,False,"light"
    @staticmethod
    def clean(): fill_rect(0,0,320,222,Screen.palette["Background"])
    @staticmethod
    def main(): GUI.Menu.draw()
    class Menu:
        @staticmethod
        def draw():
            def draw_curseur(curseur):
                if curseur == "play":
                    draw_string(" >  play  <",110,100,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
                    draw_string("  graph        ",120,130,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
                    draw_string("  settings        ",105,160,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
                elif curseur == "graph":
                    draw_string("  play        ",120,100,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
                    draw_string(" >  graph  <",110,130,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
                    draw_string("  settings        ",105,160,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
                elif curseur == "settings":
                    draw_string("  play        ",120,100,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
                    draw_string("  graph        ",120,130,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
                    draw_string(" >  settings  <",95,160,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
            GUI.clean() ; I = iter(Curseur("play","graph","settings",default="play"))
            draw_string("Snake",138,50,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
            draw_string("  play  ",120,100,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
            draw_string("  graph  ",120,130,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
            draw_string("  settings  ",105,160,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
            while True:
                if keydown(KEY_UP): I.sens = "L" ; next(I) ; draw_curseur(I.curs) ; sleep(0.15)
                if keydown(KEY_DOWN): I.sens = "R" ; next(I) ; draw_curseur(I.curs) ; sleep(0.15)
                if keydown(KEY_OK) and I.curs == "play": GUI.Play.draw() ; break
                if keydown(KEY_OK) and I.curs == "graph": GUI.Graph.draw() ; break
                if keydown(KEY_OK) and I.curs == "settings": GUI.Settings.draw() ; break
    class Play:
        @staticmethod
        def draw():
            GUI.clean()
            draw_string("Score:0",125,10,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
            dx,dy,s,q,food,v,pt,GUI.Play.score = 0,1,[[160,110]],[160,110],True,GUI.speed,monotonic(),0 ; sleep(0.15)
            def find_pos(fx,fy,x,y):
                if fy < y: return 0,-1
                if fy > y: return 0,1
                if fx < x: return -1,0
                if fx > x: return 1,0
            while True:
                ct = monotonic() ; dt = ct-pt
                if food: fx,fy = 10 * randint(0,31),10 * randint(3,21) ; food = False
                fill_rect(fx,fy,10,10,Screen.palette["FoodColor"])
                if keydown(KEY_UP) and not GUI.bot: dx,dy = 0,-1
                if keydown(KEY_DOWN) and not GUI.bot: dx,dy = 0,1
                if keydown(KEY_LEFT) and not GUI.bot: dx,dy = -1,0
                if keydown(KEY_RIGHT) and not GUI.bot: dx,dy = 1,0
                if GUI.bot: dx,dy = find_pos(fx,fy,*s[0])
                if keydown(KEY_BACKSPACE): break ; sleep(0.15)
                if keydown(KEY_OK):
                    draw_string("Pause",130,100,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"]) ; sleep(0.15)
                    while True:
                        if keydown(KEY_OK):
                            fill_rect(0,0,320,222,Screen.palette["Background"])
                            draw_string("Score:",125,10,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
                            draw_string(str(GUI.Play.score),185,10,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
                            fill_rect(q[0],q[1],10,10,Screen.palette["Background"])
                            fill_rect(s[0][0],s[0][1],10,10,Screen.palette["SnakeColor"])
                            fill_rect(fx,fy,10,10,Screen.palette["FoodColor"])
                            sleep(0.15) ; break
                        if keydown(KEY_BACKSPACE): GUI.Menu.draw() ; break
                if dt > v:
                    pt,x,y = monotonic(),s[0][0] + 10*dx,s[0][1] + 10*dy ; s.insert(0,[x,y])
                    if x < 0 or x > 310 or y < 0 or y > 210 or color(get_pixel(x,y)) == Screen.palette["SnakeColor"]: draw_string("Game Over",120,100,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"]) ; break
                    if color(get_pixel(x,y)) != Screen.palette["FoodColor"]: q = s.pop() ; fill_rect(q[0],q[1],10,10,Screen.palette["Background"])
                    else: GUI.Play.score += 1 ; draw_string(str(GUI.Play.score),185,10,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"]) ; food = True
                    fill_rect(s[0][0],s[0][1],10,10,Screen.palette["SnakeColor"])
            while True:
                if keydown(KEY_BACKSPACE): GUI.Graph.list_score.append(GUI.Play.score) ; GUI.clean() ; GUI.Menu.draw() ; break
    class Graph:
        list_score = [0]
        @staticmethod
        def draw():
            GUI.clean()
            draw_string("Graphics",120,20,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
            draw_string("Maximum Score : "+str(max(GUI.Graph.list_score)),15,200,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
            fill_rect(10,0,1,222,Screen.palette["PrimaryColor"]);fill_rect(0,196,320,1,Screen.palette["PrimaryColor"])
            for n,bar in enumerate(GUI.Graph.list_score): fill_rect(10+n*(3+2),195,3,-bar,Screen.palette["PrimaryColor"])
            while True:
                if keydown(KEY_BACKSPACE): GUI.clean() ; GUI.Menu.draw() ; break
    class Settings:
        @staticmethod
        def draw():
            def draw_curseur(curseur):
                if curseur == "speed":
                    draw_string(">   "+str(GUI.speed)+"   <    ",165,80,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
                    draw_string("    "+str(GUI.bot)+"        ",165,110,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
                    draw_string("    "+GUI.color_mode+"        ",165,140,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
                elif curseur == "bot":
                    draw_string("    "+str(GUI.speed)+"       ",165,80,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
                    draw_string(">   "+str(GUI.bot)+"   <    ",165,110,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
                    draw_string("    "+str(GUI.color_mode)+"        ",165,140,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
                elif curseur == "color mode":
                    draw_string("    "+str(GUI.speed)+"       ",165,80,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
                    draw_string("    "+str(GUI.bot)+"        ",165,110,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
                    draw_string(">   "+GUI.color_mode+"   <    ",165,140,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
            def change_color(mode):
                if mode == "light": Screen.palette["Background"] = (255,255,255) ; Screen.palette["PrimaryText"] = (0,200,200) ;Screen.palette["SecondaryText"] = (255,255,255) ; Screen.palette["PrimaryColor"] = (0,0,0)
                elif mode == "dark": Screen.palette["Background"] = (80,80,100) ; Screen.palette["PrimaryText"] = (255,255,255) ; Screen.palette["SecondaryText"] = (80,80,100) ; Screen.palette["PrimaryColor"] = (255,255,255)
            GUI.clean() ; I = iter(Curseur("speed","bot","color mode")) ; I_speed = iter(Curseur(0,0.05,0.1,0.15,0.2,0.25,0.3,default=GUI.speed)) ; I_bot = iter(Curseur(False,True,default=GUI.bot)) ; I_color_mode = iter(Curseur("light","dark",default=GUI.color_mode))
            draw_string("Settings",110,30,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
            draw_string("speed",25,80,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
            draw_string("simple bot",25,110,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
            draw_string("color mode",25,140,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
            draw_string("    "+str(GUI.speed)+"       ",165,80,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
            draw_string("    "+str(GUI.bot)+"       ",165,110,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
            draw_string("    "+GUI.color_mode+"        ",165,140,Screen.palette["PrimaryText"],Screen.palette["SecondaryText"])
            while True:
                if I.curs == "speed" and keydown(KEY_RIGHT): I_speed.sens = "R" ; next(I_speed) ; GUI.speed = I_speed.curs ; draw_curseur(I.curs) ; sleep(0.15)
                if I.curs == "speed" and keydown(KEY_LEFT): I_speed.sens = "L" ; next(I_speed) ; GUI.speed = I_speed.curs ; draw_curseur(I.curs) ; sleep(0.15)
                if I.curs == "bot" and keydown(KEY_RIGHT): I_bot.sens = "R" ; next(I_bot) ; GUI.bot = I_bot.curs ; draw_curseur(I.curs) ; sleep(0.15)
                if I.curs == "bot" and keydown(KEY_LEFT): I_bot.sens = "L" ; next(I_bot) ; GUI.bot = I_bot.curs ; draw_curseur(I.curs) ; sleep(0.15)
                if I.curs == "color mode" and keydown(KEY_RIGHT): I_color_mode.sens = "R" ; next(I_color_mode) ; GUI.color_mode = I_color_mode.curs ; draw_curseur(I.curs) ; sleep(0.15)
                if I.curs == "color mode" and keydown(KEY_LEFT): I_color_mode.sens = "L" ; next(I_color_mode) ; GUI.color_mode = I_color_mode.curs ; draw_curseur(I.curs) ; sleep(0.15)
                if keydown(KEY_UP): I.sens = "L" ; next(I) ; draw_curseur(I.curs) ; sleep(0.15)
                if keydown(KEY_DOWN): I.sens = "R" ; next(I) ; draw_curseur(I.curs) ; sleep(0.15)
                if keydown(KEY_BACKSPACE): change_color(GUI.color_mode) ; GUI.clean() ; GUI.Menu.draw() ; break

GUI.main()