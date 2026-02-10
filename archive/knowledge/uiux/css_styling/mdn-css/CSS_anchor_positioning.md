# CSS anchor positioning

Source: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_anchor_positioning

---

# CSS anchor positioning

The **CSS anchor positioning** module defines features that allow you to tether elements together. Certain elements are defined as **anchor elements**; **anchor-positioned elements** can then have their size and position set based on the size and location of the anchor elements to which they are bound.

In addition, the specification provides CSS-only mechanisms to:

- Specify a set of alternative positions for an anchored element; when the default rendering position causes it to overflow its containing block and/or be rendered offscreen, the browser will try rendering the anchored element in the alternative positions instead.
- Declare conditions under which anchor-positioned elements should be hidden, in situations where it is not appropriate to tether them to anchor elements.

## [Reference](#reference)

### [Properties](#properties)

- [`anchor-scope`](/en-US/docs/Web/CSS/Reference/Properties/anchor-scope)
- [`anchor-name`](/en-US/docs/Web/CSS/Reference/Properties/anchor-name)
- [`position-anchor`](/en-US/docs/Web/CSS/Reference/Properties/position-anchor)
- [`position-area`](/en-US/docs/Web/CSS/Reference/Properties/position-area)
- [`position-try-fallbacks`](/en-US/docs/Web/CSS/Reference/Properties/position-try-fallbacks)
- [`position-try-order`](/en-US/docs/Web/CSS/Reference/Properties/position-try-order)
- [`position-try`](/en-US/docs/Web/CSS/Reference/Properties/position-try) shorthand
- [`position-visibility`](/en-US/docs/Web/CSS/Reference/Properties/position-visibility)

### [At-rules and descriptors](#at-rules_and_descriptors)

- [`@position-try`](/en-US/docs/Web/CSS/Reference/At-rules/@position-try)

### [Functions](#functions)

- [`anchor()`](/en-US/docs/Web/CSS/Reference/Values/anchor)
- [`anchor-size()`](/en-US/docs/Web/CSS/Reference/Values/anchor-size)

### [Data types and values](#data_types_and_values)

