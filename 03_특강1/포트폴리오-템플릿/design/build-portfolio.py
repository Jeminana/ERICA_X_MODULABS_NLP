"""Authoring source for the initial bilingual page; no build step is needed to view it.

Running this script replaces portfolio/index.html. Preserve later manual additions
(such as card news) before regenerating it.
"""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parent.parent
NAME = 'Ahmad Najmi Bin Muhamad Sade'
REPO = 'https://github.com/Jeminana/CakGo_AI-powered-indoor-object-finding-assistant'
REPORT = REPO + '/blob/main/tests/results/real_photos/COMPARISON.md'
LINKEDIN = 'https://www.linkedin.com/in/ahmad-najmi-830078360'
HEADLINE_KO = '사용자의 문제에서 출발해 AI 모델을 구현하고 실험하는 AI 연구자를 지향합니다.'
HEADLINE_EN = 'I aim to become an AI researcher who starts with users’ problems and implements and experiments with AI models.'

def t(ko, en):
    return f'<span lang="ko">{escape(ko)}</span><span lang="en">{escape(en)}</span>'

def heading(number, label, ko, en, id):
    return f'<div class="section-heading"><div><p class="eyebrow">{number} / {label}</p><h2 id="{id}">{t(ko,en)}</h2></div></div>'

person = {'@context':'https://schema.org','@type':'Person','name':'나즈미 '+NAME,
          'alternateName':NAME,'description':HEADLINE_KO,
          'affiliation':{'@type':'CollegeOrUniversity','name':'한양대학교 ERICA'},
          'email':'sadenajmi@gmail.com','sameAs':[LINKEDIN]}

body = f'''
<a class="skip" href="#main">{t('본문 바로가기','Skip to content')}</a>
<div class="topbar"><div class="wrap topbar-inner">
  <a class="brand" href="#profile" aria-label="Najmi — home"><span class="monogram" aria-hidden="true">AN</span><span class="brand-word">NAJMI / PORTFOLIO</span></a>
  <nav aria-label="Main navigation"><a href="#works">{t('작업물','Projects')}</a><a href="#case">{t('대표 프로젝트','Case study')}</a><a href="#contact">{t('연락','Contact')}</a></nav>
  <div class="languages" role="group" aria-label="Language / 언어"><button type="button" data-language="ko" aria-pressed="true" aria-label="한국어로 보기">한국어</button><button type="button" data-language="en" aria-pressed="false" aria-label="View in English">English</button></div>
</div></div>
<main class="wrap" id="main">
<!-- 1. Profile -->
<header class="profile" id="profile"><div>
  <p class="eyebrow">AI RESEARCH · HUMAN-CENTERED THINKING</p>
  <h1><span lang="ko">나즈미<span class="english-name">{NAME}</span></span><span lang="en">Ahmad Najmi<br>Bin Muhamad Sade</span></h1>
  <p class="school">{t('한양대학교 ERICA 인공지능학과 3학년 · AI 연구원 지망','Hanyang University ERICA · Artificial Intelligence · Third year · Aspiring AI researcher')}</p>
  <p class="headline">{t(HEADLINE_KO,HEADLINE_EN)}</p>
  <p class="intro">{t('컴퓨터 비전과 자연어처리에 관심을 두고, 직접 구현하고 실험하며 배웁니다. 생활 물품 탐색 프로토타입 CakGo를 만들었고, 현재 음성 분석과 계층적 계획·메모리 재사용을 탐구하고 있습니다.','I learn by building and testing, with interests in computer vision and natural language processing. I worked on CakGo, an everyday object-finding prototype, and I am now exploring voice analysis, hierarchical planning, and memory reuse.')}</p>
  <div class="actions"><a class="button primary" href="#case">{t('대표 프로젝트 보기','Explore CakGo')} <span aria-hidden="true">↗</span></a><a class="button" href="{LINKEDIN}">LinkedIn <span aria-hidden="true">↗</span></a></div>
</div><aside class="focus-card" aria-labelledby="focus-title">
  <div class="focus-head"><span>FEATURED PROJECT / 01</span><span>2026</span></div>
  <h2 id="focus-title">CakGo<span style="color:var(--accent)">.</span></h2>
  <p class="project-sub">{t('일상의 물건을 찾는 또 하나의 방법.','Another way to find everyday objects.')}</p>
  <div class="scan"><p class="scan-title">COMPUTER VISION × ACCESSIBILITY</p><div class="scan-flow">{t('카메라','Camera')}<b aria-hidden="true">→</b>{t('탐지','Detect')}<b aria-hidden="true">→</b>{t('음성 안내','Voice')}</div><p class="scan-caption">{t('실내 생활 물품 탐색 보조 프로토타입','Indoor everyday object-finding prototype')}</p></div>
  <div class="focus-foot">{t('팀 4명 · 팀장 · 프로토타입 완료','Team of 4 · Team lead · Prototype complete')}<a href="#demo">{t('시연 영상','Watch demo')} ↗</a></div>
</aside></header>
<div class="interests"><strong>AREAS OF INTEREST</strong><span>Computer Vision</span><span>Natural Language Processing</span><span>Hierarchical Planning</span></div>
<!-- 2. Work inventory -->
<section id="works" class="major-section" aria-labelledby="works-title">
{heading('01','SELECTED WORK','구현하고, 실험하고, 배우는 과정','Building, testing, learning.','works-title')}
<div class="cards">
'''

