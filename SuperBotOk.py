import random as rand

BLANCO='-'
TOT=0
J1={
    'pieces':'xX',
    'adversary':'oO',
    'crown':7,
    'direction':{
        'x':[(1,-1),(1,1)],
        'X':[(-1,-1),(-1,1),(1,-1),(1,1)]
        #igual
    }
}

J2={
    'pieces':'oO',
    'adversary':'xX',
    'crown':0,
    'direction':{
        'o':[(-1,-1),(-1,1)],
        'O':[(1,-1),(1,1),(-1,-1),(-1,1)]
        #se cambio
    }
}

def recmov(tablero,J,i,j):
    R=[]
    T=[]
    for dir in J['direction'][tablero[i][j]]:
        i_=i+2*dir[0]
        j_=j+2*dir[1]
        if i_ in range(8) and j_ in range(8) and tablero[i+dir[0]][j+dir[1]] in J['adversary'] and tablero[i_][j_]==BLANCO:
            T=recmov(makeMove(tablero,[(i,j),(i_,j_)],J),J,i_,j_)
            for k in range(len(T)):
                T[k]=[(i,j)]+T[k]
            R=R+T
    if len(R)==0:
        return [[(i,j)]]
    return R

def makeMove(tablero,m,J):
    E=[[tablero[i][j] for j in range(8)]for i in range(8)]
    if not (m is None):
        for i in range(1,len(m)):
            E[m[i][0]][m[i][1]]=E[m[i-1][0]][m[i-1][1]]
            E[m[i-1][0]][m[i-1][1]]=BLANCO
            if abs(m[i-1][0]-m[i][0])>1:
                x=int((m[i-1][0]+m[i][0])/2)
                y=int((m[i-1][1]+m[i][1])/2)
                E[x][y]=BLANCO
            if m[i][0]==J['crown']:
                E[m[i][0]][m[i][1]]=J['pieces'][1]

    return E

def moves(tablero,J):
    M=[]
    take=False
    for i in range(8):
        for j in range(8):
            if tablero[i][j] in J['pieces']:
                T=recmov(tablero,J,i,j)
                if len(T[0])>1:
                    take=True
                    M=M+T
    if not take:
        for i in range(8):
            for j in range(8):
                if tablero[i][j] in J['pieces']:
                    for dir in J['direction'][tablero[i][j]]:
                        if i+dir[0] in range(8) and j+dir[1] in range(8) and tablero[i+dir[0]][j+dir[1]]==BLANCO:
                            M=M+[[(i,j),(i+dir[0],j+dir[1])]]
    return M

def asegurar(E,M,J):
    s = []
    if J in J1['pieces']:
        ##print "estoy en asegurar J1"
        s=estaEnPeligro1(E,M,J)
        
        if s!=None:
            for k in range (len(M)):
                if M[k][1][0]==s[0] and M[k][1][1] == s[1]:
                    return M[k]
        
    if J in J2['pieces']:
        #print "estoy en asegurar J2"
 
        #for i in range (len(M)):
        #   print M[i]
        #return null 
        s=estaEnPeligro2(E,M,J)
        
        if s!=None:
            for k in range (len(M)):
                if M[k][1][0]==s[0] and M[k][1][1] == s[1]:
                    return M[k]
    return coronar(E,M,J)

def estaEnPeligro2(E,M,J):
    #print "validando estaEnPeligro2"
    for i in range (8):
        for j in range (8):
            #print E[i][j]
            if j+1<8 and i+1<8 and E[i][j] in J2['pieces'] and E[i-1][j-1] in J2['adversary']:
                if E[i+1][j+1] ==BLANCO:
                    #print "voy a retornar1"
                    return i+1,j+1
            elif j+1<8 and i+1<8 and E[i][j] in J2['pieces'] and E[i+1][j-1] ==BLANCO:
                if E[i-1][j+1] in J2['adversary']: 
                    #print "voy a retornar 2"
                    return i+1,j-1
            elif j+1<8 and i+1<8 and E[i][j] in J2['pieces'] and E[i+1][j-1] in J2['adversary'][1]:
                if E[i-1][j+1] ==BLANCO:
                    #print "voy a retornar 3"
                    return i-1,j+1  
            elif j+1<8 and i+1<8 and E[i][j] in J2['pieces'] and E[i-1][j-1] ==BLANCO:
                if E[i+1][j+1] in J2['adversary'][1] :
                    #print "voy a retornar 4"
                    return i-1,j-1
    #print "voy a retornar none"
    return None

