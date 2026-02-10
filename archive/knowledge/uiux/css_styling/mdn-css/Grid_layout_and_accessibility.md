# Grid layout and accessibility

Source: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout/Grid_layout_and_accessibility

---

# Grid layout and accessibility

HTML is the content layer of a website where we create semantic, well-structured documents. CSS is the presentation layer; we apply CSS to create, among other things, the desired layout for our content. Two-dimensional grid structures are defined using [CSS grid layout](/en-US/docs/Web/CSS/Guides/Grid_layout).

Even though modern HTML and CSS are designed to enable the creation of semantic, accessible content and designs, there are ways to *create* accessibility issues with grids. This article looks at the potential issues that can arise, and how to avoid them.

## [Re-ordering content in CSS grid layout](#re-ordering_content_in_css_grid_layout)

We've already seen in these guides that CSS grid layout gives us the power to re-order our page content by positioning items using [line-based placement of grid template areas](/en-US/docs/Web/CSS/Guides/Grid_layout/Line-based_placement). This placement can be done without considering the item's location in the source. There is also the [`order`](/en-US/docs/Web/CSS/Reference/Properties/order) property, which can change how items auto-place. The [`grid-auto-flow`](/en-US/docs/Web/CSS/Reference/Properties/grid-auto-flow) property has a `dense` value, which can take items visually out of the DOM order.

