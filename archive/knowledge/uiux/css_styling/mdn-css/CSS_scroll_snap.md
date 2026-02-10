# CSS scroll snap

Source: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scroll_snap

---

# CSS scroll snap

The **CSS scroll snap** module provides properties that let you control the panning and scrolling behavior by defining snap positions. Content can be snapped into position as the user scrolls overflowing content within a [scroll container](/en-US/docs/Glossary/Scroll_container), providing paging and scroll positioning.

This module includes the scroll container scroll-padding properties to adjust the optimal viewing region of paging during scroll-into-view operations. It also includes scroll-margin and scroll-alignment, set on the scroll container's children, to adjust the children's visual area when that child is scrolled into view, as well as a property to force scrolling to stop on individual children.

## [Scroll snap in action](#scroll_snap_in_action)

To view scroll snapping in the box below, scroll up-and-down and left-and-right through the grid of 45 numbered boxes in the scrollable viewport.
Click "Play" in the example below to view the or edit the source in the MDN Playground:

```
const positions = ["start", "center", "end"];
const inlineDirection = document.getElementById("inline");
const blockDirection = document.getElementById("block");
const stop = document.getElementById("stop");
const snap = document.getElementById("snap");
const all = document.querySelector("article");
const rules = document.getElementById("css-output").sheet.cssRules;

setSST();
setSSA();

inlineDirection.addEventListener("change", () => {
  setSSA();
});
blockDirection.addEventListener("change", () => {
  setSSA();
});
stop.addEventListener("change", () => {
  setSST();
});
snap.addEventListener("change", () => {
  all.classList.toggle("snapDisabled");
});

function setSSA() {
  rules[0].style.scrollSnapAlign = `${positions[blockDirection.value]} ${
    positions[inlineDirection.value]
  }`;
}

function setSST() {
  if (stop.checked) {
    rules[0].style.scrollSnapStop = "always";
  } else {
    rules[0].style.scrollSnapStop = "normal";
  }
}
```

```
<article>
  <ul>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
  </ul>
  <div>
    <fieldset>
      <legend>Change the options</legend>
      <p>
        <label
          ><input
            type="range"
            min="0"
            max="2"
            value="1"
            list="places"
            id="block" />
          block position</label
        >
      </p>
      <p>
        <label>
          <input
            type="range"
            min="0"
            max="2"
            value="1"
            list="places"
            id="inline" />
          inline position
        </label>
      </p>
      <p>
        <label>
          <input type="checkbox" id="stop" />
          Prevent scrolling past boxes
        </label>
      </p>
    </fieldset>

    <p>
      <label><input type="checkbox" id="snap" /> disable snapping</label>
    </p>

    <datalist id="places">
      <option value="0">start</option>
      <option value="1">center</option>
      <option value="2">end</option>
    </datalist>
  </div>
</article>
```

```
li {
  /*
  starts with:
      scroll-snap-align: center center;
      scroll-snap-stop: normal (defaults);

  CSS gets changed with JavaScript when you change the controls.
  the following can be set:
      scroll-snap-stop: always | normal;
      scroll-snap-align: start | center | end {2}
        */
}
ul {
  overflow: auto;
  scroll-snap-type: both mandatory;
  overscroll-behavior-x: contain;
}
article.snapDisabled fieldset {
  opacity: 20%;
  pointer-events: none;
}
article.snapDisabled ul {
  scroll-snap-type: initial;
  overscroll-behavior-x: initial;
}

@layer page-setup {
  article {
    display: flex;
    gap: 2vw;
  }
  div {
    flex: 1;
  }
  ul {
    display: grid;
    gap: 6.25vw;
    padding: 12.5vw;
    box-sizing: border-box;
    border: 1px solid;
    grid-template-columns: repeat(5, 1fr);
    background: conic-gradient(
      at bottom left,
      red 0deg,
      yellow 15deg,
      green 30deg,
      blue 45deg,
      purple 60deg,
      magenta 75deg
    );
    background-attachment: local;
    margin: auto;
    width: 20vw;
    height: 20vw;
  }
  li {
    scroll-snap-align: center;
    height: 12.5vw;
    width: 12.5vw;
    outline: 3px inset;
    list-style-type: none;
    background: white;
    font-family: monospace;
    font-size: 3rem;
    line-height: 12vw;
    text-align: center;
    counter-increment: items 1;
  }
  li::after {
    content: counter(items);
  }
  input {
    vertical-align: bottom;
  }
  p {
    font-family: monospace;
  }
}
```

