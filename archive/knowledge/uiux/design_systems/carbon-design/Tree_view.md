# Tree view

Source: https://carbondesignsystem.com/components/tree-view/usage/

---

# Tree view

Feature flag

A tree view is a hierarchical structure that provides nested levels of
navigation.

- [Live demo](#live-demo)
- [Overview](#overview)
- [Formatting](#formatting)
- [Content](#content)
- [Behaviors](#behaviors)
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

This live demo contains only a preview of functionality and styles available for this component. View the [full demo](https://react.carbondesignsystem.com/?path=/story/components-treeview--default&globals=theme:white) on Storybook for additional information such as its version, controls, and API documentation.

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

A tree view consists of nested heading levels that create a content hierarchy
for users and assist with navigating large amounts of information. Following on
with the tree analogy, the tree view component has branch nodes that can be
expanded or collapsed to reveal or hide child nodes. The tree may also have leaf
nodes. Leaf nodes can appear at any level of the tree hierarchy and do not have
child nodes.

![Example of tree view with node icons](/static/139960bb76a2a46e5d165f73d5ba2152/3cbba/tree-view-usage-0.png)

### When to use

- Often used for navigating file system structures that are made up of folders
  and documents.
- To organize large amounts of information that can nest within multiple levels.

### When not to use

- To show and hide UI elements or content on a page.
- When you only need one level of nested information. In this case, use a
  different component like the [accordion](/components/accordion/usage/) or
  [data table](/components/data-table/usage/) for expandable views that go one
  level deep.
- As the primary navigation in a product’s UI. Instead, use the UI Shell left
  panel for product navigation. A combination of the
  [UI shell left panel](/components/UI-shell-left-panel/usage/) and the
  [breadcrumb](/components/breadcrumb/usage/) component can support an
  information architecture several levels deep.

### Feature flags

A [feature flag](/components/overview/feature-flags/) has been added to tree
view to improve accessibility and changes parts of its functionality, not its
visual appearance. For code-specific feature flag information, refer to the
[Code](/components/tree-view/code/) tab. The current tree view is not being
deprecated, but teams are encouraged to use the feature flag tree view for their
products moving forward. Once the next major release (v12) is released in the
future, this feature flag will become the default version of the component.

## Formatting

### Anatomy

The tree view is composed of branch and leaf nodes that are designed to nest and
organize large sets of information.

![Anatomy of tree view](/static/b9c6f5693c7ecfb0f627cdcde57e76f1/3cbba/tree-view-usage-1.png)

1. **Branch node**: A node that has one or more child nodes. Can be expanded or
   collapsed to reveal or hide child nodes.
2. **Leaf node**: A node that has no child nodes and can appear at any level of
   the tree view hierarchy. A leaf node may be referred to as a child node when
   it is nested underneath a branch node.
3. **Caret icon**: An icon to expand or collapse a branch node.
4. **Node icon** (optional): An icon to visually represent and support a node
   label, they can assist the user to scan different content types quickly.

### Sizing

There are two node sizes: small (default), and extra small. Supporting two
different node sizes gives you more flexibility when structuring a tree view. If
you have a tree structure with complex nesting levels, use the extra small node
size to keep as much information in view as possible. When in doubt of which
size to use, use the small node size because it is our default.

| Node size | Height (px/rem) | Purpose |
| --- | --- | --- |
| *Small* | 32 / 2 | This is the default size and is the most commonly used as it has similar geometries as the UI shell left navigation panel. |
| *Extra small* | 24 / 1.5 | Use when space is constricted on the page and/or when you need a more condensed view to show more of the tree view on the screen. |

![Size comparison of the two nodes](/static/a11aff0ab6bbeade8354d3d19be481e3/3cbba/tree-view-usage-2.png)

### Alignment

#### Stacking nodes

Nodes stack directly on top of each other with 0px space between them. Having
nodes flush with each other ensures consistent spacing and alignment between
each node in the tree view.

![Examples of aligning stacking nodes](/static/6efb2b137252e09a10cd274cf7d6fd1b/3cbba/tree-view-usage-3.png)

#### Nesting nodes

Nested nodes in a tree view rely on vertical type and icon alignment to visually
group nodes together. Branch icons and leaf icons sit to the left of type and
align vertically.

![Example of aligning nesting nodes](/static/8fc7bb079b9b9f8df1388c979d19ef37/3cbba/tree-view-usage-4.png)

## Content

### Main elements

You may be able to label your nodes, or the labels may be generated from code.
If you have control of your label names, follow these guidelines.

#### Branch node label

Be brief but clear while summarizing what kind of child nodes the branch node
contains.

#### Leaf node label

Be brief and descriptive about what information the leaf node contains.

### Overflow content

If the node label is too long for one line in your tree view, add an ellipsis

```
…
```

Copy to clipboard

and accompany with a browser-based tooltip to show the full string of text.

While truncation is not preferred, you can customize the view by
[positioning](/patterns/overflow-content/#variations) the ellipsis at the
front-line, mid-line, or end-line of a node label depending on what information
is most useful to the user to keep persistent in the tree view.

![Example of overflowing content](/static/0365d4c70b0569cf2a1428f692fdbfa5/3cbba/tree-view-usage-5.png)

### Further guidance

For further content guidance, see Carbon’s
[content guidelines](/guidelines/content/overview/).

## Behaviors

### States

Branch nodes and leaf nodes share the same styles for different states. The only
difference between the structure of the two is the addition of a caret icon for
expanding or collapsing branch nodes.

![Example of node states](/static/99e6c5024b6522488bbb7d2cea472899/3cbba/tree-view-usage-6.png)

#### Selection indicator

If the branch node of a selected child node is collapsed, the parent node should
inherit the selected state so the user does not lose the context of what is
selected, even if it is out of view.

![Example of a selected node](/static/933e3ca85f6507362305c2b1abc223d3/3cbba/tree-view-usage-6b.png)

Example of selected child node when the parent is open (left) and when the
parent is collapsed (right).

### Interactions

#### Focus

When a single-select tree receives focus:

- Focus is set on the previously selected node.
- If none of the nodes were selected before the tree receives focus, focus is
  set on the first node.

#### Expanding and collapsing

- To expand or collapse a branch node the user can click anywhere within the
  caret icon bounding box.

![Example showing click target areas for a branch node](/static/d082f44d066b1cc72ad1b02101e27750/3cbba/tree-view-usage-7.png)

#### Selecting

- To select a branch node the user can click anywhere on the node excluding the
  caret icon bounding box.
- To select a leaf node the user can click anywhere on the node container.

![Example showing click target areas for selecting a node](/static/ae077e471c50eac16c55491746072d77/3cbba/tree-view-usage-8.png)

  

#### Keyboard controls

| Key | Interaction |
| --- | --- |
| *Right arrow* | When focus is on a closed node, opens the node; focus does not move. |
|  | When focus is on an open node, moves focus to the first child node. |
|  | When focus is on a leaf node, does nothing. |
| *Left arrow* | When focus is on an open node, closes the node. |
|  | When focus is on a child node that is also either a leaf node or a closed node, moves focus to its parent node. |
|  | When focus is on a top level node that is also either a leaf node or a closed node, does nothing. |
| *Down arrow* | Moves focus to the next node that is focusable without opening or closing a node. |
| *Up arrow* | Moves focus to the previous node that is focusable without opening or closing. |
| *Enter* | Activates a node. In single-select trees where selection does not follow focus, the default action is typically to select the focused node. |

## Modifiers

### Node icons

You can add node icons to visually represent and support a written node label.
We recommend having consistent icon usage for all branch and leaf nodes. Make
sure the icons accurately represent each node that they are related to. Using a
folder icon for branch nodes and a document icon for leaf nodes is a commonly
recognized pairing of icons used in tree view structures. If individual node
data cannot be identified, do not display icons. When in doubt, use nodes
without icons.

![Example of tree view with node icons](/static/8ce41c79409c9f0155c7577f74cfa674/3cbba/tree-view-usage-9.png)

#### Aligning icons

It is important when adding icons to nodes in a tree view that there is an icon
present for every node. Not having an icon for every branch or leaf node can
cause alignment inconsistencies and make groupings of nodes harder to visualize.

![Example of node icons used correctly in tree](/static/1e33b3652c2d78a358248902f8f0c94f/a5df1/tree-view-usage-do-10a.png)

Do consistently use icons for each node in a tree view.

![Incorrect example showing only some nodes using icons.](/static/6ee14165881b2701a0c3419b5cc6dd13/a5df1/tree-view-usage-dont-10b.png)

Do not mix text-only and icon nodes in a tree view.

## Related

#### Tree view versus accordion

Use the [accordion](/accordion/usage/) component when you need to organize
lengthy information in sections that only go one level deep. Tree view is best
used for nesting categories of information in a hierarchy of multiple levels /
in a hierarchical form.

#### Tree view versus UI Shell left panel

Use the [UI Shell left panel](/UI-shell-left-panel/usage/) component for product
navigation. A combination of the UI Shell left panel and the
[breadcrumb](/components/breadcrumb/usage/) component can support an information
architecture several levels deep of a product. Tree view is best used for on
page navigation instead of being used for architecture of a website or product.

#### Tree view versus data table

Use the [data table](/components/data-table/usage/) component for displaying
large amounts of detailed information that is easy to scan horizontally in one
view. Data table rows can be expanded, but we recommend only expanding a row one
level deep. Tree view is used to organize multiple nested levels of information
with concise labels that do not need to be organized in a column structure.

## References

- [Tree](https://www.w3.org/TR/aria-role/roles#tree) (W3C Recommendation)
- [TreeView](https://www.w3.org/wiki/TreeView) (W3C Wiki 2012)
- [Tree view React app](https://pages.github.ibm.com/conrad-schmidt/Tree/) (WKC)
- [Tree view specifications](https://ibm.ent.box.com/s/azascty1rmgik858zy1kw3cw6f0a4zo1)
  (WKC)
- [Tree view WAI-ARIA practices](https://www.w3.org/TR/wai-aria-practices/#TreeView)
  (W3C)

## Feedback

Help us improve this component by providing feedback, asking questions, and
leaving any other comments on
[GitHub](https://github.com/carbon-design-system/carbon-website/issues/new?assignees=&labels=feedback&template=feedback.md).

[Edit this page on GitHub](https://github.com/carbon-design-system/carbon-website/edit/main/src/pages/components/tree-view/usage.mdx)

[Previous

Components: Tooltip](/components/tooltip/usage/)

[Next

Tree view: Style](/components/tree-view/style/)