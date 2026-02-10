# :focus-visible

Source: https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-visible

---

# :focus-visible

Baseline
Widely available

This feature is well established and works across many devices and browser versions. Itâs been available across browsers since March 2022.

- [Learn more](/en-US/docs/Glossary/Baseline/Compatibility)
- [See full compatibility](#browser_compatibility)
- [Report feedback](https://survey.alchemer.com/s3/7634825/MDN-baseline-feedback?page=%2Fen-US%2Fdocs%2FWeb%2FCSS%2FReference%2FSelectors%2F%3Afocus-visible&level=high)

 

The **`:focus-visible`** pseudo-class applies while an element matches the [`:focus`](/en-US/docs/Web/CSS/Reference/Selectors/:focus) pseudo-class and the UA ([User Agent](/en-US/docs/Glossary/User_agent)) determines via heuristics that the focus should be made evident on the element. (Many browsers show a "focus ring" by default in this case.)

## [Try it](#try_it)

```
label {
  display: block;
  margin-top: 1em;
}

input:focus-visible {
  outline: 2px solid crimson;
  border-radius: 3px;
}

select:focus-visible {
  border: 2px dashed crimson;
  border-radius: 3px;
  outline: none;
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

This selector is useful to provide a different focus indicator based on the user's input modality (mouse vs. keyboard).

## [Syntax](#syntax)

css

```
:focus-visible {
  /* ... */
}
```

## [:focus vs :focus-visible](#focus_vs_focus-visible)

Originally, user-agent CSS set focus styles based only on the `:focus` pseudo-class, styling most focused elements with a focus ring outline. This meant all elements, including all links and buttons, had a focus ring applied when focused, which many found ugly. Because of the appearance, some authors removed the user-agent outline focus styles. Changing focus style can decrease usability, while removing focus styles makes keyboard navigation inaccessible for sighted users.

Browsers no longer visibly indicate focus (such as by drawing a "focus ring"), around each element when it has focus. Instead, they use a variety of heuristics to provide focus indicators only when it would be most helpful to the user. For instance, when a button is clicked using a pointing device, the focus is generally not visually indicated, but when a text box needing user input has focus, focus is indicated. While focus styles are always required when users are navigating the page with the keyboard or when focus is managed via scripts, focus styles are not required when the user knows where they are putting focus, such as when they use a pointing device such as a mouse or finger to physically set focus on an element, unless that element continues to need user attention.

The `:focus` pseudo-class always matches the currently-focused element. The `:focus-visible` pseudo-class also matches the focused element, but only if the user needs to be informed where the focus currently is. Because the `:focus-visible` pseudo-class matches the focused element when needed, using the `:focus-visible` (instead of the `:focus` pseudo-class) allows authors to change the appearance of the focus indicator without changing when the focus indicator appears.

When the [`:focus`](/en-US/docs/Web/CSS/Reference/Selectors/:focus) pseudo-class is used, it always targets the currently focused element. This means that when a user employs a pointing device, a visible focus ring appears around the focused element, which some consider obtrusive. The `:focus-visible` pseudo-class respects user agents' selective focus indication behavior while still allowing focus indicator customization.

## [Accessibility](#accessibility)

### [Low vision](#low_vision)

Make sure the visual focus indicator can be seen by people with low vision. This will also benefit anyone use a screen in a brightly lit space (like outside in the sun). [WCAG 2.1 SC 1.4.11 Non-Text Contrast](https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast.html) requires that the visual focus indicator be at least 3 to 1.

- Accessible Visual Focus Indicators: [Give Your Site Some Focus! Tips for Designing Useful and Usable Focus Indicators](https://www.deque.com/blog/give-site-focus-tips-designing-usable-focus-indicators/)

### [Cognition](#cognition)

It may not be obvious as to why the focus indicator is appearing and disappearing if a person is using mixed forms of input. For users with cognitive concerns, or who are less technologically literate, this lack of consistent behavior for interactive elements may be confusing.

## [Examples](#examples)

### [Comparing :focus and :focus-visible](#comparing_focus_and_focus-visible)

This example presents three pairs of controls. Each pair consists of a [`text`](/en-US/docs/Web/HTML/Reference/Elements/input/text) input and a button.

- The first pair does not add any custom styles for focus states, and shows the default case.
- The second pair adds styles using the `:focus` pseudo-class.
- The third pair adds styles using the `:focus-visible` pseudo-class.

html

```
<input type="text" value="Default styles" /><br />
<button>Default styles</button><br />

<input class="focus-only" type="text" value=":focus" /><br />
<button class="focus-only">:focus</button><br />

<input class="focus-visible-only" type="text" value=":focus-visible" /><br />
<button class="focus-visible-only">:focus-visible</button>
```

css

```
input,
button {
  margin: 10px;
}

.focus-only:focus {
  outline: 2px solid black;
}

.focus-visible-only:focus-visible {
  outline: 4px dashed darkorange;
}
```

If you click each element in turn, you will see that when `:focus` is used to style the focus ring, the UA draws the focus ring when the user clicks the button. However, when `:focus-visible` is used to style the focus ring, the UA does not draw the focus ring when the user clicks the button, just like in the default case.

If you then tab through each element, you will see that in all three cases â default, `:focus`, and `:focus-visible` â the UA draws the focus ring around the button when the user navigates to it with the keyboard.

This shows how `:focus-visible` enables a designer to follow the browser's logic in determining when a focus ring should be shown.

### [Providing a :focus fallback](#providing_a_focus_fallback)

If your code has to work in old browser versions that do not support `:focus-visible`, check supports of `:focus-visible` with [`@supports`](/en-US/docs/Web/CSS/Reference/At-rules/@supports) and repeat the same focus styling in it, but inside a `:focus` rule. Note that even if you do not specify anything at all for `:focus`, old browsers will simply display the native outline, which can be enough.

html

```
<button class="button with-fallback" type="button">Button with fallback</button>
<button class="button without-fallback" type="button">
  Button without fallback
</button>
```

css

```
.button {
  margin: 10px;
  border: 2px solid darkgray;
  border-radius: 4px;
}

.button:focus-visible {
  /* Draw the focus when :focus-visible is supported */
  outline: 3px solid deepskyblue;
  outline-offset: 3px;
}

@supports not selector(:focus-visible) {
  .button.with-fallback:focus {
    /* Fallback for browsers without :focus-visible support */
    outline: 3px solid deepskyblue;
    outline-offset: 3px;
  }
}
```

## [Specifications](#specifications)

| Specification |
| --- |
| [Selectors Level 4  # the-focus-visible-pseudo](https://drafts.csswg.org/selectors/#the-focus-visible-pseudo) |

## [Browser compatibility](#browser_compatibility)

## [See also](#see_also)

- [`:focus`](/en-US/docs/Web/CSS/Reference/Selectors/:focus)
- [`:focus-within`](/en-US/docs/Web/CSS/Reference/Selectors/:focus-within)

## Help improve MDN

Was this page helpful to you?

Yes

No

[Learn how to contribute](/en-US/docs/MDN/Community/Getting_started)

This page was last modified on Dec 16, 2025 by [MDN contributors](/en-US/docs/Web/CSS/Reference/Selectors/:focus-visible/contributors.txt).

[View this page on GitHub](https://github.com/mdn/content/blob/main/files/en-us/web/css/reference/selectors/_colon_focus-visible/index.md?plain=1 "Folder: en-us/web/css/reference/selectors/_colon_focus-visible (Opens in a new tab)") â¢ [Report a problem with this content](https://github.com/mdn/content/issues/new?template=page-report.yml&mdn-url=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FReference%2FSelectors%2F%3Afocus-visible&metadata=%3C%21--+Do+not+make+changes+below+this+line+--%3E%0A%3Cdetails%3E%0A%3Csummary%3EPage+report+details%3C%2Fsummary%3E%0A%0A*+Folder%3A+%60en-us%2Fweb%2Fcss%2Freference%2Fselectors%2F_colon_focus-visible%60%0A*+MDN+URL%3A+https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FReference%2FSelectors%2F%3Afocus-visible%0A*+GitHub+URL%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fblob%2Fmain%2Ffiles%2Fen-us%2Fweb%2Fcss%2Freference%2Fselectors%2F_colon_focus-visible%2Findex.md%0A*+Last+commit%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fcommit%2F33094d735e90b4dcae5733331b79c51fee997410%0A*+Document+last+modified%3A+2025-12-16T15%3A14%3A26.000Z%0A%0A%3C%2Fdetails%3E "This will take you to GitHub to file a new issue.")