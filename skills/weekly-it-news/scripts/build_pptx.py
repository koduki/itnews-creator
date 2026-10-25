#!/usr/bin/env python3
"""Offline, stdlib-only fallback for a real editable .pptx in Copilot Chat.

Usage: python scripts/build_pptx.py plan.json output.pptx
Input is a JSON object with slides. This is intentionally a limited fallback,
not a replacement for Microsoft's richer native PowerPoint composition tools.
No network, pip or external package is required. Images must already exist as
local .png/.jpg files made available by the user/host with suitable reuse rights.
"""
import argparse
import json
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr
from zipfile import ZipFile, ZIP_DEFLATED

EMU = 914400
SW, SH = 12192000, 6858000  # 13.333 × 7.5 in (16:9)
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
REL = 'http://schemas.openxmlformats.org/package/2006/relationships'
C = 'http://schemas.openxmlformats.org/package/2006/content-types'


def e(txt):
    return escape(str(txt), {'"': '&quot;'})


def shape(sid, name, text, x, y, w, h, size=2200, color='333333', bold=False, fill=None, align='l'):
    if text is None: text = ''
    lines = str(text).split('\n')
    nv = (f'<p:nvSpPr><p:cNvPr id="{sid}" name={quoteattr(name)}/>'
          '<p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>')
    geom = f'<a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
    geom += f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>' if fill else '<a:noFill/>'
    geom += '<a:ln><a:noFill/></a:ln>'
    paras = []
    for textline in lines:
        rp = (f'<a:rPr lang="ja-JP" sz="{size}" b="{1 if bold else 0}">'
              f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
              '<a:latin typeface="Noto Sans JP"/><a:ea typeface="Noto Sans JP"/></a:rPr>')
        paras.append(f'<a:p><a:pPr algn="{align}"/><a:r>{rp}<a:t>{e(textline)}</a:t></a:r><a:endParaRPr lang="ja-JP"/></a:p>')
    body = '<p:txBody><a:bodyPr wrap="square" lIns="0" rIns="0" tIns="0" bIns="0"/><a:lstStyle/>' + ''.join(paras) + '</p:txBody>'
    return f'<p:sp>{nv}<p:spPr>{geom}</p:spPr>{body}</p:sp>'


def image(sid, rid, name, x, y, w, h):
    return (f'<p:pic><p:nvPicPr><p:cNvPr id="{sid}" name={quoteattr(name)}/>'
            '<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>'
            f'<p:blipFill><a:blip r:embed="rId{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')


def slide_xml(shapes):
    head = f'<p:sld xmlns:p="{P}" xmlns:a="{A}" xmlns:r="{R}"><p:cSld><p:spTree>'
    group = '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
    return head + group + ''.join(shapes) + '</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'


def rels(items):
    return f'<Relationships xmlns="{REL}">' + ''.join(f'<Relationship Id="rId{i}" Type="{R}/{kind}" Target={quoteattr(target)}/>' for i, kind, target in items) + '</Relationships>'


def theme_xml():
    colors = [('dk1','000000'),('lt1','FFFFFF'),('dk2','333333'),('lt2','F3F3F3'),('accent1','C00000'),('accent2','888888'),('accent3','2074B7'),('accent4','44A68C'),('accent5','A07AB4'),('accent6','D69C3D'),('hlink','0563C1'),('folHlink','954F72')]
    scheme = ''.join(f'<a:{n}><a:srgbClr val="{c}"/></a:{n}>' for n,c in colors)
    font = '<a:majorFont><a:latin typeface="Aptos Display"/><a:ea typeface="Noto Sans JP"/><a:cs typeface="Aptos"/></a:majorFont><a:minorFont><a:latin typeface="Aptos"/><a:ea typeface="Noto Sans JP"/><a:cs typeface="Aptos"/></a:minorFont>'
    fmt = ('<a:fmtScheme name="Plain">'
           '<a:fillStyleLst><a:solidFill><a:schemeClr val="accent1"/></a:solidFill></a:fillStyleLst>'
           '<a:lnStyleLst><a:ln w="9525"><a:solidFill><a:schemeClr val="accent1"/></a:solidFill></a:ln></a:lnStyleLst>'
           '<a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>'
           '<a:bgFillStyleLst><a:solidFill><a:schemeClr val="lt1"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme>')
    return f'<a:theme xmlns:a="{A}" name="Weekly IT News"><a:themeElements><a:clrScheme name="Plain">{scheme}</a:clrScheme><a:fontScheme name="Plain">{font}</a:fontScheme>{fmt}</a:themeElements></a:theme>'


