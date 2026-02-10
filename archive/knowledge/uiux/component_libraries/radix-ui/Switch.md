# Switch

Source: https://www.radix-ui.com/primitives/docs/components/switch

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

# Switch

A control that allows the user to toggle between checked and not checked.

Airplane mode

index.jsxindex.jsxstyles.cssstyles.css

```
import * as React from "react";

import { Switch } from "radix-ui";

import "./styles.css";

const SwitchDemo = () => (

<form>

<div style={{ display: "flex", alignItems: "center" }}>

<label
				className="Label"
				htmlFor="airplane-mode"
				style={{ paddingRight: 15 }}
			>

Airplane mode

</label>

<Switch.Root className="SwitchRoot" id="airplane-mode">

<Switch.Thumb className="SwitchThumb" />

</Switch.Root>

</div>

</form>

);

export default SwitchDemo;

Expand code
```

## Features

Full keyboard navigation.

Can be controlled or uncontrolled.

## [Installation](#installation)

Install the component from your command line.

```
npm install @radix-ui/react-switch
```

## [Anatomy](#anatomy)

Import all parts and piece them together.

```
import { Switch } from "radix-ui";

export default () => (

<Switch.Root>

<Switch.Thumb />

</Switch.Root>

);
```

## [API Reference](#api-reference)

### [Root](#root)

Contains all the parts of a switch. An `input` will also render when used within a `form` to ensure events propagate correctly.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |
| `defaultChecked` Prop description | `boolean` | No default value |
| `checked` Prop description | `boolean` | No default value |
| `onCheckedChange` Prop description | `function` See full type | No default value |
| `disabled` Prop description | `boolean` | No default value |
| `required` Prop description | `boolean` | No default value |
| `name` Prop description | `string` | No default value |
| `value` Prop description | `string` | `on` |

| Data attribute | Values |
| --- | --- |
| `[data-state]` | `"checked" | "unchecked"` |
| `[data-disabled]` | Present when disabled |

### [Thumb](#thumb)

The thumb that is used to visually indicate whether the switch is on or off.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |

| Data attribute | Values |
| --- | --- |
| `[data-state]` | `"checked" | "unchecked"` |
| `[data-disabled]` | Present when disabled |

## [Accessibility](#accessibility)

Adheres to the [`switch` role requirements](https://www.w3.org/WAI/ARIA/apg/patterns/switch).

### [Keyboard Interactions](#keyboard-interactions)

| Key | Description |
| --- | --- |
| `Space` | Toggles the component's state. |
| `Enter` | Toggles the component's state. |

Previous[Slider](/primitives/docs/components/slider)

Next[Tabs](/primitives/docs/components/tabs)

[Edit this page on GitHub.](https://github.com/radix-ui/website/edit/main/data/primitives/docs/components/switch.mdx "Edit this page on GitHub.")