# Slider

Source: https://carbondesignsystem.com/components/slider/usage/

---

# Slider

Sliders provide a visual indication of adjustable content, where the user can
increase or decrease the value by moving the handle along a horizontal track.

- [Live demo](#live-demo)
- [Overview](#overview)
- [Formatting](#formatting)
- [Content](#content)
- [Behaviors](#behaviors)
- [Default slider](#default-slider)
- [Range slider](#range-slider)
- [Modifiers](#modifiers)
- [Feedback](#feedback)

## Live demo

Theme selector

White

---

Variant selector

Default

---

This live demo contains only a preview of functionality and styles available for this component. View the [full demo](https://react.carbondesignsystem.com/?path=/story/components-slider--default&globals=theme:white) on Storybook for additional information such as its version, controls, and API documentation.

### Accessibility testing status For every latest release, Carbon runs tests on all components to meet the [accessibility requirements](https://www.ibm.com/able/requirements/requirements/). These different statuses report the work that Carbon has done in the back end. These tests appear only when the components are stable.

[##### Default state

Tested](//accessibility/#accessibility-testing-status)

[##### Advanced states

Tested](//accessibility/#accessibility-testing-status)

[##### Screen reader

Manually tested](//accessibility/#accessibility-testing-status)

[##### Keyboard navigation

Not available](//accessibility/#accessibility-testing-status)

## Overview

A slider allows a user to select a single value or range of values available
within the slider track. The slider comes in two different variants: default and
range. The default slider is accompanied by a label and a number input that
doubles as a display for the slider’s current selected value. The range slider
has a label and two number inputs to display the slider’s selected range of
values.

### When to use

- Use when selecting a single value or range of number values.
- Use sliders when there is a need to show a selection of a single value or
  range of values.
- Use when needing to expose a variety of options or to limit the number of
  options quickly.

### When not to use

- Do not use for extremely large ranges, for example, 1-1000.
- Do not use ranges that are too small, for example, 1-3.
- Do not use complex inputted values that are not numbers.

### Variants

| Variant | Purpose |
| --- | --- |
| [Default slider](/components/default-slider/usage/#default-slider) | Default sliders allow users to select a single value within the slider track. |
| [Range slider](/components/range-slider/usage/#range-slider) | Range sliders allow users to define minimum and maximum values from a predefined range within the slider track. |

## Formatting

### Default slider anatomy

![Anatomy of a default slider.](/static/ef012b6b6c1167a676fc44cf9491edab/3cbba/anatomy-default-slider.png)

1. **Label:** Text describing what kind of value will be selected from the
   slider.
2. **Min value:** The minimum value that can be selected in the slider range.
3. **Max value:** The maximum value that can be selected in the slider range.
4. **Number input:** An input to specify a selected value within the slider
   range.
5. **Handle:** An indicator that can be moved on the track within the slider
   range to specify a selected value.
6. **Track:** Shows a user’s available minimum and maximum values on the range
   to select from.

### Range slider anatomy

![Anatomy of a range slider.](/static/6fb6facc9acb20528298185d5325e25b/3cbba/anatomy-range-slider.png)

1. **Label:** Text describing what kind of value will be selected from the
   slider.
2. **Min value number input:** An input to specify a selected minimum value
   within the slider range.
3. **Max value number input:** An input to specify a selected maximum value
   within the slider range.
4. **Min value:** The minimum value that can be selected in the slider range.
5. **Max value:** The maximum value that can be selected in the slider range.
6. **Handles:** Two indicators that can be moved on the track within the slider
   range to specify selected minimum and maximum values.
7. **Track:** Shows a user’s available minimum and maximum values on the range
   to select from.

## Content

### Main elements

#### Labels

- Labels inform users what kind of value(s) they are selecting in the slider.
- Keep the label short and concise by limiting it to a single line of text.
- Labels should be placed above the slider so the label does not become obscured
  when interacting with the handle.

#### Min and max values

- Min and max value text indicate a slider’s minimum and maximum value range.
- Keep min and max value text should accurately reflect the user’s selection
  using the handles or the number input.

![Do label the slider appropriately with the value being modified.](/static/72d7ac38556dfb4d86108ae7c5db09f2/3cbba/content-range-slider-do.png)

Do label the slider appropriately with the value being modified

![Do not use in ranges that result in non-discrete large increments.](/static/fb741c49b37fe1281599037376cbc419/3cbba/content-range-slider-dont.png)

Do not use in ranges that result in non-discrete large increments

## Behaviors

### States

The default and range sliders have the following states: **enabled**, **hover**,
**focus**, **active**, **error**, **warning**, **disabled**, **read-only**, and
**skeleton**. For more information on states, visit the
[interactive state](https://carbondesignsystem.com/components/slider/style#interactive-states)
guidance on the style tab.

| State | When to use |
| --- | --- |
| *Enabled* | When the slider is live, and a user is not directly interacting with it. The enabled state is commonly referred to as the default or normal state of the component. |
| *Hover* | When a user’s mouse cursor is hovering over the fields or handles of the slider component. Use a tooltip on hover if the slider does not have number inputs to show the selected values |
| *Focus* | When a user tabs to or clicks on a field or handle, it becomes focused, indicating the user has successfully navigated to the component. Use a tooltip on focus if the slider does not have number inputs to show the selected values. |
| *Active* | When a user is pressing down on the handles of the slider component and interacting with it. Use a tooltip on active if the slider does not have number inputs to show the selected values. |
| *Error* | When a slider component marked as “required” has not had an option selected, if the selected values are out of range, or if the values are not numbers . It can also be triggered due to a system error. This state requires a user response before data can be submitted or saved. |
| *Warning* | When you need to call the user’s attention to an exception condition. The condition might not be an error but can cause problems if not resolved. |
| *Disabled* | When the user cannot interact with a component and all interactive functions have been removed. Unlike read-only states, disabled states are not focusable, are not read by screen readers, and do not need to pass visual contrast, making them inaccessible if they need to be interpreted. |
| *Read-only* | When the user can review but not modify the component. This state removes all interactive functions like the disabled state but can still be focusable, accessible by screen readers, and passes visual contrast for readability. |

## Interactions

### Mouse

Users can trigger a value change by clicking anywhere on the horizontal track.
Users can also drag the slider handle. Either method repositions the slider and
automatically updates the value in the number input for the single slider. The
closest value (minimum or maximum value) will be updated depending on where the
user clicks on the range slider. Either method repositions the slider and
automatically updates the value in the number input.

### Keyboard (default slider)

Users can enter an exact numeric value into the number input field or use the

```
up
```

Copy to clipboard

,

```
down
```

Copy to clipboard

,

```
left
```

Copy to clipboard

, or

```
right
```

Copy to clipboard

arrow keys to change the value. Either method
adjusts the slider handle to the corresponding position.

Users can also increment the value by using the arrow keys when the slider
receives focus. The arrow keys, in combination with the

```
shift
```

Copy to clipboard

key can alter
the slider by the value of the

```
stepMultiplier
```

Copy to clipboard

.

### Keyboard (range slider)

Once focus is established on the range slider, the user can define a numerical
range by:

- Entering the exact value into the text field.
- Moving the slider handle with their mouse, which automatically updates the
  value in the number input.
- Using the

  ```
  up
  ```

  Copy to clipboard

  ,

  ```
  down
  ```

  Copy to clipboard

  ,

  ```
  left
  ```

  Copy to clipboard

  , or

  ```
  right
  ```

  Copy to clipboard

  arrow keys automatically updates
  the value in the number input and moves the slider handle to the corresponding
  value.
- The step size increment is how many increments the inputted value and slider
  handle will jump when using the arrow keys. Make sure to set the step size
  increments to reasonable values.
- ```
  Up
  ```

  Copy to clipboard

  ,

  ```
  down
  ```

  Copy to clipboard

  ,

  ```
  left
  ```

  Copy to clipboard

  , or

  ```
  right
  ```

  Copy to clipboard

  arrow keys change the value by one step size
  increment. Example: Pressing the

  ```
  right
  ```

  Copy to clipboard

  arrow key changes the inputted value
  from 59 to 60, increasing the value by 1 unit.
- ```
  Shift +
  ```

  Copy to clipboard

  ```
  up
  ```

  Copy to clipboard

  ,

  ```
  down
  ```

  Copy to clipboard

  ,

  ```
  left
  ```

  Copy to clipboard

  , or

  ```
  right
  ```

  Copy to clipboard

  arrow keys changes the value by 10
  step size increments. Example: Typing

  ```
  shift +
  ```

  Copy to clipboard

  and

  ```
  right
  ```

  Copy to clipboard

  arrow key changes
  the value from 60 to 70, increasing the inputted value by 10 units.
- ```
  Home
  ```

  Copy to clipboard

  : When focus is on an selectors, moves focus to the first range selector
  header.
- ```
  End
  ```

  Copy to clipboard

  : When focus is on an selectors, moves focus to the last range selector
  header.

## Default slider

The default slider, in its most basic form, is accompanied by a label, a number
input, and a slider track with a handle. Users can use the handle or the number
input to select a value from within the slider track. When needing to select a
range within the slider track, use the range slider instead.

![Example of a default slider in context](/static/c13f67789743205ee35068e04e5f291b/3cbba/default-slider-ui.png)

Example of a default slider in context

## Range slider

The range slider allows users to select a range of values from the slider track.
The range slider consists of a label and two number inputs to type in values,
which will determine the minimum and maximum range within the slider track. A
user can manually input minimum and maximum values by clicking on the number
input or moving the slider’s handles.

![Example of a range slider in context](/static/96eebd5ae8b3223b6a90be54a29d9260/3cbba/range-slider-ui.png)

Example of a range slider in context

It is best practice to describe the range value in numbers and to not use a
slider as a date selector. To select dates, use the
[date picker](https://carbondesignsystem.com/components/date-picker/usage/)
component.

![Do describe the range in numbers.](/static/efdf5fd15b06e5c9181184f253900bf6/3cbba/variant-range-slider-do.png)

Do describe the range in numbers

![Do not use as a date selector.](/static/a306770bb7313061fd6e40728db33318/3cbba/variant-range-slider-dont.png)

Do not use as a date selector

## Modifiers

#### Sliders without a number input

If the slider does not include number inputs to display the selected values, use
a tooltip on hover, focus, and active to show the selected values.

![Using a tooltip to show the selected values when there are no number inputs](/static/1abd76a372a554f34531e0326802e4df/3cbba/slider-modifier-tooltip.png)

Using a tooltip to show the selected values when there are no number inputs

#### Sliders with custom value

For sliders with custom value, show a tooltip on hover, focus, and active to
display the selected value. These labels can vary by use case, the tooltip
should help users understand their selection without needing a separate input.

For example, between values of low and high, the tooltip should display low when
the handle is near the start of the range, medium when it’s around the middle,
and high when it approaches the end.

![Using a tooltip to show the selected values with custom value](/static/79f7da1da212cf3132b1db383e18feeb/3cbba/slider-modifier-2-tooltip.png)

Example shows custom values as low, medium, and high by using a tooltip to
show the selected values

## Feedback

Help us improve this component by providing feedback, asking questions, and
leaving any other comments on
[GitHub](https://github.com/carbon-design-system/carbon-website/issues/new?assignees=&labels=feedback&template=feedback.md).

[Edit this page on GitHub](https://github.com/carbon-design-system/carbon-website/edit/main/src/pages/components/slider/usage.mdx)

[Previous

Components: Select](/components/select/usage/)

[Next

Slider: Style](/components/slider/style/)