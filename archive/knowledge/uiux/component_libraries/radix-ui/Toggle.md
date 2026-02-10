# Toggle

Source: https://www.radix-ui.com/primitives/docs/components/toggle

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

Components

# Toggle

A two-state button that can be either on or off.

index.jsxindex.jsxstyles.cssstyles.css

```
import * as React from "react";

import { Toggle } from "radix-ui";

import { FontItalicIcon } from "@radix-ui/react-icons";

import "./styles.css";

const ToggleDemo = () => (

<Toggle.Root className="Toggle" aria-label="Toggle italic">

<FontItalicIcon />

</Toggle.Root>

);

export default ToggleDemo;

Expand code
```

## Features

Full keyboard navigation.

Can be controlled or uncontrolled.

## [Installation](#installation)

Install the component from your command line.

```
npm install @radix-ui/react-toggle
```

## [Anatomy](#anatomy)

Import the component.

```
import { Toggle } from "radix-ui";

export default () => <Toggle.Root />;
```

## [API Reference](#api-reference)

### [Root](#root)

The toggle.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |
| `defaultPressed` Prop description | `boolean` | No default value |
| `pressed` Prop description | `boolean` | No default value |
| `onPressedChange` Prop description | `function` See full type | No default value |
| `disabled` Prop description | `boolean` | No default value |

| Data attribute | Values |
| --- | --- |
| `[data-state]` | `"on" | "off"` |
| `[data-disabled]` | Present when disabled |

## [Accessibility](#accessibility)

### [Keyboard Interactions](#keyboard-interactions)

| Key | Description |
| --- | --- |
| `Space` | Activates/deactivates the toggle. |
| `Enter` | Activates/deactivates the toggle. |

Previous[Toast](/primitives/docs/components/toast)

Next[Toggle Group](/primitives/docs/components/toggle-group)

[Edit this page on GitHub.](https://github.com/radix-ui/website/edit/main/data/primitives/docs/components/toggle.mdx "Edit this page on GitHub.")