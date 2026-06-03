const fs=require('fs'),path=require('path');
const dir=path.join(__dirname,'patterns');
const files=['waves.json','blobs.json','spirals.json','drapes.json','flow.json'];
let all=[];
for(const f of files){const arr=JSON.parse(fs.readFileSync(path.join(dir,f),'utf8'));for(const p of arr)all.push(p);}
// selected global indices (curated for flowy + variety)
const sel=[0,21,8,15,20, 23,26,30,36,40, 47,54,58, 66,71,73,76,82, 89,93];
const picked=sel.map(i=>{const p=all[i];return {name:p.name,n:p.n,steps:p.steps,code:p.code};});
// sanity: eval each + spread check
for(const p of picked){const fn=eval('('+p.code+')');let set=new Set();for(let y=0;y<p.n;y++)for(let x=0;x<p.n;x++){let v=Math.max(0,Math.min(p.steps,Math.round(fn(x,y,p.n,p.steps))));set.add(v);}if(set.size<3)console.log('LOW SPREAD',p.name,set.size);}
fs.writeFileSync(path.join(__dirname,'selected.json'),JSON.stringify(picked,null,0));
console.log('Selected',picked.length,'patterns:');
console.log(picked.map((p,i)=>`${i+1}. ${p.name} (n${p.n})`).join('\n'));
