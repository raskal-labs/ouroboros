from pathlib import Path
import re

path = Path('js/app.js')
s = path.read_text()


def exact(old, new, label):
    global s
    if old not in s:
        raise SystemExit(f'missing exact target: {label}')
    s = s.replace(old, new, 1)


def sub(pattern, repl, label):
    global s
    s, n = re.subn(pattern, lambda m: repl, s, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f'expected one regex target for {label}, got {n}')


exact(
    'const display={outline:true,outlineThickness:.08,referenceCircle:false,mouthTailGuide:false,closurePreview:false,gazeArrow:true,gazeOpacity:.95};',
    'const display={outline:true,outlineThickness:.08,referenceCircle:false,mouthTailGuide:false,closurePreview:false,gazeArrow:true,gazeOpacity:.95,gazeStars:true};',
    'display defaults')
exact(
    'const earth={x:0,y:0,r:2.15,depth:6.5,scale:1,alpha:1,locked:true};',
    'const earth={x:0,y:0,r:2.50,depth:6.5,scale:1,alpha:1,locked:true};',
    'earth default')
exact(
    'const defaultBiteOffset={x:closedPose[0].x-closedPose[closedPose.length-1].x,y:closedPose[0].y-closedPose[closedPose.length-1].y};\n',
    '',
    'old bite offset')
exact(
    'let biteTail=true,preserveLength=false,preserveTarget=null;',
    'let biteTail=true,preserveLength=false,preserveTarget=null;\nlet sparkleFrame=0,sparkleTimer=0;',
    'sparkle state')
exact(
    'function mutate(fn){const before=sceneState();fn();commit(before);syncAllUI();draw();}',
    'function mutate(fn){const before=sceneState();fn();commit(before);syncAllUI();draw();syncSparkleAnimation();}',
    'mutate animation sync')
exact(
    'function applyScene(s){pts=clone(s.pts||pts);selected=Number.isInteger(s.selected)?clamp(s.selected,-1,pts.length-1):-1;snakeScale=+(s.snakeScale??1);perspectiveStrength=+(s.perspectiveStrength??1);Object.assign(endpoint,s.endpoint||{});Object.assign(earth,s.earth||{});Object.assign(moon,s.moon||{});Object.assign(lighting,s.lighting||{});crossingOverrides=clone(s.crossingOverrides||{});Object.assign(display,s.display||{});if(s.constraints){biteTail=s.constraints.biteTail??biteTail;preserveLength=s.constraints.preserveLength??preserveLength;preserveTarget=Number.isFinite(+s.constraints.preserveTarget)?+s.constraints.preserveTarget:null;}if(preserveLength&&!Number.isFinite(preserveTarget))preserveTarget=arcLength();if(s.flags){showPoints=s.flags.showPoints??showPoints;showLabels=s.flags.showLabels??showLabels;showArrows=s.flags.showArrows??showArrows;showXray=s.flags.showXray??showXray;showNumbers=s.flags.showNumbers??showNumbers;showTransitions=s.flags.showTransitions??showTransitions;showContacts=s.flags.showContacts??showContacts;diagnosticMode=s.flags.diagnosticMode??diagnosticMode;cleanMode=s.flags.cleanMode??cleanMode;}syncAllUI();draw();autosave();}',
    'function applyScene(s){pts=clone(s.pts||pts);selected=Number.isInteger(s.selected)?clamp(s.selected,-1,pts.length-1):-1;snakeScale=+(s.snakeScale??1);perspectiveStrength=+(s.perspectiveStrength??1);Object.assign(endpoint,s.endpoint||{});Object.assign(earth,s.earth||{});Object.assign(moon,s.moon||{});Object.assign(lighting,s.lighting||{});crossingOverrides=clone(s.crossingOverrides||{});Object.assign(display,s.display||{});if(s.constraints){biteTail=s.constraints.biteTail??biteTail;preserveLength=s.constraints.preserveLength??preserveLength;preserveTarget=Number.isFinite(+s.constraints.preserveTarget)?+s.constraints.preserveTarget:null;}if(preserveLength&&!Number.isFinite(preserveTarget))preserveTarget=arcLength();if(s.flags){showPoints=s.flags.showPoints??showPoints;showLabels=s.flags.showLabels??showLabels;showArrows=s.flags.showArrows??showArrows;showXray=s.flags.showXray??showXray;showNumbers=s.flags.showNumbers??showNumbers;showTransitions=s.flags.showTransitions??showTransitions;showContacts=s.flags.showContacts??showContacts;diagnosticMode=s.flags.diagnosticMode??diagnosticMode;cleanMode=s.flags.cleanMode??cleanMode;}syncAllUI();draw();autosave();syncSparkleAnimation();}',
    'applyScene animation sync')