def estaEnPeligro1(E,M,J):
    #print "validando estaEnPeligro1"
    for i in range (7 -1 -1):
        for j in range (7 -1 -1):
     #       print E[i][j]
            if j-1>=0 and i-1>=0 and E[i][j] in J1['pieces'] and E[i+1][j+1] in J1['adversary']:
                if E[i-1][j-1] ==BLANCO:
      #              print "voy a retornar 1"
                    return i-1,j-1
            elif j-1>0 and i-1>0 and E[i][j] in J1['pieces'] and E[i-1][j+1] ==BLANCO:
                if E[i+1][j-1] in J2['adversary']: 
       #             print "voy a retornar 2"
                    return i-1,j+1
            elif j-1 >0 and i-1>0 and E[i][j] in J1['pieces'] and E[i-1][j+1] in J1['adversary'][1]:
                if E[i+1][j-1] ==BLANCO:
        #            print "voy a retornar 3"
                    return i+1,j-1  
            elif j-1>0 and i-1>0 and E[i][j] in J1['pieces'] and E[i+1][j+1] ==BLANCO:
                if E[i-1][j-1] in J1['adversary'][1] :
         #           print "voy a retornar 4"
                    return i+1,j+1
    #print "voy a retornar none"
    return None

def coronar(E,M,J):
    #print "voy a coronar"
    for i in range (len(M)):
        if J in J1['pieces']:
            if M[i][1][0]==J1['crown']:
                return M[i]
        if J in J2['pieces']:
            if M[i][1][0]==J2['crown']:
                return M[i]
    return movQueen(E,M,J)

def movQueen(E,M,J):
    ##print "estoy en queen"
    return movUp(E,M,J)

