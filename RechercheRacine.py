def bissection (f, x0, x1, tol):
    fx0 = f(x0)
    fx1 = f(x1)
    
    if fx0*fx1 > 0:
        print("Erreur : Les ordonnées des valeurs fournies ne sont pas de signe opposé")
        return [x0, 1]
    if abs(fx0) < tol:
        return [x0, 0]
    if abs(fx1) < tol:
        return [x1, 0]
    x2 = (x0+x1)/2
    while abs(x0-x1)>tol:
        x2 = (x0+x1)/2
        fx2 = f(x2)
        if abs(fx2) < tol:
            return [x2, 0]
        if fx0*fx2>0:
            x0 = x2
            fx0 = fx2
        else :
            x1 = x2
            fx1 = fx2        
    return [x2, 0]

def secante (f, x0, x1, tol):
    fx0 = f(x0)
    fx1 = f(x1)
    
    if abs(fx0)<tol:
        return [x0, 0]
    if abs(fx1)<tol:
        return [x1, 0]
    if abs(fx1-fx0)<tol:
        print("Erreur")
        return[x0, 1]
    
    itérations = 0
    while abs(x1-x0)>tol:
        if fx1 - fx0 == 0:
            print("Erreur : Division par zéro (pente nulle)")
            return [x0, -1]
        x2 = x1 - fx1*(x1-x0)/(fx1-fx0)
        x0, fx0 = x1, fx1
        x1, fx1 = x2, f(x2)
        
        if abs(fx1) < tol:
            return [x1, 0]
        
        itérations+=1
        if itérations > 500:
            print("Erreur : Limite d'itérations atteinte")
            return [x2, -1]       
    return [x1, 0]