# Controlling ratios of flex items along the main axis

Source: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flexible_box_layout/Controlling_ratios_of_flex_items_along_the_main_axis

---

# Controlling ratios of flex items along the main axis

In this guide, we explore the three properties that control the size and flexibility of flex items along the main axis: [`flex-grow`](/en-US/docs/Web/CSS/Reference/Properties/flex-grow), [`flex-shrink`](/en-US/docs/Web/CSS/Reference/Properties/flex-shrink), and [`flex-basis`](/en-US/docs/Web/CSS/Reference/Properties/flex-basis). Fully understanding how these properties work with growing and shrinking items is the key to mastering [CSS flexible box layout](/en-US/docs/Web/CSS/Guides/Flexible_box_layout).

## [A first look](#a_first_look)

Our three properties control the following aspects of a flex item's flexibility:

- `flex-grow`: How much of the positive free space does this item get?
- `flex-shrink`: How much negative free space can be removed from this item?
- `flex-basis`: What is the size of the item before growing and shrinking happens?

The properties are usually expressed using the shorthand [`flex`](/en-US/docs/Web/CSS/Reference/Properties/flex) property. The following code would set the `flex-grow` property to `2`, `flex-shrink` to `1` and `flex-basis` to `auto`.

css

```
.item {
  flex: 2 1 auto;
}
```

## [Important concepts when working on the main axis](#important_concepts_when_working_on_the_main_axis)

To understand the `flex` properties, it is helpful to know the *natural size* of flex items before any growing or shrinking takes place. Additionally, it is important to understand the concept of *free space*, which is the difference between the combined natural size of all the flex items along the main axis and the size of the main axis itself.

### [Flex item sizing](#flex_item_sizing)

To determine how much space is available to lay out flex items, the browser needs to know how big the item is to start with. How is this calculated for items that don't have a width or a height applied using an absolute length unit?

In CSS, the [`min-content`](/en-US/docs/Web/CSS/Reference/Values/min-content) and [`max-content`](/en-US/docs/Web/CSS/Reference/Values/max-content) keywords can be used in place of a [`<length>`](/en-US/docs/Web/CSS/Reference/Values/length) unit. Generally, `min-content` is the smallest size an element can be while still fitting the longest word, and `max-content` is the size the element would need to be to fit all the content without wrapping.

The example below contains two paragraph elements with different strings of text. The first paragraph has a width of `min-content`. Notice that the text has used all of the soft wrapping opportunities available to it, becoming as small as possible without overflowing. This is the `min-content` size of that string. Essentially, the longest word in the string is dictating the size.

The second paragraph, with a value of `max-content`, does the opposite. It grows as large as it needs to be to fit the content without taking soft-wrapping opportunities. It will overflow the box it is in if that container is too narrow.

html

```
<p class="min-content">
  I am sized with min-content and so I will take all of the soft-wrapping
  opportunities.
</p>
<p class="max-content">
  I am sized with max-content and so I will take none of the soft-wrapping
  opportunities.
</p>
```

css

```
.min-content {
  width: min-content;
  border: 2px dotted rgb(96 139 168);
}
.max-content {
  width: max-content;
  border: 2px dotted rgb(96 139 168);
}
```

Remember this behavior and what effects `min-content` and `max-content` have as we explore `flex-grow` and `flex-shrink` later in this article.

### [Positive and negative free space](#positive_and_negative_free_space)

We also need to understand the concept of **positive and negative free space**. When a flex container has *positive free space*, it has more space than required to display the flex items inside the container. For example, a `500px`-wide container, with [`flex-direction`](/en-US/docs/Web/CSS/Reference/Properties/flex-direction) set to `row` and containing three `100px`-wide flex items has `200px` of positive free space. This positive free space can be distributed between the items if filling the container is desired.

![Image showing space left over after items have been displayed.](/en-US/docs/Web/CSS/Guides/Flexible_box_layout/Controlling_flex_item_ratios/basics7.png)