The CSS grid layout specification includes a [Reordering and Accessibility](https://drafts.csswg.org/css-grid/#order-accessibility) section. The introduction to that section details what browsers should do when content is visually reordered using grid layout:

> Grid layout gives authors great powers of rearrangement over the document. However, these are not a substitute for correct ordering of the document source. The `order` property and grid placement do not affect ordering in non-visual media (such as speech). Likewise, rearranging grid items visually does not affect the default traversal order of sequential navigation modes (such as cycling through links, see e.g., [`tabindex`](/en-US/docs/Web/HTML/Reference/Global_attributes/tabindex)).

If you reorder things visually using grid layout, this will not change how the items are ordered if the content is being read out by a screen reader, or other text to speech user agent. In addition, the reordering will not change tab order. This means that someone navigating using the keyboard could be tabbing through links on your site and suddenly find themselves jumping from the top to the bottom of the document due to a reordered item being next in the tab order.

The specification warns authors (the CSSWG term for web developers) not to do this reordering.

> Authors must use `order` and the grid-placement properties only for visual, not logical, reordering of content. Style sheets that use these features to perform logical reordering are non-conforming.

What does this mean for designing with grid layout in practice?

### [Visual not logical re-ordering](#visual_not_logical_re-ordering)

Any time you reorder things with grid layout â or with flexbox â you only perform *visual reordering*. The underlying source is what controls things like text to speech, and the tab order of the document. We can see how this works with an example.

In this example, we have a grid containing five items, each containing a link. The items are placed with line-based placement properties. We've positioned box 1 on the second row of the grid so it visually appears as the fourth item in the list. If we navigate through the links with the tab key, the tab order still begins with box 1, as it comes first in the source.

```
* {
  box-sizing: border-box;
}

.wrapper {
  border: 2px solid #f76707;
  border-radius: 5px;
  background-color: #fff4e6;
}

.wrapper > div {
  border: 2px solid #ffa94d;
  border-radius: 5px;
  background-color: #ffd8a8;
  padding: 1em;
  color: #d9480f;
}
```

css

```
.wrapper {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-auto-rows: 100px;
}

.box1 {
  grid-column: 1;
  grid-row: 2;
}
```

html

```
<div class="wrapper">
  <div class="box box1"><a href="">One</a></div>
  <div class="box box2"><a href="">Two</a></div>
  <div class="box box3"><a href="">Three</a></div>
  <div class="box box4"><a href="">Four</a></div>
  <div class="box box5"><a href="">Five</a></div>
</div>
```

The specification says that in this scenario, if box 1 really makes sense logically in that position, we should go back to our HTML source and make the change there rather than reordering using grid layout. This is what is meant by visual versus logical reordering; logical ordering is important for the meaning and structure of our document and we should make sure that we preserve that structure.

## [How should we approach accessibility for grid layout?](#how_should_we_approach_accessibility_for_grid_layout)

From the specification we know that we need to ensure our document maintains the logical order of our content. How should we approach our development to make sure that we maintain accessibility for the different users and the ways that they interact with our pages?

[Start with a structured and accessible document](#start_with_a_structured_and_accessible_document)
:   A grid layout should mean we do not need to change our document source in order to get the layout that we want. Therefore the starting point of your page should be a well structured and accessible source document. This is quite often going to give you a good structure for *your smallest screen devices too*. If a user is scrolling through a long document on mobile, the priorities for that user quite often map to what should be a priority in the source.

[Create a responsive, and responsible grid](#create_a_responsive_and_responsible_grid)
:   With a solid document structure defined in your HTML, you can use CSS to add your layout on top. You will likely use [media queries](/en-US/docs/Web/CSS/Guides/Media_queries) to make changes for different screen sizes and devices, including creating additional columns for larger screens. Grid can be very useful here. For example, elements deprioritized in the mobile source order can be moved into a sidebar in a desktop layout. The key here is to keep testing. A good test is to *tab around the document*. Does the order still make sense? Check that you do not end up leaping from the top to the bottom of the layout in a peculiar way. That is a sign that you need to address something about the layout.

[Returning to the source](#returning_to_the_source)
:   If at any time in the design process you find yourself using grid to relocate the position of an element, consider whether you should return to your document and make a change to the logical order too. The nice thing about using CSS grid layout is that you should be able to move an item in the source to match the logical order, without needing to make big changes to your layout. The onus is on us as developers to remember to go back to our source and update it to maintain logical order.

## [Grid and the danger of markup flattening](#grid_and_the_danger_of_markup_flattening)

Another issue to be aware of in CSS grid layout and to a lesser extent in CSS flexbox, is the temptation to *flatten* markup. As we have discovered, for an item to become a grid item it needs to be a direct child of the grid container. Therefore, where you have a [`<ul>`](/en-US/docs/Web/HTML/Reference/Elements/ul) element inside a grid container, *that* `ul` becomes a grid item â the child [`<li>`](/en-US/docs/Web/HTML/Reference/Elements/li) elements do not.

The [`subgrid`](/en-US/docs/Web/CSS/Guides/Grid_layout/Subgrid) value of `grid-template-columns` and `grid-template-rows` solves this problem. It allows the grid to be inherited by grid items and passed down the tree. Alternatively, setting `display: contents` on a grid item causes the element's children to become grid items. If you set an item to `display: contents`, the box it would normally create disappears and the boxes of the child elements appear as if they have risen up a level.

Starting out with a well-structured document is a very good way to avoid accessibility problems.

## [See also](#see_also)

- [Flexbox & the keyboard navigation disconnect](https://tink.uk/flexbox-the-keyboard-navigation-disconnect/) and [(Human After All): Accessibility remix video](https://www.youtube.com/watch?v=spxT2CmHoPk) via LÃ©onie Watson (2016)
- [Grid, content re-ordering and accessibility](https://css-tricks.com/grid-content-re-ordering-and-accessibility/) via CSS-tricks (2019)
- [`display: contents` is not a CSS reset](https://adrianroselli.com/2018/05/display-contents-is-not-a-css-reset.html) via Adrian Roselli (2024)

## Help improve MDN

Was this page helpful to you?

Yes

No

[Learn how to contribute](/en-US/docs/MDN/Community/Getting_started)

This page was last modified on Nov 7, 2025 by [MDN contributors](/en-US/docs/Web/CSS/Guides/Grid_layout/Accessibility/contributors.txt).

[View this page on GitHub](https://github.com/mdn/content/blob/main/files/en-us/web/css/guides/grid_layout/accessibility/index.md?plain=1 "Folder: en-us/web/css/guides/grid_layout/accessibility (Opens in a new tab)") â¢ [Report a problem with this content](https://github.com/mdn/content/issues/new?template=page-report.yml&mdn-url=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FGuides%2FGrid_layout%2FAccessibility&metadata=%3C%21--+Do+not+make+changes+below+this+line+--%3E%0A%3Cdetails%3E%0A%3Csummary%3EPage+report+details%3C%2Fsummary%3E%0A%0A*+Folder%3A+%60en-us%2Fweb%2Fcss%2Fguides%2Fgrid_layout%2Faccessibility%60%0A*+MDN+URL%3A+https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FGuides%2FGrid_layout%2FAccessibility%0A*+GitHub+URL%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fblob%2Fmain%2Ffiles%2Fen-us%2Fweb%2Fcss%2Fguides%2Fgrid_layout%2Faccessibility%2Findex.md%0A*+Last+commit%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fcommit%2F85fccefc8066bd49af4ddafc12c77f35265c7e2d%0A*+Document+last+modified%3A+2025-11-07T15%3A58%3A06.000Z%0A%0A%3C%2Fdetails%3E "This will take you to GitHub to file a new issue.")