"""Create a self-contained HTML submission without changing the working website."""
from pathlib import Path
from base64 import b64encode
from html import escape
from html.parser import HTMLParser
import re

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / 'portfolio'
OUT = PUBLIC / '나즈미_인공지능학과_2024079443.html'

def uri(path, mime):
    return 'data:' + mime + ';base64,' + b64encode(path.read_bytes()).decode('ascii')

html = (PUBLIC/'index.html').read_text(encoding='utf-8')
css = (PUBLIC/'styles.css').read_text(encoding='utf-8')
font = uri(ROOT/'design/pretendard-variable.woff2', 'font/woff2')
license_text = (ROOT/'design/pretendard-license.txt').read_text(encoding='utf-8')
font_css = '/* Embedded Pretendard font license:\n' + license_text.replace('*/','* /') + '\n*/\n'
font_css += '@font-face{font-family:"Pretendard Variable";font-style:normal;font-weight:100 900;font-display:swap;src:url("' + font + '") format("woff2")}\n'
extra_css = '''
.embedded-overview{margin-top:32px;border:1px solid var(--line);border-radius:16px;padding:24px}
.embedded-overview summary{cursor:pointer;color:var(--accent);font-size:18px;font-weight:600}
.embedded-overview h2{font-size:28px;margin:24px 0}
.embedded-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:16px}
.embedded-grid figure{min-width:0;margin:0}.embedded-grid a{display:block}
.embedded-grid img{display:block;width:100%;height:auto;border:1px solid #a18759;border-radius:12px}
.embedded-grid figcaption{font-size:12px;color:var(--muted);margin-top:10px}
@media(max-width:900px){.embedded-grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(max-width:600px){.embedded-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.embedded-overview{padding:16px}}
'''
html = re.sub(r'<link\b[^>]*rel="stylesheet"[^>]*>\s*', '', html)
html = html.replace('</head>', '<style>\n' + font_css + css + extra_css + '\n</style></head>')
html = html.replace('poster="cakgo-demo-poster.jpg"', 'poster="' + uri(PUBLIC/'cakgo-demo-poster.jpg','image/jpeg') + '"')
html = html.replace('src="cakgo-demo.mp4"', 'src="' + uri(PUBLIC/'cakgo-demo.mp4','video/mp4') + '"')
html = html.replace('href="cakgo-demo.mp4"', 'href="#demo" data-embedded-video')

titles = [('나즈미 소개','Meet Najmi'),('관심과 동기','Interests and motivation'),('역량과 협업','Skills and collaboration'),('프로젝트와 연구','Projects and research'),('성장 방향과 연락처','Direction and contact')]
grid = ''
for number,(ko,en) in enumerate(titles,1):
    path = f'cardnews/card-{number:02}.png'
    html = html.replace(f'src="{path}"', 'src="' + uri(PUBLIC/path,'image/png') + '"')
    html = html.replace(f'href="{path}"', f'href="#cardnews" data-embedded-download="{number}"')
    grid += f'<figure><a href="#cardnews" data-embedded-download="{number}" download="najmi-card-{number:02}.png"><img data-embedded-image="{number}" width="1080" height="1350" alt="{escape(ko+" / "+en,quote=True)}"></a><figcaption>{number:02} / <span lang="ko">{ko}</span><span lang="en">{en}</span></figcaption></figure>'

html = html.replace('href="cardnews/overview.html"', 'href="#all-cards" data-open-overview')
overview = '<section aria-label="Card news overview / 카드뉴스 모아 보기"><details class="embedded-overview" id="all-cards"><summary><span lang="ko">자기소개 카드뉴스 다섯 장 한눈에 보기</span><span lang="en">All five personal-introduction cards</span></summary><h2><span lang="ko">나를 소개하는 카드뉴스</span><span lang="en">Meet me in five cards</span></h2><div class="embedded-grid">' + grid + '</div></details></section>'
marker = '<section class="major-section" aria-labelledby="beyond-title">'
assert marker in html
html = html.replace(marker,overview+marker,1)
script = '''
<script>
(() => {
  const originals = Array.from(document.querySelectorAll('#cardnews .cardnews-item img'));
  document.querySelectorAll('[data-embedded-image]').forEach(image => {
    image.src = originals[Number(image.dataset.embeddedImage)-1].src;
  });
  document.querySelectorAll('[data-embedded-download]').forEach(link => {
    const number = Number(link.dataset.embeddedDownload);
    link.href = originals[number-1].src;
    link.download = 'najmi-card-' + String(number).padStart(2,'0') + '.png';
  });
  document.querySelectorAll('[data-embedded-video]').forEach(link => {
    link.href = document.querySelector('video source').src;
    link.download = 'cakgo-demo.mp4';
  });
  document.querySelectorAll('[data-open-overview]').forEach(link => {
    link.addEventListener('click', () => { document.getElementById('all-cards').open = true; });
  });
})();
</script>
'''
html = html.replace('</body>',script+'</body>')

class Audit(HTMLParser):
    def __init__(self):
        super().__init__();self.assets=[];self.links=[];self.ids=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs:self.ids.append(attrs['id'])
        for key in ['src','poster']:
            if key in attrs:self.assets.append(attrs[key])
        if tag=='link' and 'href' in attrs:self.assets.append(attrs['href'])
        if tag=='a':self.links.append(attrs.get('href',''))

audit=Audit();audit.feed(html)
assert all(src.startswith('data:') for src in audit.assets)
assert all(link.startswith(('#','https:','mailto:')) for link in audit.links)
assert len(audit.ids)==len(set(audit.ids))
assert '{{' not in html
assert '2024709443' not in html
OUT.write_text(html,encoding='utf-8')
print('Created:',OUT.name)
print('File size:',round(OUT.stat().st_size/1_000_000,2),'MB')
print('Styles, font, five PNGs, poster, and video are embedded. No local asset dependencies.')
