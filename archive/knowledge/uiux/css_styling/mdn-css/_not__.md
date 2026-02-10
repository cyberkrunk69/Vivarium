# :not()

Source: https://developer.mozilla.org/en-US/docs/Web/CSS/:not

---

# :not()

Baseline
Widely available

This feature is well established and works across many devices and browser versions. Itâs been available across browsers since July 2015.

- [Learn more](/en-US/docs/Glossary/Baseline/Compatibility)
- [See full compatibility](#browser_compatibility)
- [Report feedback](https://survey.alchemer.com/s3/7634825/MDN-baseline-feedback?page=%2Fen-US%2Fdocs%2FWeb%2FCSS%2FReference%2FSelectors%2F%3Anot&level=high)

 

The **`:not()`** [CSS](/en-US/docs/Web/CSS) [pseudo-class](/en-US/docs/Web/CSS/Reference/Selectors/Pseudo-classes) represents elements that do not match a list of selectors. Since it prevents specific items from being selected, it is known as the *negation pseudo-class*.

## [Try it](#try_it)

```
p:not(.irrelevant) {
  font-weight: bold;
}

p > strong,
p > b.important {
  color: crimson;
}

p > :not(strong, b.important) {
  color: darkmagenta;
}
```

```
<p>
  <b>Mars</b> is one of the most Earth-like planets. <b>Mars</b> day is almost
  the same as an Earth day, only <strong>37 minutes</strong> longer.
</p>

<p class="irrelevant">
  <b class="important">NASA</b>'s Jet <del>Momentum</del> Propulsion Laboratory
  is designing mission concepts to survive the <b>Venus</b> extreme temperatures
  and atmospheric pressure.
</p>
```

The `:not()` pseudo-class has a number of [quirks, tricks, and unexpected results](#description) that you should be aware of before using it.

## [Syntax](#syntax)

css

```
:not(<complex-selector-list>) {
  /* ... */
}
```

### [Parameters](#parameters)

The `:not()` pseudo-class requires a [selector list](/en-US/docs/Web/CSS/Guides/Selectors/Selector_structure#selector_list), a comma-separated list of one or more selectors, as its argument. The list must not contain a [pseudo-element](/en-US/docs/Web/CSS/Reference/Selectors/Pseudo-elements), but any other simple, compound, and complex selectors are allowed.

## [Description](#description)

There are several unusual effects and outcomes when using `:not()` that you should keep in mind when using it:

- Useless selectors can be written using this pseudo-class. For example, `:not(*)` matches any element which is not an element, which is obviously nonsense, so the accompanying rule will never be applied.
- This pseudo-class can increase the [specificity](/en-US/docs/Web/CSS/Guides/Cascade/Specificity) of a rule. For example, `#foo:not(#bar)` will match the same element as the simpler `#foo`, but has the higher specificity of two `id` selectors.
- The specificity of the `:not()` pseudo-class is replaced by the specificity of the most specific selector in its comma-separated argument of selectors; providing the same specificity as if it had been written [`:not(:is(argument))`](/en-US/docs/Web/CSS/Reference/Selectors/:is).
- `:not(.foo)` will match anything that isn't `.foo`, *including [`<html>`](/en-US/docs/Web/HTML/Reference/Elements/html) and [`<body>`](/en-US/docs/Web/HTML/Reference/Elements/body).*
- This selector will match everything that is "not an X". This may be surprising when used with [descendant combinators](/en-US/docs/Web/CSS/Reference/Selectors/Descendant_combinator), since there are multiple paths to select a target element. For instance, `body :not(table) a` will still apply to links inside a [`<table>`](/en-US/docs/Web/HTML/Reference/Elements/table), since [`<tr>`](/en-US/docs/Web/HTML/Reference/Elements/tr), [`<tbody>`](/en-US/docs/Web/HTML/Reference/Elements/tbody), [`<th>`](/en-US/docs/Web/HTML/Reference/Elements/th), [`<td>`](/en-US/docs/Web/HTML/Reference/Elements/td), [`<caption>`](/en-US/docs/Web/HTML/Reference/Elements/caption), etc. can all match the `:not(table)` part of the selector. To avoid this, you can use `body a:not(table a)` instead, which will only apply to links that are not descendants of a table.
- You can negate several selectors at the same time. Example: `:not(.foo, .bar)` is equivalent to `:not(.foo):not(.bar)`.
- If any selector passed to the `:not()` pseudo-class is invalid or not supported by the browser, the whole rule will be invalidated. The effective way to overcome this behavior is to use [`:is()`](/en-US/docs/Web/CSS/Reference/Selectors/:is) pseudo-class, which accepts a forgiving selector list. For example `:not(.foo, :invalid-pseudo-class)` will invalidate a whole rule, but `:not(:is(.foo, :invalid-pseudo-class))` will match any (*including [`<html>`](/en-US/docs/Web/HTML/Reference/Elements/html) and [`<body>`](/en-US/docs/Web/HTML/Reference/Elements/body)*) element that isn't `.foo`.

## [Examples](#examples)

### [Using :not() with valid selectors](#using_not_with_valid_selectors)

This example shows a few ways of using `:not()`.

#### HTML

html

```
<p>I am a paragraph.</p>
<p class="fancy">I am so very fancy!</p>
<div>I am NOT a paragraph.</div>
<h2>
  <span class="foo">foo inside h2</span>
  <span class="bar">bar inside h2</span>
</h2>
```

#### CSS

css

```
.fancy {
  text-shadow: 2px 2px 3px gold;
}

/* <p> elements that don't have a class `.fancy` */
p:not(.fancy) {
  color: green;
}

/* Elements that are not <p> elements */
body :not(p) {
  text-decoration: underline;
}

/* Elements that are not <div>s or `.fancy` */
body :not(div):not(.fancy) {
  font-weight: bold;
}

/* Elements that are not <div>s or `.fancy` */
body :not(div, .fancy) {
  text-decoration: overline underline;
}

/* Elements inside an <h2> that aren't a <span> with a class of `.foo` */
h2 :not(span.foo) {
  color: red;
}
```

#### Result

### [Using :not() with invalid selectors](#using_not_with_invalid_selectors)

This example shows the use of `:not()` with invalid selectors and how to prevent invalidation.

#### HTML

html

```
<p class="foo">I am a paragraph with .foo</p>
<p class="bar">I am a paragraph with .bar</p>
<div>I am a div without a class</div>
<div class="foo">I am a div with .foo</div>
<div class="bar">I am a div with .bar</div>
<div class="foo bar">I am a div with .foo and .bar</div>
```

#### CSS

css

```
/* Invalid rule, does nothing */
p:not(.foo, :invalid-pseudo-class) {
  color: red;
  font-style: italic;
}

/* Select all <p> elements without the `foo` class */
p:not(:is(.foo, :invalid-pseudo-class)) {
  color: green;
  border-top: dotted thin currentColor;
}

/* Select all <div> elements without the `foo` or the `bar` class */
div:not(.foo, .bar) {
  color: red;
  font-style: italic;
}

/* Select all <div> elements without the `foo` or the `bar` class */
div:not(:is(.foo, .bar)) {
  border-bottom: dotted thin currentColor;
}
```

#### Result

The `p:not(.foo, :invalid-pseudo-class)` rule is invalid because it contains an invalid selector. The `:is()` pseudo-class accepts a forgiving selector list, so the `:is(.foo, :invalid-pseudo-class)` rule is valid and equivalent to `:is(.foo)`. Thus, the `p:not(:is(.foo, :invalid-pseudo-class))` rule is valid and equivalent to `p:not(.foo)`.

If `:invalid-pseudo-class` was a valid selector, the first two rules above would still be equivalent (the last two rules showcase that). The use of `:is()` makes the rule more robust.

## [Specifications](#specifications)

| Specification |
| --- |
| [Selectors Level 4  # negation](https://drafts.csswg.org/selectors/#negation) |

## [Browser compatibility](#browser_compatibility)

## [See also](#see_also)

- [Pseudo-classes](/en-US/docs/Web/CSS/Reference/Selectors/Pseudo-classes)
- [Learn: Pseudo-classes and pseudo-elements](/en-US/docs/Learn_web_development/Core/Styling_basics/Pseudo_classes_and_elements)
- Other functional CSS pseudo-classes:

  - [`:has()`](/en-US/docs/Web/CSS/Reference/Selectors/:has)
  - [`:is()`](/en-US/docs/Web/CSS/Reference/Selectors/:is)
  - [`:where()`](/en-US/docs/Web/CSS/Reference/Selectors/:where)
- [How :not() chains multiple selectors](/en-US/blog/css-not-pseudo-multiple-selectors/) on MDN blog (2023)

## Help improve MDN

Was this page helpful to you?

Yes

No

[Learn how to contribute](/en-US/docs/MDN/Community/Getting_started)

This page was last modified on Dec 16, 2025 by [MDN contributors](/en-US/docs/Web/CSS/Reference/Selectors/:not/contributors.txt).

[View this page on GitHub](https://github.com/mdn/content/blob/main/files/en-us/web/css/reference/selectors/_colon_not/index.md?plain=1 "Folder: en-us/web/css/reference/selectors/_colon_not (Opens in a new tab)") â¢ [Report a problem with this content](https://github.com/mdn/content/issues/new?template=page-report.yml&mdn-url=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FReference%2FSelectors%2F%3Anot&metadata=%3C%21--+Do+not+make+changes+below+this+line+--%3E%0A%3Cdetails%3E%0A%3Csummary%3EPage+report+details%3C%2Fsummary%3E%0A%0A*+Folder%3A+%60en-us%2Fweb%2Fcss%2Freference%2Fselectors%2F_colon_not%60%0A*+MDN+URL%3A+https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FReference%2FSelectors%2F%3Anot%0A*+GitHub+URL%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fblob%2Fmain%2Ffiles%2Fen-us%2Fweb%2Fcss%2Freference%2Fselectors%2F_colon_not%2Findex.md%0A*+Last+commit%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fcommit%2F33094d735e90b4dcae5733331b79c51fee997410%0A*+Document+last+modified%3A+2025-12-16T15%3A14%3A26.000Z%0A%0A%3C%2Fdetails%3E "This will take you to GitHub to file a new issue.")