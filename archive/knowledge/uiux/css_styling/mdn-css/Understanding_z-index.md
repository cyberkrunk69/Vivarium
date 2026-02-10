# Understanding z-index

Source: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_positioned_layout/Understanding_z-index

---

# Understanding z-index

In the most basic cases, when text, images, and other elements are arranged on the page without overlapping, [HTML](/en-US/docs/Web/HTML) pages can be considered two-dimensional. In such cases, there is a single rendering flow, and all elements are aware of the space taken by others. CSS isn't that simple â CSS positioning, transformation, containment, and other features can cause elements to overlap. In this guide, we introduce the [`z-index`](/en-US/docs/Web/CSS/Reference/Properties/z-index) property, which lets you place elements in front or behind other elements in the same [stacking context](/en-US/docs/Web/CSS/Guides/Positioned_layout/Stacking_context).

## [Layers on the z-axis](#layers_on_the_z-axis)

The elements rendered on a page are comprised of a series of boxes. Each box has a position in three dimensions. In addition to their inline and block positions, boxes lie along a third dimension known as the *z-axis*. Controlling an element's z-axis position becomes especially relevant when element boxes overlap visually. Several property values can cause elements to overlap. The [`z-index`](/en-US/docs/Web/CSS/Reference/Properties/z-index) property provides you a way to control how they overlap!

By default, element boxes are rendered on Layer 0. The `z-index` property allows you to position elements on different layers along the z-axis, in addition to the default rendering layer. Each element's position along the imaginary z-axis (z-index value) is expressed as an integer (positive, negative, or zero) and controls the stacking order during rendering. Greater numbers mean elements are closer to the observer.

If you are not familiar with the term 'z-axis', imagine the page as a stack of layers, each with an assigned number. Layers are rendered in numerical order, with larger numbers appearing on top of smaller numbers (*X* in the table below represents an arbitrary positive integer):

| Layer | Description |
| --- | --- |
| Bottom layer | Farthest from the observer |
| Layer -X | Layers with negative `z-index` values |
| Layer 0 | Default rendering layer |
| Layer X | Layers with positive `z-index` values |
| Top layer | Closest to the observer |

## [Elements in normal flow](#elements_in_normal_flow)

By default, when no `z-index` property is specified, elements are rendered on the default rendering layer (Layer 0).

Consider the following three elements:

html

```
<div id="div1">#1</div>
<div id="div2">#2</div>
<div id="div3">#3</div>
```

Without any positioning properties applied, these elements flow normally in document order, one after another, without overlapping.

css

```
div {
  height: 100px;
  width: 100px;
  outline: 1px dotted;
  line-height: 100px;
  font-size: 40px;
  text-align: center;
  font-family: "Helvetica", "Arial", sans-serif;
}

#div1 {
  background-color: lightpink;
}

#div2 {
  background-color: lightyellow;
}

#div3 {
  background-color: lightgreen;
}
```

## [Default layering behavior](#default_layering_behavior)

