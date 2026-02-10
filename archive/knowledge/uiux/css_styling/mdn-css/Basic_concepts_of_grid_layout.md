# Basic concepts of grid layout

Source: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout/Basic_concepts_of_grid_layout

---

# Basic concepts of grid layout

[CSS grid layout](/en-US/docs/Web/CSS/Guides/Grid_layout) introduces a two-dimensional grid system to CSS. Grids can be used to lay out major page areas or small user interface elements. This guide introduces the CSS grid layout and the terminology that is part of the CSS grid layout specification. The features shown in this overview will then be explained in greater detail in the other guides in this series.

## [What is a grid?](#what_is_a_grid)

A grid is a set of intersecting horizontal and vertical lines defining rows and columns. Elements can be placed onto the grid within these column and row lines. CSS grid layout has the following features:

### [Fixed and flexible track sizes](#fixed_and_flexible_track_sizes)

You can create a grid with fixed track sizes â using pixels for example. This sets the grid to the specified pixel which fits to the layout you desire. You can also create a grid using flexible sizes with percentages or with the [`fr`](#the_fr_unit) unit designed for this purpose.

### [Item placement](#item_placement)

You can place items into a precise location on the grid using line numbers, names or by targeting an area of the grid. Grid also contains an algorithm to control the placement of items not given an explicit position on the grid.

### [Creation of additional tracks to hold content](#creation_of_additional_tracks_to_hold_content)

You can define an explicit grid with grid layout. The features defined by the grid layout module provide the flexibility to add additional rows and columns when needed. Features such as adding "as many columns that will fit into a container" are included.

### [Alignment control](#alignment_control)

CSS grid layout and [CSS box alignment](/en-US/docs/Web/CSS/Guides/Box_alignment) features enable us to control how the items align once placed into a grid area, and how the entire grid is aligned.

### [Control of overlapping content](#control_of_overlapping_content)

More than one item can be placed into a grid cell or area and they can partially overlap each other. This layering may then be controlled with the [`z-index`](/en-US/docs/Web/CSS/Reference/Properties/z-index) property.

Grid is a powerful layout method that, when combined with other parts of CSS such as [flexbox](/en-US/docs/Web/CSS/Guides/Flexible_box_layout), can help you create layouts that are responsive, flexible, and accessible. It all starts by creating a grid in your **[grid container](/en-US/docs/Glossary/Grid_Container)**.

## [Grid container](#grid_container)

We create a *grid container* by declaring `display: grid` or `display: inline-grid` on an element. As soon as we do this, all *direct children* of that element become *grid items*.

In this example, we have a containing div with a class of `wrapper`. Nested inside are five child elements.

html

```
<div class="wrapper">
  <div>One</div>
  <div>Two</div>
  <div>Three</div>
  <div>Four</div>
  <div>Five</div>
</div>
```

We make the `.wrapper` a grid container using `display: grid;`.

css

```
.wrapper {
  display: grid;
}
```

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

All the direct children are now grid items. In a web browser, you won't see any difference to how these items are displayed before turning them into a grid, as grid has created a single column grid for the items. If you inspect the grid in your browsers developer tools, you may see a small icon next to the value `grid`. Click this and, in most browsers, the grid on this element will be overlaid in the browser window.

![Using the grid highlighter in Firefox DevTools to view a grid](/en-US/docs/Web/CSS/Guides/Grid_layout/Basic_concepts/1-grid-inspector.png)

As you learn and then work with the CSS grid layout, your browser tools will give you a better idea of what is happening with your grids visually.

If we want to start making this more grid-like we need to add column tracks.

## [Grid tracks](#grid_tracks)

We define rows and columns on our grid with the [`grid-template-rows`](/en-US/docs/Web/CSS/Reference/Properties/grid-template-rows) and [`grid-template-columns`](/en-US/docs/Web/CSS/Reference/Properties/grid-template-columns) properties. These define [grid tracks](/en-US/docs/Glossary/Grid_Tracks). A *grid track* is the space between any two adjacent lines on the grid. The image below shows a highlighted track â this is the first-row track in our grid.

![A box with 3 grid items. Above the three items is a solid light green area which is the track.](/en-US/docs/Web/CSS/Guides/Grid_layout/Basic_concepts/1_grid_track.png)

Grid tracks are defined in the [explicit grid](#implicit_and_explicit_grids) by using the `grid-template-columns` and `grid-template-rows` properties or the shorthand `grid` or `grid-template` properties. Tracks are also created in the implicit grid by positioning a grid item outside of the tracks created in the explicit grid.

### [Basic example](#basic_example)

We can add column tracks to our earlier example by adding the `grid-template-columns` property, then defining the size of the column tracks.

We have now created a grid with three 200-pixel-wide column tracks. The child items will be laid out on this grid one in each grid cell.

html

```
<div class="wrapper">
  <div>One</div>
  <div>Two</div>
  <div>Three</div>
  <div>Four</div>
  <div>Five</div>
</div>
```

css

```
.wrapper {
  display: grid;
  grid-template-columns: 200px 200px 200px;
}
```

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

### [The fr unit](#the_fr_unit)

Tracks can be defined using any length unit. Grid also introduces an additional length unit to help us create flexible grid tracks. The [`fr`](/en-US/docs/Web/CSS/Reference/Values/flex_value) unit represents a fraction of the available space in the grid container. The next grid definition would create three equal width tracks that grow and shrink according to the available space.

html

```
<div class="wrapper">
  <div>One</div>
  <div>Two</div>
  <div>Three</div>
  <div>Four</div>
  <div>Five</div>
</div>
```

css

```
.wrapper {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
}
```

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

### [Unequal sizes](#unequal_sizes)

In this example, we create a definition with a `2fr` track then two `1fr` tracks. The available space is split into four. Two parts are given to the first track and one part each to the next two tracks.

html

```
<div class="wrapper">
  <div>One</div>
  <div>Two</div>
  <div>Three</div>
  <div>Four</div>
  <div>Five</div>
</div>
```

css

```
.wrapper {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
}
```

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

### [Mixing flexible and absolute sizes](#mixing_flexible_and_absolute_sizes)

In this final example, we mix absolute sized tracks with `fr` units. The first track is `500px`, so the fixed width is taken away from the available space. The remaining space is divided into three and assigned in proportion to the two flexible tracks.

html

```
<div class="wrapper">
  <div>One</div>
  <div>Two</div>
  <div>Three</div>
  <div>Four</div>
  <div>Five</div>
</div>
```

css

```
.wrapper {
  display: grid;
  grid-template-columns: 500px 1fr 2fr;
}
```

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

### [Track listings with repeat() notation](#track_listings_with_repeat_notation)

Large grids with many tracks can use the [`repeat()`](/en-US/docs/Web/CSS/Reference/Values/repeat) notation, to repeat all or a section of the list of grid tracks. For example the grid definition:

css

```
.wrapper {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
}
```

Can also be written as:

css

```
.wrapper {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}
```

Repeat notation can be used for a part of the list of tracks. In this example, we create an 8-column grid; the initial track is `20px`, then a repeating section of 6 `1fr` tracks, and a final `20px` track.

css

```
.wrapper {
  display: grid;
  grid-template-columns: 20px repeat(6, 1fr) 20px;
}
```

Repeat notation (`repeat()`) uses the track listing to create a repeating pattern of tracks. In this example, the grid will have 10 tracks; a `1fr` track is followed by a `2fr` track, with this pattern being repeated five times.

css

```
.wrapper {
  display: grid;
  grid-template-columns: repeat(5, 1fr 2fr);
}
```

### [Implicit and explicit grids](#implicit_and_explicit_grids)

When creating our example grid, we specifically defined our column tracks with the [`grid-template-columns`](/en-US/docs/Web/CSS/Reference/Properties/grid-template-columns) property, with the grid creating rows as needed to fit the content. The columns define the explicit grid while the rows are part of the implicit grid.

The *explicit grid* consists of rows and columns defined with [`grid-template-columns`](/en-US/docs/Web/CSS/Reference/Properties/grid-template-columns) or [`grid-template-rows`](/en-US/docs/Web/CSS/Reference/Properties/grid-template-rows). The
*implicit grid* extends the defined explicit grid when content is placed outside of that grid, such as into the rows by drawing additional grid lines.

If you place something outside of the defined grid or, due to the amount of content, more grid tracks are needed, then the grid creates rows and columns in the *implicit grid*. These implicit tracks are auto-sized by default, meaning the size of the created rows or columns is influenced by both their content and by the available free space within the grid container. The `auto` keyword allows the generated tracks to accommodate content while also sharing any remaining space.

You can also define a set size for tracks created in the implicit grid with the [`grid-auto-rows`](/en-US/docs/Web/CSS/Reference/Properties/grid-auto-rows) and [`grid-auto-columns`](/en-US/docs/Web/CSS/Reference/Properties/grid-auto-columns) properties.

In this example, we set `grid-auto-rows: 200px`, ensuring the tracks created in this implicit grid are `200px` tall.

html

```
<div class="wrapper">
  <div>One</div>
  <div>Two</div>
  <div>Three</div>
  <div>Four</div>
  <div>Five</div>
</div>
```

css

```
.wrapper {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-auto-rows: 200px;
}
```

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

### [Track sizing and minmax](#track_sizing_and_minmax)

When setting up an explicit grid or defining the sizing for automatically created rows or columns we may want to give tracks a minimum size, but also ensure they expand to fit any content that is added. For example, we may want our rows to never collapse smaller than 100 pixels, but if our content stretches to 300 pixels in height, then we would like the row to stretch to that height. This is solved by the [`minmax()`](/en-US/docs/Web/CSS/Reference/Values/minmax) function.

In this example, we use `minmax()` within the `grid-auto-rows` property value. By setting `grid-auto-rows: minmax(100px, auto);`, automatically created rows will be a minimum of `100px` tall, and have a maximum of `auto`. Setting `auto` as the maximum value allows the track to grow to accommodate its content (up to its `max-content` size) while also sharing any available free space within the grid container.

css

```
.wrapper {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-auto-rows: minmax(100px, auto);
}
```

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

```
<div class="wrapper">
  <div>One</div>
  <div>
    Two
    <p>We have some more content.</p>
    <p>This makes me taller than 100 pixels.</p>
  </div>
  <div>Three</div>
  <div>Four</div>
  <div>Five</div>
</div>
```

## [Grid lines](#grid_lines)

It should be noted that when we define a grid we define the grid tracks, not the lines. Grid then gives us numbered lines to use when positioning items. In our three column, two row grid we have four column lines.

![Diagram showing numbered grid lines.](/en-US/docs/Web/CSS/Guides/Grid_layout/Basic_concepts/1_diagram_numbered_grid_lines.png)

Lines are numbered according to the writing mode of the document. In a left-to-right language, line 1 is on the left-hand side of the grid. In a right-to-left language, it is on the right-hand side of the grid. Lines can also be named, which is discussed in the [grid layout using named grid lines](/en-US/docs/Web/CSS/Guides/Grid_layout/Named_grid_lines) guide.

### [Positioning items against lines](#positioning_items_against_lines)

The following example demonstrates basic line-based placement; when placing an item, we target the line rather than the track. We explore this in greater detail in the [grid layout using line-based placement](/en-US/docs/Web/CSS/Guides/Grid_layout/Line-based_placement) guide.

In this example, the first two items on our three column track grid are placed using the [`grid-column-start`](/en-US/docs/Web/CSS/Reference/Properties/grid-column-start), [`grid-column-end`](/en-US/docs/Web/CSS/Reference/Properties/grid-column-end), [`grid-row-start`](/en-US/docs/Web/CSS/Reference/Properties/grid-row-start) and [`grid-row-end`](/en-US/docs/Web/CSS/Reference/Properties/grid-row-end) properties. Working from left to right, the first item is placed against column line 1, and spans to column line 4, which in our case is the far-right line on the grid. It begins at row line 1 and ends at row line 3, therefore spanning two row tracks.

The second item starts on grid column line 1, and spans one track. This is the default, so we do not need to specify the end line. It also spans two row tracks from row line 3 to row line 5. The other items will place themselves into empty spaces on the grid.

html

```
<div class="wrapper">
  <div class="box1">One</div>
  <div class="box2">Two</div>
  <div class="box3">Three</div>
  <div class="box4">Four</div>
  <div class="box5">Five</div>
</div>
```

css

```
.wrapper {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-auto-rows: 100px;
}

.box1 {
  grid-column-start: 1;
  grid-column-end: 4;
  grid-row-start: 1;
  grid-row-end: 3;
}

.box2 {
  grid-column-start: 1;
  grid-row-start: 3;
  grid-row-end: 5;
}
```

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

Use the grid inspector in your developer tools to see how the items are positioned against the lines of the grid.

### [Line-positioning shorthands](#line-positioning_shorthands)

The longhand values used above can be compressed onto one line for columns with the [`grid-column`](/en-US/docs/Web/CSS/Reference/Properties/grid-column) shorthand, and one line for rows with the [`grid-row`](/en-US/docs/Web/CSS/Reference/Properties/grid-row) shorthand. The following example would give the same positioning as in the previous code, but with far less CSS. The value before the forward slash character (`/`) is the start line, the value after the end line.

You can omit the end value if the area only spans one track.

css

```
.wrapper {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-auto-rows: 100px;
}

.box1 {
  grid-column: 1 / 4;
  grid-row: 1 / 3;
}

.box2 {
  grid-column: 1;
  grid-row: 3 / 5;
}
```

## [Grid cells](#grid_cells)

A *grid cell* is the smallest unit on a grid. Conceptually it is like a table cell. As we saw in our earlier examples, once a grid is defined as a parent the child items will lay themselves out in one cell each of the defined grid. In the below image, the first cell of the grid is highlighted.

![The first cell of the grid highlighted](/en-US/docs/Web/CSS/Guides/Grid_layout/Basic_concepts/1_grid_cell.png)

## [Grid areas](#grid_areas)

Items can span one or more cells both by row or by column, and this creates a *grid area*. Grid areas must be rectangular â it isn't possible to create an L-shaped area for example. The highlighted grid area spans two row and two column tracks.

![A grid area](/en-US/docs/Web/CSS/Guides/Grid_layout/Basic_concepts/1_grid_area.png)

## [Gutters](#gutters)

*Gutters* or *alleys* between grid cells can be created using the [`column-gap`](/en-US/docs/Web/CSS/Reference/Properties/column-gap) and [`row-gap`](/en-US/docs/Web/CSS/Reference/Properties/row-gap) properties, or the shorthand [`gap`](/en-US/docs/Web/CSS/Reference/Properties/gap). In the below example, we add a 10-pixel gap between columns and a `1em` gap between rows.

css

```
.wrapper {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  column-gap: 10px;
  row-gap: 1em;
}
```

html

```
<div class="wrapper">
  <div>One</div>
  <div>Two</div>
  <div>Three</div>
  <div>Four</div>
  <div>Five</div>
</div>
```

```
* {
  box-sizing: border-box;
}

.wrapper {
  column-gap: 10px;
  row-gap: 1em;
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

Any space used by gaps will be accounted for before space is assigned to the flexible length `fr` tracks, and gaps act for sizing purposes like a regular grid track, however you cannot place anything into a gap. In terms of line-based positioning, the gap acts like a thick, transparent line.

## [Nesting grids](#nesting_grids)

A grid item can become a grid container. In the following example, we extend the three-column grid with two positioned items seen earlier, adding sub-items to the first grid item. As these nested items are not direct children of the grid they do not participate in grid layout and so display in a normal document flow.

![Nested grid in flow](/en-US/docs/Web/CSS/Guides/Grid_layout/Basic_concepts/1_nested_grids_in_flow.png)

### [Nesting without subgrid](#nesting_without_subgrid)

If we set `box1` to `display: grid`, we can give it a track definition and it too will become a grid. The items then lay out on this new grid.

css

```
.box1 {
  grid-column-start: 1;
  grid-column-end: 4;
  grid-row-start: 1;
  grid-row-end: 3;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}
```

html

```
<div class="wrapper">
  <div class="box box1">
    <div class="nested">a</div>
    <div class="nested">b</div>
    <div class="nested">c</div>
  </div>
  <div class="box box2">Two</div>
  <div class="box box3">Three</div>
  <div class="box box4">Four</div>
  <div class="box box5">Five</div>
</div>
```

css

```
* {
  box-sizing: border-box;
}

.wrapper {
  border: 2px solid #f76707;
  border-radius: 5px;
  gap: 3px;
  background-color: #fff4e6;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}

.box {
  border: 2px solid #ffa94d;
  border-radius: 5px;
  background-color: #ffd8a8;
  padding: 1em;
  color: #d9480f;
}

.box1 {
  grid-column: 1 / 4;
}

.nested {
  border: 2px solid #ffec99;
  border-radius: 5px;
  background-color: #fff9db;
  padding: 1em;
}
```

In this case the nested grid has no relationship to the parent. As you can see in the example it has not inherited the [`gap`](/en-US/docs/Web/CSS/Reference/Properties/gap) of the parent and the lines in the nested grid do not align to the lines in the parent grid.

### [Subgrid](#subgrid)

In addition to regular grids, we can create *subgrid*. The `subgrid` value lets us create nested grids that use the track definition of the parent grid.

To use them, we edit the above nested grid example to change the track definition of `grid-template-columns: repeat(3, 1fr)`, to `grid-template-columns: subgrid`. The nested grid then uses the parent grid tracks to lay out items.

css

```
.box1 {
  grid-column-start: 1;
  grid-column-end: 4;
  grid-row-start: 1;
  grid-row-end: 3;
  display: grid;
  grid-template-columns: subgrid;
}
```

## [Layering items with z-index](#layering_items_with_z-index)

Grid items can occupy the same cell, and in this case we can use the [`z-index`](/en-US/docs/Web/CSS/Reference/Properties/z-index) property to control the order in which overlapping items stack.

### [Overlapping without z-index](#overlapping_without_z-index)

If we return to our example with items positioned by line number, we can change this to make two items overlap.

html

```
<div class="wrapper">
  <div class="box box1">One</div>
  <div class="box box2">Two</div>
  <div class="box box3">Three</div>
  <div class="box box4">Four</div>
  <div class="box box5">Five</div>
</div>
```

css

```
.wrapper {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-auto-rows: 100px;
}

.box1 {
  grid-column-start: 1;
  grid-column-end: 4;
  grid-row-start: 1;
  grid-row-end: 3;
}

.box2 {
  grid-column-start: 1;
  grid-row-start: 2;
  grid-row-end: 4;
}
```

```
* {
  box-sizing: border-box;
}

.wrapper {
  border: 2px solid #f76707;
  border-radius: 5px;
  background-color: #fff4e6;
}

.box {
  border: 2px solid #ffa94d;
  border-radius: 5px;
  background-color: #ffd8a8;
  padding: 1em;
  color: #d9480f;
}
```

The item `box2` is now overlapping `box1`, it displays on top as it comes later in the source order.

### [Controlling the order](#controlling_the_order)

We can control the order in which items stack up by using the `z-index` property - just like positioned items. If we give `box2` a lower `z-index` than `box1` it will display below `box1` in the stack.

css

```
.wrapper {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-auto-rows: 100px;
}

.box1 {
  grid-column-start: 1;
  grid-column-end: 4;
  grid-row-start: 1;
  grid-row-end: 3;
  z-index: 2;
}

.box2 {
  grid-column-start: 1;
  grid-row-start: 2;
  grid-row-end: 4;
  z-index: 1;
}
```

```
<div class="wrapper">
  <div class="box box1">One</div>
  <div class="box box2">Two</div>
  <div class="box box3">Three</div>
  <div class="box box4">Four</div>
  <div class="box box5">Five</div>
</div>
```

```
* {
  box-sizing: border-box;
}

.wrapper {
  border: 2px solid #f76707;
  border-radius: 5px;
  background-color: #fff4e6;
}

.box {
  border: 2px solid #ffa94d;
  border-radius: 5px;
  background-color: #ffd8a8;
  padding: 1em;
  color: #d9480f;
}
```

## [Next steps](#next_steps)

In this overview, we took a very quick look at the possibilities of grid layouts. Explore and play with the code examples, and then move on to the guide, [relationship of grid layout with other layout methods](/en-US/docs/Web/CSS/Guides/Grid_layout/Relationship_with_other_layout_methods), where we will really start to dig into the details of CSS grid layout.

## Help improve MDN

Was this page helpful to you?

Yes

No

[Learn how to contribute](/en-US/docs/MDN/Community/Getting_started)

This page was last modified on Dec 16, 2025 by [MDN contributors](/en-US/docs/Web/CSS/Guides/Grid_layout/Basic_concepts/contributors.txt).

[View this page on GitHub](https://github.com/mdn/content/blob/main/files/en-us/web/css/guides/grid_layout/basic_concepts/index.md?plain=1 "Folder: en-us/web/css/guides/grid_layout/basic_concepts (Opens in a new tab)") â¢ [Report a problem with this content](https://github.com/mdn/content/issues/new?template=page-report.yml&mdn-url=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FGuides%2FGrid_layout%2FBasic_concepts&metadata=%3C%21--+Do+not+make+changes+below+this+line+--%3E%0A%3Cdetails%3E%0A%3Csummary%3EPage+report+details%3C%2Fsummary%3E%0A%0A*+Folder%3A+%60en-us%2Fweb%2Fcss%2Fguides%2Fgrid_layout%2Fbasic_concepts%60%0A*+MDN+URL%3A+https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FGuides%2FGrid_layout%2FBasic_concepts%0A*+GitHub+URL%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fblob%2Fmain%2Ffiles%2Fen-us%2Fweb%2Fcss%2Fguides%2Fgrid_layout%2Fbasic_concepts%2Findex.md%0A*+Last+commit%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fcommit%2F33094d735e90b4dcae5733331b79c51fee997410%0A*+Document+last+modified%3A+2025-12-16T15%3A14%3A26.000Z%0A%0A%3C%2Fdetails%3E "This will take you to GitHub to file a new issue.")