bite_block = r'''function bodyThicknessWorld(p,index,total){const scale=Math.max(currentScale(),1e-6);return bodyThickness(p.z,index,total,p.width,p.source??0)/scale;}
function headMouthWorld(samples=null){samples=samples||sampleCurve();if(samples.length<2)return{x:pts[0]?.x||0,y:pts[0]?.y||0};const p=samples[0],next=samples[1],sx=p.x,sy=-p.y,nx=next.x,ny=-next.y,angle=Math.atan2(sy-ny,sx-nx)+rad(endpoint.headRotation),radius=bodyThicknessWorld(p,0,samples.length)*endpoint.headSize,lx=radius*.98,ly=radius*.17,c=Math.cos(angle),sn=Math.sin(angle),mx=sx+lx*c-ly*sn,my=sy+lx*sn+ly*c;return{x:mx,y:-my};}
function tailTipWorld(samples=null){samples=samples||sampleCurve();const n=samples.length;if(n<2)return{x:pts[pts.length-1]?.x||0,y:pts[pts.length-1]?.y||0};const p=samples[n-1],q=samples[n-2],sx=p.x,sy=-p.y,qx=q.x,qy=-q.y,angle=Math.atan2(sy-qy,sx-qx)+rad(endpoint.tailDirection),ux=Math.cos(angle),uy=Math.sin(angle),nx=-uy,ny=ux,width=bodyThicknessWorld(p,n-1,n)*endpoint.tailWidth,length=width*1.7*endpoint.tailLength,curve=endpoint.tailCurvature*width,tx=sx+ux*length+nx*curve,ty=sy+uy*length+ny*curve;return{x:tx,y:-ty};}
function biteAnchorsWorld(){const samples=sampleCurve();return{mouth:headMouthWorld(samples),tip:tailTipWorld(samples)};}
function translateEndpointSide(index,dx,dy){if(!Number.isFinite(dx)||!Number.isFinite(dy)||pts.length<3)return;const last=pts.length-1,dir=index===0?1:-1,weights=[1,.62,.24];for(let k=0;k<weights.length;k++){const j=index+dir*k;if(j<0||j>last)break;pts[j].x+=dx*weights[k];pts[j].y+=dy*weights[k];}}
function enforceBiteVisual(authoritativeIndex=null){if(!biteTail||pts.length<3)return;const last=pts.length-1,target=authoritativeIndex===0?last:0;for(let iter=0;iter<6;iter++){const{mouth,tip}=biteAnchorsWorld(),dx=target===last?mouth.x-tip.x:tip.x-mouth.x,dy=target===last?mouth.y-tip.y:tip.y-mouth.y,d=Math.hypot(dx,dy);if(!Number.isFinite(d)||d<.004)return;const maxStep=Math.max(.18,.55*snakeScale),k=Math.min(1,maxStep/d);translateEndpointSide(target,dx*k,dy*k);}}
function preserveEndpointCorrection(index,dx,dy){if(!preserveLength||!Number.isFinite(preserveTarget)||pts.length<4)return;const last=pts.length-1;if(index!==0&&index!==last)return;const dir=index===0?1:-1;const weights=[.68,.42,.22,.10];for(let k=1;k<=weights.length;k++){const j=index+dir*k;if(j<=0||j>=last)break;pts[j].x+=dx*weights[k-1];pts[j].y+=dy*weights[k-1];}
for(let iter=0;iter<8;iter++){const current=arcLength(),error=current-preserveTarget;if(!Number.isFinite(current)||!Number.isFinite(error))return;if(Math.abs(error)<.002)return;const j=index+dir,k=j+dir;if(j<=0||j>=last||k<0||k>last)return;const vx=pts[j].x-pts[index].x,vy=pts[j].y-pts[index].y,L=Math.hypot(vx,vy);if(!Number.isFinite(L)||L<1e-6)return;const ux=vx/L,uy=vy/L,maxStep=Math.max(.002,L*.25),step=clamp(error*.42,-maxStep,maxStep);const before=arcLength();const ox=pts[j].x,oy=pts[j].y,okx=pts[k].x,oky=pts[k].y;pts[j].x-=ux*step;pts[j].y-=uy*step;if(k!==last&&k!==0){pts[k].x-=ux*step*.32;pts[k].y-=uy*step*.32;}const after=arcLength();if(!Number.isFinite(after)||Math.abs(after-preserveTarget)>Math.abs(before-preserveTarget)+1e-6){pts[j].x=ox;pts[j].y=oy;pts[k].x=okx;pts[k].y=oky;return;}}
}
function movePoint(index,dx,dy){if(index<0||index>=pts.length||!Number.isFinite(dx)||!Number.isFinite(dy))return;pts[index].x+=dx;pts[index].y+=dy;const endpointDrag=index===0||index===pts.length-1;if(endpointDrag){preserveEndpointCorrection(index,dx,dy);if(biteTail){enforceBiteVisual(index);if(preserveLength){preserveEndpointCorrection(index,0,0);enforceBiteVisual(index);}}}else if(preserveLength){preserveTarget=arcLength();}}
function setSelectedCoordinate(axis,value){if(selected<0||!Number.isFinite(value))return;const p=pts[selected],delta=value-p[axis];if(axis==="x")movePoint(selected,delta,0);else movePoint(selected,0,delta);}
function setSelectedScalar(key,value){if(selected<0||!Number.isFinite(value))return;pts[selected][key]=value;if(biteTail&&(selected===0||selected===pts.length-1))enforceBiteVisual(selected);}
const headBiteKeys=new Set(["headSize","headRotation","neckWidth","mouthOpen"]),tailBiteKeys=new Set(["tailLength","tailWidth","tailDirection","tailCurvature"]);
function setEndpointValue(key,value){endpoint[key]=value;if(!biteTail)return;if(headBiteKeys.has(key))enforceBiteVisual(0);else if(tailBiteKeys.has(key))enforceBiteVisual(pts.length-1);}
function setBiteState(next){next=!!next;if(next===biteTail)return;const before=sceneState();biteTail=next;if(biteTail)enforceBiteVisual(null);if(preserveLength)preserveTarget=arcLength();commit(before);syncAllUI();draw();syncSparkleAnimation();}
function setPreserveLength(next){next=!!next;if(next===preserveLength)return;const before=sceneState();preserveLength=next;preserveTarget=next?arcLength():null;commit(before);syncAllUI();draw();}

function bodyThickness'''
sub(r'function biteOffset\(\).*?\n\nfunction bodyThickness', bite_block, 'bite solver')

