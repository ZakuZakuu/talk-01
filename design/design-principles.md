# Design principles worth stealing

Date: 2026-11-25 · Status: **working notes. A checklist for us, not a theory.**

## Why this exists

The owner's verdict on round 2: three concepts that were all "a bit short of something". They did not catch the eye, compared with Teenage Engineering (TE), Nothing or Braun. The owner also noted that TE products are simple at a glance but quite intricate up close. This note collects what those designers say about their own method, turns it into a checklist, and scores round 2 against it.

I am an assistant working from flat vector sketches. I cannot judge taste for the owner. What I can do is make the work **more varied, more bold and more detailed**, and let the owner's taste pick.

## What the sources say

Evidence level: **[interview]** = said by the designer or founder in a published interview I read; **[analysis]** = a third party's reading; **[inferred]** = my reading.

### Teenage Engineering
- The founder says the products are not the whole business, and describes making what a ten-year-old would find fascinating. **[interview, [Highsnobiety](https://www.highsnobiety.com/p/teenage-engineering-interview/)]**
- The process is hands-on: when someone says "wouldn't it be cool if...", the founder builds a model at home (wood shop, 3D printers, sewing machine) and brings it in. Out of around a hundred prototypes, **one person decides** which ships; a designer reports a verdict like "No, that's ugly" after weeks of work. No spreadsheets or customer surveys. **[interview, same source]**
- The products pair minimalist industrial design with a childlike sense of humour (a cow on the OP-1 interface, a tape dispenser, a vinyl cutter). **[interview, same source]**
- Constraint is treated as the aesthetic: a tiny palette (orange, black, white, aluminium, screen green), monospaced type, exposed screws and pictograms. The pictogram influence is described as post-Bauhaus (Ulm). **[analysis, [Blake Crosley](https://blakecrosley.com/guides/design/teenage-engineering); secondary, so treat specifics as unverified]**
- Another interview exists on SFMOMA ([link](https://www.sfmoma.org/read/stay-curious-stay-naive-an-interview-with-teenage-engineering-jesper-kouthoofd/)); the page blocked my fetch, so I only saw a search excerpt: he sets restrictions when he designs. **[excerpt only]**

### Nothing / CMF
- The design director says the goal is hardware that is **instantly recognisable**, the product should feel "almost like a logo". Screws and components are treated as **graphic features**; the transparent back echoes the layout of older electronics. **[interview, [Creative Bloq](https://www.creativebloq.com/design/product-design/why-nothing-designs-its-phones-like-logos)]**
- The team trusts its gut because data "leads to the same place as everyone else", takes 1970s products as seriously as new renders, and keeps old tech (Game Boy Color, Casio keyboards) in the studio. **[interview, [Dezeen](https://www.dezeen.com/2024/02/20/nothing-tech-smartphone-design-adam-bates-interview/)]**
- A studio saying: **"God can see it"** (about details). They 3D-print over-scaled models to inspect every nook, and a simple product can go through 50 to 100 prototypes laid out on a table, next to colour sources like a lipstick or a deck of cards. The colour palette is deliberately narrow and expanded slowly. **[interview, [Wallpaper](https://www.wallpaper.com/tech/nothing-design-team-interview)]**

### Braun / Dieter Rams
- Rams's ten principles are widely summarised; the ones that matter here: **as little design as possible**, **thorough down to the last detail**, **honest**, **unobtrusive**. [[IxDF summary](https://ixdf.org/literature/article/dieter-rams-10-timeless-commandments-for-good-design)] The T3 pocket radio is described as a plain box with a dial and speaker openings; one less reliable blog says the dial sits on the side because the thumb reaches it. [[Buxton Collection](https://microsoft.com/buxtoncollection/detail.aspx?id=179)]

## The checklist (our working "skill")

1. **Logo test.** Fill the shape with solid black. Can you recognise it, and tell it from the others? If not, the silhouette is not done.
2. **One hero, oversized, a little absurd.** The reference's slanted lever is the hero. Pick one control or feature and exaggerate its scale or its angle, rather than polishing five features equally.
3. **Three distances.** At **3 m**: silhouette and colour only. At **30 cm**: the hero plus two or three big features. At **3 cm**: micro-details (small type, numbers, pictograms, screw heads, seams, tiny holes). Simple-looking products are rich at 3 cm. Round 2 mostly had distances 1 and 2.
4. **One signal colour for what you touch.** Neutral body, one loud colour used *only* on the parts that move, plus at most one material accent (translucent, metal). Three or four colours in total.
5. **Show the structure.** Screws, seams, holes and cable channels are ornament, arranged on a grid. "God can see it": nothing is accidental.
6. **A small vocabulary, repeated.** Choose one angle, one radius family and one shape motif (circle, dot, 30° cut) and repeat them. This is what makes a complicated object look calm.
7. **Honest, small labels.** Monospaced or stencil type, pictograms, numbers. Labels are decoration and instruction at once.
8. **A little humour.** Names, tiny status text, a surprising detail. Personality beats polish.
9. **Make it physical early.** Print rough models, hold them, line them up. Many options, one decider.
10. **Constraint is the engine.** Decide what to leave out first.

## Round 2 scored against the checklist (honest)

| Rule | D Dial | E Armed | F Handset | Comment |
|---|---|---|---|---|
| 1 Logo test | weak | weak | medium | D and E are rounded rectangles; F has a flared outline |
| 2 Hero, oversized | medium | medium | weak | D's wheel is large but not exaggerated; no strong angle anywhere |
| 3 Three distances | 1-2 only | 1-2 only | 1-2 only | very little 3 cm detail |
| 4 Signal colour | ok | ok | ok | orange on the movable parts; palettes were arbitrary |
| 5 Show the structure | weak | weak | weak | the bay and feet were drawn but not used as ornament |
| 6 Repeated motif | weak | weak | weak | each part had its own shape language |
| 7 Honest small labels | ok | ok | ok | labels existed but not as a design layer |
| 8 Humour | none | none | none | |
| 9 Physical early | not yet | not yet | not yet | the mock-up idea was only suggested |
| 10 Constraint | ok | ok | ok | clear "left out" lists, but too safe |

Verdict: the structure was coherent, the **look was not distinctive**. I read "avoid a random mash-up" as "stay restrained", and restraint without a strong shape or detail layer just looks generic.

## What changes now

- **Shape first.** Round 3 is a *silhouette lineup*: six very different shapes, each with a hero, so the owner can run the logo test by gut ([`concepts/round-3/`](concepts/round-3/README.md)).
- **Apply the owner's new constraints:** the back cover is a **small hatch**, not the whole back; the stand is a **small U**, or **the hatch itself is the stand**.
- **Details come after choosing.** Once one or two shapes are picked, develop them at the three distances with a motif, a label layer, exposed structure and small humour.
- **Physical mocks** of the favourite shape to check the hand, as TE and Nothing do.

## What I need from the owner

Taste, not design skill: which shapes attract or repel, and any objects (retro or modern) whose look you love. A short description or a link is enough; I will not copy or redistribute their images.
