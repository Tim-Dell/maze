##----- Importation des Modules -----##
from tkinter import *
from functools import partial
from random import *
from enum import Enum
direction_id = 0
    
def creaboard(n,c):    ##----- Création du caneva -----##
    global board
    board = Canvas(fen, width = n*c+2, height = n*c+2, bg = 'white')
    board.grid(row = 0, column = 0, rowspan=4, padx=3, pady=3)
    edge = board.create_rectangle(2,2,n*c+2,n*c+2)


def mazesize():
    global c
    check = 0
    str_n = size_form.get()
    n = int(str_n)
    
    if 4 < n <= 15:
        c = 30
    elif 4 < n <= 30:
        c = 20
    elif 4 < n <= 80:
        c = 10
    else:
        ADD.itemconfigure(scrolltxt, text = 'OUPS ! Il Faut Saisir Un Nombre Entier Entre 5 Et 80')
        warning(0,"red")
        check = 1
    
    if check == 0:
        ADD.itemconfigure(scrolltxt, text = "C'est Parti ! Dirigez-Vous A L'aide Des Fleches")
        warning(0,"spring green")
        
    return n,c
                

def vertiwalls(c,n):    #création murs verticaux
    vertical = []
    for ligne in range(n):         
        for colonne in range(1,n):    
            vertical.append(board.create_line\
                    (c*colonne+2,ligne*c+2,c*colonne+2,ligne*c+2+c ))
    
    return vertical

def horiwalls(c,n):        #création murs horizontaux
    horizontal = []   
    for ligne in range(1,n):         
        for colonne in range(n):    
            horizontal.append(board.create_line\
                    (c*colonne+2,ligne*c+2,c*colonne+2+c,ligne*c+2 ))
    
    return horizontal

