# Search

Source: https://carbondesignsystem.com/components/search/usage/

---

# Search

Search enables users to specify a word or a phrase to find relevant content
without navigation.

- [Live demo](#live-demo)
- [Overview](#overview)
- [Formatting](#formatting)
- [Content](#content)
- [Behaviors](#behaviors)
- [Related](#related)
- [Feedback](#feedback)

## Live demo

Theme selector

White

---

Variant selector

Default

---

This live demo contains only a preview of functionality and styles available for this component. View the [full demo](https://react.carbondesignsystem.com/?path=/story/components-search--default&globals=theme:white) on Storybook for additional information such as its version, controls, and API documentation.

### Accessibility testing status For every latest release, Carbon runs tests on all components to meet the [accessibility requirements](https://www.ibm.com/able/requirements/requirements/). These different statuses report the work that Carbon has done in the back end. These tests appear only when the components are stable.

Variant

Search

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

Not available](//accessibility/#accessibility-testing-status)

[##### Keyboard navigation

Tested](//accessibility/#accessibility-testing-status)

## Overview

Search offers users a way to explore a website or application using keywords.
Search can be used as the primary means of discovering content or as a filter to
aid the user in finding content.

### When to use

- To help users find data more efficiently within a complex or large data set.
- Use at a global level when searching an entire site.
- Use at a page level when searching through content on one page specifically.
- Use at a component level when searching data in a component, like a
  [data table](https://carbondesignsystem.com/components/data-table/usage/#search).

### When not to use

- Do not use when there is small or limited amounts of data.
- Do not use when the information is simple and can be found easily within one
  view.

## Formatting

### Anatomy

1. **Field:** The place where a user enters their search query.
2. **Search icon:** Signifies a search field. The magnifying glass icon is a
   universal way to indicate search.
3. **Field text:** Inputted search text by the user. Placeholder text is visible
   before the user types into the field.
4. **Close icon:** Appears after the user has actively typed into the search
   field. Acts as a function to clear the search field.

- Default
- Fluid

![Default search anatomy](/static/9b9ce4f95e48343793a2e188a96feeb2/3cbba/search-anatomy-fixed.png)

![Fluid search anatomy](/static/634b1ad345467254c5412ca9979dc3ac/3cbba/search-anatomy-fluid.png)

### Styling

There are two styles of search, default and fluid. They share the same
functionality but look visually different, influencing where to use them.

| Style | Appearance | Use case |
| --- | --- | --- |
| Default | A traditional style where there is no label indicated. | Use when white space is needed between components. For example, a default search style is typically used at a global or page level. |
| Fluid | An alternative style where a label is placed inside of the search field and is stacked inline with the user input field text. | Use in expressive moments, fluid forms, and contained spaces. |

![Default and fluid search styles](/static/2f5543ef0f0695bfd9e0fac8e1e1fa6c/3cbba/search-styles.png)

A default style input is shown on the top and fluid style is on the bottom.

### Sizing

#### Default input heights

There are three default search height sizes: small, medium, and large. The width
varies in size based on content, layout, and design. Supporting three different
search sizes gives you more flexibility when structuring layouts.

| Size | Height (px/rem) | Use case |
| --- | --- | --- |
| Small (sm) | 32 / 2 | Use when space is constricted within a design. |
| Medium (md) | 40 / 2.5 | This is the default size and the most commonly used size. When in doubt, use the medium size. |
| Large (lg) | 48 / 3 | Use when there is a lot of space to work with. The large size is typically at a global level when the user is searching content within a page view. |

![Default search sizes](/static/95d5bf92f72fc5ad37c9341de802c5f5/3cbba/search-sizes-fixed.png)

#### Fluid input height

There is only one input height at 64px and it is visually larger than the
default heights.

![Fluid search size](/static/befd841464b0b14f6b29945a82320525/3cbba/search-sizes-fluid.png)

### Placement

Place the search component within a user interface where users expect to find it
and where it is appropriate for how it is being used in context, whether at a
global level, page-specific level, or within a component.

The default search can be arranged on the grid to align the container with other
components containers. Search can also hang to align with other hanging
component containers on the same page, depending on the use case.

![Do align the default search container vertically with other text on the page.](/static/8aa5a4edf59b4d650e6c1c77e5e05f6f/a5df1/search-do-fixed.png)

Do align the default search container vertically with other text on the page.

![Do hang the fluid search container with other hanging components.](/static/565fe5c59b09e12ac23fbbb856618b49/a5df1/search-do-fluid.png)

Do hang the fluid search container with other hanging components.

## Content

### Main elements

#### Placeholder text

Useful and short text hinting at what the user can search for. For example,
“Search for networks or devices.”

#### Field text

- Key words entered by the user to find a search result.
- Keep the field text concise and relate the field text as closely to the result
  you want to find.

### Further guidance

For further content guidance, see Carbon’s
[content guidelines](https://carbondesignsystem.com/guidelines/content/overview/).

## Behaviors

### States

The search component has four states: enabled, focus, filled, and disabled.

- Default
- Fluid

![Default search states](/static/86adeb9ed24513be9c795e3f1aa87810/3cbba/search-states-fixed.png)

![Fluid search states](/static/f4d8d0660ab42194af6620df026d8ce1/3cbba/search-states-fluid.png)

### Interactions

#### Mouse

Click on the search field input to start typing. Once a user starts typing, a
close icon (‘x’) will appear and provides a way to clear the input field by
clicking on the Close icon.

#### Keyboard

Press

```
Enter
```

Copy to clipboard

to submit text as a search term, or press

```
Esc
```

Copy to clipboard

to clear the
search field. Once a user starts typing, a Close icon (‘x’) will appear and
provides a way to clear the input field by pressing the

```
Space
```

Copy to clipboard

or

```
Enter
```

Copy to clipboard

keys.

- Default
- Fluid

![Default search click areas](/static/57c8123bb2b37970cae444a88948811f/3cbba/search-click-area-fixed.png)

![Fluid search click areas](/static/af73b4496cba0bacbd62d0c611517b5e/3cbba/search-click-area-fluid.png)

## Related

#### Components

- [Data table](https://carbondesignsystem.com/components/data-table/usage/)
- [UI shell header](https://carbondesignsystem.com/components/UI-shell-header/usage/)

#### Patterns

- [Filtering](https://carbondesignsystem.com/patterns/filtering/)
- [Search](https://carbondesignsystem.com/patterns/search-pattern/)

## Feedback

Help us improve this component by providing feedback, asking questions, and
leaving any other comments on
[GitHub](https://github.com/carbon-design-system/carbon-website/issues/new?assignees=&labels=feedback&template=feedback.md).

[Edit this page on GitHub](https://github.com/carbon-design-system/carbon-website/edit/main/src/pages/components/search/usage.mdx)

[Previous

Components: Radio button](/components/radio-button/usage/)

[Next

Search: Style](/components/search/style/)