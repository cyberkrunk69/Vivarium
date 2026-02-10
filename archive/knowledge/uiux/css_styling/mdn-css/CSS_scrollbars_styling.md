# CSS scrollbars styling

Source: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scrollbars_styling

---

# CSS scrollbars styling

The **CSS scrollbars styling** module defines properties that you can use for visual styling of scrollbars. You can customize the width of the scrollbar as required. You can also customize the color of the scrollbar *track*, which is the background of the scrollbar, and the color of the scrollbar *thumb*, which is the draggable handle of the scrollbar.

## [Scrollbar styling in action](#scrollbar_styling_in_action)

This example defines a thin scrollbar with a red thumb and an orange track. To view the thumb, you will need to scroll the text. After the scrollbar is visible, hover over it to see the track.

```
.poem {
  width: 300px;
  height: 100px;
  border: 1px solid;
}
```

css

```
.poem {
  overflow: scroll;
  scrollbar-color: red orange;
  scrollbar-width: thin;
}
```

```
<blockquote class="poem">
  <h3>A Small Needful Fact</h3>
  <pre>
Is that Eric Garner worked
for some time for the Parks and Rec.
Horticultural Department, which means,
perhaps, that with his very large hands,
perhaps, in all likelihood,
he put gently into the earth
some plants which, most likely,
some of them, in all likelihood,
continue to grow, continue
to do what such plants do, like house
and feed small and necessary creatures,
like being pleasant to touch and smell,
like converting sunlight
into food, like making it easier
for us to breathe.
</pre
  >
  <p>
    - <a href="https://onbeing.org/poetry/a-small-needful-fact/">Ross Gay</a>
  </p>
</blockquote>
```

**Note:**
When customizing scrollbars, ensure that the thumb and track have enough contrast with the surrounding background. Also ensure that the scrollbar hit area is large enough for people who use touch input.

## [Reference](#reference)

### [CSS properties](#css_properties)

- [`scrollbar-width`](/en-US/docs/Web/CSS/Reference/Properties/scrollbar-width)
- [`scrollbar-color`](/en-US/docs/Web/CSS/Reference/Properties/scrollbar-color)

## [Related concepts](#related_concepts)

- [`overflow-block`](/en-US/docs/Web/CSS/Reference/Properties/overflow-block) CSS property
- [`overflow-inline`](/en-US/docs/Web/CSS/Reference/Properties/overflow-inline) CSS property
- [`overflow-x`](/en-US/docs/Web/CSS/Reference/Properties/overflow-x) CSS property
- [`overflow-y`](/en-US/docs/Web/CSS/Reference/Properties/overflow-y) CSS property
- [`overflow`](/en-US/docs/Web/CSS/Reference/Properties/overflow) CSS shorthand property
- [`overflow-clip-margin`](/en-US/docs/Web/CSS/Reference/Properties/overflow-clip-margin) CSS property
- [`scrollbar-gutter`](/en-US/docs/Web/CSS/Reference/Properties/scrollbar-gutter) CSS property
- [`scroll-behavior`](/en-US/docs/Web/CSS/Reference/Properties/scroll-behavior) CSS property
- [`scroll-margin`](/en-US/docs/Web/CSS/Reference/Properties/scroll-margin) CSS shorthand property
- [`scroll-padding`](/en-US/docs/Web/CSS/Reference/Properties/scroll-padding) CSS shorthand property
- [`scroll-snap-align`](/en-US/docs/Web/CSS/Reference/Properties/scroll-snap-align) CSS property
- [`scroll-snap-stop`](/en-US/docs/Web/CSS/Reference/Properties/scroll-snap-stop) CSS property
- [`scroll-snap-type`](/en-US/docs/Web/CSS/Reference/Properties/scroll-snap-type) CSS property
- [`::-webkit-scrollbar`](/en-US/docs/Web/CSS/Reference/Selectors/::-webkit-scrollbar) pseudo-element
- [scroll container](/en-US/docs/Glossary/Scroll_container) glossary term
- [`scrollbar`](/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/scrollbar_role) ARIA role

## [Specifications](#specifications)

| Specification |
| --- |
| [CSS Scrollbars Styling Module Level 1](https://drafts.csswg.org/css-scrollbars/) |

## [See also](#see_also)

- [`scroll-timeline`](/en-US/docs/Web/CSS/Reference/Properties/scroll-timeline), [`scroll-timeline-axis`](/en-US/docs/Web/CSS/Reference/Properties/scroll-timeline-axis), [`scroll-timeline-name`](/en-US/docs/Web/CSS/Reference/Properties/scroll-timeline-name)
- [CSS overflow](/en-US/docs/Web/CSS/Guides/Overflow) module
- [CSS scroll snap](/en-US/docs/Web/CSS/Guides/Scroll_snap) module

## Help improve MDN

Was this page helpful to you?

Yes

No

[Learn how to contribute](/en-US/docs/MDN/Community/Getting_started)

This page was last modified on Nov 7, 2025 by [MDN contributors](/en-US/docs/Web/CSS/Guides/Scrollbars_styling/contributors.txt).

[View this page on GitHub](https://github.com/mdn/content/blob/main/files/en-us/web/css/guides/scrollbars_styling/index.md?plain=1 "Folder: en-us/web/css/guides/scrollbars_styling (Opens in a new tab)") â¢ [Report a problem with this content](https://github.com/mdn/content/issues/new?template=page-report.yml&mdn-url=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FGuides%2FScrollbars_styling&metadata=%3C%21--+Do+not+make+changes+below+this+line+--%3E%0A%3Cdetails%3E%0A%3Csummary%3EPage+report+details%3C%2Fsummary%3E%0A%0A*+Folder%3A+%60en-us%2Fweb%2Fcss%2Fguides%2Fscrollbars_styling%60%0A*+MDN+URL%3A+https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FGuides%2FScrollbars_styling%0A*+GitHub+URL%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fblob%2Fmain%2Ffiles%2Fen-us%2Fweb%2Fcss%2Fguides%2Fscrollbars_styling%2Findex.md%0A*+Last+commit%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fcommit%2F85fccefc8066bd49af4ddafc12c77f35265c7e2d%0A*+Document+last+modified%3A+2025-11-07T15%3A58%3A06.000Z%0A%0A%3C%2Fdetails%3E "This will take you to GitHub to file a new issue.")