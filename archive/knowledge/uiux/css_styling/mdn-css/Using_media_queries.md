# Using media queries

Source: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_media_queries/Using_media_queries

---

# Using media queries

**Media queries** allow you to apply CSS styles depending on a device's media type (such as print vs. screen) or other features or characteristics such as screen resolution or orientation, [aspect ratio](/en-US/docs/Glossary/Aspect_ratio), browser [viewport](/en-US/docs/Glossary/Viewport) width or height, user preferences such as preferring reduced motion, data usage, or transparency.

Media queries are used for the following:

- To conditionally apply styles with the [CSS](/en-US/docs/Web/CSS) [`@media`](/en-US/docs/Web/CSS/Reference/At-rules/@media), [`@custom-media`](/en-US/docs/Web/CSS/Reference/At-rules/@custom-media) and [`@import`](/en-US/docs/Web/CSS/Reference/At-rules/@import) [at-rules](/en-US/docs/Web/CSS/Guides/Syntax/At-rules).
- To target specific media for the [`<style>`](/en-US/docs/Web/HTML/Reference/Elements/style), [`<link>`](/en-US/docs/Web/HTML/Reference/Elements/link), [`<source>`](/en-US/docs/Web/HTML/Reference/Elements/source), and other [HTML](/en-US/docs/Web/HTML) elements with the `media=` or `sizes="` attributes.
- To [test and monitor media states](/en-US/docs/Web/CSS/Guides/Media_queries/Testing) using the [`Window.matchMedia()`](/en-US/docs/Web/API/Window/matchMedia) and [`EventTarget.addEventListener()`](/en-US/docs/Web/API/EventTarget/addEventListener) methods.

**Note:**
The examples on this page use CSS's `@media` for illustrative purposes, but the basic syntax remains the same for all types of media queries.

## [Syntax](#syntax)

A media query is composed of an optional *media type* and any number of *media feature* expressions, which may optionally be combined in various ways using *logical operators*.
Media queries are case-insensitive.

