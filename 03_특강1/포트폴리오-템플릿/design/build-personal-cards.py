"""Generate the five personal-introduction cards requested by the user.

The former CakGo-only set is preserved in design/cakgo-cardnews-backup/.
PNG exports use verify-portfolio.mjs --export-cards.
"""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / 'portfolio' / 'cardnews'
NAME = 'Ahmad Najmi Bin Muhamad Sade'
CAPTIONS = ['나즈미 소개', '관심과 동기', '역량과 협업', '프로젝트와 연구', '성장 방향과 연락처']

def section(number, classes, label, title, lines, visual, footer):
    support = '<p class="support">' + ''.join(f'<span>{escape(line)}</span>' for line in lines) + '</p>' if lines else ''
    return f'''<div class="card-shell"><section class="news-card personal {classes}" id="card-{number:02}" aria-labelledby="title-{number:02}">
<div class="card-top"><span>NAJMI / ABOUT ME</span><span>{number:02} — 05</span></div>
<p class="section-label">{escape(label)}</p><h2 id="title-{number:02}">{title}</h2>{support}{visual}
<div class="card-bottom"><span>나즈미 · AI RESEARCH</span><span>{footer}</span></div></section></div>'''

cards = [f'''<div class="card-shell"><section class="news-card cover personal-cover" id="card-01" aria-labelledby="title-01">
<div class="card-top"><span>NAJMI / ABOUT ME</span><span>01 — 05</span></div><div class="watermark" aria-hidden="true">AI</div>
<p class="name">나즈미</p><p class="english-name">{NAME}</p><p class="school">한양대학교 ERICA 인공지능학과 3학년</p>
<h2 id="title-01">사용자의 문제에서 출발해<br>AI 모델을 구현하고 실험하는<br><span class="gold">AI 연구자</span>를 지향합니다.</h2>
<div class="featured"><span>관심 직무</span><strong>AI 연구원</strong></div>
<div class="card-bottom"><span>PERSONAL BRANDING / 2026</span><span>HELLO, I’M NAJMI</span></div></section></div>''']

values = '<div class="personal-values" aria-label="나의 관심과 학습 태도">' + ''.join(f'<div><span>{i:02}</span><strong>{value}</strong></div>' for i,value in enumerate(['사람 중심','직접 실험','협업과 성장'],1)) + '</div>'
cards.append(section(2,'personal-interest','01 · 나의 관심과 동기',
    '기술보다 먼저,<br><span class="gold">사람의 불편</span>을<br>살펴봅니다.',
    ['CakGo에서는 시각적 어려움이 있는 사람의',
     '실내 물품 탐색에 초점을 맞췄습니다.',
     '컴퓨터 비전과 자연어처리에 관심이 있습니다.'],values,'MOTIVATION'))

skills = '<div class="pipeline" aria-label="내가 경험한 기술과 협업 역할">' + ''.join(f'<div class="pipeline-step"><b>{i:02}</b><strong>{name}</strong><span class="flow-arrow" aria-hidden="true">↗</span></div>' for i,name in enumerate(['모델 학습·평가','실험 구성요소 통합','팀 운영·PR 관리'],1)) + '</div>'
cards.append(section(3,'personal-skills','02 · 나의 역량과 협업',
    '모델 실험과<br>팀의 작업을<br><span class="gold">하나로 잇습니다.</span>',
    ['CakGo 팀장으로 YOLO 파인튜닝·평가를 맡았습니다.',
     'SUARA에서는 음색 실험과 파이프라인 통합을 맡습니다.',
     '학생단체 회장·재무 활동으로 운영 경험을 쌓았습니다.'],skills,'SKILLS & COLLABORATION'))

projects = '<div class="personal-projects" aria-label="프로젝트별 진행 상태">' + ''.join(f'<div><span>{status}</span><strong>{name}</strong><small>{area}</small></div>' for status,name,area in [('프로토타입 완료','CakGo','객체 탐지'),('진행 중','SUARA','음성 분석'),('진행 중','개인 연구','계층적 계획')]) + '</div>'
cards.append(section(4,'personal-research','03 · 나의 프로젝트와 연구',
    '프로젝트를 만들고,<br><span class="gold">연구 질문</span>을<br>넓혀 갑니다.',
    ['CakGo · 실내 물품 탐색 프로토타입을 완성했습니다.',
     'SUARA · 음색·가창 음성 임베딩을 실험합니다.',
     '개인 연구 · 계층적 계획과 메모리 재사용을 탐구합니다.'],projects,'PROJECTS & RESEARCH'))