render_front = r'''const PS1_GOLD=[[86,53,12],[124,79,18],[169,114,27],[214,158,43],[247,210,99]];
const PS1_OCEAN=[[19,39,70],[28,57,91],[38,76,112],[57,101,139],[83,130,164]];
const PS1_LAND=[[70,91,47],[91,113,58],[116,137,68],[143,159,83]];
const artSnap=v=>Math.round(v);
function rgb(c,a=1){return`rgba(${c[0]},${c[1]},${c[2]},${a})`;}
function ps1Poly(points,fill,stroke=null,lineWidth=1){if(!points.length)return;ctx.beginPath();ctx.moveTo(points[0].x,points[0].y);for(let i=1;i<points.length;i++)ctx.lineTo(points[i].x,points[i].y);ctx.closePath();ctx.fillStyle=fill;ctx.fill();if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=lineWidth;ctx.setLineDash([]);ctx.stroke();}}
let ditherPatternCache=null;
function ditherPattern(){if(ditherPatternCache)return ditherPatternCache;const c=document.createElement("canvas"),g=c.getContext("2d");c.width=c.height=4;g.clearRect(0,0,4,4);g.fillStyle="#fff";g.fillRect(0,0,1,1);g.fillRect(2,2,1,1);ditherPatternCache=ctx.createPattern(c,"repeat");return ditherPatternCache;}
function regularPoly(x,y,r,n,offset=0){const out=[];for(let i=0;i<n;i++){const a=offset+i*Math.PI*2/n;out.push({x:artSnap(x+Math.cos(a)*r),y:artSnap(y+Math.sin(a)*r)});}return out;}
function drawStars(){ctx.fillStyle="rgba(226,232,244,.48)";for(let i=0;i<105;i++){const x=artSnap((i*149.31)%W),y=artSnap((i*91.73)%H),r=i%14===0?2:1;ctx.fillRect(x,y,r,r);}}
function lightDot(nx,ny){const a=rad(lighting.direction),lx=Math.cos(a),ly=Math.sin(a);return clamp((nx*lx+ny*ly)*.5+.5,0,1);}
function moonState(){const a=rad(moon.angle);return{x:earth.x+Math.cos(a)*moon.radius,y:earth.y+Math.sin(a)*moon.radius,z:clamp(earth.depth+moon.relativeDepth,0,14)};}
function drawMoon(behindPass){if(!moon.visible)return;const m=moonState(),scale=currentScale(),x=cx+viewX+m.x*scale,y=cy+viewY-m.y*scale,r=moon.size*scale*depthScale(m.z),front=earthFrontDepth(m.x,m.y),behind=front!==null&&m.z<front;if(behind!==behindPass)return;const outer=regularPoly(x,y,r,9,Math.PI/9),shadow=regularPoly(x+r*.12,y+r*.12,r*.96,9,Math.PI/9);if(lighting.shadows)ps1Poly(shadow,"rgba(0,0,0,.22)");ps1Poly(outer,"#9ca1a8","#454a52",1.5);ctx.save();ctx.beginPath();ctx.moveTo(outer[0].x,outer[0].y);for(let i=1;i<outer.length;i++)ctx.lineTo(outer[i].x,outer[i].y);ctx.closePath();ctx.clip();ps1Poly([{x:x-r,y:y-r*.7},{x:x+r*.25,y:y-r},{x:x-r*.05,y:y+r*.2}],"#c7c9c9");ps1Poly([{x:x-r*.05,y:y+r*.2},{x:x+r,y:y-r*.1},{x:x+r,y:y+r}],"#747a83");ctx.restore();if(diagnosticMode&&!cleanMode&&showLabels){ctx.fillStyle="#ddd";ctx.font="10px -apple-system";ctx.textAlign="center";ctx.fillText(`Moon ${m.z.toFixed(1)}`,x,y-r-7);}}
function drawEarth(){const scale=currentScale(),x=cx+viewX+earth.x*scale,y=cy+viewY-earth.y*scale,r=earthApparentRadius()*scale,alpha=earth.alpha;ctx.save();ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.clip();ctx.fillStyle=rgb(PS1_OCEAN[1],alpha);ctx.fillRect(x-r,y-r,r*2,r*2);const lightA=rad(lighting.direction),centre={x:artSnap(x-Math.cos(lightA)*r*.12),y:artSnap(y-Math.sin(lightA)*r*.12)};for(let i=0;i<14;i++){const a0=-Math.PI/2+i*Math.PI*2/14,a1=-Math.PI/2+(i+1)*Math.PI*2/14,mid=(a0+a1)/2,lit=clamp((Math.cos(mid-lightA)+1)*.5*(lighting.enabled?lighting.intensity:0)+.18,0,1),shade=clamp(Math.round(lit*4),0,4),p0={x:artSnap(x+Math.cos(a0)*r*1.04),y:artSnap(y+Math.sin(a0)*r*1.04)},p1={x:artSnap(x+Math.cos(a1)*r*1.04),y:artSnap(y+Math.sin(a1)*r*1.04)};ps1Poly([centre,p0,p1],rgb(PS1_OCEAN[shade],alpha));}
const land=[[[-.72,-.58],[-.47,-.73],[-.20,-.60],[-.15,-.38],[-.34,-.27],[-.55,-.34]],[[-.03,-.35],[.24,-.53],[.54,-.40],[.67,-.13],[.49,.06],[.25,.03],[.12,.28],[-.08,.17]],[[-.25,.38],[.02,.27],[.29,.38],[.22,.62],[-.03,.73],[-.28,.61]]];land.forEach((shape,j)=>{const points=shape.map(([px,py])=>({x:artSnap(x+px*r),y:artSnap(y+py*r)}));ps1Poly(points,rgb(PS1_LAND[1+j%3],.88*alpha),rgb(PS1_LAND[0],.38*alpha),1);});const pat=ditherPattern();if(pat){ctx.globalAlpha=.09*alpha;ctx.fillStyle=pat;ctx.fillRect(x-r,y-r,r*2,r*2);ctx.globalAlpha=1;}ctx.restore();ctx.strokeStyle=`rgba(174,198,218,${.7*alpha})`;ctx.lineWidth=2;ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.stroke();if(diagnosticMode&&!cleanMode&&showLabels){ctx.fillStyle="#d8eaff";ctx.font="10px -apple-system";ctx.textAlign="center";ctx.fillText(`Earth ${earth.depth.toFixed(1)}`,x,y-r-8);}if(!earth.locked&&diagnosticMode&&!cleanMode){ctx.strokeStyle="rgba(120,220,255,.65)";ctx.lineWidth=1.5;ctx.setLineDash([6,5]);ctx.beginPath();ctx.arc(x,y,r+5,0,Math.PI*2);ctx.stroke();ctx.setLineDash([]);}}
function diagnosticStyle'''
sub(r'function drawStars\(\).*?\nfunction diagnosticStyle', render_front, 'PS1 sky Earth Moon')

