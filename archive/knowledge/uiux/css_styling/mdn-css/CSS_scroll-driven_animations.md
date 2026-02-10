# CSS scroll-driven animations

Source: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scroll-driven_animations

---

# CSS scroll-driven animations

The **CSS scroll-driven animations** module provides functionality that builds on the [CSS animations module](/en-US/docs/Web/CSS/Guides/Animations) and [Web Animations API](/en-US/docs/Web/API/Web_Animations_API). It allows you to animate property values along a scroll-based timeline rather than the default time-based document timeline. This means that you can animate an element by scrolling the element, its scroll container, or its root element, rather than just by the passing of time.

## [Scroll-driven animations in action](#scroll-driven_animations_in_action)

You can define the scroller that controls the animation either by naming the animation or with the [`scroll()`](/en-US/docs/Web/CSS/Reference/Properties/animation-timeline/scroll) function.

```
<main>
  <div></div>
</main>
```

css

```
main {
  scroll-timeline: --main-timeline;
}

div {
  animation: background-animation linear;
  animation-timeline: scroll(nearest inline);
}

div::after {
  animation: shape-animation linear;
  animation-timeline: --main-timeline;
}
```

```
@layer animations {
  @keyframes background-animation {
    0% {
      background-color: palegoldenrod;
    }
    100% {
      background-color: magenta;
    }
  }
  @keyframes shape-animation {
    0% {
      left: 0;
      top: 0;
      background-color: black;
    }
    50% {
      top: calc(100% - var(--elSize));
      left: calc(50% - var(--elSize));
      background-color: red;
    }
    100% {
      left: calc(100vw - var(--elSize));
      top: 0;
      rotate: 1800deg;
      background-color: white;
    }
  }
}

@layer page-setup {
  :root {
    --elSize: 50px;
  }
  main {
    height: 90vh;
    overflow: scroll;
    border: 1px solid;
    margin: 5vh auto;
  }
  div {
    height: 400vh;
    width: 400vw;
  }
  div::after {
    content: "";
    border: 1px solid red;
    height: var(--elSize);
    width: var(--elSize);
    position: absolute;
    border-radius: 20px;
    corner-shape: superellipse(-4);
  }
}

@layer no-support {
  @supports not (scroll-timeline: --main-timeline) {
    body::before {
      content: "Your browser doesn't support scroll-driven animations.";
      background-color: wheat;
      display: block;
      text-align: center;
    }
  }
}
```

Scroll the element in the inline direction to see its background color change. Scroll it vertically to see the generated content move, spin, and change colors.

## [Reference](#reference)

### [Properties](#properties)

- [`animation-range`](/en-US/docs/Web/CSS/Reference/Properties/animation-range) shorthand
  - [`animation-range-end`](/en-US/docs/Web/CSS/Reference/Properties/animation-range-end)
  - [`animation-range-start`](/en-US/docs/Web/CSS/Reference/Properties/animation-range-start)
- [`scroll-timeline`](/en-US/docs/Web/CSS/Reference/Properties/scroll-timeline) shorthand
  - [`scroll-timeline-axis`](/en-US/docs/Web/CSS/Reference/Properties/scroll-timeline-axis)
  - [`scroll-timeline-name`](/en-US/docs/Web/CSS/Reference/Properties/scroll-timeline-name)
- [`timeline-scope`](/en-US/docs/Web/CSS/Reference/Properties/timeline-scope)
- [`view-timeline`](/en-US/docs/Web/CSS/Reference/Properties/view-timeline) shorthand
  - [`view-timeline-axis`](/en-US/docs/Web/CSS/Reference/Properties/view-timeline-axis)
  - [`view-timeline-inset`](/en-US/docs/Web/CSS/Reference/Properties/view-timeline-inset)
  - [`view-timeline-name`](/en-US/docs/Web/CSS/Reference/Properties/view-timeline-name)

### [Data types and values](#data_types_and_values)