signature = f'<div class="quote" aria-hidden="true">”</div><div class="signature"><p class="korean-name">나즈미</p><p class="english-name">{NAME}</p><a class="email" href="mailto:sadenajmi@gmail.com">sadenajmi@gmail.com ↗</a></div>'
cards.append(section(5,'closing personal-direction','04 · 나의 성장 방향',
    '사람을 이해하고,<br><span class="gold">AI로 도움을 주는</span><br>연구자로 성장하겠습니다.',
    ['한국 AI·IT 분야에서 실무 경험을 쌓고 싶습니다.',
     '모델 구현·실험과 업무 한국어 역량을 키우겠습니다.',
     '사용자의 필요를 확인하며 연구하고 싶습니다.'],signature,'LET’S CONNECT'))

downloads = ''.join(f'<a href="card-{i:02}.png" download>{i:02} {title} ↓</a>' for i,title in enumerate(CAPTIONS,1))
html = f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#100a1c"><title>나를 소개하는 카드뉴스 | 나즈미</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css"><link rel="stylesheet" href="cards.css"></head>
<body><header class="viewer"><a href="../index.html#cardnews">← 포트폴리오로 돌아가기</a><h1>나를 소개하는 카드뉴스 · 나즈미</h1><p>나의 관심과 동기, 역량, 프로젝트와 연구, 성장 방향을 다섯 장에 담았습니다.<br>각 이미지는 1080 × 1350 PNG로 내려받을 수 있습니다.</p><a href="overview.html">다섯 장 한눈에 보기 ↗</a><nav class="downloads" aria-label="카드 이미지 다운로드">{downloads}</nav></header>
<main>{''.join(cards)}</main><p class="preview-footer"><a href="overview.html">나를 소개하는 카드뉴스 다섯 장 한눈에 보기 ↗</a><br>배포 전 연락 채널을 수록했습니다. 배포 후 마지막 카드에 포트폴리오 공개 주소를 추가할 수 있습니다.</p>
<script>(()=>{{const shells=document.querySelectorAll('.card-shell');const fit=()=>shells.forEach(s=>s.style.setProperty('--card-scale',s.clientWidth/1080));fit();window.addEventListener('resize',fit);}})();</script></body></html>'''
(DEST/'index.html').write_text(html,encoding='utf-8')

overview = (DEST/'overview.html').read_text(encoding='utf-8')
head = overview.split('<body><main>')[0].replace('CakGo 카드뉴스 한눈에 보기 | 나즈미','나를 소개하는 카드뉴스 한눈에 보기 | 나즈미')
grid = ''.join(f'<figure><a class="image-link" href="card-{i:02}.png" aria-label="{i}번 {title} 원본 이미지 보기"><img src="card-{i:02}.png" width="1080" height="1350" alt="{i}. {title}"></a><figcaption><div class="caption"><span class="number">{i:02}</span><h2>{title}</h2></div><a class="download" href="card-{i:02}.png" download>PNG 다운로드 ↓</a></figcaption></figure>' for i,title in enumerate(CAPTIONS,1))
(DEST/'overview.html').write_text(head + f'''<body><main><header><a class="back" href="../index.html#cardnews">← 포트폴리오로 돌아가기</a><p class="eyebrow">NAJMI / PERSONAL BRANDING</p><h1>나를 소개하는 카드뉴스</h1><p>나즈미 {NAME} · 한양대학교 ERICA 인공지능학과 3학년</p></header><section class="grid" aria-label="자기소개 카드뉴스 다섯 장 모아 보기">{grid}</section><footer><span>이미지를 누르면 원본 크기로 볼 수 있습니다.</span><a class="detail-link" href="index.html">카드 한 장씩 크게 보기 ↗</a></footer></main></body></html>''',encoding='utf-8')
print('Updated the five-card set and overview to introduce Najmi personally.')
