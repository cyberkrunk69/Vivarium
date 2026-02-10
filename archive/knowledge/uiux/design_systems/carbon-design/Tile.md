# Tile

Source: https://carbondesignsystem.com/components/tile/usage/

---

# Tile

Feature flag

Tiles are a highly flexible component for displaying a wide variety of content,
including information, getting started, how-to, next steps, and more.

Tile
[with AI label](https://react.carbondesignsystem.com/?path=/story/components-tile--with-ai-label)
changes the visual appearance of the component and introduces an AI
explainability feature when AI is present in the component.

- [Live demo](#live-demo)
- [Overview](#overview)
- [Variants](#variants)
- [Formatting](#formatting)
- [Content](#content)
- [Base](#base)
- [Clickable](#clickable)
- [Selectable](#selectable)
- [Expandable](#expandable)
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

This live demo contains only a preview of functionality and styles available for this component. View the [full demo](https://react.carbondesignsystem.com/?path=/story/components-tile--default&globals=theme:white) on Storybook for additional information such as its version, controls, and API documentation.

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

Tile is a component that can contain various content and nested components and
can have interactive functions. Tile is often laid out in groups, is a different
color than the UI background, and responds to the grid. Tiles have no pre-set
styles and are purposely flexible so product teams can determine their tile
content for specific use cases.

![Example of the tile component in a UI](/static/f54982885ff280cc5f85ef6466db8328/3cbba/tile-usage-overview.png)

Example of the tile component in a UI

#### Tiles versus cards

Tiles are simple and foundational. Cards can be very complex. Cards are built
upon the tile foundation and have various patterns of information hierarchy,
multiple actions, overflow menus, selectable features, etc. Carbon does not have
a card pattern, but we link out to several card patterns within our pattern
asset library (PAL) ecosystem below:

- [Productive versus Expressive cards](https://pages.github.ibm.com/cdai-design/pal/components/card/overview/)
  (Carbon for IBM Products)
- [Dashboard cards](https://pages.github.ibm.com/ai-applications/design/patterns/dashboards-v2/overview/#dashboard-cards)
  (IBM Sustainability Software Design)
- [Cards](https://www.ibm.com/standards/carbon/components/cards) (Carbon for
  IBM.com)

### When to use

Tiles are reusable components that provide shortcuts to building cards and other
modules. Use tiles to group related information in flexible containers. Here are
some common use cases for when to use tiles:

- To contain related groupings of information or actions
- To guide users to take actions or navigate
- To present options for single or multiple selections
- To hide or show large amounts of content

### When not to use

Tiles reside on the same plane as the page background layer and do not have
elevation. Tiles organize essential information and have the same visual
hierarchy as content on the same page.

Do not add a drop shadow to tiles and use them to reveal secondary information,
actions, or notifications. Use [modals](/components/modal/usage),
[popovers](/components/popover/usage), and
[dialogs](https://carbondesignsystem.com/patterns/dialog-pattern/) that have
elevation and are appropriate for this use case instead.

### Variants

Tiles can have different functions and are implemented in four ways: base,
clickable, selectable, and expandable. These tile variants are flexible to
support various use cases when building more complicated card features.

| Variant | Purpose |
| --- | --- |
| [Base](#base) | For high-level, short, and digestible content pieces such as features, plans, or services offered. |
| [Clickable](#clickable) | For prompting an action, navigating or directing to other pieces of information about the subject matter. This variant has an available feature flag. |
| [Selectable](#selectable) | For presenting options to a user in a structured manner, such as a set of pricing plans. This variant has available feature flags. |
| [Expandable](#expandable) | For hiding and revealing a large amount of content to focus on specific pieces of information. This variant has an available feature flag. |

### Feature flags

[Feature flags](/components/overview/feature-flags/) have been added to the
clickable, selectable, and expandable variants of tile to improve accessibility
and changes its visual appearance, not its functionality. For code-specific
feature flag information, refer to the [Code](/components/tile/code/) tab. These
current variants of tile are not being deprecated, but teams are encouraged to
use the feature flag tile for their products moving forward. Once the next major
release (v12) is released in the future, these feature flags will become the
default version of the component.

The following are the feature flag changes made to tile.

- A border has been added to the clickable, selectable, and expandable variants
  of tile to visually indicate they are operable.
- Single-select tile icons have been changed from checkmark icons to radio
  button icons, where as multi-select tile icons have been changed from
  checkmark icons to checkbox icons. These icons appear in the enabled state
  instead of only on hover before making a selection.

- Flag enabled
- Flag disabled

![Interactive tiles with the feature flag enabled](/static/11a834e65091fb57ac36e51cdc512b0f/3cbba/tile-usage-feature-flag-enabled.png)

![Interactive tiles with the feature flag disabled](/static/5dff26143540bbf684b7ef0910da710a/3cbba/tile-usage-feature-flag-disabled.png)

## Formatting

### Sizing

Tile width varies depending on the three basic gutter modes: **wide**,
**narrow**, and **condensed**. Tile height varies depending on the content
placed within it while using
[spacing tokens](https://carbondesignsystem.com/elements/spacing/overview/) and
following
[aspect ratios](https://carbondesignsystem.com/elements/2x-grid/usage/#continuity).
The minimum tile height is a 2:1 aspect ratio. As the content grows, set
vertical spacing between sections within the content area.

### Alignment

#### Tile groups

Tile groups are helpful when aligning tiles that have a strong relationship.
Tile groups usually flow horizontally from left to right and have hierarchical
importance, similar to navigation or catalog tiles.

![Example image of tiles on the wide grid](/static/1d9558f804c8f51926cef86f06882c22/3cbba/tile-usage-wide-grid.png)

Example image of tiles on the wide grid

![Example image of tiles on the narrow grid](/static/bfd0f56814949ae98099bb3d52380930/3cbba/tile-usage-narrow-grid.png)

Example image of tiles on the narrow grid

![Example image of tiles on the condensed grid](/static/118d07a7921045dcf4707b3ca285b3d7/3cbba/tile-usage-condensed-grid.png)

Example image of tiles on the condensed grid

![Example of "do" of tile matching](/static/590d51b2056638465cc48394064b0290/6e9cd/tile-usage-group-do.png)

Do match the tile variants in groups.

![Example of "do not" of tile mixing](/static/9974a971593ed06af0d3db9d6aa10dab/6e9cd/tile-usage-group-dont.png)

Do not mix different variants of tiles in groups.

#### Layout

There are three basic layouts for tiles: **standard**, **vertical masonry**, and
**horizontal masonry**. The standard layout is the the most commonly used.

- In a standard layout, tiles are the same in height and width as all other
  tiles in the group.
- In a vertical masonry layout, tiles can vary in height, but are consistent in
  width.
- In a horizontal masonry layout, tiles can vary in width; different rows of
  tiles may vary in height, but tiles within a row should be consistent in
  height.

![Tile layouts](/static/22acc83f052e9993ee2615a1cefcf1bd/3cbba/tile-usage-18.png)

Examples of standard, vertical masonry, and horizontal masonry tile layouts

## Content

### Main elements

#### Tile text

Tile text can vary based on the content. It can consist of heading text, body
text, label text, and include interactive elements.

### Further guidance

For further content guidance, see
Carbon’s [content guidelines](https://carbondesignsystem.com/guidelines/content/overview/).

## Base

Base tiles are used to display information to the user, such as features or
services offered. Base tiles are often seen on marketing pages to promote
content or on highly interactive dashboards. These tiles can have internal
calls-to-action (CTAs), such as a [buttons](/components/button/usage) or
[links](/components/link/usage).

![Example of base tiles](/static/e1bdc5d773f9a48a2275acd4e1017f4b/3cbba/tile-usage-base.png)

Example of base tiles

### Anatomy

![Anatomy of base tiles](/static/3a5a88e3ecb4d22f33aea72990f70cb5/3cbba/tile-usage-base-anatomy.png)

Anatomy of base tiles

1. **Container**: Contains all content in a tile.
2. **Text**: The text in a tile.
3. **Interactive elements (optional)**: Elements like links or buttons in a tile
   that are interactive.

### Alignment

When placing interactive elements within base tiles, place links at the bottom
left of the tile and span buttons in width at the bottom to indicate
call-to-action items.

![Example of "do" on base tile](/static/94fcceed8e3568b225e47c2721c16710/a5df1/tile-usage-base-link-do.png)

Do left align the link at the bottom of the base tile.

![Example of "do" on base tile](/static/34112a6fddaf3a828cbc7a9b0498e7d2/a5df1/tile-usage-base-button-do.png)

Do span the button in width at the bottom of the base tile.

### States

Base tiles only have an **enabled** state because they are not operable by a
mouse or keyboard. For more information about base tile states, see the
[Style](https://carbondesignsystem.com/components/tile/style) tab.

### Interactions

#### Mouse

Base tiles are not operable by a mouse unless they contain interactive elements
within them. Interactive elements can be clicked on and activated.

#### Keyboard

- Base tiles do not receive focus unless they contain interactive elements.
- ```
  Tab
  ```

  Copy to clipboard

  moves focus forward through interactive elements within base tile in a
  logical order.
- ```
  Shift
  ```

  Copy to clipboard

  +

  ```
  Tab
  ```

  Copy to clipboard

  moves focus backward through interactive elements within base
  tile in a logical order.
- ```
  Enter
  ```

  Copy to clipboard

  activates the base tiles interactive elements.

### Clickable areas

Base tiles can have interactive elements within them, like links or buttons,
which can be clicked on.

![Clickable areas of base tile with interactive elements](/static/43e089be502eb20cddbd36eb34db6378/3cbba/tile-usage-base-clickable-areas.png)

Clickable areas of base tile with interactive elements

## Clickable

Clickable tiles can be used as navigational elements that redirect the user to a
new page. In these situations, the entire tile is in a clickable state. Due to
accessibility concerns, clickable tiles cannot contain separate internal CTAs
but can contain pictograms, icons, or media such as illustrations or images.

Clickable tile has an available
[feature flag](/components/overview/feature-flags/).

- Flag enabled
- Flag disabled

![Clickable tile with the feature flag enabled](/static/bc58c0edd2c56cd49f4e2e634889ddab/3cbba/tile-usage-clickable-flag-enabled.png)

![Clickable tile with the feature flag disabled](/static/1a3474cbba5f692c18c865ade1355b90/3cbba/tile-usage-clickable-flag-disabled.png)

### Anatomy

![Anatomy of clickable tile with the feature flag enabled](/static/2206108cbd74b032cf1f54dad7228834/3cbba/tile-usage-clickable-anatomy.png)

Anatomy of clickable tile with the feature flag enabled

1. **Container**: Contains all content within a tile.
2. **Text**: The text within a tile.
3. **Icon**: The icon that visually indicates the tile is navigational.
4. **Border**: The border that visually indicates the tile is interactive.

### Alignment

#### Icons

On clickable tiles, use the arrow icon paired with the

```
$icon-interactive
```

Copy to clipboard

color
token. Place the icon at the bottom right to indicate navigation. Avoid
confusing the user with multiple click targets, like interactive links or
buttons, since the whole tile is already clickable.

![Example of "do" on clickable tile](/static/4fa4741f99fe0ba4e90eb9c2c29ab2a0/a5df1/tile-usage-clickable-arrow-do.png)

Do right align the arrow icon when it is by itself.

![Example of "do" on clickable tile](/static/379645ad5360828df1ffb54cab6f81af/a5df1/tile-usage-clickable-arrow-pdf-do.png)

Do right align the arrow icon when there is additional text.

![Example of "do" on clickable tile](/static/28a2ba69cbcb0aa070c583d7e1b5bb0a/a5df1/tile-usage-clickable-arrow-pictogram-do.png)

Do right align the arrow icon when there is a decorative icon or pictogram.

![Example of "do not" on clickable tile](/static/f88d015fe08c9ab3884259247f4649c9/a5df1/tile-usage-clickable-link-dont.png)

Do not add interactive links or components on clickable tiles.

### States

Clickable tiles have **enabled**, **hover**, **focus**, and **disabled** states.
For more information about clickable tile states, see the
[Style](https://carbondesignsystem.com/components/tile/style) tab.

### Interactions

#### Mouse

The clickable tile is triggered by clicking anywhere within the tile container.

#### Keyboard

- ```
  Tab
  ```

  Copy to clipboard

  moves focus forward through clickable tiles in a logical order.
- ```
  Shift
  ```

  Copy to clipboard

  +

  ```
  Tab
  ```

  Copy to clipboard

  moves focus backward through clickable tiles in a logical
  order.
- ```
  Enter
  ```

  Copy to clipboard

  activates the tile and navigates you to its destination.

### Clickable areas

Clickable tiles can be triggered by clicking anywhere on the tiles container.

![Clickable areas of clickable tile with the feature flag enabled](/static/19bc657386e980ca29407d6d067ee929/3cbba/tile-usage-clickable-clickable-areas.png)

Clickable areas of clickable tile with the feature flag enabled

## Selectable

Selectable tiles are used to present different options for users to select from.
Selectable tiles can contain internal CTAs, like links to documentation, if the
CTA is given a click target of its own in addition to the tile’s click target.
Selectable tiles can either have single-selection or multi-selection.

Selectable tile has available
[feature flags](/components/overview/feature-flags/).

### Single-select

Use single-select tiles when the user can only select one tile from a tile
group.

- Flag enabled
- Flag disabled

![Single-select tile with the feature flag enabled](/static/f39da855a77208b08e337003c3cf043d/3cbba/tile-usage-selectable-single-select-flag-enabled.png)

![Single-select tile with the feature flag disabled](/static/4b19ee17d63eccdd463a8d6ed478d640/3cbba/tile-usage-selectable-single-select-flag-disabled.png)

### Multi-select

Use multi-select tiles when the user can select multiple tiles from a tile
group.

- Flag enabled
- Flag disabled

![Multi-select tile with the feature flag enabled](/static/d91e1a054f1ec5bb7f49712570718533/3cbba/tile-usage-selectable-multi-select-flag-enabled.png)

![Multi-select tile with the feature flag disabled](/static/f437e37d67dfb9e1ba37b4ab3bb38a13/3cbba/tile-usage-selectable-multi-select-flag-disabled.png)

### Anatomy

![Anatomy of selectable tile with feature flags](/static/af74d15bda1e5d310d3510ce0b1e5d11/3cbba/tile-usage-selectable-anatomy.png)

Anatomy of selectable tile with the feature flags enabled

1. **Container**: Contains all content within a tile.
2. **Text**: The text within a tile.
3. **Icon**: The radio or checkbox icon that visually indicates the tile is
   selectable.
4. **Border**: The border that visually indicates the tile is interactive.

### States

Selectable tiles have **enabled**, **hover**, **hover selected**, **selected**,
**focus**, and **disabled** states. For more information about base tile states,
see the [Style](https://carbondesignsystem.com/components/tile/style/) tab.

### Interactions

#### Mouse

The clickable tile is triggered by clicking anywhere within the tile container.

#### Keyboard

- ```
  Tab
  ```

  Copy to clipboard

  moves focus forward through selectable tiles in a logical order.
- ```
  Shift
  ```

  Copy to clipboard

  +

  ```
  Tab
  ```

  Copy to clipboard

  moves focus backward through selectable tiles in a logical
  order.
- ```
  Enter
  ```

  Copy to clipboard

  selects the tile.

### Clickable areas

Selectable tiles can be selected by clicking anywhere on the tiles container.

![Clickable areas of selectable tile with the feature flags enabled](/static/fe225a16974fe5a19567a37a515c228a/3cbba/tile-usage-selectable-clickable-areas.png)

Clickable areas of selectable tile with the feature flags enabled

### Expandable

Expandable tiles are used to reveal or hide additional information to the user
and can be expanded and collapsed differently depending on their content. If an
expandable tile does not have interactive elements, clicking anywhere in the
tile expands and collapses the tile. If an expandable tile has interactive
elements, the chevron icon button expands and collapses the tile.

Expandable tile has an available
[feature flag](/components/overview/feature-flags/).

### Without interactive elements

Use the container expansion functionality to expand and collapse the tile when
there are no interactive elements.

- Flag enabled
- Flag disabled

![Expandable tile without interactive elements with the feature flag enabled](/static/9d682bf5652d7c2cb75d9c2bd8e9adc0/3cbba/tile-usage-expandable-non-interactive-flag-enabled.png)

![Expandable tile without interactive elements with the feature flag disabled](/static/4354c3088f9db8e2cbdaacaa7cfc3291/3cbba/tile-usage-expandable-non-interactive-flag-disabled.png)

### With interactive elements

Use the button expansion functionality to expand and collapse the tile when
including interactive elements.

- Flag enabled
- Flag disabled

![Expandable tile with interactive elements with the feature flag enabled](/static/68f66b33ce3db88c2f8e4e66d1567e68/3cbba/tile-usage-expandable-interactive-flag-enabled.png)

![Expandable tile with interactive elements with the feature flag disabled](/static/a618fc936b9ef8da185bc9c6f8aaa57c/3cbba/tile-usage-expandable-interactive-flag-disabled.png)

### Anatomy

![Anatomy of expandable tile with the feature flag enabled](/static/cdf29c3b46a5a043dcf15072159dc4fa/3cbba/tile-usage-expandable-anatomy.png)

Anatomy of expandable tile with the feature flag enabled

1. **Container**: Contains all content within a tile.
2. **Text**: The text within a tile.
3. **Interactive elements (optional)**: Interactive elements like links or
   buttons placed within a tile.
4. **Icon**: The icon that visually indicates the tile is expandable.
5. **Border**: The border that visually indicates the tile is interactive.

### States

Expandable tiles have **enabled**, **hover**, **focus**, and **disabled**
states. For more information about expandable tile states, see the
[Style](https://carbondesignsystem.com/components/tile/style/) tab.

### Interactions

#### Mouse

- Without interactive elements: The tile is expanded by clicking anywhere within
  the tile container.
- With interactive elements: The tile is expanded by clicking on the button in
  the bottom right of the tile.

#### Keyboard

- ```
  Tab
  ```

  Copy to clipboard

  moves focus forward through tiles. If there are interactive elements,

  ```
  Tab
  ```

  Copy to clipboard

  moves focus forward in a logical order.
- ```
  Shift
  ```

  Copy to clipboard

  +

  ```
  Tab
  ```

  Copy to clipboard

  moves focus backward through tiles. If there are interactive
  elements,

  ```
  Tab
  ```

  Copy to clipboard

  moves focus forward in a logical order.
- ```
  Enter
  ```

  Copy to clipboard

  expands and collapses the tile.

### Clickable areas

If the expandable tile does not have interactive elements, it can be expanded or
collapsed by clicking anywhere on the tiles container. If the expandable tile
has interactive elements, it can be expanded or collapsed by clicking on the
button in the bottom right corner. Interactive elements within a tile can also
be clicked on and have their own click targets.

![Clickable areas of expandable tile with the feature flag enabled](/static/1fa6d3feffb65a8f0fca182d5a49d426/3cbba/tile-usage-expandable-clickable-areas.png)

Clickable areas of expandable tile with the feature flag enabled

## AI presence

Tile has a modification that takes on the AI visual styling when the AI label is
present in the container. The AI variants function the same as the normal
versions except with the addition of the AI label which is both a visual
indicator and the trigger for the explainability popover.

For more information on designing for AI, see the
[Carbon for AI](/guidelines/carbon-for-ai/) guidelines.

![Base, clickable, and selectable tiles with AI presence and feature flags enabled](/static/dd6721e604f28a5d87251025e0b88611/3cbba/tile-usage-AI-presence.png)

Base, clickable, and selectable tiles with AI presence and feature flags
enabled

## Related

#### Grid

To learn more about how to build tiles correctly on the grid, see Carbon’s
[2x grid](/elements/2x-grid/implementation).

#### Aspect ratio

The aspect ratio is important when building tiles and images. For further
guidance, see Carbon’s
[aspect ratio](https://www.carbondesignsystem.com/elements/2x-grid/overview/#aspect-ratio)
and its
[implementation](https://www.carbondesignsystem.com/elements/2x-grid/implementation#screen-regions).

#### Buttons

When in doubt, use full-span button alignment within tiles. For further
guidance, see Carbon’s
[buttons](https://carbondesignsystem.com/components/button/usage/).

#### Link

Link has variants depending on the context. For further guidance, see Carbon’s
[link](https://carbondesignsystem.com/components/link/usage/).

#### Spacing

Spacing helps deliver clear and functional layouts. For further guidance, see
Carbon’s [spacing](https://carbondesignsystem.com/elements/spacing/overview/).

## References

Hagan Rivers,
[Interactions design with cards/tiles](https://medium.com/@hagan.rivers/interaction-design-with-cards-tiles-5a6895aa220d/)
(Medium, 2017)

## Feedback

Help us improve this component by providing feedback, asking questions, and
leaving any other comments on
[GitHub](https://github.com/carbon-design-system/carbon-website/issues/new?assignees=&labels=feedback&template=feedback.md).

[Edit this page on GitHub](https://github.com/carbon-design-system/carbon-website/edit/main/src/pages/components/tile/usage.mdx)

[Previous

Components: Text input](/components/text-input/usage/)

[Next

Tile: Style](/components/tile/style/)