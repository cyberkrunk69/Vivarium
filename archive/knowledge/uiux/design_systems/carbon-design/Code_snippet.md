# Code snippet

Source: https://carbondesignsystem.com/components/code-snippet/usage/

---

# Code snippet

Code snippets are strings or small blocks of reusable code that can be copied
and inserted in a code file.

- [Live demo](#live-demo)
- [Overview](#overview)
- [Formatting](#formatting)
- [Content](#content)
- [Universal behaviors](#universal-behaviors)
- [Inline](#inline)
- [Single line](#single-line)
- [Multi-line](#multi-line)
- [Modifiers](#modifiers)
- [Feedback](#feedback)

## Live demo

Theme selector

White

---

Variant selector

Inline

---

This live demo contains only a preview of functionality and styles available for this component. View the [full demo](https://react.carbondesignsystem.com/?path=/story/components-codesnippet--inline&globals=theme:white) on Storybook for additional information such as its version, controls, and API documentation.

### Accessibility testing status For every latest release, Carbon runs tests on all components to meet the [accessibility requirements](https://www.ibm.com/able/requirements/requirements/). These different statuses report the work that Carbon has done in the back end. These tests appear only when the components are stable.

[##### Default state

Partially tested](//accessibility/#accessibility-testing-status)

[##### Advanced states

Tested](//accessibility/#accessibility-testing-status)

[##### Screen reader

Manually tested](//accessibility/#accessibility-testing-status)

[##### Keyboard navigation

Tested](//accessibility/#accessibility-testing-status)

## Overview

There are three different variants of code snippets to help cater to varied line
length use cases—inline, single line, and multi-line.

### Variants

| Variant | Purpose |
| --- | --- |
| [Inline](#inline) | A block of text used inline with sentences or paragraphs. |
| [Single line](#single-line) | A single line of code. |
| [Multi-line](#multi-line) | Multiple lines of code with the ability to show more or less strings. |

### When to use

- Use a code snippet to help the user copy strings of text easily, or if you
  want to call out key words for the user.
- Code snippets are typically used in code documentation to help the user get
  started quickly.

### When not to use

- Do not use a code snippet if you want the user to change the input value. Our
  code snippets are read only.

## Formatting

### Anatomy

![Code snippet anatomy](/static/19ae20a3b0034b34355b4c4e503a8dd9/3cbba/code-snippet-usage-1.png)

1. **Snippet text:** Lines or a block of code.
2. **Copy button (optional)**: An icon button to copy the code to the clipboard.
3. **Show more button (optional)**: A ghost button to expand or collapse the
   code snippet to show more or fewer lines of code.

### Placement

Code snippet containers should vertically align to the grid with other form
components on a page.

*Note: If using an inline code snippet, the snippet will live within a body of
text.*

![Do align code snippet containers to the grid.](/static/3cc037a350d20153507d193727d3d8d6/a5df1/code-snippet-usage-2-do.png)

Do align code snippet containers to the grid.

![Do not align code snippet text to the grid and hang the container.](/static/18471de5c4e81eeb0cc34644e9bc47b0/a5df1/code-snippet-usage-2-don't.png)

Do not align code snippet text to the grid and hang the container.

## Content

### Main elements

#### Snippet text

- Make sure the code is using the correct syntax so that the code will not break
  if the user copies it to their clipboard.

#### Copy button tooltip

- The copy button should be accompanied by a tooltip. Tooltip feedback text
  should be concise and describe the action taken when the user clicks the copy
  button. By default we display the text “Copied to clipboard”.

#### Show more button

- The ghost button text should describe what the button will reveal or hide when
  the user clicks it. By default we display the text “Show more” or “Show less”.

### Further guidance

For further content guidance, see Carbon’s
[content guidelines](/guidelines/content/overview).

## Universal behaviors

### Copy to clipboard

Code snippets by default have a copy functionality that allows users to copy the
provided code to their clipboard. The copy icon must be accompanied by a
confirmation tooltip that states the successful action of copying an item to the
clipboard. Having copy functionality is optional and can be removed if it’s not
necessary for your use case.

![Code snippet copy to clipboard tooltip](/static/2512f009d0c265ab7fa04cfc7bc502e3/3cbba/code-snippet-usage-3.png)

## Interactions

#### Mouse

An inline code snippet can be copied by clicking anywhere on the snippet itself.

![Inline code snippet click target](/static/33f962bda636d2477c23b9dbec2ddc78/3cbba/code-snippet-usage-4a.png)

A single line code snippet can be copied by clicking on the “copy” icon. The
browser also provides an ability to manually highlight the text and choose
“copy” from the context menu (right click).

![Single line code snippet click targets](/static/cdeb0764e54beda3346f10efefa48581/3cbba/code-snippet-usage-4b.png)

A multi-line code snippet can be copied by clicking on the copy icon or by
manually highlighting the text and right clicking “copy”.

![Multi-line code snippet click targets](/static/22b04ada75f071b7881ed15d7bf82234/3cbba/code-snippet-usage-4c.png)

#### Keyboard

#### Copy button:

- An inline code snippet, and the copy button of the single line and multiline
  snippets can be focused by pressing

  ```
  Tab
  ```

  Copy to clipboard

  .
- The copy functionality can be activated by pressing either

  ```
  Space
  ```

  Copy to clipboard

  or

  ```
  Enter
  ```

  Copy to clipboard

  .
- After the copy is activated, the focus remains on the button since there is no
  change in context.

#### Show more button:

- The “Show more” ghost button in the multi-line code snippet can be focused by
  pressing

  ```
  Tab
  ```

  Copy to clipboard

  .
- Show more or less code by pressing

  ```
  Space
  ```

  Copy to clipboard

  or

  ```
  Enter
  ```

  Copy to clipboard

  while the ghost button
  is in focus.

For additional keyboard interactions, see the
[accessibility tab](/components/code-snippet/accessibility#keyboard-interaction).

## Inline

Use inline code snippets within bodies of text. Using code snippets inline helps
create emphasis on important key words to copy and makes long bodies of text
easier to scan. Refrain from having inline code snippets that extend to multiple
lines.

![Inline code snippet in context](/static/591f23a2048a58d2887327b0f1a33ad5/3cbba/code-snippet-usage-5.png)

## Single line

Use single line code snippets for longer strings of code that can still be
presented on one line.

![Single line code snippet in context](/static/766b78fe8f51d0dbfd54c89e702b3c5f/3cbba/code-snippet-usage-6a.png)

### Single line overflow content

If the text in a single line code snippet is lengthy, the text overflows into a
horizontal scroll.

![Single line code snippet with overflow text](/static/adb14b78b3f131234a179d75fa8f14eb/3cbba/code-snippet-usage-6b.png)

## Multi-line

Use multi-line code snippets for displaying multiple lines of code.

![Multi-line code snippet with overflow text](/static/d2187abb3f7509854c71a3cb6d170577/3cbba/code-snippet-usage-7a.png)

### Multi-line overflow content

#### Show more button

A Show more ghost button can be added to a multi-line code snippet to show more
or fewer lines of code. Use this functionality if your layout is tight on space.

![Expanded and collapsed multi-line code snippet](/static/907db95360b7c8e49a2fbbdc52ab0a2b/3cbba/code-snippet-usage-7b.png)

#### Vertical scroll

Alternatively, you can apply vertical scrolling to the code snippet if there are
more than nine lines of code.

#### Horizontal scroll

Terminal commands are often longer strings and should only appear on one line.
Apply horizontal scrolling to maintain the set width of the box for these longer
strings.

## Modifiers

#### Light

Use the

```
light
```

Copy to clipboard

prop modifier when using a code snippet on a background other
than the UI background for that theme. The light prop changes the background
color token of the code snippet from

```
field-01
```

Copy to clipboard

to

```
field-02
```

Copy to clipboard

.

![Light prop applied to a single line code snippet](/static/a4a0aca70c6d598af2c022df80e5e02a/3cbba/code-snippet-usage-8.png)

## Feedback

Help us improve this component by providing feedback, asking questions, and
leaving any other comments on
[GitHub](https://github.com/carbon-design-system/carbon-website/issues/new?assignees=&labels=feedback&template=feedback.md).

[Edit this page on GitHub](https://github.com/carbon-design-system/carbon-website/edit/main/src/pages/components/code-snippet/usage.mdx)

[Previous

Components: Checkbox](/components/checkbox/usage/)

[Next

Code snippet: Style](/components/code-snippet/style/)