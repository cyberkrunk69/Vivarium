# CSS Flexbox Layout Guide | CSS-Tricks

Source: https://css-tricks.com/snippets/css/a-guide-to-flexbox/

---

#### Table of contents

1. [Background](#aa-background)
2. [Basics and terminology](#aa-basics-and-terminology)
3. [Flexbox properties](#aa-flexbox-properties)
4. [Prefixing Flexbox](#aa-prefixing-flexbox)
5. [Examples](#aa-examples)
6. [Flexbox tricks](#aa-flexbox-tricks)
7. [Browser support](#aa-browser-support)
8. [Bugs](#aa-bugs)
9. [Related properties](#aa-related-properties)
10. [More information](#aa-more-information)
11. [More sources](#aa-more-sources)

#### Get the poster!

Reference this guide a lot? Here’s a high-res image you can print!

[Download Free](https://css-tricks.com/wp-content/uploads/2022/02/css-flexbox-poster.png)

![](https://i0.wp.com/css-tricks.com/wp-content/uploads/2020/06/43150-1.jpg?resize=1024%2C1024&ssl=1)

---

### Background

The `Flexbox Layout` (Flexible Box) module ([a W3C Candidate Recommendation](https://www.w3.org/TR/css-flexbox/) as of October 2017) aims at providing a more efficient way to lay out, align and distribute space among items in a container, even when their size is unknown and/or dynamic (thus the word “flex”).

The main idea behind the flex layout is to give the container the ability to alter its items’ width/height (and order) to best fill the available space (mostly to accommodate to all kind of display devices and screen sizes). A flex container expands items to fill available free space or shrinks them to prevent overflow.

Most importantly, the flexbox layout is direction-agnostic as opposed to the regular layouts (block which is vertically-based and inline which is horizontally-based). While those work well for pages, they lack flexibility (no pun intended) to support large or complex applications (especially when it comes to orientation changing, resizing, stretching, shrinking, etc.).

**Note:** Flexbox layout is most appropriate to the components of an application, and small-scale layouts, while the [Grid](https://css-tricks.com/snippets/css/complete-guide-grid/) layout is intended for larger scale layouts.

### Basics and terminology

Since flexbox is a whole module and not a single property, it involves a lot of things including its whole set of properties. Some of them are meant to be set on the container (parent element, known as “flex container”) whereas the others are meant to be set on the children (said “flex items”).

If “regular” layout is based on both block and inline flow directions, the flex layout is based on “flex-flow directions”. Please have a look at this figure from the specification, explaining the main idea behind the flex layout.

![A diagram explaining flexbox terminology. The size across the main axis of flexbox is called the main size, the other direction is the cross size. Those sizes have a main start, main end, cross start, and cross end.](https://css-tricks.com/wp-content/uploads/2018/11/00-basic-terminology.svg)

Items will be laid out following either the `main axis` (from `main-start` to `main-end`) or the cross axis (from `cross-start` to `cross-end`).

- **main axis** – The main axis of a flex container is the primary axis along which flex items are laid out. Beware, it is not necessarily horizontal; it depends on the `flex-direction` property (see below).
- **main-start | main-end** – The flex items are placed within the container starting from main-start and going to main-end.
- **main size** – A flex item’s width or height, whichever is in the main dimension, is the item’s main size. The flex item’s main size property is either the ‘width’ or ‘height’ property, whichever is in the main dimension.
- **cross axis** – The axis perpendicular to the main axis is called the cross axis. Its direction depends on the main axis direction.
- **cross-start | cross-end** – Flex lines are filled with items and placed into the container starting on the cross-start side of the flex container and going toward the cross-end side.
- **cross size** – The width or height of a flex item, whichever is in the cross dimension, is the item’s cross size. The cross size property is whichever of ‘width’ or ‘height’ that is in the cross dimension.

### Flexbox properties

![](https://css-tricks.com/wp-content/uploads/2018/10/01-container.svg)

## Properties for the Parent (flex container)

#### display

This defines a flex container; inline or block depending on the given value. It enables a flex context for all its direct children.

```
.container {
  display: flex; /* or inline-flex */
}
```

Note that CSS columns have no effect on a flex container.

#### flex-direction

![the four possible values of flex-direction being shown: top to bottom, bottom to top, right to left, and left to right](https://css-tricks.com/wp-content/uploads/2018/10/flex-direction.svg)

This establishes the main-axis, thus defining the direction flex items are placed in the flex container. Flexbox is (aside from optional wrapping) a single-direction layout concept. Think of flex items as primarily laying out either in horizontal rows or vertical columns.

```
.container {
  flex-direction: row | row-reverse | column | column-reverse;
}
```

- `row` (default): left to right in `ltr`; right to left in `rtl`
- `row-reverse`: right to left in `ltr`; left to right in `rtl`
- `column`: same as `row` but top to bottom
- `column-reverse`: same as `row-reverse` but bottom to top

#### flex-wrap

![two rows of boxes, the first wrapping down onto the second](https://css-tricks.com/wp-content/uploads/2018/10/flex-wrap.svg)

By default, flex items will all try to fit onto one line. You can change that and allow the items to wrap as needed with this property.

```
.container {
  flex-wrap: nowrap | wrap | wrap-reverse;
}
```

- `nowrap` (default): all flex items will be on one line
- `wrap`: flex items will wrap onto multiple lines, from top to bottom.
- `wrap-reverse`: flex items will wrap onto multiple lines from bottom to top.

There are some [visual demos of `flex-wrap` here](https://css-tricks.com/almanac/properties/f/flex-wrap/).

#### flex-flow

This is a shorthand for the `flex-direction` and `flex-wrap` properties, which together define the flex container’s main and cross axes. The default value is `row nowrap`.

```
.container {
  flex-flow: column wrap;
}
```

#### justify-content

![flex items within a flex container demonstrating the different spacing options](https://css-tricks.com/wp-content/uploads/2018/10/justify-content.svg)

This defines the alignment along the main axis. It helps distribute extra free space leftover when either all the flex items on a line are inflexible, or are flexible but have reached their maximum size. It also exerts some control over the alignment of items when they overflow the line.

```
.container {
  justify-content: flex-start | flex-end | center | space-between | space-around | space-evenly | start | end | left | right ... + safe | unsafe;
}
```

- `flex-start` (default): items are packed toward the start of the flex-direction.
- `flex-end`: items are packed toward the end of the flex-direction.
- `start`: items are packed toward the start of the `writing-mode` direction.
- `end`: items are packed toward the end of the `writing-mode` direction.
- `left`: items are packed toward left edge of the container, unless that doesn’t make sense with the `flex-direction`, then it behaves like `start`.
- `right`: items are packed toward right edge of the container, unless that doesn’t make sense with the `flex-direction`, then it behaves like `end`.
- `center`: items are centered along the line
- `space-between`: items are evenly distributed in the line; first item is on the start line, last item on the end line
- `space-around`: items are evenly distributed in the line with equal space around them. Note that visually the spaces aren’t equal, since all the items have equal space on both sides. The first item will have one unit of space against the container edge, but two units of space between the next item because that next item has its own spacing that applies.
- `space-evenly`: items are distributed so that the spacing between any two items (and the space to the edges) is equal.

Note that that browser support for these values is nuanced. For example, `space-between` never got support from some versions of Edge, and start/end/left/right aren’t in Chrome yet. MDN [has detailed charts](https://developer.mozilla.org/en-US/docs/Web/CSS/justify-content). The safest values are `flex-start`, `flex-end`, and `center`.

There are also two additional keywords you can pair with these values: `safe` and `unsafe`. Using `safe` ensures that however you do this type of positioning, you can’t push an element such that it renders off-screen (e.g. off the top) in such a way the content can’t be scrolled too (called “data loss”).

#### align-items

![demonstration of differnet alignment options, like all boxes stuck to the top of a flex parent, the bottom, stretched out, or along a baseline](https://css-tricks.com/wp-content/uploads/2018/10/align-items.svg)

This defines the default behavior for how flex items are laid out along the **cross axis** on the current line. Think of it as the `justify-content` version for the cross-axis (perpendicular to the main-axis).

```
.container {
  align-items: stretch | flex-start | flex-end | center | baseline | first baseline | last baseline | start | end | self-start | self-end + ... safe | unsafe;
}
```

- `stretch` (default): stretch to fill the container (still respect min-width/max-width)
- `flex-start` / `start` / `self-start`: items are placed at the start of the cross axis. The difference between these is subtle, and is about respecting the `flex-direction` rules or the `writing-mode` rules.
- `flex-end` / `end` / `self-end`: items are placed at the end of the cross axis. The difference again is subtle and is about respecting `flex-direction` rules vs. `writing-mode` rules.
- `center`: items are centered in the cross-axis
- `baseline`: items are aligned such as their baselines align

The `safe` and `unsafe` modifier keywords can be used in conjunction with all the rest of these keywords (although note [browser support](https://developer.mozilla.org/en-US/docs/Web/CSS/align-items)), and deal with helping you prevent aligning elements such that the content becomes inaccessible.

#### align-content

![examples of the align-content property where a group of items cluster at the top or bottom, or stretch out to fill the space, or have spacing.](https://css-tricks.com/wp-content/uploads/2018/10/align-content.svg)

This aligns a flex container’s lines within when there is extra space in the cross-axis, similar to how `justify-content` aligns individual items within the main-axis.

**Note:** This property only takes effect on multi-line flexible containers, where `flex-wrap` is set to either `wrap` or `wrap-reverse`). A single-line flexible container (i.e. where `flex-wrap` is set to its default value, `no-wrap`) will not reflect `align-content`.

```
.container {
  align-content: flex-start | flex-end | center | space-between | space-around | space-evenly | stretch | start | end | baseline | first baseline | last baseline + ... safe | unsafe;
}
```

- `normal` (default): items are packed in their default position as if no value was set.
- `flex-start` / `start`: items packed to the start of the container. The (more supported) `flex-start` honors the `flex-direction` while `start` honors the `writing-mode` direction.
- `flex-end` / `end`: items packed to the end of the container. The (more support) `flex-end` honors the `flex-direction` while end honors the `writing-mode` direction.
- `center`: items centered in the container
- `space-between`: items evenly distributed; the first line is at the start of the container while the last one is at the end
- `space-around`: items evenly distributed with equal space around each line
- `space-evenly`: items are evenly distributed with equal space around them
- `stretch`: lines stretch to take up the remaining space

The `safe` and `unsafe` modifier keywords can be used in conjunction with all the rest of these keywords (although note [browser support](https://developer.mozilla.org/en-US/docs/Web/CSS/align-items)), and deal with helping you prevent aligning elements such that the content becomes inaccessible.

#### gap, row-gap, column-gap

![](https://css-tricks.com/wp-content/uploads/2021/09/gap-1.svg)

[The `gap` property](https://css-tricks.com/almanac/properties/g/gap/) explicitly controls the space between flex items. It applies that spacing *only between items* not on the outer edges.

```
.container {
  display: flex;
  ...
  gap: 10px;
  gap: 10px 20px; /* row-gap column gap */
  row-gap: 10px;
  column-gap: 20px;
}
```

The behavior could be thought of as a *minimum* gutter, as if the gutter is bigger somehow (because of something like `justify-content: space-between;`) then the gap will only take effect if that space would end up smaller.

It is not exclusively for flexbox, `gap` works in grid and multi-column layout as well.

![](https://css-tricks.com/wp-content/uploads/2018/10/02-items.svg)

## Properties for the Children (flex items)

#### order

![Diagram showing flexbox order. A container with the items being 1 1 1 2 3, -1 1 2 5, and 2 2 99.](https://css-tricks.com/wp-content/uploads/2018/10/order.svg)

By default, flex items are laid out in the source order. However, the `order` property controls the order in which they appear in the flex container.

```
.item {
  order: 5; /* default is 0 */
}
```

Items with the same `order` revert to source order.

#### flex-grow

![two rows of items, the first has all equally-sized items with equal flex-grow numbers, the second with the center item at twice the width because its value is 2 instead of 1.](https://css-tricks.com/wp-content/uploads/2018/10/flex-grow.svg)

This defines the ability for a flex item to grow if necessary. It accepts a unitless value that serves as a proportion. It dictates what amount of the available space inside the flex container the item should take up.

If all items have `flex-grow` set to `1`, the remaining space in the container will be distributed equally to all children. If one of the children has a value of `2`, that child would take up twice as much of the space as either one of the others (or it will try, at least).

```
.item {
  flex-grow: 4; /* default 0 */
}
```

Negative numbers are invalid.

#### flex-shrink

This defines the ability for a flex item to shrink if necessary.

```
.item {
  flex-shrink: 3; /* default 1 */
}
```

Negative numbers are invalid.

#### flex-basis

This defines the default size of an element before the remaining space is distributed. It can be a length (e.g. 20%, 5rem, etc.) or a keyword. The `auto` keyword means “look at my width or height property” (which was temporarily done by the `main-size` keyword until deprecated). The `content` keyword means “size it based on the item’s content” – this keyword isn’t well supported yet, so it’s hard to test and harder to know what its brethren `max-content`, `min-content`, and `fit-content` do.

```
.item {
  flex-basis:  | auto; /* default auto */
}
```

If set to `0`, the extra space around content isn’t factored in. If set to `auto`, the extra space is distributed based on its `flex-grow` value. [See this graphic.](http://www.w3.org/TR/css3-flexbox/images/rel-vs-abs-flex.svg)

#### flex

This is the shorthand for `flex-grow,` `flex-shrink` and `flex-basis` combined. The second and third parameters (`flex-shrink` and `flex-basis`) are optional. The default is `0 1 auto`, but if you set it with a single number value, like `flex: 5;`, that changes the `flex-basis` to 0%, so it’s like setting `flex-grow: 5; flex-shrink: 1; flex-basis: 0%;`.

```
.item {
  flex: none | [ <'flex-grow'> <'flex-shrink'>? || <'flex-basis'> ]
}
```

**It is recommended that you use this shorthand property** rather than set the individual properties. The shorthand sets the other values intelligently.

#### align-self

![One item with a align-self value is positioned along the bottom of a flex parent instead of the top where all the rest of the items are.](https://css-tricks.com/wp-content/uploads/2018/10/align-self.svg)

This allows the default alignment (or the one specified by `align-items`) to be overridden for individual flex items.

Please see the `align-items` explanation to understand the available values.

```
.item {
  align-self: auto | flex-start | flex-end | center | baseline | stretch;
}
```

Note that `float`, `clear` and `vertical-align` have no effect on a flex item.

### Prefixing Flexbox

Flexbox requires some vendor prefixing to support the most browsers possible. It doesn’t just include prepending properties with the vendor prefix, but there are actually entirely different property and value names. This is because the Flexbox spec has changed over time, creating an [“old”, “tweener”, and “new”](https://css-tricks.com/old-flexbox-and-new-flexbox/) versions.

Perhaps the best way to handle this is to write in the new (and final) syntax and run your CSS through [Autoprefixer](https://css-tricks.com/autoprefixer/), which handles the fallbacks very well.

Alternatively, here’s a Sass `@mixin` to help with some of the prefixing, which also gives you an idea of what kind of things need to be done:

```
@mixin flexbox() {
  display: -webkit-box;
  display: -moz-box;
  display: -ms-flexbox;
  display: -webkit-flex;
  display: flex;
}

@mixin flex($values) {
  -webkit-box-flex: $values;
  -moz-box-flex:  $values;
  -webkit-flex:  $values;
  -ms-flex:  $values;
  flex:  $values;
}

@mixin order($val) {
  -webkit-box-ordinal-group: $val;  
  -moz-box-ordinal-group: $val;     
  -ms-flex-order: $val;     
  -webkit-order: $val;  
  order: $val;
}

.wrapper {
  @include flexbox();
}

.item {
  @include flex(1 200px);
  @include order(2);
}
```

### Examples

Let’s start with a very very simple example, solving an almost daily problem: perfect centering. It couldn’t be any simpler if you use flexbox.

```
.parent {
  display: flex;
  height: 300px; /* Or whatever */
}

.child {
  width: 100px;  /* Or whatever */
  height: 100px; /* Or whatever */
  margin: auto;  /* Magic! */
}
```

This relies on the fact a margin set to `auto` in a flex container absorb extra space. So setting a margin of `auto` will make the item perfectly centered in both axes.

Now let’s use some more properties. Consider a list of 6 items, all with fixed dimensions, but can be auto-sized. We want them to be evenly distributed on the horizontal axis so that when we resize the browser, everything scales nicely, and without media queries.

```
.flex-container {
  /* We first create a flex layout context */
  display: flex;

  /* Then we define the flow direction 
     and if we allow the items to wrap 
   * Remember this is the same as:
   * flex-direction: row;
   * flex-wrap: wrap;
   */
  flex-flow: row wrap;

  /* Then we define how is distributed the remaining space */
  justify-content: space-around;
}
```

Done. Everything else is just some styling concern. Below is a pen featuring this example. Be sure to go to CodePen and try resizing your windows to see what happens.

Let’s try something else. Imagine we have a right-aligned navigation element on the very top of our website, but we want it to be centered on medium-sized screens and single-columned on small devices. Easy enough.

```
/* Large */
.navigation {
  display: flex;
  flex-flow: row wrap;
  /* This aligns items to the end line on main-axis */
  justify-content: flex-end;
}

/* Medium screens */
@media all and (max-width: 800px) {
  .navigation {
    /* When on medium sized screens, we center it by evenly distributing empty space around items */
    justify-content: space-around;
  }
}

/* Small screens */
@media all and (max-width: 500px) {
  .navigation {
    /* On small screens, we are no longer using row direction but column */
    flex-direction: column;
  }
}
```

Let’s try something even better by playing with flex items flexibility! What about a mobile-first 3-columns layout with full-width header and footer. And independent from source order.

```
.wrapper {
  display: flex;
  flex-flow: row wrap;
}

/* We tell all items to be 100% width, via flex-basis */
.wrapper > * {
  flex: 1 100%;
}

/* We rely on source order for mobile-first approach
 * in this case:
 * 1. header
 * 2. article
 * 3. aside 1
 * 4. aside 2
 * 5. footer
 */

/* Medium screens */
@media all and (min-width: 600px) {
  /* We tell both sidebars to share a row */
  .aside { flex: 1 auto; }
}

/* Large screens */
@media all and (min-width: 800px) {
  /* We invert order of first sidebar and main
   * And tell the main element to take twice as much width as the other two sidebars 
   */
  .main { flex: 3 0px; }
  .aside-1 { order: 1; }
  .main    { order: 2; }
  .aside-2 { order: 3; }
  .footer  { order: 4; }
}
```

### Flexbox tricks!

[flexbox](https://css-tricks.com/tag/flexbox/) [images](https://css-tricks.com/tag/images/)

**Article**
on
Oct 3, 2019 

### [Adaptive Photo Layout with Flexbox](https://css-tricks.com/adaptive-photo-layout-with-flexbox/)

[![](https://i0.wp.com/css-tricks.com/wp-content/cache/breeze-extra/gravatars/xekW7bvN-80x80.jpeg?resize=80%2C80&ssl=1)](https://css-tricks.com/author/timvandamme/) 
[Tim Van Damme](https://css-tricks.com/author/timvandamme/)

[flexbox](https://css-tricks.com/tag/flexbox/)

**Article**
on
Oct 8, 2020 

### [Balancing on a Pivot with Flexbox](https://css-tricks.com/balancing-on-a-pivot-with-flexbox/)

[![](https://i0.wp.com/css-tricks.com/wp-content/cache/breeze-extra/gravatars/me-80x80.jpg?resize=80%2C80&ssl=1)](https://css-tricks.com/author/j-merkenich/) 
[Julian Merkenich](https://css-tricks.com/author/j-merkenich/)

[ellipsis](https://css-tricks.com/tag/ellipsis/) [overflow](https://css-tricks.com/tag/overflow/) [text-overflow](https://css-tricks.com/tag/text-overflow/)

**Link**
on
Jul 21, 2020 

### [Using Flexbox and text ellipsis together](https://css-tricks.com/using-flexbox-and-text-ellipsis-together/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

**Article**
on
Jun 19, 2015 

### [Useful Flexbox Technique: Alignment Shifting Wrapping](https://css-tricks.com/useful-flexbox-technique-alignment-shifting-wrapping/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

[ecommerce](https://css-tricks.com/tag/ecommerce/) [shopify](https://css-tricks.com/tag/shopify/)

**Article**
on
Jan 15, 2016 

### [Designing A Product Page Layout with Flexbox](https://css-tricks.com/designing-a-product-page-layout-with-flexbox/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/d348b21b603ab8dbb124029321608bd74ec16726f7bfaf1a23ea1b613d3e5284)](https://css-tricks.com/author/levin-mejia/) 
[Levin Mejia](https://css-tricks.com/author/levin-mejia/)

**Article**
on
May 11, 2016 

### [Flexbox and Truncated Text](https://css-tricks.com/flexbox-truncated-text/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

[absolute position](https://css-tricks.com/tag/absolute-position/) [flexbox](https://css-tricks.com/tag/flexbox/)

**Link**
on
Mar 18, 2020 

### [Flexbox and absolute positioning](https://css-tricks.com/flexbox-and-absolute-positioning/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

**Article**
on
Mar 10, 2014 

### [Filling the Space in the Last Row with Flexbox](https://css-tricks.com/filling-space-last-row-flexbox/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

### Browser support

This browser support data is from [Caniuse](http://caniuse.com/#feat=flexbox), which has more detail. A number indicates that browser supports the feature at that version and up.

#### Desktop

| Chrome | Firefox | IE | Edge | Safari |
| --- | --- | --- | --- | --- |
| 21\* | 28 | 11 | 12 | 6.1\* |

#### Mobile / Tablet

| Android Chrome | Android Firefox | Android | iOS Safari |
| --- | --- | --- | --- |
| 144 | 147 | 4.4 | 7.0-7.1\* |

### Bugs

Flexbox is certainly not without its bugs. The best collection of them I’ve seen is Philip Walton and Greg Whitworth’s [Flexbugs](https://github.com/philipwalton/flexbugs). It’s an open-source place to track all of them, so I think it’s best to just link to that.

### Related properties

[align-content](https://css-tricks.com/tag/align-content/) [flexbox](https://css-tricks.com/tag/flexbox/)

**Almanac**
on
Apr 17, 2013 

### [align-content](https://css-tricks.com/almanac/properties/a/align-content/)

[`.element { align-content: space-around; }`](https://css-tricks.com/almanac/properties/a/align-content/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/60e8a54180b64b3c9e409f0dcc5b4b124b292edc71648ec4401a6bb0c6e106b1)](https://css-tricks.com/author/34cross/) 
[34 Cross](https://css-tricks.com/author/34cross/)

**Almanac**
on
Apr 11, 2013 

### [align-items](https://css-tricks.com/almanac/properties/a/align-items/)

[`.element { align-items: flex-start; }`](https://css-tricks.com/almanac/properties/a/align-items/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/60e8a54180b64b3c9e409f0dcc5b4b124b292edc71648ec4401a6bb0c6e106b1)](https://css-tricks.com/author/34cross/) 
[34 Cross](https://css-tricks.com/author/34cross/)

**Almanac**
on
Apr 19, 2013 

### [align-self](https://css-tricks.com/almanac/properties/a/align-self/)

[`.box { align-self: flex-end; }`](https://css-tricks.com/almanac/properties/a/align-self/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/60e8a54180b64b3c9e409f0dcc5b4b124b292edc71648ec4401a6bb0c6e106b1)](https://css-tricks.com/author/34cross/) 
[34 Cross](https://css-tricks.com/author/34cross/)

**Almanac**
on
Sep 28, 2020 

### [column-gap](https://css-tricks.com/almanac/properties/g/gap/column-gap/)

[`.example { column-gap: 25px; }`](https://css-tricks.com/almanac/properties/g/gap/column-gap/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/a8e040142716a4b44d014d80fbcf99c635b1d8faabfe469b6954a8ef2f168595)](https://css-tricks.com/author/geoffgraham/) 
[Geoff Graham](https://css-tricks.com/author/geoffgraham/)

[display](https://css-tricks.com/tag/display/)

**Almanac**
on
Sep 5, 2011 

### [display](https://css-tricks.com/almanac/properties/d/display/)

[`.element { display: inline-block; }`](https://css-tricks.com/almanac/properties/d/display/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/82ba1e1fe4aca49cdcd66ff387fee32e787abbd0ae6d42750be22ea7c89a5102)](https://css-tricks.com/author/saracope/) 
[Sara Cope](https://css-tricks.com/author/saracope/)

**Almanac**
on
Aug 13, 2020 

### [gap](https://css-tricks.com/almanac/properties/g/gap/)

[`.element { gap: 20px 30px; }`](https://css-tricks.com/almanac/properties/g/gap/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/4526d37720aa1e3389c64d28339da0ca1cbf4f7e6d47ff155f71a565a4db3093)](https://css-tricks.com/author/seyedi/) 
[Mojtaba Seyedi](https://css-tricks.com/author/seyedi/)

**Almanac**
on
Dec 2, 2020 

### [justify-items](https://css-tricks.com/almanac/properties/j/justify-items/)

[`.element { justify-items: center; }`](https://css-tricks.com/almanac/properties/j/justify-items/)

[![](https://i0.wp.com/css-tricks.com/wp-content/cache/breeze-extra/gravatars/lJ1-nP6Q_400x400-80x80.jpg?resize=80%2C80&ssl=1)](https://css-tricks.com/author/mohitkhare/) 
[Mohit Khare](https://css-tricks.com/author/mohitkhare/)

**Almanac**
on
Aug 31, 2011 

### [flex](https://css-tricks.com/almanac/properties/f/flex/)

[`.element { flex: 1 1 100px; }`](https://css-tricks.com/almanac/properties/f/flex/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/82ba1e1fe4aca49cdcd66ff387fee32e787abbd0ae6d42750be22ea7c89a5102)](https://css-tricks.com/author/saracope/) 
[Sara Cope](https://css-tricks.com/author/saracope/)

**Almanac**
on
Apr 19, 2013 

### [flex-basis](https://css-tricks.com/almanac/properties/f/flex-basis/)

[`.element { flex-basis: 100px; }`](https://css-tricks.com/almanac/properties/f/flex-basis/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/60e8a54180b64b3c9e409f0dcc5b4b124b292edc71648ec4401a6bb0c6e106b1)](https://css-tricks.com/author/34cross/) 
[34 Cross](https://css-tricks.com/author/34cross/)

**Almanac**
on
Apr 17, 2013 

### [flex-direction](https://css-tricks.com/almanac/properties/f/flex-direction/)

[`.element { flex-direction: column-reverse; }`](https://css-tricks.com/almanac/properties/f/flex-direction/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/avatar)](https://css-tricks.com/author/)

**Almanac**
on

### [flex-flow](https://css-tricks.com/almanac/properties/f/flex-flow/)

[`.element { flex-flow: row wrap; }`](https://css-tricks.com/almanac/properties/f/flex-flow/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/avatar)](https://css-tricks.com/author/)

[flex-grow](https://css-tricks.com/tag/flex-grow/) [flexbox](https://css-tricks.com/tag/flexbox/)

**Almanac**
on
Apr 18, 2013 

### [flex-grow](https://css-tricks.com/almanac/properties/f/flex-grow/)

[`.flex-item { flex-grow: 2; }`](https://css-tricks.com/almanac/properties/f/flex-grow/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

**Almanac**
on
Apr 19, 2013 

### [flex-shrink](https://css-tricks.com/almanac/properties/f/flex-shrink/)

[`.element { flex-shrink: 2; }`](https://css-tricks.com/almanac/properties/f/flex-shrink/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/avatar)](https://css-tricks.com/author/)

**Almanac**
on
Apr 17, 2013 

### [flex-wrap](https://css-tricks.com/almanac/properties/f/flex-wrap/)

[`.example { flex-wrap: wrap; }`](https://css-tricks.com/almanac/properties/f/flex-wrap/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

**Almanac**
on

### [justify-content](https://css-tricks.com/almanac/properties/j/justify-content/)

[`.element { justify-content: center; }`](https://css-tricks.com/almanac/properties/j/justify-content/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/60e8a54180b64b3c9e409f0dcc5b4b124b292edc71648ec4401a6bb0c6e106b1)](https://css-tricks.com/author/34cross/) 
[34 Cross](https://css-tricks.com/author/34cross/)

**Almanac**
on
Mar 18, 2021 

### [justify-self](https://css-tricks.com/almanac/properties/j/justify-self/)

[`.element { justify-self: stretch; }`](https://css-tricks.com/almanac/properties/j/justify-self/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/a8e040142716a4b44d014d80fbcf99c635b1d8faabfe469b6954a8ef2f168595)](https://css-tricks.com/author/geoffgraham/) 
[Geoff Graham](https://css-tricks.com/author/geoffgraham/)

**Almanac**
on
Sep 28, 2020 

### [row-gap](https://css-tricks.com/almanac/properties/g/gap/row-gap/)

[`.element { row-gap: 2rem; }`](https://css-tricks.com/almanac/properties/g/gap/row-gap/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/a8e040142716a4b44d014d80fbcf99c635b1d8faabfe469b6954a8ef2f168595)](https://css-tricks.com/author/geoffgraham/) 
[Geoff Graham](https://css-tricks.com/author/geoffgraham/)

### More information

- [CSS Flexible Box Layout Module Level 1](https://www.w3.org/TR/css-flexbox-1/) (W3C)
- [A CSS Flexbox Cheatsheet](https://www.digitalocean.com/community/cheatsheets/css-flexbox?utm_medium=content_acq&utm_source=css-tricks&utm_campaign=&utm_content=awareness_bestsellers) (DigitalOcean)
- [Centering Things in CSS With Flexbox](https://www.digitalocean.com/community/tutorials/css-centering-using-flexbox?utm_medium=content_acq&utm_source=css-tricks&utm_campaign=&utm_content=awareness_bestsellers) (DigitalOcean)

**Link**
on
Sep 26, 2013 

### [Solved by Flexbox](https://css-tricks.com/solved-flexbox/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

**Link**
on
Nov 25, 2013 

### [Flexbox Cheat Sheet](https://css-tricks.com/flexbox-cheat-sheet/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

**Link**
on
Dec 23, 2012 

### [Dive Into Flexbox](https://css-tricks.com/dive-into-flexbox/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

[flexbox](https://css-tricks.com/tag/flexbox/) [grid](https://css-tricks.com/tag/grid/) [layout](https://css-tricks.com/tag/layout/)

**Link**
on
Oct 23, 2018 

### [Use Cases for Flexbox](https://css-tricks.com/use-cases-for-flexbox/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

[flexbox](https://css-tricks.com/tag/flexbox/) [grid](https://css-tricks.com/tag/grid/) [layout](https://css-tricks.com/tag/layout/)

**Article**
on
Feb 12, 2019 

### [Quick! What’s the Difference Between Flexbox and Grid?](https://css-tricks.com/quick-whats-the-difference-between-flexbox-and-grid/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

[flexbox](https://css-tricks.com/tag/flexbox/) [grid](https://css-tricks.com/tag/grid/)

**Article**
on
Mar 31, 2017 

### [Does CSS Grid Replace Flexbox?](https://css-tricks.com/css-grid-replace-flexbox/)

[![](https://i0.wp.com/css-tricks.com/wp-content/cache/breeze-extra/gravatars/me-black-white-80x80.jpg?resize=80%2C80&ssl=1)](https://css-tricks.com/author/robinrendle/) 
[Robin Rendle](https://css-tricks.com/author/robinrendle/)

[flexbox](https://css-tricks.com/tag/flexbox/) [grid](https://css-tricks.com/tag/grid/)

**Link**
on
Jun 25, 2020 

### [Grid for layout, flexbox for components](https://css-tricks.com/grid-for-layout-flexbox-for-components/)

[![](https://i0.wp.com/css-tricks.com/wp-content/cache/breeze-extra/gravatars/me-black-white-80x80.jpg?resize=80%2C80&ssl=1)](https://css-tricks.com/author/robinrendle/) 
[Robin Rendle](https://css-tricks.com/author/robinrendle/)

[flexbox](https://css-tricks.com/tag/flexbox/) [grid](https://css-tricks.com/tag/grid/)

**Link**
on
Apr 13, 2016 

### [Should I use Grid or Flexbox?](https://css-tricks.com/use-grid-flexbox/)

[![](https://i0.wp.com/css-tricks.com/wp-content/cache/breeze-extra/gravatars/me-black-white-80x80.jpg?resize=80%2C80&ssl=1)](https://css-tricks.com/author/robinrendle/) 
[Robin Rendle](https://css-tricks.com/author/robinrendle/)

**Article**
on
Jun 22, 2016 

### [Don’t Overthink It (Flexbox) Grids](https://css-tricks.com/dont-overthink-flexbox-grids/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

[logical properties](https://css-tricks.com/tag/logical-properties/) [writing-mode](https://css-tricks.com/tag/writing-mode/)

**Article**
on
Jan 23, 2020 

### [Building Multi-Directional Layouts](https://css-tricks.com/building-multi-directional-layouts/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/04af99c422a2af830c5912efeef0ba0ddbc8af26372158f1598839e6fb31f1eb)](https://css-tricks.com/author/ahmadalfy/) 
[Ahmad El-Alfy](https://css-tricks.com/author/ahmadalfy/)

[flexbox](https://css-tricks.com/tag/flexbox/) [margin](https://css-tricks.com/tag/margin/)

**Article**
on
Jan 6, 2020 

### [How Auto Margins Work in Flexbox](https://css-tricks.com/how-auto-margins-work-in-flexbox/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

[flexbox](https://css-tricks.com/tag/flexbox/)

**Article**
on
Dec 26, 2015 

### [`flex-grow` is weird. Or is it?](https://css-tricks.com/flex-grow-is-weird/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/de3be7ba94c6a1bf0e69c7c0af6de3e54b8bcc53e716f54c972e080745128dac)](https://css-tricks.com/author/mmatuzo/) 
[Manuel Matuzovic](https://css-tricks.com/author/mmatuzo/)

[flex-basis](https://css-tricks.com/tag/flex-basis/) [flex-grow](https://css-tricks.com/tag/flex-grow/) [flex-shrink](https://css-tricks.com/tag/flex-shrink/) [flexbox](https://css-tricks.com/tag/flexbox/)

**Article**
on
Nov 10, 2020 

### [Understanding flex-grow, flex-shrink, and flex-basis](https://css-tricks.com/understanding-flex-grow-flex-shrink-and-flex-basis/)

[![](https://i0.wp.com/css-tricks.com/wp-content/cache/breeze-extra/gravatars/me-black-white-80x80.jpg?resize=80%2C80&ssl=1)](https://css-tricks.com/author/robinrendle/) 
[Robin Rendle](https://css-tricks.com/author/robinrendle/)

[flexbox](https://css-tricks.com/tag/flexbox/) [grid](https://css-tricks.com/tag/grid/) [internet explorer](https://css-tricks.com/tag/internet-explorer/)

**Article**
on
Feb 18, 2019 

### [IE10-Compatible Grid Auto-Placement with Flexbox](https://css-tricks.com/ie10-compatible-grid-auto-placement-with-flexbox/)

[![](https://i0.wp.com/css-tricks.com/wp-content/cache/breeze-extra/gravatars/profile-pic-80x80.png?resize=80%2C80&ssl=1)](https://css-tricks.com/author/bholt/) 
[Brian Holt](https://css-tricks.com/author/bholt/)

**Article**
on
Aug 7, 2012 

### [“Old” Flexbox and “New” Flexbox](https://css-tricks.com/old-flexbox-and-new-flexbox/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

**Article**
on
Feb 18, 2013 

### [Using Flexbox: Mixing Old and New for the Best Browser Support](https://css-tricks.com/using-flexbox/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

### More sources

- [CSS Flexible Box Layout Module Level 1](https://www.w3.org/TR/css-flexbox-1/) (W3C)
- [A CSS Flexbox Cheatsheet](https://www.digitalocean.com/community/cheatsheets/css-flexbox?utm_medium=content_acq&utm_source=css-tricks&utm_campaign=&utm_content=awareness_bestsellers) (DigitalOcean)
- [Centering Things in CSS With Flexbox](https://www.digitalocean.com/community/tutorials/css-centering-using-flexbox?utm_medium=content_acq&utm_source=css-tricks&utm_campaign=&utm_content=awareness_bestsellers) (DigitalOcean)
- [CSS Layout: Flexbox](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Flexbox) (MDN)
- [Use Cases for Flexbox](https://www.smashingmagazine.com/2018/10/flexbox-use-cases/) (Smashing Magazine)