- [`anchor-center`](/en-US/docs/Web/CSS/Guides/Anchor_positioning/Using#centering_on_the_anchor_using_anchor-center)
- [`<anchor-side>`](/en-US/docs/Web/CSS/Reference/Values/anchor#anchor-side)
- [`<anchor-size>`](/en-US/docs/Web/CSS/Reference/Values/anchor-size#anchor-size)
- [`<position-area>`](/en-US/docs/Web/CSS/Reference/Values/position-area_value)
- [`<try-size>`](/en-US/docs/Web/CSS/Reference/Properties/position-try-order#try-size)
- [`<try-tactic>`](/en-US/docs/Web/CSS/Reference/Properties/position-try-fallbacks#try-tactic)

### [HTML attributes](#html_attributes)

- [`anchor`](/en-US/docs/Web/HTML/Reference/Global_attributes/anchor) 
  Non-standard

### [Interfaces](#interfaces)

- [`CSSPositionTryDescriptors`](/en-US/docs/Web/API/CSSPositionTryDescriptors)
- [`CSSPositionTryRule`](/en-US/docs/Web/API/CSSPositionTryRule)
- [`HTMLElement.anchorElement`](/en-US/docs/Web/API/HTMLElement/anchorElement) 
  Non-standard

## [Guides](#guides)

[Using CSS anchor positioning](/en-US/docs/Web/CSS/Guides/Anchor_positioning/Using)
:   An introductory guide to fundamental anchor positioning concepts, including associating, positioning, and sizing elements relative to their anchor.

[Fallback options and conditional hiding for overflow](/en-US/docs/Web/CSS/Guides/Anchor_positioning/Try_options_hiding)
:   A guide to the mechanisms CSS anchor positioning provides to prevent anchor-positioned elements from overflowing their containing elements or the viewport, including position try fallback options and conditionally hiding elements.

## [Related concepts](#related_concepts)

- [CSS logical properties and values](/en-US/docs/Web/CSS/Guides/Logical_properties_and_values) module:
  - [`inset-block-start`](/en-US/docs/Web/CSS/Reference/Properties/inset-block-start)
  - [`inset-block-end`](/en-US/docs/Web/CSS/Reference/Properties/inset-block-end)
  - [`inset-inline-start`](/en-US/docs/Web/CSS/Reference/Properties/inset-inline-start)
  - [`inset-inline-end`](/en-US/docs/Web/CSS/Reference/Properties/inset-inline-end)
  - [`inset-block`](/en-US/docs/Web/CSS/Reference/Properties/inset-block)
  - [`inset-inline`](/en-US/docs/Web/CSS/Reference/Properties/inset-inline)
  - [`inset`](/en-US/docs/Web/CSS/Reference/Properties/inset) shorthand
  - [`inline-size`](/en-US/docs/Web/CSS/Reference/Properties/inline-size)
  - [`min-block-size`](/en-US/docs/Web/CSS/Reference/Properties/min-block-size)
  - [`min-inline-size`](/en-US/docs/Web/CSS/Reference/Properties/min-inline-size)
  - [`block-size`](/en-US/docs/Web/CSS/Reference/Properties/block-size)
  - [`max-block-size`](/en-US/docs/Web/CSS/Reference/Properties/max-block-size)
  - [`max-inline-size`](/en-US/docs/Web/CSS/Reference/Properties/max-inline-size)
  - [`margin-block`](/en-US/docs/Web/CSS/Reference/Properties/margin-block)
  - [`margin-block-end`](/en-US/docs/Web/CSS/Reference/Properties/margin-block-end)
  - [`margin-block-start`](/en-US/docs/Web/CSS/Reference/Properties/margin-block-start)
  - [`margin-inline`](/en-US/docs/Web/CSS/Reference/Properties/margin-inline)
  - [`margin-inline-end`](/en-US/docs/Web/CSS/Reference/Properties/margin-inline-end)
  - [`margin-inline-start`](/en-US/docs/Web/CSS/Reference/Properties/margin-inline-start)
  - [Inset properties](/en-US/docs/Glossary/Inset_properties) glossary term
- [CSS positioned layout](/en-US/docs/Web/CSS/Guides/Positioned_layout) module:
  - [`top`](/en-US/docs/Web/CSS/Reference/Properties/top)
  - [`left`](/en-US/docs/Web/CSS/Reference/Properties/left)
  - [`bottom`](/en-US/docs/Web/CSS/Reference/Properties/bottom)
  - [`right`](/en-US/docs/Web/CSS/Reference/Properties/right)
- [CSS box model](/en-US/docs/Web/CSS/Guides/Box_model) module:
  - [`width`](/en-US/docs/Web/CSS/Reference/Properties/width)
  - [`height`](/en-US/docs/Web/CSS/Reference/Properties/height)
  - [`min-width`](/en-US/docs/Web/CSS/Reference/Properties/min-width)
  - [`min-height`](/en-US/docs/Web/CSS/Reference/Properties/min-height)
  - [`max-width`](/en-US/docs/Web/CSS/Reference/Properties/max-width)
  - [`max-height`](/en-US/docs/Web/CSS/Reference/Properties/max-height)
  - [`margin`](/en-US/docs/Web/CSS/Reference/Properties/margin)
  - [`margin-bottom`](/en-US/docs/Web/CSS/Reference/Properties/margin-bottom)
  - [`margin-left`](/en-US/docs/Web/CSS/Reference/Properties/margin-left)
  - [`margin-right`](/en-US/docs/Web/CSS/Reference/Properties/margin-right)
  - [`margin-top`](/en-US/docs/Web/CSS/Reference/Properties/margin-top)
- [CSS box alignment](/en-US/docs/Web/CSS/Guides/Box_alignment) module:
  - [`align-items`](/en-US/docs/Web/CSS/Reference/Properties/align-items)
  - [`align-self`](/en-US/docs/Web/CSS/Reference/Properties/align-self)
  - [`justify-items`](/en-US/docs/Web/CSS/Reference/Properties/justify-items)
  - [`justify-self`](/en-US/docs/Web/CSS/Reference/Properties/justify-self)
  - [`place-items`](/en-US/docs/Web/CSS/Reference/Properties/place-items)
  - [`place-self`](/en-US/docs/Web/CSS/Reference/Properties/place-self)

## [Specifications](#specifications)

| Specification |
| --- |
| [CSS Anchor Positioning Module Level 1](https://drafts.csswg.org/css-anchor-position-1/) |

## [See also](#see_also)

- [CSS scroll anchoring](/en-US/docs/Web/CSS/Guides/Scroll_anchoring) module
- [Learn: CSS positioning](/en-US/docs/Learn_web_development/Core/CSS_layout/Positioning)
- [CSS logical properties and values](/en-US/docs/Web/CSS/Guides/Logical_properties_and_values) module
- [Learn: Sizing items in CSS](/en-US/docs/Learn_web_development/Core/Styling_basics/Sizing)

## Help improve MDN

Was this page helpful to you?

Yes

No

[Learn how to contribute](/en-US/docs/MDN/Community/Getting_started)

This page was last modified on Jan 7, 2026 by [MDN contributors](/en-US/docs/Web/CSS/Guides/Anchor_positioning/contributors.txt).

[View this page on GitHub](https://github.com/mdn/content/blob/main/files/en-us/web/css/guides/anchor_positioning/index.md?plain=1 "Folder: en-us/web/css/guides/anchor_positioning (Opens in a new tab)") â¢ [Report a problem with this content](https://github.com/mdn/content/issues/new?template=page-report.yml&mdn-url=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FGuides%2FAnchor_positioning&metadata=%3C%21--+Do+not+make+changes+below+this+line+--%3E%0A%3Cdetails%3E%0A%3Csummary%3EPage+report+details%3C%2Fsummary%3E%0A%0A*+Folder%3A+%60en-us%2Fweb%2Fcss%2Fguides%2Fanchor_positioning%60%0A*+MDN+URL%3A+https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FGuides%2FAnchor_positioning%0A*+GitHub+URL%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fblob%2Fmain%2Ffiles%2Fen-us%2Fweb%2Fcss%2Fguides%2Fanchor_positioning%2Findex.md%0A*+Last+commit%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fcommit%2F8300697ca75ca1e77175912110d4fe9ef48cb0bb%0A*+Document+last+modified%3A+2026-01-07T12%3A06%3A40.000Z%0A%0A%3C%2Fdetails%3E "This will take you to GitHub to file a new issue.")