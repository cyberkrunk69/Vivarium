# :is()

Source: https://developer.mozilla.org/en-US/docs/Web/CSS/:is

---

# :is()

Baseline
Widely available

This feature is well established and works across many devices and browser versions. Itâs been available across browsers since January 2021.

- [Learn more](/en-US/docs/Glossary/Baseline/Compatibility)
- [See full compatibility](#browser_compatibility)
- [Report feedback](https://survey.alchemer.com/s3/7634825/MDN-baseline-feedback?page=%2Fen-US%2Fdocs%2FWeb%2FCSS%2FReference%2FSelectors%2F%3Ais&level=high)

 

The **`:is()`** [CSS](/en-US/docs/Web/CSS) [pseudo-class](/en-US/docs/Web/CSS/Reference/Selectors/Pseudo-classes) function takes a selector list as its argument, and selects any element that can be selected by one of the selectors in that list. This is useful for writing large selectors in a more compact form.

**Note:**
Originally named `:matches()` (and `:any()`), this selector was renamed to `:is()` in [CSSWG issue #3258](https://github.com/w3c/csswg-drafts/issues/3258).

## [Try it](#try_it)

```
ol {
  list-style-type: upper-alpha;
  color: darkblue;
}

:is(ol, ul, menu:unsupported) :is(ol, ul) {
  color: green;
}

:is(ol, ul) :is(ol, ul) ol {
  list-style-type: lower-greek;
  color: chocolate;
}
```

```
<ol>
  <li>Saturn</li>
  <li>
    <ul>
      <li>Mimas</li>
      <li>Enceladus</li>
      <li>
        <ol>
          <li>Voyager</li>
          <li>Cassini</li>
        </ol>
      </li>
      <li>Tethys</li>
    </ul>
  </li>
  <li>Uranus</li>
  <li>
    <ol>
      <li>Titania</li>
      <li>Oberon</li>
    </ol>
  </li>
</ol>
```

## [Syntax](#syntax)

css

```
:is(<forgiving-selector-list>) {
  /* ... */
}
```

### [Parameters](#parameters)

The `:is()` pseudo-class requires a [selector list](/en-US/docs/Web/CSS/Guides/Selectors/Selector_structure#selector_list), a comma-separated list of one or more selectors as its argument. The list must not contain a [pseudo-element](/en-US/docs/Web/CSS/Reference/Selectors/Pseudo-elements), but any other simple, compound, and complex selectors are allowed.

### [Difference between :is() and :where()](#difference_between_is_and_where)

The difference between the two is that `:is()` counts towards the specificity of the overall selector (it takes the specificity of its most specific argument), whereas [`:where()`](/en-US/docs/Web/CSS/Reference/Selectors/:where) has a specificity value of 0. This is demonstrated by the [example on the `:where()` reference page](/en-US/docs/Web/CSS/Reference/Selectors/:where#examples).

### [Forgiving Selector Parsing](#forgiving_selector_parsing)

The specification defines `:is()` and `:where()` as accepting a [forgiving selector list](https://drafts.csswg.org/selectors-4/#typedef-forgiving-selector-list).

In CSS when using a selector list, if any of the selectors are invalid then the whole list is deemed invalid. When using `:is()` or `:where()` instead of the whole list of selectors being deemed invalid if one fails to parse, the incorrect or unsupported selector will be ignored and the others used.

css

```
:is(:valid, :unsupported) {
  /* â¦ */
}
```

Will still parse correctly and match `:valid` even in browsers which don't support `:unsupported`, whereas:

css

```
:valid,
:unsupported {
  /* â¦ */
}
```

Will be ignored in browsers which don't support `:unsupported` even if they support `:valid`.

## [Examples](#examples)

### [Simplifying list selectors](#simplifying_list_selectors)

The `:is()` pseudo-class can greatly simplify your CSS selectors. For example, take the following CSS:

css

```
/* 3-deep (or more) unordered lists use a square */
ol ol ul,
ol ul ul,
ol menu ul,
ol dir ul,
ol ol menu,
ol ul menu,
ol menu menu,
ol dir menu,
ol ol dir,
ol ul dir,
ol menu dir,
ol dir dir,
ul ol ul,
ul ul ul,
ul menu ul,
ul dir ul,
ul ol menu,
ul ul menu,
ul menu menu,
ul dir menu,
ul ol dir,
ul ul dir,
ul menu dir,
ul dir dir,
menu ol ul,
menu ul ul,
menu menu ul,
menu dir ul,
menu ol menu,
menu ul menu,
menu menu menu,
menu dir menu,
menu ol dir,
menu ul dir,
menu menu dir,
menu dir dir,
dir ol ul,
dir ul ul,
dir menu ul,
dir dir ul,
dir ol menu,
dir ul menu,
dir menu menu,
dir dir menu,
dir ol dir,
dir ul dir,
dir menu dir,
dir dir dir {
  list-style-type: square;
}
```

You can replace it with:

css

```
/* 3-deep (or more) unordered lists use a square */
:is(ol, ul, menu, dir) :is(ol, ul, menu, dir) :is(ul, menu, dir) {
  list-style-type: square;
}
```

### [Simplifying section selectors](#simplifying_section_selectors)

The `:is()` pseudo-class is particularly useful when dealing with HTML [sections and headings](/en-US/docs/Web/HTML/Reference/Elements/Heading_Elements). Since [`<section>`](/en-US/docs/Web/HTML/Reference/Elements/section), [`<article>`](/en-US/docs/Web/HTML/Reference/Elements/article), [`<aside>`](/en-US/docs/Web/HTML/Reference/Elements/aside), and [`<nav>`](/en-US/docs/Web/HTML/Reference/Elements/nav) are commonly nested together, without `:is()`, styling them to match one another can be tricky.

For example, without `:is()`, styling all the [h1](/en-US/docs/Web/HTML/Reference/Elements/Heading_Elements) elements at different depths could be very complicated:

css

```
/* Level 0 */
h1 {
  font-size: 30px;
}

/* Level 1 */
section h1,
article h1,
aside h1,
nav h1 {
  font-size: 25px;
}

/* Level 2 */
section section h1,
section article h1,
section aside h1,
section nav h1,
article section h1,
article article h1,
article aside h1,
article nav h1,
aside section h1,
aside article h1,
aside aside h1,
aside nav h1,
nav section h1,
nav article h1,
nav aside h1,
nav nav h1 {
  font-size: 20px;
}

/* Level 3 */
/* don't even think about it! */
```

Using `:is()`, though, it's much easier:

css

```
/* Level 0 */
h1 {
  font-size: 30px;
}
/* Level 1 */
:is(section, article, aside, nav) h1 {
  font-size: 25px;
}
/* Level 2 */
:is(section, article, aside, nav) :is(section, article, aside, nav) h1 {
  font-size: 20px;
}
/* Level 3 */
:is(section, article, aside, nav)
  :is(section, article, aside, nav)
  :is(section, article, aside, nav)
  h1 {
  font-size: 15px;
}
```

### [:is() does not select pseudo-elements](#is_does_not_select_pseudo-elements)

The `:is()` pseudo-class does not match pseudo-elements. So rather than this:

css

```
some-element:is(::before, ::after) {
  display: block;
}
```

or this:

css

```
:is(some-element::before, some-element::after) {
  display: block;
}
```

instead do:

css

```
some-element::before,
some-element::after {
  display: block;
}
```

## [Specifications](#specifications)

| Specification |
| --- |
| [Selectors Level 4  # matches-pseudo](https://drafts.csswg.org/selectors/#matches-pseudo) |

## [Browser compatibility](#browser_compatibility)

## [See also](#see_also)

- [`:where()`](/en-US/docs/Web/CSS/Reference/Selectors/:where) - Like `:is()`, but with 0 [specificity](/en-US/docs/Web/CSS/Guides/Cascade/Specificity).
- [Selector list](/en-US/docs/Web/CSS/Reference/Selectors/Selector_list)
- [Web components](/en-US/docs/Web/API/Web_components)

## Help improve MDN

Was this page helpful to you?

Yes

No

[Learn how to contribute](/en-US/docs/MDN/Community/Getting_started)

This page was last modified on Dec 16, 2025 by [MDN contributors](/en-US/docs/Web/CSS/Reference/Selectors/:is/contributors.txt).

[View this page on GitHub](https://github.com/mdn/content/blob/main/files/en-us/web/css/reference/selectors/_colon_is/index.md?plain=1 "Folder: en-us/web/css/reference/selectors/_colon_is (Opens in a new tab)") â¢ [Report a problem with this content](https://github.com/mdn/content/issues/new?template=page-report.yml&mdn-url=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FReference%2FSelectors%2F%3Ais&metadata=%3C%21--+Do+not+make+changes+below+this+line+--%3E%0A%3Cdetails%3E%0A%3Csummary%3EPage+report+details%3C%2Fsummary%3E%0A%0A*+Folder%3A+%60en-us%2Fweb%2Fcss%2Freference%2Fselectors%2F_colon_is%60%0A*+MDN+URL%3A+https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FReference%2FSelectors%2F%3Ais%0A*+GitHub+URL%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fblob%2Fmain%2Ffiles%2Fen-us%2Fweb%2Fcss%2Freference%2Fselectors%2F_colon_is%2Findex.md%0A*+Last+commit%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fcommit%2F33094d735e90b4dcae5733331b79c51fee997410%0A*+Document+last+modified%3A+2025-12-16T15%3A14%3A26.000Z%0A%0A%3C%2Fdetails%3E "This will take you to GitHub to file a new issue.")