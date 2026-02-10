# CSS Grid Layout Guide | CSS-Tricks

Source: https://css-tricks.com/snippets/css/complete-guide-grid/

---

Our comprehensive guide to CSS grid, focusing on all the settings both for the grid parent container and the grid child elements.

Reference this guide a lot? [Here’s a high-resolution image you can print!](https://css-tricks.com/wp-content/uploads/2022/02/css-grid-poster.png)

---

### Introduction

CSS Grid Layout (aka “Grid” or “CSS Grid”), is a two-dimensional grid-based layout system that, compared to any web layout system of the past, completely changes the way we design user interfaces. CSS has always been used to layout our web pages, but it’s never done a very good job of it. First, we used tables, then floats, positioning and inline-block, but all of these methods were essentially hacks and left out a lot of important functionality (vertical centering, for instance).

[CSS Flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/) is also a very great layout tool, but its one-directional flow has [different use cases](https://css-tricks.com/quick-whats-the-difference-between-flexbox-and-grid/) — and they actually [work together](https://css-tricks.com/css-grid-replace-flexbox/) quite well! CSS Grid is the very first CSS module created specifically to solve the layout problems we’ve all been hacking our way around for as long as we’ve been making websites.

The intention of this guide is to present CSS Grid concepts as they exist in the latest version of the specification. So, we will not cover [the out-of-date Internet Explorer syntax](https://css-tricks.com/css-grid-in-ie-debunking-common-ie-grid-misconceptions/) or other historical hacks.

---

### Key Terms

Before diving into the concepts of CSS Grid, it’s important to understand the terminology. Since the terms involved here are all kinda conceptually similar, it’s easy to confuse them with one another if you don’t first memorize their meanings defined by the CSS Grid specification. But don’t worry, there aren’t many of them.

Grid Container

The element on which `display: grid` is applied. It’s the direct parent of all the grid items. In this example `container` is the grid container.

```
<div class="container">
  <div class="item item-1"> </div>
  <div class="item item-2"> </div>
  <div class="item item-3"> </div>
</div>
```

Grid Item

The children (i.e. *direct* descendants) of the grid container. Here the `item` elements are grid items, but `sub-item` isn’t.

```
<div class="container">
  <div class="item"> </div>
  <div class="item">
    <p class="sub-item"> </p>
  </div>
  <div class="item"> </div>
</div>
```

Grid Line

The dividing lines that make up the structure of the grid. They can be either vertical (“column grid lines”) or horizontal (“row grid lines”) and reside on either side of a row or column. Here the yellow line is an example of a column grid line.

![](https://css-tricks.com/wp-content/uploads/2018/11/terms-grid-line.svg)
Grid Track

The space between two adjacent grid lines. You can think of them as the columns or rows of the grid. Here’s the grid track between the second and third-row grid lines.

![](https://css-tricks.com/wp-content/uploads/2021/08/terms-grid-track.svg)
Grid Area

The total space surrounded by four grid lines. A grid area may be composed of any number of grid cells. Here’s the grid area between row grid lines 1 and 3, and column grid lines 1 and 3.

![](https://css-tricks.com/wp-content/uploads/2018/11/terms-grid-area.svg)
Grid Cell

The space between two adjacent row and two adjacent column grid lines. It’s a single “unit” of the grid. Here’s the grid cell between row grid lines 1 and 2, and column grid lines 2 and 3.

![](https://css-tricks.com/wp-content/uploads/2018/11/terms-grid-cell.svg)

---

### CSS Grid Properties

![](https://css-tricks.com/wp-content/uploads/2018/10/01-container.svg)

#### Parent Container Properties

`display`

Defines the element as a grid container and establishes a new grid formatting context for its contents.

Values:

- **`grid`:** Generates a block-level grid
- **`inline-grid`:** Generates an inline-level grid

```
.container {
  display: grid | inline-grid;
}
```

The ability to pass grid parameters down through nested elements (aka subgrids) has been moved to [CSS Grid Specification Level 2.](https://www.w3.org/TR/css-grid-2/#subgrids) Here’s [a quick explanation](https://css-tricks.com/grid-level-2-and-subgrid/).

`grid-template-*`

Defines the columns and rows of the grid with a space-separated list of values. The values represent the track size, and the space between them represents the grid line.

Values:

- **`<track-size>`:** Can be a length, a percentage, or a fraction of the free space in the grid using the `fr` unit.
- **`<line-name>`:** An arbitrary name of your choosing.

```
.container {
  grid-template-columns: ...  ...;
  /* e.g. 
      1fr 1fr
      minmax(10px, 1fr) 3fr
      repeat(5, 1fr)
      50px auto 100px 1fr
  */
  grid-template-rows: ... ...;
  /* e.g. 
      min-content 1fr min-content
      100px 1fr max-content
  */
}
```

Grid lines are automatically assigned positive numbers from these assignments (`-1` being an alternate for the very last row).

![](https://css-tricks.com/wp-content/uploads/2018/11/template-columns-rows-01.svg)

But you can choose to explicitly name the lines. Note the bracket syntax for the line names:

```
.container {
  grid-template-columns: [first] 40px [line2] 50px [line3] auto [col4-start] 50px [five] 40px [end];
  grid-template-rows: [row1-start] 25% [row1-end] 100px [third-line] auto [last-line];
}
```

![Grid with user named lines](https://css-tricks.com/wp-content/uploads/2018/11/template-column-rows-02.svg)

Note that a line can have more than one name. For example, here the second line will have two names: `row1-end` and `row2-start`:

```
.container {
  grid-template-rows: [row1-start] 25% [row1-end row2-start] 25% [row2-end];
}
```

If your definition contains repeating parts, you can use the [`repeat()` notation](https://www.digitalocean.com/community/tutorials/css-css-grid-layout-repeat-notation?utm_medium=content_acq&utm_source=css-tricks&utm_campaign=&utm_content=awareness_bestsellers) to streamline things:

```
.container {
  grid-template-columns: repeat(3, 20px [col-start]);
}
```

Which is equivalent to this:

```
.container {
  grid-template-columns: 20px [col-start] 20px [col-start] 20px [col-start];
}
```

If multiple lines share the same name, they can be referenced by their line name and count.

```
.item {
  grid-column-start: col-start 2;
}
```

The `fr` unit allows you to set the size of a track as a fraction of the free space of the grid container. For example, this will set each item to one third the width of the grid container:

```
.container {
  grid-template-columns: 1fr 1fr 1fr;
}
```

The free space is calculated *after* any non-flexible items. In this example the total amount of free space available to the `fr` units doesn’t include the 50px:

```
.container {
  grid-template-columns: 1fr 50px 1fr 1fr;
}
```

[Continue Reading](https://css-tricks.com/almanac/properties/g/grid/grid-template-columns/)

`grid-template`

A shorthand for setting `grid-template-rows`, `grid-template-columns`, and `grid-template-areas` in a single declaration.

Values:

- **`none`:**  Sets all three properties to their initial values.
- **`<grid-template-rows>` / `<grid-template-columns`>:** Sets `grid-template-columns` and `grid-template-rows` to the specified values, respectively, and sets `grid-template-areas` to `none`

```
.container {
  grid-template: none | <grid-template-rows> / <grid-template-columns>;
}
```

It also accepts a more complex but quite handy syntax for specifying all three. Here’s an example:

```
.container {
  grid-template:
    [row1-start] "header header header" 25px [row1-end]
    [row2-start] "footer footer footer" 25px [row2-end]
    / auto 50px auto;
}
```

That’s equivalent to this:

```
.container {
  grid-template-rows: [row1-start] 25px [row1-end row2-start] 25px [row2-end];
  grid-template-columns: auto 50px auto;
  grid-template-areas: 
    "header header header" 
    "footer footer footer";
}
```

Since `grid-template` doesn’t reset the *implicit* grid properties (`grid-auto-columns`, `grid-auto-rows`, and `grid-auto-flow`), which is probably what you want to do in most cases, it’s recommended to use the `grid` property instead of `grid-template`.

[Continue Reading](https://css-tricks.com/almanac/properties/g/grid/grid-template/)

`grid-template-areas`

Defines a grid template by referencing the names of the grid areas which are specified with the `grid-area` property. Repeating the name of a grid area causes the content to span those cells. A period signifies an empty cell. The syntax itself provides a visualization of the structure of the grid.

Values:

- **`<grid-area-name>`:** The name of a grid area specified with `grid-area`.
- **`.`:** A period signifies an empty grid cell.
- **`none`:** No grid areas are defined.

```
.container {
  grid-template-areas: 
    "<grid-area-name> | . | none | ..."
    "...";
}
```

Example:

```
.item-a {
  grid-area: header;
}
.item-b {
  grid-area: main;
}
.item-c {
  grid-area: sidebar;
}
.item-d {
  grid-area: footer;
}

.container {
  display: grid;
  grid-template-columns: 50px 50px 50px 50px;
  grid-template-rows: auto;
  grid-template-areas: 
    "header header header header"
    "main main . sidebar"
    "footer footer footer footer";
}
```

That’ll create a grid that’s four columns wide by three rows tall. The entire top row will be composed of the **header** area. The middle row will be composed of two **main** areas, one empty cell, and one **sidebar** area. The last row is all **footer**.

![Example of grid-template-areas](https://css-tricks.com/wp-content/uploads/2018/11/dddgrid-template-areas.svg)

Each row in your declaration needs to have the same number of cells.

You can use any number of adjacent periods to declare a single empty cell. As long as the periods have no spaces between them they represent a single cell.

Notice that you’re not naming lines with this syntax, just areas. When you use this syntax the lines on either end of the areas are actually getting named automatically. If the name of your grid area is ***foo***, the name of the area’s starting row line and starting column line will be ***foo*-start**, and the name of its last row line and last column line will be ***foo*-end**. This means that some lines might have multiple names, such as the far left line in the above example, which will have three names: `header-start`, `main-start`, and `footer-start`.

[Continue Reading](https://css-tricks.com/almanac/properties/g/grid/grid-template-areas/)

`grid`

A shorthand for setting all of the following properties in a single declaration: `grid-template-rows`, `grid-template-columns`, `grid-template-areas`, `grid-auto-rows`, `grid-auto-columns`, and `grid-auto-flow`

You can only specify the explicit or the implicit grid properties in a single grid declaration.

Values:

- **`none`:** Sets all sub-properties to their initial values.
- **`<grid-template>`:** Works the same as the `grid-template` shorthand.
- **`<grid-template-rows> / [ auto-flow && dense? ] <grid-auto-columns>?`:** Sets `grid-template-rows` to the specified value. If the `auto-flow` keyword is to the right of the slash, it sets `grid-auto-flow` to `column`. If the `dense` keyword is specified additionally, the auto-placement algorithm uses a “dense” packing algorithm. If `grid-auto-columns` is omitted, it is set to `auto`.
- **`[ auto-flow && dense? ] <grid-auto-rows>? / <grid-template-columns>`:** Sets `grid-template-columns` to the specified value. If the `auto-flow` keyword is to the left of the slash, it sets `grid-auto-flow` to `row`. If the `dense` keyword is specified additionally, the auto-placement algorithm uses a “dense” packing algorithm. If `grid-auto-rows` is omitted, it is set to `auto`.

Examples:

The following two code blocks are equivalent:

```
.container {
  grid: 100px 300px / 3fr 1fr;
}

.container {
  grid-template-rows: 100px 300px;
  grid-template-columns: 3fr 1fr;
}
```

The following two code blocks are equivalent:

```
.container {
  grid: auto-flow / 200px 1fr;
}

.container {
  grid-auto-flow: row;
  grid-template-columns: 200px 1fr;
}
```

The following two code blocks are equivalent:

```
.container {
  grid: auto-flow dense 100px / 1fr 2fr;
}

.container {
  grid-auto-flow: row dense;
  grid-auto-rows: 100px;
  grid-template-columns: 1fr 2fr;
}
```

And the following two code blocks are equivalent:

```
.container {
  grid: 100px 300px / auto-flow 200px;
}

.container {
  grid-template-rows: 100px 300px;
  grid-auto-flow: column;
  grid-auto-columns: 200px;
}
```

It also accepts a more complex but quite handy syntax for setting everything at once. You specify `grid-template-areas`, `grid-template-rows` and `grid-template-columns`, and all the other sub-properties are set to their initial values. What you’re doing is specifying the line names and track sizes inline with their respective grid areas. This is easiest to describe with an example:

```
.container {
  grid: [row1-start] "header header header" 1fr [row1-end]
        [row2-start] "footer footer footer" 25px [row2-end]
        / auto 50px auto;
}
```

That’s equivalent to this:

```
.container {
  grid-template-areas: 
    "header header header"
    "footer footer footer";
  grid-template-rows: [row1-start] 1fr [row1-end row2-start] 25px [row2-end];
  grid-template-columns: auto 50px auto;    
}
```

[Continue Reading](https://css-tricks.com/almanac/properties/g/grid/)

`justify-items`

Aligns grid items along the *inline (row)* axis (as opposed to `align-items` which aligns along the *block (column)* axis). This value applies to all grid items inside the container.

Values:

- **`stretch` (default):** Fills the whole width of the cell.
- **`start`:** Aligns items to be flush with the start edge of their cell
- **`end`:** Aligns items to be flush with the end edge of their cell
- **`center`:** Aligns items in the center of their cell

```
.container {
  justify-items: start | end | center | stretch;
}
```

Examples:

```
.container {
  justify-items: start;
}
```

![Example of justify-items set to start](https://css-tricks.com/wp-content/uploads/2018/11/justify-items-start.svg)

```
.container {
  justify-items: end;
}
```

![Example of justify-items set to end](https://css-tricks.com/wp-content/uploads/2018/11/justify-items-end.svg)

```
.container {
  justify-items: center;
}
```

![Example of justify-items set to center](https://css-tricks.com/wp-content/uploads/2018/11/justify-items-center.svg)

```
.container {
  justify-items: stretch;
}
```

![Example of justify-items set to stretch](https://css-tricks.com/wp-content/uploads/2018/11/justify-items-stretch.svg)

This behavior can also be set on individual grid items via the `justify-self` property.

[Continue Reading](https://css-tricks.com/almanac/properties/j/justify-items/)

`align-items`

Aligns grid items along the *block (column)* axis (as opposed to `justify-items` which aligns along the *inline (row)* axis). This value applies to all grid items inside the container.

Values:

- **`stretch` (default):** Fills the whole height of the cell (this is the default)
- **`start`:** Aligns items to be flush with the start edge of their cell
- **`end`:** Aligns items to be flush with the end edge of their cell
- **`center`:** Aligns items in the center of their cell
- **`baseline`:** Align items [along text baseline](https://codepen.io/chriscoyier/pen/NWvvPRj). There are modifiers to `baseline` — `first baseline` and `last baseline` which will use the baseline from the first or last line in the case of multi-line text.

```
.container {
  align-items: start | end | center | stretch;
}
```

Examples:

```
.container {
  align-items: start;
}
```

![Example of align-items set to start](https://css-tricks.com/wp-content/uploads/2018/11/align-items-start.svg)

```
.container {
  align-items: end;
}
```

![Example of align-items set to end](https://css-tricks.com/wp-content/uploads/2018/11/align-items-end.svg)

```
.container {
  align-items: center;
}
```

![Example of align-items set to center](https://css-tricks.com/wp-content/uploads/2018/11/align-items-center.svg)

```
.container {
  align-items: stretch;
}
```

![Example of align-items set to stretch](https://css-tricks.com/wp-content/uploads/2018/11/align-items-stretch.svg)

This behavior can also be set on individual grid items via the `align-self` property.

There are also modifier keywords `safe` and `unsafe` (usage is like `align-items: safe end`). The `safe` keyword means “try to align like this, but not if it means aligning an item such that it moves into inaccessible overflow area”, while `unsafe` will allow moving content into inaccessible areas (“data loss”).

[Continue Reading](https://css-tricks.com/almanac/properties/a/align-items/)

`place-items`

`place-items` sets both the `align-items` and `justify-items` properties in a single declaration.

Values:

- **`<align-items>` / `<justify-items>`:** The first value sets `align-items`, the second value `justify-items`. If the second value is omitted, the first value is assigned to both properties.

This can be very useful for super quick multi-directional centering:

```
.center {
  display: grid;
  place-items: center;
}
```

[Continue Reading](https://css-tricks.com/almanac/properties/p/place-items/)

`justify-content`

Sometimes the total size of your grid might be less than the size of its grid container. This could happen if all of your grid items are sized with non-flexible units like `px`. In this case you can set the alignment of the grid within the grid container. This property aligns the grid along the *inline (row)* axis (as opposed to `align-content` which aligns the grid along the *block (column)* axis).

Values:

- **`start`:** Aligns the grid to be flush with the start edge of the grid container.
- **`end`:** Aligns the grid to be flush with the end edge of the grid container.
- **`center`:** Aligns the grid in the center of the grid container.
- **`stretch`:** Resizes the grid items to allow the grid to fill the full width of the grid container.
- **`space-around`:** Places an even amount of space between each grid item, with half-sized spaces on the far ends.
- **`space-between`:** Places an even amount of space between each grid item, with no space at the far ends.
- **`space-evenly`:** Places an even amount of space between each grid item, including the far ends.

```
.container {
  justify-content: start | end | center | stretch | space-around | space-between | space-evenly;    
}
```

Examples:

```
.container {
  justify-content: start;
}
```

![Example of justify-content set to start](https://css-tricks.com/wp-content/uploads/2018/11/justify-content-start.svg)

```
.container {
  justify-content: end;    
}
```

![Example of justify-content set to end](https://css-tricks.com/wp-content/uploads/2018/11/justify-content-end.svg)

```
.container {
  justify-content: center;    
}
```

![Example of justify-content set to center](https://css-tricks.com/wp-content/uploads/2018/11/justify-content-center.svg)

```
.container {
  justify-content: stretch;    
}
```

![Example of justify-content set to stretch](https://css-tricks.com/wp-content/uploads/2018/11/justify-content-stretch.svg)

```
.container {
  justify-content: space-around;    
}
```

![Example of justify-content set to space-around](https://css-tricks.com/wp-content/uploads/2018/11/justify-content-space-around.svg)

```
.container {
  justify-content: space-between;    
}
```

![Example of justify-content set to space-between](https://css-tricks.com/wp-content/uploads/2018/11/justify-content-space-between.svg)

```
.container {
  justify-content: space-evenly;    
}
```

![Example of justify-content set to space-evenly](https://css-tricks.com/wp-content/uploads/2018/11/justify-content-space-evenly.svg)

[Continue Reading](https://css-tricks.com/almanac/properties/j/justify-content/)

`align-content`

Sometimes the total size of your grid might be less than the size of its grid container. This could happen if all of your grid items are sized with non-flexible units like `px`. In this case you can set the alignment of the grid within the grid container. This property aligns the grid along the *block (column)* axis (as opposed to `justify-content` which aligns the grid along the *inline (row)* axis).

Values:

- **`start`:** Aligns the grid to be flush with the start edge of the grid container.
- **`end`:** Aligns the grid to be flush with the end edge of the grid container.
- **`center`:** Aligns the grid in the center of the grid container.
- **`stretch`:** Resizes the grid items to allow the grid to fill the full height of the grid container.
- **`space-around`:** Places an even amount of space between each grid item, with half-sized spaces on the far ends.
- **`space-between`:** Places an even amount of space between each grid item, with no space at the far ends.
- **`space-evenly`:** Places an even amount of space between each grid item, including the far ends.

```
.container {
  align-content: start | end | center | stretch | space-around | space-between | space-evenly;    
}
```

Examples:

```
.container {
  align-content: start;    
}
```

![Example of align-content set to start](https://css-tricks.com/wp-content/uploads/2018/11/align-content-start.svg)

```
.container {
  align-content: end;    
}
```

![Example of align-content set to end](https://css-tricks.com/wp-content/uploads/2018/11/align-content-end.svg)

```
.container {
  align-content: center;    
}
```

![Example of align-content set to center](https://css-tricks.com/wp-content/uploads/2018/11/align-content-center.svg)

```
.container {
  align-content: stretch;    
}
```

![Example of align-content set to stretch](https://css-tricks.com/wp-content/uploads/2018/11/align-content-stretch.svg)

```
.container {
  align-content: space-around;    
}
```

![Example of align-content set to space-around](https://css-tricks.com/wp-content/uploads/2018/11/align-content-space-around.svg)

```
.container {
  align-content: space-between;    
}
```

![Example of align-content set to space-between](https://css-tricks.com/wp-content/uploads/2018/11/align-content-space-between.svg)

```
.container {
  align-content: space-evenly;    
}
```

![Example of align-content set to space-evenly](https://css-tricks.com/wp-content/uploads/2018/11/align-content-space-evenly.svg)

[Continue Reading](https://css-tricks.com/almanac/properties/a/align-content/)

`place-content`

`place-content` sets both the `align-content` and `justify-content` properties in a single declaration.

Values:

- **`<align-content>` / `<justify-content>`:** The first value sets `align-content`, the second value `justify-content`. If the second value is omitted, the first value is assigned to both properties.

[Continue Reading](https://css-tricks.com/almanac/properties/p/place-content/)

`grid-auto-*`

Specifies the size of any auto-generated grid tracks (aka *implicit grid tracks*). Implicit tracks get created when there are more grid items than cells in the grid or when a grid item is placed outside of the explicit grid. (See [The Difference Between Explicit and Implicit Grids](https://css-tricks.com/difference-explicit-implicit-grids/).)

Values:

- **`<track-size>`:** Can be a length, a percentage, or a fraction of the free space in the grid (using the `fr` unit).

```
.container {
  grid-auto-columns: <track-size> ...;
  grid-auto-rows: <track-size> ...;
}
```

To illustrate how implicit grid tracks get created, think about this:

```
.container {
  grid-template-columns: 60px 60px;
  grid-template-rows: 90px 90px;
}
```

![Example of 2x2 grid](https://css-tricks.com/wp-content/uploads/2018/11/grid-auto-columns-rows-01.svg)

This creates a 2×2 grid.

But now imagine you use `grid-column` and `grid-row` to position your grid items like this:

```
.item-a {
  grid-column: 1 / 2;
  grid-row: 2 / 3;
}
.item-b {
  grid-column: 5 / 6;
  grid-row: 2 / 3;
}
```

![Example of implicit tracks](https://css-tricks.com/wp-content/uploads/2018/11/grid-auto-columns-rows-02.svg)

We told `.item-b` to start on column line 5 and end at column line 6, *but we never defined a column line 5 or 6*. Because we referenced lines that don’t exist, implicit tracks with widths of 0 are created to fill in the gaps. We can use `grid-auto-columns` and `grid-auto-rows` to specify the widths of these implicit tracks:

```
.container {
  grid-auto-columns: 60px;
}
```

![grid-auto-columns-rows](https://css-tricks.com/wp-content/uploads/2018/11/grid-auto-columns-rows-03.svg)

[Continue Reading](https://css-tricks.com/almanac/properties/g/grid/grid-auto-columns/)

`grid-auto-flow`

If you have grid items that you don’t explicitly place on the grid, the *auto-placement algorithm* kicks in to automatically place the items. This property controls how the auto-placement algorithm works.

Values:

- **`row`:** Tells the auto-placement algorithm to fill in each row in turn, adding new rows as necessary (default)
- **`column:`** Tells the auto-placement algorithm to fill in each column in turn, adding new columns as necessary
- **`dense`:** Tells the auto-placement algorithm to attempt to fill in holes earlier in the grid if smaller items come up later

```
.container {
  grid-auto-flow: row | column | row dense | column dense;
}
```

Note that **`dense`** only changes the visual order of your items and might cause them to appear out of order, which is bad for accessibility.

Examples:

```
<section class="container">
  <div class="item-a">item-a</div>
  <div class="item-b">item-b</div>
  <div class="item-c">item-c</div>
  <div class="item-d">item-d</div>
  <div class="item-e">item-e</div>
</section>
```

You define a grid with five columns and two rows, and set `grid-auto-flow` to `row` (which is also the default):

```
.container {
  display: grid;
  grid-template-columns: 60px 60px 60px 60px 60px;
  grid-template-rows: 30px 30px;
  grid-auto-flow: row;
}
```

When placing the items on the grid, you only specify spots for two of them:

```
.item-a {
  grid-column: 1;
  grid-row: 1 / 3;
}

.item-e {
  grid-column: 5;
  grid-row: 1 / 3;
}
```

Because we set `grid-auto-flow` to `row`, our grid will look like this. Notice how the three items we didn’t place (**item-b**, **item-c** and **item-d**) flow across the available rows:

![Example of grid-auto-flow set to row](https://css-tricks.com/wp-content/uploads/2018/11/grid-auto-flow-01.svg)

If we instead set `grid-auto-flow` to `column`, **item-b**, **item-c** and **item-d** flow down the columns:

```
.container {
  display: grid;
  grid-template-columns: 60px 60px 60px 60px 60px;
  grid-template-rows: 30px 30px;
  grid-auto-flow: column;
}
```

![Example of grid-auto-flow set to column](https://css-tricks.com/wp-content/uploads/2018/11/grid-auto-flow-02.svg)

[Continue Reading](https://css-tricks.com/almanac/properties/g/grid/grid-auto-flow/)

`gap`
![](https://css-tricks.com/wp-content/uploads/2021/09/gap-1.svg)

[The `gap` property](https://css-tricks.com/almanac/properties/g/gap/) explicitly controls the space between flex items. It applies that spacing *only between items* not on the outer edges. It is a shorthand that combines the `row-gap` and `column-gap` properties.

```
.container {
  display: flex;
  /* ... */
  gap: 10px;
  gap: 10px 20px; /* row-gap column gap */
  row-gap: 10px;
  column-gap: 20px;
}
```

The behavior could be thought of as a *minimum* gutter, as if the gutter is bigger somehow (because of something like `justify-content: space-between;`) then the gap will only take effect if that space would end up smaller.

It is not exclusively for CSS Grid, `gap` works in [Flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/) and multi-column layout as well.

[Continue Reading](https://css-tricks.com/almanac/properties/g/gap/)

![](https://css-tricks.com/wp-content/uploads/2018/10/02-items.svg)

#### Child Item Properties

`grid-column-*`  
`grid-row-*`

Determines a grid item’s location within the grid by referring to specific grid lines. `grid-column-start`/`grid-row-start` is the line where the item begins, and `grid-column-end`/`grid-row-end` is the line where the item ends.

Values:

- **`<line>`:** Can be a number to refer to a numbered grid line, or a name to refer to a named grid line.
- **`span <number>`:** The item will span across the provided number of grid tracks.
- **`span <name>`:** The item will span across until it hits the next line with the provided name.
- **`auto`:** Indicates auto-placement, an automatic span, or a default span of one.

```
.item {
  grid-column-start: <number> | <name> | span <number> | span <name> | auto;
  grid-column-end: <number> | <name> | span <number> | span <name> | auto;
  grid-row-start: <number> | <name> | span <number> | span <name> | auto;
  grid-row-end: <number> | <name> | span <number> | span <name> | auto;
}
```

Examples:

```
.item-a {
  grid-column-start: 2;
  grid-column-end: five;
  grid-row-start: row1-start;
  grid-row-end: 3;
}
```

![Example of grid-row/column-start/end](https://css-tricks.com/wp-content/uploads/2018/11/grid-column-row-start-end-01.svg)

```
.item-b {
  grid-column-start: 1;
  grid-column-end: span col4-start;
  grid-row-start: 2;
  grid-row-end: span 2;
}
```

![Example of grid-row/column-start/end](https://css-tricks.com/wp-content/uploads/2018/11/grid-column-row-start-end-02.svg)

If no `grid-column-end`/`grid-row-end` is declared, the item will span 1 track by default.

Items can overlap each other. You can use `z-index` to control their stacking order.

`grid-column`  
`grid-row`

Shorthand for `grid-column-start` + `grid-column-end`, and `grid-row-start` + `grid-row-end`, respectively.

Values:

- **`<start-line>` / `<end-line>`:** Each one accepts all the same values as the longhand version, including span

```
.item {
  grid-column: <start-line> / <end-line> | <start-line> / span <value>;
  grid-row: <start-line> / <end-line> | <start-line> / span <value>;
}
```

Example:

```
.item-c {
  grid-column: 3 / span 2;
  grid-row: third-line / 4;
}
```

![Example of grid-column/grid-row](https://css-tricks.com/wp-content/uploads/2018/11/grid-column-row.svg)

If no end line value is declared, the item will span 1 track by default.

`grid-area`

Gives an item a name so that it can be referenced by a template created with the `grid-template-areas` property. Alternatively, this property can be used as an even shorter shorthand for `grid-row-start` + `grid-column-start` + `grid-row-end` + `grid-column-end`.

Values:

- **`<name>`**: A name of your choosing.
- **`<row-start>` / `<column-start>` / `<row-end>` / `<column-end>`:** Can be numbers or named lines.

```
.item {
  grid-area: <name> | <row-start> / <column-start> / <row-end> / <column-end>;
}
```

Examples:

As a way to assign a name to the item:

```
.item-d {
  grid-area: header;
}
```

As the short-shorthand for `grid-row-start` + `grid-column-start` + `grid-row-end` + `grid-column-end`:

```
.item-d {
  grid-area: 1 / col4-start / last-line / 6;
}
```

![Example of grid-area](https://css-tricks.com/wp-content/uploads/2018/11/grid-area.svg)

[Continue Reading](https://css-tricks.com/almanac/properties/g/grid-area/)

`justify-self`

Aligns a grid item inside a cell along the *inline (row)* axis (as opposed to `align-self` which aligns along the *block (column)* axis). This value applies to a grid item inside a single cell.

Values:

- **`start`:** Aligns the grid item to be flush with the start edge of the cell
- **`end`:** Aligns the grid item to be flush with the end edge of the cell
- **`center`:** Aligns the grid item in the center of the cell
- **`stretch`:** Fills the whole width of the cell (this is the default)

```
.item {
  justify-self: start | end | center | stretch;
}
```

Examples:

```
.item-a {
  justify-self: start;
}
```

![Example of justify-self set to start](https://css-tricks.com/wp-content/uploads/2018/11/justify-self-start.svg)

```
.item-a {
  justify-self: end;
}
```

![alt="Example](https://css-tricks.com/wp-content/uploads/2018/11/justify-self-end.svg)

```
.item-a {
  justify-self: center;
}
```

![Example of justify-self set to center](https://css-tricks.com/wp-content/uploads/2018/11/justify-self-center.svg)

```
.item-a {
  justify-self: stretch;
}
```

![Example of justify-self set to stretch](https://css-tricks.com/wp-content/uploads/2018/11/justify-self-stretch.svg)

To set alignment for *all* the items in a grid, this behavior can also be set on the grid container via the `justify-items` property.

[Continue Reading](https://css-tricks.com/almanac/properties/j/justify-self/)

`align-self`

Aligns a grid item inside a cell along the *block (column)* axis (as opposed to `justify-self` which aligns along the *inline (row)* axis). This value applies to the content inside a single grid item.

Values:

- **`stretch` (default):** Fills the whole height of the cell.
- **`start`:** Aligns the grid item to be flush with the start edge of the cell.
- **`end`:** Aligns the grid item to be flush with the end edge of the cell.
- **`center`:** Aligns the grid item in the center of the cell.

```
.item {
  align-self: start | end | center | stretch;
}
```

Examples:

```
.item-a {
  align-self: start;
}
```

![Example of align-self set to start](https://css-tricks.com/wp-content/uploads/2018/11/align-self-start.svg)

```
.item-a {
  align-self: end;
}
```

![Example of align-self set to end](https://css-tricks.com/wp-content/uploads/2018/11/align-self-end.svg)

```
.item-a {
  align-self: center;
}
```

![Example of align-self set to center](https://css-tricks.com/wp-content/uploads/2018/11/align-self-center.svg)

```
.item-a {
  align-self: stretch;
}
```

![Example of align-self set to stretch](https://css-tricks.com/wp-content/uploads/2018/11/align-self-stretch.svg)

To align *all* the items in a grid, this behavior can also be set on the grid container via the `align-items` property.

[Continue Reading](https://css-tricks.com/almanac/properties/a/align-self/)

`place-self`

`place-self` sets both the `align-self` and `justify-self` properties in a single declaration.

Values:

- **`auto`:** The “default” alignment for the layout mode.
- **`<align-self>` / `<justify-self>`:** The first value sets `align-self`, the second value `justify-self`. If the second value is omitted, the first value is assigned to both properties.

Examples:

```
.item-a {
  place-self: center;
}
```

![place self set to center](https://css-tricks.com/wp-content/uploads/2018/11/place-self-center.svg)

```
.item-a {
  place-self: center stretch;
}
```

![place set set to center stretch](https://css-tricks.com/wp-content/uploads/2018/11/place-self-center-stretch.svg)

All major browsers except Edge support the `place-self` shorthand property.

[Continue Reading](https://css-tricks.com/almanac/properties/p/place-self/)

---

### Special Units, Values, & Functions

The `fr` Unit

You’ll likely end up using a lot of [fractional units](https://css-tricks.com/introduction-fr-css-unit/) in CSS Grid, like `1fr`. They essentially mean “portion of the remaining space”. So a declaration like:

```
grid-template-columns: 1fr 3fr;
```

Means, loosely, `25% 75%`. Except that those percentage values are much more firm than fractional units are. For example, if you added padding to those percentage-based columns, now you’ve broken 100% width (assuming a `content-box` box model). Fractional units also much more friendly in combination with other units, as you can imagine:

```
grid-template-columns: 50px min-content 1fr;
```

Keyword Values

When sizing rows and columns, you can use all the [lengths](https://css-tricks.com/the-lengths-of-css/) you are used to, like `px`, rem, %, etc, but you also have keywords:

- **`min-content`:** The minimum size of the content. Imagine a line of text like “E pluribus unum”, the min-content is likely the width of the word “pluribus.”
- **`max-content`:** The maximum size of the content. Imagine the sentence above, the `max-content` is the length of the whole sentence.
- **`auto`:** This keyword is a lot like `fr` units, except that they “lose” the fight in sizing against `fr` units when allocating the remaining space.
Sizing Functions

- **`fit-content()`:** Uses the space available, but never less than `min-content` and never more than `max-content`.
- **`max()`:** The CSS `max()` function takes two or more comma-separated arguments of spacing values, evaluates them, and returns the largest value of the bunch.
- **`min()`:** The CSS `min()` function takes two or more comma-separated arguments of spacing values, evaluates them, and returns the smallest value of the bunch.
- **`minmax()`:** The CSS `minmax()` function is used exclusively with CSS Grid to define a size range for grid tracks (i.e., the grid’s rows and columns). It lets you specify two arguments — a minimum size and a maximum size for a track — allowing the grid track to grow and shrink within that range, depending on the available space.
The `repeat()` Function

The `repeat()` function can save some typing:

```
grid-template-columns:
  1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr;

/* easier: */
grid-template-columns:
  repeat(8, 1fr);

/* especially when: */
grid-template-columns:
  repeat(8, minmax(10px, 1fr));
```

But `repeat()` can get extra fancy when combined with keywords:

- **`auto-fill`:** Fit as many possible columns as possible on a row, even if they are empty.
- `auto-fit:` Fit whatever columns there are into the space. Prefer expanding columns to fill space rather than empty columns.

This bears the most famous snippet in all of CSS Grid and one of the [all-time great CSS tricks](https://css-tricks.com/books/greatest-css-tricks/flexible-grids/):

```
grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
```

The difference between the keywords is [spelled out in detail here](https://css-tricks.com/auto-sizing-columns-css-grid-auto-fill-vs-auto-fit/).

---

### Subgrid

Subgrid is an extremely useful feature of grids that allows grid items to have a grid of their own that inherits grid lines from the parent grid.

```
.parent-grid {
  display: grid;
  grid-template-columns: repeat(9, 1fr);
}
.grid-item {
  grid-column: 2 / 7;

  display: grid;
  grid-template-columns: subgrid;
}
.child-of-grid-item {
  /* gets to participate on parent grid! */
  grid-column: 3 / 6;
}
```

It’s also useful to know about `display: contents;`. This is *not* the same as subgrid, but it can be a useful tool sometimes in a similar fashion.

```
<div class="grid-parent">

  <div class="grid-item"></div>
  <div class="grid-item"></div>

  <ul style="display: contents;">
    <!-- These grid-items get to participate on 
         the same grid!-->
    <li class="grid-item"></li>
    <li class="grid-item"></li>
  </ul>

</div>
```

[grid](https://css-tricks.com/tag/grid/)

**Link**
on
May 8, 2018 

### [Grid Level 2 and Subgrid](https://css-tricks.com/grid-level-2-and-subgrid/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

[grid](https://css-tricks.com/tag/grid/) [subgrid](https://css-tricks.com/tag/subgrid/)

**Link**
on
Jun 20, 2019 

### [Hello Subgrid!](https://css-tricks.com/hello-subgrid/)

[![](https://i0.wp.com/css-tricks.com/wp-content/cache/breeze-extra/gravatars/me-black-white-80x80.jpg?resize=80%2C80&ssl=1)](https://css-tricks.com/author/robinrendle/) 
[Robin Rendle](https://css-tricks.com/author/robinrendle/)

[flexbox](https://css-tricks.com/tag/flexbox/) [grid](https://css-tricks.com/tag/grid/) [subgrid](https://css-tricks.com/tag/subgrid/)

**Article**
on
Sep 30, 2020 

### [Achieving Vertical Alignment (Thanks, Subgrid!)](https://css-tricks.com/achieving-vertical-alignment-thanks-subgrid/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/13a6f6183bda8f2810a35a909289b0e26b201f0d5be7cb596b92d7f867f3ef1f)](https://css-tricks.com/author/cathydutton/) 
[Cathy Dutton](https://css-tricks.com/author/cathydutton/)

---

### CSS Grid & Masonry Layouts

Think of masonry layouts like erecting a wall of stones or bricks:

![A gray stone wall.](https://i0.wp.com/css-tricks.com/wp-content/uploads/2018/11/masonry.jpg?resize=1024%2C711)

There are [lots of approaches to CSS masonry](https://css-tricks.com/piecing-together-approaches-for-a-css-masonry-layout/), but mostly of them are trickery and either have major downsides or aren’t what you quite expect.

The CSS Working Group is in the process of defining an official approach for creating masonry layouts in the CSS Grid specification. This is an ongoing discussion at the time of this writing. In the meantime, you can read about [the competing proposals](https://css-tricks.com/css-masonry-css-grid/) debating whether to use a CSS Grid or Flexbox approach, get context on [the discussions](https://css-tricks.com/masonry-watching-a-css-feature-evolve/) that led to deciding on a CSS Grid approach, and even [learn how to create a masonry layout today](https://css-tricks.com/making-a-masonry-layout-that-works-today/) using an alternative approach.

---

### Animating CSS Grid

According to the CSS Grid Layout Module Level 1 specification, there are 5 animatable grid properties:

- `gap`, `row-gap`, `column-gap` as a length, percentage, or calculation.
- `grid-template-columns`, `grid-template-rows` as a simple list of lengths, percentages, or calculations, provided the only differences are the values of the length, percentage, or calculated components in the list.

As of this writing, only the animation of `gap`, `row-gap`, `column-gap` is implemented in any of the tested browsers.

| Browser | `gap`, `row-gap`, `column-gap` | `grid-template-columns` | `grid-template-rows` |
| --- | --- | --- | --- |
| Firefox | supported ✅ 53+ | supported ✅ 66+ | supported ✅ 66+ |
| Safari 12.0 | not supported ❌ | not supported ❌ | not supported ❌ |
| Chrome | supported ✅ 66+ | not supported ❌ | not supported ❌ |
| Chrome for Android 66+, Opera Mini 33+ | supported ✅ | not supported ❌ | not supported ❌ |
| Edge | supported ✅ 16+ | not supported ❌ | not supported ❌ |

View Demo

---

### Tutorials & Videos

Learning Tutorials

[grid](https://css-tricks.com/tag/grid/) [layout](https://css-tricks.com/tag/layout/)

**Article**
on
Mar 13, 2017 

### [Getting Started with CSS Grid](https://css-tricks.com/getting-started-css-grid/)

[![](https://i0.wp.com/css-tricks.com/wp-content/cache/breeze-extra/gravatars/me-black-white-80x80.jpg?resize=80%2C80&ssl=1)](https://css-tricks.com/author/robinrendle/) 
[Robin Rendle](https://css-tricks.com/author/robinrendle/)

[grid](https://css-tricks.com/tag/grid/)

**Article**
on
Jul 21, 2017 

### [A Collection of Interesting Facts about CSS Grid Layout](https://css-tricks.com/collection-interesting-facts-css-grid-layout/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/de3be7ba94c6a1bf0e69c7c0af6de3e54b8bcc53e716f54c972e080745128dac)](https://css-tricks.com/author/mmatuzo/) 
[Manuel Matuzovic](https://css-tricks.com/author/mmatuzo/)

[fr](https://css-tricks.com/tag/fr/) [typography](https://css-tricks.com/tag/typography/)

**Article**
on
Jun 12, 2017 

### [An Introduction to the `fr` CSS unit](https://css-tricks.com/introduction-fr-css-unit/)

[![](https://i0.wp.com/css-tricks.com/wp-content/cache/breeze-extra/gravatars/me-black-white-80x80.jpg?resize=80%2C80&ssl=1)](https://css-tricks.com/author/robinrendle/) 
[Robin Rendle](https://css-tricks.com/author/robinrendle/)

[grid](https://css-tricks.com/tag/grid/)

**Article**
on
Dec 29, 2017 

### [Auto-Sizing Columns in CSS Grid: `auto-fill` vs `auto-fit`](https://css-tricks.com/auto-sizing-columns-css-grid-auto-fill-vs-auto-fit/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/dfce7f1d9c81f17ed70151da50aa13b6d32b77eeaa9f1e3314230a7f0d2909b8)](https://css-tricks.com/author/sarasoueidan/) 
[Sara Soueidan](https://css-tricks.com/author/sarasoueidan/)

[flexbox](https://css-tricks.com/tag/flexbox/) [grid](https://css-tricks.com/tag/grid/)

**Article**
on
Mar 31, 2017 

### [Does CSS Grid Replace Flexbox?](https://css-tricks.com/css-grid-replace-flexbox/)

[![](https://i0.wp.com/css-tricks.com/wp-content/cache/breeze-extra/gravatars/me-black-white-80x80.jpg?resize=80%2C80&ssl=1)](https://css-tricks.com/author/robinrendle/) 
[Robin Rendle](https://css-tricks.com/author/robinrendle/)

[grid](https://css-tricks.com/tag/grid/) [grid-auto-flow](https://css-tricks.com/tag/grid-auto-flow/) [grid-template-columns](https://css-tricks.com/tag/grid-template-columns/) [grid-template-rows](https://css-tricks.com/tag/grid-template-rows/) [implicit grid](https://css-tricks.com/tag/implicit-grid/)

**Article**
on
Aug 1, 2022 

### [Exploring CSS Grid’s Implicit Grid and Auto-Placement Powers](https://css-tricks.com/exploring-css-grids-implicit-grid-and-auto-placement-powers/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/c16ca31febf1ccf880613914aa584da7cac990d02a585c1d6c9aff416ce8e28f)](https://css-tricks.com/author/afiftemani/) 
[Temani Afif](https://css-tricks.com/author/afiftemani/)

[fit-content](https://css-tricks.com/tag/fit-content/) [max-content](https://css-tricks.com/tag/max-content/) [min-content](https://css-tricks.com/tag/min-content/)

**Link**
on
May 20, 2021 

### [fit-content and fit-content()](https://css-tricks.com/fit-content-and-fit-content/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

**Link**
on
Nov 6, 2017 

### [Flexbox and Grids, your layout’s best friends](https://css-tricks.com/flexbox-grids-layouts-best-friends/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

[flexbox](https://css-tricks.com/tag/flexbox/) [grid](https://css-tricks.com/tag/grid/)

**Link**
on
Jun 25, 2020 

### [Grid for layout, flexbox for components](https://css-tricks.com/grid-for-layout-flexbox-for-components/)

[![](https://i0.wp.com/css-tricks.com/wp-content/cache/breeze-extra/gravatars/me-black-white-80x80.jpg?resize=80%2C80&ssl=1)](https://css-tricks.com/author/robinrendle/) 
[Robin Rendle](https://css-tricks.com/author/robinrendle/)

[flexbox](https://css-tricks.com/tag/flexbox/) [grid](https://css-tricks.com/tag/grid/) [layout](https://css-tricks.com/tag/layout/)

**Article**
on
Feb 12, 2019 

### [Quick! What’s the Difference Between Flexbox and Grid?](https://css-tricks.com/quick-whats-the-difference-between-flexbox-and-grid/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

[grid](https://css-tricks.com/tag/grid/) [grid-auto-flow](https://css-tricks.com/tag/grid-auto-flow/)

**Article**
on
Jan 8, 2020 

### [The Auto-Flowing Powers of Grid’s Dense Keyword](https://css-tricks.com/the-auto-flowing-powers-of-grids-dense-keyword/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/a8e040142716a4b44d014d80fbcf99c635b1d8faabfe469b6954a8ef2f168595)](https://css-tricks.com/author/geoffgraham/) 
[Geoff Graham](https://css-tricks.com/author/geoffgraham/)

[grid](https://css-tricks.com/tag/grid/)

**Article**
on
Aug 10, 2017 

### [The Difference Between Explicit and Implicit Grids](https://css-tricks.com/difference-explicit-implicit-grids/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/de3be7ba94c6a1bf0e69c7c0af6de3e54b8bcc53e716f54c972e080745128dac)](https://css-tricks.com/author/mmatuzo/) 
[Manuel Matuzovic](https://css-tricks.com/author/mmatuzo/)

[grid](https://css-tricks.com/tag/grid/) [layout](https://css-tricks.com/tag/layout/)

**Article**
on
Nov 2, 2016 

### [Things I’ve Learned About CSS Grid Layout](https://css-tricks.com/things-ive-learned-css-grid-layout/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/5499ca0b40f9d4d28a48605872b9f1a0a5258f1878c11b95e070ec8a3edcaaf1)](https://css-tricks.com/author/olliew/) 
[Ollie Williams](https://css-tricks.com/author/olliew/)

[grid](https://css-tricks.com/tag/grid/)

**Link**
on
Nov 18, 2020 

### [Thinking Outside the Box with CSS Grid](https://css-tricks.com/thinking-outside-the-box-with-css-grid/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

[grid](https://css-tricks.com/tag/grid/) [grid-template-areas](https://css-tricks.com/tag/grid-template-areas/) [layout](https://css-tricks.com/tag/layout/) [naming](https://css-tricks.com/tag/naming/)

**Article**
on
Aug 26, 2022 

### [Using Grid Named Areas to Visualize (and Reference) Your Layout](https://css-tricks.com/using-grid-named-areas-to-visualize-and-reference-your-layout/)

[![](https://i0.wp.com/css-tricks.com/wp-content/cache/breeze-extra/gravatars/69065327-80x80.jpeg?resize=80%2C80&ssl=1)](https://css-tricks.com/author/selvampreethi/) 
[Preethi Selvam](https://css-tricks.com/author/selvampreethi/)

Video Screencasts

**Video**
on
Oct 24, 2012 

### [#115: Don’t Overthink It Grids](https://css-tricks.com/videos/115-dont-overthink-it-grids/)

▶ Running Time: 17:19

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

on
Sep 10, 2012 

### [#019: Building a Simple Grid](https://css-tricks.com/lodge/v10/019-building-a-simple-grid/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

on
Sep 12, 2012 

### [#032: Making The Grid Responsive](https://css-tricks.com/lodge/v10/032-making-the-grid-responsive/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

[grid](https://css-tricks.com/tag/grid/)

**Video**
on
Feb 20, 2017 

### [#153: Getting Started with CSS Grid](https://css-tricks.com/videos/153-getting-started-with-css-grid/)

▶ Running Time: 47:26

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/a8e040142716a4b44d014d80fbcf99c635b1d8faabfe469b6954a8ef2f168595)](https://css-tricks.com/author/geoffgraham/) 
[Geoff Graham](https://css-tricks.com/author/geoffgraham/)

**Video**
on
Jul 30, 2021 

### [#208: A CSS Grid Layout with Pictures Down One Side Matched Up with Paragraphs on the Other](https://css-tricks.com/videos/208-a-css-grid-layout-with-pictures-down-one-side-matched-up-with-paragraphs-on-the-other/)

▶ Running Time: 21:17

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

[aspect ratio](https://css-tricks.com/tag/aspect-ratio/) [grid](https://css-tricks.com/tag/grid/)

**Video**
on
Apr 6, 2020 

### [#179: A Grid of Squares](https://css-tricks.com/videos/179-a-grid-of-squares/)

▶ Running Time: 16:34

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

---

### Browser Support

This browser support data is from [Caniuse](http://caniuse.com/#feat=css-grid), which has more detail. A number indicates that browser supports the feature at that version and up.

#### Desktop

| Chrome | Firefox | IE | Edge | Safari |
| --- | --- | --- | --- | --- |
| 57 | 52 | 11\* | 16 | 10.1 |

#### Mobile / Tablet

| Android Chrome | Android Firefox | Android | iOS Safari |
| --- | --- | --- | --- |
| 144 | 147 | 144 | 10.3 |

---

### Specifications

- [CSS Grid Layout Module Level 1](https://www.w3.org/TR/css-grid-1/) (Candidate Recommendation): Provides the initial definition of CSS Grid and its properties.
- [CSS Grid Layout Module Level 2](https://drafts.csswg.org/css-grid/) (Candidate Recommendation Draft): Includes the initial definition for the [Subgrid](https://www.w3.org/TR/css-grid-2/) feature.
- [CSS Grid Layout Module Level 3](https://drafts.csswg.org/css-grid-3/) (Editor’s Draft): Includes the first working definition for [Masonry layouts](https://drafts.csswg.org/css-grid-3/#masonry-model).