snake_block = r'''function segmentLight(a,b){if(!lighting.enabled)return 0;const dx=b.y-a.y,dy=-(b.x-a.x),L=Math.hypot(dx,dy)||1;return lightDot(dx/L,dy/L)*lighting.intensity;}
function fogRGB(c,z){const amount=clamp((6.5-z)/6.5,0,1)*clamp(+lighting.depthFog||0,0,.5);return[Math.round(lerp(c[0],38,amount)),Math.round(lerp(c[1],42,amount)),Math.round(lerp(c[2],52,amount))];}
function goldShade(index,z,a=1){return rgb(fogRGB(PS1_GOLD[clamp(index,0,PS1_GOLD.length-1)],z),a);}
function coarseRun(run){if(run.length<=3)return run.slice();const out=[run[0]];for(let i=4;i<run.length-1;i+=4)out.push(run[i]);if(out[out.length-1]!==run[run.length-1])out.push(run[run.length-1]);return out;}
function facetGeom(a,b,scale=.48){const dx=b.x-a.x,dy=b.y-a.y,L=Math.hypot(dx,dy)||1,nx=-dy/L,ny=dx/L,ha=a.width*scale,hb=b.width*scale,ca={x:artSnap(a.x),y:artSnap(a.y)},cb={x:artSnap(b.x),y:artSnap(b.y)};return{ca,cb,la:{x:artSnap(a.x+nx*ha),y:artSnap(a.y+ny*ha)},lb:{x:artSnap(b.x+nx*hb),y:artSnap(b.y+ny*hb)},ra:{x:artSnap(a.x-nx*ha),y:artSnap(a.y-ny*ha)},rb:{x:artSnap(b.x-nx*hb),y:artSnap(b.y-ny*hb)},nx,ny};}
function drawFacetSection(a,b,i){const g=facetGeom(a,b),z=(a.z+b.z)/2,li=segmentLight(a,b),base=clamp(Math.round(1+li*2.2),0,4),side=lightDot(g.nx,g.ny)>=.5,left=clamp(base+(side?1:-1),0,4),right=clamp(base+(side?-1:1),0,4);ps1Poly([g.la,g.lb,g.cb,g.ca],goldShade(left,z));ps1Poly([g.ca,g.cb,g.rb,g.ra],goldShade(right,z));const tri=i%2===0?[g.ca,g.lb,g.cb]:[g.ca,g.cb,g.ra];ps1Poly(tri,goldShade(clamp(base+1,0,4),z,.34));ctx.strokeStyle="rgba(54,34,10,.34)";ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(g.ca.x,g.ca.y);ctx.lineTo(g.cb.x,g.cb.y);ctx.stroke();if(i%3===0){ctx.save();ctx.beginPath();ctx.moveTo(g.la.x,g.la.y);ctx.lineTo(g.lb.x,g.lb.y);ctx.lineTo(g.rb.x,g.rb.y);ctx.lineTo(g.ra.x,g.ra.y);ctx.closePath();ctx.clip();const pat=ditherPattern();if(pat){ctx.globalAlpha=.065;ctx.fillStyle=pat;const xs=[g.la.x,g.ra.x,g.lb.x,g.rb.x],ys=[g.la.y,g.ra.y,g.lb.y,g.rb.y],minX=Math.min(...xs),maxX=Math.max(...xs),minY=Math.min(...ys),maxY=Math.max(...ys);ctx.fillRect(minX-2,minY-2,Math.max(4,maxX-minX+4),Math.max(4,maxY-minY+4));}ctx.restore();}}
function drawPS1Run(run){const coarse=coarseRun(run);if(coarse.length<2)return;if(display.outline)drawVariableRibbon(coarse,1+display.outlineThickness*2.2,"#3b270b");for(let i=1;i<coarse.length;i++)drawFacetSection(coarse[i-1],coarse[i],i);}
function drawHiddenSegment(a,b,type){if(!showXray||cleanMode)return;const width=(a.width+b.width)/2,style=diagnosticStyle(type);ctx.lineCap="round";ctx.strokeStyle=style.body;ctx.lineWidth=width;ctx.setLineDash([Math.max(6,width*.30),Math.max(5,width*.18)]);ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();ctx.setLineDash([]);const dx=b.x-a.x,dy=b.y-a.y,L=Math.hypot(dx,dy);if(L<2)return;const ux=dx/L,uy=dy/L,nx=-uy,ny=ux,spacing=Math.max(9,width*.37),len=width*.46;ctx.strokeStyle=style.hash;ctx.lineWidth=Math.max(1.2,width*.05);for(let d=spacing*.5;d<L;d+=spacing){const x=a.x+ux*d,y=a.y+uy*d;ctx.beginPath();ctx.moveTo(x-nx*len-ux*len*.25,y-ny*len-uy*len*.25);ctx.lineTo(x+nx*len+ux*len*.25,y+ny*len+uy*len*.25);ctx.stroke();if(type==="both"){ctx.beginPath();ctx.moveTo(x+nx*len-ux*len*.25,y+ny*len-uy*len*.25);ctx.lineTo(x-nx*len+ux*len*.25,y-ny*len+uy*len*.25);ctx.stroke();}}}
function drawSnake(screen){for(let i=1;i<screen.length;i++){const a=screen[i-1],b=screen[i],aa=occType(a),bb=occType(b);let type="visible";if(aa==="both"||bb==="both")type="both";else if(aa==="earth"||bb==="earth")type="earth";else if(aa==="snake"||bb==="snake")type="snake";if(type!=="visible")drawHiddenSegment(a,b,type);}let run=[];const flush=()=>{if(run.length>1)drawPS1Run(run);run=[];};for(let i=1;i<screen.length;i++){const a=screen[i-1],b=screen[i],visible=occType(a)==="visible"&&occType(b)==="visible";if(visible){if(!run.length)run.push(a);run.push(b);}else flush();}flush();}
function headGeometry'''
sub(r'function drawVisibleOutline\(screen\).*?\nfunction headGeometry', snake_block, 'PS1 snake body')