With scroll snap, one of the numbered boxes that you scroll to will snap into place. The initial CSS makes the numbered box snap into the center of the viewport. Use the sliders to change the block and inline snap positions.

Using snap properties, you can allow or block the scrolling past an element, a numbered box in this case. Select the "Prevent scrolling past boxes" checkbox to force all scrolling actions to be limited to scrolling to an adjacent box.

To compare scroll snapping to regular scrolling, check the "disable snapping" checkbox and try scrolling again.

## [Reference](#reference)

### [Properties on containers](#properties_on_containers)

- [`scroll-snap-type`](/en-US/docs/Web/CSS/Reference/Properties/scroll-snap-type)
- [`scroll-padding`](/en-US/docs/Web/CSS/Reference/Properties/scroll-padding)
  - [`scroll-padding-top`](/en-US/docs/Web/CSS/Reference/Properties/scroll-padding-top)
  - [`scroll-padding-right`](/en-US/docs/Web/CSS/Reference/Properties/scroll-padding-right)
  - [`scroll-padding-bottom`](/en-US/docs/Web/CSS/Reference/Properties/scroll-padding-bottom)
  - [`scroll-padding-left`](/en-US/docs/Web/CSS/Reference/Properties/scroll-padding-left)
  - [`scroll-padding-inline`](/en-US/docs/Web/CSS/Reference/Properties/scroll-padding-inline)
  - [`scroll-padding-inline-start`](/en-US/docs/Web/CSS/Reference/Properties/scroll-padding-inline-start)
  - [`scroll-padding-inline-end`](/en-US/docs/Web/CSS/Reference/Properties/scroll-padding-inline-end)
  - [`scroll-padding-block`](/en-US/docs/Web/CSS/Reference/Properties/scroll-padding-block)
  - [`scroll-padding-block-start`](/en-US/docs/Web/CSS/Reference/Properties/scroll-padding-block-start)
  - [`scroll-padding-block-end`](/en-US/docs/Web/CSS/Reference/Properties/scroll-padding-block-end)

### [Properties on children](#properties_on_children)

- [`scroll-snap-align`](/en-US/docs/Web/CSS/Reference/Properties/scroll-snap-align)
- [`scroll-margin`](/en-US/docs/Web/CSS/Reference/Properties/scroll-margin)
  - [`scroll-margin-top`](/en-US/docs/Web/CSS/Reference/Properties/scroll-margin-top)
  - [`scroll-margin-right`](/en-US/docs/Web/CSS/Reference/Properties/scroll-margin-right)
  - [`scroll-margin-bottom`](/en-US/docs/Web/CSS/Reference/Properties/scroll-margin-bottom)
  - [`scroll-margin-left`](/en-US/docs/Web/CSS/Reference/Properties/scroll-margin-left)
  - [`scroll-margin-inline`](/en-US/docs/Web/CSS/Reference/Properties/scroll-margin-inline)
  - [`scroll-margin-inline-start`](/en-US/docs/Web/CSS/Reference/Properties/scroll-margin-inline-start)
  - [`scroll-margin-inline-end`](/en-US/docs/Web/CSS/Reference/Properties/scroll-margin-inline-end)
  - [`scroll-margin-block`](/en-US/docs/Web/CSS/Reference/Properties/scroll-margin-block)
  - [`scroll-margin-block-start`](/en-US/docs/Web/CSS/Reference/Properties/scroll-margin-block-start)
  - [`scroll-margin-block-end`](/en-US/docs/Web/CSS/Reference/Properties/scroll-margin-block-end)
- [`scroll-snap-stop`](/en-US/docs/Web/CSS/Reference/Properties/scroll-snap-stop)

### [Events](#events)

- [`scrollsnapchange`](/en-US/docs/Web/API/Element/scrollsnapchange_event "scrollsnapchange") 
  Experimental
- [`scrollsnapchanging`](/en-US/docs/Web/API/Element/scrollsnapchanging_event "scrollsnapchanging") 
  Experimental

### [Interfaces](#interfaces)

- [`SnapEvent`](/en-US/docs/Web/API/SnapEvent) 
  Experimental
  - [`SnapEvent.snapTargetBlock`](/en-US/docs/Web/API/SnapEvent/snapTargetBlock) 
    Experimental
  - [`SnapEvent.snapTargetInline`](/en-US/docs/Web/API/SnapEvent/snapTargetInline) 
    Experimental

## [Guides](#guides)