cards = [
    ('COMPUTER VISION', '완료 · 대표', 'Complete · Featured', 'CakGo', 'CakGo',
     '2026.10.13–2026.10.22 · 팀 4명', '2026.10.13–2026.10.22 · Team of 4',
     '휴대폰 카메라와 한국어 음성 안내로 시각적 어려움이 있는 사용자의 실내 물품 탐색을 돕는 프로토타입.',
     'A phone-camera prototype with Korean voice guidance, intended to help people with visual difficulties find indoor objects.',
     '내 역할 · 팀장', 'My role · Team lead',
     'YOLO 파인튜닝·실사진 평가, 일정·역할 배분, PR·병합 관리, 통합 지원과 시연 준비.',
     'YOLO fine-tuning and real-photo evaluation, task planning, PR and merge management, integration support, and demo preparation.'),
    ('VOICE ANALYSIS', '진행 중', 'In progress', 'SUARA System', 'SUARA System',
     '2026년 2학기–현재 · 팀 6명', 'Semester 2, 2026–present · Team of 6',
     '음역과 음색 등 개인의 목소리 특성을 분석해 적합한 노래를 추천하는 시스템을 개발하고 있습니다.',
     'Developing a system to recommend suitable songs using vocal characteristics such as range and timbre.',
     '내 역할 · 실험과 통합, 팀 운영', 'My role · Experiments, integration, coordination',
     '음색·가창 음성 임베딩 실험, 메인 파이프라인 통합, PR 관리, 업무 분담과 교수·회의 일정 조율.',
     'Timbre and singing-voice embedding experiments, pipeline integration, PR management, task distribution, and lecturer and meeting coordination.'),
    ('INDIVIDUAL RESEARCH', '진행 중', 'In progress', '계층적 계획과 메모리 재사용', 'Hierarchical planning & memory reuse',
     '2026년 2학기–현재 · 개인 연구', 'Semester 2, 2026–present · Individual research',
     '이전 계획과 의존성 정보를 재사용해 반복 계산·토큰 사용·추론 지연을 줄일 수 있는지 탐구합니다.',
     'Investigating whether previous plans and dependency information can be reused to reduce computation, token use, and inference latency.',
     '내 역할 · 연구 전반', 'My role · Research overall',
     '관련 문헌 검토, 접근법 비교와 시나리오 설계. 효율 개선은 아직 검증하지 않은 연구 목표입니다.',
     'Literature review, approach comparison, and scenario design. Efficiency improvements remain research goals, not verified results.')
]
for i, (category, sk, se, nk, ne, pk, pe, dk, de, rk, re, wk, we) in enumerate(cards, 1):
    link = f'<a class="card-link" href="#case">{t("과정 자세히 보기","Read the case study")} ↗</a>' if i == 1 else ''
    if i == 2:
        link = f'<a class="card-link" href="https://github.com/Jeminana/SUARA-System">{t("공개 코드 저장소","Public code repository")} ↗</a>'
    body += f'<article class="card {"featured" if i == 1 else ""}"><div class="card-top"><span class="project-number">0{i} / {category}</span><span class="status">{t(sk,se)}</span></div><h3>{t(nk,ne)}</h3><p class="meta">{t(pk,pe)}</p><p class="description">{t(dk,de)}</p><p class="role"><strong>{t(rk,re)}</strong>{t(wk,we)}</p>{link}</article>\n'

