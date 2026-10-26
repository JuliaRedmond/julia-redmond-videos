"""Worst-case navy-on-background contrast for stills made with: node render.js <script> <out.mp4> --stills=... --notext
Usage: python3 contrast.py <png> [<png> ...]   (needs >= 4.5:1 inside the text area, y 420-1570, x 60-1020)"""
import sys
from PIL import Image
import numpy as np
def L(a):
    a=a/255.;a=np.where(a<=.03928,a/12.92,((a+.055)/1.055)**2.4);return .2126*a[...,0]+.7152*a[...,1]+.0722*a[...,2]
nl=float(L(np.array([0x1D,0x2D,0x42],float)))
worst=99
for f in sys.argv[1:]:
    a=np.array(Image.open(f).convert('RGB'),float)[420:1570,60:1020]
    worst=min(worst,(float(L(a).min())+.05)/(nl+.05))
print('worst-case navy-on-background contrast',round(worst,2),'PASS' if worst>=4.5 else 'FAIL')
sys.exit(0 if worst>=4.5 else 1)
