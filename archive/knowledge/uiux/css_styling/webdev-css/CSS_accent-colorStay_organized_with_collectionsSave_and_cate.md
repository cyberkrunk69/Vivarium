# CSS accent-colorStay organized with collectionsSave and categorize content based on your preferences.

Source: https://web.dev/articles/accent-color

---

- [Home](https://web.dev/)
- [Articles](https://web.dev/articles)

# CSS accent-color Stay organized with collections Save and categorize content based on your preferences.

Bring your brand color to built-in HTML form inputs with one line of code.

![Adam Argyle](https://web.dev/images/authors/adamargyle.jpg)

Adam Argyle

![Joey Arhar](https://web.dev/images/authors/jarhar.jpg)

Joey Arhar

Published: August 11, 2021

Today's HTML form elements are [difficult to
customize](https://codepen.io/GeoffreyCrofte/pen/BiHzp). It feels as if it's
a choice between few or no custom styles, or resetting input styles and
build it up from scratch. Building it up from scratch ends up being much more
work than anticipated. It can also lead to forgotten styles for element states
([indeterminate](https://developer.mozilla.org/docs/Web/CSS/:indeterminate),
I'm looking at you), and the loss of built-in accessibility features.
To fully recreate what the browser provides may be more
work than you're looking to take on.

```
accent-color: hotpink;
```

CSS `accent-color` from the [CSS UI
specification](https://www.w3.org/TR/css-ui-4/#widget-accent) is here to tint
elements with one line of CSS, saving you from customization efforts by
providing a way to bring your brand into elements.

![A light theme screenshot of an accent-color demo where
    checkbox, radio buttons, a range slider and progress element
    are all tinted hotpink.](/static/articles/accent-color/image/a-light-theme-screenshot-e2988ab5bb352.png)

[Demo](https://codepen.io/web-dot-dev/pen/PomBZdy)

The `accent-color` property also works with
[`color-scheme`](/articles/color-scheme), allowing authors to tint both
the light and dark elements.
In the following example the user has a dark theme active, the page uses
`color-scheme: light dark`, and uses the same `accent-color: hotpink` for dark
themed hotpink tinted controls.

![A dark theme screenshot of an accent-color demo where
    checkbox, radio buttons, a range slider and progress element
    are all tinted hotpink.](/static/articles/accent-color/image/a-dark-theme-screenshot-5c090145c9c8e.png)

[Demo](https://codepen.io/web-dot-dev/pen/PomBZdy)

## Supported elements

Currently, only four elements will tint via the `accent-color` property:
[checkbox](#checkbox), [radio](#radio), [range](#range) and
[progress](#progress). Each can be previewed here
<https://accent-color.glitch.me> in light and
dark color schemes.

### Checkbox

### Radio

### Range

### Progress

## Guaranteeing contrast

To prevent inaccessible elements from existing, browsers with `accent-color`
need to determine an [eligible contrast
color](https://webaim.org/articles/contrast/) to be used alongside the custom
accent. Below is a screenshot demonstrating how Chrome 94 (left) and Firefox 92
Nightly (right) differ in their algorithms:

![A screenshot of Firefox and Chromium side by side,
  rendering a full spectrum of checkboxes in various hues and darknesses.](/static/articles/accent-color/image/a-screenshot-firefox-ch-cff62212a549a.png)

The most important thing to take away from this, is to **trust the browser**.
Provide a brand color, and trust that it will make smart decisions for you.

## Extra: More tinting

You may be wondering how to tint more than these four form elements? Here's a
minimal sandbox which tints:

- the focus ring
- text selection highlights
- list [markers](/articles/css-marker-pseudo-element)
- arrow indicators (Webkit only)
- scrollbar thumb (Firefox only)

```
html {
  --brand: hotpink;
  scrollbar-color: hotpink Canvas;
}

:root { accent-color: var(--brand); }
:focus-visible { outline-color: var(--brand); }
::selection { background-color: var(--brand); }
::marker { color: var(--brand); }

:is(
  ::-webkit-calendar-picker-indicator,
  ::-webkit-clear-button,
  ::-webkit-inner-spin-button,
  ::-webkit-outer-spin-button
) {
  color: var(--brand);
}
```

### Potential future

The spec does not limit the application of `accent-color` to the four elements
shown in this article, more support could be added later. Elements like the
selected `<option>` in a `<select>` could be highlighted with the
`accent-color`.

What else do you like to tint on the web? Tweet
[@argyleink](https://twitter.com/argyleink) with your selector and it might get
added to this article!

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2021-08-11 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2021-08-11 UTC."],[],[]]