head_block = r'''function headEyeScreen(screen){const{p,angle,radius}=headGeometry(screen),exLocal=radius*endpoint.eyeX,eyLocal=radius*endpoint.eyeY,c=Math.cos(angle),sn=Math.sin(angle);return{x:p.x+exLocal*c-eyLocal*sn,y:p.y+exLocal*sn+eyLocal*c,radius,angle};}
function drawHead(screen){const{p,angle,radius}=headGeometry(screen),type=occType(p),style=diagnosticStyle(type),visible=type==="visible",outline=visible?"#3b270b":style.hash,coords=[[1.30,.04],[1.08,-.48],[.42,-.78],[-.52,-.76],[-1.18,-.38],[-1.32,.12],[-.88,.66],[.08,.82],[.86,.56]];ctx.save();ctx.translate(artSnap(p.x),artSnap(p.y));ctx.rotate(angle);ctx.beginPath();ctx.moveTo(coords[0][0]*radius,coords[0][1]*radius);for(let i=1;i<coords.length;i++)ctx.lineTo(coords[i][0]*radius,coords[i][1]*radius);ctx.closePath();ctx.fillStyle=visible?goldShade(2,p.z):style.body;ctx.fill();ctx.save();ctx.clip();if(visible){ps1Poly([{x:-1.3*radius,y:-.1*radius},{x:.25*radius,y:-.82*radius},{x:.52*radius,y:.02*radius}],goldShade(4,p.z));ps1Poly([{x:.52*radius,y:.02*radius},{x:1.35*radius,y:-.18*radius},{x:1.25*radius,y:.58*radius},{x:-.15*radius,y:.78*radius}],goldShade(1,p.z));const pat=ditherPattern();if(pat){ctx.globalAlpha=.07;ctx.fillStyle=pat;ctx.fillRect(-radius*1.4,-radius*.9,radius*2.8,radius*1.8);ctx.globalAlpha=1;}}ctx.restore();ctx.strokeStyle=outline;ctx.lineWidth=Math.max(1.5,radius*.055);ctx.stroke();const ex=radius*endpoint.eyeX,ey=radius*endpoint.eyeY,eyeH=Math.max(1.2,radius*.18*endpoint.eyeOpen);ctx.fillStyle="#f2e7bd";ctx.beginPath();ctx.ellipse(ex,ey,radius*.19,eyeH,0,0,Math.PI*2);ctx.fill();ctx.strokeStyle="#5d3b0d";ctx.lineWidth=Math.max(1,radius*.025);ctx.stroke();const ga=rad(endpoint.gazeDirection-angle*180/Math.PI),px=ex+Math.cos(ga)*radius*.08,py=ey+Math.sin(ga)*radius*.08;ctx.fillStyle="#15110c";ctx.beginPath();ctx.rect(px-Math.max(1.2,radius*.055),py-Math.max(1.2,radius*.055),Math.max(2.4,radius*.11),Math.max(2.4,radius*.11));ctx.fill();ctx.strokeStyle=outline;ctx.lineWidth=Math.max(1.2,radius*.055);ctx.beginPath();ctx.moveTo(radius*.38,radius*.25);ctx.lineTo(radius*.70,radius*(.29+.18*endpoint.mouthOpen));ctx.lineTo(radius*.98,radius*.17);ctx.stroke();ctx.restore();if(display.gazeArrow&&diagnosticMode&&!cleanMode)drawGazeArrow(screen);}
function drawGazeArrow(screen){const eye=headEyeScreen(screen),a=rad(endpoint.gazeDirection),len=Math.max(38,eye.radius*2.2),alpha=clamp(+display.gazeOpacity||0,0,1);ctx.strokeStyle=`rgba(100,220,255,${alpha})`;ctx.fillStyle=`rgba(100,220,255,${alpha})`;ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(eye.x,eye.y);ctx.lineTo(eye.x+Math.cos(a)*len,eye.y+Math.sin(a)*len);ctx.stroke();ctx.save();ctx.translate(eye.x+Math.cos(a)*len,eye.y+Math.sin(a)*len);ctx.rotate(a);ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(-9,-5);ctx.lineTo(-9,5);ctx.closePath();ctx.fill();ctx.restore();}
function tailScreenGeometry(screen){const n=screen.length,p=screen[n-1],q=screen[n-2],base=Math.atan2(p.y-q.y,p.x-q.x)+rad(endpoint.tailDirection),ux=Math.cos(base),uy=Math.sin(base),nx=-uy,ny=ux,width=p.width*endpoint.tailWidth,length=width*1.7*endpoint.tailLength,curve=endpoint.tailCurvature*width,tip={x:artSnap(p.x+ux*length+nx*curve),y:artSnap(p.y+uy*length+ny*curve)},baseL={x:artSnap(p.x-ux*width*.35+nx*width),y:artSnap(p.y-uy*width*.35+ny*width)},baseR={x:artSnap(p.x-ux*width*.35-nx*width),y:artSnap(p.y-uy*width*.35-ny*width)},midL={x:artSnap(p.x+ux*length*.48+nx*(curve*.58+width*.55)),y:artSnap(p.y+uy*length*.48+ny*(curve*.58+width*.55))},midR={x:artSnap(p.x+ux*length*.48+nx*(curve*.58-width*.55)),y:artSnap(p.y+uy*length*.48+ny*(curve*.58-width*.55))};return{p,q,tip,baseL,baseR,midL,midR,width};}
function drawTail(screen){const g=tailScreenGeometry(screen),type=occType(g.p),style=diagnosticStyle(type),visible=type==="visible",shape=[g.tip,g.midL,g.baseL,g.baseR,g.midR];ps1Poly(shape,visible?goldShade(2,g.p.z):style.body,visible?"#3b270b":style.hash,2);if(visible){ps1Poly([g.tip,g.midL,g.midR],goldShade(4,g.p.z,.62));ps1Poly([g.midL,g.baseL,g.baseR,g.midR],goldShade(1,g.p.z,.46));}}
function drawSpriteStar(x,y,size,level){const palette=["#b7c6dc","#e7e2b6","#fff0a0","#fff8d2"],c=palette[clamp(level,0,3)],sizePx=Math.max(1,size);ctx.fillStyle=c;ctx.beginPath();ctx.moveTo(artSnap(x),artSnap(y-sizePx*1.7));ctx.lineTo(artSnap(x+sizePx*.55),artSnap(y-sizePx*.55));ctx.lineTo(artSnap(x+sizePx*1.7),artSnap(y));ctx.lineTo(artSnap(x+sizePx*.55),artSnap(y+sizePx*.55));ctx.lineTo(artSnap(x),artSnap(y+sizePx*1.7));ctx.lineTo(artSnap(x-sizePx*.55),artSnap(y+sizePx*.55));ctx.lineTo(artSnap(x-sizePx*1.7),artSnap(y));ctx.lineTo(artSnap(x-sizePx*.55),artSnap(y-sizePx*.55));ctx.closePath();ctx.fill();}
function drawGazeSparkles(screen){if(biteTail||!display.gazeStars||occType(screen[0])!=="visible")return;const eye=headEyeScreen(screen),a=rad(endpoint.gazeDirection),ux=Math.cos(a),uy=Math.sin(a),nx=-uy,ny=ux,layout=[[1.65,-.25],[2.20,.28],[2.75,-.10],[3.28,.38],[3.86,-.31],[4.42,.10]];for(let i=0;i<layout.length;i++){const[d,o]=layout[i],phase=(Math.floor(sparkleFrame/(1+i%3))+i*2)%4,x=eye.x+ux*eye.radius*d+nx*eye.radius*o,y=eye.y+uy*eye.radius*d+ny*eye.radius*o;drawSpriteStar(x,y,1.5+(phase===3?1.8:phase*.35),phase);}const ephase=sparkleFrame%4;drawSpriteStar(eye.x-eye.radius*.055,eye.y-eye.radius*.075,1.2+(ephase===3?1.4:ephase*.25),Math.min(3,1+ephase));}
function syncSparkleAnimation(){const active=!biteTail&&!!display.gazeStars&&!document.hidden;if(active&&!sparkleTimer){sparkleTimer=setInterval(()=>{sparkleFrame=(sparkleFrame+1)%840;draw();},120);}else if(!active&&sparkleTimer){clearInterval(sparkleTimer);sparkleTimer=0;}}
function drawDirectionArrows(screen){if(!showArrows)return;const reversed=[...screen].reverse();let acc=0;const spacing=58*viewZoom;for(let i=1;i<reversed.length;i++){const a=reversed[i-1],b=reversed[i],dx=b.x-a.x,dy=b.y-a.y,len=Math.hypot(dx,dy);acc+=len;if(acc<spacing)continue;acc=0;const angle=Math.atan2(dy,dx),x=(a.x+b.x)/2,y=(a.y+b.y)/2,size=Math.max(5,8*viewZoom);ctx.save();ctx.translate(artSnap(x),artSnap(y));ctx.rotate(angle);ctx.fillStyle="rgba(255,232,128,.96)";ctx.beginPath();ctx.moveTo(size,0);ctx.lineTo(-size*.62,-size*.62);ctx.lineTo(-size*.62,size*.62);ctx.closePath();ctx.fill();ctx.restore();}}
function depthPointColour'''
sub(r'function drawHead\(screen\).*?\nfunction depthPointColour', head_block, 'PS1 head tail sparkle')

