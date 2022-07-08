import pyxel
import random
"""
Nom du Jeu = Between Worlds
Team = AMA LucLaCourbe Students
Description du jeu :
Between Worlds est un jeu de plateforme en 2D qui se joue sur deux mondes différents à la fois. Lors de votre aventure dans notre 1er niveau, vous tomberez sur de multiples obstacles à franchir et ennemis à battre. Toutefois, vous devrez vous munir de votre mystérieux pouvoir afin de franchir certains d'entre eux... Voyagez à travers les mondes afin d'arriver à la sortie de nos parcours ! La AMA vous souhaite une excellente et agréable expérience de jeu.
Se déplacer à droite : Flèche de droite
Se déplacer à gauche : Flèche de gauche 
Sauter : Touche Espace
Changer de dimension : Touche A


 """

scroll_bord_x = 80
tile_sol = [(4, 5), (4, 8), (2, 12), (2, 13), (2, 14),(0, 1), (0, 2), (0, 3), (2, 4), (2, 5), (2, 6), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (1, 3), (3, 1), (4, 1), (5, 1), (6, 1), (0, 9), (1, 9), (2, 9), (0, 10), (1, 10), (2, 10), (0, 11), (1, 11), (2, 11), (3, 9), (3, 10), (4, 9), (5,9), (6, 9),(0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3), (4, 1), (5, 1), (6, 1), (0, 9), (1, 9), (2, 9), (0, 10), (1, 10), (2, 10), (0, 11), (1, 11), (2, 11), (3, 9), (4, 9), (5,9), (6, 9), (1, 4), (1, 5), (1, 6), (1,12), (1, 13), (1, 14), (0, 30), (1, 30), (2, 30), (0, 31), (0, 32), (1, 31), (1, 32), (2, 31), (2, 32)]
niveau_1 = (0, 0)
monstre = [(4, 5)]
niveau = 1

scroll_x = 0
player = None
chrono = 0

nb_map = 0
dimtp = False
mouv = 0
liste_text = []
collision = ""

changelevel = 0

def get_tile(tile_x, tile_y): # PERMET DE RETURN LA TILE
    global collision
    if (pyxel.tilemap(nb_map).pget(tile_x, tile_y)) == (3,28) or (pyxel.tilemap(nb_map).pget(tile_x, tile_y)) == (4, 28):
        collision = "sorcier"
    elif (pyxel.tilemap(nb_map).pget(tile_x, tile_y)) == (4, 8):
        collision = "abeille"
    elif (pyxel.tilemap(nb_map).pget(tile_x, tile_y)) == (4, 5):
        collision = "monstre"
    elif (pyxel.tilemap(nb_map).pget(tile_x, tile_y)) == (4, 5):
        collision = "monstre"
    elif (pyxel.tilemap(nb_map).pget(tile_x, tile_y)) == (0, 14):
        collision = "echelle"
    elif (pyxel.tilemap(nb_map).pget(tile_x, tile_y)) == (0, 5):
        collision = "echelle"
    elif (pyxel.tilemap(nb_map).pget(tile_x, tile_y)) == (0, 6):
        collision = "echelle"
    elif (pyxel.tilemap(nb_map).pget(tile_x, tile_y)) == (3, 4):
        collision = "eau"
    elif (pyxel.tilemap(nb_map).pget(tile_x, tile_y)) == (3, 5):
        collision = "eau"
    return pyxel.tilemap(nb_map).pget(tile_x, tile_y)


def detect_collision(x, y, dy):
    x1 = x // 8
    y1 = y // 31
    x2 = (x + 8 - 1) // 8
    y2 = (y + 31 - 1) // 8
    for yi in range(y1, y2 + 1):
        for xi in range(x1, x2 + 1):
            if get_tile(xi, yi) in tile_sol: # RECUL DU PERSONNAGE SI COLLISION
                return True
                print(get_tile(xi, yi))
    if dy > 0 and y % 8 == 1:
        for xi in range(x1, x2 + 1):
            if get_tile(xi, y1 + 1) in tile_sol: # SI LE BLOCK EN DESSOUS Y+1 
                return True

    return False