- [`<axis>`](/en-US/docs/Web/CSS/Reference/Values/axis)
- [`<timeline-range-name>`](/en-US/docs/Web/CSS/Reference/Values/timeline-range-name)

### [Functions](#functions)

- [`scroll()`](/en-US/docs/Web/CSS/Reference/Properties/animation-timeline/scroll)
- [`view()`](/en-US/docs/Web/CSS/Reference/Properties/animation-timeline/view)

### [Interfaces](#interfaces)

- [`ScrollTimeline`](/en-US/docs/Web/API/ScrollTimeline)
- [`ViewTimeline`](/en-US/docs/Web/API/ViewTimeline)

## [Guides](#guides)

[Scroll-driven animation timelines](/en-US/docs/Web/CSS/Guides/Scroll-driven_animations/Timelines)
:   Scroll-driven animation timelines and creating scroll-driven animations.

## [Related concepts](#related_concepts)

- [CSS animations](/en-US/docs/Web/CSS/Guides/Animations) module
  - [`animation-timeline`](/en-US/docs/Web/CSS/Reference/Properties/animation-timeline)
  - [`@keyframes`](/en-US/docs/Web/CSS/Reference/At-rules/@keyframes) at-rule
  - [`<keyframe-selector>`](/en-US/docs/Web/CSS/Reference/Selectors/Keyframe_selectors)
- [CSS overflow](/en-US/docs/Web/CSS/Guides/Overflow) module
  - [Scroll container](/en-US/docs/Glossary/Scroll_container)
  - [Scrollport](/en-US/docs/Glossary/Scroll_container#scrollport)
- [Web Animations](/en-US/docs/Web/API/Web_Animations_API) API
  - [`Element.animate()`](/en-US/docs/Web/API/Element/animate)
  - [`Animation`](/en-US/docs/Web/API/Animation)
  - [`AnimationTimeline`](/en-US/docs/Web/API/AnimationTimeline)
  - [`DocumentTimeline`](/en-US/docs/Web/API/DocumentTimeline)
  - [`KeyframeEffect`](/en-US/docs/Web/API/KeyframeEffect)

## [Specifications](#specifications)

| Specification |
| --- |
| [Scroll-driven Animations](https://drafts.csswg.org/scroll-animations-1/) |

## [See also](#see_also)

- [Animate elements on scroll with scroll-driven animations](https://developer.chrome.com/docs/css-ui/scroll-driven-animations) via developer.chrome.com (2023)

## Help improve MDN

Was this page helpful to you?

Yes

No

[Learn how to contribute](/en-US/docs/MDN/Community/Getting_started)

This page was last modified on Jan 7, 2026 by [MDN contributors](/en-US/docs/Web/CSS/Guides/Scroll-driven_animations/contributors.txt).

[View this page on GitHub](https://github.com/mdn/content/blob/main/files/en-us/web/css/guides/scroll-driven_animations/index.md?plain=1 "Folder: en-us/web/css/guides/scroll-driven_animations (Opens in a new tab)") â¢ [Report a problem with this content](https://github.com/mdn/content/issues/new?template=page-report.yml&mdn-url=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FGuides%2FScroll-driven_animations&metadata=%3C%21--+Do+not+make+changes+below+this+line+--%3E%0A%3Cdetails%3E%0A%3Csummary%3EPage+report+details%3C%2Fsummary%3E%0A%0A*+Folder%3A+%60en-us%2Fweb%2Fcss%2Fguides%2Fscroll-driven_animations%60%0A*+MDN+URL%3A+https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FGuides%2FScroll-driven_animations%0A*+GitHub+URL%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fblob%2Fmain%2Ffiles%2Fen-us%2Fweb%2Fcss%2Fguides%2Fscroll-driven_animations%2Findex.md%0A*+Last+commit%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fcommit%2Fa397ab763a6686a4056af755e4da32ac735b9fa5%0A*+Document+last+modified%3A+2026-01-07T12%3A08%3A12.000Z%0A%0A%3C%2Fdetails%3E "This will take you to GitHub to file a new issue.")