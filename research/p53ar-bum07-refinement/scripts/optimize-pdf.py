"""Optional document compression immediately AFTER export-pdf.cjs.
JPEG90 inside PDFs, no intentional downsampling; never changes source PNGs.
Do not repeatedly recompress an already optimized PDF.
"""
from pathlib import Path
import subprocess,tempfile,shutil,os
r=Path(__file__).resolve().parents[1]
for name in ['BUM07-P53AR-COMPARISON.pdf']:
 if os.environ.get('P52_BOOK')=='turnaround'and'EXPRESSIONS'in name:continue
 if os.environ.get('P52_BOOK')=='expressions'and'TURNAROUND'in name:continue
 source=r/name
 with tempfile.TemporaryDirectory(prefix='p52-pdf-')as tmp:
  out=Path(tmp)/name
  subprocess.run(['gs','-sDEVICE=pdfwrite','-dCompatibilityLevel=1.6','-dBATCH','-dNOPAUSE','-dSAFER','-dPDFSETTINGS=/prepress','-dDownsampleColorImages=false','-dDownsampleGrayImages=false','-dDownsampleMonoImages=false','-dAutoFilterColorImages=false','-dColorImageFilter=/DCTEncode','-dAutoFilterGrayImages=false','-dGrayImageFilter=/DCTEncode','-dJPEGQ=90','-sOutputFile='+str(out),str(source)],check=True,stdout=subprocess.DEVNULL)
  assert out.read_bytes().startswith(b'%PDF-');shutil.copy2(out,source)
 print('PDF_SCREEN_COPY_READY',name,source.stat().st_size)
