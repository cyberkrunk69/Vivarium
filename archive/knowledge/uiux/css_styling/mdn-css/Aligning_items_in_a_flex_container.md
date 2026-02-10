# Aligning items in a flex container

Source: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flexible_box_layout/Aligning_items_in_a_flex_container

---

# Aligning items in a flex container

One of the reasons flexbox is so useful is that it enables proper alignment, including providing a quick method of vertically centering elements. In this guide, we will take a thorough look at how the alignment and justification properties work in flexbox.

## [Using alignment in flexbox](#using_alignment_in_flexbox)

Flexbox provides several properties to control alignment and spacing, with `align-items` and `justify-content` being fundamental for centering elements. To center an element, we use the [`align-items`](/en-US/docs/Web/CSS/Reference/Properties/align-items) property to align the item on the [cross axis](/en-US/docs/Glossary/Cross_Axis), which in this case is the [block axis](/en-US/docs/Glossary/Flow_relative_values) running vertically. We use [`justify-content`](/en-US/docs/Web/CSS/Reference/Properties/justify-content) to align the item on the main axis, which in this case is the inline axis running horizontally.

![The cross axis is the vertical axis and the main axis is the horizontal axis.](/en-US/docs/Web/CSS/Guides/Flexible_box_layout/Aligning_items/align1.png)

Change the size of the container or nested element in the code example below. The nested element always remains centered.

html

```
<div class="box">
  <div></div>
</div>
```

css

```
.box {
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dotted rgb(96 139 168);
}

.box div {
  width: 100px;
  height: 100px;
  border: 2px solid rgb(96 139 168);
  border-radius: 5px;
  background-color: rgb(96 139 168 / 0.2);
}
```

## [Properties for controlling alignment in flexbox](#properties_for_controlling_alignment_in_flexbox)

The properties we will look at in this guide are as follows.

- [`justify-content`](/en-US/docs/Web/CSS/Reference/Properties/justify-content): Controls the alignment of all items on the main axis.
- [`align-items`](/en-US/docs/Web/CSS/Reference/Properties/align-items): Controls the alignment of all items on the cross axis.
- [`align-self`](/en-US/docs/Web/CSS/Reference/Properties/align-self): Controls the alignment of an individual flex item on the cross axis.
- [`align-content`](/en-US/docs/Web/CSS/Reference/Properties/align-content): Controls the space between flex lines on the cross axis.
- [`gap`](/en-US/docs/Web/CSS/Reference/Properties/gap), [`column-gap`](/en-US/docs/Web/CSS/Reference/Properties/column-gap), and [`row-gap`](/en-US/docs/Web/CSS/Reference/Properties/row-gap): Used to create gaps or gutters between flex items.

We will also discover how auto margins can be used for alignment in flexbox.

## [Aligning items on the cross axis](#aligning_items_on_the_cross_axis)

The [`align-items`](/en-US/docs/Web/CSS/Reference/Properties/align-items) property, set on the flex container, and the [`align-self`](/en-US/docs/Web/CSS/Reference/Properties/align-self) property, set on flex items, control the alignment of flex items on the cross axis. The cross axis runs down the columns if [`flex-direction`](/en-US/docs/Web/CSS/Reference/Properties/flex-direction) is `row` and along the rows if `flex-direction` is `column`.

In this basic flex example, we're using cross-axis alignment. When we add `display: flex` to a container, the child items become flex items arranged in a row. By default, they will all stretch to match the height of the tallest item, as that item defines the height of the items on the cross axis. If the flex container has a height set, the items will stretch to that height, regardless of how much content is in each item.

![Three items, one with additional text causing it to be taller than the others.](/en-US/docs/Web/CSS/Guides/Flexible_box_layout/Aligning_items/align2.png)

![Three items stretched to 200 pixels tall](/en-US/docs/Web/CSS/Guides/Flexible_box_layout/Aligning_items/align3.png)

The reason the items become the same height is that the initial value of `align-items`, the property that controls alignment on the cross axis, is set to `stretch`.

We can use other values to control how the items align:

- `align-items: stretch`
- `align-items: flex-start`
- `align-items: flex-end`
- `align-items: start`
- `align-items: end`
- `align-items: center`
- `align-items: baseline`
- `align-items: first baseline`
- `align-items: last baseline`

In the example below, the value of `align-items` is `stretch`. Try the other values and see how the items align against each other in the flex container.

html

```
<div class="box">
  <div>One</div>
  <div>Two</div>
  <div>Three <br />has <br />extra <br />text</div>
</div>
```

