# :focus-within

Source: https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-within

---

# :focus-within

Baseline
Widely available

This feature is well established and works across many devices and browser versions. Itâs been available across browsers since January 2020.

- [Learn more](/en-US/docs/Glossary/Baseline/Compatibility)
- [See full compatibility](#browser_compatibility)
- [Report feedback](https://survey.alchemer.com/s3/7634825/MDN-baseline-feedback?page=%2Fen-US%2Fdocs%2FWeb%2FCSS%2FReference%2FSelectors%2F%3Afocus-within&level=high)

 

The **`:focus-within`** [CSS](/en-US/docs/Web/CSS) [pseudo-class](/en-US/docs/Web/CSS/Reference/Selectors/Pseudo-classes) matches an element if the element or any of its descendants are focused. In other words, it represents an element that is itself matched by the [`:focus`](/en-US/docs/Web/CSS/Reference/Selectors/:focus) pseudo-class or has a descendant that is matched by `:focus`. (This includes descendants in [shadow trees](/en-US/docs/Web/API/Web_components/Using_shadow_DOM).)

## [Try it](#try_it)

```
label {
  display: block;
  margin-top: 1em;
}

label:focus-within {
  font-weight: bold;
}
```

```
<form>
  <p>Which flavor would you like to order?</p>
  <label>Full Name: <input name="firstName" type="text" /></label>
  <label
    >Flavor:
    <select name="flavor">
      <option>Cherry</option>
      <option>Green Tea</option>
      <option>Moose Tracks</option>
      <option>Mint Chip</option>
    </select>
  </label>
</form>
```

This selector is useful, to take a common example, for highlighting an entire [`<form>`](/en-US/docs/Web/HTML/Reference/Elements/form) container when the user focuses on one of its [`<input>`](/en-US/docs/Web/HTML/Reference/Elements/input) fields.

## [Syntax](#syntax)

css

```
:focus-within {
  /* ... */
}
```

## [Examples](#examples)

In this example, the form will receive special coloring styles when either text input receives focus.

### [HTML](#html)

html

```
<p>Try typing into this form.</p>

<form>
  <label for="given_name">Given Name:</label>
  <input id="given_name" type="text" />
  <br />
  <label for="family_name">Family Name:</label>
  <input id="family_name" type="text" />
</form>
```

### [CSS](#css)

css

```
form {
  border: 1px solid;
  color: gray;
  padding: 4px;
}

form:focus-within {
  background: #ffff88;
  color: black;
}

input {
  margin: 4px;
}
```

### [Result](#result)

## [Specifications](#specifications)

| Specification |
| --- |
| [Selectors Level 4  # the-focus-within-pseudo](https://drafts.csswg.org/selectors/#the-focus-within-pseudo) |

## [Browser compatibility](#browser_compatibility)

## [See also](#see_also)

- [`:focus`](/en-US/docs/Web/CSS/Reference/Selectors/:focus)
- [`:focus-visible`](/en-US/docs/Web/CSS/Reference/Selectors/:focus-visible)
- [Grab your user's attention with the focus-within selector](https://dev.to/vtrpldn/grab-your-user-s-attention-with-the-focus-within-css-selector-4d4)

## Help improve MDN

Was this page helpful to you?

Yes

No

[Learn how to contribute](/en-US/docs/MDN/Community/Getting_started)

This page was last modified on Nov 3, 2025 by [MDN contributors](/en-US/docs/Web/CSS/Reference/Selectors/:focus-within/contributors.txt).

[View this page on GitHub](https://github.com/mdn/content/blob/main/files/en-us/web/css/reference/selectors/_colon_focus-within/index.md?plain=1 "Folder: en-us/web/css/reference/selectors/_colon_focus-within (Opens in a new tab)") â¢ [Report a problem with this content](https://github.com/mdn/content/issues/new?template=page-report.yml&mdn-url=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FReference%2FSelectors%2F%3Afocus-within&metadata=%3C%21--+Do+not+make+changes+below+this+line+--%3E%0A%3Cdetails%3E%0A%3Csummary%3EPage+report+details%3C%2Fsummary%3E%0A%0A*+Folder%3A+%60en-us%2Fweb%2Fcss%2Freference%2Fselectors%2F_colon_focus-within%60%0A*+MDN+URL%3A+https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FReference%2FSelectors%2F%3Afocus-within%0A*+GitHub+URL%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fblob%2Fmain%2Ffiles%2Fen-us%2Fweb%2Fcss%2Freference%2Fselectors%2F_colon_focus-within%2Findex.md%0A*+Last+commit%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fcommit%2Fc52ed787442db9d65b21f5c2874fa6bfd08a253a%0A*+Document+last+modified%3A+2025-11-03T17%3A48%3A17.000Z%0A%0A%3C%2Fdetails%3E "This will take you to GitHub to file a new issue.")