- [Media types](/en-US/docs/Web/CSS/Reference/At-rules/@media#media_types) define the broad category of device for which the media query applies: `all`, `print`, `screen`.

  The type is optional (assumed to be `all`) except when using the `only` logical operator.
- [Media features](/en-US/docs/Web/CSS/Reference/At-rules/@media#media_features) describe a specific characteristic of the [user agent](/en-US/docs/Glossary/User_agent), output device, or environment:

  - [`any-hover`](/en-US/docs/Web/CSS/Reference/At-rules/@media/any-hover)
  - [`any-pointer`](/en-US/docs/Web/CSS/Reference/At-rules/@media/any-pointer)
  - [`aspect-ratio`](/en-US/docs/Web/CSS/Reference/At-rules/@media/aspect-ratio)
  - [`color`](/en-US/docs/Web/CSS/Reference/At-rules/@media/color)
  - [`color-gamut`](/en-US/docs/Web/CSS/Reference/At-rules/@media/color-gamut)
  - [`color-index`](/en-US/docs/Web/CSS/Reference/At-rules/@media/color-index)
  - [`device-aspect-ratio`](/en-US/docs/Web/CSS/Reference/At-rules/@media/device-aspect-ratio) 
    Deprecated
  - [`device-height`](/en-US/docs/Web/CSS/Reference/At-rules/@media/device-height) 
    Deprecated
  - [`device-posture`](/en-US/docs/Web/CSS/Reference/At-rules/@media/device-posture)
  - [`device-width`](/en-US/docs/Web/CSS/Reference/At-rules/@media/device-width) 
    Deprecated
  - [`display-mode`](/en-US/docs/Web/CSS/Reference/At-rules/@media/display-mode)
  - [`dynamic-range`](/en-US/docs/Web/CSS/Reference/At-rules/@media/dynamic-range)
  - [`forced-colors`](/en-US/docs/Web/CSS/Reference/At-rules/@media/forced-colors)
  - [`grid`](/en-US/docs/Web/CSS/Reference/At-rules/@media/grid)
  - [`height`](/en-US/docs/Web/CSS/Reference/At-rules/@media/height)
  - [`hover`](/en-US/docs/Web/CSS/Reference/At-rules/@media/hover)
  - [`inverted-colors`](/en-US/docs/Web/CSS/Reference/At-rules/@media/inverted-colors)
  - [`monochrome`](/en-US/docs/Web/CSS/Reference/At-rules/@media/monochrome)
  - [`orientation`](/en-US/docs/Web/CSS/Reference/At-rules/@media/orientation)
  - [`overflow-block`](/en-US/docs/Web/CSS/Reference/At-rules/@media/overflow-block)
  - [`overflow-inline`](/en-US/docs/Web/CSS/Reference/At-rules/@media/overflow-inline)
  - [`pointer`](/en-US/docs/Web/CSS/Reference/At-rules/@media/pointer)
  - [`prefers-color-scheme`](/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-color-scheme)
  - [`prefers-contrast`](/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-contrast)
  - [`prefers-reduced-motion`](/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion)
  - [`prefers-reduced-transparency`](/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-transparency)
  - [`resolution`](/en-US/docs/Web/CSS/Reference/At-rules/@media/resolution)
  - [`scripting`](/en-US/docs/Web/CSS/Reference/At-rules/@media/scripting)
  - [`update`](/en-US/docs/Web/CSS/Reference/At-rules/@media/update)
  - [`video-dynamic-range`](/en-US/docs/Web/CSS/Reference/At-rules/@media/video-dynamic-range)
  - [`width`](/en-US/docs/Web/CSS/Reference/At-rules/@media/width)

  For example, the [`hover`](/en-US/docs/Web/CSS/Reference/At-rules/@media/hover) feature allows a query to check whether the device supports hovering over elements.
  Media feature expressions test for their presence or value, and are entirely optional.
  Each media feature expression must be surrounded by parentheses.
- [Logical operators](/en-US/docs/Web/CSS/Reference/At-rules/@media#logical_operators) can be used to compose a complex media query: `not`, `and`, and `only`.
  You can also combine multiple media queries into a single rule by separating them with commas.

A media query computes to `true` when the media type (if specified) matches the device on which a document is being displayed *and* all media feature expressions compute as true.
Queries involving unknown media types are always false.

**Note:**
A style sheet with a media query attached to its [`<link>`](/en-US/docs/Web/HTML/Reference/Elements/link) tag [will still download](https://scottjehl.github.io/CSS-Download-Tests/) even if the query returns `false`, the download will happen but the priority of downloading will be much lower.
Nevertheless, its contents will not apply unless and until the result of the query changes to `true`.
You can read why this happens in Tomayac's blog [Why Browser Download Stylesheet with Non-Matching Media Queries](https://medium.com/@tomayac/why-browsers-download-stylesheets-with-non-matching-media-queries-eb61b91b85a2).

## [Targeting media types](#targeting_media_types)

Media types describe the general category of a given device.
Although websites are commonly designed with screens in mind, you may want to create styles that target special devices such as printers or audio-based screen readers.
For example, this CSS targets printers:

css

```
@media print {
  /* â¦ */
}
```

You can also target multiple devices.
For instance, this `@media` rule uses two media queries to target both screen and print devices:

css

```
@media screen, print {
  /* â¦ */
}
```

See [media types](/en-US/docs/Web/CSS/Reference/At-rules/@media#media_types) for the list of available media types.
Because media types describe devices in very broad terms, most of the originally-defined media types were deprecated, with just `screen`, `print`, and `all` remaining. To target more specific attributes, use *media features* instead.

## [Targeting media features](#targeting_media_features)

Media features describe the specific characteristics of a given [user agent](/en-US/docs/Glossary/User_agent), output device, or environment.
For instance, you can apply specific styles to widescreen monitors, computers that use mice, or devices that are being used in low-light conditions.
This example applies styles when the user's *primary* input mechanism (such as a mouse) can hover over elements:

css

```
@media (hover: hover) {
  /* â¦ */
}
```

Media features are either range or discrete.

*Discrete features* take their value from an [enumerated](/en-US/docs/Glossary/Enumerated) set of possible keyword values. For example, the discrete `orientation` feature accepts either `landscape` or `portrait`.

css

```
@media print and (orientation: portrait) {
  /* â¦ */
}
```

Many *range features* can be prefixed with "min-" or "max-" to express "minimum condition" or "maximum condition" constraints.
For example, this CSS will apply styles only if your browser's [viewport](/en-US/docs/Glossary/Viewport) width is equal to or narrower than 1250px:

css

```
@media (max-width: 1250px) {
  /* â¦ */
}
```

The following media queries are equivalent to the above example:

css

```
@media (width <= 1250px) {
  /* â¦ */
}

@media (1250px >= width) {
  /* â¦ */
}
```

With media query range features, you can either use the inclusive `min-` and `max-` prefixes or the more concise range syntax operators `<=` and `>=`.

The following media queries are equivalent:

css

```
@media (min-width: 30em) and (max-width: 50em) {
  /* â¦ */
}

@media (30em <= width <= 50em) {
  /* â¦ */
}

@media (50em >= width >= 30em) {
  /* â¦ */
}
```

The range comparisons above are inclusive. To exclude the comparison value, use `<` and/or `>`.

css

```
@media (30em < width < 50em) {
  /* â¦ */
}

@media (50em > width > 30em) {
  /* â¦ */
}
```

If you create a media feature query without specifying a value, the nested styles will be used as long as the feature's value is not `0` or `none`.
For example, this CSS will apply to any device with a color screen:

css

```
@media (color) {
  /* â¦ */
}
```

If a feature doesn't apply to the device on which the browser is running, expressions involving that media feature are always false.

For more [Media feature](/en-US/docs/Web/CSS/Reference/At-rules/@media#media_features) examples, please see the reference page for each specific feature.

## [Creating complex media queries](#creating_complex_media_queries)

Sometimes you may want to create a media query that depends on multiple conditions. This is where the *logical operators* come in: `not`, `and`, and `only`.
Furthermore, you can combine multiple media queries into a comma-separated list; this allows you to apply the same styles in different situations, with the contained media queries evaluated as a logical `or` composition: interpreted as if each media query were within parentheses with an `or` between them.

In the previous example, we saw the `and` operator used to group a media *type* with a media *feature*.
The `and` operator can also combine multiple media features within a single media query.
The `not` operator negates a media query, or a media feature when used with brackets, basically reversing their normal meanings.
The `or` operator can, under certain conditions, be used to combine multiple media features within a single media query.
Lastly, the `only` operator was used to prevent older browsers from applying the styles without evaluating the media feature expressions but it has no effect in modern browsers.

**Note:**
In most cases, the `all` media type is used by default when no other type is specified.
However, if you use the `only` operator, you must explicitly specify a media type. You can see `only screen` or `only print` as a whole.

### [Combining multiple types or features](#combining_multiple_types_or_features)

The `and` keyword combines a media feature with a media type *or* other media features.
This example combines two media features to restrict styles to landscape-oriented devices with a width of at least 30 ems:

css

```
@media (width >= 30em) and (orientation: landscape) {
  /* â¦ */
}
```

To limit the styles to devices with a screen, you can chain the media features to the `screen` media type:

css

```
@media screen and (width >= 30em) and (orientation: landscape) {
  /* â¦ */
}
```

### [Testing for multiple queries](#testing_for_multiple_queries)

You can use a comma-separated list of media queries to apply styles when the user's device matches any one of various media types, features, or states.

The following rule contains two media queries. The block's styles will apply if either the user's device has a height of 680px or more *or* if the browser viewport is in portrait mode (the viewport height is greater than the viewport width):

css

```
@media (height >= 680px), screen and (orientation: portrait) {
  /* â¦ */
}
```

In this example, if the user is printing to a PDF and the page height is 800px, the media query returns true because the first query component â which tests whether the viewport has a height of `680px` or more â is true.
Likewise, if a user is on a smartphone in portrait mode with a viewport height of 480px, the media query returns true because the second query component is true.

In a comma-separated list of media queries, the individual media queries end at the comma or, in the case of the last media query in the list, at the opening bracket (`{`).

### [Inverting a query's meaning](#inverting_a_querys_meaning)

The `not` keyword inverts the meaning of a single media query. For example, the CSS styles in this media query will apply to everything *except* printed media:

css

```
@media not print {
  /* â¦ */
}
```

The `not` negates only the media query it is applied to. The `not`, without parenthesis, negates all the features within the media query in which it is contained. This means, in a comma-separated list of media queries, each `not` applies to the single query it is contained within, applying to *all* the features within that single query. In this example, the `not` applies to the first media query `screen and (color)`, which concludes at the first comma:

css

```
@media not screen and (color), print and (color) {
  /* â¦ */
}
```

Because the query starts with a media type `screen`, you *cannot* wrap `screen and (color)` with parentheses. On the other hand, if your media query consists of features only, then you *must* parenthesize the query:

css

```
@media not ((width > 1000px) and (color)), print and (color) {
  /* â¦ */
}
```

Parentheses limit the components of the query that get negated. For example, to negate the `(width > 1000px)` query only:

css

```
@media (not (width > 1000px)) and (color), print and (color) {
  /* â¦ */
}
```

`not` only negates the query to its right. In this example, we negate the `hover` media feature but not the `screen` media type:

css

```
@media screen and not (hover) {
  /* â¦ */
}
```

The `not (hover)` matches if the device has no hover capability. In this case, because of its ordering, the `not` applies to `hover` but not to `screen`.

### [Improving compatibility with older browsers](#improving_compatibility_with_older_browsers)

The `only` keyword prevents older browsers that do not support media queries with media features from applying the given styles.
*It has no effect on modern browsers.*

css

```
@media only screen and (color) {
  /* â¦ */
}
```

### [Testing for multiple features with `or`](#testing_for_multiple_features_with_or)

You can use `or` to test for a match among more than one feature, resolving to `true` if any of the features are true.
For example, the following query tests for devices that have a monochrome display or hover capability:

css

```
@media (not (color)) or (hover) {
  /* â¦ */
}
```

Note that you cannot use the `or` operator on the same level as the `and` and `not` operators. You can either separate the media features with a comma or use parenthesis to group sub-expressions of media features to clarify the order of evaluation.

For example, the following queries are both valid:

css

```
@media ((color) and (hover)) or (monochrome) {
  /* â¦ */
}

/* or */
@media (color) and (hover), (monochrome) {
  /* â¦ */
}
```

## [See also](#see_also)

- [@media](/en-US/docs/Web/CSS/Reference/At-rules/@media)
- [Container queries](/en-US/docs/Web/CSS/Guides/Containment/Container_queries)
- [Testing media queries programmatically](/en-US/docs/Web/CSS/Guides/Media_queries/Testing)
- [CSS Animations Between Media Queries](https://davidwalsh.name/animate-media-queries)
- [Extended Mozilla media features](/en-US/docs/Web/CSS/Reference/Mozilla_extensions#media_features)
- [Extended WebKit media features](/en-US/docs/Web/CSS/Reference/Webkit_extensions#media_features)

## Help improve MDN

Was this page helpful to you?

Yes

No

[Learn how to contribute](/en-US/docs/MDN/Community/Getting_started)

This page was last modified on Dec 2, 2025 by [MDN contributors](/en-US/docs/Web/CSS/Guides/Media_queries/Using/contributors.txt).

[View this page on GitHub](https://github.com/mdn/content/blob/main/files/en-us/web/css/guides/media_queries/using/index.md?plain=1 "Folder: en-us/web/css/guides/media_queries/using (Opens in a new tab)") â¢ [Report a problem with this content](https://github.com/mdn/content/issues/new?template=page-report.yml&mdn-url=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FGuides%2FMedia_queries%2FUsing&metadata=%3C%21--+Do+not+make+changes+below+this+line+--%3E%0A%3Cdetails%3E%0A%3Csummary%3EPage+report+details%3C%2Fsummary%3E%0A%0A*+Folder%3A+%60en-us%2Fweb%2Fcss%2Fguides%2Fmedia_queries%2Fusing%60%0A*+MDN+URL%3A+https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FGuides%2FMedia_queries%2FUsing%0A*+GitHub+URL%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fblob%2Fmain%2Ffiles%2Fen-us%2Fweb%2Fcss%2Fguides%2Fmedia_queries%2Fusing%2Findex.md%0A*+Last+commit%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fcommit%2F3ee2355c3c90cf92c3119b82f8ebfa5d16c91c53%0A*+Document+last+modified%3A+2025-12-02T16%3A36%3A33.000Z%0A%0A%3C%2Fdetails%3E "This will take you to GitHub to file a new issue.")