css

```
.box {
  border: 2px dotted rgb(96 139 168);
  display: flex;
  align-items: stretch;
}

.box div {
  width: 100px;
  background-color: rgb(96 139 168 / 0.2);
  border: 2px solid rgb(96 139 168);
  border-radius: 5px;
}
```

### [Aligning one item with `align-self`](#aligning_one_item_with_align-self)

The `align-items` property sets the `align-self` property on all of the flex items as a group. This means you can explicitly declare the [`align-self`](/en-US/docs/Web/CSS/Reference/Properties/align-self) property to target a single item. The `align-self` property accepts all of the same values as `align-items`, plus a value of `auto`, which resets the value to that defined on the flex container.

In this next live example, the flex container has `align-items: flex-start`, which means the items are all aligned to the start of the cross axis. Using the `first-child` selector, the first item is set to `align-self: stretch`. Another item with the `selected` class has `align-self: center` set. Change the value of `align-items` or change the values of `align-self` on the individual items to see how this works.

html

```
<div class="box">
  <div>One</div>
  <div>Two</div>
  <div class="selected">Three</div>
  <div>Four</div>
</div>
```

css

```
.box {
  border: 2px dotted rgb(96 139 168);
  display: flex;
  align-items: flex-start;
  height: 200px;
}
.box div {
  background-color: rgb(96 139 168 / 0.2);
  border: 2px solid rgb(96 139 168);
  border-radius: 5px;
  padding: 20px;
}
.box > *:first-child {
  align-self: stretch;
}
.box .selected {
  align-self: center;
}
```

### [Changing the main axis](#changing_the_main_axis)

Thus far, we have looked at alignment behavior when the `flex-direction` defaults to `row` while working in a language written top to bottom, with a horizontal main axis and vertical cross axis.

![Three items, the first aligned to flex-start, second to center, third to flex-end. Aligning on the vertical axis.](/en-US/docs/Web/CSS/Guides/Flexible_box_layout/Aligning_items/align4.png)

Keeping the same writing mode, when the `flex-direction` is changed to `column`, the `align-items` and `align-self` properties will align the items to the left and right instead of top and bottom; these properties are still aligning items along the cross axis, but the cross axis is now horizontal!

![Three items, the first aligned to flex-start, second to center, third to flex-end. Aligning on the horizontal axis.](/en-US/docs/Web/CSS/Guides/Flexible_box_layout/Aligning_items/align5.png)

You can try this out in the example below, which has a flex container with `flex-direction: column` yet otherwise is exactly the same as the previous example.

html

```
<div class="box">
  <div>One</div>
  <div>Two</div>
  <div class="selected">Three</div>
  <div>Four</div>
</div>
```

css

```
.box {
  border: 2px dotted rgb(96 139 168);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 200px;
}
.box div {
  background-color: rgb(96 139 168 / 0.2);
  border: 2px solid rgb(96 139 168);
  border-radius: 5px;
  padding: 20px;
}
.box > *:first-child {
  align-self: stretch;
}
.box .selected {
  align-self: center;
}
```

## [Aligning content on the cross axis with the `align-content` property](#aligning_content_on_the_cross_axis_with_the_align-content_property)

So far, we have focused on aligning items or individual items inside the area defined by a [flex container](/en-US/docs/Glossary/Flex_Container) containing a single line of flex items. When flex items are allowed to wrap across multiple lines, the [`align-content`](/en-US/docs/Web/CSS/Reference/Properties/align-content) property can be used to control the distribution of space between the lines, also known as **packing flex lines**.

For `align-content` to have an effect, the cross axis dimension (the height in this case) of the flex container must be greater than needed to display the items. It then works on all the items as a set. The `align-content` values dictate what happens with the extra available space and the alignment of the entire set of items within it.

The `align-content` property takes the following values:

- `align-content: flex-start`
- `align-content: flex-end`
- `align-content: start`
- `align-content: end`
- `align-content: center`
- `align-content: space-between`
- `align-content: space-around`
- `align-content: space-evenly`
- `align-content: stretch`
- `align-content: normal` (behaves as `stretch`)
- `align-content: baseline`
- `align-content: first baseline`
- `align-content: last baseline`

In the live example below, the flex container has a height of `400 pixels`, which is more than needed to display our items. The value of `align-content` is `space-between`, which means that the available space is shared out *between* the flex lines, which are placed flush with the start and end of the container on the cross axis.

Try out the other values to see how the `align-content` property works.

html

