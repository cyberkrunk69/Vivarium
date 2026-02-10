# Toolbar

Source: https://www.radix-ui.com/primitives/docs/components/toolbar

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

# Toolbar

A container for grouping a set of controls, such as buttons, toggle groups or
dropdown menus.

[Edited 2 hours ago](#)Share

index.jsxindex.jsxstyles.cssstyles.css

```
import * as React from "react";

import { Toolbar } from "radix-ui";

import {
	StrikethroughIcon,
	TextAlignLeftIcon,
	TextAlignCenterIcon,
	TextAlignRightIcon,
	FontBoldIcon,
	FontItalicIcon,
} from "@radix-ui/react-icons";

import "./styles.css";

const ToolbarDemo = () => (

<Toolbar.Root className="ToolbarRoot" aria-label="Formatting options">

<Toolbar.ToggleGroup type="multiple" aria-label="Text formatting">

<Toolbar.ToggleItem
				className="ToolbarToggleItem"
				value="bold"
				aria-label="Bold"
			>

<FontBoldIcon />

</Toolbar.ToggleItem>

<Toolbar.ToggleItem
				className="ToolbarToggleItem"
				value="italic"
				aria-label="Italic"
			>

<FontItalicIcon />

</Toolbar.ToggleItem>

<Toolbar.ToggleItem
				className="ToolbarToggleItem"
				value="strikethrough"
				aria-label="Strike through"
			>

<StrikethroughIcon />

</Toolbar.ToggleItem>

</Toolbar.ToggleGroup>

<Toolbar.Separator className="ToolbarSeparator" />

<Toolbar.ToggleGroup
			type="single"
			defaultValue="center"
			aria-label="Text alignment"
		>

<Toolbar.ToggleItem
				className="ToolbarToggleItem"
				value="left"
				aria-label="Left aligned"
			>

<TextAlignLeftIcon />

</Toolbar.ToggleItem>

<Toolbar.ToggleItem
				className="ToolbarToggleItem"
				value="center"
				aria-label="Center aligned"
			>

<TextAlignCenterIcon />

</Toolbar.ToggleItem>

<Toolbar.ToggleItem
				className="ToolbarToggleItem"
				value="right"
				aria-label="Right aligned"
			>

<TextAlignRightIcon />

</Toolbar.ToggleItem>

</Toolbar.ToggleGroup>

<Toolbar.Separator className="ToolbarSeparator" />

<Toolbar.Link
			className="ToolbarLink"
			href="#"
			target="_blank"
			style={{ marginRight: 10 }}
		>

Edited 2 hours ago

</Toolbar.Link>

<Toolbar.Button className="ToolbarButton" style={{ marginLeft: "auto" }}>

Share

</Toolbar.Button>

</Toolbar.Root>

);

export default ToolbarDemo;

Expand code
```

## Features

Full keyboard navigation.

## [Installation](#installation)

Install the component from your command line.

```
npm install @radix-ui/react-toolbar
```

## [Anatomy](#anatomy)

Import the component.

```
import { Toolbar } from "radix-ui";

export default () => (

<Toolbar.Root>

<Toolbar.Button />

<Toolbar.Separator />

<Toolbar.Link />

<Toolbar.ToggleGroup>

<Toolbar.ToggleItem />

</Toolbar.ToggleGroup>

</Toolbar.Root>

);
```

## [API Reference](#api-reference)

### [Root](#root)

Contains all the toolbar component parts.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |
| `orientation` Prop description | `enum` See full type | `"horizontal"` |
| `dir` Prop description | `enum` See full type | No default value |
| `loop` Prop description | `boolean` | `true` |

| Data attribute | Values |
| --- | --- |
| `[data-orientation]` | `"vertical" | "horizontal"` |

### [Button](#button)

A button item.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |

| Data attribute | Values |
| --- | --- |
| `[data-orientation]` | `"vertical" | "horizontal"` |

### [Link](#link)

A link item.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |

### [ToggleGroup](#togglegroup)

A set of two-state buttons that can be toggled on or off.

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

| Data attribute | Values |
| --- | --- |
| `[data-orientation]` | `"vertical" | "horizontal"` |

### [ToggleItem](#toggleitem)

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

### [Separator](#separator)

Used to visually separate items in the toolbar.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |

| Data attribute | Values |
| --- | --- |
| `[data-orientation]` | `"vertical" | "horizontal"` |

## [Examples](#examples)

### [Use with other primitives](#use-with-other-primitives)

All our primitives which expose a `Trigger` part, such as `Dialog`, `AlertDialog`, `Popover`, `DropdownMenu` can be composed within a toolbar by using the [`asChild` prop](/primitives/docs/guides/composition).

Here is an example using our `DropdownMenu` primitive.

```
import { Toolbar, DropdownMenu } from "radix-ui";

export default () => (

<Toolbar.Root>

<Toolbar.Button>Action 1</Toolbar.Button>

<Toolbar.Separator />

<DropdownMenu.Root>

<Toolbar.Button asChild>

<DropdownMenu.Trigger>Trigger</DropdownMenu.Trigger>

</Toolbar.Button>

<DropdownMenu.Content>…</DropdownMenu.Content>

</DropdownMenu.Root>

</Toolbar.Root>

);
```

## [Accessibility](#accessibility)

Uses [roving tabindex](https://www.w3.org/TR/wai-aria-practices-1.2/examples/radio/radio.html) to manage focus movement among items.

### [Keyboard Interactions](#keyboard-interactions)

| Key | Description |
| --- | --- |
| `Tab` | Moves focus to the first item in the group. |
| `Space` | Activates/deactivates the item. |
| `Enter` | Activates/deactivates the item. |
| `ArrowDown` | Moves focus to the next item depending on `orientation`. |
| `ArrowRight` | Moves focus to the next item depending on `orientation`. |
| `ArrowUp` | Moves focus to the previous item depending on `orientation`. |
| `ArrowLeft` | Moves focus to the previous item depending on `orientation`. |
| `Home` | Moves focus to the first item. |
| `End` | Moves focus to the last item. |

Previous[Toggle Group](/primitives/docs/components/toggle-group)

Next[Tooltip](/primitives/docs/components/tooltip)

[Edit this page on GitHub.](https://github.com/radix-ui/website/edit/main/data/primitives/docs/components/toolbar.mdx "Edit this page on GitHub.")