# HypeProof AI 랜딩페이지 개선 리서치

> Linear.app 벤치마킹 + 모던 랜딩페이지 베스트 프랙티스

---

## 🎯 Linear.app 핵심 패턴 분석

### 1. Hero Section
| Linear | HypeProof 현재 | 개선안 |
|--------|---------------|--------|
| **제품 스크린샷** 중심 | 텍스트만 있음 | 실제 리서치/팟캐스트 미리보기 추가 |
| 명확한 가치 제안 | ✅ 있음 | 유지 |
| 두 개의 CTA (Start, Contact) | 하나만 있음 | "Listen Now" + "Contact" 듀얼 CTA |

### 2. Social Proof (신뢰 지표)
| Linear | HypeProof 현재 | 개선안 |
|--------|---------------|--------|
| **기업 로고** (OpenAI, Ramp 등) | ❌ 없음 | 협업사/출연자 로고 또는 통계 |
| "Powering the world's best..." | ❌ 없음 | "Featured by...", "100+ episodes" 등 |

### 3. Feature Section 깊이
| Linear | HypeProof 현재 | 개선안 |
|--------|---------------|--------|
| **스크린샷 + 상세 설명** | 아이콘 + 짧은 텍스트 | 각 트랙별 상세 페이지 링크 |
| 인터랙티브 데모 | ❌ 없음 | 팟캐스트 플레이어 임베드 |
| 서브 피처 그리드 | ❌ 없음 | 연구 주제, 에피소드 목록 |

### 4. AI/Tech 하이라이트
Linear는 "AI-assisted" 섹션을 별도로 강조:
- Triage Intelligence
- Linear MCP (Claude, ChatGPT 연동)
- Self-driving operations

**HypeProof 적용안**: 
- "AI-Powered Research" 섹션 추가
- 사용하는 AI 도구들 (Claude, OpenClaw 등) 소개

---

## 🔥 추가할 섹션 우선순위

### P0 (즉시 적용)
1. **Social Proof Bar**
   - 숫자 통계: "12 Episodes", "5 Researchers", "3 Active Projects"
   - 또는 미디어 출연/인용 로고

2. **CTA 개선**
   - Primary: "Listen to Latest Episode" (팟캐스트로 연결)
   - Secondary: "Contact Us"

3. **Latest Content Preview**
   - 최신 팟캐스트 에피소드 카드
   - 최신 리서치 칼럼 미리보기

### P1 (1주 내)
4. **Product Demo / Visual**
   - Hero에 실제 콘텐츠 스크린샷
   - 또는 애니메이션 일러스트레이션

5. **Testimonials / Quotes**
   - 청취자/독자 피드백
   - 또는 팀원들의 철학 인용문

6. **Newsletter Signup**
   - 이메일 구독 폼
   - "Get weekly AI insights"

### P2 (2주 내)
7. **Interactive Elements**
   - 팟캐스트 미니 플레이어
   - 리서치 토픽 인터랙티브 그래프

8. **Blog/Column Integration**
   - 실제 칼럼 콘텐츠 연동
   - CMS 또는 MDX 기반

---

## 🎨 디자인 개선 포인트

### Linear 스타일 요소
```css
/* 1. Gradient Text (이미 있음) */
.text-gradient {
  background: linear-gradient(to right, #fff, #a78bfa);
  -webkit-background-clip: text;
}

/* 2. Subtle Grid Background (이미 있음) */
.grid-pattern { ... }

/* 3. Glass Cards with Border Glow */
.glass-card:hover {
  border-color: rgba(168, 85, 247, 0.5);
  box-shadow: 0 0 30px rgba(168, 85, 247, 0.1);
}

/* 4. Staggered Animations */
.feature-card:nth-child(1) { animation-delay: 0s; }
.feature-card:nth-child(2) { animation-delay: 0.1s; }
.feature-card:nth-child(3) { animation-delay: 0.2s; }
```

### 추가 마이크로 인터랙션
- Hover시 카드 약간 위로 (✅ 있음)
- 스크롤 진입시 fade-in (✅ 있음)
- **추가**: 배경 orb 마우스 추적
- **추가**: 타이핑 효과 (Hero 태그라인)

---

## 📊 성과 측정 추가

### Vercel Analytics 연동
```tsx
// layout.tsx
import { Analytics } from '@vercel/analytics/next';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

### 추적할 이벤트
- CTA 클릭률
- 스크롤 깊이
- 팟캐스트 플레이어 재생
- 외부 링크 클릭

---

## 🚀 구현 로드맵

### Week 1
- [ ] Social proof bar 추가
- [ ] Dual CTA 구현
- [ ] Vercel Analytics 연동

### Week 2
- [ ] Latest content preview 섹션
- [ ] Newsletter signup form
- [ ] Hero visual/screenshot 추가

### Week 3
- [ ] Testimonials 섹션
- [ ] 팟캐스트 플레이어 임베드
- [ ] 실제 칼럼 콘텐츠 연동

---

## 참고 자료

- **Linear.app**: https://linear.app
- **Vercel.com**: https://vercel.com (유사한 다크 테마)
- **Raycast.com**: https://raycast.com (개발자 타겟)
- **Framer Motion**: https://framer.com/motion (애니메이션)

---

*Generated: 2026-02-06*
