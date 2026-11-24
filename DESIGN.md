---
name: Plant Biogeography
description: A bilingual lab site drawn as a hypsometric relief map of Anatolia, crossed by the mustard line of the Anatolian Diagonal.
colors:
  diagonal-mustard: "#efb100"
  relief-ink: "#1b2620"
  relief-ink-soft: "#3f4f45"
  survey-paper: "#e1f0c9"
  alpine-stone: "#d6eabb"
  steppe-ochre: "#cbe3a6"
  steppe-ink: "#3a5417"
  foothill-sage: "#bfdc96"
  lowland-green: "#276a3e"
  on-lowland: "#f3f8ee"
  on-lowland-soft: "#d2e6cf"
  map-rule: "#a9c98a"
  band-0-lowland: "#4f9a5c"
  band-1-plain: "#86b866"
  band-2-hill: "#c7e09a"
  band-3-plateau: "#e3e3a0"
  band-4-steppe: "#eec27c"
  band-5-upland: "#d9955f"
  band-6-alpine: "#e1f0c9"
  ink-on-mustard: "#1b1500"
typography:
  display:
    fontFamily: "Archivo, Arial Narrow, Arial, sans-serif"
    fontSize: "min(9.2cqi, 3.6rem)"
    fontWeight: 800
    lineHeight: 0.95
    letterSpacing: "0.02em"
    fontVariation: "\"wdth\" 125"
  headline:
    fontFamily: "Archivo, Arial Narrow, Arial, sans-serif"
    fontSize: "clamp(1.8rem, 4.8vw, 2.9rem)"
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: "0.012em"
    fontVariation: "\"wdth\" 125"
  title-taxon:
    fontFamily: "Source Serif 4, Georgia, Times New Roman, serif"
    fontSize: "clamp(1.55rem, 3.6vw, 2.1rem)"
    fontWeight: 600
    lineHeight: 1.1
  title:
    fontFamily: "Archivo, Arial Narrow, Arial, sans-serif"
    fontSize: "1.05rem"
    fontWeight: 700
    lineHeight: 1.2
    fontVariation: "\"wdth\" 100"
  lede:
    fontFamily: "Source Serif 4, Georgia, Times New Roman, serif"
    fontSize: "1.3rem"
    fontWeight: 400
    lineHeight: 1.45
  body:
    fontFamily: "Source Serif 4, Georgia, Times New Roman, serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Archivo, Arial Narrow, Arial, sans-serif"
    fontSize: "0.9rem"
    fontWeight: 500
    lineHeight: 1.2
  wordmark:
    fontFamily: "Archivo, Arial Narrow, Arial, sans-serif"
    fontSize: "0.82rem"
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: "0.08em"
    fontVariation: "\"wdth\" 125"
  data:
    fontFamily: "Martian Mono, ui-monospace, Menlo, Consolas, monospace"
    fontSize: "0.78rem"
    fontWeight: 400
    letterSpacing: "0.02em"
    fontFeature: "\"tnum\" 1"
rounded:
  swatch: "2px"
  tile: "3px"
  panel: "4px"
  control: "6px"
  toggle: "7px"
  pill: "999px"
spacing:
  gutter: "16px"
  row: "1rem"
  row-loose: "1.25rem"
  annotation: "1.6rem"
  stack: "clamp(1.75rem, 4vw, 2.75rem)"
  band: "clamp(3.5rem, 8vw, 6.5rem)"
  container: "72rem"
components:
  button-solid:
    backgroundColor: "{colors.relief-ink}"
    textColor: "{colors.survey-paper}"
    rounded: "{rounded.control}"
    padding: "0.7rem 1.15rem"
    height: "2.9rem"
  button-line:
    backgroundColor: "transparent"
    textColor: "{colors.relief-ink}"
    rounded: "{rounded.control}"
    padding: "0.7rem 1.15rem"
    height: "2.9rem"
  button-contact:
    backgroundColor: "{colors.diagonal-mustard}"
    textColor: "{colors.ink-on-mustard}"
    rounded: "{rounded.control}"
    padding: "0.7rem 1.15rem"
    height: "2.9rem"
  chip:
    backgroundColor: "transparent"
    textColor: "{colors.steppe-ink}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "0.4rem 0.9rem"
    height: "2.5rem"
  chip-selected:
    backgroundColor: "{colors.relief-ink}"
    textColor: "{colors.survey-paper}"
    rounded: "{rounded.pill}"
  nav-link:
    textColor: "{colors.relief-ink-soft}"
    typography: "{typography.label}"
    rounded: "{rounded.control}"
    padding: "0.45rem 0.7rem"
  nav-link-active:
    backgroundColor: "{colors.alpine-stone}"
    textColor: "{colors.relief-ink}"
  lang-toggle-on:
    backgroundColor: "{colors.relief-ink}"
    textColor: "{colors.survey-paper}"
    typography: "{typography.data}"
    rounded: "{rounded.toggle}"
    height: "2.3rem"
  cartouche:
    backgroundColor: "{colors.survey-paper}"
    textColor: "{colors.relief-ink}"
    rounded: "{rounded.panel}"
    padding: "clamp(1.4rem, 3.5vw, 2.4rem)"
    width: "38rem"
  team-tile:
    backgroundColor: "{colors.band-2-hill}"
    rounded: "{rounded.tile}"
