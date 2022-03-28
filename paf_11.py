############################################################################ REGLES DU JEU  ############################################################################################
#   FAIRE  LE MEILLEUR SCORE
#   POUR CELA, ALLER LE PLUS LOIN POSSIBLE EN RAMASSANT DES PIECES ,  LE SCORE FINAL VAUT LE NOMBRE DE PIECES x 1000 + LA DISTANCE (3 PIECES MAX)
# ATTENTION IL NE FAUT PAS TOMBER DANS LES TROU SINON LA PARTIE EST PERDUE
########################################################################################################################################################################################

############################################################################ BUGS  ######################################################################################################
#   1 - NAIN SUIS TRAJECTOIRE HORIZONTALE A L INFINI SI SAUT EN VALEUR NEGATIVE (EN ARRIERE)  ET POUR UNE CERTAINE PETITE VALEUR POSITIVE
#   2 - SI LE JOUEUR PASSE DE L ETAT 0 A L ETAT 1 APRES ETRE REVENU DE L ETAT 1, IL NE PEUT PAS REPASSER 0 L ETAT 1
#   3 - LORS DE LA PHASE DE VOL , LE NAIN PEUT REBONDIR ALORS QU'IL EST AU DESSUS D4UN TROU
########################################################################################################################################################################################


#####################################################################################################
## DEFINTIONS 
#####################################################################################################
from pygame_functions import *
from pygame.locals import *
import pygame, math, sys, os, random , time , pickle