def anti_colli(x, y, dx, dy):
    abs_dx = abs(dx)
    abs_dy = abs(dy)
    if abs_dx > abs_dy:
        sign = 1 if dx > 0 else -1
        for _ in range(abs_dx):
            if detect_collision(x + sign, y, dy):
                break
            x += sign
        sign = 1 if dy > 0 else -1
        for _ in range(abs_dy):
            if detect_collision(x, y + sign, dy):
                break
            y += sign
    else:
        sign = 1 if dy > 0 else -1
        for _ in range(abs_dy):
            if detect_collision(x, y + sign, dy):
                break
            y += sign
        sign = 1 if dx > 0 else -1
        for _ in range(abs_dx):
            if detect_collision(x + sign, y, dy):
                break
            x += sign
    return x, y, dx, dy


def detect_mur(x, y):
    tile = get_tile(x // 8, y // 8)
    return tile == tile_sol or tile[0] >= mur_tile_x






class Player:
    global dimtp, nb_map, mouv
    def __init__(self, x, y):
        self.x = 3
        self.y = 50
        self.dx = 0
        self.dy = 0
        self.direction = 1
        self.is_falling = False
        self.jump = False
        self.life = 3

    def update(self):
        global mouv, scroll_x
        global scroll_x, dimtp, nb_map, collision, changelevel
        if collision == "eau":
            collision = ""
            self.y = 150
        if self.y > 130:
            self.x = 3
            dx = 0
            scroll_x = 0
            self.y = 50
        last_y = self.y

        if self.life <= 3:
            pyxel.text(28, 32, "Vous êtes mort!", 8)
        if changelevel == 0:
            if pyxel.btn(pyxel.KEY_LEFT):
                self.dx = -2
                self.direction = -1
                mouv = 1
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.dx = 2
                self.direction = 1
                mouv = 1
            if pyxel.btnr(pyxel.KEY_RIGHT) or pyxel.btnr(pyxel.KEY_LEFT):
                mouv = 0
            if pyxel.btnr(pyxel.KEY_A):
                dimtp = True
                if nb_map <= 6:
                    nb_map += 1
                elif nb_map == 7:
                    nb_map = 6
                self.y-=3
            if pyxel.btnr(pyxel.KEY_S):
                changelevel = 1
                chrono = 0
                self.x = 3
                self.y = 50
        self.dy = min(self.dy + 1, 3)
        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.jump == False:
                self.dy = -6
            self.jump = True
        if pyxel.frame_count % 22 == 0:
            self.jump = False


        self.x, self.y, self.dx, self.dy = anti_colli(self.x, self.y, self.dx, self.dy)
        if self.x < scroll_x:
            self.x = scroll_x
        if self.y < 0:
            self.y = 0
        self.dx = int(self.dx * 0.8)
        self.is_falling = self.y > last_y

        if self.x > scroll_x + scroll_bord_x:
            last_scroll_x = scroll_x
            scroll_x = min(self.x - scroll_bord_x, 240 * 8)
        if self.x < scroll_x + scroll_bord_x:
            last_scroll_x = scroll_x
            scroll_x = min(self.x - scroll_bord_x, 240 * 8)

        # COLLISIONS

        if collision == "abeille":
            self.y -= 35
            collision = ""
    def draw(self):
        global nb_map, dimtp, mouv, collision, chrono, changelevel
        u = 71
        if mouv == 1:
            if pyxel.frame_count % 6 == 0:
                posone = 193
                u = 71
            else:
                posone = 193
                u = 88
        if self.direction > 0:
            w = -14
        else:
            w = 14
        if dimtp == True:
            if pyxel.frame_count % 2 == 0:
                dimtp = False
                if nb_map == 1:
                    dimtp = False
                    self.y-=2
                elif nb_map == 0:
                    dimtp = False
                    self.y-=2
                elif nb_map == 2:
                    dimtp = False
                    self.y-=3
                    nb_map = 0

                if nb_map == 4:
                    dimtp = False
                    self.y-=2
                elif nb_map == 3:
                    dimtp = False
                    self.y-=2
                elif nb_map == 5:
                    dimtp = False
                    self.y-=3
                    nb_map = 3

                if nb_map == 7:
                    dimtp = False
                    self.y-=2
                elif nb_map == 6:
                    dimtp = False
                    self.y-=2
                elif nb_map > 7:
                    dimtp = False
                    self.y-=3
                    nb_map = 6

        if collision == "sorcier":
            if nb_map == 0:
                pyxel.text(self.x-68,0, "Bienvenue à LLC Courbe!\nAppuye sur A pour changer de \ndimension!\nFinis le monde de tutoriel \nafin d'acceder au niveaux \naléatoires!\nOu appuye sur la touche S!", 3)
            else:
                pyxel.text(self.x-68,0, "Arrive jusqu'a l'echelle\npour passer au prochain\nniveau aleatoire\nConseil: Utilisez le\nDouble Jump", 3)
            collision = ""
        elif collision == "echelle":
            changelevel = 1
            chrono = 0
            self.x = 3
            self.y = 50
            collision = ""
        # MONSTRES 
        if pyxel.frame_count % 30 == 0:
            if nb_map == 0 or nb_map == 1:
                pyxel.tilemap(nb_map).pset(37, 7, (4, 5))
                pyxel.tilemap(nb_map).pset(38, 7, (0, 0))

                pyxel.tilemap(nb_map).pset(45, 11, (4, 5))
                pyxel.tilemap(nb_map).pset(46, 11, (0, 0))
            if nb_map == 0:
                pyxel.tilemap(nb_map).pset(49, 10, (0, 0))
                pyxel.tilemap(nb_map).pset(50, 10, (4, 8))
            elif nb_map == 1:
                pyxel.tilemap(nb_map).pset(54, 8, (0, 0))
                pyxel.tilemap(nb_map).pset(53, 8, (4, 8))
        elif pyxel.frame_count % 15 == 0:
            if nb_map == 0 or nb_map == 1:
                pyxel.tilemap(nb_map).pset(45, 11, (0, 0))
                pyxel.tilemap(nb_map).pset(46, 11, (4, 5))
                
                pyxel.tilemap(nb_map).pset(37, 7, (0, 0))
                pyxel.tilemap(nb_map).pset(38, 7, (4, 5))
            if nb_map == 0:
                pyxel.tilemap(nb_map).pset(49, 10, (4, 8))
                pyxel.tilemap(nb_map).pset(50, 10, (0, 0))
            elif nb_map == 1:
                pyxel.tilemap(nb_map).pset(54, 8, (4, 8))
                pyxel.tilemap(nb_map).pset(53, 8, (0, 0))
        pyxel.blt(self.x, self.y, 0, u, 193, w, 31, 6)

        if changelevel == 1:
            pyxel.fill(0, 0, 0)
            pyxel.text(self.x-68, 0, "Chargement du niveau\n    aléatoire", 7)
            if pyxel.frame_count % 30 == 0:
                chrono+=1
            if chrono == 2:
                changelevel = 0
                nb_map = random.choice((3, 7))







class App:
    def __init__(self):
        pyxel.init(128, 128, title="LLC Courbe")
        pyxel.load("3.pyxres")

        pyxel.image(0).rect(0, 8, 24, 8, 2)

        global player
        player = Player(0, 0)
        pyxel.run(self.update, self.draw) # LANCEMENT DU JEU


    def update(self):
        if pyxel.btn(pyxel.KEY_ESCAPE):
            pyxel.quit()

        player.update()
        

    def draw(self):
        global liste_text, nb_map, changelevel
        pyxel.cls(0)

        pyxel.camera()
        if changelevel == 0:
            if nb_map <= 7:
                pyxel.bltm(0, 0, nb_map, (scroll_x // 4) % 128, 128, 128, 128)
                pyxel.bltm(0, 0, nb_map, scroll_x, 0, 128, 128, 2)

        pyxel.camera(scroll_x, 0)
        player.draw()




def game_over():
    global scroll_x, enemies
    scroll_x = 0
    player.x = 0
    player.y = 0
    player.dx = 0
    player.dy = 0
    enemies = []


App()
