# Direction Provider

Source: https://www.radix-ui.com/primitives/docs/utilities/direction-provider

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

# Direction Provider

Wraps your app to provide global reading direction.

## Features

Enables all primitives to inherit global reading direction.

## [Installation](#installation)

Install the component from your command line.

```
npm install @radix-ui/react-direction
```

## [Anatomy](#anatomy)

Import the component.

```
import { Direction } from "radix-ui";

export default () => <Direction.Provider />;
```

## [API Reference](#api-reference)

### [Provider](#provider)

When creating localized apps that require right-to-left (RTL) reading direction, you need to wrap your application with the `Direction.Provider` component to ensure all of the primitives adjust their behavior based on the `dir` prop.

| Prop | Type | Default |
| --- | --- | --- |
| `dir` Prop description | `enum` See full type | No default value |

## [Example](#example)

Use the direction provider.

```
import { Direction } from "radix-ui";

export default () => (

<Direction.Provider dir="rtl">{/* your app */}</Direction.Provider>

);
```

Previous[Accessible Icon](/primitives/docs/utilities/accessible-icon)

Next[Portal](/primitives/docs/utilities/portal)

[Edit this page on GitHub.](https://github.com/radix-ui/website/edit/main/data/primitives/docs/utilities/direction-provider.mdx "Edit this page on GitHub.")