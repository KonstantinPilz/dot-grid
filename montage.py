import json, math
from PIL import Image, ImageDraw, ImageFont
data=json.load(open('grids.json'))
CELL=160          # native px per pattern tile
COLS=4
PAD=6
LBL=16
BG=(231,227,216); DOT=(92,83,71)
try: font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",11)
except: font=ImageFont.load_default()

def draw_pattern(d, size):
    n=d['n']; s=d['steps']; g=d['grid']
    img=Image.new('RGB',(size,size),BG); dr=ImageDraw.Draw(img)
    base=0.18
    cell=size/n
    for y in range(n):
        for x in range(n):
            lv=g[y*n+x]
            frac=base+(lv/s)*(1-base)
            r=frac*cell/2
            cx=(x+0.5)*cell; cy=(y+0.5)*cell
            dr.ellipse([cx-r,cy-r,cx+r,cy+r],fill=DOT)
    return img

# paginate: per_page tiles
PER_PAGE=24  # 4 cols x 6 rows
pages=math.ceil(len(data)/PER_PAGE)
for pg in range(pages):
    chunk=data[pg*PER_PAGE:(pg+1)*PER_PAGE]
    rows=math.ceil(len(chunk)/COLS)
    W=COLS*CELL+(COLS+1)*PAD
    H=rows*(CELL+LBL+PAD)+PAD
    page=Image.new('RGB',(W,H),(40,40,40)); pd=ImageDraw.Draw(page)
    for i,d in enumerate(chunk):
        idx=pg*PER_PAGE+i
        c=i%COLS; r=i//COLS
        x=PAD+c*(CELL+PAD); y=PAD+r*(CELL+LBL+PAD)
        page.paste(draw_pattern(d,CELL),(x,y))
        pd.text((x+2,y+CELL+2),f"{idx} {d['name']} [{d['theme'][:4]}]",fill=(230,230,230),font=font)
    page.save(f'/tmp/m{pg}.png')
    print(f'/tmp/m{pg}.png',page.size,'patterns',pg*PER_PAGE,'-',pg*PER_PAGE+len(chunk)-1)
