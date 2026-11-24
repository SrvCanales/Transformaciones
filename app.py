import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Transformaciones lineales en R²", page_icon="◫", layout="wide")
st.markdown(
    """<style>
#MainMenu,header,footer{visibility:hidden}
.stApp{background:#12141c}
.block-container{padding:.6rem .8rem 0 .8rem;max-width:1500px}
iframe{border:0;border-radius:14px}
</style>""",
    unsafe_allow_html=True,
)

# Toda la interacción vive en el navegador (canvas + JS): así los parámetros,
# el arrastre y la animación son instantáneos, sin reruns de Streamlit.
HTML = r"""
<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{--bg:#12141c;--deep:#0d0f16;--panel:#181b26;--line:#272b3a;--text:#eeeae2;--muted:#8c92a4;--sol:#e8b94e;--p1:#e0674f;--p2:#3fa796;--p3:#8b7fd6;--p4:#d45a94;--p5:#5aa9e6}
*{box-sizing:border-box}
html,body{margin:0;min-height:100%;height:100%;background:var(--bg);color:var(--text);font:14px/1.5 Inter,system-ui,-apple-system,"Segoe UI",sans-serif}
#app{display:grid;grid-template-columns:390px 1fr;height:100vh}
#panel{overflow:auto;padding:18px 18px 28px;background:var(--deep);border-right:1px solid var(--line)}
#stage{position:relative;min-width:0}
canvas{position:absolute;inset:0;width:100%;height:100%}
h1{font-size:17px;margin:0 0 2px;font-weight:650;letter-spacing:.2px}
h1 span{color:var(--sol)}
.sub{color:var(--muted);font-size:12px;margin-bottom:14px}
h2{font-size:11px;text-transform:uppercase;letter-spacing:1.2px;color:var(--muted);margin:0 0 10px;font-weight:600}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px;margin-bottom:12px}
.cols,.mat{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:0 18px}
.cols{margin-bottom:4px;text-align:center;font-weight:650}
.c1{color:var(--p1)}.c2{color:var(--p2)}
.mat{position:relative;padding:10px 18px}
.mat:before,.mat:after{content:"";position:absolute;top:0;bottom:0;width:10px;border:2px solid var(--muted)}
.mat:before{left:0;border-right:0;border-radius:7px 0 0 7px}
.mat:after{right:0;border-left:0;border-radius:0 7px 7px 0}
.mat input{width:100%;min-width:0;background:var(--bg);color:var(--text);border:1px solid var(--line);border-radius:9px;padding:9px 4px;text-align:center;font:600 18px ui-monospace,SFMono-Regular,Menlo,monospace;outline:0}
.mat input.c1{border-color:var(--p1)}.mat input.c2{border-color:var(--p2)}
.mat input:focus{box-shadow:0 0 0 3px rgba(232,185,78,.25)}
.dets{display:flex;justify-content:space-between;color:var(--muted);font-size:12px;margin-top:6px;padding:0 4px}
.dets b{color:var(--text);font-family:ui-monospace,monospace}
.row{display:flex;gap:8px}
button{font:600 13px inherit;font-family:inherit;border-radius:9px;padding:10px 14px;cursor:pointer;border:1px solid var(--line);background:transparent;color:var(--text)}
button:hover{border-color:var(--muted)}
#go{flex:1;background:var(--sol);border-color:var(--sol);color:#12141c}
#go:hover{filter:brightness(1.08)}
input[type=range]{width:100%;accent-color:var(--sol);margin:12px 0 2px}
.sw{display:flex;align-items:center;gap:10px;padding:5px 0;cursor:pointer;user-select:none}
.sw input{display:none}
.sw i{width:34px;height:20px;border-radius:20px;background:var(--line);position:relative;transition:.2s;flex:none}
.sw i:after{content:"";position:absolute;left:3px;top:3px;width:14px;height:14px;border-radius:50%;background:var(--muted);transition:.2s}
.sw input:checked+i{background:var(--sol)}
.sw input:checked+i:after{left:17px;background:#12141c}
.mut,.mut p{color:var(--muted);font-size:12.5px}
#vr{font:12px ui-monospace,monospace;color:var(--p3);margin-top:6px;display:none}
.lam{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px}
.chip{border:1px solid var(--c);border-radius:10px;padding:8px 10px;background:var(--bg)}
.chip small{display:block;color:var(--c);font-weight:650}
.chip b{font:600 17px ui-monospace,monospace}
.badge{display:inline-block;background:var(--sol);color:#12141c;border-radius:20px;padding:2px 10px;font-weight:650;font-size:12px;margin-bottom:6px}
#interp p{margin:6px 0}
#interp ul{margin:6px 0;padding:0;list-style:none}
#interp li{border-left:3px solid var(--c);padding-left:9px;margin:4px 0;font-size:13px}
.ev{border-left:3px solid var(--c);padding:3px 10px;margin:6px 0}
.ev b{display:block}.ev span{color:var(--muted);font-size:12.5px}
.case{opacity:.42;padding:8px 10px;border-left:2px solid var(--line);margin:4px 0;font-size:12.5px;transition:.2s}
.case b{display:block;font-size:13px}
.case.on{opacity:1;border-color:var(--sol);background:var(--bg);border-radius:0 8px 8px 0}
.zoom{position:absolute;top:12px;right:12px;display:flex;flex-direction:column;gap:6px}
.zoom button{width:34px;height:34px;padding:0;background:rgba(24,27,38,.85)}
#hint{position:absolute;left:14px;bottom:12px;color:var(--muted);font-size:12px;pointer-events:none}
@media(max-width:820px){
 #app{grid-template-columns:1fr;height:auto}
 #stage{order:-1;height:min(92vw,560px)}
 #panel{border-right:0;overflow:visible}
}
</style></head><body>
<div id="app">
<aside id="panel">
 <h1>Transformaciones lineales <span>ℝ²</span></h1>
 <div class="sub">x ↦ Mx · cada columna de M es la imagen de un vector de la base</div>

 <div class="card">
  <div class="cols"><span class="c1">v₁</span><span class="c2">v₂</span></div>
  <div class="mat">
   <input id="a" type="number" step="0.1" class="c1"><input id="b" type="number" step="0.1" class="c2">
   <input id="c" type="number" step="0.1" class="c1"><input id="d" type="number" step="0.1" class="c2">
  </div>
  <div class="dets"><span>det M = <b id="detv"></b></span><span>tr M = <b id="trv"></b></span></div>
 </div>

 <div class="card">
  <div class="row"><button id="go">▶ Transformar</button><button id="rs">↺ Reiniciar</button></div>
  <input id="tt" type="range" min="0" max="1" step="0.001" value="0">
  <div class="mut" style="display:flex;justify-content:space-between"><span>plano original</span><span>plano transformado</span></div>
 </div>

 <div class="card">
  <h2>Mostrar</h2>
  <label class="sw"><input type="checkbox" id="dt"><i></i>Determinante (área orientada)</label>
  <label class="sw"><input type="checkbox" id="es" checked><i></i>Autoespacios</label>
  <label class="sw"><input type="checkbox" id="pv" checked><i></i>Vista previa del destino</label>
  <label class="sw"><input type="checkbox" id="vv"><i></i>Vector v manipulable con el cursor</label>
  <div id="vr"></div>
 </div>

 <div class="card"><h2>Autovalores</h2><div class="lam" id="lam"></div><div id="interp"></div></div>
 <div class="card"><h2>Autoespacio y base</h2><div id="space"></div></div>
 <div class="card"><h2>Todas las combinaciones</h2><div id="cases"></div></div>
</aside>
<main id="stage"><canvas id="cv"></canvas>
 <div class="zoom"><button id="zi">+</button><button id="zo">−</button><button id="zr">⌂</button></div>
 <div id="hint"></div>
</main>
</div>
<script>
const $=id=>document.getElementById(id);
const cv=$('cv'),ctx=cv.getContext('2d');
const C={text:'#eeeae2',muted:'#8c92a4',sol:'#e8b94e',p1:'#e0674f',p2:'#3fa796',p3:'#8b7fd6',p4:'#d45a94',p5:'#5aa9e6'};
const EC=[C.p4,C.p5];
const M={a:2,b:1,c:1,d:2};
let t=0,A=null,scale=64,V={x:1,y:1.5},drag=false,W=0,H=0,dpr=1,dirty=true,E={},EV=[];
const f=x=>{const r=+x.toFixed(3);return (Object.is(r,-0)?0:r).toString()};
const sub=i=>['','₁','₂'][i];
const inv=()=>{dirty=true};
const Mt=()=>({a:1+(M.a-1)*t,b:M.b*t,c:M.c*t,d:1+(M.d-1)*t});
const S=(x,y)=>[W/2+x*scale,H/2-y*scale];

const CASES={
 pp:['λ₁ > 0 , λ₂ > 0','Ambas direcciones propias conservan su sentido y solo se escalan: se estiran si |λ|>1, se comprimen si |λ|<1. La orientación se preserva (det > 0).'],
 nn:['λ₁ < 0 , λ₂ < 0','Ambas direcciones propias invierten su sentido y se escalan por |λ|: equivale a una simetría central (giro de 180°) combinada con dilataciones. det > 0, la orientación se conserva.'],
 pn:['λ₁ > 0 , λ₂ < 0','Se conserva el sentido en la recta del autovalor positivo y se invierte en la del negativo: es una reflexión respecto de la primera recta, con escalas. det < 0, el plano se "voltea".'],
 p0:['λ₁ > 0 , λ₂ = 0','El plano se aplasta sobre la recta propia de λ>0; el autoespacio de λ=0 (el núcleo) se colapsa al origen. det = 0.'],
 n0:['λ₁ = 0 , λ₂ < 0','El plano se aplasta sobre la recta propia de λ<0, invirtiendo su sentido; el núcleo se colapsa al origen. det = 0.'],
 z0:['λ₁ = λ₂ = 0','Colapso total: el plano se aplasta sobre una recta (transformación nilpotente) o sobre el origen si M = 0. det = 0.'],
 cx:['λ = α ± βi (complejos conjugados)','Ninguna recta real se conserva. La transformación es una rotación de ángulo θ = atan2(β, α) combinada con un escalamiento r = |λ| = √det: espiral hacia afuera si r>1, hacia adentro si r<1 y rotación pura si r=1.']
};

function eig(){
 const {a,b,c,d}=M,T=a+d,D=a*d-b*c,disc=T*T-4*D,e=1e-9;
 const ev=l=>Math.abs(b)>e?[b,l-a]:Math.abs(c)>e?[l-d,c]:(Math.abs(l-a)<e?[1,0]:[0,1]);
 E={T,D,cx:disc<-e};EV=[];
 if(E.cx){E.re=T/2;E.im=Math.sqrt(-disc)/2;return}
 const s=Math.sqrt(Math.max(disc,0));
 E.l=[(T+s)/2,(T-s)/2];
 E.scalar=Math.abs(b)<e&&Math.abs(c)<e&&Math.abs(a-d)<e;
 E.rep=s<e&&!E.scalar;
 if(E.scalar)EV=[{w:[1,0],l:E.l[0],i:1,plane:1},{w:[0,1],l:E.l[0],i:2,plane:1}];
 else if(E.rep)EV=[{w:ev(E.l[0]),l:E.l[0],i:1}];
 else EV=E.l.map((l,i)=>({w:ev(l),l,i:i+1}));
 EV.forEach(o=>{const n=Math.hypot(o.w[0],o.w[1])||1;o.u=[o.w[0]/n,o.w[1]/n]});
}
const mag=l=>{const m=Math.abs(l);return m<1e-9?'colapsa al origen':(m>1+1e-9?'expande ×'+f(m):m<1-1e-9?'comprime ×'+f(m):'conserva la longitud')+(l<-1e-9?' e invierte el sentido':'')};
const chip=(c,l,v)=>`<div class="chip" style="--c:${c}"><small>${l}</small><b>${v}</b></div>`;

function update(){
 eig();
 $('detv').textContent=f(E.D);$('trv').textContent=f(E.T);
 let key,lam,extra;
 if(E.cx){
  key='cx';const th=Math.atan2(E.im,E.re)*180/Math.PI,r=Math.sqrt(E.D);
  lam=chip(C.p4,'λ₁',f(E.re)+' + '+f(E.im)+'i')+chip(C.p5,'λ₂',f(E.re)+' − '+f(E.im)+'i');
  extra=`<p>Aquí α = ${f(E.re)}, β = ${f(E.im)} → θ = ${f(th)}°, r = ${f(r)} (${r>1+1e-9?'espiral hacia afuera':r<1-1e-9?'espiral hacia adentro':'rotación pura'}).</p>`;
 }else{
  const s=E.l.map(v=>Math.abs(v)<1e-9?0:Math.sign(v));
  key={'1,1':'pp','-1,-1':'nn','1,-1':'pn','1,0':'p0','0,-1':'n0','0,0':'z0'}[s.join()];
  lam=chip(C.p4,'λ₁',f(E.l[0]))+chip(C.p5,'λ₂',f(E.l[1]));
  extra='<ul>'+E.l.map((l,i)=>`<li style="--c:${EC[i]}">λ${sub(i+1)} = ${f(l)}: ${mag(l)}</li>`).join('')+'</ul>';
 }
 $('lam').innerHTML=lam;
 $('interp').innerHTML=`<span class="badge">${CASES[key][0]}</span><p>${CASES[key][1]}</p>${extra}`;
 $('cases').innerHTML=Object.keys(CASES).map(k=>`<div class="case ${k==key?'on':''}"><b>${CASES[k][0]}</b>${CASES[k][1]}</div>`).join('');
 let h;
 if(E.cx)h='<p class="mut">Sin autoespacio real: ninguna recta por el origen queda invariante (los autovectores son complejos).</p>';
 else if(E.scalar)h=`<div class="ev" style="--c:${EC[0]}"><b>E(λ) = ℝ²</b><span>base: {(1, 0), (0, 1)} · M = λI, todo vector es autovector</span></div>`;
 else{
  h=EV.map(o=>`<div class="ev" style="--c:${EC[o.i-1]}"><b>E(λ${sub(o.i)}) = span{u${sub(o.i)}}</b><span>base: {(${f(o.w[0])}, ${f(o.w[1])})} ≈ (${f(o.u[0])}, ${f(o.u[1])}) unitario${Math.abs(o.l)<1e-9?' · es el núcleo':''}</span></div>`).join('');
  if(E.rep)h+='<p class="mut">λ repetido con un solo autovector: dim E = 1 &lt; 2 (no diagonalizable, tipo cizalla).</p>';
 }
 $('space').innerHTML=h;
}

function ln(a,b,col,w,al,dash){ctx.save();ctx.globalAlpha=al;ctx.strokeStyle=col;ctx.lineWidth=w;ctx.setLineDash(dash||[]);ctx.beginPath();ctx.moveTo(a[0],a[1]);ctx.lineTo(b[0],b[1]);ctx.stroke();ctx.restore()}
function arrow(x,y,col,w,al,dash,label){
 const o=S(0,0),p=S(x,y),dx=p[0]-o[0],dy=p[1]-o[1],L=Math.hypot(dx,dy);
 ctx.save();ctx.globalAlpha=al;ctx.strokeStyle=col;ctx.fillStyle=col;ctx.lineWidth=w;ctx.setLineDash(dash||[]);
 if(L>1){
  const h=Math.min(12,L*.5),ux=dx/L,uy=dy/L;
  ctx.beginPath();ctx.moveTo(o[0],o[1]);ctx.lineTo(p[0]-ux*h*.7,p[1]-uy*h*.7);ctx.stroke();
  ctx.setLineDash([]);ctx.beginPath();ctx.moveTo(p[0],p[1]);
  ctx.lineTo(p[0]-ux*h-uy*h*.45,p[1]-uy*h+ux*h*.45);ctx.lineTo(p[0]-ux*h+uy*h*.45,p[1]-uy*h-ux*h*.45);ctx.fill();
 }
 if(label){ctx.font='600 14px system-ui,sans-serif';ctx.fillText(label,p[0]+9,p[1]-9)}
 ctx.restore();
}
function quad(m,fill,al,dash,lab){
 const p=[S(0,0),S(m.a,m.c),S(m.a+m.b,m.c+m.d),S(m.b,m.d)];
 ctx.save();ctx.beginPath();p.forEach((q,i)=>i?ctx.lineTo(q[0],q[1]):ctx.moveTo(q[0],q[1]));ctx.closePath();
 if(fill){ctx.globalAlpha=.16;ctx.fillStyle=C.sol;ctx.fill()}
 ctx.globalAlpha=al;ctx.strokeStyle=C.sol;ctx.lineWidth=1.6;ctx.setLineDash(dash||[]);ctx.stroke();
 if(lab){ctx.globalAlpha=1;ctx.fillStyle=C.text;ctx.font='600 13px system-ui,sans-serif';ctx.textAlign='center';ctx.fillText(lab,(p[0][0]+p[2][0])/2,(p[0][1]+p[2][1])/2+4)}
 ctx.restore();
}

let lastHint='';
function draw(){
 dirty=false;ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,W,H);
 const m=Mt(),det=m.a*m.d-m.b*m.c,fr=m.a*m.a+m.b*m.b+m.c*m.c+m.d*m.d;
 const smin=Math.sqrt(Math.max(0,(fr-Math.sqrt(Math.max(0,fr*fr-4*det*det)))/2));
 const R=Math.hypot(W,H)/scale/2,N=Math.min(60,Math.ceil(R/Math.max(smin,.05))),L=R*1.3/Math.max(smin,.02);
 const T=(x,y)=>S(m.a*x+m.b*y,m.c*x+m.d*y);
 if(t>.001){const r=Math.ceil(R);for(let k=-r;k<=r;k++){ln(S(k,-R),S(k,R),C.muted,1,.09);ln(S(-R,k),S(R,k),C.muted,1,.09)}}
 for(let k=-N;k<=N;k++){if(!k)continue;ln(T(k,-L),T(k,L),C.muted,1,.26);ln(T(-L,k),T(L,k),C.muted,1,.26)}
 ln(T(-L,0),T(L,0),C.p1,1.6,.55);ln(T(0,-L),T(0,L),C.p2,1.6,.55);
 const pv=$('pv').checked&&t<.999;
 if($('dt').checked){if(pv)quad(M,0,.5,[5,5]);quad(m,1,.95,0,'det = '+f(det))}
 if(pv){arrow(M.a,M.c,C.p1,1.6,.5,[5,5]);arrow(M.b,M.d,C.p2,1.6,.5,[5,5])}
 if($('es').checked)EV.forEach(o=>{
  const col=EC[o.i-1];
  if(!o.plane)ln(S(-o.u[0]*R*3,-o.u[1]*R*3),S(o.u[0]*R*3,o.u[1]*R*3),col,1.6,.85,[7,6]);
  const k=1-t+t*o.l;arrow(o.u[0]*k,o.u[1]*k,col,3,1,0,'u'+sub(o.i));
 });
 arrow(m.a,m.c,C.p1,3.2,1,0,'v₁');arrow(m.b,m.d,C.p2,3.2,1,0,'v₂');
 let hint='';
 if($('vv').checked){
  const q=[m.a*V.x+m.b*V.y,m.c*V.x+m.d*V.y];
  if(t>.001){const o=S(V.x,V.y);ctx.save();ctx.strokeStyle=C.p3;ctx.globalAlpha=.5;ctx.beginPath();ctx.arc(o[0],o[1],5,0,7);ctx.stroke();ctx.restore()}
  arrow(q[0],q[1],C.p3,3.2,1,0,'v');
  const p=S(q[0],q[1]);ctx.save();ctx.fillStyle=C.p3;ctx.strokeStyle=C.text;ctx.lineWidth=2;ctx.beginPath();ctx.arc(p[0],p[1],7,0,7);ctx.fill();ctx.stroke();ctx.restore();
  $('vr').textContent=`v = (${f(V.x)}, ${f(V.y)})  ↦  Mₜv = (${f(q[0])}, ${f(q[1])})`;
  hint=Math.abs(det)<1e-6?'Con det(Mₜ) = 0 no se puede arrastrar: pulsa Reiniciar.':'Haz clic o arrastra sobre el plano para mover v';
 }
 if(hint!==lastHint){$('hint').textContent=hint;lastHint=hint}
}

const ease=p=>p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2;
function play(to){A={from:t,to,t0:performance.now(),dur:1800*Math.abs(to-t)+1}}
function loop(now){
 if(A){const p=Math.max(0,Math.min(1,(now-A.t0)/A.dur));t=A.from+(A.to-A.from)*ease(p);$('tt').value=t;dirty=true;if(p>=1)A=null}
 if(dirty)draw();
 requestAnimationFrame(loop);
}

['a','b','c','d'].forEach(k=>{
 const el=$(k);el.value=M[k];
 el.addEventListener('input',()=>{const v=parseFloat(el.value);M[k]=isFinite(v)?v:0;update();inv()});
});
$('go').onclick=()=>play(1);
$('rs').onclick=()=>play(0);
$('tt').addEventListener('input',e=>{A=null;t=+e.target.value;inv()});
['dt','es','pv'].forEach(i=>$(i).addEventListener('change',inv));
$('vv').addEventListener('change',()=>{
 const on=$('vv').checked;$('vr').style.display=on?'block':'none';
 cv.style.cursor=on?'crosshair':'default';cv.style.touchAction=on?'none':'auto';inv();
});
const zoom=k=>{scale=Math.min(220,Math.max(18,scale*k));inv()};
$('zi').onclick=()=>zoom(1.25);$('zo').onclick=()=>zoom(.8);$('zr').onclick=()=>{scale=64;inv()};
cv.addEventListener('wheel',e=>{e.preventDefault();zoom(Math.exp(-e.deltaY*.0015))},{passive:false});

function setV(e){
 const r=cv.getBoundingClientRect(),m=Mt(),det=m.a*m.d-m.b*m.c;
 if(Math.abs(det)<1e-6)return;
 const X=(e.clientX-r.left-W/2)/scale,Y=-(e.clientY-r.top-H/2)/scale;
 V.x=(m.d*X-m.b*Y)/det;V.y=(-m.c*X+m.a*Y)/det;inv();
}
cv.addEventListener('pointerdown',e=>{if(!$('vv').checked)return;drag=true;cv.setPointerCapture(e.pointerId);setV(e)});
cv.addEventListener('pointermove',e=>{if(drag)setV(e)});
['pointerup','pointercancel'].forEach(n=>cv.addEventListener(n,()=>{drag=false}));

new ResizeObserver(()=>{
 const r=cv.getBoundingClientRect();W=r.width;H=r.height;dpr=window.devicePixelRatio||1;
 cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr);inv();
}).observe(cv);

update();requestAnimationFrame(loop);
</script></body></html>
"""

components.html(HTML, height=900, scrolling=True)
