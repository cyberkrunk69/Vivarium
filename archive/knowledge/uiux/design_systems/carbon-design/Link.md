# Link

Source: https://carbondesignsystem.com/components/link/usage/

---

# Link

Links are used as navigational elements. They navigate users to another
location, such as a different site, resource, or section within the same page.

- [Live demo](#live-demo)
- [Overview](#overview)
- [Formatting](#formatting)
- [Content](#content)
- [Universal behaviors](#universal-behaviors)
- [Standalone link](#standalone-link)
- [Inline link](#inline-link)
- [Modifiers](#modifiers)
- [Related](#related)
- [Reference](#reference)
- [Feedback](#feedback)

## Live demo

Theme selector

White

---

Variant selector

Default

---

This live demo contains only a preview of functionality and styles available for this component. View the [full demo](https://react.carbondesignsystem.com/?path=/story/components-link--default&globals=theme:white) on Storybook for additional information such as its version, controls, and API documentation.

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

Links are used as navigational elements and can be used on their own or inline
with text. They provide a lightweight option for navigation, but like other
interactive elements, too many links will clutter a page and make it difficult
for users to identify their next steps. This is especially true for inline
links, which should be used sparingly.

### When to use

Use links when you want users to:

- Navigate to a different page within the application
- Navigate to an entirely different site
- Jump to an element on the same page
- Link to emails or phone numbers

### When not to use

Do not use links for actions that will change data or manipulate how it is
displayed, change a state, or trigger an action. Instead, use
[buttons](https://carbondesignsystem.com/components/button/usage/) to guide
users to specific actions.

Do not use images as links. Instead, use a
[tile](https://carbondesignsystem.com/components/tile/usage/) that can contain
an image and additional information such as links.

### Variants

| Variant | Usage |
| --- | --- |
| [Standalone](#standalone-link) | Used on their own or directly following content and do not use underlines. They can be paired with an icon. |
| [Inline](#inline-link) | Used within a sentence or paragraph and is styled with an underline. They should not be paired with an icon. |

## Formatting

### Anatomy

![Link anatomy image](/static/0b6e034078c86427d509d86931ed1f46/3cbba/link-usage-anatomy.png)

1. **Link text:** Communicates what is being linked to.
2. **Icon (optional)** Indicates the destination or type of content being.
   referenced

### Sizing

There are three size variants for the link component: small, medium, and large.
Inline link sizes should match the type size of the text it is inline with.
Standalone link sizes should match the default body copy size of the page.

| Size | Height (px / rem) |
| --- | --- |
| Small | 16 / 1 |
| Medium | 18 / 1.125 |
| Large | 22 / 1.375 |

![Sizing applies to both standalone and inline links](/static/dd11bf8164e73560a7fea9ffd3105575/3cbba/link-usage-size.png)

Sizing applies to both standalone and inline links

### Placement

Inline links usually sit within a sentence or paragraph, while standalone links
can sit on their own, separated from other text. Consider reducing the number of
inline links in a single sentence to simplify the message.

![Example of inline link in a notification](/static/e71f2d5de49d9519ec7051b43289bae8/3cbba/link-usage-placement-1.png)

Example of inline link in a notification

![Example of standalone link in a card](/static/88903c1c6218d0f65190b9aef932a70d/3cbba/link-usage-placement-2.png)

Example of standalone link in a card

## Content

#### Link text

- Use distinctive and meaningful link text.
- Ensure that links accurately reflect the content users will find at the link
  destination.
- If your design uses generic link names such as “read more,” consider making
  them unique. See the
  [Accessibility](https://carbondesignsystem.com/components/link/accessibility#ensure-link-context)
  tab for more information.
- Avoid using the same link text for different destinations on the same page and
  try to differentiate between links by using unique text for each.
- Ensure links are understandable but not excessively long, especially if they
  wrap.

#### Icon indicator

Use the appropriate icon to convey the link destination. It’s common to use the
“launch” icon for external links and the “arrow right” icon for internal links.
Whatever icons you choose to use, ensure that the same icons are used
consistently for navigating to or launching new pages.

### Further guidance

For further content guidance, see Carbon’s
[Content guidelines](https://carbondesignsystem.com/guidelines/content/overview/).

## Universal behaviors

## States

List has six main states – enabled (unvisited), hover, focus, active, visited,
and disabled. Learn more about states on the
[Style](https://carbondesignsystem.com/components/link/style) tab.

| State | When to use |
| --- | --- |
| Enabled (unvisited) | This is the default state of a link. When the user has not clicked on a link yet. |
| Hover | When the user hovers the cursor over a link. |
| Focus | When the user tabs to or clicks on the link, it becomes focused, indicating the user has successfully navigated to the component. |
| Active | When the user is clicking on a link. |
| Visited | When the user has previously clicked on unvisited links. There’s a change in the color token as ```  $link-visited ```   Copy to clipboard . |
| Disabled | When a user cannot interact with the link. Links could be temporarily inactive or unavailable. |

### Interactions

#### Mouse

Users can open a link by clicking anywhere on the link text or on the associated
icon.

#### Keyboard

Users can open a link by pressing

```
Enter
```

Copy to clipboard

while the link has focus. For
additional keyboard interactions, see the
[Accessibility](https://carbondesignsystem.com/components/link/accessibility#keyboard-interactions)
tab.

### Responsive behavior

Clicking or activating on a link can:

- Open up a modal with read-only information
- Navigate the user to a new page, changing the URL and causing a browser
  refresh
- Support jumps to different sections within the same page
- Open web resources such as images, videos, or HTML documents

### Clickable areas

Both standalone and inline links are clickable across the entire width of the
text. Standalone link with an icon has an expanded clickable area that includes
the icon.

![Standalone and inline links with their clickable areas](/static/a5edb31f33265a5761f5b55603eb244d/3cbba/link-usage-clickable.png)

Standalone and inline links with their clickable areas

## Standalone link

Standalone links are used on their own directly following content. They should
not be used within sentences or paragraphs. Standalone links are the default
link style for Carbon and only have an underline in the hover state, focus
state, and active state.

The standalone link component can be paired with an icon. Icons should always be
the same color as the link text. When necessary, utilize appropriate icons to
distinguish them from ghost buttons or inline links when they appear within the
same context or page.

![Example shows the standalone link within context](/static/2d8fdb7276309944c7437de5af549512/3cbba/link-usage-standalone.png)

Example shows the standalone link within context

### Inline link

Inline links are used in sentences or paragraphs of text. The inline link
behaves the same as the standalone link but it is styled with an underline. This
helps differentiate them from the text they are placed next to and makes it
clear users can interact with them.

Inline links should not be used on their own and should not be paired with
icons.

![Example shows inline links within the body text](/static/372a558f8264b264df37d174b7f45b81/3cbba/03_link_inline_608.png)

Example shows inline links within the body text

## Modifiers

### Visited style

By default, the link component does not use a visited style. Visited links
indicate that a user has already opened the link so they can be a helpful
indicator during task completion. Visited styles should be used sparingly
because they often clutter the page and add further visual noise as users are
trying to navigate a product. They can be used to show users they have already
clicked on a link if it’s important.

![Example shows unvisited and visited links](/static/6d11b7da89dadd9b7fb41cb020d0501e/3cbba/link-usage-modifiers-1.png)

Example shows unvisited and visited links

### Links that trigger actions

Some links trigger actions to aid task completion in addition to navigation.
These links should still serve a navigation purpose. A common example is linking
phone numbers, so clicking the website automatically opens and calls the phone
number when clicked. The link text and any accompanying icons should clarify
what action will be triggered and where the user will be directed.

![Example shows inline links for email](/static/041dd092dbb97a81a2eecd61b96e1847/3cbba/link-usage-modifiers-2.png)

Example shows inline links for email

![Do use links when actions navigate users to resources](/static/a98294d6a70a3ac4af18b2381807069d/a5df1/link-usage-modifiers-do.png)

Do use links when actions navigate users to resources

![Do not use buttons when actions serve as a navigation purpose](/static/c7ee23a9bdcf62d2bb20d1cd5d2bf153/a5df1/link-usage-modifiers-dont.png)

Do not use buttons when actions serve as a navigation purpose

### Link grouping

**Code unavailability** The following specs are not developed for the link
component but are recommended by design as the proper distance between grouped
links. View the [Style](https://carbondesignsystem.com/components/link/style/)
tab for details.

Links can be grouped horizontally or vertically. One variation displays links in
a horizontal row with an icon and is typically used within the main body of the
page. Vertical links are typically used for resource links on the side of the
main page content or additional links in tiles.

![Example shows horizontal and vertical grouping of links](/static/70aaba55c42eb11c0f97e9923672a6f6/3cbba/link-usage-grouping.png)

Example shows horizontal and vertical grouping of links

## Related

#### Button

Buttons are used to initialize an action. Button labels express what action will
occur when the user interacts with it. For further guidance, see Carbon’s
[button](https://www.carbondesignsystem.com/components/button/usage/).

#### Tile

Tiles are a highly flexible component for displaying a wide variety of content,
including information, getting started, how-to, next steps, and more. For
further guidance, see Carbon’s
[tile](https://carbondesignsystem.com/components/tile/usage/).

## Reference

Jakob Nielsen,
[Guidelines for Visualizing Links](https://www.nngroup.com/articles/guidelines-for-visualizing-links/),
(Nielsen Norman Group, 2004)

## Feedback

Help us improve this component by providing feedback, asking questions, and
leaving any other comments on
[GitHub](https://github.com/carbon-design-system/carbon-website/issues/new?assignees=&labels=feedback&template=feedback.md).

[Edit this page on GitHub](https://github.com/carbon-design-system/carbon-website/edit/main/src/pages/components/link/usage.mdx)

[Previous

Components: Inline loading](/components/inline-loading/usage/)

[Next

Link: Style](/components/link/style/)