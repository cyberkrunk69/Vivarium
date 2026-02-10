# Radio Group

Source: https://www.radix-ui.com/primitives/docs/components/radio-group

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

# Radio Group

A set of checkable buttons—known as radio buttons—where no more than one of
the buttons can be checked at a time.

Default

Comfortable

Compact

index.jsxindex.jsxstyles.cssstyles.css

```
import * as React from "react";

import { RadioGroup } from "radix-ui";

import "./styles.css";

const RadioGroupDemo = () => (

<form>

<RadioGroup.Root
			className="RadioGroupRoot"
			defaultValue="default"
			aria-label="View density"
		>

<div style={{ display: "flex", alignItems: "center" }}>

<RadioGroup.Item className="RadioGroupItem" value="default" id="r1">

<RadioGroup.Indicator className="RadioGroupIndicator" />

</RadioGroup.Item>

<label className="Label" htmlFor="r1">

Default

</label>

</div>

<div style={{ display: "flex", alignItems: "center" }}>

<RadioGroup.Item className="RadioGroupItem" value="comfortable" id="r2">

<RadioGroup.Indicator className="RadioGroupIndicator" />

</RadioGroup.Item>

<label className="Label" htmlFor="r2">

Comfortable

</label>

</div>

<div style={{ display: "flex", alignItems: "center" }}>

<RadioGroup.Item className="RadioGroupItem" value="compact" id="r3">

<RadioGroup.Indicator className="RadioGroupIndicator" />

</RadioGroup.Item>

<label className="Label" htmlFor="r3">

Compact

</label>

</div>

</RadioGroup.Root>

</form>

);

export default RadioGroupDemo;

Expand code
```

## Features

Full keyboard navigation.

Supports horizontal/vertical orientation.

Can be controlled or uncontrolled.

## [Installation](#installation)

Install the component from your command line.

```
npm install @radix-ui/react-radio-group
```

## [Anatomy](#anatomy)

Import all parts and piece them together.

```
import { RadioGroup } from "radix-ui";

export default () => (

<RadioGroup.Root>

<RadioGroup.Item>

<RadioGroup.Indicator />

</RadioGroup.Item>

</RadioGroup.Root>

);
```

## [API Reference](#api-reference)

### [Root](#root)

Contains all the parts of a radio group.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |
| `defaultValue` Prop description | `string` | No default value |
| `value` Prop description | `string` | No default value |
| `onValueChange` Prop description | `function` See full type | No default value |
| `disabled` Prop description | `boolean` | No default value |
| `name` Prop description | `string` | No default value |
| `required` Prop description | `boolean` | No default value |
| `orientation` Prop description | `enum` See full type | `undefined` |
| `dir` Prop description | `enum` See full type | No default value |
| `loop` Prop description | `boolean` | `true` |

| Data attribute | Values |
| --- | --- |
| `[data-disabled]` | Present when disabled |

### [Item](#item)

An item in the group that can be checked. An `input` will also render when used within a `form` to ensure events propagate correctly.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |
| `value` Prop description | `string` | No default value |
| `disabled` Prop description | `boolean` | No default value |
| `required` Prop description | `boolean` | No default value |

| Data attribute | Values |
| --- | --- |
| `[data-state]` | `"checked" | "unchecked"` |
| `[data-disabled]` | Present when disabled |

### [Indicator](#indicator)

Renders when the radio item is in a checked state. You can style this element directly, or you can use it as a wrapper to put an icon into, or both.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |
| `forceMount` Prop description | `boolean` | No default value |

| Data attribute | Values |
| --- | --- |
| `[data-state]` | `"checked" | "unchecked"` |
| `[data-disabled]` | Present when disabled |

## [Accessibility](#accessibility)

Adheres to the [Radio Group WAI-ARIA design pattern](https://www.w3.org/WAI/ARIA/apg/patterns/radio) and uses [roving tabindex](https://www.w3.org/WAI/ARIA/apg/patterns/radio/examples/radio) to manage focus movement among radio items.

### [Keyboard Interactions](#keyboard-interactions)

| Key | Description |
| --- | --- |
| `Tab` | Moves focus to either the checked radio item or the first radio item in the group. |
| `Space` | When focus is on an unchecked radio item, checks it. |
| `ArrowDown` | Moves focus and checks the next radio item in the group. |
| `ArrowRight` | Moves focus and checks the next radio item in the group. |
| `ArrowUp` | Moves focus to the previous radio item in the group. |
| `ArrowLeft` | Moves focus to the previous radio item in the group. |

Previous[Progress](/primitives/docs/components/progress)

Next[Scroll Area](/primitives/docs/components/scroll-area)

[Edit this page on GitHub.](https://github.com/radix-ui/website/edit/main/data/primitives/docs/components/radio-group.mdx "Edit this page on GitHub.")