# Accessibility

Source: https://carbondesignsystem.com/guidelines/accessibility/keyboard/

---

# Accessibility

Keyboard accessibility enables users who rely on or prefer using a keyboard to
use your product. All interactive content and elements should include keyboard
functionality.

## Keyboard accessibility

Common keyboard interactions include using the

```
tab
```

Copy to clipboard

key to select different
interactive elements on a page and using the

```
enter
```

Copy to clipboard

key or the

```
spacebar
```

Copy to clipboard

to
activate an in-focus element.

[##### IBM Checkpoint 2.1.1 Keyboard

![IBM bee icon](/2a7ef6c341581a6ceee69391700f13f0/bee.svg)](https://www.ibm.com/able/requirements/requirements/#2_1_1)

### Focus indicators

The

```
tab
```

Copy to clipboard

key navigates through all interactive elements on a page in the order
they appear in the HTML document. A default visual indicator is provided by the
web browser in use. The display is a border around the focused element. When an
element is in focus, it can be further activated using the keyboard.

[##### IBM Checkpoint 2.4.7 Focus Visible

![IBM bee icon](/2a7ef6c341581a6ceee69391700f13f0/bee.svg)](https://www.ibm.com/able/requirements/requirements/#2_4_7)

### Navigation order

The order in which interactive elements receive focus should be logical and
predictable. Create the tab flow hierarchy by using the source code to arrange
the keyboard navigation. A common flow might begin with the header, followed by
the main navigation, then content navigation (from left to right, top to
bottom), and end with the footer. Try to give all your users the same
experience.

Use natively-accessible elements in navigation to activate links, buttons, and
form controls with a keyboard. Reinforce
[semantic HTML](./developers#use-semantic-html) to convey intent and meaning
instead of solely defining the look and feel of an element. Enhance with ARIA
(Accessible Rich Internet Application) labels when necessary.

[##### IBM Checkpoint 2.4.3 Focus Order

![IBM bee icon](/2a7ef6c341581a6ceee69391700f13f0/bee.svg)](https://www.ibm.com/able/requirements/requirements/#2_4_3)

### Landmarks

For users of screen readers, communicate the different areas of the screen and
what they do with landmarks by using appropriate HTML5 labels. Screen reader
users can then quickly jump to any area they want.

[##### IBM Checkpoint 1.3.1 Info and Relationships

![IBM bee icon](/2a7ef6c341581a6ceee69391700f13f0/bee.svg)](https://www.ibm.com/able/requirements/requirements/#1_3_1)

[Edit this page on GitHub](https://github.com/carbon-design-system/carbon-website/edit/main/src/pages/guidelines/accessibility/keyboard.mdx)

[Previous

Accessibility: Developers](/guidelines/accessibility/developers/)

[Next

Guidelines: Carbon for AI](/guidelines/carbon-for-ai/)