A flex container has *negative free space* when the combined value of the natural sizes of the flex items is larger than the available space in the flex container. If the three flex items in the `500px`-wide container example above are each `200px` wide instead of `100px`, their combined natural width is `600px`, resulting in `100px` of negative free space. This space can be removed from the items to make them fit the container, or the items will overflow.

![The items overflow the container](/en-US/docs/Web/CSS/Guides/Flexible_box_layout/Controlling_flex_item_ratios/ratios1.png)

We need to understand this distribution of positive free space and removal of negative free space to learn about the property components of the `flex` shorthand.

In the following examples, the [`flex-direction`](/en-US/docs/Web/CSS/Reference/Properties/flex-direction) is set to `row`, so the size of items will be determined by their width. We will be calculating the positive and negative free space by comparing the total width of all the items with the container's width. You could also try out each example with `flex-direction: column`. The main axis would then be the column, and you would then compare the height of the items and their container to calculate the positive and negative free space.

## [The `flex-basis` property](#the_flex-basis_property)

The [`flex-basis`](/en-US/docs/Web/CSS/Reference/Properties/flex-basis) property specifies the initial size of a flex item before any distribution of the positive or negative free space happens. The initial value for this property is `auto`. This property accepts the same values as the [`width`](/en-US/docs/Web/CSS/Reference/Properties/width) and [`height`](/en-US/docs/Web/CSS/Reference/Properties/height) properties, and it also accepts the `content` keyword.