To stack the elements, we can [position](/en-US/docs/Web/CSS/Reference/Properties/position#types_of_positioning) them.
If we use absolute positioning to place them in (almost) the same spot, the default stacking order follows the source order: the first element in the HTML appears at the bottom layer and the last element appears at the top layer.

css

```
div {
  position: absolute;
}

#div1 {
  top: 0;
  left: 0;
}

#div2 {
  top: 10px;
  left: 10px;
}

#div3 {
  top: 20px;
  left: 20px;
}
```

## [Rearranging layers](#rearranging_layers)

We can use the CSS [`z-index`](/en-US/docs/Web/CSS/Reference/Properties/z-index) property to position each element along the z-axis, effectively rearranging the stacking order.

By adding `z-index` values, we change the default layer order:

css

```
#div1 {
  z-index: 5;
}

#div2 {
  z-index: -9;
}

#div3 {
  z-index: 0;
}
```

The element with the lowest `z-index` value appears on the bottom layer. The element with the highest `z-index` value appears on the top layer. In this example, `-9` is the lowest value, so `#div2` is behind all the others. The first element in the source order, `#div1`, has the greatest value, so it appears on top of all the others.

## [Impact of stacking contexts](#impact_of_stacking_contexts)

Using `z-index` may appear fairly straightforward at first: a single property assigned a single integer number with a seemingly understandable behavior. When `z-index` is applied to complex hierarchies of HTML elements, many find the resulting behavior hard to understand or predict.

If the elements are not siblings, the stacking behavior can become more complicated because each element may belong to a different [stacking context](/en-US/docs/Web/CSS/Guides/Positioned_layout/Stacking_context). This is shown in the example below.

html

```
<section>
  <div id="div1">#1</div>
  <div id="div2">#2</div>
</section>
<div id="div3">#3</div>
```

css

```
section {
  position: absolute;
  z-index: 2;
}
```

Even though the `z-index` value of `#div3` (`0`) is greater than that of `#div2` (`-9`), `#div2` appears above `#div3` because `#div1` and `#div2` are nested in a separate stacking context created by `<section>`. The `<section>` element and `#div3` are siblings, and since the `<section>` element's z-index is greater than that of `#div3` (`2` versus `0`), `#div3` is placed behind `<section>` and all of `<section>`'s contents. For more in-depth details about the topic, see our [Stacking context](/en-US/docs/Web/CSS/Guides/Positioned_layout/Stacking_context) guide.

## [Conclusion](#conclusion)

As we've seen in this guide, `z-index` provides a way to control how elements stack along z-axis. You learned how the integer values of the `z-index` property can be used to alter the stacking order. However, as demonstrated in the last example, stacking orders can be complicated. Stacking orders follow a series of complex stacking rules to ensure that all browsers stack the same content in the same manner providing consistency and predictability. It's important to understand the [features that create stacking contexts](/en-US/docs/Web/CSS/Guides/Positioned_layout/Stacking_context#features_creating_stacking_contexts) and how [nested stacking contexts](/en-US/docs/Web/CSS/Guides/Positioned_layout/Stacking_context#nested_stacking_contexts) affect layer order.

## [See also](#see_also)

- [Stacking without the `z-index` property](/en-US/docs/Web/CSS/Guides/Positioned_layout/Stacking_without_z-index)
- [Stacking floating elements](/en-US/docs/Web/CSS/Guides/Positioned_layout/Stacking_floating_elements)
- [Using `z-index`](/en-US/docs/Web/CSS/Guides/Positioned_layout/Using_z-index)
- [Stacking context](/en-US/docs/Web/CSS/Guides/Positioned_layout/Stacking_context)
- [CSS positioned layout](/en-US/docs/Web/CSS/Guides/Positioned_layout) module

## Help improve MDN

Was this page helpful to you?

Yes

No

[Learn how to contribute](/en-US/docs/MDN/Community/Getting_started)

This page was last modified on Nov 7, 2025 by [MDN contributors](/en-US/docs/Web/CSS/Guides/Positioned_layout/Understanding_z-index/contributors.txt).

[View this page on GitHub](https://github.com/mdn/content/blob/main/files/en-us/web/css/guides/positioned_layout/understanding_z-index/index.md?plain=1 "Folder: en-us/web/css/guides/positioned_layout/understanding_z-index (Opens in a new tab)") â¢ [Report a problem with this content](https://github.com/mdn/content/issues/new?template=page-report.yml&mdn-url=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FGuides%2FPositioned_layout%2FUnderstanding_z-index&metadata=%3C%21--+Do+not+make+changes+below+this+line+--%3E%0A%3Cdetails%3E%0A%3Csummary%3EPage+report+details%3C%2Fsummary%3E%0A%0A*+Folder%3A+%60en-us%2Fweb%2Fcss%2Fguides%2Fpositioned_layout%2Funderstanding_z-index%60%0A*+MDN+URL%3A+https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FGuides%2FPositioned_layout%2FUnderstanding_z-index%0A*+GitHub+URL%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fblob%2Fmain%2Ffiles%2Fen-us%2Fweb%2Fcss%2Fguides%2Fpositioned_layout%2Funderstanding_z-index%2Findex.md%0A*+Last+commit%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fcommit%2F85fccefc8066bd49af4ddafc12c77f35265c7e2d%0A*+Document+last+modified%3A+2025-11-07T15%3A58%3A06.000Z%0A%0A%3C%2Fdetails%3E "This will take you to GitHub to file a new issue.")