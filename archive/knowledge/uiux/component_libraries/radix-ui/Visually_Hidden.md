# Visually Hidden

Source: https://www.radix-ui.com/primitives/docs/utilities/visually-hidden

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

# Visually Hidden

Hides content from the screen in an accessible way.

## Features

Visually hides content while preserving it for assistive technology.

## [Installation](#installation)

Install the component from your command line.

```
npm install @radix-ui/react-visually-hidden
```

## [Anatomy](#anatomy)

Import the component.

```
import { VisuallyHidden } from "radix-ui";

export default () => <VisuallyHidden.Root />;
```

## [Basic example](#basic-example)

Use the visually hidden primitive.

```
import { VisuallyHidden } from "radix-ui";

import { GearIcon } from "@radix-ui/react-icons";

export default () => (

<button>

<GearIcon />

<VisuallyHidden.Root>Settings</VisuallyHidden.Root>

</button>

);
```

## [API Reference](#api-reference)

### [Root](#root)

Anything you put inside this component will be hidden from the screen but will be announced by screen readers.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |

## [Accessibility](#accessibility)

This is useful in certain scenarios as an alternative to traditional labelling with `aria-label` or `aria-labelledby`.

Previous[Slot](/primitives/docs/utilities/slot)

[Edit this page on GitHub.](https://github.com/radix-ui/website/edit/main/data/primitives/docs/utilities/visually-hidden.mdx "Edit this page on GitHub.")