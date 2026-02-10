# Toggle Group

Source: https://www.radix-ui.com/primitives/docs/components/toggle-group

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

# Toggle Group

A set of two-state buttons that can be toggled on or off.

index.jsxindex.jsxstyles.cssstyles.css

```
import * as React from "react";

import { ToggleGroup } from "radix-ui";

import {
	TextAlignLeftIcon,
	TextAlignCenterIcon,
	TextAlignRightIcon,
} from "@radix-ui/react-icons";

import "./styles.css";

const ToggleGroupDemo = () => (

<ToggleGroup.Root
		className="ToggleGroup"
		type="single"
		defaultValue="center"
		aria-label="Text alignment"
	>

<ToggleGroup.Item
			className="ToggleGroupItem"
			value="left"
			aria-label="Left aligned"
		>

<TextAlignLeftIcon />

</ToggleGroup.Item>

<ToggleGroup.Item
			className="ToggleGroupItem"
			value="center"
			aria-label="Center aligned"
		>

<TextAlignCenterIcon />

</ToggleGroup.Item>

<ToggleGroup.Item
			className="ToggleGroupItem"
			value="right"
			aria-label="Right aligned"
		>

<TextAlignRightIcon />

</ToggleGroup.Item>

</ToggleGroup.Root>

);

export default ToggleGroupDemo;

Expand code
```

## Features

Full keyboard navigation.

Supports horizontal/vertical orientation.

Support single and multiple pressed buttons.

Can be controlled or uncontrolled.

## [Installation](#installation)

Install the component from your command line.

```
npm install @radix-ui/react-toggle-group
```

## [Anatomy](#anatomy)

Import the component.

```
import { ToggleGroup } from "radix-ui";

export default () => (

<ToggleGroup.Root>

<ToggleGroup.Item />

</ToggleGroup.Root>

);
```

## [API Reference](#api-reference)

### [Root](#root)

Contains all the parts of a toggle group.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |
| `type*` Prop description | `enum` See full type | No default value |
| `value` Prop description | `string` | No default value |
| `defaultValue` Prop description | `string` | No default value |
| `onValueChange` Prop description | `function` See full type | No default value |
| `value` Prop description | `string[]` | `[]` |
| `defaultValue` Prop description | `string[]` | `[]` |
| `onValueChange` Prop description | `function` See full type | No default value |
| `disabled` Prop description | `boolean` | `false` |
| `rovingFocus` Prop description | `boolean` | `true` |
| `orientation` Prop description | `enum` See full type | `undefined` |
| `dir` Prop description | `enum` See full type | No default value |
| `loop` Prop description | `boolean` | `true` |

| Data attribute | Values |
| --- | --- |
| `[data-orientation]` | `"vertical" | "horizontal"` |

### [Item](#item)

An item in the group.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |
| `value*` Prop description | `string` | No default value |
| `disabled` Prop description | `boolean` | No default value |

| Data attribute | Values |
| --- | --- |
| `[data-state]` | `"on" | "off"` |
| `[data-disabled]` | Present when disabled |
| `[data-orientation]` | `"vertical" | "horizontal"` |

## [Examples](#examples)

### [Ensuring there is always a value](#ensuring-there-is-always-a-value)

You can control the component to ensure a value.

```
import * as React from "react";

import { ToggleGroup } from "radix-ui";

export default () => {

const [value, setValue] = React.useState("left");

return (

<ToggleGroup.Root
			type="single"
			value={value}
			onValueChange={(value) => {
				if (value) setValue(value);
			}}
		>

<ToggleGroup.Item value="left">

<TextAlignLeftIcon />

</ToggleGroup.Item>

<ToggleGroup.Item value="center">

<TextAlignCenterIcon />

</ToggleGroup.Item>

<ToggleGroup.Item value="right">

<TextAlignRightIcon />

</ToggleGroup.Item>

</ToggleGroup.Root>

);

};
```

## [Accessibility](#accessibility)

Uses [roving tabindex](https://www.w3.org/TR/wai-aria-practices-1.2/examples/radio/radio.html) to manage focus movement among items.

### [Keyboard Interactions](#keyboard-interactions)

| Key | Description |
| --- | --- |
| `Tab` | Moves focus to either the pressed item or the first item in the group. |
| `Space` | Activates/deactivates the item. |
| `Enter` | Activates/deactivates the item. |
| `ArrowDown` | Moves focus to the next item in the group. |
| `ArrowRight` | Moves focus to the next item in the group. |
| `ArrowUp` | Moves focus to the previous item in the group. |
| `ArrowLeft` | Moves focus to the previous item in the group. |
| `Home` | Moves focus to the first item. |
| `End` | Moves focus to the last item. |

Previous[Toggle](/primitives/docs/components/toggle)

Next[Toolbar](/primitives/docs/components/toolbar)

[Edit this page on GitHub.](https://github.com/radix-ui/website/edit/main/data/primitives/docs/components/toggle-group.mdx "Edit this page on GitHub.")