If `flex-basis` is set to `auto`, the initial size of the item is the [`<length-percentage>`](/en-US/docs/Web/CSS/Reference/Values/length-percentage) size of the main size, if any was set. For example, if the item has `width: 200px` set, then `200px` would be the `flex-basis` for this item. Percentage values are relative to the flex container's inner main size. If `width: 50%` were set, the `flex-basis` for this item would be half of the container's content-box width. If no such size is set, meaning the item is auto-sized, then `auto` resolves to the size of its content (see the [`min-` and `max-content` sizing](#flex_item_sizing) discussion above), meaning the `flex-basis` is the item's `max-content` size.

This example contains three inflexible flex items, with both `flex-grow` and `flex-shrink` set to `0`. The first item, which has an explicit width of `150px`, takes a `flex-basis` of `150px`, whereas the other two items have no width set and so are sized according to their content width or `max-content`.

html

```
<div class="box">
  <div>One</div>
  <div>Two</div>
  <div>Three</div>
</div>
```

css

```
.box > * {
  border: 2px solid rgb(96 139 168);
  border-radius: 5px;
  background-color: rgb(96 139 168 / 0.2);
  flex: 0 0 auto;
}

.box {
  width: 500px;
  border: 2px dotted rgb(96 139 168);
  display: flex;
}

.box :first-child {
  width: 150px;
}
```

In addition to the `auto` keyword and any other valid [`width`](/en-US/docs/Web/CSS/Reference/Properties/width) value, you can use the `content` keyword as the `flex-basis`. This results in the `flex-basis` being based on the content size, even if there is a `width` set on the item. This creates the same effect as removing any width set and using `auto` as the `flex-basis`. While similar to setting `max-content`, the `content` value enables any [`aspect-ratio`](/en-US/docs/Web/CSS/Reference/Properties/aspect-ratio) to be calculated based on the cross-axis size.

To completely ignore the size of the flex item during space distribution, set `flex-basis` to `0` and set a non-zero `flex-grow` value. Let's learn `flex-grow` before looking at this value in action.

## [The `flex-grow` property](#the_flex-grow_property)

The [`flex-grow`](/en-US/docs/Web/CSS/Reference/Properties/flex-grow) property specifies the **flex grow factor**, which determines how much a flex item will grow relative to the other flex items in the flex container when positive free space is distributed.

If all items have the same `flex-grow` factor, the positive free space will be distributed evenly among them. For this scenario, common practice is to set `flex-grow: 1`, but you could give them any value, such as `88`, `100`, or `1.2`; it is a ratio. If the factor is the same for all the flex items in the container and there is positive free space, that space will be distributed equally.

### [Combining `flex-grow` and `flex-basis`](#combining_flex-grow_and_flex-basis)

Things can get confusing in terms of how `flex-grow` and `flex-basis` interact. Let's consider the case of three flex items of differing content lengths and the following `flex` rules applied to them:

css

```
.class {
  flex: 1 1 auto;
}
```

In this case, the `flex-basis` value is `auto` and the items don't have a width set, so they are auto-sized. This means the `flex-basis` used is the `max-content` size of each item. After laying out the items, there is some positive free space in the flex container, which is shown in the image below as the hatched area; the hatched area is the positive free space that will be distributed between the three items based on their `flex-grow` factors:

![Three items taking a bit more than half the width, with the rest of the width being hatched](/en-US/docs/Web/CSS/Guides/Flexible_box_layout/Controlling_flex_item_ratios/ratios2.png)

We are working with a `flex-basis` equal to the content size. This means the available space to distribute is subtracted from the total available space (the width of the flex container), and the remaining space is then shared equally between the three items. The biggest item remains the largest because it started from a bigger size, even though it has the same amount of spare space as the others:

![The hatched area was divided into thirds, with each item getting a single portion appended.](/en-US/docs/Web/CSS/Guides/Flexible_box_layout/Controlling_flex_item_ratios/ratios3.png)

To create three equally-sized items, even if the original elements have different sizes, set the `flex-basis` component to `0`:

css

```
.class {
  flex: 1 1 0;
}
```

Here, for the purpose of space distribution calculation, we are setting the size of each item to `0`. This means all the space is available for distribution. Since all the items have the same `flex-grow` factor, they each get an equal amount of space. This results in three equal-width flex items.

Try changing the `flex-grow` factor from 1 to 0 in this live example to see the different behavior:

html

```
<div class="box">
  <div>One</div>
  <div>Two</div>
  <div>Three has more content</div>
</div>
```

css

```
.box > * {
  border: 2px solid rgb(96 139 168);
  border-radius: 5px;
  background-color: rgb(96 139 168 / 0.2);
  flex: 1 1 0;
}

.box {
  width: 400px;
  border: 2px dotted rgb(96 139 168);
  display: flex;
}
```

### [Giving items different flex-grow factors](#giving_items_different_flex-grow_factors)

Using `flex-grow` and `flex-basis` together enables us to control individual item sizes by setting different `flex-grow` factors. If we keep the `flex-basis` at `0` so that all the space can be distributed, we can create differently sized flex items by assigning each item a different `flex-grow` factor.

In the example below, we use `1` as the `flex-grow` factor for the first two items and double it to `2` for the third item. With `flex-basis: 0` set on all the items, the available space is distributed as follows:

1. The `flex-grow` factor values of all the sibling flex items are added together (the total is 4 in this case).
2. The positive free space in the flex container is divided by this total value.
3. The free space is distributed according to the individual values. In this case, the first item gets one part, the second one part, and the third two parts. This means that the third item is twice the size of the first and second items.

html

```
<div class="box">
  <div class="one">One</div>
  <div class="two">Two</div>
  <div class="three">Three</div>
</div>
```

css

```
.box > * {
  border: 2px solid rgb(96 139 168);
  border-radius: 5px;
  background-color: rgb(96 139 168 / 0.2);
  flex: 1 1 0;
}

.box {
  border: 2px dotted rgb(96 139 168);
  display: flex;
}

.one {
  flex: 1 1 0;
}

.two {
  flex: 1 1 0;
}

.three {
  flex: 2 1 0;
}
```

Remember that you can use any positive value here. It is the ratio between the items that matters. You can use large numbers or decimals; it's up to you. To test this, change the `flex-grow` values in the above example to `.25`, `.25`, and `.50`. You should see the same result.

## [The `flex-shrink` property](#the_flex-shrink_property)

The [`flex-shrink`](/en-US/docs/Web/CSS/Reference/Properties/flex-shrink) property specifies the **flex shrink factor**, which determines how much the flex item will shrink relative to the rest of the flex items in the flex container when negative free space is distributed.

This property deals with situations where the combined `flex-basis` value of the flex items is too large to fit in the flex container and would otherwise overflow. As long as an item's `flex-shrink` is a positive value, the item will shrink to not overflow the container.

While `flex-grow` is used to add available space to items that can grow, `flex-shrink` is used to remove space to ensure items fit in their container without overflowing.

In this example, there are three `200px`-wide flex items in a `500px`-wide container. With `flex-shrink` set to `0`, the items are not allowed to shrink, causing them to overflow the container.

html

```
<div class="box">
  <div>One</div>
  <div>Two</div>
  <div>Three has more content</div>
</div>
```

css

```
.box > * {
  border: 2px solid rgb(96 139 168);
  border-radius: 5px;
  background-color: rgb(96 139 168 / 0.2);
  flex: 0 0 auto;
  width: 200px;
}

.box {
  width: 500px;
  border: 2px dotted rgb(96 139 168);
  display: flex;
}
```

Change the `flex-shrink` value to `1`; each item will shrink by the same amount, fitting all the items into the container. The negative free space has been proportionally removed from each item, making each flex item smaller than its initial width.

### [Combining `flex-shrink` and `flex-basis`](#combining_flex-shrink_and_flex-basis)

It may appear that `flex-shrink` works in the same way as `flex-grow`, by shrinking rather than growing elements. However, there are some important differences to note.

The concept of [flex base size](#what_determines_the_base_size_of_an_item) affects how negative space is distributed across flex items. The flex shrink factor is multiplied by the flex base size when distributing negative space. This distributes negative space in proportion to how much the item is able to shrink. So, for example, a small item won't shrink to zero before a larger item has been noticeably reduced.

Small items will not shrink to less than their `min-content` size, which is the smallest size the element can be if it used all the available soft wrapping opportunities.

This example demonstrates `min-content` flooring, with the `flex-basis` resolving to the size of the content. If you change the width on the flex container, such as increasing it to `700px`, and then reduce the flex item width, you can see that the first two items will wrap. However, they will never become smaller than their `min-content` size. When the container gets small, the space is only removed from the third item when shrunken further.

html

```
<div class="box">
  <div>Item One</div>
  <div>Item Two</div>
  <div>Item Three has more content and so has a larger size</div>
</div>
```

css

```
.box > * {
  border: 2px solid rgb(96 139 168);
  border-radius: 5px;
  background-color: rgb(96 139 168 / 0.2);
  flex: 1 1 auto;
}

.box {
  border: 2px dotted rgb(96 139 168);
  width: 500px;
  display: flex;
}
```

In practice, this shrinking behavior provides reasonable results. It prevents content from disappearing completely and from becoming smaller than its minimum content size. The above rules are sensible for content that needs to shrink to fit its container.

### [Giving items different `flex-shrink` factors](#giving_items_different_flex-shrink_factors)

In the same way as `flex-grow`, you can give flex items different `flex-shrink` factors. This can help change the default behavior if, for example, you want an item to shrink more or less rapidly than its siblings or to not shrink at all.

In this example, the first item has a `flex-shrink` factor of `1`, the second item `0` (so it won't shrink at all), and the third item `4`, making a total of `5` shrink factors. The third item, therefore, shrinks approximately four times more rapidly than the first, but neither will shrink below their `min-content` width. Play around with the different values: as with `flex-grow`, you can use decimals or larger numbers here as well.

html

```
<div class="box">
  <div class="one">One</div>
  <div class="two">Two</div>
  <div class="three">Three</div>
</div>
```

css

```
.box > * {
  border: 2px solid rgb(96 139 168);
  border-radius: 5px;
  background-color: rgb(96 139 168 / 0.2);
  width: 200px;
}

.box {
  display: flex;
  width: 500px;
  border: 2px dotted rgb(96 139 168);
}

.one {
  flex: 1 1 auto;
}

.two {
  flex: 1 0 auto;
}

.three {
  flex: 2 4 auto;
}
```

## [Mastering sizing of flex items](#mastering_sizing_of_flex_items)

To understand how flex item sizing works, you need to consider the factors below, which we've discussed in these guides:

### [What determines the base size of an item?](#what_determines_the_base_size_of_an_item)

- Is `flex-basis` set to `auto`, and does the item have a width set? If so, the size will be based on that width.
- Is `flex-basis` set to `auto`, but the item doesn't have a width set? If so, the size will be based on the item's content size.
- Is `flex-basis` a length or a percentage, but not zero? If so, this will be the size of the item (floored at `min-content`).
- Is `flex-basis` set to `0`? If so, the item's size will not be taken into consideration for the space-sharing calculation.

### [Is there available space?](#is_there_available_space)

Items can grow only if there is positive free space, and they won't shrink unless there is negative free space.

- If we add up the widths of all the items (or heights if working in a column), is that total **less** than the total width (or height) of the container? If so, there will be positive free space, and `flex-grow` will come into play.
- If we add up the widths of all the items (or heights if working in a column), is that total **more** than the total width (or height) of the container? If so, there will be negative free space, and `flex-shrink` will come into play.

### [What are the other ways to distribute space?](#what_are_the_other_ways_to_distribute_space)

If you do not want space added to the items, remember that you can manage free space between or around items using the alignment properties described in the guide for aligning items in a flex container. The [`justify-content`](/en-US/docs/Web/CSS/Reference/Properties/justify-content) property will enable the distribution of free space between or around items. You can also use auto margins on flex items to absorb space and create gaps between items.

With all these flex properties available to you, you will find that most layout tasks are possible, although it might take a little bit of experimentation at first.

## Help improve MDN

Was this page helpful to you?

Yes

No

[Learn how to contribute](/en-US/docs/MDN/Community/Getting_started)

This page was last modified on Nov 7, 2025 by [MDN contributors](/en-US/docs/Web/CSS/Guides/Flexible_box_layout/Controlling_flex_item_ratios/contributors.txt).

[View this page on GitHub](https://github.com/mdn/content/blob/main/files/en-us/web/css/guides/flexible_box_layout/controlling_flex_item_ratios/index.md?plain=1 "Folder: en-us/web/css/guides/flexible_box_layout/controlling_flex_item_ratios (Opens in a new tab)") â¢ [Report a problem with this content](https://github.com/mdn/content/issues/new?template=page-report.yml&mdn-url=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FGuides%2FFlexible_box_layout%2FControlling_flex_item_ratios&metadata=%3C%21--+Do+not+make+changes+below+this+line+--%3E%0A%3Cdetails%3E%0A%3Csummary%3EPage+report+details%3C%2Fsummary%3E%0A%0A*+Folder%3A+%60en-us%2Fweb%2Fcss%2Fguides%2Fflexible_box_layout%2Fcontrolling_flex_item_ratios%60%0A*+MDN+URL%3A+https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FGuides%2FFlexible_box_layout%2FControlling_flex_item_ratios%0A*+GitHub+URL%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fblob%2Fmain%2Ffiles%2Fen-us%2Fweb%2Fcss%2Fguides%2Fflexible_box_layout%2Fcontrolling_flex_item_ratios%2Findex.md%0A*+Last+commit%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fcommit%2F85fccefc8066bd49af4ddafc12c77f35265c7e2d%0A*+Document+last+modified%3A+2025-11-07T15%3A58%3A06.000Z%0A%0A%3C%2Fdetails%3E "This will take you to GitHub to file a new issue.")