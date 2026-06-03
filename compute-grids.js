const fs=require('fs'),path=require('path');
const dir=path.join(__dirname,'patterns');
const files=['waves.json','blobs.json','spirals.json','drapes.json','flow.json'];
let out=[];
for(const f of files){const arr=JSON.parse(fs.readFileSync(path.join(dir,f),'utf8'));const theme=f.replace('.json','');
 for(const p of arr){let fn;try{fn=eval('('+p.code+')')}catch(e){continue}
  const n=p.n,s=p.steps,g=[];for(let y=0;y<n;y++)for(let x=0;x<n;x++){let v;try{v=fn(x,y,n,s)}catch(e){v=0}v=Math.max(0,Math.min(s,Math.round(v)));g.push(v)}
  out.push({name:p.name,theme,n,steps:s,grid:g});}}
fs.writeFileSync(path.join(__dirname,'grids.json'),JSON.stringify(out));
console.log('computed',out.length,'grids');