guides = r'''function drawMouthTailGuide(){if(!display.mouthTailGuide)return;const anchors=biteAnchorsWorld(),a=project({...anchors.mouth,z:pts[0].z}),b=project({...anchors.tip,z:pts[pts.length-1].z}),d=Math.hypot(anchors.mouth.x-anchors.tip.x,anchors.mouth.y-anchors.tip.y);ctx.strokeStyle="rgba(120,220,255,.55)";ctx.lineWidth=1.5;ctx.setLineDash([5,5]);ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();ctx.setLineDash([]);ctx.fillStyle="#9ee8ff";ctx.font="10px -apple-system";ctx.textAlign="center";ctx.fillText(d.toFixed(2),(a.x+b.x)/2,(a.y+b.y)/2-6);}
function drawClosurePreview(){if(!display.closurePreview)return;const anchors=biteAnchorsWorld(),hs=project({...anchors.mouth,z:pts[0].z}),ts=project({...anchors.tip,z:pts[pts.length-1].z}),mx=(hs.x+ts.x)/2,my=Math.min(hs.y,ts.y)-currentScale()*.55;ctx.strokeStyle="rgba(255,220,140,.48)";ctx.lineWidth=2;ctx.setLineDash([8,6]);ctx.beginPath();ctx.moveTo(hs.x,hs.y);ctx.lineTo(mx,my);ctx.lineTo(ts.x,ts.y);ctx.stroke();ctx.setLineDash([]);}
function drawTopologyMarkers'''
sub(r'function drawMouthTailGuide\(\).*?\nfunction drawTopologyMarkers', guides, 'bite guide anchors')

