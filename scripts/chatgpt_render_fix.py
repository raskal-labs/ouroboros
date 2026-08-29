from pathlib import Path
import re

path = Path('js/app.js')
s = path.read_text()

head = r'''function drawHead(screen){const{p,angle,radius}=headGeometry(screen),type=occType(p),style=diagnosticStyle(type),visible=type==="visible",outline=visible?"#3b270b":style.hash,coords=[[1.30,.04],[1.08,-.48],[.42,-.78],[-.52,-.76],[-1.18,-.38],[-1.32,.12],[-.88,.66],[.08,.82],[.86,.56]],trace=()=>{ctx.beginPath();ctx.moveTo(coords[0][0]*radius,coords[0][1]*radius);for(let i=1;i<coords.length;i++)ctx.lineTo(coords[i][0]*radius,coords[i][1]*radius);ctx.closePath();};ctx.save();ctx.translate(artSnap(p.x),artSnap(p.y));ctx.rotate(angle);trace();ctx.fillStyle=visible?goldShade(2,p.z):style.body;ctx.fill();ctx.save();trace();ctx.clip();if(visible){ps1Poly([{x:-1.3*radius,y:-.1*radius},{x:.25*radius,y:-.82*radius},{x:.52*radius,y:.02*radius}],goldShade(4,p.z));ps1Poly([{x:.52*radius,y:.02*radius},{x:1.35*radius,y:-.18*radius},{x:1.25*radius,y:.58*radius},{x:-.15*radius,y:.78*radius}],goldShade(1,p.z));const pat=ditherPattern();if(pat){ctx.globalAlpha=.07;ctx.fillStyle=pat;ctx.fillRect(-radius*1.4,-radius*.9,radius*2.8,radius*1.8);ctx.globalAlpha=1;}}ctx.restore();trace();ctx.strokeStyle=outline;ctx.lineWidth=Math.max(1.5,radius*.055);ctx.stroke();const ex=radius*endpoint.eyeX,ey=radius*endpoint.eyeY,eyeH=Math.max(1.2,radius*.18*endpoint.eyeOpen);ctx.fillStyle="#f2e7bd";ctx.beginPath();ctx.ellipse(ex,ey,radius*.19,eyeH,0,0,Math.PI*2);ctx.fill();ctx.strokeStyle="#5d3b0d";ctx.lineWidth=Math.max(1,radius*.025);ctx.stroke();const ga=rad(endpoint.gazeDirection-angle*180/Math.PI),px=ex+Math.cos(ga)*radius*.08,py=ey+Math.sin(ga)*radius*.08;ctx.fillStyle="#15110c";ctx.beginPath();ctx.rect(px-Math.max(1.2,radius*.055),py-Math.max(1.2,radius*.055),Math.max(2.4,radius*.11),Math.max(2.4,radius*.11));ctx.fill();ctx.strokeStyle=outline;ctx.lineWidth=Math.max(1.2,radius*.055);ctx.beginPath();ctx.moveTo(radius*.38,radius*.25);ctx.lineTo(radius*.70,radius*(.29+.18*endpoint.mouthOpen));ctx.lineTo(radius*.98,radius*.17);ctx.stroke();ctx.restore();if(display.gazeArrow&&diagnosticMode&&!cleanMode)drawGazeArrow(screen);}'''
s, n = re.subn(r'function drawHead\(screen\)\{.*?\}\nfunction drawGazeArrow', lambda m: head+'\nfunction drawGazeArrow', s, count=1, flags=re.S)
if n != 1:
    raise SystemExit(f'head replacement count {n}')

tail = r'''function drawTail(screen){const g=tailScreenGeometry(screen),type=occType(g.p),style=diagnosticStyle(type),visible=type==="visible",shape=[g.tip,g.midL,g.baseL,g.baseR,g.midR],outline=visible?"#3b270b":style.hash;ps1Poly(shape,visible?goldShade(2,g.p.z):style.body);if(visible){ps1Poly([g.tip,g.midL,g.midR],goldShade(4,g.p.z,.62));ps1Poly([g.midL,g.baseL,g.baseR,g.midR],goldShade(1,g.p.z,.46));}ctx.beginPath();ctx.moveTo(shape[0].x,shape[0].y);for(let i=1;i<shape.length;i++)ctx.lineTo(shape[i].x,shape[i].y);ctx.closePath();ctx.strokeStyle=outline;ctx.lineWidth=2;ctx.setLineDash([]);ctx.stroke();}'''
s, n = re.subn(r'function drawTail\(screen\)\{.*?\}\nfunction drawSpriteStar', lambda m: tail+'\nfunction drawSpriteStar', s, count=1, flags=re.S)
if n != 1:
    raise SystemExit(f'tail replacement count {n}')

path.write_text(s)