body += f'''
</div></section>
<!-- 3. Featured case study: official five-part checklist -->
<section id="case" class="major-section" aria-labelledby="case-title">
{heading('02','FEATURED CASE STUDY','CakGo, 문제에서 프로토타입까지','CakGo, from problem to prototype.','case-title')}
<article class="case"><div class="case-header"><div><h3>CakGo</h3><p class="one-liner">{t('시각적 어려움이 있는 사람의 실내 생활 물품 탐색을 돕습니다.','Helping people with visual difficulties find everyday objects indoors.')}</p></div><p class="case-facts">2026.10.13–2026.10.22<br>{t('팀 4명 / 팀장 · 완료한 프로토타입','Team of 4 / Team lead · Completed prototype')}</p></div>
<div class="case-layout">
<aside class="demo" id="demo"><figure><video controls playsinline preload="metadata" poster="cakgo-demo-poster.jpg" aria-label="CakGo demonstration video"><source src="cakgo-demo.mp4" type="video/mp4"><a href="cakgo-demo.mp4">{t('CakGo 시연 영상 파일 열기','Open the CakGo demo video')}</a></video><figcaption>{t('직접 준비한 CakGo 시연 영상 · 약 1분 40초. 프로토타입의 동작을 보여 주는 기록입니다.','CakGo demonstration video · about 1 min 40 sec. A recording of the prototype in use.')}</figcaption></figure><a class="evidence-link" href="{REPO}">{t('공개 코드 저장소','Public code repository')} ↗</a><a class="evidence-link" href="cakgo-demo.mp4" download>{t('시연 영상 다운로드','Download demo video')} ↓</a></aside>
<div>
'''

parts = [
    ('problem','문제','Problem',
     '시각장애나 노화, 심한 난시·근시·원시 등으로 물건을 찾기 어려운 사람을 돕고자 했습니다. 실내에서 자주 사용하는 안경·열쇠·지갑 등 생활 물품을 찾는 상황에 초점을 맞췄습니다. 휴대폰 카메라로 보이는 물건을 찾고 방향을 음성으로 안내하는 보조 수단을 만들고자 했습니다.',
     'I wanted to help people who struggle to find objects because of visual impairment, aging, or severe astigmatism, nearsightedness, or farsightedness. The focus was on frequently used indoor items such as glasses, keys, and wallets. We aimed to offer a supporting tool that identifies visible objects through a phone camera and gives spoken directional guidance.'),
    ('approach','접근','Approach',
     'YOLO와 Grounding DINO를 비교하고, 팀이 촬영한 실제 사진 94장으로 실사용 조건의 탐지 결과를 살폈습니다. 실사진에서의 미탐과 오탐을 함께 고려해 Grounding DINO 다중 프롬프트 방식을 최종 탐지 모델로 선택했습니다. 물건을 설명해 개인 물품별 학습 없이 찾는 YOLOE 방식도 시도했지만 성공하지 못했습니다.',
     'We compared YOLO and Grounding DINO, examining detection results on 94 real photographs taken by the team. Considering both missed detections and false alarms, the team selected Grounding DINO with multi-prompt input as the final detector. We also tried YOLOE for description-based search without training separately on personal items, but that experiment was unsuccessful.'),
    ('design','에이전트 설계','Agent design',
     '실제 구현은 휴대폰 카메라 입력, 객체 탐지, 화면 표시와 한국어 음성 안내를 연결한 파이프라인입니다. 최종 탐지에는 Grounding DINO 다중 프롬프트 방식을 사용했습니다. 저는 YOLO 파인튜닝·실사진 평가, 팀 운영과 통합 지원을 맡았습니다. 시연용 접속 링크와 데모 영상도 준비했습니다.',
     'The actual implementation is a pipeline connecting phone-camera input, object detection, visual display, and Korean spoken guidance. Grounding DINO with multi-prompt input is the final detector. My work covered YOLO fine-tuning, real-photo evaluation, team coordination, and integration support. I also prepared the demo access link and demonstration video.'),
    ('results','결과','Results',
     '카메라 입력부터 탐지와 한국어 음성 안내까지 연결한 프로토타입을 완성했습니다. 실사진 비교에서는 먼 거리와 어두운 조명에서의 한계, 미탐과 오탐을 확인했습니다. 이 평가는 대상 사용자 설문이나 사용성 검증을 대신하지 않습니다.',
     'We completed a prototype connecting camera input, detection, and Korean spoken guidance. The real-photo comparison documented missed detections, false alarms, and difficulties with distance and dim lighting. This evaluation does not substitute for a survey or usability study with intended users.'),
    ('learned','배운 것','Lessons learned',
     '문제 정의와 동기, 핵심 용어를 먼저 정리하고 작업의 우선순위와 역할을 나누는 법을 배웠습니다. 기존 모델을 학습하고 프로젝트에 적용하며, 팀 작업을 연결하려면 지속적인 소통과 충분한 준비가 필요하다는 점도 배웠습니다. 다시 진행한다면 대상 사용자 설문으로 실제로 찾기 어려운 물품과 필요한 도움을 파악한 뒤, 탐지 대상과 기능을 정하겠습니다.',
     'I learned to clarify the problem, motivation, and key terms before prioritizing and dividing tasks. Training and applying existing models also taught me that integrating teammates’ work requires continuing communication and thorough preparation. If I repeated the project, I would first survey intended users about the objects they struggle to find and the help they need, then prioritize objects and features accordingly.')
]
for i, (id, hk, he, pk, pe) in enumerate(parts, 1):
    extra = ''
    if id == 'approach':
        extra = f'<p class="source">{t("근거: ","Evidence: ")}<a href="{REPORT}">{t("실사진 모델 비교 보고서","Real-photo model comparison")} ↗</a></p>'
    elif id == 'design':
        extra = f'<div class="system-flow" aria-label="System pipeline">{t("카메라 입력","Camera input")}<b aria-hidden="true">→</b><span>Grounding DINO</span><b aria-hidden="true">→</b>{t("화면·음성 안내","Visual & voice guidance")}</div>'
    elif id == 'results':
        extra = f'<div class="outcome"><strong>{t("구현한 것","Implemented")}</strong><p>{t("카메라 기반 물품 탐지, 화면 표시, 한국어 음성 출력 안내.","Camera-based object detection, visual output, and Korean spoken guidance.")}</p></div><div class="outcome limit"><strong>{t("안 된 것과 남은 과제","Unsuccessful and unfinished")}</strong><p>{t("YOLOE 설명 기반 탐색은 성공하지 못했습니다. 찾을 물건을 음성으로 선택하는 STT는 구현하지 않았으며, 추가하고 싶은 기능으로 남았습니다.","YOLOE description-based search was unsuccessful. Speech-to-text for choosing an object was not implemented and remains a desired addition.")}</p></div>'
    body += f'<div class="case-part" id="{id}"><span class="step-number">0{i}</span><div><h4>{t(hk,he)}</h4><p>{t(pk,pe)}</p>{extra}</div></div>\n'