[Basic concepts of CSS scroll snap](/en-US/docs/Web/CSS/Guides/Scroll_snap/Basic_concepts)
:   An overview and examples of CSS scroll snap features.

[Using scroll snap events](/en-US/docs/Web/CSS/Guides/Scroll_snap/Using_scroll_snap_events)
:   A guide to using the [`scrollsnapchanging`](/en-US/docs/Web/API/Element/scrollsnapchanging_event "scrollsnapchanging") and [`scrollsnapchange`](/en-US/docs/Web/API/Element/scrollsnapchange_event "scrollsnapchange") scroll snap events that are fired when the browser determines a new snap target is pending or selected.

## [Related concepts](#related_concepts)

- [`:target`](/en-US/docs/Web/CSS/Reference/Selectors/:target) pseudo-class
- [`overflow`](/en-US/docs/Web/CSS/Reference/Properties/overflow) CSS property
- Element [`scroll()`](/en-US/docs/Web/API/Element/scroll "scroll()") method
- Element [`scrollBy()`](/en-US/docs/Web/API/Element/scrollBy "scrollBy()") method
- Element [`scrollIntoView()`](/en-US/docs/Web/API/Element/scrollIntoView "scrollIntoView()") method
- Element [`scrollTo()`](/en-US/docs/Web/API/Element/scrollTo "scrollTo()") method
- Element [`scroll`](/en-US/docs/Web/API/Element/scroll_event "scroll") event
- Element [`scrollend`](/en-US/docs/Web/API/Element/scrollend_event "scrollend") event
- [`scrollbar`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/scrollbar_role) ARIA role
- [Scroll container](/en-US/docs/Glossary/Scroll_container) glossary term

## [Specifications](#specifications)

| Specification |
| --- |
| [CSS Scroll Snap Module Level 1](https://drafts.csswg.org/css-scroll-snap/) |
| [CSS Scroll Snap Module Level 2](https://drafts.csswg.org/css-scroll-snap-2/) |

## [See also](#see_also)

- [CSS overflow](/en-US/docs/Web/CSS/Guides/Overflow) module
- [CSS scrollbars styling](/en-US/docs/Web/CSS/Guides/Scrollbars_styling) module
- [CSS scroll anchoring](/en-US/docs/Web/CSS/Guides/Scroll_anchoring) module
- [Keyboard-only scrolling areas](https://adrianroselli.com/2022/06/keyboard-only-scrolling-areas.html) on adrianroselli.com (2022)
- [Scroll snap examples](https://codepen.io/collection/KpqBGW) on CodePen (2022)
- [Well-controlled scrolling with CSS scroll snap](https://web.dev/articles/css-scroll-snap) on web.dev (2021)
- [Practical CSS scroll snapping/](https://css-tricks.com/practical-css-scroll-snapping/) on CSS-Tricks (2020)
- [CSS scroll snap](https://12daysofweb.dev/2022/css-scroll-snap/) on 12 Days of Web (2019)

## Help improve MDN

Was this page helpful to you?

Yes

No

[Learn how to contribute](/en-US/docs/MDN/Community/Getting_started)

This page was last modified on Nov 8, 2025 by [MDN contributors](/en-US/docs/Web/CSS/Guides/Scroll_snap/contributors.txt).

[View this page on GitHub](https://github.com/mdn/content/blob/main/files/en-us/web/css/guides/scroll_snap/index.md?plain=1 "Folder: en-us/web/css/guides/scroll_snap (Opens in a new tab)") â¢ [Report a problem with this content](https://github.com/mdn/content/issues/new?template=page-report.yml&mdn-url=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FGuides%2FScroll_snap&metadata=%3C%21--+Do+not+make+changes+below+this+line+--%3E%0A%3Cdetails%3E%0A%3Csummary%3EPage+report+details%3C%2Fsummary%3E%0A%0A*+Folder%3A+%60en-us%2Fweb%2Fcss%2Fguides%2Fscroll_snap%60%0A*+MDN+URL%3A+https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FGuides%2FScroll_snap%0A*+GitHub+URL%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fblob%2Fmain%2Ffiles%2Fen-us%2Fweb%2Fcss%2Fguides%2Fscroll_snap%2Findex.md%0A*+Last+commit%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fcommit%2F11d748f9e217b6a9fd16291d7815a6f803f0136d%0A*+Document+last+modified%3A+2025-11-08T03%3A33%3A06.000Z%0A%0A%3C%2Fdetails%3E "This will take you to GitHub to file a new issue.")