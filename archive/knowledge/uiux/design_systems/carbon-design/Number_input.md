# Number input

Source: https://carbondesignsystem.com/components/number-input/usage/

---

# Number input

Number input lets users enter a numeric value and incrementally increase or
decrease the value with a two-segment control.

Number input
[with AI label](https://react.carbondesignsystem.com/?path=/story/components-numberinput--with-ai-label)
is now stable. This addition changes the visual appearance of the component and
introduces an AI explainability feature when AI is present in the component. See
the [AI presence](/components/number-input/usage/#ai-presence) section for more
details.

- [Live demo](#live-demo)
- [Overview](#overview)
- [Formatting](#formatting)
- [Content](#content)
- [Behaviors](#behaviors)
- [AI presence](#ai-presence)
- [Related](#related)
- [References](#references)
- [Feedback](#feedback)

## Live demo

Theme selector

White

---

Variant selector

Default

---

This live demo contains only a preview of functionality and styles available for this component. View the [full demo](https://react.carbondesignsystem.com/?path=/story/components-numberinput--default&globals=theme:white) on Storybook for additional information such as its version, controls, and API documentation.

### Accessibility testing status For every latest release, Carbon runs tests on all components to meet the [accessibility requirements](https://www.ibm.com/able/requirements/requirements/). These different statuses report the work that Carbon has done in the back end. These tests appear only when the components are stable.

Variant

Number input

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

Not tested](//accessibility/#accessibility-testing-status)

[##### Advanced states

Not tested](//accessibility/#accessibility-testing-status)

[##### Screen reader

Not available](//accessibility/#accessibility-testing-status)

[##### Keyboard navigation

Not available](//accessibility/#accessibility-testing-status)

## Overview

Number inputs are similar to text inputs, but are used to specify only a numeric
value. Number inputs incrementally increase or decrease the value with a
two-segment control. Number input reduces input efforts for adjusting small
values.

![number input image](/static/1f2d02b94281fb0548decc69860c796c/3cbba/number-input-usage-1.png)

### When to use

- The user needs to input a numeric value
- Adjusting small values when increasing or decreasing them requires only a few
  clicks
- When users may not know exact values and only want to change the values that
  are relative to its current state

### When not to use

- It is best practice not to use number input if large value changes are
  expected. For example, when the value sets from 1 to 30, number input is not a
  great option because it requires many clicks to reach 30. In this case, use
  [slider](https://carbondesignsystem.com/components/slider/usage/) when numeric
  values are large or when there is a wide range of numeric options.
- It is also best to avoid number input for continuous variables such as prices,
  distances, lengths, or human heights. When the exact value is important to
  specify within a wide range, use
  [text input](https://carbondesignsystem.com/components/text-input/usage/)
  instead.

## Formatting

### Anatomy

- Default
- Fluid

![Anatomy of a default number input](/static/4073555e2416c6d3b2487d228de9260f/3cbba/number-input-usage-2.png)

![Anatomy of a fluid number input](/static/a5d529f0e4e4b777227c2c731bfb20fa/3cbba/number-input-usage-2-fluid.png)

1. **Label**: Text that informs the user about the content they need to enter in
   the field. It is required unless you get an approved accessibility exemption.
2. **Numeric value**: The value changes when user enters a value into the field
   or uses the subtract or add controls.
3. **Helper text**: Assistive text that can provide additional aid or context to
   the user. Often used to explain the correct data format.
4. **Field**: The container in which a user enters data.
5. **Subtract icon**: This icon triggers decremental values.
6. **Add icon**: This icon triggers incremental values.
7. **Status icon**: Indicates the state of the number input, either error or
   warning.
8. **Error or Warning text**: It replaces the helper text when an error or
   warning state appears.

### Styling

There are two styles of number inputs, default and fluid. They share the same
functionality but look visually different, influencing where to use them.

| Style | Appearance | Use case |
| --- | --- | --- |
| Default | A traditional style where the label is positioned outside and above the input field. | Use when white space is needed between input components or in productive moments where space is at a premium, and smaller components are needed. |
| Fluid | An alternative style where the label is placed inside of the input field and is stacked inline with the user input text. | Use in expressive moments, fluid forms, contained spaces, or attached to complex components, like a toolbar. |

![An example of a default and fluid number input](/static/7211058e77f0c6313fa27d7569341c8b/3cbba/number-input-usage-11.png)

A default style input is shown on the left and fluid style is on the right.

### Sizing

#### Default input heights

Number input has three sizes default input heights: **small**, **medium**, and
**large**. The width varies in size based on content, layout, and design.

| Size | Height (px/rem) | Use case |
| --- | --- | --- |
| Small (sm) | 32 / 2 | Use when space is constricted or when placing a number input in a form that is long and complex. |
| Medium (md) | 40 / 2.5 | This is the default size and the most commonly used size. When in doubt, use the medium size. |
| Large (lg) | 48 / 3 | Use when there is a lot of space to work with. The large size is typically used in simple forms or when a number input is placed by itself on a page. |

![Default number input sizes](/static/5c67259d63351f89cde613f24944bab1/3cbba/number-input-usage-3.png)

#### Fluid input heights

There is only one fluid input height and it is visually larger than the default
heights. The input is a set height of 64px except when a warning or error
message has been added to the bottom.

![Fluid input size example](/static/33a63d73cf372412db3315f7dca0399a/3cbba/number-input-usage-3-fluid.png)

## Content

### Main elements

#### Label

- Always include a label so that users know how to complete the field
- Keep the label short and concise
- Use sentence-style capitalization for the label

![Do include a label](/static/bed62427f71e19b5e3923a3ce27ed91d/3cbba/number-input-usage-4.png)

Do include a label

![Do not hide label](/static/22c4212d010f3cd26bf8c6b67a3c06c7/3cbba/number-input-usage-5.png)

Do not hide a label that helps user understand the context of number input

#### Helper text

- Indicates the input value if it has a maximum or minimum
- Helper text is optional but if present will be replaced by warning and error
  messages when needed

#### Overflow content

Label, numeric value, and helper text should be short and not exceed two lines.

## Behaviors

### States

The number input has a series of states for both field and controls elements:
**enabled**, **hover**, **focus**, **error**, **warning**, **disabled**, and
**read-only**.

| State | When to use |
| --- | --- |
| *Enabled* | When the number input is live but a user is not directly interacting with it. This is commonly referred to as the default or normal state of the component. An enabled number input field should contain a default value. |
| *Hover* | When a user’s mouse cursor is hovering over the field or the button controls. |
| *Focus* | When a user tabs to or clicks on the number input, the field or controls become focused, indicating the user has successfully navigated to the component. |
| *Error* | When the required number input has not been filled in. It can also be triggered due to a system error. This state requires a user response before data can be submitted or saved. |
| *Warning* | When you need to call the user  ’s attention to an exception condition. The condition might not be an error but can cause problems if not resolved. |
| *Disabled* | When the user cannot interact with a component and all interactive functions have been removed. Unlike read-only states, disabled states are not focusable, are not read by screen readers, and do not need to pass visual contrast, making them inaccessible if they need to be interpreted. |
| *Skeleton* | Use on an initial page load to indicate that the number input has not yet fully loaded. |
| *Read-only* | When the user can review but not modify the component. This state removes all interactive functions like the disabled state but can still be focusable, accessible by screen readers, and passes visual contrast for readability. |

- Default
- Fluid

![Default number input interactive states](/static/f4a85b21cb033158ceca4dae1062f530/3cbba/number-input-usage-6.png)

![Fluid number input interactive states](/static/e65d637064490ac82ae5b67d4c9fc02c/3cbba/number-input-usage-6-fluid.png)

### Interactions

#### Mouse

Users can click on the input field and change the value by typing inside the
input field. Users can also increase or decrease the values by pressing on the
add or subtract icon controls.

- Default
- Fluid

![Default number input mouse and keyboard interactions](/static/a0fc7cb708b7152d8785283b5b4c03be/3cbba/number-input-usage-7.png)

![Fluid number input mouse and keyboard interactions](/static/560400477ce7f7c39c7f3e0f4e6b7caa/3cbba/number-input-usage-7-fluid.png)

#### Keyboard

Users can navigate to the number input field by pressing

```
Tab
```

Copy to clipboard

. Users can then
increase the value by pressing

```
Up arrow
```

Copy to clipboard

or decrease the value by pressing

```
Down arrow
```

Copy to clipboard

.

### Validation

#### Invalid

An error state is triggered if the data is invalid or a required field is left
empty. Error states have three visual indicators to signify invalid content: a
red border, an error icon indicator, and an error message.

![number input validation](/static/02dae1db6afb251d649116d8943de113/3cbba/number-input-usage-8.png)

### Default values

Numeric input should always have a default. The default will usually be ‘1’.
Sometimes, you will have input value defaulted to ‘0’. For example, when booking
a hotel room, it may set the default number of adults as ‘1’ and the default
number of children as ‘0’.

![Do set default for input value](/static/87bac3b07c692b30558698e69656c20a/a5df1/number-input-usage-9.png)

Do set a clear default that most users are likely to select

![Do not leave value input blank](/static/0efe86b66236dce435e35946539ab492/3cbba/number-input-usage-10.png)

Do not leave value input blank

## AI presence

Number input has a modification that takes on the AI visual styling when the AI
label is present in the input. The AI variant of number input functions the same
as the normal version except with the addition of the AI label which is both a
visual indicator and the trigger for the explainability popover.

For more information on designing for AI, see the
[Carbon for AI](/guidelines/carbon-for-ai/) guidelines.

- Default
- Fluid

![Default number input AI presence example](/static/d71f489cd490b6aaecbb3b2111c5a6b8/3cbba/number-input-style-ai-default.png)

![Fluid number input AI presence example](/static/9b4e4685c55b17347c66f76e882ce4af/3cbba/number-input-style-ai-fluid.png)

### Revert to AI

A number input can toggle between the AI variant and the non-AI variant
depending on the user’s interaction. If the user manually overrides the
AI-suggested content then the input will change from the AI variant to the
non-AI variant. Once edited, the user should still be able to switch back to the
initially AI generated content via a revert to AI button.

- Default
- Fluid

![Default number input AI revert example](/static/1075160ad93bbaf28edc636d33ff5da9/3cbba/number-input-usage-13.png)

![Fluid number input AI revert example](/static/6fba933841bb7f3cf9432b06c5becb48/3cbba/number-input-usage-15.png)

## Related

- Use [slider](https://carbondesignsystem.com/components/slider/usage/) when
  numeric values are large or when there is a wide range of numeric options.
- When the exact value is important to specify within a wide range, use
  [text input](https://carbondesignsystem.com/components/text-input/usage/)
  instead.

## References

Yuxuan (Tammy) Zhou,
[Design Guidelines for Input Steppers](https://www.nngroup.com/articles/input-steppers/)
(Nielsen Norman Group, 2018)

## Feedback

Help us improve this component by providing feedback, asking questions, and
leaving any other comments on
[GitHub](https://github.com/carbon-design-system/carbon-website/issues/new?assignees=&labels=feedback&template=feedback.md).

[Edit this page on GitHub](https://github.com/carbon-design-system/carbon-website/edit/main/src/pages/components/number-input/usage.mdx)

[Previous

Components: Notification](/components/notification/usage/)

[Next

Number input: Style](/components/number-input/style/)