import numpy as np, wave
sr=44100; D=34.0; N=int(sr*D); rng=np.random.default_rng(11)
bpm=138; beat=60/bpm; e8=beat/2; bar=beat*4
L=np.zeros(N);R=np.zeros(N)
mid=lambda n:440*2**((n-69)/12)
def note(m,at,dur,vel,pan=.5,honk=8):
    f=mid(m); n=int(min(2.6,dur+1.2)*sr); x=np.arange(n)/sr
    dec=1.6+f/110
    s=np.zeros(n)
    for c in (-honk,0,honk):                       # 3 slightly detuned strings = honky-tonk
        ff=f*2**(c/1200)
        for h in range(1,9):
            s+=np.sin(2*np.pi*ff*h*(1+.0004*h*h)*x)*(h**-1.15)*np.exp(-x*dec*(1+.35*h))
    s*=np.minimum(1,x/.002)
    rel=np.where(x>dur,np.exp(-(x-dur)*22),1.0); s*=rel
    k=int(.006*sr); s[:k]+=rng.standard_normal(k)*np.linspace(1,0,k)*.25   # hammer click
    i=int(max(0,at)*sr); j=min(N,i+n)
    if j<=i:return
    s=s[:j-i]*vel*.22
    L[i:j]+=s*(1-pan)*2;R[i:j]+=s*pan*2
chords={'C':(48,43,[55,60,64]),'G7':(43,50,[53,59,62]),'C7':(48,43,[55,58,64]),'F':(41,48,[57,60,65]),
        'Fm':(41,48,[56,60,65]),'A7':(45,52,[55,61,64]),'D7':(38,45,[54,60,64])}
prog=['C','C','G7','C','C7','F','Fm','C','A7','D7','G7','C','C','G7','C','C7','F','Fm','C','A7','D7','G7']
mel=[ [(0,79,1),(1,76,2),(3,72,1),(4,76,1),(5,79,2),(7,76,1)],
      [(0,84,3),(3,79,1),(4,76,2),(6,72,2)],
      [(0,74,1),(1,77,2),(3,74,1),(4,71,1),(5,74,2),(7,77,1)],
      [(0,79,3),(3,76,1),(4,72,4)],
      [(0,76,1),(1,79,2),(3,82,1),(4,79,1),(5,76,2),(7,72,1)],
      [(0,81,3),(3,77,1),(4,81,2),(6,84,2)],
      [(0,80,1),(1,77,2),(3,72,1),(4,77,1),(5,80,2),(7,77,1)],
      [(0,79,2),(2,76,2),(4,72,2),(6,67,2)],
      [(0,76,1),(1,81,2),(3,85,1),(4,81,1),(5,76,2),(7,73,1)],
      [(0,78,1),(1,81,2),(3,84,1),(4,81,1),(5,78,2),(7,74,1)],
      [(0,79,2),(2,77,2),(4,74,2),(6,71,2)],
      [(0,79,1),(1,76,2),(3,72,1),(4,76,1),(5,79,2),(7,84,1)],
      [(0,84,3),(3,79,1),(4,76,2),(6,72,2)],
      [(0,74,1),(1,77,2),(3,74,1),(4,71,1),(5,74,2),(7,77,1)] ]
mel=mel+[mel[i] for i in range(3,11)]
for b,name in enumerate(prog):
    t0=b*bar; root,fifth,ch=chords[name]
    for beat_i in range(4):
        at=t0+beat_i*beat+rng.normal(0,.004)
        if beat_i in (0,2):
            note(root if beat_i==0 else fifth,at,beat*.8,.62*rng.uniform(.9,1.05),.42,honk=5)
        else:
            for m in ch: note(m,at,beat*.55,.34*rng.uniform(.9,1.05),.5,honk=6)
    for (i8,m,d) in mel[b]:
        at=t0+i8*e8+rng.normal(0,.006)
        accent=1.12 if i8 in (1,3,5) else 1.0
        note(m,at,max(.1,d*e8*.9),.62*accent*rng.uniform(.92,1.05),.58,honk=9)
# small room reverb + old-film band limit
ir_n=int(.5*sr);ir=rng.standard_normal((2,ir_n))*np.exp(-np.arange(ir_n)/sr*9)
def rev(x,i):
    n=len(x)+len(i);return np.fft.irfft(np.fft.rfft(x,n)*np.fft.rfft(i,n),n)[:N]
L2=L+rev(L,ir[0])*.01;R2=R+rev(R,ir[1])*.01
y=np.stack([L2,R2],1)
F=np.fft.rfftfreq(N,1/sr);mask=((F>140)&(F<6500)).astype(float);mask=np.convolve(mask,np.ones(60)/60,'same')
y=np.stack([np.fft.irfft(np.fft.rfft(y[:,c])*mask,N) for c in (0,1)],1)
y*=(10**(-18.5/20))/np.sqrt((y**2).mean()); pk=np.abs(y).max()
if pk>.5:y*=.5/pk
t=np.arange(N)/sr;y*=np.minimum(1,t/.05)[:,None]
w=wave.open('./rag_b1.wav','wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr)
w.writeframes((y*32767).astype('<i2').tobytes());w.close();print('peak',np.abs(y).max(),'bars',len(prog),'secs',len(prog)*bar)