```
<div class="box">
  <div>One</div>
  <div>Two</div>
  <div>Three</div>
  <div>Four</div>
  <div>Five</div>
  <div>Six</div>
  <div>Seven</div>
  <div>Eight</div>
</div>
```

css

```
.box {
  width: 450px;
  border: 2px dotted rgb(96 139 168);
  display: flex;
  flex-wrap: wrap;
  height: 300px;
  align-content: space-between;
}

.box > * {
  padding: 20px;
  border: 2px solid rgb(96 139 168);
  border-radius: 5px;
  background-color: rgb(96 139 168 / 0.2);
  flex: 1 1 100px;
}

.box div {
  background-color: rgb(96 139 168 / 0.2);
  border: 2px solid rgb(96 139 168);
  border-radius: 5px;
  padding: 20px;
}
```

Once again we can switch our `flex-direction` to `column` in order to see how this property behaves when we are working by column. As before, we need enough space in the cross axis to have some free space after displaying all of the items.

html

```
<div class="box">
  <div>One</div>
  <div>Two</div>
  <div>Three</div>
  <div>Four</div>
  <div>Five</div>
  <div>Six</div>
  <div>Seven</div>
  <div>Eight</div>
</div>
```

css

```
.box {
  display: flex;
  flex-wrap: wrap;
  flex-direction: column;
  width: 400px;
  height: 300px;
  align-content: space-between;
  border: 2px dotted rgb(96 139 168);
}

.box > * {
  padding: 20px;
  border: 2px solid rgb(96 139 168);
  border-radius: 5px;
  background-color: rgb(96 139 168 / 0.2);
  flex: 1 1 100px;
}

.box div {
  background-color: rgb(96 139 168 / 0.2);
  border: 2px solid rgb(96 139 168);
  border-radius: 5px;
  padding: 20px;
}
```

## [Aligning content on the main axis](#aligning_content_on_the_main_axis)

Now that we have seen how alignment works on the cross axis, we can take a look at the main axis. Here we only have one property available to us â `justify-content`. This is because we are only dealing with items as a group on the main axis. With `justify-content` we control what happens with available space, should there be more space than is needed to display the items.

In our initial example with `display: flex` on the container, the items display as a row and all line up at the start of the container. This is due to the initial value of `justify-content` being `normal`, which behaves as `start`. Any available space is placed at the end of the items.

![Three items, each 100 pixels wide in a 500 pixel container. The available space is at the end of the items.](/en-US/docs/Web/CSS/Guides/Flexible_box_layout/Aligning_items/align6.png)

The `baseline` values aren't relevant in this dimension. Otherwise, the `justify-content` property accepts the same values as `align-content`.

- `justify-content: flex-start`
- `justify-content: flex-end`
- `justify-content: start`
- `justify-content: end`
- `justify-content: left`
- `justify-content: right`
- `justify-content: center`
- `justify-content: space-between`
- `justify-content: space-around`
- `justify-content: space-evenly`
- `justify-content: stretch` (behaves as start)
- `justify-content: normal` (behaves as stretch, which behaves as start)

In the example below, the value of `justify-content` is `space-between`. The available space after displaying the items is distributed between the items. The left and right item line up flush with the start and end.

html

```
<div class="box">
  <div>One</div>
  <div>Two</div>
  <div>Three</div>
  <div>Four</div>
</div>
```

css

```
.box {
  display: flex;
  justify-content: space-between;
  border: 2px dotted rgb(96 139 168);
}

.box > * {
  padding: 20px;
  border: 2px solid rgb(96 139 168);
  border-radius: 5px;
  background-color: rgb(96 139 168 / 0.2);
}
```

If the main axis is in the block direction because `flex-direction` is set to `column`, then `justify-content` will distribute space between items in that dimension as long as there is space in the flex container to distribute.

html

```
<div class="box">
  <div>One</div>
  <div>Two</div>
  <div>Three</div>
  <div>Four</div>
</div>
```

css

```
.box {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 300px;
  border: 2px dotted rgb(96 139 168);
}

.box > * {
  padding: 20px;
  border: 2px solid rgb(96 139 168);
  border-radius: 5px;
  background-color: rgb(96 139 168 / 0.2);
}
```

### [Alignment and writing modes](#alignment_and_writing_modes)

Remember that with all of these alignment methods, the values of `start` and `end` are writing mode-aware. If the value of `justify-content` is `start` and the writing mode is left-to-right, as in English, the items will align starting at the left side of the container.

![Three items lined up on the left](/en-US/docs/Web/CSS/Guides/Flexible_box_layout/Aligning_items/basics5.png)

