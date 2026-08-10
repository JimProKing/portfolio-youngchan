# YC.RUNTIME — 이영찬 포트폴리오

토스인컴 Security Engineer 등 채용 지원용 **개인 소개 웹사이트**.

- GitHub: [JimProKing](https://github.com/JimProKing)
- 로컬: 부팅 연출 → 스토리 타임라인 → 프로젝트 벤토 → 커맨드 팔레트(`⌘K` / `Ctrl+K`)

## 로컬 실행

```powershell
cd C:\Users\a\Desktop\portfolio-youngchan
npm install
npm run dev
```

브라우저에서 http://localhost:5173 열기.  
또는 `python -m http.server 5173` / `index.html` 더블클릭.

## Railway 배포

1. [railway.app](https://railway.app)에서 새 프로젝트 → **Deploy from GitHub** (이 폴더를 푸시한 레포 연결)
2. 루트에 `package.json` / `railway.toml` / `nixpacks.toml` 이 있으므로 **별도 설정 없이** 빌드·기동됩니다.
3. 생성되는 Public URL을 이력서·지원서 포트폴리오 링크에 넣으면 됩니다.

CLI로 배포할 때:

```powershell
cd C:\Users\a\Desktop\portfolio-youngchan
# railway login 후
railway init
railway up
```

`PORT` 환경변수는 Railway가 자동 주입합니다 (`serve`가 `0.0.0.0:$PORT`로 listen).

## 이력서 PDF

```powershell
python generate_resume.py
```

결과: `이영찬_이력서.pdf` (같은 폴더)

## 구성

```
index.html
css/style.css
js/app.js
README.md
```

빌드 도구 없음. 정적 파일만으로 GitHub Pages / Netlify / Railway 등에 배포 가능.

## 커맨드 팔레트

| 명령 | 동작 |
|------|------|
| `whoami` | 한 줄 소개 |
| `projects` | 프로젝트 섹션 |
| `story` | 스토리 |
| `github` | GitHub 열기 |
| `email` | 메일 |
| `aegis` | Aegis Cortex 저장소 |
| `help` | 전체 목록 |

## 커스터마이즈

- 연락처·프로젝트 링크: `index.html`
- 색·타이포: `css/style.css` 의 `:root`
- 부팅 로그 문구: `js/app.js` 의 `lines` 배열
