# Accessible Icon

Source: https://www.radix-ui.com/primitives/docs/utilities/accessible-icon

---

[Radix Homepage](/)[Made by WorkOS](https://workos.com)

[Radix Homepage](/)[Made by WorkOS](https://workos.com)

[ThemesThemes](/)[PrimitivesPrimitives](/primitives)[IconsIcons](/icons)[ColorsColors](/colors)

[Documentation](/primitives/docs)[Case studies](/primitives/case-studies)[Blog](/blog)

Search

`/`

#### Overview

[Introduction](/primitives/docs/overview/introduction)[Getting started](/primitives/docs/overview/getting-started)[Accessibility](/primitives/docs/overview/accessibility)[Releases](/primitives/docs/overview/releases)

#### Guides

[Styling](/primitives/docs/guides/styling)[Animation](/primitives/docs/guides/animation)[Composition](/primitives/docs/guides/composition)[Server-side rendering](/primitives/docs/guides/server-side-rendering)

#### Components

[Accordion](/primitives/docs/components/accordion)[Alert Dialog](/primitives/docs/components/alert-dialog)[Aspect Ratio](/primitives/docs/components/aspect-ratio)[Avatar](/primitives/docs/components/avatar)[Checkbox](/primitives/docs/components/checkbox)[Collapsible](/primitives/docs/components/collapsible)[Context Menu](/primitives/docs/components/context-menu)[Dialog](/primitives/docs/components/dialog)[Dropdown Menu](/primitives/docs/components/dropdown-menu)[Form

Preview](/primitives/docs/components/form)[Hover Card](/primitives/docs/components/hover-card)[Label](/primitives/docs/components/label)[Menubar](/primitives/docs/components/menubar)[Navigation Menu](/primitives/docs/components/navigation-menu)[One-Time Password Field

Preview](/primitives/docs/components/one-time-password-field)[Password Toggle Field

Preview](/primitives/docs/components/password-toggle-field)[Popover](/primitives/docs/components/popover)[Progress](/primitives/docs/components/progress)[Radio Group](/primitives/docs/components/radio-group)[Scroll Area](/primitives/docs/components/scroll-area)[Select](/primitives/docs/components/select)[Separator](/primitives/docs/components/separator)[Slider](/primitives/docs/components/slider)[Switch](/primitives/docs/components/switch)[Tabs](/primitives/docs/components/tabs)[Toast](/primitives/docs/components/toast)[Toggle](/primitives/docs/components/toggle)[Toggle Group](/primitives/docs/components/toggle-group)[Toolbar](/primitives/docs/components/toolbar)[Tooltip](/primitives/docs/components/tooltip)

#### Utilities

[Accessible Icon](/primitives/docs/utilities/accessible-icon)[Direction Provider](/primitives/docs/utilities/direction-provider)[Portal](/primitives/docs/utilities/portal)[Slot](/primitives/docs/utilities/slot)[Visually Hidden](/primitives/docs/utilities/visually-hidden)

Utilities

# Accessible Icon

Makes icons accessible by adding a label.

## Features

Quickly make any icon accessible by wrapping it and providing a meaningful label.

No visual difference, but announced correctly by screen readers.

## [Installation](#installation)

Install the component from your command line.

```
npm install @radix-ui/react-accessible-icon
```

## [Anatomy](#anatomy)

Import the component.

```
import { AccessibleIcon } from "radix-ui";

export default () => <AccessibleIcon.Root />;
```

## [API Reference](#api-reference)

### [Root](#root)

Contains the icon to make accessible.

| Prop | Type | Default |
| --- | --- | --- |
| `label*` Prop description | `string` | No default value |

## [Accessibility](#accessibility)

Most icons or icon systems come with no accessibility built-in. For example, the same visual **cross** icon may in fact mean **"close"** or **"delete"**. This component lets you give meaning to icons used throughout your app.

This is built with [Visually Hidden](/primitives/docs/utilities/visually-hidden).

Previous[Tooltip](/primitives/docs/components/tooltip)

Next[Direction Provider](/primitives/docs/utilities/direction-provider)

[Edit this page on GitHub.](https://github.com/radix-ui/website/edit/main/data/primitives/docs/utilities/accessible-icon.mdx "Edit this page on GitHub.")