def image_valid(path):
    if not path.is_file(): raise ValueError(f'Image file not found: {path}')
    data=path.read_bytes()
    if data.startswith(b'\x89PNG\r\n\x1a\n') and path.suffix.lower()=='.png': return data, 'png'
    if data.startswith(b'\xff\xd8\xff') and path.suffix.lower() in ('.jpg','.jpeg'): return data, 'jpeg'
    raise ValueError('Only genuine local PNG/JPEG image bytes are supported: '+str(path))


def render_slide(slide, index, base, media):
    layout = slide.get('layout','explainer')
    title = slide.get('title','')
    if not isinstance(title,str): raise ValueError('Slide title must be text')
    shapes=[]; nextid=2; photo_rel=None
    def add(txt,x,y,w,h,sz=2200,color='333333',bold=False,fill=None):
        nonlocal nextid
        shapes.append(shape(nextid,f'Editable text {nextid}',txt,x,y,w,h,sz,color,bold,fill));nextid+=1
    if layout == 'cover':
        add(slide.get('date',''),800000,1400000,10000000,800000,3500,'C00000',True)
        add(title or 'Weekly IT News！',800000,2600000,11000000,1500000,4600,'333333',True)
    else:
        add(title,700000,340000,11200000,800000,2800,'C00000',True)
        add('',700000,1230000,10800000,30000,200,'C00000',False,'C00000')
        bullets=slide.get('bullets',[])
        if not isinstance(bullets,list) or any(not isinstance(x,str) for x in bullets): raise ValueError('bullets must be a list of strings')
        if bullets:
            height=min(5100000,max(2800000,len(bullets)*720000))
            texts='\n'.join(('• '+x) for x in bullets)
            add(texts,900000,1700000,10300000,height,2100,'333333')
        if slide.get('image'):
            asset=(base / slide['image']).resolve()
            # Image bytes must come from a host/user-provided file. Never perform network fetches.
            data, ext=image_valid(asset)
            key=f'image{len(media)+1}.{ext}';media.append((key,data,ext,index))
            photo_rel=(2,key)
            if bullets:
                # Put photo in the right half alongside shorter bullets.
                shapes[-1]=shape(nextid-1, f'Editable text {nextid-1}', texts, 750000,1550000,5000000,4400000,1700,'333333')
                shapes.append(image(nextid,2,'Authentic source image',6200000,1500000,5150000,3800000))
            else:
                shapes.append(image(nextid,2,'Authentic source image',700000,1420000,10900000,4400000))
            nextid+=1
        caption=slide.get('caption','')
        source=slide.get('source_url','')
        if caption or source:
            add((caption+'  '+source).strip(),700000,6100000,10900000,460000,1200,'666666')
    return slide_xml(shapes),photo_rel