contact_draw = r'''function drawContactShadows(){if(!lighting.shadows)return;for(const p of pts){if(p.contact!=="TOUCHING_EARTH")continue;const s=project(p),ex=project({x:earth.x,y:earth.y,z:earth.depth}),dx=s.x-ex.x,dy=s.y-ex.y,L=Math.hypot(dx,dy)||1,x=s.x-dx/L*7,y=s.y-dy/L*7;ctx.save();ctx.translate(artSnap(x),artSnap(y));ctx.rotate(Math.atan2(dy,dx));ctx.scale(1,.38);ps1Poly(regularPoly(0,0,14,8,Math.PI/8),"rgba(0,0,0,.24)");ctx.restore();}}
function draw(){ctx.clearRect(0,0,W,H);drawStars();drawReferenceCircle();drawMoon(true);drawEarth();drawMoon(false);drawContactShadows();const screen=classify(sampleCurve());drawSnake(screen);drawDirectionArrows(screen);drawHead(screen);drawTail(screen);drawGazeSparkles(screen);drawMouthTailGuide();drawClosurePreview();drawTopologyMarkers(screen);drawPoints();}

function nearestPoint'''
sub(r'function drawContactShadows\(\).*?\n\nfunction nearestPoint', contact_draw, 'PS1 draw pipeline')

exact(
    'pointX:{apply:v=>{if(selected>=0)setSelectedCoordinate("x",v);}},pointY:{apply:v=>{if(selected>=0)setSelectedCoordinate("y",v);}},depth:{apply:v=>{if(selected>=0)pts[selected].z=v;}},pointWidth:{apply:v=>{if(selected>=0)pts[selected].width=v;}},',
    'pointX:{apply:v=>{if(selected>=0)setSelectedCoordinate("x",v);}},pointY:{apply:v=>{if(selected>=0)setSelectedCoordinate("y",v);}},depth:{apply:v=>setSelectedScalar("z",v)},pointWidth:{apply:v=>setSelectedScalar("width",v)},',
    'endpoint point scalar controls')
exact(
    'snakeScale:{apply:v=>{if(v<=0||Math.abs(v-snakeScale)<1e-10)return;const ratio=v/snakeScale;let mx=0,my=0;for(const p of pts){mx+=p.x;my+=p.y;}mx/=pts.length;my/=pts.length;for(const p of pts){p.x=mx+(p.x-mx)*ratio;p.y=my+(p.y-my)*ratio;}snakeScale=v;if(preserveLength)preserveTarget=arcLength();}},',
    'snakeScale:{apply:v=>{if(v<=0||Math.abs(v-snakeScale)<1e-10)return;const ratio=v/snakeScale;let mx=0,my=0;for(const p of pts){mx+=p.x;my+=p.y;}mx/=pts.length;my/=pts.length;for(const p of pts){p.x=mx+(p.x-mx)*ratio;p.y=my+(p.y-my)*ratio;}snakeScale=v;if(biteTail)enforceBiteVisual(null);if(preserveLength)preserveTarget=arcLength();}},',
    'snake scale bite')
exact(
    'headSize:{apply:v=>endpoint.headSize=v},headRotation:{apply:v=>endpoint.headRotation=v},neckWidth:{apply:v=>endpoint.neckWidth=v},eyeOpen:{apply:v=>endpoint.eyeOpen=v},eyeX:{apply:v=>endpoint.eyeX=v},eyeY:{apply:v=>endpoint.eyeY=v},gazeDirection:{apply:v=>endpoint.gazeDirection=v},mouthOpen:{apply:v=>endpoint.mouthOpen=v},tailLength:{apply:v=>endpoint.tailLength=v},tailWidth:{apply:v=>endpoint.tailWidth=v},tailDirection:{apply:v=>endpoint.tailDirection=v},tailCurvature:{apply:v=>endpoint.tailCurvature=v},',
    'headSize:{apply:v=>setEndpointValue("headSize",v)},headRotation:{apply:v=>setEndpointValue("headRotation",v)},neckWidth:{apply:v=>setEndpointValue("neckWidth",v)},eyeOpen:{apply:v=>setEndpointValue("eyeOpen",v)},eyeX:{apply:v=>setEndpointValue("eyeX",v)},eyeY:{apply:v=>setEndpointValue("eyeY",v)},gazeDirection:{apply:v=>setEndpointValue("gazeDirection",v)},mouthOpen:{apply:v=>setEndpointValue("mouthOpen",v)},tailLength:{apply:v=>setEndpointValue("tailLength",v)},tailWidth:{apply:v=>setEndpointValue("tailWidth",v)},tailDirection:{apply:v=>setEndpointValue("tailDirection",v)},tailCurvature:{apply:v=>setEndpointValue("tailCurvature",v)},',
    'endpoint geometry controls')
exact(
    '$("farBtn").onclick=()=>{if(selected>=0)mutate(()=>pts[selected].z=3);};$("centreBtn").onclick=()=>{if(selected>=0)mutate(()=>pts[selected].z=6.5);};$("nearBtn").onclick=()=>{if(selected>=0)mutate(()=>pts[selected].z=10);};',
    '$("farBtn").onclick=()=>{if(selected>=0)mutate(()=>setSelectedScalar("z",3));};$("centreBtn").onclick=()=>{if(selected>=0)mutate(()=>setSelectedScalar("z",6.5));};$("nearBtn").onclick=()=>{if(selected>=0)mutate(()=>setSelectedScalar("z",10));};',
    'depth buttons bite')