def game():
    
    ### On défini l'état du nain
    state=0
    
    #On créé ma console 
    screenSize(1678,1000)
    
    ## détermine la police des textes qui seront affichés
    font = pygame.font.SysFont(None, 20)

    ### BACKGROUND : on initalise une liste d images 
    BG=[r"C:\Users\pablo\Desktop\Projet Transverse\BG_Trou_V1.jpg",  r"C:\Users\pablo\Desktop\Projet Transverse\BG_V1.jpg" , r"C:\Users\pablo\Desktop\Projet Transverse\BG_V1.jpg"]

    ### CHARIOTS : on défini un Sprite Chariot 
    chariot_nain= makeSprite(r"C:\Users\pablo\Desktop\Projet Transverse\chariot_2_BIS.png") #SPRITE CHARIOT + NAIN
    addSpriteImage(chariot_nain,r"C:\Users\pablo\Desktop\Projet Transverse\chariot-pencher_sans_nain_BIS.png") #SPRITE CHARIOT PENCHE 
    addSpriteImage(chariot_nain,r"C:\Users\pablo\Desktop\Projet Transverse\chariot-pencher_BIS.png")  #SPRITE CHARIOT PENCHE + NAIN
    addSpriteImage(chariot_nain,r"C:\Users\pablo\Desktop\Projet Transverse\thumbnail_feu1.png") #SPRITES FLAMES
    addSpriteImage(chariot_nain,r"C:\Users\pablo\Desktop\Projet Transverse\thumbnail_feu2.png")
    addSpriteImage(chariot_nain,r"C:\Users\pablo\Desktop\Projet Transverse\thumbnail_feu3.png")
    addSpriteImage(chariot_nain,r"C:\Users\pablo\Desktop\Projet Transverse\thumbnail_feu4.png")
    addSpriteImage(chariot_nain,r"C:\Users\pablo\Desktop\Projet Transverse\thumbnail_feu5.png")
    addSpriteImage(chariot_nain,r"C:\Users\pablo\Desktop\Projet Transverse\thumbnail_feu6.png")
    addSpriteImage(chariot_nain,r"C:\Users\pablo\Desktop\Projet Transverse\thumbnail_feu7.png")
    addSpriteImage(chariot_nain,r"C:\Users\pablo\Desktop\Projet Transverse\thumbnail_feu8.png")
    addSpriteImage(chariot_nain,r"C:\Users\pablo\Desktop\Projet Transverse\thumbnail_feu9.png")
    addSpriteImage(chariot_nain,r"C:\Users\pablo\Desktop\Projet Transverse\vide.png")  #SPRITE VIDE 

    ###NAIN : on défini un Sprite Chariot 
    nain= makeSprite(r"C:\Users\pablo\Desktop\Projet Transverse\nain1.png")   # SPRITE NAIN ALLONGE 

    ### AUTRE : o défnini les Sprites restants
    Game_over= makeSprite(r"C:\Users\pablo\Desktop\Projet Transverse\Game_over.png")  # SPRITE GAME OVER
    Quit_game=makeSprite(r"C:\Users\pablo\Desktop\Projet Transverse\Quit_Game_Button.png") # SPRITE QUIT GAME



    chariotImg=0   #On intialise le compteur qui donnera le numéro de l'image voulue pour le sprite chariot 

    #Initialisation des variables A et B, qui vont permettre de faire tourner les boucles while de chaque état du chariot 
    A=False
    B=False


    xPos=0  #accélération
    xChar=0   #memoire de position du chariot permettant de le deplacer en horizontal selon la vitesse du défilement du fond d'écran
    x=0  # coordonnée horizontale du chariot
    xMem=0  #mémoire sur la position horizontale du nain au moment du début du vol
    xPress=0  #décélération du chariot pour le state 0
    xPosMem=0   #memoire sur l'acceleration
    yPos=280  #position verticale
    F=0    #force appliquée par le joueur qui appuie sur un touche 
    m=2.5      #masse
    g=9.81 #acceleration due to gravitation force
    cpt2=0  #permet de stopper la chute dans le trou auw bonnes coordonnées 
    cptF=-1  #permet le sens du déplacement vertical
    f=0  #compteur pour changer image des flames

    h=0  #Permet d'appliquer equation physique du sommet de la parabole formée par le vol 
    effective_h=0   # h  que l 'on va appliquer => résultat de la valeur de h comme étant un pourcentage de la hauteur totale


    #variables nécesaires pour les pièces
    coins=[]    #liste de tout les Sprites d'une pièce 
    coinx=[]    #liste de toutes les coordonnées X des  Sprites  pièce 
    coiny=[]    #liste de toutes les coordonnées T des  Sprites  pièce 
    coinY=0   #coordonnées Y d'une pièce 
    coinX=0   #coordonnées X d'une pièce 
    CoinPos=0    ##coordonnées X d'une pièce actualisée 
    coinImg=0    #numéro de l image affichée par le sprite pièce
    CoinIMG=[]   #liste des coinImg pour chaque pièce
    Cash=0     # somme des pièces gagnées
    Money=''   #permettra d'afficher Cash comme une suite de caractères 

    #variable nécessaire pour le score
    Score=''   #permettra d'afficher le score comme une suite de caractères 

    Quit=" " #permettra d'afficher la suite de caractères qui demande de cliquer sur echap

    ##pour changer des parametres
    A1 =""   #permettra de récuperer le caractère voulu pour modifier la masse ou la gravité
    A2=" "   #permettra de récuperer le caractère voulu pour modifier la masse ou la gravité
    
    #Cette boucle permet d'actualiser le jeu, elle est active tant que le joueur n'appuie pas sur échap
    while True:
        
        # pour quitter la partie             
        for event in pygame.event.get(): #loop to quit the option and come back to the main loop with the menu
             if event.type == QUIT:
                 pygame.quit()
                 sys.exit()
             if event.type == KEYDOWN:
                 if event.key == K_ESCAPE:
                     running = False



        ### POUR CHANGER DES PARAMETRES DEPUIS LE SHELL => RETIRER '#' POUR RENDRE ACTIF #########################################
        #A1=input("DO YOU WANT TO CHANGE A PARAMETER ?  enter Y or N for YES or NO  :   ")
        #while A1!='y' and  A1!='Y' and  A1!='n' and  A1!='N':
        #    A1=input("DO YOU WANT TO CHANGE A PARAMETER ? enter Y or N for YES or NO :   ")
        #if A1=='y' or A1=='Y':
        #   A2=input("WHAT PARAMETER DO YOU WANT TO CHANGE ?   enter G for gravity's acceleration or W for dwarf's weight  :  ")
        #   while A2!='G' and  A2!='g' and  A2!='W' and  A2!='w':
        #        A2=input("WHAT PARAMETER DO YOU WANT TO CHANGE ?   enter G for gravity's acceleration or W for dwarf's weight  :  ")
        #if A2=='G' or  A2=='g':
        #    print("ENTER THE NEW VALUE FOR GRAVITY'S ACCELERATION (initially 9.81)  :   ")
        #    g=int(input())
        #if A2=='W' or  A2=='w':
        #    print("ENTER THE NEW VALUE FOR THE WEIGHT OF THE DWARF (initially 2.5)  :   ")
        #    m=int(input())
        #######################################################################################################
        #####################################################################################################
        ## BOUCLE D'INITIALISATION DU JEU
        #####################################################################################################




        
        ####################################################################################################
        ##CREER LES 3 PIECES DISPONIBLES
        ####################################################################################################
        for i in range (3):
            ### PIECE
            new_coin=makeSprite(r"C:\Users\pablo\Desktop\Projet Transverse\coin.png")  #CREE UN SPRITE PIECE 
            addSpriteImage(new_coin,r"C:\Users\pablo\Desktop\Projet Transverse\vide.png")  #SPRITE VIDE N 12
            coinX=int(random.randint(7400,40000))  #SELECTIONNE UNE COORDONNEE X AU HASARD entre 7400 (premier trou) et 400000 (limite supposée)
            coinY=int(random.randint(0,350))    #SELECTIONNE UNE COORDONNEE Y AU HASARD entre 0 et 350 (hauteur max de la fenetre dans laquelle le nain se deplace)
            CoinIMG.append(coinImg)   #ajoute l etat du sprite a une liste des etats de sprite de toutes les pieces 
            coins.append(new_coin)   #ajoute le sprite piece a une liste des sprites de pieces
            coinx.append(coinX)  #ajoute la coordonnée x du sprite piece  a une liste de coordonnées x de sprites de pieces 
            coiny.append(coinY)    #ajoute la coordonnée y du sprite piece  a une liste de coordonnées y de sprites de pieces 
            moveSprite(coins[i],coinx[i],coiny[i])  #déplace le sprite de la piece qui vient d etre créee aux coordonnées générées aléatoirement 
            showSprite(coins[i]) #affiche une premiere fois les pieces => on ne les voit pas car leurs coordonnées sont plus grandes que les limites de la console 
        
        #####################################################################################################
        ## STATE 0 - INTRO  --> le chariot se déplace de gauche a droite dans la moitié gauche de la console : ainsi le chariot ne se déplace pas à l'infini sur la gauche 
        #####################################################################################################

        if state==0:
            
            #on pose un premier  background 
            setBackgroundImage( BG[1] )
            xPress=0  #on redéfini xPress à 0 car il sinon il a déja une valeur si le chariot revient de l etat 1 
            
            #####################################################################################################
            ## DEMARRE LA BOUCLE 
            #####################################################################################################
            while A==False and B==False:  #cette boucle tourne tant que les deux conditions sont vérifiées : c est le cas car ce sont les valeurs de base de A et B 
                
                tick(60) #frames per second  : cette fonction permet de choisir le nombre de frames par secondes
                
                #pour limiter mvt sur la gauche
                if x>=0:
                    #mouvement vers la droite
                    if keyPressed("right") :  #détecte quand la flèche droite est pressée
                        x+=5    #on modifie la position du chariot 
                        xPress+=1  #on enregistre que la flèche à été pressé une fois 
                        
                    #mouvement vers la gauche
                    elif keyPressed("left"):   #meme processus avec la fleche gauche 
                        x-=5
                        xPress-=1
                    
                    #arrête la poussée si aucune touche n'est pressée : permet d avancer en décélérant, pour pus de réalisme 
                    else:
                        if xPress>0:  #si le mouvement partait vers la droite 
                            x+=5
                            xPress-=0.5
                        elif xPress<0: #si le mouvement partait vers la droite 
                            x-=5
                            xPress+=0.5
                        
                else:   #ce else se réfère au if x>=0, il permet de ne pas dépasser sur la gauche, en autorisant uniquement un mvt vers la droite
                    xPress=0
                    #mouvement vers la droite
                    if keyPressed("right") :   
                        x+=5
                    

                if x>650: #Si la position horizontale x dépasse 650 , alors on passe à l'état 1, a partir du quand on peut sauter 
                    x+=10  #permet de bien marquer la scission entre etat 1 et 0
                    state=1  #passage au state 1
                    A=True  #permet de farie tourner le while du state 1, et arrete le while du state 0 

                
                #met à jour Sprite
                moveSprite(chariot_nain,x,280)  #déplace le chariot horizontalement selon la valeur de x a chaque nouvelle itération du while
                    
                    
                #affiche sprite chariot+nain
                showSprite(chariot_nain)  #permet d'afficher le chariot a chaque nouvelle itération du while

                
                

        #####################################################################################################
        ## STATE 1 - BASIC MOVE  : à partir d'ici c est le fond d'écran qui se déplace et non le chariot, cet etat permet d'acéder aux etats 2 et 3 , respectivement l'envol et la chute 
        #####################################################################################################
        if state==1:
            
            #on pose une certaine suite de backgrounds, qui vont s'enchainer infiniment 
            setBackgroundImage( [BG[1],BG[2],BG[1],BG[2],BG[0]] )  

            #####################################################################################################
            ## DEMARRE LA BOUCLE 
            #####################################################################################################
            while A==True and B==False:  #cette boucle tourne tant que les deux conditions sont vérifiées : c est le cas car ce sont les valeurs de base de A et B 
                
                tick(60) #frames per second  : cette fonction permet de choisir le nombre de frames par secondes
                
                #mouvement vers la droite
                if keyPressed("right") :  #détecte quand la flèche droite est pressée
                    F-=0.5  #applique de la force sur le chariot (ici le signe est inversé car on applique le déplacement au fond d'écran, qui se déplace donc dans le sens inverse) 

                    
                #mouvement vers la gauche
                elif keyPressed("left"):   #détecte quand la flèche gauche est pressée
                    F+=0.5   #applique de la force sur le chariot (ici le signe est inversé car on applique le déplacement au fond d'écran, qui se déplace donc dans le sens inverse) 

                    
                #arrête la poussée si aucune touche n'est pressée  : applique décélération 
                else:  
                    if F>0:
                        F-=0.5  
                    else:
                        F+=0.5
         

                        
                           
                #applique mouvement
                xPos=int(F/m)  #ici on a bien l 'accélération qui vaut la force fois la masse (cf . Lois de Newton)
                x-=xPos  #x mesure la distance parcourue, c est l opposé de l'accélération car l'accélération est appliquée au fond d 'écran et non au chariot
                
                        
                 # on passe au state 1 on appuyant sur espace 
                if keyPressed("space"):   #détecte si l'on appuie sur espace
                    xPosMem=xPos  #enregistre xPosMem comme l'accélération (et donc la vitesse) à laquelle le nain commence son saut
                    xMem=x   #enregistre xPosMem comme la position à laquelle le nain commence son saut
                    state=2  #permet de passer a l'état 2, état du saut 
                    B=True  #modifie la variable qui stoppe le while du state 1 et fait fonctionner le while du state 2
                    chariotImg+=1  #change valeur du compteru de sprite
                    changeSpriteImage(chariot_nain,chariotImg)  #applique le changement de sprite 
                    
                if x>=7204 and B==False:  #permet de passer a l 'état 3 (chute) si la barre espace n est pas pressée et la valeur de x trop grand (coordonnée X du trou)
                    state=3  #permet de passer a l'état 2, état de la chute 
                    A=False #modifie la variable qui stoppe le while du state 1 et fait fonctionner le while du state 3
                    B=True  #modifie la variable qui stoppe le while du state 1 et fait fonctionner le while du state 3
                    
                #on repasse au state 0 pour ne pas déborder sur la gauche 
                if x<=650:  #permet de passer a l 'état 0 si la coordonnées x est asssez petit
                    x=640  #permet de marquer la démarcation 
                    state=0 #permet de passer a l'état 0 , ou le chariot se déplace et non le fond d 'écran 
                    A=False  #modifie la variable qui stoppe le while du state 1 et fait fonctionner le while du state 0
                       
                #applique mouvement horizontal au background selon valeur de xPos
                scrollBackground(xPos,0) 
                
                #met à jour Sprite chariot + nain 
                moveSprite(chariot_nain,651,280)
                    
                    
                #affiche sprite chariot + nain 
                showSprite(chariot_nain)
            
                
        #####################################################################################################
        ## STATE 2 - FLIGHT  : était correspondant au saut 
        #####################################################################################################

        if state==2:
            
            
            #caclule la hauteur max de la parabole selon la formule physique 
            h=int(((xPosMem^2)*(0.12)/(4*g))*100)
            #applique h adapté au jeu, sous la forme de pourcentage de la taille verticale de la fenetre
            effective_h= int ((-h)*350/10)
            
            # modifie image du sprite chariot penché sans nain 
            chariotImg=1
            changeSpriteImage(chariot_nain,chariotImg)

            #####################################################################################################
            ## DEMARRE LA BOUCLE 
            #####################################################################################################
            while A==True and B==True:  #cette boucle tourne tant que les deux conditions sont vérifiées : c est le cas car ce sont les valeurs de base de A et B 
                
                #Ici x continue de progresser mais selon la derniere valeure de l accélération xPos
                x-=xPosMem
                
                tick(60) #frames per second
                
                
                # fait disparaître le chariot sans nain , une fois que celui ci sort de la console
                xChar+=xPosMem
                if 651+xChar<=-400 :  #651 = position de base du chariot
                    chariotImg=12
                    changeSpriteImage(chariot_nain,chariotImg)
                     
                #### FIN PARTIE  : quand le nain a fini son vol 
                if xPosMem==0 : 
                    yPos=350  #le fait se stopper a la hauteur des rails
                    ### AFFICHE LE SCORE ET ENREGISTRE LE RECORD
                    Score="Score : "   
                    Score+=str(x-xMem + Cash)
                    score=x-xMem+Cash
                    highscore=get_highscore()
                    change_highscore(score,highscore)
                    ScoreSprite = makeLabel(Score, 80, 20, 20, fontColour='white', font='Arial', background="clear")
                    showLabel(ScoreSprite)
                    
                    ###AFFICHE LE NOMBRE DE PIECES GAGNEES
                    Money="Cash  : "
                    Money+=str(Cash)
                    MoneySprite = makeLabel(Money, 80, 20, 90, fontColour='white', font='Arial', background="clear")
                    showLabel(MoneySprite)
                    
                    ### ANNONCE QU IL FAUT QUITTER 
                    Quit="Press 'Esc' to leave"
                    QuitSprite = makeLabel(Quit, 80, 550, 20, fontColour='white', font='Arial', background="clear")
                    showLabel(QuitSprite)
                    #Annonce fin de partie
                    #AFFICHE SPRITE "QUIT GAME"
                    moveSprite(Quit_game,830,300,True)   
                    showSprite(Quit_game)
        
                    
                    
                #on augmente le compteur pour varier yPos et stopper chariot
                if (yPos>=350 or yPos<=350-effective_h) and effective_h!=0:  #fonctionne si le nain atteinds le sol ou la limite en hauteur, et que la hauteur limite n est pas le sol 
                    cptF+=1 #selon valeur de ce compteur, yPos monte ou descend 
                    
                    
                if yPos>=350:  
                    xPosMem=int(xPosMem-(3*xPosMem/10))   #a chaque rebond , l'accélération diminue d'un tier 
                    # on calcule la hauteur max avec sin(20°)=0,34  => sin^2(20)=0.12
                    h=int(((xPosMem^2)*(0.12)/(4*g))*100)
                    effective_h=int ( (-h)*350/10)  #on applique h comme pourcentage de la hauteur 
                    if effective_h<=-120: #délimite la hauteur max
                        effective_h=120
                    
                #on applique la force verticale  positive ou negative selon la valeur du compteur cptF, et tant que la hauteur max appliquée n est pas 0 
                if cptF%2==0 and effective_h!=0:  
                    yPos+=int(g/m)    
                elif cptF%2==1 and  effective_h!=0 :  
                    yPos-=int(g/m)
                     
                #applique mouvement au background selon valeur de xPos
                scrollBackground(xPosMem,0)
                
                
                #met à jour Sprite chariot+nain et nain
                moveSprite(chariot_nain,651+xChar,280)
                moveSprite(nain,651,yPos)    
                    
                    
                #affiche sprite chariot+nain et nain
                showSprite(chariot_nain)
                showSprite(nain)

                #### PIECES ########################################################
                ## on déplace les pièces en même temps que le fond d'écran 
                for i in range (3):
                    CoinPos=coinx[i]-x  #on détermine leur position selon la progression du nain x
                    if 0<=CoinPos<1678:  #si leur position x est comprise dans la console alors on les affiches 
                        moveSprite(coins[i],CoinPos,coiny[i])
                        showSprite(coins[i])
                        ## COLLISION 
                        if touching(coins[i],nain) :  #on applique la fonction qui détecte une superposition de sprites
                            Cash+=1000  #on augmente la valeur de la monnaie
                            #on change l 'image du sprite piece pour applqiuer l image vide et ainsi faire disparaitre la piece car elle a été attrapée par le nain 
                            CoinIMG[i]=1
                            changeSpriteImage(coins[i],CoinIMG[i])             
                    elif 0>=CoinPos: #on change l 'image du sprite piece pour appliquer l image vide et ainsi faire disparaitre la piece , car elle est en dehors de la console
                        CoinIMG[i]=1
                        changeSpriteImage(coins[i],CoinIMG[i])

                
                

        #####################################################################################################
        ## STATE 3 - FALL : on fait tomber le nain si il est a la meme position X qu un trou 
        #####################################################################################################
                
        if state==3:
            
            if chariotImg==0: #on verifie que le Sprite arrivant est un chariot pas penché avec un nain
                chariotImg=2  #on transforme ce Sprite avec une image de chariot penché sans nain 
            changeSpriteImage(chariot_nain,chariotImg)  #on applique le changement de Sprite 
            
            #####################################################################################################
            ## DEMARRE LA BOUCLE 
            #####################################################################################################
            while A==False and B==True:  #cette boucle tourne tant que les deux conditions sont vérifiées : c est le cas car ce sont les valeurs de base de A et B 
                f+=1 #on lance un compteur qui augmente a chaque itération de la boucle while, afin de changer les images de la flamme pour créer animation
                print(f)  #ralenti flammes
                if cpt2<5  :  #permet de faire la chute et d 'atterir dans les coordonnées du fond du trou 
                    xPos-=5  #on modifie la coordonnée X du chariot 
                    yPos+=40 #on modifie la coordonnée Y du chariot 
                    cpt2+=1
                    
                    #applique mouvement au background selon valeur de xPos
                    scrollBackground(xPos,0)
                    
                    #met à jour Sprite
                    moveSprite(chariot_nain,650,yPos)
                    
                elif f%100==0 :  #permet de ralentir nombre d 'itérations 
                    if chariotImg<11 and keyPressed("esc")==False: 
                        #change image du sprite chariot (images des flammes)
                        chariotImg+=1
                        changeSpriteImage(chariot_nain,chariotImg)
                        #met à jour Sprite
                        moveSprite(chariot_nain,650,yPos)
                        if f>=1000:
                            ## AFFICHE Game Over et message de fin  a partir de quelques secondes
                            moveSprite(Game_over,830,300,True)
                            showSprite(Game_over)
                            Quit="Press 'Esc' to leave"
                            QuitSprite = makeLabel(Quit, 80, 550, 20, fontColour='white', font='Arial', background="clear")
                            showLabel(QuitSprite)
                            
                    elif chariotImg==11 and keyPressed("esc")==False:
                        #reveint à la première image de flame
                        chariotImg=3
                        
                        if f>=1000:
                            ## AFFICHE Game Over et message de fin  a partir de quelques secondes
                            moveSprite(Game_over,830,300,True)
                            showSprite(Game_over)
                            Quit="Press 'Esc' to leave"
                            QuitSprite = makeLabel(Quit, 80, 550, 20, fontColour='white', font='Arial', background="clear")
                            showLabel(QuitSprite)
                            
                            
                            
                # pour quitter la partie si on appuie sur echap     
                if keyPressed("esc")==True:
                    pygame.quit()


                        
                     
                
        #FIN DES STATES---------------------------------------------------------------------------------------------------------------------------
                


                

    #####################################################################################################
    ## QUITTER - APPUYER SUR 'ESC'
    #####################################################################################################  
    endWait()