However if the writing mode is right-to-left as in Arabic, the items will line up starting at the right side of the container.

![Three items lined up from the right](/en-US/docs/Web/CSS/Guides/Flexible_box_layout/Aligning_items/basics6.png)

The live example below has the `direction` property set to `rtl` to force a right-to-left flow for our items. You can remove this, or change the values of `justify-content` to see how flexbox behaves when the start of the inline direction is on the right.

html

```
<div class="box">
  <div>One</div>
  <div>Two</div>
  <div>Three</div>
  <div>Four</div>
</div>
```

css

```
.box {
  direction: rtl;
  display: flex;
  justify-content: flex-end;
  border: 2px dotted rgb(96 139 168);
}

.box > * {
  padding: 20px;
  border: 2px solid rgb(96 139 168);
  border-radius: 5px;
  background-color: rgb(96 139 168 / 0.2);
}
```

## [Alignment and `flex-direction`](#alignment_and_flex-direction)

The direction of `start` of the line will also change if you change the `flex-direction` property â for example, using `row-reverse` instead of `row`.

In this next example, `flex-direction: row-reverse` and `justify-content: flex-end` define the direction and location of the items within the flex container. In a left to right language, the items line up on the left. Try changing `flex-direction: row-reverse` to `flex-direction: row`. You will see that the items now move to the right-hand side, and the visual order of the items is reversed.

html

```
<div class="box">
  <div>One</div>
  <div>Two</div>
  <div>Three</div>
  <div>Four</div>
</div>
```

css

```
.box {
  display: flex;
  flex-direction: row-reverse;
  justify-content: flex-end;
  border: 2px dotted rgb(96 139 168);
}

.box > * {
  padding: 20px;
  border: 2px solid rgb(96 139 168);
  border-radius: 5px;
  background-color: rgb(96 139 168 / 0.2);
}
```

While this may all seem a little confusing, the rule to remember is that unless you do something to change it, flex items lay themselves out in the direction that words are laid out in the language of your document along the inline, row axis. `start` and `flex-start` will be where the beginning of a sentence of text would start.

![Diagram showing start on the left and end on the right.](/en-US/docs/Web/CSS/Guides/Flexible_box_layout/Aligning_items/align8.png)

You can switch them to display in the block direction for the language of your document by selecting `flex-direction: column`. Then, `start` and `flex-start` will be where the top of your first paragraph of text would start.

![Diagram showing start at the top and end at the bottom.](/en-US/docs/Web/CSS/Guides/Flexible_box_layout/Aligning_items/align10.png)

If you change `flex-direction` to one of the reverse values, they will lay themselves out from the end axis and in the reverse order to the way words are written in the language of your document. Then, `start` and `flex-start` will change to the end of that axis â so to the location where your lines would wrap if working in rows, or at the end of your last paragraph of text in the block direction.

![Diagram showing start on the right and end on the left.](/en-US/docs/Web/CSS/Guides/Flexible_box_layout/Aligning_items/align9.png)

![Diagram showing end at the top and start at the bottom](/en-US/docs/Web/CSS/Guides/Flexible_box_layout/Aligning_items/align11.png)

## [Using auto margins for main axis alignment](#using_auto_margins_for_main_axis_alignment)

We don't have a `justify-items` or `justify-self` property available to us on the main axis as our items are treated as a group on that axis. However it is possible to do some individual alignment in order to separate an item or a group of items from others by using auto margins along with flexbox.

A common pattern is a navigation bar where some key items are aligned to the right, with the main group on the left. You might think that this should be a use case for a `justify-self` property. However, consider the image below. As an example, take the following image with three items on one side and two on the other. If `justify-self` were to work on flex items and was set on item *d*, it would also change the alignment of item *e* that follows, which may or may not be what is intended.

![Five items, in two groups. Three on the left and two on the right.](/en-US/docs/Web/CSS/Guides/Flexible_box_layout/Aligning_items/align7.png)

Instead, the *d* item can be pushed over using CSS margins.

In this live example, item 4 is separated from the first three items by setting [`margin-left`](/en-US/docs/Web/CSS/Reference/Properties/margin-left) to `auto`, which consumes all the space it can in its axis. This is how centering a block with [`margin`](/en-US/docs/Web/CSS/Reference/Properties/margin) auto left and right works. Each side tries to take as much space as it can, and so the block is pushed into the middle.

In this live example, the flex items are arranged in a row with the basic flex values, and the class `push`, set on the fourth item, applies `margin-left: auto` to that item. Try removing the class on the fourth item or adding the class to a different item to see how it works.

