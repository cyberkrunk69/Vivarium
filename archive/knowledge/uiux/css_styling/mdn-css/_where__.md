# :where()

Source: https://developer.mozilla.org/en-US/docs/Web/CSS/:where

---

# :where()

Baseline
Widely available

This feature is well established and works across many devices and browser versions. Itâs been available across browsers since January 2021.

- [Learn more](/en-US/docs/Glossary/Baseline/Compatibility)
- [See full compatibility](#browser_compatibility)
- [Report feedback](https://survey.alchemer.com/s3/7634825/MDN-baseline-feedback?page=%2Fen-US%2Fdocs%2FWeb%2FCSS%2FReference%2FSelectors%2F%3Awhere&level=high)

 

The **`:where()`** [CSS](/en-US/docs/Web/CSS) [pseudo-class](/en-US/docs/Web/CSS/Reference/Selectors/Pseudo-classes) function takes a selector list as its argument, and selects any element that can be selected by one of the selectors in that list.

The difference between `:where()` and [`:is()`](/en-US/docs/Web/CSS/Reference/Selectors/:is) is that `:where()` always has 0 [specificity](/en-US/docs/Web/CSS/Guides/Cascade/Specificity), whereas `:is()` takes on the specificity of the most specific selector in its arguments.

## [Try it](#try_it)

```
ol {
  list-style-type: upper-alpha;
  color: darkblue;
}

/* Not applied to ol, because of lower specificity */
:where(ol, ul, menu:unsupported) :where(ol, ul) {
  color: green;
}

:where(ol, ul) :where(ol, ul) ol {
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
:where(<complex-selector-list>) {
  /* ... */
}
```

### [Parameters](#parameters)

The `:where()` pseudo-class requires a [selector list](/en-US/docs/Web/CSS/Guides/Selectors/Selector_structure#selector_list), a comma-separated list of one or more selectors, as its argument. The list must not contain a [pseudo-element](/en-US/docs/Web/CSS/Reference/Selectors/Pseudo-elements), but any other simple, compound, and complex selectors are allowed.

### [Forgiving Selector Parsing](#forgiving_selector_parsing)

The specification defines `:is()` and `:where()` as accepting a [forgiving selector list](/en-US/docs/Web/CSS/Reference/Selectors/Selector_list#forgiving_selector_list).

In CSS when using a selector list, if any of the selectors are invalid then the whole list is deemed invalid. When using `:is()` or `:where()` instead of the whole list of selectors being deemed invalid if one fails to parse, the incorrect or unsupported selector will be ignored and the others used.

css

```
:where(:valid, :unsupported) {
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

### [Comparing :where() and :is()](#comparing_where_and_is)

This example shows how `:where()` works, and also illustrates the difference between `:where()` and `:is()`.

Take the following HTML:

html

```
<article>
  <h2>:is()-styled links</h2>
  <section class="is-styling">
    <p>
      Here is my main content. This
      <a href="https://mozilla.org">contains a link</a>.
    </p>
  </section>

  <aside class="is-styling">
    <p>
      Here is my aside content. This
      <a href="https://developer.mozilla.org">also contains a link</a>.
    </p>
  </aside>

  <footer class="is-styling">
    <p>
      This is my footer, also containing
      <a href="https://github.com/mdn">a link</a>.
    </p>
  </footer>
</article>

<article>
  <h2>:where()-styled links</h2>
  <section class="where-styling">
    <p>
      Here is my main content. This
      <a href="https://mozilla.org">contains a link</a>.
    </p>
  </section>

  <aside class="where-styling">
    <p>
      Here is my aside content. This
      <a href="https://developer.mozilla.org">also contains a link</a>.
    </p>
  </aside>

  <footer class="where-styling">
    <p>
      This is my footer, also containing
      <a href="https://github.com/mdn">a link</a>.
    </p>
  </footer>
</article>
```

In this somewhat-contrived example, we have two articles that each contain a section, an aside, and a footer. They differ by the classes used to mark the child elements.

To group the selection of links, while keeping the `is-styling` and `where-styling` styles distinct, we *could* use `:is()` or `:where()`, in the following manner:

css

```
html {
  font-family: sans-serif;
  font-size: 150%;
}

:is(section.is-styling, aside.is-styling, footer.is-styling) a {
  color: red;
}

:where(section.where-styling, aside.where-styling, footer.where-styling) a {
  color: orange;
}
```

However, what if we later want to override the color of links in the footers using a compound selector made up of low-specificity type selectors?

css

```
footer a {
  color: blue;
}
```

This won't work for the red links, because the selectors inside `:is()` count towards the specificity of the overall selector, and class selectors have a higher specificity than element selectors.

However, selectors inside `:where()` have specificity 0, so the orange footer link will be overridden by our type-only compound selector.

**Note:**
You can also find this example on GitHub; see [is-where](https://mdn.github.io/css-examples/is-where/).

## [Specifications](#specifications)

| Specification |
| --- |
| [Selectors Level 4  # zero-matches](https://drafts.csswg.org/selectors/#zero-matches) |

## [Browser compatibility](#browser_compatibility)

## [See also](#see_also)

- [`:is()`](/en-US/docs/Web/CSS/Reference/Selectors/:is)
- [Selector list](/en-US/docs/Web/CSS/Reference/Selectors/Selector_list)
- [Web components](/en-US/docs/Web/API/Web_components)
- [Forgiving selector list](https://drafts.csswg.org/selectors-4/#typedef-forgiving-selector-list) via csswg.org.

## Help improve MDN

Was this page helpful to you?

Yes

No

[Learn how to contribute](/en-US/docs/MDN/Community/Getting_started)

This page was last modified on Jan 26, 2026 by [MDN contributors](/en-US/docs/Web/CSS/Reference/Selectors/:where/contributors.txt).

[View this page on GitHub](https://github.com/mdn/content/blob/main/files/en-us/web/css/reference/selectors/_colon_where/index.md?plain=1 "Folder: en-us/web/css/reference/selectors/_colon_where (Opens in a new tab)") â¢ [Report a problem with this content](https://github.com/mdn/content/issues/new?template=page-report.yml&mdn-url=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FReference%2FSelectors%2F%3Awhere&metadata=%3C%21--+Do+not+make+changes+below+this+line+--%3E%0A%3Cdetails%3E%0A%3Csummary%3EPage+report+details%3C%2Fsummary%3E%0A%0A*+Folder%3A+%60en-us%2Fweb%2Fcss%2Freference%2Fselectors%2F_colon_where%60%0A*+MDN+URL%3A+https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FReference%2FSelectors%2F%3Awhere%0A*+GitHub+URL%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fblob%2Fmain%2Ffiles%2Fen-us%2Fweb%2Fcss%2Freference%2Fselectors%2F_colon_where%2Findex.md%0A*+Last+commit%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fcommit%2F235f91c4deeb3a62492fdc82565afc56c11ec153%0A*+Document+last+modified%3A+2026-01-26T10%3A30%3A01.000Z%0A%0A%3C%2Fdetails%3E "This will take you to GitHub to file a new issue.")