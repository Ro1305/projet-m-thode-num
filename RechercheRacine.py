def bissection (f, x0, x1, tol):
    fx0 = f(x0)
    fx1 = f(x1)
    
    if fx0*fx1 > 0:
        print("Erreur : Les ordonnées des valeurs fournies ne sont pas de signe opposé")
        return [x0, 1]
    if fx0 == 0:
        return [x0, 0]
    if fx1 == 0:
        return [x1, 0]
    r = abs(fx1-fx0)
    
    while r>tol:
        x2 = (x0+x1)/2
        fx2 = f(x2)
        if fx2 == 0:
            return [x2, 0]
        if fx0*fx2>0:
            x0 = x2
            fx0 = fx2
        else :
            x1 = x2
            fx1 = fx2
        
        r = abs(fx1-fx0)
    return [x2, 0]

def secante (f, x0, x1, tol):
    fx0 = f(x0)
    fx1 = f(x1)
    
    if fx0 == 0:
        return [x0, 0]
    if fx1 == 0:
        return [x1, 0]
    r = abs(fx1-fx0)
    itérations = 0
    while r>tol:
        if fx1 - fx0 == 0:
            print("Erreur : Division par zéro (pente nulle)")
            return [x0, -1]
        x2 = x0 - fx0*(x1-x0)/(fx1-fx0)
        x0, fx0 = x1, fx1
        x1, fx1 = x2, f(x2)
        if fx1 == 0:
            return [x1, 0]
        r = abs(fx1-fx0)
        itérations+=1
        if itérations > 500:
            print("Erreur : Limite d'itérations atteinte")
            return [x2, -1]       
    return [x1, 0]