def build(plan_path,output):
    plan_path=Path(plan_path).resolve();output=Path(output)
    if output.suffix.lower() != '.pptx':
        raise ValueError('Output must be a .pptx file, not Word/PDF')
    deck=json.loads(plan_path.read_text(encoding='utf-8'))
    if not isinstance(deck,dict) or not isinstance(deck.get('slides'),list) or not deck['slides']:
        raise ValueError('JSON requires a nonempty slides array')
    if len(deck['slides'])>100:raise ValueError('Too many slides for this minimal fallback')
    slides=deck['slides'];media=[]; xmls=[]; relations=[]
    if any('topic_id' in slide or 'role' in slide for slide in slides if isinstance(slide, dict)):
        # Validate continuity before emitting a PPTX; never silently re-sort an authored story.
        from importlib.util import spec_from_file_location, module_from_spec
        flow_path = Path(__file__).with_name('check_editorial_flow.py')
        spec = spec_from_file_location('itnews_flow_validator', flow_path)
        if spec is None or spec.loader is None: raise ValueError('Missing continuity validator')
        validator = module_from_spec(spec)
        spec.loader.exec_module(validator)
        errors=validator.validate_plan(deck,final=False)
        if errors: raise ValueError('Invalid news storyboard: ' + '; '.join(errors))
    minimum=deck.get('min_evidence_images',0)
    if not isinstance(minimum,int) or isinstance(minimum,bool) or minimum<0:
        raise ValueError('min_evidence_images must be a nonnegative integer')
    for i,entry in enumerate(slides,1):
        if not isinstance(entry,dict):raise ValueError('Each slide must be an object')
        content,pic=render_slide(entry,i,plan_path.parent,media);xmls.append(content)
        relations.append(rels([(1,'slideLayout','../slideLayouts/slideLayout1.xml')]+([(2,'image','../media/'+pic[1])] if pic else [])))
    if len(media)<minimum:
        raise ValueError(f'Image requirement unmet: {len(media)} local source images embedded; {minimum} required')
    content_types=f'<Types xmlns="{C}"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/><Default Extension="jpeg" ContentType="image/jpeg"/><Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/><Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/><Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/><Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'+''.join(f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>' for i in range(1,len(slides)+1))+'</Types>'
    ids=''.join(f'<p:sldId id="{255+i}" r:id="rId{i+1}"/>' for i in range(1,len(slides)+1))
    presentation=f'<p:presentation xmlns:p="{P}" xmlns:a="{A}" xmlns:r="{R}"><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst><p:sldIdLst>{ids}</p:sldIdLst><p:sldSz cx="{SW}" cy="{SH}" type="screen16x9"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>'
    prels=rels([(1,'slideMaster','slideMasters/slideMaster1.xml')]+[(i+1,'slide',f'slides/slide{i}.xml') for i in range(1,len(slides)+1)])
    master=f'<p:sldMaster xmlns:p="{P}" xmlns:a="{A}" xmlns:r="{R}"><p:cSld name="Plain"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld><p:clrMap accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" bg1="lt1" bg2="lt2" tx1="dk1" tx2="dk2" hlink="hlink" folHlink="folHlink"/><p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst><p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles></p:sldMaster>'
    layout=f'<p:sldLayout xmlns:p="{P}" xmlns:a="{A}" xmlns:r="{R}" type="blank" preserve="1"><p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>'
    files={'[Content_Types].xml':content_types,'_rels/.rels':rels([(1,'officeDocument','ppt/presentation.xml')]),'ppt/presentation.xml':presentation,'ppt/_rels/presentation.xml.rels':prels,'ppt/slideMasters/slideMaster1.xml':master,'ppt/slideMasters/_rels/slideMaster1.xml.rels':rels([(1,'slideLayout','../slideLayouts/slideLayout1.xml'),(2,'theme','../theme/theme1.xml')]),'ppt/slideLayouts/slideLayout1.xml':layout,'ppt/slideLayouts/_rels/slideLayout1.xml.rels':rels([(1,'slideMaster','../slideMasters/slideMaster1.xml')]),'ppt/theme/theme1.xml':theme_xml()}
    for i,(xml,rs) in enumerate(zip(xmls,relations),1):
        files[f'ppt/slides/slide{i}.xml']=xml;files[f'ppt/slides/_rels/slide{i}.xml.rels']=rs
    output.parent.mkdir(parents=True,exist_ok=True)
    with ZipFile(output,'w',ZIP_DEFLATED) as z:
        for name,body in sorted(files.items()):z.writestr(name,body)
        for name,data,ext,i in media:z.writestr('ppt/media/'+name,data)
    print(f'PPTX created: {output} ({len(slides)} slides, {len(media)} supplied local images)')
    return len(slides),len(media)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('plan');ap.add_argument('pptx');args=ap.parse_args()
    build(args.plan,args.pptx)

if __name__=='__main__':main()