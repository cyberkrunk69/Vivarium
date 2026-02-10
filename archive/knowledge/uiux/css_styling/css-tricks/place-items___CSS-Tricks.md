# place-items | CSS-Tricks

Source: https://css-tricks.com/almanac/properties/p/place-items/

---

The `place-items` property in CSS is shorthand for the `align-items` and `justify-items` properties, combining them into a single declaration.

A common usage is doing *horizontal and vertical* centering with [Grid](https://css-tricks.com/snippets/css/complete-guide-grid/):

```
.center-inside-of-me {
  display: grid;
  place-items: center;
}
```

These properties have gained use with the introduction of Flexbox and Grid layouts, but are also applied to:

- Block-level boxes
- Absolutely-positioned boxes
- Static-position of absolutely positioned boxes
- Table cells

### Syntax

The property accepts dual values, the first for `align-items` and the second for `justify-items`. As a refresher, `align-items` aligns content along the vertical (column) axis whereas `justify-items` aligns along the horizontal (row) axis.

```
.item {
  display: grid;
  place-items: start center;
}
```

This is the same as writing:

```
.item {
  display: grid;
  align-items: start;
  justify-items: center;
}
```

If only one value is provided, then it sets both properties. For example, this:

```
.item {
  display: grid;
  place-items: start;
}
```

…is the same as writing this:

```
.item {
  display: grid;
  align-items: start;
  justify-items: start;
}
```

### Accepted Values

What makes this property interesting is that it behaves differently based on the context it is used. For example, some values only apply to Flexbox and will not work in a Grid setting. Additionally, some values apply to the `align-items` property where others apply to the `justify-items` side.

Further, the values themselves can be thought of as falling into a number of types of alignment: contextual, [distribution](https://drafts.csswg.org/css-align/#distribution-values), [positional](https://drafts.csswg.org/css-align/#positional-values) (which becomes [self-positional](https://drafts.csswg.org/css-align/#typedef-self-position) if directly applied to a child-element in the layout), and [baseline](https://drafts.csswg.org/css-align/#baseline-values).

Rachel Andrew has an excellent [Box Alignment cheat sheet](https://rachelandrew.co.uk/css/cheatsheets/box-alignment) that helps illustrate the effect of the values.

| Value | Type | Description |
| --- | --- | --- |
| `auto` | Contextual | The value adjusts accordingly based on the context of the element. It uses the `justify-items` value of the element’s parent element. If not parent exists or it is applied to an element that is positioned with `absolute`, then the value becomes `normal`. |
| `normal` | Contextual | Takes the default behavior of the layout context where it is applied.  • Block-level layouts: `start` • Absolute-positioning: `start` for replaced absolute elements and `stretch` for all others • Table layouts: Value is ignored • Flexbox layouts: Value is ignored • Grid layouts: `stretch`, unless an aspect ratio or [intrinsic sizing](https://www.w3.org/TR/css-sizing-3/#intrinsic-sizes) is used where it behaves like `start` |
| `stretch` | Distribution | Expands the element to both edges of the container vertically for `align-items` and horizontally for `justify-items`. |
| `start` | Positional | All elements are aligned against each other on the starting (left) edge of the container |
| `end` | Positional | All elements are aligned against each other on the ending (right) edge of the container |
| `center` | Positional | Items are aligned next to each other toward the center of the container |
| `left` | Positional | Items are aligned next to each other toward the left side of the container. If the property is not parallel to a standard top, right, bottom, left axis, then it behaves like `end`. |
| `right` | Positional | Items are aligned next to each other toward the right side of the container. If the property is not parallel to a standard top, right, bottom, left axis, then it behaves like `start`. |
| `flex-start` | Positional | A flexbox-only value (that falls back to `start`) where items are packed toward the starting edge of the container. |
| `flex-end` | Positional | A flexbox-only value (that falls back to `end`) where items are packed toward the ending edge of the container. |
| `self-start` | Self-Positional | Allows an item in a layout to align itself on the container edge based on its own starting side. Basically overrides what the set value is on the parent. |
| `self-end` | Self-Positional | Allows an item in a layout to align itself on the container edge based on its own ending side instead of inheriting the the container’s positional value. Basically overrides what the set value is on the parent. |
| `first baseline` `last baseline` | Baseline | Aligns all elements within a group (i.e. cells within a row) by matching up their alignment baselines. Defaults to `first` if `baseline` is used on its own. |

### Browser Support

This property is included in the [CSS Box Alignment Model Level 3 specification](https://drafts.csswg.org/css-align-3/#place-items-property).

[Browser support](https://caniuse.com/mdn-css_properties_place-items_flex_context) is pretty wide and stable

#### Grid support

#### Flexbox support

### References

- [**CSS Box Alignment Model Level 3**](https://drafts.csswg.org/css-align-3/#place-items-property) – The official specification where the `place-items` property is initially defined.
- [**Mozilla Developer Network**](https://developer.mozilla.org/en-US/docs/Web/CSS/place-items) – The Mozilla team’s documentation.
- [**Box Alignment Cheat Sheet**](https://rachelandrew.co.uk/css/cheatsheets/box-alignment) – Rachel Andrew’s outline is a super helpful resource for grasping alignment terms and their definitions.

### Related properties

**Almanac**
on
Apr 11, 2013 

### [align-items](https://css-tricks.com/almanac/properties/a/align-items/)

[`.element { align-items: flex-start; }`](https://css-tricks.com/almanac/properties/a/align-items/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/60e8a54180b64b3c9e409f0dcc5b4b124b292edc71648ec4401a6bb0c6e106b1)](https://css-tricks.com/author/34cross/) 
[34 Cross](https://css-tricks.com/author/34cross/)

**Almanac**
on
Dec 2, 2020 

### [justify-items](https://css-tricks.com/almanac/properties/j/justify-items/)

[`.element { justify-items: center; }`](https://css-tricks.com/almanac/properties/j/justify-items/)

[![](https://i0.wp.com/css-tricks.com/wp-content/cache/breeze-extra/gravatars/lJ1-nP6Q_400x400-80x80.jpg?resize=80%2C80&ssl=1)](https://css-tricks.com/author/mohitkhare/) 
[Mohit Khare](https://css-tricks.com/author/mohitkhare/)

**Almanac**
on
Mar 18, 2021 

### [justify-self](https://css-tricks.com/almanac/properties/j/justify-self/)

[`.element { justify-self: stretch; }`](https://css-tricks.com/almanac/properties/j/justify-self/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/a8e040142716a4b44d014d80fbcf99c635b1d8faabfe469b6954a8ef2f168595)](https://css-tricks.com/author/geoffgraham/) 
[Geoff Graham](https://css-tricks.com/author/geoffgraham/)