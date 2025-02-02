import numpy as np
import math
import concore
dT = 0.1
global Prev_Error, I, freq
Prev_Error = 0
I = 0

sp = concore.tryparam('sp', 67.5)
Kp = concore.tryparam('Kp', 0.075)
Ki = concore.tryparam('Ki', 0.02)
Kd = concore.tryparam('Kd', 0.005)
freq = concore.tryparam('freq',30)
sigout = concore.tryparam('sigout',True)
cin = concore.tryparam('cin', 'hr')

def  pid_controller(ym):
    global Prev_Error, I, freq
    if cin == 'hr':
        Error = sp - ym[1]
    elif cin == 'map':
        Error = sp - ym[0]
    else:
        print('invalid control input '+cin)
        quit()
    P = Error
    I = I + Error*dT 
    D = (Error - Prev_Error )/dT	
    amp = Kp*P + Ki*I + Kd*D
    Prev_Error = Error      
    if sigout:
        amp = 3.0/(1.0 + math.exp(amp))
    ustar = np.array([amp,freq])    
    return ustar


concore.default_maxtime(150)
concore.delay = 0.02
init_simtime_u = "[0.0, 0.0,0.0]"
init_simtime_ym = "[0.0, 70.0,91]"
u = np.array([concore.initval(init_simtime_u)]).T
print("Mayuresh's and Shannon's PID controller: sp is "+str(sp))
print(concore.params)
while(concore.simtime<concore.maxtime):
    while concore.unchanged():
        ym = concore.read(1,"ym",init_simtime_ym)
    ym = np.array(ym)
    
    if concore.simtime < 0:
        ustar = np.array([0.0,30.0])
    else:
        ustar =  pid_controller(ym)
    
    print(str(concore.simtime) + " u="+str(ustar) + "ym="+str(ym))
    concore.write(1,"u",list(ustar),delta=0)



#from ast import literal_eval
#try:
#    params = literal_eval(open(concore.inpath+"1/concore.params").read())
#except:
#    params = dict()


