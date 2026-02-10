# CSS view transitions

Source: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_view_transitions

---

# CSS view transitions

The **CSS view transitions** module defines the behavior of the [View Transition API](/en-US/docs/Web/API/View_Transition_API), which allows developers to create animated transitions between different states within a document and across documents. This module also defines the CSS properties and pseudo-elements for styling these transitions.

## [Reference](#reference)

### [Properties](#properties)

- [`view-transition-class`](/en-US/docs/Web/CSS/Reference/Properties/view-transition-class)
- [`view-transition-name`](/en-US/docs/Web/CSS/Reference/Properties/view-transition-name)

### [At-rules and descriptors](#at-rules_and_descriptors)

- [`@view-transition`](/en-US/docs/Web/CSS/Reference/At-rules/@view-transition)
  - [`navigation`](/en-US/docs/Web/CSS/Reference/At-rules/@view-transition#navigation) descriptor

### [Selectors and pseudo-elements](#selectors_and_pseudo-elements)

- [`:active-view-transition`](/en-US/docs/Web/CSS/Reference/Selectors/:active-view-transition)
- [`:active-view-transition-type()`](/en-US/docs/Web/CSS/Reference/Selectors/:active-view-transition-type)
- [`::view-transition`](/en-US/docs/Web/CSS/Reference/Selectors/::view-transition)
- [`::view-transition-image-pair()`](/en-US/docs/Web/CSS/Reference/Selectors/::view-transition-image-pair)
- [`::view-transition-group()`](/en-US/docs/Web/CSS/Reference/Selectors/::view-transition-group)
- [`::view-transition-new()`](/en-US/docs/Web/CSS/Reference/Selectors/::view-transition-new)
- [`::view-transition-old()`](/en-US/docs/Web/CSS/Reference/Selectors/::view-transition-old)

### [Interfaces](#interfaces)

- [`CSSViewTransitionRule`](/en-US/docs/Web/API/CSSViewTransitionRule)
- [`ViewTransition`](/en-US/docs/Web/API/ViewTransition)
  - [`ViewTransition.skipTransition()`](/en-US/docs/Web/API/ViewTransition/skipTransition) method
  - [`ViewTransition.updateCallbackDone`](/en-US/docs/Web/API/ViewTransition/updateCallbackDone)
  - [`ViewTransition.ready`](/en-US/docs/Web/API/ViewTransition/ready)
  - [`ViewTransition.finished`](/en-US/docs/Web/API/ViewTransition/finished)
- [`Document.startViewTransition()`](/en-US/docs/Web/API/Document/startViewTransition) method

## [Guides](#guides)

[Using the View Transition API](/en-US/docs/Web/API/View_Transition_API/Using)
:   Explains how to create view transitions and customize transition animations, including manipulating active view transitions.

## [Related concepts](#related_concepts)

- [`pagereveal`](/en-US/docs/Web/API/PageRevealEvent "pagereveal") event
- [`pageswap`](/en-US/docs/Web/API/PageSwapEvent "pageswap") event
- [`Document.visibilityState`](/en-US/docs/Web/API/Document/visibilityState)
- [CSS animations](/en-US/docs/Web/CSS/Guides/Animations) module

  - [`animation`](/en-US/docs/Web/CSS/Reference/Properties/animation)
  - [`@keyframes`](/en-US/docs/Web/CSS/Reference/At-rules/@keyframes)
  - [`CSSKeyframesRule`](/en-US/docs/Web/API/CSSKeyframesRule)
  - [`CSSStyleRule`](/en-US/docs/Web/API/CSSStyleRule)
  - [Web animations API](/en-US/docs/Web/API/Web_Animations_API)
- [CSS transforms](/en-US/docs/Web/CSS/Guides/Transforms) module

  - [`transform`](/en-US/docs/Web/CSS/Reference/Properties/transform)
  - [`<transform-function>`](/en-US/docs/Web/CSS/Reference/Values/transform-function)

## [Specifications](#specifications)

| Specification |
| --- |
| [CSS View Transitions Module Level 1](https://drafts.csswg.org/css-view-transitions-1/) |
| [CSS View Transitions Module Level 2](https://drafts.csswg.org/css-view-transitions-2/) |

## [See also](#see_also)

- [Pseudo-elements](/en-US/docs/Web/CSS/Reference/Selectors/Pseudo-elements)
- [Functional pseudo-classes](/en-US/docs/Web/CSS/Reference/Selectors/Pseudo-classes#functional_pseudo-classes)
- [Learn: Pseudo-classes and pseudo-elements](/en-US/docs/Learn_web_development/Core/Styling_basics/Pseudo_classes_and_elements)

## Help improve MDN

Was this page helpful to you?

Yes

No

[Learn how to contribute](/en-US/docs/MDN/Community/Getting_started)

This page was last modified on Nov 7, 2025 by [MDN contributors](/en-US/docs/Web/CSS/Guides/View_transitions/contributors.txt).

[View this page on GitHub](https://github.com/mdn/content/blob/main/files/en-us/web/css/guides/view_transitions/index.md?plain=1 "Folder: en-us/web/css/guides/view_transitions (Opens in a new tab)") â¢ [Report a problem with this content](https://github.com/mdn/content/issues/new?template=page-report.yml&mdn-url=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FGuides%2FView_transitions&metadata=%3C%21--+Do+not+make+changes+below+this+line+--%3E%0A%3Cdetails%3E%0A%3Csummary%3EPage+report+details%3C%2Fsummary%3E%0A%0A*+Folder%3A+%60en-us%2Fweb%2Fcss%2Fguides%2Fview_transitions%60%0A*+MDN+URL%3A+https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FGuides%2FView_transitions%0A*+GitHub+URL%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fblob%2Fmain%2Ffiles%2Fen-us%2Fweb%2Fcss%2Fguides%2Fview_transitions%2Findex.md%0A*+Last+commit%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fcommit%2F85fccefc8066bd49af4ddafc12c77f35265c7e2d%0A*+Document+last+modified%3A+2025-11-07T15%3A58%3A06.000Z%0A%0A%3C%2Fdetails%3E "This will take you to GitHub to file a new issue.")