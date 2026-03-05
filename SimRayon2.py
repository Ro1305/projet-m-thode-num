import numpy as np 
from scipy import integrate

def odefunction(x, y, profilTemperature):
    Ts = 288.15
    ns = 1.000272983820855
    z = y[0]
    i = y[1]
    T, dTdz = profilTemperature(z)
    dy = np.zeros(2)
    dy[0] = np.tan(i)
    dy[1] = (-(ns-1)*(Ts/T**2)*dTdz)*(1/(1+(ns-1)*(Ts/T)))
    return dy

def trajetRayonEuler(intervalle, y0, dx, profilTemperature):
    x0, xf = intervalle
    z0, i0 = y0
    
    x = [x0]
    Y = [np.array(y0)]
    
    while x[-1] < xf :
        dx2 = min(dx, xf-x[-1])
        pente = odefunction(x[-1], Y[-1], profilTemperature)
        xs = x[-1] + dx2
        ys = Y[-1] + dx2 * pente
        
        x.append(xs)
        Y.append(ys)
    return np.array(x), np.array(Y).T

def profilTemperatureLin(z):
    h = 0.5
    Th = 288.15
    Tsol = 303.15
    if z < h :
        T = ((Th-Tsol)/h)*z+Tsol
        dTdz = (Th-Tsol)/h
    else :
        T = Th
        dTdz = 0
    return T, dTdz

def trajetRayonIVP(intervalle, y0, rtol, profilTemperature):
    sol = integrate.solve_ivp(odefunction, intervalle, y0, rtol=rtol, args=(profilTemperature, ))
    return sol.t, sol.y



x_ivp, y_ivp = trajetRayonIVP(intervalle, y0, 1e-10, profilTemperatureLin)
z_final_ref = y_ivp[0, -1]