# Toggle

Source: https://carbondesignsystem.com/components/toggle/usage/

---

# Toggle

Feature flag

A toggle is used to quickly switch between two possible states. They are
commonly used for “on/off” switches.

- [Live demo](#live-demo)
- [Overview](#overview)
- [Formatting](#formatting)
- [Content](#content)
- [Behaviors](#behaviors)
- [Default toggle](#default-toggle)
- [Small toggle](#small-toggle)
- [Related](#related)
- [Feedback](#feedback)

## Live demo

Theme selector

White

---

Variant selector

Default toggle

---

This live demo contains only a preview of functionality and styles available for this component. View the [full demo](https://react.carbondesignsystem.com/?path=/story/components-toggle--default&globals=theme:white) on Storybook for additional information such as its version, controls, and API documentation.

### Accessibility testing status For every latest release, Carbon runs tests on all components to meet the [accessibility requirements](https://www.ibm.com/able/requirements/requirements/). These different statuses report the work that Carbon has done in the back end. These tests appear only when the components are stable.

[##### Default state

Tested](//accessibility/#accessibility-testing-status)

[##### Advanced states

Tested](//accessibility/#accessibility-testing-status)

[##### Screen reader

Manually tested](//accessibility/#accessibility-testing-status)

[##### Keyboard navigation

Tested](//accessibility/#accessibility-testing-status)

## Overview

Toggle is a control that is used to quickly switch between two possible states.
Toggles are only used for these binary actions that occur immediately after the
user “flips the switch”. They are commonly used for “on/off” switches.

![Example of the toggle component in a UI](/static/355cd8d24e1ec305e68a8c11e9802681/3cbba/toggle_usage_overview.png)

Example of the toggle component in a UI

### When to use

- To turn off and on a single option that affects the system or page settings.
- Ideal for settings or preferences that can be immediately applied.
- Recommended for actions where the change is reversible without additional
  confirmation.

### When not to use

- Avoid using toggles if the action requires immediate feedback or confirmation,
  such as deleting a file.
- Don’t use toggles for more than two options; instead, use a
  [dropdown](/components/dropdown/usage/),
  [radio button](/components/radio-button/usage/), or
  [checkbox](/components/checkbox/usage/).
- Avoid using toggles for settings that aren’t binary in nature or don’t provide
  instant application; instead use a different UI component, like a checkbox, in
  combination with a [button](/components/button/usage/).

### Variants

| Variant | Purpose |
| --- | --- |
| [Default toggle](#default-toggle) | Use the default toggle when you need to specify a label text in addition to the toggle state text. Default toggles appear in forms or within full pages of information. |
| [Small toggle](#small-toggle) | Use the small toggle when you do not need to specify label or state text. Small toggles are more compact in size and are used inline with other components. |

### Feature flags

A [feature flag](/components/overview/feature-flags/) has been added to the
toggle to adjust its label spacing and changes its visual appearance, not its
functionality. For code-specific feature flag information, refer to the
[Code](/components/toggle/code/) tab. The current toggle is not being
deprecated, but teams are encouraged to use the feature flag toggle for their
products moving forward. Once the next major release (v12) is released in the
future, this feature flag will become the default version of the component.

The following is the feature flag change made to the toggle.

- The spacing between the toggles label and its container is now 8px instead of
  16px to improve consistency across our label spacing in other components.
- This change applies to both the default and small toggles.

- Flag enabled
- Flag disabled

![Toggle with feature flag enabled](/static/3067e3e2b1ebab86b6e7c1369e4e5d84/3cbba/toggle-usage-feature-flag-enabled.png)

![Toggle with feature flag disabled](/static/c2dc3d77cf10c2abaa1c07e76ee33124/3cbba/toggle-usage-feature-flag-disabled.png)

## Formatting

### Anatomy

Default and small toggles are both comprised of a label text, a toggle button,
and a state text. Default toggles are required to display a component label and
state text, unlike the small toggle, where both these elements are optional. The
small toggle displays a checkmark tick in the “on” state to ensure the toggle is
still accessible when label and state text are unavailable.

![Anatomy of default and small toggle variants](/static/20cc6cc2c93aa843e54d6cbb67fdd1bd/3cbba/toggle-usage-anatomy.png)

Anatomy of default and small toggle

#### 1. Default toggle

A. Label text   
 B. Toggle   
 C. State text

#### 2. Small toggle

A. Label text (optional)   
 B. Toggle   
 C. State text (optional)   
D. Checkmark tick (on state)

### Sizing

The toggle component is available in two sizes: **default** and **small**.

![Sizes of toggle](/static/1249a7dba6af2f085564ed80f18c0648/3cbba/toggle-usage-sizes.png)

Sizes of toggle

## Content

#### Label text

The label text must accompany the toggle to provide additional context and
clarify its state. However, the label text is optional for small toggle.

#### State text

Use the state text to describe the binary action of toggle so that the action is
clear. It must be three words or less and is displayed on the side of a toggle.
The state text is optional for small toggle.

#### Language

Use adjectives rather than verbs to describe actions and the state of the object
affected.

### Further guidance

For further content guidance, see Carbon’s
[content guidelines](https://carbondesignsystem.com/guidelines/content/overview/).

## Behaviors

### States

The default and small toggle have two main states: **on** and **off**. Other
interactive states are **focus**, **disabled**, **read-only**, and **skeleton**.
For more information on toggle states, see the
[Style](/components/toggle/style/) tab.

| State | When to use |
| --- | --- |
| On | When a user clicks or uses the arrow keys to switch on the component. |
| Off | When a user clicks or uses the arrow keys to switch off the component. |
| Focus | When a user presses tab or clicks on the toggle, it becomes focused, indicating the user has successfully navigated to the component. |
| Disabled | When a user is not allowed to interact with the toggle due to either permissions, dependencies, or pre-requisites. The disabled state completely removes the interactive function from a component. The styling is not subject to WCAG contrast compliance. |
| Read-only | When the user can review but not modify the component. This state removes all interactive functions like the disabled state but can still be focusable, accessible by screen readers, and passes visual contrast for readability. |
| Skeleton | Use on an initial page load to indicate that the toggle has not yet fully loaded. |

### Interactions

#### Mouse

Toggle component is triggered on

```
Click
```

Copy to clipboard

which switches between the “on” and
“off” states. It also has a visible focus state when selected, ensuring
accessibility.

#### Keyboard

For keyboard navigation, users can focus the toggle using the

```
Tab
```

Copy to clipboard

key,
providing visual feedback for keyboard users. Pressing

```
Enter
```

Copy to clipboard

or

```
Space
```

Copy to clipboard

changes the toggle’s state between “on” and “off”.

### Clickable areas

The toggle component has two clickable areas: the toggle switch itself and the
label associated with it. Users can click either area to change the toggle’s
state.

![Clickable areas of default and small toggle](/static/600d68e77db8c0ffc59af5d52fc880a5/3cbba/toggle-usage-clickable-areas.png)

Clickable areas of default and small toggle

## Default toggle

The default toggle is larger in size than the small toggle. They are commonly
used in forms and can appear within full pages of information that are not
restricted in space. Default toggles are required to display a visible label and
a state text.

Default toggle has an available
[feature flag](/components/overview/feature-flags/).

- Flag enabled
- Flag disabled

![Default toggle with feature flag enabled](/static/25cf26351b6bcd8bd8838f63a41908f6/3cbba/toggle-usage-default-flag-enabled.png)

![Default toggle with feature flag disabled](/static/6d97d4e8cd976027e59d9396b00ab5ac/3cbba/toggle-usage-default-flag-disabled.png)

## Small toggle

The small toggle is often used in condensed spaces and appear inline with other
components or content. The label and state text are optional for the small
toggle.

Small toggle has an available
[feature flag](/components/overview/feature-flags/).

- Flag enabled
- Flag disabled

![Small toggle with feature flag enabled](/static/d66145a2f9dd19fe7977ff4e457b3ad9/3cbba/toggle-usage-small-flag-enabled.png)

![Small toggle with feature flag disabled](/static/a41b9ad1e74c6191df79be23b6d4625d/3cbba/toggle-usage-small-flag-disabled.png)

Unlike the default toggle, the small toggle is more compact in size and displays
a checkmark tick in the on state to ensure the toggle is still accessible
without requiring visible label or state text. For example, inside
[data table](/components/data-table/usage) rows.

![Example of a small toggle in context without a visible label or state text](/static/5f21fc2b16dc28ca84478ac5f6afec14/3cbba/toggle-usage-small.png)

Example of a small toggle in context without a visible label or state text

## Related

- [Button](/components/button/usage/)
- [Checkbox](/components/checkbox/usage/)
- [Data table](/components/data-table/usage/)
- [Dropdown](/components/dropdown/usage/)
- [Radio button](/components/radio-button/usage/)

## Feedback

Help us improve this component by providing feedback, asking questions, and
leaving any other comments on
[GitHub](https://github.com/carbon-design-system/carbon-website/issues/new?assignees=&labels=feedback&template=feedback.md).

[Edit this page on GitHub](https://github.com/carbon-design-system/carbon-website/edit/main/src/pages/components/toggle/usage.mdx)

[Previous

Components: Tile](/components/tile/usage/)

[Next

Toggle: Style](/components/toggle/style/)