# Text input

Source: https://carbondesignsystem.com/components/text-input/usage/

---

# Text input

Text inputs enable users to enter free-form text data. You can use them for long
and short-form entries.

[Text input](https://react.carbondesignsystem.com/?path=/story/components-textinput--with-ai-label)
and
[text area](https://react.carbondesignsystem.com/?path=/story/components-textarea--with-ai-label)
with AI label are now stable. These additions change the visual appearance of
the components and introduces an AI explainability feature when AI is present in
the components. See the [AI presence](/components/text-input/usage/#ai-presence)
section for more details.

- [Live demo](#live-demo)
- [Overview](#overview)
- [Text input](#text-input)
- [Text area](#text-area)
- [Formatting](#formatting)
- [Content](#content)
- [Universal behaviors](#universal-behaviors)
- [Modifiers](#modifiers)
- [AI Presence](#ai-presence)
- [Related](#related)
- [Feedback](#feedback)

## Live demo

Theme selector

White

---

Variant selector

Default

---

This live demo contains only a preview of functionality and styles available for this component. View the [full demo](https://react.carbondesignsystem.com/?path=/story/components-textinput--default&globals=theme:white) on Storybook for additional information such as its version, controls, and API documentation.

### Accessibility testing status For every latest release, Carbon runs tests on all components to meet the [accessibility requirements](https://www.ibm.com/able/requirements/requirements/). These different statuses report the work that Carbon has done in the back end. These tests appear only when the components are stable.

Variant

Text input

---

[##### Default state

Tested](//accessibility/#accessibility-testing-status)

[##### Advanced states

Tested](//accessibility/#accessibility-testing-status)

[##### Screen reader

Manually tested](//accessibility/#accessibility-testing-status)

[##### Keyboard navigation

Tested](//accessibility/#accessibility-testing-status)

[##### Default state

Tested](//accessibility/#accessibility-testing-status)

[##### Advanced states

Tested](//accessibility/#accessibility-testing-status)

[##### Screen reader

Manually tested](//accessibility/#accessibility-testing-status)

[##### Keyboard navigation

Tested](//accessibility/#accessibility-testing-status)

[##### Default state

Not tested](//accessibility/#accessibility-testing-status)

[##### Advanced states

Not tested](//accessibility/#accessibility-testing-status)

[##### Screen reader

Manually tested](//accessibility/#accessibility-testing-status)

[##### Keyboard navigation

Not available](//accessibility/#accessibility-testing-status)

[##### Default state

Not tested](//accessibility/#accessibility-testing-status)

[##### Advanced states

Not tested](//accessibility/#accessibility-testing-status)

[##### Screen reader

Not available](//accessibility/#accessibility-testing-status)

[##### Keyboard navigation

Not available](//accessibility/#accessibility-testing-status)

## Overview

Text inputs enable users to enter free-form text data. The type of text field
used should reflect the length of the content you expect the user to enter. The
default text input is for short, one-line content, whereas text area is for
longer, multi-line entries.

![Text input and text area example](/static/e84198fa0dca3973f497a6d2677e731f/3cbba/text-input-usage-2.png)

#### When to use

- A user needs to input unique information that cannot be predicted with a
  preset of options.
- A user needs to input memorable data that can be entered more quickly in a
  free-hand format versus a more complex control.

#### When not to use

- If a user can only enter an option from a predefined list then avoid using a
  free-form text input as it is likely to result in an error. Consider using a
  selection control such as a dropdown, select, or radio button group instead.

### Variants

| Variant | Purpose |
| --- | --- |
| [Text input](/components/text-input/usage/#text-input) | When the expected user input is a single line of text. |
| [Text area](/components/text-input/usage/#text-area) | When the expected user input is more than a few words that could span multiple lines. |

## Text input

Use a text input when the expected user input is a single line of text. Text
inputs have a fixed height and are used to enter simple free-form data entries
with any combination of letters, numbers, or symbols. There are two styles of
text input, default and fluid, which share the same functionality but look
visually different. The context of how or where the component is used will
dictate which style to use.

| Style | Purpose |
| --- | --- |
| Default | Default is the most commonly used text input style with the label and helper text outside the field. Use when white space is needed between input components or in productive moments where space is at a premium, and smaller components are needed. |
| Fluid | Fluid is an alternate styling for text input used in more expressive moments. Use in fluid forms, contained spaces, or attached to complex components, like a toolbar. Fluid components always sit flush with components around them. |

### Anatomy

- Default
- Fluid

![Anatomy of a text input in the default style](/static/f1873e0003e08b79688ec3f91886b100/3cbba/text-input-usage-anatomy-fixed.png)

![Anatomy of a text input in the fluid style](/static/f100c94bdadb109182c75ea3215e2c78/3cbba/text-input-usage-anatomy-fluid.png)

1. **Label**: Text that informs the user about the content they need to enter in
   the field. It is required unless you get an approved accessibility exemption.
2. **Value**: The content the user has entered into the field.
3. **Field**: The container in which a user enters data. Must meet 3:1 non-text
   contrast requirements.
4. **Helper text** (optional): Assistive text that can provide additional aid or
   context to the user. Often used to explain the correct data format. It is
   positioned below the field in the default style and surfaced through a
   tooltip in the fluid style.

### Sizing

#### Default input heights

There are three text input height sizes: small, medium, and large. Supporting
three sizes gives you more flexibility in structuring layouts. Be sure to use a
consistent field height when pairing form components on the same page.

| Size | Height (px/rem) | Use case |
| --- | --- | --- |
| Small (sm) | 32 / 2 | Use when space is constricted or when placing a text input in a form that is long and complex. |
| Medium (md) | 40 / 2.5 | This is the default size and the most commonly used size. When in doubt, use the medium size. |
| Large (lg) | 48 / 3 | Use when there is a lot of space to work with. The large size is typically used in simple forms or when a text input is placed by itself on a page. |

![Default text input heights](/static/4914792ec452ee8665da92b60161abe2/3cbba/text-input-usage-size.png)

#### Fluid input heights

There is only one fluid input height and it is visually larger than the default
heights. The input is a set height expect for when a warning or error message
has been added to the bottom.

![Fluid text input heights](/static/c052e6f4e332c9ad1575f1bcfdfc2842/3cbba/text-input-usage-size-fluid.png)

## Text area

Use a text area when the expected user input is more than a few words and could
span multiple lines. It is commonly used for features like user commentary or
descriptions. It supports all the same states and functionality as text input
except for the password functionality. Text area has several unique
functionalities not included in the text input, like the resize handle, word
counter and character counter.

| Style | Purpose |
| --- | --- |
| Default | Default is the most commonly used text area style with the label and helper text outside the field. Use when white space is needed between input components or in productive moments where space is at a premium, and smaller components are needed. |
| Fluid | Fluid is an alternate styling for text area used in more expressive moments. Use in fluid forms, contained spaces, or attached to complex components, like a toolbar. Fluid components always sit flush with components around them. |

### Anatomy

- Default
- Fluid

![Anatomy of a text area in the default style](/static/32a4edc50adedd15e5d6b9997d154c0f/3cbba/text-area-usage-anatomy-fixed.png)

![Anatomy of a text area in the fluid style](/static/4713b17f8b16c75a81d1d0a6deaf789b/3cbba/text-area-usage-anatomy-fluid.png)

1. **Label**: Text that informs the user about the content they need to enter in
   the field. It is required unless you get an approved accessibility exemption.
2. **Value**: The content the user has entered into the field.
3. **Field**: The container in which a user enters data. Must meet 3:1 non-text
   contrast requirements.
4. **Resize handle**: Allows a user to manipulate the field height by making it
   longer or shorter.
5. **Optional versus required indicator** (optional): This label indicates if
   the field is optional or required for the user to complete.
6. **Counter** (optional)
   - Character counter: Indicate the number of characters being entered and the
     total number of characters allowed.
   - Word counter: Indicate the number of words being entered and the total
     number of words allowed.

### Sizing

Text area has a variable height that can be lengthened or shortened by the user
using the resize handle in the bottom right of the field. By default, text area
has a minimum height of 40px/2.5rem but no maximum height.

#### Resize handle

Included by default in both default and fluid text area is the resize handle. It
allows a user to manipulate the field height by making it longer or shorter. The
resize handle has no effect on the width of the text area container, it only
effects the height. If the user makes the field size shorter than the content
inside the field then a vertical scroll will become available.

![Example showing the resize handle in text area](/static/1fdf41041c129944be3f56c5c88c8b0a/3cbba/text-area-usage-resize.png)

## Formatting

### Alignment

Input labels should vertically align to the grid and with other type elements on
the page. The alignment of the input container will differ based on the style of
text input you are using. Default inputs are always flush to the columns and
fluid inputs will hang into the gutters.

![Do align field containers to the grid.](/static/397213c8fe1f5ccc6cccbe47761e5fb0/a5df1/text-input-usage-4-do.png)

Align default input containers to the grid so the input label aligns with other type of the page.

![Do hang fluid field containers to the gutter.](/static/ac51d516d81f2129abd005d9099e1b7c/a5df1/text-input-usage-4-do-fluid.png)

Hang fluid input containers into the gutters so the input label aligns with other type of the page.

#### Placement

The field widths of both text input and text area should reflect the intended
length of the content while still aligning to the grid columns or mini unit
grid. Unlike the height, the width of the text area cannot be controlled by the
user. There are no minimum or maximum widths but you should avoid excessively
wide fields that are disproportionate to the intended data being collected.

![Do use proportional widths](/static/535f473bbc31d886cc1f40a257727cc9/a5df1/text-input-width-do.png)

Do make text input widths proportional to the content and align to grid columns.

![Do not make inputs excessively wide.](/static/0aa6ed5a71e71bf605a0941b635c7ee1/a5df1/text-input-width-dont.png)

Do not make text inputs excessively wide just to fill in space.

### Alignment

Labels and field containers should vertically align to the grid and with other
form components on a page.

![Do align field containers to the grid.](/static/397213c8fe1f5ccc6cccbe47761e5fb0/a5df1/text-input-usage-4-do.png)

Do align field containers to the grid.

![Do not align field text to the grid and hang the field in the gutter.](/static/539711e32bc2ca8db8a52975da220d4d/a5df1/text-input-usage-4-dont.png)

Do not align field text to the grid and hang the field in the gutter.

## Content

### Main elements

#### Labels

Effective labeling helps users understand what information to enter into a text
input. Text fields should always have a label. There are rare instances were the
context of an input negates the need for a visible label but we advise you
consult an accessibility expert before proceeding with a label-less design.

- Use sentence-style capitalization for all labels, except for product names and
  proper nouns.
- Keep the label short and concise.
- Do not use colons after label names.

#### Helper text

Optional helper text is pertinent information that assists the user in correctly
completing a field. It is often used to explain the correct data format.

- Use sentence-style capitalization, and in most cases, write the text as full
  sentences with punctuation.
- When used, helper text appears persistently underneath the field, except when
  an error or warning message replaces it.

#### Placeholder text

Optional placeholder text provides hints or examples of what to enter.
Placeholder text disappears after the user begins entering data into the input.
As such, it should not be used as a replacement for a persistent label nor
should it contain crucial information.

- Use sentence-style capitalization, and in most cases, write the text as a
  direct statement without punctuation.
- Placeholder text is not required and by default not shown in text input
  fields.
- Placeholder text can be harmful to user interactions and should only be added
  when necessary.

### Overflow content

#### Overflow in a text input

If a user’s content is unexpectedly too long for the single line of a text input
then the value content can horizontally scroll inside the field container when
moving the cursor from one end of the value to the other.

#### Overflow in a text area

If a user’s content exceeds the vertical space of the variable text area then a
user can either expand the field container using the resize handle or they can
vertically scroll the content inside the set field container.

### Further guidance

For further content guidance, see Carbon’s
[content guidelines](/guidelines/content/overview).

## Universal behaviors

The behaviors listed in this section are universal across all variants. For
behaviors that are unique to each variant, see each of the component variant
sections below.

### States

The text input and text area have multiple interactive states: **enabled**,
**active**, **focus**, **error**, **warning**, **disabled**, **skeleton**, and
**read-only**. For more details on text input and text area interactive states,
see the [style tab](https://carbondesignsystem.com/components/text-input/style).

| State | When to use |
| --- | --- |
| *Enabled* | When a text input or text area is live but a user is not directly interacting with it. This is commonly referred to as the default or normal state of the component. An enabled text input field can contain no content, placeholder text, or user generate content. |
| *Active* | When a user is actively typing content into the field. |
| *Focus* | When a user ```  tabs ```   Copy to clipboard to or clicks on the text input or text area, it becomes focused, indicating the user has successfully navigated to the component. |
| *Error* | When the user input is invalid or a required text input or text area has not been filled in. It can also be triggered due to a system error. This state requires a user response before data can be submitted or saved. |
| *Warning* | When you need to call the user’s attention to an exception condition. The condition might not be an error but can cause problems if not resolved. |
| *Disabled* | When the user cannot interact with a component and all interactive functions have been removed. Unlike read-only states, disabled states are not focusable, are not read by screen readers, and do not need to pass visual contrast, making them inaccessible if they need to be interpreted. |
| *Skeleton* | Use on an initial page load to indicate that the text input or text area has not yet fully loaded. |
| *Read-only* | When the user can review but not modify the component. This state removes all interactive functions like the disabled state but can still be focusable, accessible by screen readers, and passes visual contrast for readability. |

### Validation

Real-time validation helps streamline the process and keep data clean when the
user fills out forms. Otherwise, validate the text input data when the user
submits the associated form. For complete guidance on error and validation, see
the [form pattern](https://carbondesignsystem.com/patterns/forms-pattern/).

#### Invalid

An error state is triggered if the data is invalid or a required field is left
empty. Error states have three visual indicators to signify invalid content: a
red border, an error icon indicator, and an error message.

![Example of an error state being triggered](/fbba7bf70afc3d71bc666b918417d7bf/text-input-usage-2.gif)

![Example of an error state being triggered](/static/851f0b8b51288d7f86a50dfd975a9c3c/3cbba/text-input-usage-invalid.png)

### Required versus optional

Text inputs can be labeled as either optional or required depending on the
depending on the circumstance. For more guidance on requirement labeling, see
the [form pattern](/patterns/forms-pattern/#optional-vs.-mandatory).

![Example showing optional field indicator](/static/572f19e382ca589f7a64fd953f2991fa/a5df1/text-input-usage-optional-do.png)

If the majority of the fields are required, mark only the optional field labels with (optional).

![Example showing required field indicator](/static/4dfcfd1c2fa7580f185c8c0701ffcc33/a5df1/text-input-usage-required-do.png)

If the majority of the fields are optional, mark only the required field labels with (required).

### Interactions

#### Mouse

Users can activate a text input by clicking on the field container. A separate
click is required to activate any additional actions associated with the text
input such as a password visibility toggle.

- Default
- Fluid

![Example showing click target areas for text input in the default style](/static/e16a9a641393454aedf1430b8d70115f/3cbba/text-input-usage-mouse-fixed.png)

![Example showing click target areas for text input in the fluid style](/static/e0a14add0714e232b8522a6ab860ce9d/3cbba/text-input-usage-mouse-fluid.png)

#### Keyboard

For additional keyboard interactions, see the
[accessibility tab](/components/text-input/accessibility).

| Key | Interaction |
| --- | --- |
| *Tab* | Brings focus to the text input. |
| *Enter* or *Space* | Opens any associated actions added to the input, such as a password visibility toggle. |
| *Esc* | Closes any associated actions added to the input. |
| *ctrl* or *opt* + *left/right arrows* | Moves you word by word inside the field. |
| *ctrl* or *opt* + *up/down arrows* | Relocates you to the start or end of the input content. |

## Modifiers

### Password input

Password input is a sub-variant of text input. It is used to collect private
data and will hide the characters as a user enters them. A user can choose to
toggle on the character visibility by clicking the view icon on the far right of
the input field. When using a password input be sure to provide detailed helper
text listing any requirements related to the data format, such as types of
characters allowed or date structure.

![Example of a password input](/static/723806ee59b300663f4b5f0cc0d39db5/3cbba/text-input-usage-password.png)

### Character counter

A character counter can be added to text area to indicate both the number of
characters being entered and the total number of characters allowed. Once the
max number of characters is reached the text area should prevent the user from
entering any additional character and provide messaging to the user that a limit
has been met.

![Example showing a character counter in text area](/static/190a58dbd50c4d45c0a90f9c3a510d74/3cbba/text-area-character-counter.png)

### Word counter

A word counter can be added to text area to indicate both the number of words
being entered and the total number of words allowed. Once the max number of
words is reached the text area should prevent the user from entering any
additional character and provide messaging to the user that a limit has been
met.

![Example showing a word counter in text area](/static/6d45045c2f68c8d796e36d97668808f9/3cbba/text-area-word-counter.png)

## AI presence

Text input and text area have a modification that takes on the AI visual styling
when the AI label is present in the input. The AI variant functions the same as
the normal version except with the addition of the AI label which is both a
visual indicator and the trigger for the explainability popover.

For more information on designing for AI, see the
[Carbon for AI](/guidelines/carbon-for-ai/) guidelines.

- Default
- Fluid

![Default text input and text area AI presence example](/static/d1665edaa143cbede74495086df633ca/3cbba/text-input-text-area-ai-presence-default.png)

![Fluid text input and text area AI presence example](/static/f50f5d756ba7a0a6d0daa483e2fd88a0/3cbba/text-input-text-area-ai-presence-fluid.png)

### Revert to AI

The text input and text area can toggle between the AI variant and the non-AI
variant depending on the user’s interaction. If the user manually overrides the
AI-suggested content then the input will change from the AI variant to the
non-AI variant. Once edited, the user should still be able to switch back to the
initially AI generated content via a revert to AI button.

- Default
- Fluid

![Default text input and text area AI revert example](/static/11c737774e1feda46eb6041388fa6fee/3cbba/text-input-text-area-ai-revert.png)

![Fluid text input and text area AI revert example](/static/64393442bad2c63a0b5bc52d5d121f19/3cbba/text-input-text-area-ai-revert-fluid.png)

## Related

- [Form pattern](/patterns/forms-pattern/)

## Feedback

Help us improve this component by providing feedback, asking questions, and
leaving any other comments on
[GitHub](https://github.com/carbon-design-system/carbon-website/issues/new?assignees=&labels=feedback&template=feedback.md).

[Edit this page on GitHub](https://github.com/carbon-design-system/carbon-website/edit/main/src/pages/components/text-input/usage.mdx)

[Previous

Components: Tag](/components/tag/usage/)

[Next

Text input: Style](/components/text-input/style/)