gallery = ''
card_titles = [('나즈미 소개','Meet Najmi'),('관심과 동기','Interests and motivation'),('역량과 협업','Skills and collaboration'),('프로젝트와 연구','Projects and research'),('성장 방향과 연락처','Direction and contact')]
for number, (ko, en) in enumerate(card_titles, 1):
    gallery += f'<figure class="cardnews-item"><a href="cardnews/card-{number:02}.png" download><img src="cardnews/card-{number:02}.png" width="1080" height="1350" loading="lazy" alt="{escape(ko + " / " + en, quote=True)}"></a><figcaption>{number:02} / {t(ko,en)}</figcaption></figure>'

body += f'''
</div></div></article></section>
<section id="cardnews" class="major-section" aria-labelledby="cardnews-title">
{heading('03','ABOUT ME IN FIVE CARDS','나를 소개하는 카드뉴스','Meet me in five cards.','cardnews-title')}
<p class="cardnews-intro">{t('나의 관심과 동기, 역량, 프로젝트와 연구, 성장 방향을 다섯 장에 담았습니다. 옆으로 넘겨 보거나 이미지를 눌러 저장할 수 있습니다.','Five Korean cards introducing my motivation, skills, projects, research, and future direction. Scroll sideways to explore, or select an image to download it.')}</p>
<div class="cardnews-gallery" role="region" tabindex="0" aria-label="카드뉴스 이미지 / Card news images">{gallery}</div>
<a class="button" href="cardnews/overview.html">{t('카드뉴스 다섯 장 한눈에 보기','View all five cards together')} ↗</a>
</section>
<section class="major-section" aria-labelledby="beyond-title">
{heading('04','BEYOND THE PROJECTS','기술을 배우고, 사람과 함께 성장합니다.','Learning technology. Growing with people.','beyond-title')}
<div class="beyond"><div><h3>{t('관심과 성장 방향','Interests and direction')}</h3><p>{t('컴퓨터 비전, 자연어처리, 데이터 마이닝과 AI 모델의 원리를 배우고 있습니다. 직접 구현하고 테스트한 결과를 분석하며 이론을 실제 문제와 연결하는 학습을 선호합니다.','I study computer vision, natural language processing, data mining, and the foundations of AI models. I prefer connecting theory to practical problems by implementing ideas, testing them, and analyzing the results.')}</p><p>{t('한국 AI·IT 분야에서 실무 경험을 쌓고, 기술 구현과 연구를 연결하는 역량을 키우고 싶습니다. 업무 한국어와 발표 준비, 우선순위 관리도 함께 개선하고 있습니다.','I hope to gain practical experience in Korea’s AI and IT sector and strengthen the connection between implementation and research. I am also improving professional Korean, presentation preparation, and priority management.')}</p></div>
<div><h3>{t('리더십과 공동체 경험','Leadership and community')}</h3><ul class="activity-list"><li><strong>Rakan SISWA YADIM Korea</strong>{t('초대 회장 · 공동체 프로그램 기획과 학생 교류','Founding president · Community programs and student exchange')}</li><li><strong>EMSU</strong>{t('재무 담당 · 예산 추정, 자금 관리와 행사 자원 배분','Finance role · Budget estimation, fund management, and event resources')}</li><li><strong>{t('교류와 봉사','Exchange and volunteering')}</strong>{t('행사 지원·MC, 말레이시아 방문 학생 안내, 외국인 아동 수학 교육','Event support and MC work, visiting Malaysian student guidance, and mathematics education for foreign children')}</li></ul></div></div></section>
<section class="contact" id="contact" aria-labelledby="contact-title"><p class="eyebrow">05 / CONTACT</p><h2 id="contact-title">{t('연구와 구현으로 이어질 다음 대화를 기다립니다.','Let’s talk about research and building.')}</h2><a class="contact-email" href="mailto:sadenajmi@gmail.com">sadenajmi@gmail.com ↗</a><div class="contact-meta">{t('한양대학교 ERICA 인공지능학과 3학년','Third-year AI student · Hanyang University ERICA')}<a href="{LINKEDIN}">LinkedIn ↗</a></div></section>
<footer><div class="footer-row"><p class="footer-name">{t('나즈미 '+NAME,NAME)}</p><p>{t('마지막 수정','Last updated')} <time datetime="2026-11-05">2026.11.05</time></p><a class="back-top" href="#profile">{t('맨 위로','Back to top')} ↑</a></div></footer>
</main>
'''

