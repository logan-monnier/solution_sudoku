# Ce code nécessite l'installation de python-sat.
# Pour cela il faut taper la commande suivant dans un console shell :
# pip3 install python-sat[pblib,aiger]

from pysat.solvers import Minisat22

# Pour le sudoku, les variables représentent des triplets (i,j,k) avec i, j et k dans [0,8].
# Ces triplet on la signification suivante : la variable (i,j,k) est vraie ssi
# dans la solution du sudoku, la case de coordonnée (i,j) contient le chiffre k+1.

grille = [[0, 0, 0, 0, 2, 0, 0, 1, 7],
          [0, 3, 0, 0, 0, 7, 0, 0, 8],
          [0, 0, 0, 0, 9, 0, 6, 0, 0],
          [0, 8, 0, 9, 0, 2, 0, 6, 0],
          [4, 0, 6, 0, 0, 0, 3, 0, 2],
          [0, 2, 0, 6, 0, 3, 0, 7, 0],
          [0, 0, 7, 0, 6, 0, 0, 0, 0],
          [8, 0, 0, 7, 0, 0, 0, 5, 0],
          [2, 5, 0, 0, 3, 0, 0, 0, 0]]

# On définit l comme étant les chiffres dans [0,8]
l = list(range(0, 9))

# pos contient tous les triplets (i,j,k) possibles

pos = [(i,j,k) for i in l for j in l for k in l]

def encode(i,j,k):
    """La fonction encode prend un triplet (i,j,k) de pos en argument et renvoie un nombre qui indique la variable correspondant à ce triplet.
    """
    return 1 + i + j* 9 + k * 81

def decode(n):
    """Decode prend en argument prend un nombre entre 1 et 729 qui représente une variable représentant un triplet (i,j,k) et renvoie le triplet correspondant.
    """
    m = n-1
    i = m % 9
    m= m//9
    j = m % 9
    k = m//9
    return (i,j,k)

# Instancier la variable phi1 par la contrainte SAT qui indique que
# toute case contient une valeur

phi1 = [[encode(i, j, k) for k in l] for j in l for i in l]

# Instancier la variable phi2 par la contrainte SAT qui indique
# qu'une case contient au plus une valeur

phi2 = [[-encode(i, j, k), -encode(i, j, k+1)] for (i, j, k) in pos]

# Instancier la variable phi3 par la contrainte SAT qui indique que
# sur une ligne au plus une fois chaque valeur

phi3 = [[-encode(i, j, k), -encode(i2, j, k)] for (i, j, k) in pos for i2 in l if i2 != i]

# Instancier la variable phi4 par la contrainte SAT qui indique que
# sur une colonne au plus une fois chaque valeur

phi4 = [[-encode(i, j, k), -encode(i, j2, k)] for (i, j, k) in pos for j2 in l if j2 != j]

# Instancier la variable phi5 par la contrainte SAT qui indique que
# sur un carré au plus une fois chaque valeur.

# Pour cela on peut (ce n'est pas obligé) écrire une fonction carre correspondant
# à la spécification suivante:

def carre(i1,j1,i2,j2):
    """Indique si les cases (i1,j1) et (i2,j2) appartiennent au même carré.

    Le résultat est indifférent (i.e. peut être True ou False) lorsque
    (i1,j1) et (i2,j2) sont sur la même ligne ou la même colonne.
    """
    return i1//3+j1//3*3==i2//3+j2//3*3

phi5 = [[encode(i%3+(j*3)%9, i//3+j//3*3, k) for i in l] for j in l for k in l]

# Instancier la variable phi6 par la contrainte SAT qui
# représente la grille de l'énoncé.

phi6 = [[encode(i, j, grille[i][j]-1)] for j in l for i in l if grille[i][j] != 0]

# Cette partie du programme lance le solveur SAT avec la conjonction des contraintes,
# c'est-à-dire la concaténation des listes les représentant.
with Minisat22(bootstrap_with=phi1+phi2+phi3+phi4+phi5+phi6) as m:
    # si on trouve une solution
    if m.solve():
        model = [decode(v) for v in m.get_model() if v >0] # on récupère les
                                                           # variables qui sont
                                                           # vraies dans la solution
                                                           # trouvée
        # On affiche le résultat lisiblement
        r = [[0 for i in l] for j in l]
        for (i,j,k) in model:
            r[i][j] += k+1
        print("\n")
        for ligne in r:
            print(ligne)

    else:
        print("pas de solution")
