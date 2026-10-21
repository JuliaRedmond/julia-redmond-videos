import sys,glob
from PIL import Image
import numpy as np
def L(a):
    a=a/255.;a=np.where(a<=.03928,a/12.92,((a+.055)/1.055)**2.4);return .2126*a[...,0]+.7152*a[...,1]+.0722*a[...,2]
nl=float(L(np.array([0x1D,0x2D,0x42],float)))
pre=sys.argv[1];top=490 if sys.argv[2]=='multi' else 420
w=min((float(L(np.array(Image.open(f).convert('RGB'),float)[top:1570,60:1020]).min())+.05)/(nl+.05) for f in glob.glob(pre+'_bg_*.png'))
print('worst-case navy-on-background contrast',round(w,2),'PASS' if w>=4.5 else 'FAIL')
