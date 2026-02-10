# CSS container queries

Source: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries

---

# CSS container queries

Container queries enable you to apply styles to an element based on certain attributes of its container:

- The container's size.
- Styles applied to the container.
- The container's scroll-state or that of its scrolling ancestor.

Container queries are an alternative to [media queries](/en-US/docs/Web/CSS/Guides/Media_queries), which apply styles to elements based on viewport size or other device characteristics.

This article provides an introduction to using container queries, specifically focusing on size container queries. Other guides discuss [style](/en-US/docs/Web/CSS/Guides/Containment/Container_size_and_style_queries#container_style_queries) and [scroll-state](/en-US/docs/Web/CSS/Guides/Conditional_rules/Container_scroll-state_queries) container queries in detail.

![Two different query types. First, a media query based on the viewport's width, which is the full width of the browser. Second, a container query based on the width of a container element.](/en-US/docs/Web/CSS/Guides/Containment/Container_queries/container-query.svg)

## [Using container size queries](#using_container_size_queries)

While container queries apply styles based on the container type, container size queries apply styles specifically based on the container's dimensions. To use container size queries, you need to declare a **containment context** on an element so that the browser knows you might want to query the dimensions of this container later.
To do this, use the [`container-type`](/en-US/docs/Web/CSS/Reference/Properties/container-type) property with a value of `size`, `inline-size`, or `normal`.

These values have the following effects:

[`size`](#size)
:   The query will be based on the [inline and block](/en-US/docs/Web/CSS/Guides/Logical_properties_and_values/Basic_concepts#block_and_inline_dimensions) dimensions of the container.
    Applies layout, style, and size [containment](/en-US/docs/Web/CSS/Guides/Containment/Using) to the container.

[`inline-size`](#inline-size)
:   The query will be based on the [inline](/en-US/docs/Web/CSS/Guides/Logical_properties_and_values/Basic_concepts#block_and_inline_dimensions) dimensions of the container.
    Applies layout, style, and inline-size containment to the element.

[`normal`](#normal)
:   The element is not a query container for any container size queries, but remains a query container for container style queries.

Consider the following example of a card component for a blog post with a title and some text:

html

```
<div class="post">
  <div class="card">
    <h2>Card title</h2>
    <p>Card content</p>
  </div>
</div>
```

You can create a containment context using the `container-type` property:

css

```
.post {
  container-type: inline-size;
}
```

Next, use the [`@container`](/en-US/docs/Web/CSS/Reference/At-rules/@container) at-rule to define a container query.
The query in the following example will apply styles to elements based on the size of the nearest ancestor with a containment context.
Specifically, this query will apply a larger font size for the card title if the container is wider than `700px`:

css

```
/* Default heading styles for the card title */
.card h2 {
  font-size: 1em;
}

/* If the container is larger than 700px */
@container (width > 700px) {
  .card h2 {
    font-size: 2em;
  }
}
```

Using container queries, the card can be reused in multiple areas of a page without needing to know specifically where it will be placed each time.
If the container with the card is narrower than `700px`, the font of the card title will be small, and if the card is in a container that's wider than `700px`, the font of the card title will be bigger.

For more information on the syntax of container queries, see the [`@container`](/en-US/docs/Web/CSS/Reference/At-rules/@container) page.

### [Naming containment contexts](#naming_containment_contexts)

In the previous section, a container query applied styles based on the nearest ancestor with a containment context.
It's possible to give a containment context a name using the [`container-name`](/en-US/docs/Web/CSS/Reference/Properties/container-name) property. Once named, the name can be used in a `@container` query so as to target a specific container.
The following example creates a containment context with the name `sidebar`:

css

```
.post {
  container-type: inline-size;
  container-name: sidebar;
}
```

You can then target this containment context using the `@container` at-rule:

css

```
@container sidebar (width > 700px) {
  .card {
    font-size: 2em;
  }
}
```

More information on naming containment contexts is available on the [`container-name`](/en-US/docs/Web/CSS/Reference/Properties/container-name) page.

### [Shorthand container syntax](#shorthand_container_syntax)

The shorthand way of declaring a containment context is to use the `container` property:

css

```
.post {
  container: sidebar / inline-size;
}
```

For more information on this property, see the [`container`](/en-US/docs/Web/CSS/Reference/Properties/container) reference.

### [Container query length units](#container_query_length_units)

When applying styles to a container using container queries, you can use container query length units.
These units specify a length relative to the dimensions of a query container.
Components that use units of length relative to their container are more flexible to use in different containers without having to recalculate concrete length values.

If no eligible container is available for the query, the container query length unit defaults to the [small viewport unit](/en-US/docs/Web/CSS/Reference/Values/length#small_viewport_units) for that axis (`sv*`).

The container query length units are:

- `cqw`: 1% of a query container's width
- `cqh`: 1% of a query container's height
- `cqi`: 1% of a query container's inline size
- `cqb`: 1% of a query container's block size
- `cqmin`: The smaller value of either `cqi` or `cqb`
- `cqmax`: The larger value of either `cqi` or `cqb`

The following example uses the `cqi` unit to set the font size of a heading based on the inline size of the container:

css

```
@container (width > 700px) {
  .card h2 {
    font-size: max(1.5em, 1.23em + 2cqi);
  }
}
```

For more information on these units, see the [Container query length units](/en-US/docs/Web/CSS/Reference/Values/length#container_query_length_units) reference.

## [Fallbacks for container queries](#fallbacks_for_container_queries)

For browsers that don't yet support container queries, [`grid`](/en-US/docs/Web/CSS/Reference/Properties/grid) and [`flex`](/en-US/docs/Web/CSS/Reference/Properties/flex) can be used to create a similar effect for the card component used on this page.
The following example uses a [`grid-template-columns`](/en-US/docs/Web/CSS/Reference/Properties/grid-template-columns) declaration to create a two-column layout for the card component.

css

```
.card {
  display: grid;
  grid-template-columns: 2fr 1fr;
}
```

If you want to use a single-column layout for devices with a smaller viewport, you can use a media query to change the grid template:

css

```
@media (width <= 700px) {
  .card {
    grid-template-columns: 1fr;
  }
}
```

## [See also](#see_also)

- [Media queries](/en-US/docs/Web/CSS/Guides/Media_queries)
- CSS [`@container`](/en-US/docs/Web/CSS/Reference/At-rules/@container) at-rule
- CSS [`contain`](/en-US/docs/Web/CSS/Reference/Properties/contain) property
- CSS [`container`](/en-US/docs/Web/CSS/Reference/Properties/container) shorthand property
- CSS [`container-name`](/en-US/docs/Web/CSS/Reference/Properties/container-name) property
- CSS [`content-visibility`](/en-US/docs/Web/CSS/Reference/Properties/content-visibility) property
- [Using container size and style queries](/en-US/docs/Web/CSS/Guides/Containment/Container_size_and_style_queries)
- [Using container scroll-state queries](/en-US/docs/Web/CSS/Guides/Conditional_rules/Container_scroll-state_queries)
- [Say Hello to CSS Container Queries](https://ishadeed.com/article/say-hello-to-css-container-queries/) by Ahmad Shadeed
- [Container Queries: a Quick Start Guide](https://www.oddbird.net/2021/04/05/containerqueries/)
- [Collection of Container Queries articles](https://github.com/sturobson/Awesome-Container-Queries)

## Help improve MDN

Was this page helpful to you?

Yes

No

[Learn how to contribute](/en-US/docs/MDN/Community/Getting_started)

This page was last modified on Nov 7, 2025 by [MDN contributors](/en-US/docs/Web/CSS/Guides/Containment/Container_queries/contributors.txt).

[View this page on GitHub](https://github.com/mdn/content/blob/main/files/en-us/web/css/guides/containment/container_queries/index.md?plain=1 "Folder: en-us/web/css/guides/containment/container_queries (Opens in a new tab)") â¢ [Report a problem with this content](https://github.com/mdn/content/issues/new?template=page-report.yml&mdn-url=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FGuides%2FContainment%2FContainer_queries&metadata=%3C%21--+Do+not+make+changes+below+this+line+--%3E%0A%3Cdetails%3E%0A%3Csummary%3EPage+report+details%3C%2Fsummary%3E%0A%0A*+Folder%3A+%60en-us%2Fweb%2Fcss%2Fguides%2Fcontainment%2Fcontainer_queries%60%0A*+MDN+URL%3A+https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FGuides%2FContainment%2FContainer_queries%0A*+GitHub+URL%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fblob%2Fmain%2Ffiles%2Fen-us%2Fweb%2Fcss%2Fguides%2Fcontainment%2Fcontainer_queries%2Findex.md%0A*+Last+commit%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fcommit%2F85fccefc8066bd49af4ddafc12c77f35265c7e2d%0A*+Document+last+modified%3A+2025-11-07T15%3A58%3A06.000Z%0A%0A%3C%2Fdetails%3E "This will take you to GitHub to file a new issue.")