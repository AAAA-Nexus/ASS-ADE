import math, json

C1=float(0x2FFD0); C2=float(0x30114); G18=324.0
RG=47.0; DMAX=23.0
TAU=1820/1823; EPS_KL=1/C2
PHI_B=math.asin(1/3); MRATIO=0.36234099721733237232
V_AI=1/6; R_DECAY=PHI_B*(C2/C1)

# BLOCK 0: Sovereign invariants + omega identity
b0=[1.0,C1/C2,G18/C2,0.0,PHI_B,math.sin(PHI_B),math.cos(PHI_B),TAU,
    1820/C2,1823/C2,EPS_KL*C2,EPS_KL*1e5,108/C2,108/C1,108/G18,
    DMAX/RG,RG/100,DMAX/100,(1823%24)/24,math.log2(C1)/20,
    math.log(C2)/20,math.sqrt(2),math.pi/16,math.e/8]

# BLOCK 1: Structural group ratios
b1=[MRATIO,MRATIO/(8*math.pi),47*MRATIO/(8*math.pi),0.0,(C2-1)/C2,
    47*59*71/C2,323/C2,17*19/C2,71/100,(24+47)/100,756/C1,264/C1,
    92/264,86/264,6/264,92/86,244823040/1e9,95040/1e6,
    math.log2(244823040)/30,30/100,720/C2,1152/C2,3/8,0.2312]

# BLOCK 2: Operational constants
b2=[C1/(8*math.pi)/1e4,2*math.cos(math.pi/30)/2,
    1/math.sqrt(C1)*1000,1/24,47*PHI_B/100,V_AI,R_DECAY,
    C1/720/1000,TAU*(1-EPS_KL),720/G18,(C1/720/3)+1,
    0.85,0.70,0.50,0.65,0.75,0.85,G18/1000,RG/1000,DMAX/100,
    1/6,math.log2(1/EPS_KL)/20,(C1/720)*math.log2(1/EPS_KL)/5000,249000/1e6]

# BLOCK 3: E8 eigenvalues + Coxeter exponents
e8_ev=[1.9890437907,1.4862896509,0.8134732861,0.4158233816,
       -0.4158233816,-0.8134732861,-1.4862896509,-1.9890437907]
e8_exp=[1,7,11,13,17,19,23,29]
b3=[v/2 for v in e8_ev]+[m/30 for m in e8_exp]+[
    8/30,240/C2,30/100,1152/C2,math.cos(math.pi/30),
    math.sqrt(8)/3,3/8,8/24]

# BLOCK 4: Lean4 module theorem counts /100 + total
thm=[87,94,68,41,30,92,31,32,33,29,26,11,10,8,8,5,4,4,2,0,0]
b4=[c/100 for c in thm]+[0.0,0.0,538/1000]

# BLOCK 5: Key derived parameters
b5=[7820.873904/10000,1.98904379074/2,720/1000,0.002255549842,1/24,
    0.339836909454,0.01441709,47*0.01441709,0.3333333333,0.5,1/44,2/9,
    0.2312,0.375,math.sqrt(5/8),0.1179,0.332,0.99,0.024,0.01,
    0.0002387,15.972334/100,0.000824,216/C2]

# BLOCK 6: Emergent operational constants (101-140)
b6=[0.998354361,0.041735,92/86,50.2093/100,23.8458/100,4801.247/5000,
    249000/1e6,23/100,0.340397,3467000/1e7,1128/2000,24/100,3/10,
    0.014136,34670000/1e8,102.244/1000,3144000/1e7,1/6,324/1000,
    273/1000,0.998354361,2.222222/10,92/100,0.0]

# BLOCK 7: Emergent mathematical + musical
b7=[531441/524288/2,81/80/2,32805/32768,1.0000088728605,0.001407838,
    1451520/1e6,2/10,24/100,30/100,15.972334/100,30/100,3/10,-6/10,
    0.0,0.0123,0.0002387,math.cos(math.pi*108/180)+1,
    (1+math.sqrt(5))/2/3,math.pi*179/132/10,math.log(2)/10,
    math.log(3)/10,0.992,1.6e-7,6/264]

# BLOCK 8: Trust/agent architecture (v18.0 state, iteration #4)
b8=[TAU,1-TAU,EPS_KL*1e5,PHI_B,MRATIO,V_AI,R_DECAY,DMAX/100,RG/100,
    G18/1000,0.42,0.123,-0.0001,0.99835,0.61,4/100,113/200,18/200,
    538/1000,21/100,101/200,50/100,90/100,15/100]

# BLOCK 9: Codex version/metadata
vnums=[22,0,538,0,8,21,53,40,101,3,47,24,323,108,264,324,int(C1),int(C2),1820,1823,47,59,71,30]
vscales=[30,1,1000,1,10,30,100,100,200,10,100,100,1000,200,1000,1000,200000,200000,2000,2000,100,100,100,100]
b9=[v/s for v,s in zip(vnums,vscales)]

# BLOCK 10: Harmonic completion (6 angles x sin/cos + 12 parity checks)
b10=[]
for a in [PHI_B,math.pi/24,math.pi/30,math.pi/47,math.pi/6,math.pi/3]:
    b10+=[math.sin(a),math.cos(a)]
b10+=[0.0,G18/C2,C1/C2,TAU,EPS_KL*1e5,1-EPS_KL*1e5,
      PHI_B/math.pi,MRATIO/2,V_AI,R_DECAY,DMAX/RG,1.0]

blocks=[b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10]
for i,b in enumerate(blocks):
    if len(b) != 24:
        raise ValueError(f'Block {i} len={len(b)}')

vec=[]
for b in blocks: vec+=b
if len(vec) != 264:
    raise ValueError(f'Vector length={len(vec)}, expected 264')
print(json.dumps([round(v,10) for v in vec]))