def movUp(E,M,J):
    ##print "estoy en movUp"
    if J in J1['pieces']:
     #   print "estoy en movUp J1"
        for i in range(len(M)-1, -1, -1):
            if E[M[i][0][0]] [M[i][0][1]] in J1['pieces'][0]:
      #          print M[i][1][1] < M[i][0][1]
                if M[i][1][1] > M[i][0][1]:
       #             print "ok"
                    if M[i][1][1]<7:

                        ##if  E[(M[i][1][0])][(M[i][1][1]-2)] not in J2['pieces'] and E[(M[i][1][0])-1][(M[i][1][1])-3] not in J2['adversary']:
                        if (E[(M[i][1][0])+1][(M[i][1][1]+1)] not in J1['adversary']) and E[(M[i][1][0])+1][(M[i][1][1])-1] == BLANCO and E[(M[i][1][0])-1][(M[i][1][1])+1] == BLANCO:
        #                    print "Derecha 1"
                            return M[i]
                        elif E[(M[i][1][0])+1][(M[i][1][1])+1] not in J1['adversary'] and (E[(M[i][1][0])+1][(M[i][1][1]-1)] != BLANCO and E[(M[i][1][0])-1][(M[i][1][1])+1] != BLANCO):
         #                   print "Derecha 2"
                            return M[i]
                        elif E[(M[i][1][0])+1][(M[i][1][1])+1] not in J1['adversary'] and (E[(M[i][1][0])+1][(M[i][1][1]-1)] not in J1['adversary']) and E[(M[i][1][0])-1][(M[i][1][1])+1] == BLANCO:
          #                  print "Derecha 3"
                            return M[i]
                        elif E[(M[i][1][0])+1][(M[i][1][1])+1] not in J1['adversary'] and E[(M[i][1][0])+1][(M[i][1][1]-1)] != BLANCO and E[(M[i][1][0])-1][(M[i][1][1])+1] in J1['adversary'][1]:
           #                 print "Derecha 4"
                            return M[i]
                        elif E[(M[i][1][0])+1][(M[i][1][1])+1] not in J1['adversary'] and E[(M[i][1][0])+1][(M[i][1][1]-1)] == BLANCO and E[(M[i][1][0])-1][(M[i][1][1])+1] not in J1['adversary'][1]:
            #                print "Derecha 5"
                            return M[i]
                    else:
                        return M[i]
                
                if M[i][0][1]>M[i][1][1]:

                    #if M[i][1][1]>1:
                        ##if E[(M[i][1][0])][(M[i][1][1]+2)] not in J2['pieces'] and E[(M[i][1][0])-1][(M[i][1][1])+3] not in J2['adversary']:
                            
                            if (E[(M[i][1][0])+1][(M[i][1][1]-1)] not in J1['adversary']) and E[(M[i][1][0])+1][(M[i][1][1])+1] == BLANCO and E[(M[i][1][0])-1][(M[i][1][1])-1] == BLANCO:
             #                   print "Izquierda 1"
                                return M[i]
                            elif E[(M[i][1][0])+1][(M[i][1][1])-1] not in J1['adversary'] and (E[(M[i][1][0])+1][(M[i][1][1]+1)] != BLANCO and E[(M[i][1][0])-1][(M[i][1][1])-1] != BLANCO):
              #                  print "Izquierda 2"
                                return M[i]
                            elif E[(M[i][1][0])+1][(M[i][1][1])-1] not in J1['adversary'] and (E[(M[i][1][0])+1][(M[i][1][1]+1)] not in J1['adversary']) and E[(M[i][1][0])-1][(M[i][1][1])-1] == BLANCO:
               #                 print "Izquierda 3"
                                return M[i]
                            elif E[(M[i][1][0])+1][(M[i][1][1])-1] not in J1['adversary'] and E[(M[i][1][0])+1][(M[i][1][1]+1)] != BLANCO and E[(M[i][1][0])-1][(M[i][1][1])-1] in J1['adversary'][1]:
                #                print "Izquierda 4"
                                return M[i]
                            elif E[(M[i][1][0])+1][(M[i][1][1])-1] not in J1['adversary'] and E[(M[i][1][0])+1][(M[i][1][1]+1)] == BLANCO and E[(M[i][1][0])-1][(M[i][1][1])-1] not in J1['adversary'][1]:
                 #               print "Izquierda 5"
                                return M[i]
                    #else:
                     #   return m[i]

                
    if J in J2['pieces']:
     #   print "estoy en movUp J2"
        #for i in range (len(M)):
         #   print M[i]
        #return null 
        for i in range (len(M)):
            if E[M[i][0][0]] [M[i][0][1]] in J2['pieces'][0]:
 #               print M[i][0]
  #              print M[i][1]
   #             print M[i][0][1]
    #            print M[i][1][1] 
                if M[i][0][1]>M[i][1][1]:
                    ##if M[i][1][1]<7:
                        ##if E[(M[i][1][0])][(M[i][1][1]+2)] not in J2['pieces'] and E[(M[i][1][0])-1][(M[i][1][1])+3] not in J2['adversary']:
                            if (E[(M[i][1][0])-1][(M[i][1][1]-1)] not in J2['adversary']) and E[(M[i][1][0])-1][(M[i][1][1])+1] == BLANCO and E[(M[i][1][0])+1][(M[i][1][1])-1] == BLANCO:
      #                          print "Izquierda 1"
                                return M[i]
                            elif E[(M[i][1][0])-1][(M[i][1][1])-1] not in J2['adversary'] and (E[(M[i][1][0])-1][(M[i][1][1]+1)] != BLANCO and E[(M[i][1][0])+1][(M[i][1][1])-1] != BLANCO):
       #                         print "Izquierda 2"
                                return M[i]
                            elif E[(M[i][1][0])-1][(M[i][1][1])-1] not in J2['adversary'] and (E[(M[i][1][0])-1][(M[i][1][1]+1)] not in J2['adversary']) and E[(M[i][1][0])+1][(M[i][1][1])-1] == BLANCO:
        #                        print "Izquierda 3"
                                return M[i]
                            elif E[(M[i][1][0])-1][(M[i][1][1])-1] not in J2['adversary'] and E[(M[i][1][0])-1][(M[i][1][1]+1)] != BLANCO and E[(M[i][1][0])+1][(M[i][1][1])-1] in J2['adversary'][1]:
         #                       print "Izquierda 4"
                                return M[i]
                            elif E[(M[i][1][0])-1][(M[i][1][1])-1] not in J2['adversary'] and E[(M[i][1][0])-1][(M[i][1][1]+1)] == BLANCO and E[(M[i][1][0])+1][(M[i][1][1])-1] not in J2['adversary'][1]:
          #                      print "Izquierda 5"
                                return M[i]
                    #else:
                        #return m[i]
                if M[i][1][1] > M[i][0][1]:
                    if M[i][1][1]<7:
                        ##if  E[(M[i][1][0])][(M[i][1][1]-2)] not in J2['pieces'] and E[(M[i][1][0])-1][(M[i][1][1])-3] not in J2['adversary']:
                            if (E[(M[i][1][0])-1][(M[i][1][1]+1)] not in J2['adversary']) and E[(M[i][1][0])-1][(M[i][1][1])-1] == BLANCO and E[(M[i][1][0])+1][(M[i][1][1])+1] == BLANCO:
           #                     print "Derecha 1"
                                return M[i]
                            elif E[(M[i][1][0])-1][(M[i][1][1])+1] not in J2['adversary'] and (E[(M[i][1][0])-1][(M[i][1][1]-1)] != BLANCO and E[(M[i][1][0])+1][(M[i][1][1])+1] != BLANCO):
            #                    print "Derecha 2"
                                return M[i]
                            elif E[(M[i][1][0])-1][(M[i][1][1])+1] not in J2['adversary'] and (E[(M[i][1][0])-1][(M[i][1][1]-1)] not in J2['adversary']) and E[(M[i][1][0])+1][(M[i][1][1])+1] == BLANCO:
             #                   print "Derecha 3"
                                return M[i]
                            elif E[(M[i][1][0])-1][(M[i][1][1])+1] not in J2['adversary'] and E[(M[i][1][0])-1][(M[i][1][1]-1)] != BLANCO and E[(M[i][1][0])+1][(M[i][1][1])+1] in J2['adversary'][1]:
              #                  print "Derecha 4"
                                return M[i]
                            elif E[(M[i][1][0])-1][(M[i][1][1])+1] not in J2['adversary'] and E[(M[i][1][0])-1][(M[i][1][1]-1)] == BLANCO and E[(M[i][1][0])+1][(M[i][1][1])+1] not in J2['adversary'][1]:
               #                 print "Derecha 5"
                                return M[i]
                    else:
                        return M[i]
    return rand.choice(M)

def player(E,J):
    jj=None
    M=[]
    if J in J1['pieces']:
        M=moves(E,J1)
    elif J in J2['pieces']:
        M=moves(E,J2)
    if len(M)==0:
        return None
    return asegurar(E,M,J)