---

# Design System: Plant Biogeography

## Overview

**Creative North Star: "The Relief Map"**

The site is a printed survey map of Anatolia that has come slightly alive. The first screen is a full-bleed hypsometric contour field, its tint bands stepping from lowland green through steppe ochre to pale alpine stone, crossed corner to corner by a dashed mustard line: the Anatolian Diagonal. Everything else is map furniture. The lab's name sits in a bordered cartouche, navigation is the map legend (each link keyed by a tint swatch), study groups are annotations with a location pin and a mono place line, and every section below the hero is laid on one tint band of that legend, so scrolling reads as descending from alpine stone to the lowland green of the contact section.

Density is that of a well-set reference sheet: hairline rules between rows, ruled lists instead of cards, wide-set map lettering for region-scale headings, a quiet serif for reading, and small mono coordinates for data. Colour comes from the land, never from a brand accent; the single exception is mustard, which belongs to the Diagonal and to the one action that ends a visit (writing to the lab). Motion is geological: the land rises once on load and then holds still; it lifts gently around a pointer or finger, and nothing bounces. With reduced motion the map is drawn once and stays still.

Illustration stands in for photography: each team member gets their own small seeded relief tile with a monogram label, which also leaves a slot that a real portrait can replace without redesign.

**Key Characteristics:**
- Hypsometric tint palette; one mustard line for the Anatolian Diagonal.
- Contour linework drawn live on canvas from the same tokens as the CSS.
- Wide-set uppercase map lettering (Archivo at 125% width) for the name and section titles; Source Serif 4 for reading; Martian Mono for coordinates and years.
- Ruled rows and hairline borders instead of cards and shadows.
- Navigation as a legend, buttons as legend keys, sections as tint bands.
- The land rises once, then holds still; a still map under reduced motion.
- Every string exists in Turkish and English with equal visual weight.

## Colors

A hypsometric atlas palette: greens, ochres and stone tints read as elevation, with one saturated mustard reserved for the Diagonal.