script = '''
(() => {
  const root = document.documentElement;
  const buttons = Array.from(document.querySelectorAll('[data-language]'));
  const metadata = LANGUAGE_METADATA;
  function setLanguage(language) {
    if (!Object.hasOwn(metadata, language)) return;
    root.lang = language;
    const selected = metadata[language];
    document.title = selected.title;
    document.querySelector('meta[name="description"]').content = selected.description;
    const person = JSON.parse(document.getElementById('person-data').textContent);
    person.name = selected.name;
    person.description = selected.headline;
    person.affiliation.name = selected.school;
    person.alternateName = language === 'en' ? '나즈미' : 'Ahmad Najmi Bin Muhamad Sade';
    document.getElementById('person-data').textContent = JSON.stringify(person);
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.language === language)));
  }
  buttons.forEach(button => button.addEventListener('click', () => setLanguage(button.dataset.language)));
  root.classList.add('js');
})();
'''
metadata = {
 'ko':{'title':'나즈미 '+NAME+' | 한양대학교 ERICA | AI 연구원 지망','name':'나즈미 '+NAME,'school':'한양대학교 ERICA','headline':HEADLINE_KO,'description':'한양대학교 ERICA 인공지능학과 3학년 나즈미 '+NAME+'. '+HEADLINE_KO},
 'en':{'title':NAME+' | Hanyang University ERICA | Aspiring AI researcher','name':NAME,'school':'Hanyang University ERICA','headline':HEADLINE_EN,'description':NAME+', third-year Artificial Intelligence student at Hanyang University ERICA. Exploring computer vision, voice analysis, hierarchical planning, and memory reuse.'}
}
script = script.replace('LANGUAGE_METADATA', json.dumps(metadata, ensure_ascii=False))
html = f'''<!doctype html>
<html lang="ko"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#100a1c">
<title>{escape(metadata['ko']['title'])}</title>
<meta name="description" content="{escape(metadata['ko']['description'], quote=True)}">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="styles.css">
<script type="application/ld+json" id="person-data">{json.dumps(person, ensure_ascii=False)}</script>
</head><body>{body}<script>{script}</script></body></html>
'''
(ROOT / 'portfolio' / 'index.html').write_text(html, encoding='utf-8')
print('Wrote bilingual portfolio/index.html')
