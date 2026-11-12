"""Exporta el PDF Beamer a PowerPoint visual con 25 diapositivas.
Requiere pdftoppm y pdftotext (Poppler); usa solo la biblioteca estándar.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile, ZIP_DEFLATED
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
REL = 'http://schemas.openxmlformats.org/package/2006/relationships'
CT = 'http://schemas.openxmlformats.org/package/2006/content-types'


def main():
    with ZipFile(ROOT / 'herramientas/recursos/plantilla_presentacion.pptx') as z:
        files = {n: z.read(n) for n in z.namelist()}
    with TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        subprocess.run(['pdftoppm', '-scale-to', '2400', '-png', str(ROOT/'ppt/diapositivas.pdf'), str(tmp/'slide')], check=True)
        images = sorted(tmp.glob('slide-*.png'))
        if len(images) != 25:
            raise ValueError(f'Se requieren 25 diapositivas; se encontraron {len(images)}')
        pres = ET.fromstring(files['ppt/presentation.xml'])
        ids = pres.find(f'{{{P}}}sldIdLst')
        if ids is None:
            ids = ET.Element(f'{{{P}}}sldIdLst')
            pres.insert(1, ids)
        size = pres.find(f'{{{P}}}sldSz')
        size.set('cx', '12192000'); size.set('cy', '6858000'); size.set('type', 'screen16x9')
        rels = ET.fromstring(files['ppt/_rels/presentation.xml.rels'])
        types = ET.fromstring(files['[Content_Types].xml'])
        if not any(e.get('Extension') == 'png' for e in types):
            ET.SubElement(types, f'{{{CT}}}Default', Extension='png', ContentType='image/png')
        for i, path in enumerate(images, 1):
            rid = f'rIdSlide{i}'
            ET.SubElement(ids, f'{{{P}}}sldId', id=str(255+i), attrib={f'{{{R}}}id': rid})
            ET.SubElement(rels, f'{{{REL}}}Relationship', Id=rid, Type=R+'/slide', Target=f'slides/slide{i}.xml')
            ET.SubElement(types, f'{{{CT}}}Override', PartName=f'/ppt/slides/slide{i}.xml', ContentType='application/vnd.openxmlformats-officedocument.presentationml.slide+xml')
            files[f'ppt/media/slide{i}.png'] = path.read_bytes()
            files[f'ppt/slides/slide{i}.xml'] = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:p="{P}" xmlns:a="{A}" xmlns:r="{R}"><p:cSld><p:spTree>
<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>
<p:pic><p:nvPicPr><p:cNvPr id="2" name="Diapositiva {i}" descr="Presentación del grupo 2; fuente editable en LaTeX"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr><p:blipFill><a:blip r:embed="rIdImage"/><a:stretch><a:fillRect/></a:stretch></p:blipFill><p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="12192000" cy="6858000"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>
</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr><p:transition advClick="1"><p:fade/></p:transition></p:sld>'''.encode()
            files[f'ppt/slides/_rels/slide{i}.xml.rels'] = f'''<Relationships xmlns="{REL}"><Relationship Id="rIdImage" Type="{R}/image" Target="../media/slide{i}.png"/><Relationship Id="rIdLayout" Type="{R}/slideLayout" Target="../slideLayouts/slideLayout7.xml"/></Relationships>'''.encode()
        files['ppt/presentation.xml'] = ET.tostring(pres, encoding='utf-8', xml_declaration=True)
        files['ppt/_rels/presentation.xml.rels'] = ET.tostring(rels, encoding='utf-8', xml_declaration=True)
        files['[Content_Types].xml'] = ET.tostring(types, encoding='utf-8', xml_declaration=True)
        props = ET.fromstring(files['ppt/presProps.xml'])
        show = ET.SubElement(props, f'{{{P}}}showPr')
        ET.SubElement(show, f'{{{P}}}present')
        files['ppt/presProps.xml'] = ET.tostring(props, encoding='utf-8', xml_declaration=True)
        with ZipFile(ROOT/'ppt/diapositivas.pptx', 'w', ZIP_DEFLATED) as z:
            for name, data in files.items():
                z.writestr(name, data)
    print('PowerPoint generado: ppt/diapositivas.pptx (25 diapositivas)')


if __name__ == '__main__':
    main()
