from PIL import Image
from pathlib import Path
root=Path('dist/assets/sculptures');paths=list(root.glob('digit-*.png'));images=[Image.open(p) for p in paths];boxes=[im.getchannel('A').getbbox() for im in images];top=min(b[1] for b in boxes)-5;bottom=max(b[3] for b in boxes)+5
for p,im,b in zip(paths,images,boxes):im.crop((max(0,b[0]-5),max(0,top),min(im.width,b[2]+5),min(im.height,bottom))).save(p,optimize=True)
print('Trimmed render margins for',len(paths),'numerals')
