# First sprint — research and 2D design only

This is an occasional hobby project; no fixed weekly deadlines. Keep work lightweight and reversible. First round has three parallel deliverables for discussion, not implementation.

## 1. Independent technical research
Review existing candidates and seek better verified solutions. Provide a concise decision matrix covering maturity, audio evidence, USB Audio + HID support, licensing, cost, procurement and integration effort. Check sources and cite links/versions. Recommend primary + fallback and minimal prototype BOM; explicitly list unknowns and what needs real hardware tests. Avoid duplicating existing code or designing a PCB at this stage.

## 2. Visual exploration
Produce 2–3 distinct, original 2D industrial-design concepts (SVG preferred, PNG preview optional) under design/concepts/. Start with front, rear and side views, including kickstand folded and deployed. Show lever, mic opening, controls, status LED, cable/port, proportions and rough dimensions. Explore pager/telegraph/radio-like aesthetics with restrained functional typography, tactile controls, and a compact silhouette. One option may use warm neutral plus orange, others may vary. Provide a short rationale and tradeoffs per concept. Avoid copying TE's exact case or branding. Do not generate detailed CAD, PCB or production render before owner feedback. Label all dimensions tentative.

## 3. Collaborative review
Offer opinions, challenge assumptions and propose alternatives. Identify tensions: single lever vs separate send button, gesture latency, key safety, mic port placement, stand stability, cable exit and hand noise. End with a small number of decisions for owner review. Do not treat provisional values as fixed.

## Later, only after review
A. Breadboard audio and HID prototype.
B. Confirm interaction and sound tests.
C. Parameterized enclosure and folding stand; 3D print and test.
D. Real daily use; optional custom PCB only if worthwhile.

Prefer short increments, simple documentation and small PRs; no deadlines or scope expansion.