html

```
<div class="box">
  <div>One</div>
  <div>Two</div>
  <div>Three</div>
  <div class="push">Four</div>
  <div>Five</div>
</div>
```

css

```
.box {
  display: flex;
  border: 2px dotted rgb(96 139 168);
}

.box > * {
  padding: 20px;
  border: 2px solid rgb(96 139 168);
  border-radius: 5px;
  background-color: rgb(96 139 168 / 0.2);
}
.push {
  margin-left: auto;
}
```

## [Creating gaps between items](#creating_gaps_between_items)

To create a gap between flex items, use the [`gap`](/en-US/docs/Web/CSS/Reference/Properties/gap), [`column-gap`](/en-US/docs/Web/CSS/Reference/Properties/column-gap), and [`row-gap`](/en-US/docs/Web/CSS/Reference/Properties/row-gap) properties. The [`column-gap`](/en-US/docs/Web/CSS/Reference/Properties/column-gap) property creates gaps between items in a row. The [`row-gap`](/en-US/docs/Web/CSS/Reference/Properties/row-gap) property creates gaps between flex lines when you have [`flex-wrap`](/en-US/docs/Web/CSS/Reference/Properties/flex-wrap) set to `wrap`.

The [`gap`](/en-US/docs/Web/CSS/Reference/Properties/gap) property is a shorthand that sets both `row-gap` and `column-gap`.
The gaps between flex items or flex lines depend on the direction. If the [`flex-direction`](/en-US/docs/Web/CSS/Reference/Properties/flex-direction) property creates rows, the first value defines the gap between flex lines, and the second value defines the gap between items within each line. With columns (when `flex-direction` is set to `column` or `column-reverse`), the first value defines the gap between flex items, and the second value defines the gaps between flex lines.

html

```
<div class="box">
  <div>One</div>
  <div>Two</div>
  <div>Three</div>
  <div>Four</div>
  <div>Five</div>
  <div>Six</div>
</div>
```

css

```
.box {
  display: flex;
  flex-wrap: wrap;
  row-gap: 10px;
  column-gap: 2em;
  border: 2px dotted rgb(96 139 168);
}

.box > * {
  flex: 1;
  padding: 20px;
  border: 2px solid rgb(96 139 168);
  border-radius: 5px;
  background-color: rgb(96 139 168 / 0.2);
}
```

## [See also](#see_also)

- [CSS box alignment](/en-US/docs/Web/CSS/Guides/Box_alignment) module
- [CSS flexible box layout](/en-US/docs/Web/CSS/Guides/Flexible_box_layout) module
- [Box alignment in flexbox](/en-US/docs/Web/CSS/Guides/Box_alignment/In_flexbox)
- [Box alignment in grid layout](/en-US/docs/Web/CSS/Guides/Box_alignment/In_grid_layout)

## Help improve MDN

Was this page helpful to you?

Yes

No

[Learn how to contribute](/en-US/docs/MDN/Community/Getting_started)

This page was last modified on Nov 7, 2025 by [MDN contributors](/en-US/docs/Web/CSS/Guides/Flexible_box_layout/Aligning_items/contributors.txt).

[View this page on GitHub](https://github.com/mdn/content/blob/main/files/en-us/web/css/guides/flexible_box_layout/aligning_items/index.md?plain=1 "Folder: en-us/web/css/guides/flexible_box_layout/aligning_items (Opens in a new tab)") â¢ [Report a problem with this content](https://github.com/mdn/content/issues/new?template=page-report.yml&mdn-url=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FGuides%2FFlexible_box_layout%2FAligning_items&metadata=%3C%21--+Do+not+make+changes+below+this+line+--%3E%0A%3Cdetails%3E%0A%3Csummary%3EPage+report+details%3C%2Fsummary%3E%0A%0A*+Folder%3A+%60en-us%2Fweb%2Fcss%2Fguides%2Fflexible_box_layout%2Faligning_items%60%0A*+MDN+URL%3A+https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FGuides%2FFlexible_box_layout%2FAligning_items%0A*+GitHub+URL%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fblob%2Fmain%2Ffiles%2Fen-us%2Fweb%2Fcss%2Fguides%2Fflexible_box_layout%2Faligning_items%2Findex.md%0A*+Last+commit%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fcommit%2F85fccefc8066bd49af4ddafc12c77f35265c7e2d%0A*+Document+last+modified%3A+2025-11-07T15%3A58%3A06.000Z%0A%0A%3C%2Fdetails%3E "This will take you to GitHub to file a new issue.")