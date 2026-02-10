# Pagination

Source: https://carbondesignsystem.com/components/pagination/usage/

---

# Pagination

Pagination splits content or data into several pages, with a control for
navigating to the next or previous page.

- [Live demo](#live-demo)
- [Overview](#overview)
- [Formatting](#formatting)
- [Content](#content)
- [Pagination](#pagination)
- [Pagination nav](#pagination-nav)
- [Modifiers](#modifiers)
- [Related](#related)
- [Feedback](#feedback)

## Live demo

Theme selector

White

---

Variant selector

Default

---

This live demo contains only a preview of functionality and styles available for this component. View the [full demo](https://react.carbondesignsystem.com/?path=/story/components-pagination--default&globals=theme:white) on Storybook for additional information such as its version, controls, and API documentation.

### Accessibility testing status For every latest release, Carbon runs tests on all components to meet the [accessibility requirements](https://www.ibm.com/able/requirements/requirements/). These different statuses report the work that Carbon has done in the back end. These tests appear only when the components are stable.

Variant

Pagination

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

Not tested](//accessibility/#accessibility-testing-status)

[##### Screen reader

Manually tested](//accessibility/#accessibility-testing-status)

[##### Keyboard navigation

Tested](//accessibility/#accessibility-testing-status)

## Overview

Pagination organizes and divides large amounts of content on separate pages and
gives the user control over how much content they want to view on each page.
Pagination can be used with a data table or on a page.

![Example of the pagination component in a UI](/static/477fbd6d7d1d9f7302f807f0e478f6db/3cbba/pagination-usage-overview-in-context.png)

Example of the pagination component in a UI

### When to use

- When it could take a considerable amount of time to load the available data at
  once or in a scrolling view
- When there is too much data to display on one page or within one view of a
  component
- To make large amounts of data more accessible to consume by users
- To optimize on-page real estate
- To give users more control over how they view large amounts of information

### When not to use

- Do not use it to display linear journeys, for example, in a form progression.
  Instead, use the
  [progress bar](https://carbondesignsystem.com/components/progress-bar/usage/)
  or [button](https://carbondesignsystem.com/components/button/usage/)
  components to navigate forward and backward.
- Do not use pagination superfluously, and aim to use it to improve usability or
  performance.

### Variants

| Variant | Usage |
| --- | --- |
| [Pagination](#pagination) | The pagination variant is typically connected at the bottom of the data table component to help paginate large amounts of data. |
| [Pagination nav](#pagination-nav) | The pagination nav variant is mainly used in on-page situations to help paginate either a whole page or sections of a page. |

## Formatting

### Anatomy of pagination

![Anatomy of the pagination variant](/static/55abdc3c5b7b354b5d0b38a2340095a5/3cbba/pagination-usage-anatomy.png)

Anatomy of the pagination variant

1. **Items per page:** Shows the current number of items that appear per page.
2. **Range of items:** Shows the current range of items and lists the total
   amount of items.
3. **Current page:** Shows the current page the user is on and lists the total
   amount of pages.
4. **Previous and next buttons:** Buttons that take you to the previous or next
   page.
5. **Container:** The container bar of the whole pagination component.

### Anatomy of pagination nav

![Anatomy of the pagination nav variant](/static/a581552f766fdfc7ccb2bb5219b07b16/3cbba/pagination-usage-anatomy-nav.png)

Anatomy of the pagination nav variant

1. **Unselected page button:** A page the user could select and view.
2. **Selected page button:** The current page the user is viewing.
3. **Overflow button:** Contains available pages that can be navigated to but
   cannot be shown upfront in the component because of the current viewport.
4. **Previous and next buttons:** Buttons that take you to the previous or next
   page.
5. **Container:** The container of the whole pagination component.

### Sizing

The pagination component is available in three sizes in both variants:
**large**, **medium**, and **small**.

![Sizes of pagination](/static/33848431ccc70e4f396fa0dc55327d2b/3cbba/pagination-usage-sizes.png)

Sizes of pagination

![Sizes of pagination nav](/static/3f864cdcaada8c4c1990a3beb962f5ac/3cbba/pagination-usage-sizes-pagination-nav.png)

Sizes of pagination nav

### Data table size pairings

We recommend using the same height pagination as you do for the data table
component rows to which it is connected. In some cases, the height sizes of
these two components will not be the same because we do not offer extra small
and extra large sizes for pagination. When using the extra large data table row
height, use the large pagination. When using the extra small data table row
height, use the small pagination.

![Size pairings of the pagination and data table components.](/static/710fd9075389748d790f5ed5d424cb6a/3cbba/pagination-usage-size-pairings.png)

Size pairings of the pagination and data table components

### Placement

Place the pagination near the related component or area of the page where the
information will be paginated.

#### Placing pagination with data table

When using the pagination variant with a data table, the pagination should be
stacked and below the table with no padding between them.

![Placement of the pagination variant](/static/d6a159264994c2ec71c078b3737ebfd8/3cbba/pagination-usage-placement-pagination.png)

Placement of the pagination variant

![Do stack the pagination component below the data table.](/static/240ddbea7b00a3adfa1a97d3325c0c3b/275e0/pagination-usage-placement-data-table-do.png)

Do stack the pagination component below the data table.

![Do not stack the pagination component above the data table.](/static/706215f0d449734f369ea4a2bc62c77f/275e0/pagination-usage-placement-data-table-dont.png)

Do not stack the pagination component above the data table.

#### Placing pagination nav on a page

When using the pagination nav variant on a page, float it below the content to
which it is paginating and related to. The pagination can be right aligned or
left aligned to the content above it. When it doubt, choose right alignment.

![Placement of the pagination nav variant](/static/48aeefa19f70650f7e38919157e95e6a/3cbba/pagination-usage-placement-pagination-nav.png)

Placement of the pagination nav variant

## Content

### Main elements

#### Label text

The label text in the pagination component should be concise and instructional.
It describes the items per page and the number of pages or items. We recommend
not modifying the label text unless necessary for specific use cases.

#### Select component option text

The select components option text is shown as a number, indicating the items per
page and the current page. Alternatively, this can be indicated as a word for
the “Items per page” selection instead of a number.

### Overflow content

In the pagination nav variant, an ellipsis button appears between pages to
indicate that there are numerous pages to navigate to within the ellipsis button
menu. We recommend never placing the ellipsis button at the beginning or end of
a series of pages in the pagination component.

![Placement of the pagination nav variant](/static/55af6a14b56d4c5178584722992cdfc2/3cbba/pagination-usage-overflow-pagination-nav.png)

Example of the ellipsis button for overflow content in the pagination nav
variant

### Further guidance

For further content guidance, see Carbon’s
[content guidelines](https://carbondesignsystem.com/guidelines/content/overview/).

## Pagination

The pagination variant is typically a bar attached to the bottom of a data table
to paginate its data.

![Example of the pagination variant in a UI](/static/a7637b7e0bca9a7586d04deb3d4659b8/3cbba/pagination-usage-pagination-in-context.png)

Example of the pagination variant in a UI

### States

The pagination variant has the select component and ghost icon button component
nested within it and inherits their component states. For more information on
these states, refer to the
[select](https://carbondesignsystem.com/components/select/style/) and
[ghost icon button](https://carbondesignsystem.com/components/button/style/)
style tab guidance.

### Interactions

#### Mouse

- Clicking on the select component will open the menu and reveal options.
- To close the menu, choose a different option or click outside the menu area.
- Clicking on a previous or next button will navigate you to the previous or
  next page.

#### Keyboard

- On focus, the select component menu is opened with pressing

  ```
  Space
  ```

  Copy to clipboard

  or with

  ```
  Up
  ```

  Copy to clipboard

  or

  ```
  Down
  ```

  Copy to clipboard

  arrows which also cycle through the values.
- Pressing

  ```
  Space
  ```

  Copy to clipboard

  or

  ```
  Enter
  ```

  Copy to clipboard

  selects a value and closes the menu.
- The menu can be closed by pressing

  ```
  Esc
  ```

  Copy to clipboard

  .
- The previous and next ghost icon buttons are activated by pressing

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

### Responsive behavior

The pagination variant retains all its content and nested components at every
breakpoint except for the small breakpoint. The select components have been
removed at the small breakpoint, but information on the total number of items,
items being displayed, and previous and next buttons remain.

![Pagination variant responsive behavior in all breakpoints versus the small breakpoint](/static/d63ab8f7a8f0bfb89896e6019bf6a6ba/3cbba/pagination-usage-responsiveness-pagination.png)

Pagination variant responsive behavior in all breakpoints versus the small
breakpoint

### Clickable areas

Within the pagination variant, there are four clickable areas. Two select
components allow you to change the number of items per page and the page number.
Two ghost icon buttons take you to the previous or next page.

![Pagination variant clickable areas](/static/3e6abeb0c5bbabf280b00cb9e84c1314/3cbba/pagination-usage-clickable-areas-pagination.png)

Pagination variant clickable areas

## Pagination nav

The pagination nav variant is most commonly used to paginate full pages or
sections of content on a page. It floats under and near the related content.

![Example of the pagination nav variant in a UI](/static/8b21042114d50f81d451c07c9b2c358e/3cbba/pagination-usage-pagination-nav-in-context.png)

Example of the pagination nav variant in a UI

### States

The pagination nav variant has the ghost icon button component and the  
breadcrumb overflow button component nested within it that inherits their  
component states. For more information on these states, refer to the
[select](https://carbondesignsystem.com/components/select/style/) and
[breadcrumb overflow button](https://carbondesignsystem.com/components/breadcrumb/style/)
style tab guidance.

### Interactions

#### Mouse

- Clicking on a button number will navigate you to that page.
- Clicking on a previous or next caret button will navigate you to the previous
  and next pages of the one you are currently viewing.
- Clicking on an overflow ellipsis button will open a select menu to choose a
  page to navigate to. Upon clicking on a page option from the menu, you will
  navigate to that page.

#### Keyboard

- The icon button receives focus and you can move between buttons by pressing
  the

  ```
  Up
  ```

  Copy to clipboard

  or

  ```
  Down
  ```

  Copy to clipboard

  arrows.
- The page number buttons are activated by pressing

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
- The previous and next buttons are activated by pressing

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

### Responsive behavior

In small screens, the pagination nav variant can provide an ellipsis button to
indicate there are more pages to navigate to within the ellipsis button menu.

![Pagination nav variant responsive behavior in large versus small breakpoints](/static/5253de67705ca6336c73ea6b3644462e/3cbba/pagination-usage-responsive-behavior-pagination-nav.png)

Pagination nav variant responsive behavior in large versus small breakpoints

### Clickable areas

Every button in the pagination nav variant is clickable. Two ghost icon buttons
take you to the previous or next page. The rest of the page number buttons take
you to that particular page.

![Clickable areas within the pagination nav variant](/static/8e587df1610ed7199ceb4cec9cae1e3f/3cbba/pagination-usage-clickable-areas-pagination-nav.png)

Clickable areas within the pagination nav variant

## Modifiers

### Page looping

For the pagination nav variant, instead of turning off the previous or next
caret buttons when you reach either the first or last page of the pagination
component, you can enable the option to loop through the available pages
continuously.

### Page naming

By default, the select component option text is displayed as a number, showing
items per page and the current page. However, we offer an alternative option to
use a word instead of a number for the “Items per page” selection if that better
meets your requirements.

![Select components content alternative of numbers versus words](/static/34c51cc201846cb9c9d9ce98cc5b8bf0/3cbba/pagination-usage-modifier-page-naming.png)

Select components content alternative of numbers versus words

## Related

- [Data table](https://carbondesignsystem.com/components/data-table/usage/)

## Feedback

Help us improve this component by providing feedback, asking questions, and
leaving any other comments on
[GitHub](https://github.com/carbon-design-system/carbon-website/issues/new?assignees=&labels=feedback&template=feedback.md).

[Edit this page on GitHub](https://github.com/carbon-design-system/carbon-website/edit/main/src/pages/components/pagination/usage.mdx)

[Previous

Components: Number input](/components/number-input/usage/)

[Next

Pagination: Style](/components/pagination/style/)