def initmaze(v,h,begin,end,n,c):    #initialisation du labyrinthe
    walls = []  #liste murs à visitée"
    vtiles = [] #liste cases visitée"
    walls2 = [] #liste de tout les murs ayant déjà été traité" #évite un double traitement a l'infini
    vertif = [] #liste des murs du labyrinthe à la fin"
    horif = []  
    
    vtiles.append(begin)
    
    walls.append( v[begin-begin//n] ) #ajoute le mur de droite aux murs à visité
    walls2.append(v[begin-begin//n] )
    if begin >= n:
        walls.append( h[begin-n] )    #du haut
        walls2.append(h[begin-n] )
    if begin < n*n-n:                       
        walls.append( h[ begin ] )      #d'en bas
        walls2.append(h[ begin ] )
    
    initsq = board.create_rectangle(2, (begin//n)*c+3, c+1, (begin//n)*c+c+1, \
                                    outline = 'light pink', fill = 'light pink')#première case
    endsq = board.create_rectangle(n*c-c+3, (end//n)*c+3, n*c+3, (end//n)*c+c+1, \
                                   outline = 'pale green', fill = 'pale green') #dernière case
    return vtiles,walls,walls2, vertif, horif,

def choosewall(w):          #choisi le mur a traité
    x = randint(0,len(w)-1)
    return x
    

def tileman(vt,w,x,n):         #gère le traitement des cases du labyrinthe        

    "----------horizontal---------"
        
    if w[x] >= (n*n-n)+2:
        if w[x]-((n*n-n)+2) in vt and w[x]-((n*n-n)+2) +n in vt: #vérifie si deux cases ds vt
            tile = None
                
        elif w[x]-((n*n-n)+2) in vt:      #revérifie si une case ds vt
            board.delete(w[x])            #crée un passage entre deux cases
            tile = w[x]+n-((n*n-n)+2)
            vt.append(tile)               #ajoute l'autre case ds vt
                                
        else:                             #forcement une case déjà visitée.
            board.delete(w[x])
            tile = w[x]-((n*n-n)+2)
            vt.append(tile)
                        
    "----------vertical----------"
        
    if w[x] < (n*n-n)+2:
        if ((w[x]-2) //(n-1))+(w[x]-2) in vt and ((w[x]-2) //(n-1))+(w[x]-2) +1 in vt:
            tile = None
            
        elif ((w[x]-2) //(n-1))+(w[x]-2) in vt:
            board.delete(w[x])
            tile = ((w[x]-2) //(n-1))+(w[x]-2) +1
            vt.append(tile)
            
        else:
            board.delete(w[x])
            tile = ((w[x]-2) //(n-1))+(w[x]-2)
            vt.append(tile)
    
    return tile 
    

def wallman(v,h,w,w2,t,x,n,vertif,horif):   #gère le traitement des murs

    if t is None:
        if w[x] >= (n*n-n)+2:
            horif.append(w[x])
        else:
            vertif.append(w[x])

    del w[x]
    
    if t is not None:
        if t < n*n-n and h[t] not in w2:    #verifie exception
            w.append(h[t])          #mur bas
            w2.append(h[t])
        
        if t >= n and h[t-n] not in w2:
            w.append(h[t-n])        #mur haut
            w2.append(h[t-n])

        ###--###

        if t%n != 0 and v[t-(t//n)-1] not in w2:
            w.append(v[t-(t//n)-1])  #mur gauche
            w2.append(v[t-(t//n)-1])

        
        if (t+1)%n != 0 and v[t-(t//n)] not in w2:
            w.append(v[t-(t//n)])    #mur droit
            w2.append(v[t-(t//n)])

    return w,w2,vertif,horif

def moveright(vertif,x0,x1,y0,y1,c,n):  #gère le mouvement vers la droite
    move = 1
    #x coord += 1
    x0 += 1
    x1 += 1
    #check line
    line = ((y0 + y1)/2)//c
    #check walls in line + coords
    for element in vertif:
        if line*(n-1)+2 <= element and element < (line+1)*(n-1)+2:
            x00,y00,x11,y11 = board.coords(element)
            if x11 == x1:
                move = 0
    if move == 1:
        board.coords(player, x0,y0,x1,y1)

def moveleft(vertif,x0,x1,y0,y1,c,n):  #gère le mouvement vers la Gauche
    move = 1
    #x coord -= 1
    x0 -= 1
    x1 -= 1
    #check line
    line = ((y0 + y1)/2)//c
    #check walls in line + coords
    for element in vertif:
        if line*(n-1)+2 <= element and element < (line+1)*(n-1)+2:
            x00,y00,x11,y11 = board.coords(element)
            if x00 == x0:
                move = 0
    if move == 1:
        board.coords(player, x0,y0,x1,y1)

def movedown(horif,x0,x1,y0,y1,c,n):  #gère le mouvement vers la Gauche
    move = 1
    #y coord += 1
    y0 += 1
    y1 += 1
    #check column
    column = ((x0 + x1)/2)//c
    #check walls in column + coords
    for element in horif:
        if (element-n*(n-1)-2 - column)%n == 0:
            x00,y00,x11,y11 = board.coords(element)
            if y11 == y1:
                move = 0
    if move == 1:
        board.coords(player, x0,y0,x1,y1)

def moveup(horif,x0,x1,y0,y1,c,n):  #gère le mouvement vers la Gauche
    move = 1
    #y coord -= 1
    y0 -= 1
    y1 -= 1
    #check column
    column = ((x0 + x1)/2)//c
    #check walls in column + coords
    for element in horif:
        if (element-n*(n-1)-2 - column)%n == 0:
            x00,y00,x11,y11 = board.coords(element)
            if y00 == y0:
                move = 0
    if move == 1:
        board.coords(player, x0,y0,x1,y1)

def key(event):
    global direction_id
    if event.keysym == 'Right':
        direction_id = 1
    if event.keysym == 'Down':
        direction_id = 2
    if event.keysym == 'Left':
        direction_id = 3
    if event.keysym == 'Up':
        direction_id = 4

def playerman(vertif,horif,c,n): #gère les déplacement du joueur
    global direction_id

    x0,y0,x1,y1 = board.coords(player)

    if direction_id == 1:
        moveright(vertif,x0,x1,y0,y1,c,n)
    if direction_id == 2:
        movedown(horif,x0,x1,y0,y1,c,n)
    if direction_id == 3:
        moveleft(vertif,x0,x1,y0,y1,c,n)
    if direction_id == 4:
        moveup(horif,x0,x1,y0,y1,c,n)
        
    direction_id = 0
    fen.after(10, lambda: playerman(vertif,horif,c,n))

def mazegen():      #genère le labyrinthe, enclenche ses fonctionallitées
    global solve
    n,c = mazesize()
    ADD.configure( height = n*c-80)
    creaboard(n,c)
    v = vertiwalls(c,n)
    h = horiwalls(c,n)
    (begin, end)= (0,(n-1)*n)
    vtiles,walls,walls2, vertif, horif = initmaze (v,h,begin,end, n,c)

    while len(walls) > 0:
        choicew = choosewall(walls)
        tile = tileman(vtiles,walls,choicew,n)
        walls,walls2,vertif,horif = wallman(v,h,walls,walls2,tile,choicew,n,vertif, horif)

    grid = grid_gen(vertif, horif, n)
    solve = dfs_solver(grid, n, begin//n, 0, end, begin)
    #Le jeu commence une fois generé
    global player
    player = board.create_rectangle(0.5*c, begin/n*c+0.5*c, 0.5*c+4, begin/n*c+0.5*c+4, \
                                    outline = 'lavenderblush4', fill = 'lavenderblush4')

    playerman(vertif,horif,c,n)

def grid_gen(vertif, horif, n): #retranscrit le labyrinthe sous forme d'une grille
    grid = []

    for i in range(n):
        row = []
        for j in range(n):
            row.append(Tile())
        grid.append(row)

    for i in range(n):
        grid[i][0].addWall(Directions.LEFT)
        grid[i][n-1].addWall(Directions.RIGHT)
    for j in range(n):
        grid[0][j].addWall(Directions.UP)
        grid[n-1][j].addWall(Directions.DOWN)

    for i in range(n):
        for j in range(n):
            if (2+i*(n-1)+j) in vertif:
                grid[i][j].addWall(Directions.RIGHT)
    
            if (n*(n+i))-((n-2)-j) in horif:
                grid[i][j].addWall(Directions.DOWN)

            if (1+i*(n-1)+j) in vertif:
                grid[i][j].addWall(Directions.LEFT)
            if (n*(n-1+i)-((n-2)-j)) in horif:
                grid[i][j].addWall(Directions.UP)
    return grid
                

class Tile:
    
    def __init__(self):
        self.walls = set()

    def addWall(self, dir):
        self.walls.add(dir)

    def __repr__(self):
        return '/'.join({(dir.name) for dir in self.walls})
    

class Directions(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


def dfs_solver(grid, n, i, j , end, begin, visited=set(), sol=[]): #algorithme depth-first search
    if i == end/n and j == n-1:
        sol.append((i,j))
        return sol

    visited.add(grid[i][j])

    tile = grid[i][j]
    sol.append((i, j))

    if not (Directions.RIGHT in tile.walls) and not (grid[i][j + 1] in visited):
        path = dfs_solver(grid, n, i, j + 1, end, begin, set(visited.copy()) , sol.copy())
        if path != None:
            return path
    
    if not (Directions.LEFT in tile.walls) and not (grid[i][j - 1] in visited):
        path = dfs_solver(grid, n, i, j - 1, end, begin, set(visited.copy()) , sol.copy())
        if path != None:
            return path

    if not (Directions.UP in tile.walls) and not (grid[i - 1][j] in visited):
        path = dfs_solver(grid, n, i - 1, j , end, begin, set(visited.copy()) , sol.copy())
        if path != None:
            return path

    if not (Directions.DOWN in tile.walls) and not (grid[i + 1][j] in visited):
        path = dfs_solver(grid, n, i + 1, j, end, begin, set(visited.copy()) , sol.copy())
        if path != None:
            return path

def solve_tracer(solution, c): #permet de retracer le chemin de la solution
    for (x, y) in (solution):
        trace =  board.create_rectangle((y+0.5)*c, (x+0.5)*c, (y+0.5)*c+4, (x+0.5)*c+4, \
                                    outline = 'red', fill = 'red')


def warning(counter,color):     #animation
    if counter >= 20:
        ""
    elif counter%2 == 0:
        ADD.itemconfigure(line1, fill=color)
        ADD.itemconfigure(line2, fill=color)
        counter += 1
        fen.after(250, lambda: warning(counter,color))
    elif counter%2 == 1:
        ADD.itemconfigure(line1, fill="black")
        ADD.itemconfigure(line2, fill="black")
        counter += 1
        fen.after(250, lambda: warning(counter,color))    

def moveobj(anim,x,y):      #animation
    d = 1
    XO = x-d
    if XO < -200:
        XO += 500
    ADD.coords(anim,XO,y )                                                                   
    fen.after(20, lambda: moveobj(anim,XO,y))

def ADDroll():          #ajout d'interface
    global scrolltxt
    global line1
    global line2
    line1 = ADD.create_text(100, 10, text='- - - - - - - -', \
                       fill='black', font='System 30')
    scrolltxt = ADD.create_text(300, 30, text='Entrer La Taille Du Labyrinthe Ou La Commande', \
                       fill='black', font='System 10')
    line2 = ADD.create_text(100, 50, text='- - - - - - - -', \
                       fill='black', font='System 30')
    moveobj(scrolltxt,300,30)
 
        
def fengen():   #génère la fenêtre de jeu
    global fen
    global size_form
    global ADD
    global solve
    global c
    fen = Tk()
    fen.title('Maze')
    
    bouton_gen = Button(fen, text = "Generate", command = mazegen)
    bouton_gen.grid(row = 0, column = 1, sticky=W+E, padx=3, pady=3)

    bouton_solution_trace = Button(fen, text = "Solution", command = lambda: solve_tracer(solve,c))
    bouton_solution_trace.grid(row = 4, column = 1, sticky=W+E, padx=3, pady=3)

    size_form = Entry(fen, textvariable=StringVar())
    size_form.grid(row = 1, column = 1, sticky=W+E, padx=3, pady=3)

    ADD = Canvas(fen, width = 125, height = 200, bg = 'white')
    ADD.grid(row = 2, column = 1, padx=3, pady=3)
    ADDroll()

    bouton_quitter = Button(fen, text='Quitter', command=fen.destroy)
    bouton_quitter.grid(row = 3, column = 1, sticky=W+E, padx=3, pady=3)

    fen.bind('<Right>' , key)
    fen.bind('<Down>' , key)
    fen.bind('<Left>' , key)
    fen.bind('<Up>' , key)

    fen.mainloop()

##----- Programme principal -----##

fengen()
