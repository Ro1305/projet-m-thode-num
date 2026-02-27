import numpy as np
def odefunction(x, y, profilTemperature):
    ns = 1.000272983820855
    Ts = 288.15
    z = y[0]
    i = y[1]
    T, dTdz = profilTemperature(z)
    
    dy = np.zeros(2)
    dy[0] = np.tan(i)
    dy[1] = (-(ns-1)*(Ts/T**2)*dTdz)*(1/(1+(ns-1)*(Ts/T)))
    return dy

def trajetRayonEuler(t_span, y0, dx, profilTemperature):
    x0, xf = t_span
    z0, i0 = y0
    
    x = [x0]
    Y = [np.array(y0)]
    
    while x[-1] < xf :
        h = min(dx, xf-x[-1])
        pente = odefunction(x[-1], Y[-1], profilTemperature)
        xs = x[-1] + h
        ys = Y[-1] + h * pente
        
        x.append(xs)
        Y.append(ys)
    
    return np.array(x), np.array(Y)
    

def profilTemperatureLin(z):
    h = 0.5
    Tsol = 30 + 2733.15
    Th = 15 + 273.15
    
    if z < h:
        dTdz = (Th - Tsol)/h
        T = Tsol + dTdz * z
    else: 
        T = Th
        dTdz = 0.0 
    return T, dTdz