### Primary
- **Diagonal Mustard** (#efb100): the Anatolian Diagonal line on the relief (dashed, 3.5px), its legend key, the focus ring, text selection, link underlines, small fills inside line icons, and the contact button on the lowland band.

### Secondary
- **Lowland Green** (#276a3e): the contact section's band and the role line under each person's name. It is the bottom of the map, where the page ends.
- **Steppe Ochre** (#cbe3a6) with **Steppe Ink** (#3a5417): the research band, and the chips and place lines that sit on it.
- **Foothill Sage** (#bfdc96): the people band.

### Tertiary: the hypsometric ramp
- **Band 0 Lowland** (#4f9a5c) through **Band 1 Plain** (#86b866), **Band 2 Hill** (#c7e09a), **Band 3 Plateau** (#e3e3a0), **Band 4 Steppe** (#eec27c), **Band 5 Upland** (#d9955f) to **Band 6 Alpine** (#e1f0c9). These seven steps fill the contour field between isolines (six levels), the team tiles and the legend ramp, and key the navigation (About = alpine, Research = steppe, Publications = plateau, People = hill, Contact = lowland). The canvas reads them from CSS at runtime, so a theme change repaints the map.

### Neutral
- **Survey Paper** (#e1f0c9): page ground, cartouche, the publications band and the join panel.
- **Alpine Stone** (#d6eabb): the about band, the active legend entry and hover fills.
- **Relief Ink** (#1b2620): text, solid buttons, the 1px frame on cartouche, tiles and ruled-list tops, and the footer ground.
- **Relief Ink Soft** (#3f4f45): secondary prose, citations, idle nav links.
- **Map Rule** (#a9c98a): row dividers, header underline, toggle borders.
- **On Lowland** (#f3f8ee) / **On Lowland Soft** (#d2e6cf): text and dividers on the lowland band.
- **Ink on Mustard** (#1b1500): text placed on mustard (selection, contact button).
- Contour lines are Relief Ink at 34% (rgba(27,38,32,.34)); thicker index contours at the 3rd and 5th levels.

Each section owns one colour, and the same colour is the key beside its name in the navigation (and fills the active link): About pistachio #dcedc3, Research sand #f6dcae, Publications butter #f1ecb3, People light green #c7e09a, Contact peach #f2c9a6. The site is light-only by decision, on a pistachio palette whose lightest colour is pale pistachio (#e1f0c9), with no white or cream grounds; the footer is full pistachio (#93c572): it keeps the same bright daylight palette even when the visitor's device is in dark mode, because the night version read as gloomy. The contact band is a pale lowland green (#a9d184) with ink text, and the footer sits on the foothill tint.

### Named Rules
**The One Line Rule.** Mustard is the Diagonal. It appears as the dashed line, its legend key, focus and selection, and the single action that ends a visit. It is never a section background, a heading colour or decoration.

**The Land Colour Rule.** Every surface colour is an elevation band. A new section takes the next tint from the ramp; it never introduces a hue the map does not have.

## Typography

**Display Font:** Archivo (with Arial Narrow, Arial), variable width 62 to 125, weight 400 to 800
**Body Font:** Source Serif 4 (with Georgia, Times New Roman), optical sizing on
**Label/Mono Font:** Martian Mono (with ui-monospace, Menlo, Consolas)

**Character:** Wide-set grotesque capitals do the work of map lettering across a region; a calm text serif carries the science; a mono gives coordinates, years and the e-mail address the look of surveyed data.

### Hierarchy
- **Display** (800, min(9.2cqi, 3.6rem) sized to the cartouche, 0.95, uppercase, 125% width): the lab name in the hero cartouche only.
- **Headline** (700, clamp(1.8rem, 4.8vw, 2.9rem), 1.05, 125% width, max 22ch): one per section, sentence case.
- **Title, taxon** (Source Serif 4 600 italic, clamp(1.55rem, 3.6vw, 2.1rem), 1.1): study-group names; genus and species stay italic, common words set upright.
- **Title** (Archivo 700, 1.05rem, normal width): method names and team member names. The PI's name steps up to the taxon size.
- **Lede** (Source Serif 4 400, 1.3rem, 1.45, max 40ch): the hero thesis and the first line of a section.
- **Body** (Source Serif 4 400, 1.0625rem, 1.6, prose max 66ch): reading text; publication titles at 1.08rem 600, max 70ch.
- **Label** (Archivo 500 to 600, 0.85 to 0.98rem): nav, chips, buttons, roles, small headings in the contact block.
- **Wordmark** (Archivo 700, 0.82rem, 0.08em, uppercase, 125% width): the two-line brand in the header.
- **Data** (Martian Mono 400, 0.78rem, 0.02em, tabular numerals): coordinates, the legend strip, study place lines, footer. Years in publications at 0.95rem; the e-mail address at clamp(1rem, 3.6vw, 1.35rem).

### Named Rules
**The Map Lettering Rule.** Width, not weight alone, makes a heading: region-scale text is Archivo at 125% width. Small names (methods, members) return to normal width so the wide setting stays rare.

**The Italic Taxon Rule.** Scientific names are always italic Source Serif, in titles, citations and prose alike.

## Layout

One centred container (max 72rem) with a 16px minimum side gutter that respects safe-area insets. The hero is full-bleed (clamp(36rem, 88svh, 54rem) tall), the cartouche pinned left inside the container and a translucent legend strip pinned along its bottom edge. Below it, each section is a full-width tint band with vertical padding of clamp(3.5rem, 8vw, 6.5rem) and an internal stack gap of clamp(1.75rem, 4vw, 2.75rem).

Content is organised as ruled lists: a 1px ink rule opens a list and 1px map-rule lines separate rows (row padding 1rem to 1.6rem). Two-column splits (about: 1.3fr / 1fr; contact: 1.1fr / 1fr) and a two-column study grid sit beside a five-column team grid.

Breakpoints:
- **980px**: team grid to three columns; about and contact to one column.
- **860px**: navigation collapses into a sheet under the header; the legend entries become full-width rows with larger keys and an e-mail button at the end.
- **760px**: the hero cartouche drops to the bottom of the viewport above the legend and goes full width; study grid to one column; chips scroll horizontally edge to edge with snap; team to two columns; publication years stack above titles; action buttons fill the row.
- **420px**: smaller wordmark; PI tile stacks above the bio.

The sticky header offsets anchor scrolling (scroll-padding-top 4.75rem). Hover styles apply only where a fine pointer exists.

## Elevation & Depth

The system is flat. There are no shadows anywhere; depth is the map's own: tint bands read as elevation and contour lines give relief. Layering is shown by a 1px ink frame (cartouche, tiles, monogram labels, the join panel) on top of the field. The only translucent surfaces are the two pieces of map furniture that float over content: the sticky header (paper at 94%, 10px backdrop blur, slight saturation) and the hero legend strip (paper at 90%).

### Named Rules
**The Printed Map Rule.** Nothing casts a shadow. A surface that needs to sit above the map gets a 1px ink frame and paper fill, as a cartouche does on a printed sheet.

## Shapes

Corners are nearly square, as on printed map furniture: 2px on legend keys and monogram labels, 3px on tiles, 4px on the cartouche and panels, 6px on buttons and nav entries, 7px on the language toggle and menu button. Pills (999px) are reserved for the two kinds of tag: research filter chips and hotspot labels. Lines carry the form language: hairline borders, a 3px dashed mustard Diagonal (12/9 dash on canvas), and 1.6px stroke line icons with small mustard fills. Icons are drawn as inline SVG in the same contour-and-pin vocabulary (phylogeny tree, relief rings, herbarium sheet, location pin).

### Navigation and section structure

Top navigation: About, Research (with a submenu: Main research topics, Projects, Team publications, Theses), People, Contact. On desktop the submenu opens under its trigger from the top-left (opacity + 0.97 scale, 150–180 ms, strong ease-out), on hover for precise pointers and on click/focus for everyone; Escape and outside clicks close it. In the phone sheet the sub-items are always listed, indented under Research. Each subsection has its own band colour, shown as its key in the menu: topics sand #f6dcae, projects light sand #f9e6c3, team publications butter #f1ecb3, theses pale butter #f6f2c8. In Turkish the lab name renders as "Bitki Biyocoğrafyası" in the brand, hero, footer and document title.

### Hero actions

The two opening actions sit outside the title card, on the relief, as map-label pills: "See our research" is an ink pill with a mustard arrow disc that nudges down on hover; "Contact" is a frosted paper pill with an ink envelope disc. They stack full width on narrow phones.

### Boxes and motion

Few framed boxes: figures (stats, project facts) stand open, divided by hairlines; navigation keys are small dots and the active link gets a drawn ink underline; profile links are underlined text links; portraits and the photo use soft 10–12px corners without frames. Motion is small and compositor-only: a mustard rule draws under each section heading the first time it enters view, stat figures count up once, newly revealed publications rise in with a short stagger, and portraits, the photo and arrows respond on hover only for precise pointers. Reduced motion turns all of it off.

### Palette (Japanese traditional colours, pastel)

The page now uses pale versions of traditional Japanese colours and no dark or saturated greens: kinari/shironeri paper #f7f3e8, wakaba (young leaf) #e8f1d8 for About, kaki (persimmon) #f8dcc8 for research topics, wasurenagusa (forget-me-not) #dde9f3 for projects, yamabuki #f8ecc0 for team publications, mizu (water) #d9eeee for theses, sakura #f7e1e4 for people, sango (coral) #f6d5c8 for contact, footer #ead9cd. Text is sumi #2b2b2b with warm grey #55504a; role labels use ai (indigo) #3b5f87; the accent is yamabuki-iro #f8b500. The relief uses pastel hypsometric tints (#b5d9a8 → #f7f3e8) with softened hillshade.

### Field photographs

Five lab field photographs, always shown whole (square, no cropping) so the plant or the habitat reads in full. Plant photos carry a small frosted genus label (Phyllolepidium in About, Noccaea beside the featured project, Heldreichia beside the theses). Two habitat plates sit between sections on the paper ground, photo and text side by side and alternating sides: the Heldreichia habitat (limestone scree at the edge of cedar forest) before Research, and the Noccaea and Phyllolepidium habitat (high limestone cirque) before Team publications.

## Components

### Buttons
Legend keys: plain, framed, unambiguous.
- **Shape:** gently squared (6px), 1px ink border, min height 2.9rem, padding 0.7rem 1.15rem, Archivo 600 at 0.98rem, optional 18px line icon.
- **Solid:** ink fill, paper text. Hover mixes 14% of Band 0 into the ink.
- **Line:** transparent, ink text and border. Hover adds an 8% ink wash.
- **Contact (on the lowland band):** solid becomes mustard with ink-on-mustard text (hover #ffc928); line takes the soft-lowland border.
- **Press:** scale 0.97 over 120ms on the ease-out curve. Focus: 2px mustard outline, 3px offset.

### Chips
- **Style:** pill, 1px steppe-ink border, steppe-ink text, transparent, min height 2.5rem; used as the study-group filter on the steppe band.
- **State:** selected is ink fill with paper text (aria-pressed); hover is a 12% steppe-ink wash. Hotspot tags are the static sibling: pill, 1px ink border, no states.

### Navigation (the map legend)
- **Desktop:** a row of entries in the sticky header, each a 0.7rem tint swatch (2px corners, rule border) plus an Archivo 500 label in soft ink. The section in view becomes active: stone fill, full ink.
- **Language toggle:** a bordered TR / EN segmented control in Martian Mono; the active language is ink-filled.
- **Phone:** a 44px menu button opens the legend as a sheet below the header: full-width rows with 1rem swatches, rule dividers, and a full-width e-mail button. Escape and link taps close it.

### Cartouche (signature)
The hero title block: paper fill, 1px ink frame, 4px corners, max 38rem, containing the display name, the place line, the one-line thesis and the two actions. It settles into place on load (14px rise over 1.1s).

### Relief field and legend strip (signature)
A canvas shaded-relief map: a continuous hypsometric tint (b0 to b6) with north-west hillshading and faint isolines. A ridged mountain belt follows a schematic, gently bending Anatolian Diagonal from the north-east to the Gulf of İskenderun, with real places marked in their true order along it (Gümüşhane, Erzincan, Malatya, Kahramanmaraş; fewer on phones). The land rises once on load, then holds still and lifts within roughly 90px of the pointer. The Diagonal is a dashed mustard line on a paper halo with an uppercase Archivo label. Below it a mono legend strip carries the tint ramp, the dashed Diagonal key, "Schematic relief" and the lab's coordinates.

### Study annotation
A ruled entry on the steppe band: italic taxon title, a description in soft ink (max 52ch), and a mono place line in steppe ink led by a 14px location pin, with the source citation on its own line beneath. Rows divide with steppe ink at 35%.

### Publication row
Year in Martian Mono in a 5.5rem column, then title (600), authors and journal in soft ink, DOI links that wrap anywhere. Profile links follow as line buttons with an outward-arrow icon.

### Team tile
A 4:5 tile with a 1px ink frame and 3px corners holding a relief generated from the person's name, with a paper monogram label in wide Archivo at the lower left. The role line sits under the name in lowland green. A real photograph takes the same frame.

## Do's and Don'ts

### Do:
- **Do** pick section and surface colours from the hypsometric ramp, in descending order down the page, ending on lowland green.
- **Do** keep mustard (#efb100) for the Diagonal, focus, selection, link underlines and the final contact action.
- **Do** set region-scale headings in Archivo at 125% width; return to normal width for names and small titles.
- **Do** separate content with 1px rules: an ink rule to open a list, map-rule lines between rows.
- **Do** put coordinates, years, place lines and the e-mail address in Martian Mono with tabular numerals.
- **Do** give every string a Turkish and an English version at the same size and weight.
- **Do** keep motion slow and rare (one rise on load, lift under the pointer, settle on the ease-out curve) and render a still map under reduced motion.
- **Do** draw new icons as inline 1.6px line SVGs in the contour, pin and specimen vocabulary, with at most a small mustard fill.

### Don't:
- **Don't** add drop shadows, glows or floating cards; frame with 1px ink instead.
- **Don't** use mustard as a fill for sections or headings, or as small text on the light-mode lowland band (it reaches only 4.38:1 there).
- **Don't** introduce a hue that is not an elevation band, a neutral or the Diagonal.
- **Don't** let anything bounce, spring or overshoot.
- **Don't** use stock photographs as the lab's own; use relief tiles until real photographs exist.
