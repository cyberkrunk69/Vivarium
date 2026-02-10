# Button

Source: https://carbondesignsystem.com/components/button/usage/

---

# Button

Buttons are used to initialize an action. Button labels express what action will
occur when the user interacts with it.

**Note:** Some of the examples we discuss here include fluid (full-span) and
hanging buttons which are not available for production use. This guidance
reflects our current understanding of these topics and we are working towards
releasing this work in a future version of Carbon.

- [Live demo](#live-demo)
- [Overview](#overview)
- [Formatting](#formatting)
- [Content](#content)
- [Universal behaviors](#universal-behaviors)
- [Primary button](#primary-button)
- [Secondary button](#secondary-button)
- [Tertiary button](#tertiary-button)
- [Ghost button](#ghost-button)
- [Danger button](#danger-button)
- [Modifiers](#modifiers)
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

This live demo contains only a preview of functionality and styles available for this component. View the [full demo](https://react.carbondesignsystem.com/?path=/story/components-button--default&globals=theme:white) on Storybook for additional information such as its version, controls, and API documentation.

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

Buttons are clickable elements that are used to trigger actions. They
communicate calls to action to the user and allow users to interact with pages
in a variety of ways. Button labels express what action will occur when the user
interacts with it.

#### When to use

Use buttons to communicate actions users can take and to allow users to interact
with the page. Each page should have only one primary button. Any remaining
calls to action should be represented as lower emphasis buttons.

#### When not to use

Do not use buttons as navigational elements. Instead, use
[links](https://www.carbondesignsystem.com/components/link/usage) when the
desired action is to take the user to a new page.

### Variants

Each button variant has a particular function and its design signals that
function to the user. It is, therefore, very important that the different
variants are implemented consistently across products to convey the correct
actions.

| Variant | Purpose |
| --- | --- |
| [Primary](#primary-button) | For the principal call to action on the page. Primary buttons should only appear once per screen (not including the application header, modal dialog, or side panel). |
| [Secondary](#secondary-button) | For secondary actions on each page. Secondary buttons can only be used in conjunction with a primary button. As part of a pair, the secondary button’s function is to perform the negative action of the set, such as “Cancel” or “Back”. Do not use a secondary button in isolation and do not use a secondary button for a positive action. |
| [Tertiary](#tertiary-button) | For less prominent, and sometimes independent, actions. Tertiary buttons can be used in isolation or paired with a primary button when there are multiple calls to action. Tertiary buttons can also be used for sub-tasks on a page where a primary button for the main and final action is present. |
| [Ghost](#ghost-button) | For the least pronounced actions; often used in conjunction with a primary button. In a situation such as a progress flow, a ghost button may be paired with a primary and secondary button set, where the primary button is for forward action, the secondary button is for “Back”, and the ghost button is for “Cancel”. |
| [Danger](#danger-button) | For actions that could have destructive effects on the user’s data (for example, delete or remove). Danger button has three styles: primary, tertiary, and ghost. |

## Formatting

### Anatomy

A button’s label communicates the action that is performed when the user
interacts with it. In an icon only button, that has no label, the icon must
accurately represent what the button does.

In a Carbon button, the label is always left-aligned, not center-aligned. The
icons in a button with a label is right-aligned but in an icon only button, the
icon is centered.

![Button anatomy](/static/1b27abfd7556144883e3c671402c95eb/3cbba/button_usage_2.png)

Anatomy of buttons

#### 1. Button

A. Label   
 B. Container   
 C. Icon (optional)

#### 3. Ghost button

A. Label   
 C. Icon (optional)

#### 2. Tertiary button

A. Label   
 B. Container   
 C. Icon (optional)

#### 4. Icon button

B. Container   
 C. Icon

### Button sizes

The button is available in seven different sizes: **extra small**, **small**,
**medium**, **large (productive)**, **large (expressive)**, **extra large**, and
**2XL**. The table below adds more context around the use case for each size.
For guidance on button heights, see [Size](/components/button/style/#size) on
the Style tab.

We do not recommend mixing different button sizes in #button-groups.

| Button size | Use case |
| --- | --- |
| Extra small | Use when vertical space is limited or in areas with a confined layout. |
| Small | Use when buttons are paired with 32px small sized input fields. |
| Medium | Use when buttons are paired with 40px medium sized input fields. |
| Large (productive) | This is the most common button size in software products. Pairs with 14px body copy. |
| Large (expressive) | The larger expressive type size within this button provides balance when paired with 16px body copy. Used by the IBM.com team in website banners. |
| Extra large | Use when buttons bleed to the edge of a larger component, like in the context of modals, side panel and narrow tearsheets. |
| 2XL | Use when buttons bleed to the edge of a full-screen component, like in the context of large tearsheets. |

![Button sizes](/static/66187b8b313bafed629f67032e87ccb6/3cbba/button_usage_3.png)

Sizes of buttons in relation to its usage.

### Emphasis

You don’t necessarily need to use the buttons in the order that their labels
imply. Although secondary buttons have less visual prominence because they are
less saturated than their primary counterparts, they are still tonally heavy. If
your layout requires multiple actions—as is the case with some toolbars, data
lists and dashboards—low emphasis buttons (tertiary or ghost) may be a better
choice.

The most important thing is to establish a visual hierarchy between the buttons
in your UI. Keep these best practices in mind.

#### A single, high-emphasis button

As a general rule, a layout should contain a single high-emphasis button that
makes it clear that other buttons have less importance in the hierarchy. This
high-emphasis button commands the most attention.

#### Multiple button emphasis

A high-emphasis button can be accompanied by medium- and low-emphasis buttons
that perform less important actions. Keep in mind that you should only group
together calls to action that have a relationship to one another.

![Do use high-emphasis and medium-emphasis buttons in a button group.](/static/d7252bafc6f3f6d6ef95e368993a31a5/a5df1/button_usage_8.png)

Do use high-emphasis and medium-emphasis buttons in a button group.

![Do not use two high-emphasis buttons in a button group.](/static/fded80d07f1616a2dbd5dd896be70f7b/a5df1/button_usage_9.png)

Do not use two high-emphasis buttons in a button group.

### Alignment

Alignment refers to whether the buttons are aligned to the right or the left of
a window, container, or layout. Buttons are unique, more so than any other
component, in that their alignment depends on where they appear and whether or
not they’re contained within another component.

As a general rule, on full-page designs, the primary button is on the left side
of the page. When the browser window is large and the user is scrolling to read,
it’s best to have the primary button where the user’s attention has been focused
all along. Whereas in wizards, where a user is progressing through a series of
steps or dialog windows, the primary action traditionally sits at the bottom
right. Buttons within components such as notifications, search fields, and data
tables are also right-aligned.

In some cases a button group—or even a single button in the case of a side panel
or small tile—may span the entire width of a window or container. Typical nested
button locations include:

- Banner calls to action
- Dialog windows
- Wizards
- Forms
- Cards
- Toolbars

![Primary button context](/static/7ba0382c0f40976a7927ddcec2e9c623/3cbba/button_usage_10.png)

Alignment of buttons across various layouts.

| Alignment | Use case |
| --- | --- |
| Left-justified | Banner call to actions, in-page forms, and nested buttons in components like tiles. |
| Right-justified | Inline notifications, inline field buttons and data tables, progressive forms, wizards, and single-button dialogs. |
| Full-span | Dialogs, side panel, and small tiles; currently Carbon does not offer a way to implement full-span buttons in code, without an override as mentioned [here](https://github.com/carbon-design-system/carbon/blob/66c14c2d2631a868703073a6cfabf1fd03a0b9e7/packages/styles/scss/components/button/_mixins.scss#L56), they max out at 320px. |

#### Fixed width button

Button alignment is also closely related to whether the button is treated as a
fixed or a fluid element within a layout. When we say “fixed,” there is a fixed
padding of 16px to the left and a 64px padding to the right of the button label.
The button label determines the button’s width. Refer to the
[Style tab](/components/button/style#button-structure) for more guidance.

![Example of a fixed width primary button in a layout.](/static/9b9e0e26088f8c3490884b34c71857c4/3cbba/button_usage_bg_1.png)

Example of a fixed width primary button in a layout.

#### Hanging versus non-hanging button alignment

Hanging button alignment is when the button label is aligned to the grid rather
than the container. This alignment should be used to group sections between
components and buttons that directly affect each other.

Non-hanging button alignment is when the button container is aligned to the
grid. These rules apply to buttons with a visible container. For buttons that
don’t have a visible container in the default state, such as ghost button and
danger ghost button, refer to
[ghost button](/components/button/usage/#ghost-button) alignment.

![Example of a fixed width button’s hanging alignment.](/static/f3bbeba31be95f8aa53db0ac855a0e25/a5df1/button_usage_bg_2.png)

Example of a fixed width button’s hanging alignment.

![Example of a fixed width button’s non-hanging alignment.](/static/e57d396d003094cc0250a31f618cdcac/a5df1/button_usage_bg_3.png)

Example of a fixed width button’s non-hanging alignment.

#### Fluid width button

There is a hybrid scenario where a floating primary, secondary, or tertiary
button can span a designated number of columns on the responsive column grid,
giving it a fluid width. These are called “fluid width buttons.”

Fluid width buttons are always preferable to fixed width default buttons in a
layout. When possible, set the button container’s relative position to the
responsive layout grid and match the button width to the width of other elements
on the page. Ideally, when using groups of related buttons (not including ghost
buttons unless in a tearsheet or modal), they should all be the same width. See
button groups below for more detailed information.

![Example of a fluid width primary button matching the width of a card in a layout.](/static/c802d07ce53a128d1dcd3b90e5562da0/3cbba/button_usage_bg_4.png)

Example of a fluid width primary button matching the width of a card in a
layout.

### Button groups

Button groups are a useful way of aligning buttons that have a relationship.
Group the buttons logically into sets based on usage and importance. Too many
calls to action will overwhelm and confuse users so they should be avoided.

As mentioned in the [Emphasis section](#emphasis), you don’t necessarily need to
use the buttons in the order that their labels imply. Either a secondary or a
tertiary button can be used in conjunction with a primary button. In fact, due
to the visual weight of the secondary button, it’s recommended to use tertiary
or ghost buttons in layouts with more than three calls to action.

![Example of button groups in a UI.](/static/1f9e981a53484200a07fae2ef96417e1/3cbba/button_usage_bg_5.png)

Example of button groups in a UI.

#### Button groups versus menu buttons

Button groups should be used when there are either two or three actions that a
user needs to consider. Any more than three actions should be grouped
meaningfully using [menu buttons](/components/menu-buttons/usage/), to reduce
the amount of space these actions take up on a page. Alternatively, for
interfaces that need many common actions or functions, consider using a
[toolbar](https://pages.github.ibm.com/carbon/ibm-products/components/toolbar/usage/).

![Do use menu buttons to group meaningful actions being applied to the same data.](/static/c2aa4e28aa7a6b625b1430016b95d256/6e9cd/button_usage_bg_6.png)

Do use menu buttons to group meaningful actions being applied to the same data.

![Do not use many individual buttons applying to the same data.](/static/099c1c7a89b2c30d692bc16a4a1578d3/6e9cd/button_usage_bg_7.png)

Do not use many individual buttons applying to the same data.

#### Button width in button groups

When using groups of related buttons (not including ghost buttons), they should
all be the same width. The width of all the buttons is usually determined by the
longest button label.

*Note: We recommend following this guidance for both the toolbar and the batch
actions toolbar as well.*

![Example of button width in button groups.](/static/420ddb4ec7cb31d419b633ab6e467f35/3cbba/button_usage_bg_8.png)

Example of button width in button groups.

![Do apply the same width to all buttons in a group, even if they don’t bleed.](/static/567bbe81e6afacaea3f4cb22388be5d6/a5df1/button_usage_bg_9.png)

Do apply the same width to all buttons in a group, even if they don’t bleed.

![Do not make buttons in a group different widths.](/static/c969ff343c5b7d3d0b7efb5bac42586c/a5df1/button_usage_bg_10.png)

Do not make buttons in a group different widths.

#### Hanging versus non-hanging fluid width button group alignment

This can be achieved in one of two ways, both of which are acceptable. The first
approach involves using the
[narrow gutter mode](https://carbondesignsystem.com/elements/2x-grid/usage/#gutter-modes).
In this situation, each button would be set individually on the column grid.

*Note: Carbon developers are working on the narrow gutter mode, currently
left-hanging buttons can only be achieved with an override.*

Some products don’t want to hang their buttons into the gutter, but still want a
16px distance between buttons. This can be achieved while maintaining same-width
buttons by treating the button group as a single object (rather than two
separate entities) on the grid. Each button will essentially span 50% of its
container with a programmatic 16px gutter between them.

![Example of hanging buttons in a button group.](/static/5612787209267871af699b79b984ae23/6e9cd/button_usage_bg_11.png)

Example of hanging buttons in a button group.

![The button group is treated as one element on the grid to achieve a 16px gutter between the two, without the gutter hang.](/static/51f109ddd7700302daecf0dcb370162e/6e9cd/button_usage_bg_12.png)

The button group is treated as one element on the grid to achieve a 16px gutter between the two, without the gutter hang.

#### Fluid button groups

When we say “fluid,” we mean that the button becomes a part of a larger,
compound component by bleeding to two or more edges of its container. Rather
than defining the fluid button in columns or mini units, its width is defined as
a percentage (often 50%) of the container’s width.

Within the layout of a page, primary, secondary, or tertiary variants of buttons
can have fluid widths. In more contained spaces, like in tearsheets or modals, a
ghost button can have a fluid width when paired with other buttons in a group.
Also, as a general rule, fluid buttons are never left-aligned in a layout or a
container—they’re either right-aligned or span the full width of the container.

![Login screen using a fluid input field and a fluid button.](/static/ef7ef467268c97d47789f3584e7facd1/3cbba/button_usage_11.png)

Login screen using a fluid input field and a fluid button.

![Do bleed ghost button hovers when they are paired with other fluid buttons.](/static/253b82b2f8b1846a09008dbd87bbe396/a5df1/button_usage_12.png)

Do bleed ghost button hovers when they are paired with other fluid buttons.

![Do not use a tertiary button in a fluid application.](/static/aa40a40baa862d4baf1a8b0783c4d026/a5df1/button_usage_13.png)

Do not use a tertiary button in a fluid application.

#### Fluid button border

There is a 1px border between all fluid buttons that use the

```
$button-separator
```

Copy to clipboard

token for borders. This feature adds a 3:1 distinction between the two
interactive UI elements. The border is a recommended feature to improve
accessibility. Refer to the
[Style tab](/components/button/style#button-groups-structure) for more guidance.

![Example of $button-separator token border between fluid buttons.](/static/339353ed8e87283ea49049afd54584db/3cbba/button_usage_14.png)

Example of $button-separator token border between fluid buttons.

#### Horizontally arranged groups

When using multiple buttons, the position of the primary button adheres to the
[alignment guidance](#alignment) above. To sum up, a primary button will be
left-aligned and positioned to the left of the secondary/tertiary button on
full-page designs. The primary button will be right-aligned and appear to the
right of the secondary/tertiary button within wizards and dialog windows.

**Note:** This guidance has changed. Previously we advocated maintaining the
primary button position to the right of the secondary button when the button
group was left-aligned. After talking to teams and doing more research, we’ve
revised our position.

![Button groups in context](/static/ad75c608c362d5d13c5aa025f4b98f6d/3cbba/button_usage_23.png)

#### Vertically stacked button groups

Typical product landing pages have buttons side by side. However vertical button
groups are also common in products, to save real estate in narrow columns and
occasionally side panels.

These stacked buttons can act as fluid buttons bleeding into the side panel, or
they can have a 16px spacing surrounding the side panel. The 16px spacing allows
the use of a tertiary button in the vertically stacked button group. In these
instances, the primary button is always on top and the secondary or tertiary
button is below.

*Note: Experimenting with stacked fluid buttons would require an override to the
existing code.*

![Fluid and default stacked button group examples](/static/cdc5cc07091ff4be5cd2628bc1706529/3cbba/button_usage_24.png)

#### Button group combinations

Button groups can consist of different button variants depending on the product
use case. We recommend the following combination of button groups.

Button groups with a primary button

| Number of buttons | Recommended combinations |
| --- | --- |
| 2 | - Primary and secondary button - Primary and tertiary button - Primary and ghost button - Primary and danger tertiary button - Danger primary and secondary button - Danger primary and ghost button |
| 3 | - Primary, secondary, and tertiary button - Primary, secondary, and ghost button - Primary and 2 secondary buttons - Primary and 2 tertiary buttons - Primary, tertiary, and danger tertiary |

Button groups without a primary button

| Number of buttons | Recommended combinations |
| --- | --- |
| 2 | - 2 Tertiary buttons - Tertiary and ghost button - 2 Ghost buttons |
| 3 | - 3 Tertiary buttons - 2 Tertiary and 1 danger tertiary button |

#### Button group combinations to avoid

Button groups can consist of different button variants depending on the product
use case. We recommend avoiding the following combination of button groups.

![Do not use two high-emphasis buttons in a button group.](/static/fded80d07f1616a2dbd5dd896be70f7b/a5df1/button_usage_bg_14.png)

Do not use two high-emphasis buttons in a button group.

![Do not use two high-emphasis buttons in a button group.](/static/6e1bd59b5a00b17cc5f6309ae199fc5f/a5df1/button_usage_bg_13.png)

Do not use two high-emphasis buttons in a button group.

![Do not use the secondary button in conjunction with non-primary buttons.](/static/f4285874ee5b5a871e8f6f65e907a7e8/a5df1/button_usage_bg_16.png)

Do not use the secondary button in conjunction with non-primary buttons.

![Do not use tertiary and danger tertiary buttons together.](/static/f90b46b9ab29295e31742e2b5f7fd79f/a5df1/button_usage_bg_18.png)

Do not use tertiary and danger tertiary buttons together.

![Do not use primary and danger ghost buttons together.](/static/2abc48e50980f566a0b232e5709fd09d/a5df1/button_usage_bg_15.png)

Do not use primary and danger ghost buttons together.

![Do not use tertiary and danger ghost buttons together.](/static/9139aad3079b08403a786315c5dffee2/a5df1/button_usage_bg_17.png)

Do not use tertiary and danger ghost buttons together.

## Content

### Main elements

#### Button label

A button’s label is the most important element on a button, as it communicates
the action that will be performed when the user interacts with it. Buttons need
to be clear and predictable.

Button labels should clearly indicate the action of the button. To provide
enough context, use the {verb} + {noun} content formula on
buttons except in the case of common actions like “Done”, “Close”, “Cancel”,
“Add”, or “Delete”.

There are exceptions to this rule for situations in which button length could
cause problems in compact UIs or negatively impact translation, but the
{verb} + {noun} formula is still best practice.

By default Carbon uses sentence case for all button labels.

For consistency, see Carbon’s
[content guidelines](/guidelines/content/action-labels) for a list of
recommended action labels.

![Do use the verb + noun content formula in buttons whenever possible.](/static/b1168579e269d14034c2ea75e9237975/a5df1/button_usage_26.png)

Do use the {verb} + {noun} content formula in buttons whenever possible.

![Do not use only a noun as a button label.](/static/e8f60f26377317f55f5a2845a8aa1cd5/a5df1/button_usage_27.png)

Do not use only a noun as a button label.

Label alignment

![Do left-align the label in a button, even if the button is wide.](/static/f033c8c492b327d4662a696c13c0083e/a5df1/button_usage_5.png)

Do left-align the label in a button, even if the button is wide.

![Do not center align the label in a button, even if the button is wide.](/static/da5bb4f00a9488c5b9efb0876518e2a9/a5df1/button_usage_6.png)

Do not center align the label in a button, even if the button is wide.

#### Internationalization (RTL)

For right-to-left (RTL) languages, the entire button is mirrored horizontally.
The label is right-aligned and the icon is left-aligned.

![Primary button without and with RTL.](/static/3826efdcc0068728103d1e0171c7c283/3cbba/button-usage-RTL.png)

Primary button without and with RTL.

### Overflow content

When the button’s label is too long to fit within the available space of the
button, the label should overflow and wrap to the second line. We do not
recommend truncating a button label.

As mentioned above, it is best practice to keep button label succinct and follow
the {verb} + {noun} content formula.

![Do wrap the button label to a second line if there’s overflow content.](/static/f4bae65a4da706a34e42ed03ac4b86d4/a5df1/button_usage_overflow_1.png)

Do wrap the button label to a second line if there’s overflow content.

![Do not truncate the label of a button if there’s insufficient space inside the button.](/static/c805fc20709de8442663047831b0a62f/a5df1/button_usage_overflow_2.png)

Do not truncate the label of a button if there’s insufficient space inside the button.

### Further guidance

For further content guidance, see Carbon’s
[content guidelines](https://carbondesignsystem.com/guidelines/content/overview/).

## Universal behaviors

### Primary button focus

The primary button is the default action. When dialogs appear, the primary
button typically takes focus. On a form, if focus is on a component that is not
actionable with the

```
Enter
```

Copy to clipboard

key, pressing

```
Enter
```

Copy to clipboard

will activate the primary
button.

![Primary button takes default focus when there’s no other actionable component in a dialog.](/static/4fc124a726d6336b1ef4de737dff5b37/3cbba/button_usage_ub_focus.png)

Primary button takes default focus when there’s no other actionable component
in a dialog.

### States

The default and interactive states of buttons should follow the
button [Style](/components/button/style#color) tab guidelines.

### Interactions

#### Mouse

Users can trigger a button by clicking anywhere within the button container.

![Mouse interaction for button.](/static/d95ca554d84aba10719ec77f57de25ba/3cbba/button_usage_ub_interaction.png)

Mouse interaction for button.

#### Keyboard

Users can trigger a button by pressing

```
Enter
```

Copy to clipboard

or

```
Space
```

Copy to clipboard

while the button has
focus. For additional keyboard interactions, see the
[Accessibility](/components/button/accessibility) tab.

### Loading

Buttons can have
[inline loading](https://carbondesignsystem.com/components/inline-loading/usage/)
that provides visual feedback that the action is in process. The button would be
disabled when inline loading is in progress.

![Inline loading in the context of a button.](/915fb05bd80aec9c1ecc3f2570397900/button-usage-ub-inline-loading.gif)

![Inline loading in the context of a button.](images/button_usage_ub_loading_4.png)

Inline loading in the context of a button.

## Primary button

Primary button is used for the principal call to action on the page. Primary
button should only appear once per screen (the only exceptions are temporary
flows with primary actions). Primary button helps give the user focus and gives
them context behind the expected next step.

![Primary button in the context of a product UI.](/static/fadee354c639a9d7ab573e87b62cf1f2/3cbba/button_usage_primary_1.png)

Primary button in the context of a product UI.

#### Temporary flows with primary action

There may be times when there is a primary button on a page, but through
interaction with the page content, another flow may be launched that has its own
primary button. Temporarily, there may be two primary buttons on a page.

In this case, a user has triggered something with an intention to focus on
another flow, therefore temporarily having two primary buttons on a page is
acceptable. This is the only scenario where having two primary actions on a page
is advised.

![A temporary user flow where a data table with primary action has an open side panel with its own primary action.](/static/470fe154edb3fdbc6ff34a737e0d8d82/3cbba/button_usage_primary_2.png)

A temporary user flow where a data table with primary action has an open side
panel with its own primary action.

### Best practices

#### Not every page needs a primary button

Sometimes the primary purpose of the page is to interact with other components
or read over content, rather than to trigger an action. In this case, use
tertiary and ghost buttons for these supporting actions or experiences.

![The primary intent of this page is to present content, with actions like filtering and editing represented by tertiary and ghost buttons.](/static/5b18c8f335d65ca01b8a1bfea28cc3c9/3cbba/button_usage_primary_3.png)

The primary intent of this page is to present content, with actions like
filtering and editing represented by tertiary and ghost buttons.

## Secondary button

As mentioned in the [emphasis section](#emphasis),  secondary buttons are
tonally heavy but have less visual prominence than their primary counterparts
due to their lower saturation. As a result, secondary buttons are intended to be
used in conjunction with a primary button. When used in a pair, the secondary
button executes the set’s negative action, like “Cancel” or “Back.”

![Secondary button in the context of a product UI.](/static/3727fda794e423ba7755fad8aaf86cdb/3cbba/button_usage_secondary_1.png)

Secondary button in the context of a product UI.

Secondary buttons should not be used in isolation or for a positive/primary
action. See [button groups](#button-groups) for more guidance on how to use
secondary buttons.

![Do use the secondary button in conjunction with the primary button.](/static/d7252bafc6f3f6d6ef95e368993a31a5/a5df1/button_usage_secondary_2.png)

Do use the secondary button in conjunction with the primary button.

![Do not use the secondary button in isolation or for a positive/primary action.](/static/0ef10f29fda2c840e813718eeae92f26/a5df1/button_usage_secondary_3.png)

Do not use the secondary button in isolation or for a positive/primary action.

## Tertiary button

Tertiary buttons have less prominence than a primary button and slightly more
prominence than a ghost button. Tertiary buttons work well on their own or as
part of a button group.

![Tertiary button in the context of a product UI.](/static/1dc0332dfa86b34243e2bf198af68278/3cbba/button_usage_tertiary_1.png)

Tertiary button in the context of a product UI.

Tertiary buttons should stay aligned with the content of the page. Always make
sure the tertiary button has adequate padding on all sides. As mentioned in the
[fluid button guidance](#alignment), tertiary buttons should not be used in
fluid arrangements.

![Do align the tertiary button with the rest of the content.](/static/07b9ed406f76365ebbb2fc2d9de003c9/a5df1/button_usage_tertiary_2.png)

Do align the tertiary button with the rest of the content.

![Do not use a tertiary button in a fluid arrangement.](/static/7bf758d779f8599509dca590ef5eff5d/a5df1/button_usage_tertiary_3.png)

Do not use a tertiary button in a fluid arrangement.

### Best practices

#### Tertiary buttons for page headers

It is challenging to use a primary button in the header of a page because the
content beneath the header is probably going to have a primary action, or will
in a future release. Even if the the button in the page header is not styled as
a primary button, it has significant prominence due to its hierarchical
placement at the top.. Therefore, it is advised to use a tertiary button for
page headers.

If it is determined that the button in the page header, across all tabs, should
be primary, ensure none of the content below the header contain another primary
action.

![Do use a tertiary button in the page header if there is a primary button in the content section.](/static/fc9f3739626ff80399bca137bc0eb567/a5df1/button_usage_tertiary_4.png)

Do use a tertiary button in the page header if there is a primary button in the content section.

![Do not use a primary button in the page header and the content section.](/static/fa31ed46cb6d048fb18a80a924c0d752/a5df1/button_usage_tertiary_5.png)

Do not use a primary button in the page header and the content section.

#### Tertiary buttons in button groups

In [button groups](#button-groups), where there is one primary and two other
actions with shared importance, consider using tertiary buttons.

![Example of tertiary buttons used in button groups.](/static/d00282110703398ae82f6403711fa55c/3cbba/button_usage_tertiary_6.png)

Example of tertiary buttons used in button groups.

#### Tertiary buttons in empty states

For empty states that appear on pages that already have the primary action
defined, a tertiary button is the ideal solution to launch a new task flow.

![Example of a tertiary button used with empty state content.](/static/93a57fa2c4adb09463798ae8448c5e7f/3cbba/button_usage_tertiary_7.png)

Example of a tertiary button used with empty state content.

## Ghost button

Ghost buttons have the least prominence among the button variants. Ghost buttons
are more subtle, making them ideal for supplementary actions. They work best
when they are flush against a container or horizontally grouped with other
elements.

![Ghost button in the context of a product UI.](/static/5ef8cff6045e54f017ee5d50fbdc0975/3cbba/button_usage_ghost_1.png)

Ghost button in the context of a product UI.

#### Aligning ghost buttons

Ghost buttons work well when aligned to a corner of a container. The general
rule for vertically aligning a ghost button with other content is to ensure its
label aligns with the text elsewhere on the page.

![Do align the ghost button label with the rest of the content.](/static/7e33ac37ca8a6a2ffebd3a990e7a2d93/a5df1/button_usage_ghost_2.png)

Do align the ghost button label with the rest of the content.

![Do not align the edge of the ghost button with the rest of the content, even if it looks partially aligned.](/static/a630a142a4623682e1bac6c70965743b/a5df1/button_usage_ghost_3.png)

Do not align the edge of the ghost button with the rest of the content, even if it looks partially aligned.

Ghost buttons can be useful for small supplementary actions in side panels. In
this context, extending the width of the ghost button to the full width of the
container makes this treatment seem intentional. Aligning to the full width of a
container is only recommended when the containers are smaller in size such as a
side panel of 480px (medium) and below.

![Do extend the ghost button to the full width of the side panel.](/static/455c726d8217536bf9e751ddd98272bc/a5df1/button_usage_ghost_4.png)

Do extend the ghost button to the full width of the side panel.

![Do not leave a ghost button hanging halfway within the side panel.](/static/54c48f85bb4416fc3737b81f3607908b/a5df1/button_usage_ghost_5.png)

Do not leave a ghost button hanging halfway within the side panel.

Ghost buttons can also be aligned horizontally and inline with other components
on the page.

![Example of a ghost button aligned horizontally and inline with a component.](/static/485e450b1206a9b3a732d2f17d476162/3cbba/button_usage_ghost_6.png)

Example of a ghost button aligned horizontally and inline with a component.

### Best practices

#### Ghost buttons for data table actions

Buttons in the table toolbar are often depicted as a primary button, but this
might not always be the case. Use a ghost button instead if there is another
button on the page that requires primary styling.

![A ghost button represents the data table's primary action to avoid conflict with the primary button in the page header.](/static/d4faec396cee58d0e0c6ab6090fe120f/3cbba/button_usage_ghost_7.png)

A ghost button represents the data table’s primary action to avoid conflict
with the primary button in the page header.

#### Ghost buttons in productive cards

In dashboards with multiple productive cards, ghost buttons work well as they
draw less attention than a tertiary button. For a ghost button to appear aligned
in vertical arrangements within a container, it is recommended that it touches
at least two edges of the container.

See
the [cards component](https://pages.github.ibm.com/carbon/ibm-products/components/card/overview/)
for more details.

![Example of a ghost button used in cards.](/static/9e8572bf7e4ae2823777a091d277274d/3cbba/button_usage_ghost_8.png)

Example of a ghost button used in cards.

#### Ghost button used as a cancel action

Ghost buttons work well as a cancel button in progressive flows, as they draw
less attention; users have to purposefully find and click the button to cancel.
In tearsheets, the buttons are fluid, which wouldn’t be a suitable application
for a tertiary button.

![Example of ghost button used in a modal.](/static/0b8878b60687e237bb8deb14df7517fe/3cbba/button_usage_ghost_9.png)

Example of ghost button used in a modal.

## Danger button

Danger button is used for actions that could have destructive effects, such as
“Delete”, “Remove”, or “Stop”.

The danger button has three different styles:
[primary](/components/button/style#danger-primary-button-color.mdx),
[tertiary](/components/button/style#danger-tertiary-button-color.mdx), and
[ghost](/components/button/style#danger-ghost-button-color.mdx). Determining
which danger button style to use will depend on the level of emphasis you want
to give to the destructive action. Destructive actions that are a required or
primary step in a workflow should use the primary danger button style. However,
if a destructive action is just one of several actions a user could choose from,
then a lower emphasis style like the tertiary danger button or the ghost danger
button may be more appropriate.

![Danger button in the context of a product UI.](/static/94218fba9d78e0809c2f37fa9a352e72/3cbba/button_usage_danger_primary.png)

Danger button in the context of a product UI.

![Do use a tertiary danger button for lower emphasis destructive actions.](/static/9f483ccbd68610c073eee2ca0fc0054d/a5df1/button_usage_danger_tertiary.png)

Do use a tertiary danger button for lower emphasis destructive actions.

![Do use a ghost danger button for lower emphasis destructive actions.](/static/b81924c26f3f1629e352ee4a1cd18ea0/a5df1/button_usage_danger_ghost.png)

Do use a ghost danger button for lower emphasis destructive actions.

## Modifiers

### Button with icon

Icons can be placed next to labels to clarify an action and call attention to a
button. However, icons should be used sparingly, as overuse can create visual
noise and make an experience less usable. If you use a button with an icon in
one part of your UI it does not mean that you need to add icons to all other
buttons.

- Use a 16px icon within buttons; use a 20px icon within the large expressive
  buttons.
- Icons are distinguished by their solid shape and knocked-out details.
- Icons should always appear to the right of the label.
- Icons used in buttons must be directly related to the action that the user is
  taking.
- Icons must match the color value of the label within a button.

![Do place the icon on the right side of the button after the label](/static/10fbad387d09e8aecaa1e22fd7c291ee/a5df1/button_usage_button_with_icon_1.png)

Do place the icon on the right side of the button after the label.

![Do not place the icon to the left of the label on the button.](/static/b215337ea08b46266a7c4214e620f0c1/a5df1/button_usage_button_with_icon_2.png)

Do not place the icon to the left of the label on the button.

![Do use 8px spacing between the label and the icon in a ghost button.](/static/4d6bce6f1aba2f89bd87b58da974dddb/a5df1/button_usage_button_with_icon_3.png)

Do use 8px spacing between the label and the icon in a ghost button.

![Do not leave too much space between the label and the icon in a ghost button.](/static/7b45eaa0173fdf02b41c89f140c1eb0d/a5df1/button_usage_button_with_icon_4.png)

Do not leave too much space between the label and the icon in a ghost button.

#### Universal actions with well-established icons

When deciding whether to add an icon to a button, it’s important to consider how
recognizable the icon is and whether, in other contexts, a similar icon may be
used for a different meaning. We want to avoid the same icon being used for
completely different actions.

For this reason, we have defined a set of universal actions suitable for adding
an icon alongside the button label. These have clearly defined and widely
recognized icons within IBM Software and beyond.

Icons that are not in this list can be used in buttons, as long as the icon
clearly conveys the intended action. To determine the expected use of an icon,
check its name in the
[Carbon icon library](https://carbondesignsystem.com/elements/icons/library/).

| Name of action | Associated icon | Name in icon library |
| --- | --- | --- |
| Create/Add |  | Add |
| Edit |  | Edit |
| Copy |  | Copy |
| Delete |  | Trash can |
| Remove |  | Subtract alt |
| Export |  | Export |
| Upload |  | Upload |
| Download |  | Download |
| Play/Start |  | Play |
| Pause |  | Pause |
| Stop |  | Stop outline |
| Refresh |  | Restart |

Do you think a universal action with a clearly defined icon is missing? Let us
know [here](https://github.com/carbon-design-system/carbon/issues/new/choose).

#### Do not use a defined icon to represent a different universal action

Using icons in the above list for other actions can confuse the expected outcome
and experience.

![Do use a defined icon to represent a universal action.](/static/bf0e895c33ebd565260c35d2f4252042/a5df1/button_usage_button_with_icon_5.png)

Do use a defined icon to represent a universal action.

![Do not use an icon for an action that would not be associated with it.](/static/e9199ffb792fd572a7693dbeadbd410a/a5df1/button_usage_button_with_icon_6.png)

Do not use an icon for an action that would not be associated with it.

#### Launch icon

The launch icon should be used on any call to action that launches the user into
another tab (whether the content of the new tab is part of the same product or
an entirely separate web resource). Buttons and links requiring the launch icon
are often found in the UI left navigation area, side panel, cards, and modals.
The target destination of the launch action should be made clear to the user
through the button or link label and the surrounding context.

*For IBMers only:* See the
[navigation labels](https://pages.github.ibm.com/carbon/ibm-products/guidelines/content/navigation-labels/)
of our content guide.

![Example of a tertiary button with icon indicating that clicking the button would launch a new page.](/static/d013054885568387821223c301b0d971/3cbba/button_usage_button_with_icon_7.png)

Example of a tertiary button with icon indicating that clicking the button
would launch a new page.

#### Be consistent with icon usage for buttons in a button group

Using icons in button groups is optional. We recommend showing an icon for each
button in a button group or showing no icons for consistency. A benefit of
pairing an icon with a button label is that it visually describes its action and
directs more attention to it. However, in some cases, using too many buttons
with icons in a group can create unwanted noise in the UI and tend to
overcomplicate a simple experience.

Only use icons in button groups for the universal actions listed in the table
above or for other actions where a particular icon is commonly paired and
associated.

![Do follow a consistent approach across button groups when introducing icons.](/static/74f1a4d3453ae9cab6c4a24b04eddd63/a5df1/button_usage_button_with_icon_8.png)

Do follow a consistent approach across button groups when introducing icons.

![Do follow a consistent approach across button groups when introducing icons.](/static/3ff9a2a475145e6ee8322e76f23d63b1/a5df1/button_usage_button_with_icon_9.png)

Do follow a consistent approach across button groups when introducing icons.

![Do not introduce icons only for a few buttons in a button group.](/static/e5bea5ed8e528f2ec1ee1f7bc7cc0296/a5df1/button_usage_button_with_icon_10.png)

Do not introduce icons only for a few buttons in a button group.

![Do not introduce icons only for a few buttons in a button group.](/static/86bdaa676ed25a755832fd3c7cb6c1d0/a5df1/button_usage_button_with_icon_11.png)

Do not introduce icons only for a few buttons in a button group.

#### Use the default variation for all icons

The Carbon library contains filled variants of a few icons. Since not every icon
has this variation, we advise using the default option for all icons (the only
exception is status icons, which have their own defined icon to use). Default
icons are named after their action.

![Do use the default icon which is “Play”.](/static/520ccc8744a1fb2611d55949e78c6ae2/a5df1/button_usage_button_with_icon_12.png)

Do use the default icon which is “Play”.

![Do not use the filled icon variations.](/static/87306f7dd5a3bc885f12bf51c7351185/a5df1/button_usage_button_with_icon_13.png)

Do not use the filled icon variations.

### Icon only buttons

Icon only buttons allow users to take actions, and make choices, with a single
tap. Icon buttons can take the form of a primary, secondary, tertiary, or ghost
variant but most commonly will be styled as primary or ghost buttons.

Icon only buttons should be used sparingly. “For most situations, users learn
correct interpretations better with text alone than with icons alone.” —
Wiedenbeck, S (1999). For this reason, using icon only buttons is recommended
for the following use cases:

- The icon must be standardized and recognizable without label or must represent
  an action with a strong visual attribute, such as a pin icon for a pinning
  action.
- There is insufficient space and multiple actions, therefore a toolbar using
  icon buttons is required. See
  the [toolbar component](https://pages.github.ibm.com/carbon/ibm-products/components/toolbar/usage/)
  for more details.

![Example of an icon only ghost button in a toolbar showing a tooltip on hover.](/static/c5d9562e5693be3999de84979dbe31ad/3cbba/button_usage_icon_only_button_1.png)

Example of an icon only ghost button in a toolbar showing a tooltip on hover.

#### Tooltips for icon only buttons

Regardless of how recognizable an icon may or may not be, or whether that action
lies within the universal actions list, a tooltip is always required with text
explaining what the icon button would do if clicked.

![Example of an icon only ghost button showing a tooltip on hover.](/static/99ba9629ac679e45d46a3f479f1d5c79/3cbba/button_usage_icon_only_button_2.png)

Example of an icon only ghost button showing a tooltip on hover.

#### Colors of icon only ghost buttons

Carbon builds type, color, and spacing tokens into its components, improving the
ease of component usage. Do not change the color token for icon only ghost
buttons. The same applies for specifications across components. Learn more about
icon only ghost button colors in the
[Style](/components/button/style#ghost-button-color.mdx) tab.

![Do use the system’s defined color for ghost icon only buttons.](/static/15f51899020813bf65a3f4c382bc2e4f/a5df1/button_usage_icon_only_button_3.png)

Do use the system’s defined color for ghost icon only buttons.

![Do not change the color for ghost icon only buttons.](/static/26fe18866343a01dbc2c427077bc0d2d/a5df1/button_usage_icon_only_button_4.png)

Do not change the color for ghost icon only buttons.

#### Danger buttons cannot be used in an icon only form

Danger can be a critical action and should be applied to a button that holds
higher emphasis along with a visual label. As mentioned in
the [danger button guidance](#danger-button),  it is best to use a danger button
in a primary, tertiary, or ghost button form.

![Do use a visual label in a danger button for a destructive action.](/static/c5b03b8a3ceca37dad6399dce1c63de2/a5df1/button_usage_icon_only_button_5.png)

Do use a visual label in a danger button for a destructive action.

![Do not use a danger button in an icon only form for a destructive action.](/static/72447f2d6d01a7bdbbe24f453b0b76d3/a5df1/button_usage_icon_only_button_6.png)

Do not use a danger button in an icon only form for a destructive action.

## Related

- [Button labels](https://pages.github.ibm.com/carbon/ibm-products/guidelines/content/button-labels/)
- [Fixed button bars](https://pages.github.ibm.com/carbon/ibm-products/patterns/fixed-button-bars/usage/)
- [Form pattern](/patterns/forms-pattern)
- [Icons](https://carbondesignsystem.com/elements/icons/library/)
- [Link component](/components/link/usage)
- [Menu buttons](https://carbondesignsystem.com/components/menu-buttons/usage/)
- [Modal component](/components/modal/usage)

## References

- Mehmet Goktürk,
  [*The Glossary of Human Computer Interaction, Chapter 37*](https://www.interaction-design.org/literature/book/the-glossary-of-human-computer-interaction/fitts-s-law)
  (The Interaction Design Foundation)
- Jakob Nielsen,
  [*OK-Cancel or Cancel-OK? The Trouble With Buttons*](https://www.nngroup.com/articles/ok-cancel-or-cancel-ok/)
  (Nielsen Norman Group, 2008)
- Artem Syzonenko
  [*Buttons on the web: placement and order*](https://uxdesign.cc/buttons-placement-and-order-bb1c4abadfcb)
  (UX Collective, 2019)
- Wiedenbeck, S (1999). The use of icons and labels in an end-user application
  program: An empirical study of learning and retention. Behavior & Information
  Technology, 18(2), p68–82

## Feedback

Help us improve this component by providing feedback, asking questions, and
leaving any other comments on
[GitHub](https://github.com/carbon-design-system/carbon-website/issues/new?assignees=&labels=feedback&template=feedback.md).

[Edit this page on GitHub](https://github.com/carbon-design-system/carbon-website/edit/main/src/pages/components/button/usage.mdx)

[Previous

Components: Breadcrumb](/components/breadcrumb/usage/)

[Next

Button: Style](/components/button/style/)