exact(
    'if(!$("gazeOpacity")){',
    'if(!$("gazeStarsToggle")){const grid=$("gazeArrow")?.parentElement;if(grid){const btn=document.createElement("button");btn.id="gazeStarsToggle";btn.type="button";btn.textContent="Gaze stars";grid.appendChild(btn);btn.onclick=()=>mutate(()=>display.gazeStars=!display.gazeStars);}}\nif(!$("gazeOpacity")){',
    'gaze stars control')
exact(
    'setToggle("referenceCircle",display.referenceCircle);setToggle("mouthTailGuide",display.mouthTailGuide);setToggle("closurePreview",display.closurePreview);setToggle("gazeArrow",display.gazeArrow);setToggle("arrows",showArrows);',
    'setToggle("referenceCircle",display.referenceCircle);setToggle("mouthTailGuide",display.mouthTailGuide);setToggle("closurePreview",display.closurePreview);setToggle("gazeArrow",display.gazeArrow);setToggle("gazeStarsToggle",display.gazeStars);setToggle("arrows",showArrows);',
    'sync gaze stars UI')

exact(
    'display:{outline:display.outline,outlineThickness:display.outlineThickness,referenceCircle:display.referenceCircle,mouthTailGuide:display.mouthTailGuide,closurePreview:display.closurePreview,gazeArrow:display.gazeArrow,gazeOpacity:display.gazeOpacity,arrows:showArrows,points:showPoints,depthLabels:showLabels,xray:showXray,numbers:showNumbers,transitions:showTransitions,contacts:showContacts,diagnosticMode,cleanMode}',
    'display:{outline:display.outline,outlineThickness:display.outlineThickness,referenceCircle:display.referenceCircle,mouthTailGuide:display.mouthTailGuide,closurePreview:display.closurePreview,gazeArrow:display.gazeArrow,gazeOpacity:display.gazeOpacity,gazeStars:display.gazeStars,arrows:showArrows,points:showPoints,depthLabels:showLabels,xray:showXray,numbers:showNumbers,transitions:showTransitions,contacts:showContacts,diagnosticMode,cleanMode}',
    'export gaze stars')
exact(
    'for(const key of["outline","outlineThickness","referenceCircle","mouthTailGuide","closurePreview","gazeArrow","gazeOpacity"])if(key in data.display)display[key]=data.display[key];',
    'for(const key of["outline","outlineThickness","referenceCircle","mouthTailGuide","closurePreview","gazeArrow","gazeOpacity","gazeStars"])if(key in data.display)display[key]=data.display[key];',
    'import gaze stars')
exact(
    'function inferLegacyBite(){if(pts.length<2)return true;const a=pts[0],b=pts[pts.length-1];return Math.hypot(a.x-b.x,a.y-b.y)<=Math.max(.75,.35*snakeScale);}',
    'function inferLegacyBite(){if(pts.length<2)return true;const{mouth,tip}=biteAnchorsWorld();return Math.hypot(mouth.x-tip.x,mouth.y-tip.y)<=Math.max(.50,.32*snakeScale);}',
    'legacy bite inference')
exact(
    'if(data.constraints){biteTail=data.constraints.biteTail??true;preserveLength=!!data.constraints.preserveLength;preserveTarget=Number.isFinite(+data.constraints.preserveTarget)?+data.constraints.preserveTarget:null;}else{biteTail=inferLegacyBite();preserveLength=false;preserveTarget=null;}if(preserveLength&&!Number.isFinite(preserveTarget))preserveTarget=arcLength();selected=-1;if(!silent){syncAllUI();draw();autosave();}}',
    'if(data.constraints){biteTail=data.constraints.biteTail??true;preserveLength=!!data.constraints.preserveLength;preserveTarget=Number.isFinite(+data.constraints.preserveTarget)?+data.constraints.preserveTarget:null;}else{biteTail=inferLegacyBite();preserveLength=false;preserveTarget=null;}if(biteTail)enforceBiteVisual(null);if(preserveLength&&!Number.isFinite(preserveTarget))preserveTarget=arcLength();selected=-1;if(!silent){syncAllUI();draw();autosave();syncSparkleAnimation();}}',
    'import bite enforcement')

exact(
    'Object.assign(earth,{x:0,y:0,r:2.15,depth:6.5,scale:1,alpha:1,locked:true});',
    'Object.assign(earth,{x:0,y:0,r:2.50,depth:6.5,scale:1,alpha:1,locked:true});',
    'reset Earth size')
exact(
    'Object.assign(display,{outline:true,outlineThickness:.08,referenceCircle:false,mouthTailGuide:false,closurePreview:false,gazeArrow:true,gazeOpacity:.95});snakeScale=1;',
    'Object.assign(display,{outline:true,outlineThickness:.08,referenceCircle:false,mouthTailGuide:false,closurePreview:false,gazeArrow:true,gazeOpacity:.95,gazeStars:true});snakeScale=1;',
    'reset display')
exact(
    'biteTail=true;preserveLength=false;preserveTarget=null;selected=-1;});',
    'biteTail=true;preserveLength=false;preserveTarget=null;enforceBiteVisual(null);selected=-1;});',
    'reset bite closure')

exact(
    'document.addEventListener("visibilitychange",()=>{if(document.hidden)cancelActiveInput();});',
    'document.addEventListener("visibilitychange",()=>{if(document.hidden)cancelActiveInput();syncSparkleAnimation();});',
    'visibility sparkle')
exact(
    'restoreAutosave();\nsyncAllUI();\nresize();',
    'restoreAutosave();\nif(biteTail)enforceBiteVisual(null);\nsyncAllUI();\nresize();\nsyncSparkleAnimation();',
    'startup bite/render')

path.write_text(s)
