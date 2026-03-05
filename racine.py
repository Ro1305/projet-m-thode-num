def bissection(f, x0, x1, tol):
    a = min(x0, x1)
    b = max(x0,
    fa = f(a)
    fb = f(b)
    if fa == 0: 
        return [a, 0]
    if fb == 0:
        return [b, 0]
    
    if fa*fb > 0:
        print("Erreur : Les ordonnées des valeurs fournies ne sont pas de signe opposé")
        return [a, 1]
    
    r = abs(fa-fb)
    while r>tol :
        c = (abs(b)-abs(a))/2
        fc= f(c)
        
        if fc*fa > 0:
            a = c
            fa = fc
        if fc*fb>0:
            b = c
            fb = fc
        else :
            return [c, 0]
        r = abs(fa-fb)
        
    return [c, 0]

def secante(f, x0, x1, tol):
    a = min(x0, x1)
    b = max(x0, x1)
    fa = f(a)
    fb = f(b)
    if fa == 0: 
        return [a, 0]
    if fb == 0:
        return [b, 0]
    
    r = abs(fa-fb)
    iteration = 0
    while r>tol :
        
        c = a - fa*(b-a)/(fb-fa)
        fc = f(c)
        
        iteration +=1
        if iteration > 500:
            return [a, -1]
        