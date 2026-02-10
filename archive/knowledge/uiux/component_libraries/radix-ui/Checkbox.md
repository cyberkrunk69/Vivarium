# Checkbox

Source: https://www.radix-ui.com/primitives/docs/components/checkbox

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

# Checkbox

A control that allows the user to toggle between checked and not checked.

Accept terms and conditions.

index.jsxindex.jsxstyles.cssstyles.css

```
import * as React from "react";

import { Checkbox } from "radix-ui";

import { CheckIcon } from "@radix-ui/react-icons";

import "./styles.css";

const CheckboxDemo = () => (

<form>

<div style={{ display: "flex", alignItems: "center" }}>

<Checkbox.Root className="CheckboxRoot" defaultChecked id="c1">

<Checkbox.Indicator className="CheckboxIndicator">

<CheckIcon />

</Checkbox.Indicator>

</Checkbox.Root>

<label className="Label" htmlFor="c1">

Accept terms and conditions.

</label>

</div>

</form>

);

export default CheckboxDemo;

Expand code
```

## Features

Supports indeterminate state.

Full keyboard navigation.

Can be controlled or uncontrolled.

## [Installation](#installation)

Install the component from your command line.

```
npm install @radix-ui/react-checkbox
```

## [Anatomy](#anatomy)

Import all parts and piece them together.

```
import { Checkbox } from "radix-ui";

export default () => (

<Checkbox.Root>

<Checkbox.Indicator />

</Checkbox.Root>

);
```

## [API Reference](#api-reference)

### [Root](#root)

Contains all the parts of a checkbox. An `input` will also render when used within a `form` to ensure events propagate correctly.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |
| `defaultChecked` Prop description | `boolean | 'indeterminate'` | No default value |
| `checked` Prop description | `boolean | 'indeterminate'` | No default value |
| `onCheckedChange` Prop description | `function` See full type | No default value |
| `disabled` Prop description | `boolean` | No default value |
| `required` Prop description | `boolean` | No default value |
| `name` Prop description | `string` | No default value |
| `value` Prop description | `string` | `on` |

| Data attribute | Values |
| --- | --- |
| `[data-state]` | `"checked" | "unchecked" | "indeterminate"` |
| `[data-disabled]` | Present when disabled |

### [Indicator](#indicator)

Renders when the checkbox is in a checked or indeterminate state. You can style this element directly, or you can use it as a wrapper to put an icon into, or both.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |
| `forceMount` Prop description | `boolean` | No default value |

| Data attribute | Values |
| --- | --- |
| `[data-state]` | `"checked" | "unchecked" | "indeterminate"` |
| `[data-disabled]` | Present when disabled |

## [Examples](#examples)

### [Indeterminate](#indeterminate)

You can set the checkbox to `indeterminate` by taking control of its state.

```
import { DividerHorizontalIcon, CheckIcon } from "@radix-ui/react-icons";

import { Checkbox } from "radix-ui";

export default () => {

const [checked, setChecked] = React.useState("indeterminate");

return (

<>

<StyledCheckbox checked={checked} onCheckedChange={setChecked}>

<Checkbox.Indicator>

{checked === "indeterminate" && <DividerHorizontalIcon />}

{checked === true && <CheckIcon />}

</Checkbox.Indicator>

</StyledCheckbox>

<button
				type="button"
				onClick={() =>
					setChecked((prevIsChecked) =>
						prevIsChecked === "indeterminate" ? false : "indeterminate",
					)
				}
			>

Toggle indeterminate

</button>

</>

);

};
```

## [Accessibility](#accessibility)

Adheres to the [tri-state Checkbox WAI-ARIA design pattern](https://www.w3.org/WAI/ARIA/apg/patterns/checkbox).

### [Keyboard Interactions](#keyboard-interactions)

| Key | Description |
| --- | --- |
| `Space` | Checks/unchecks the checkbox. |

Previous[Avatar](/primitives/docs/components/avatar)

Next[Collapsible](/primitives/docs/components/collapsible)

[Edit this page on GitHub.](https://github.com/radix-ui/website/edit/main/data/primitives/docs/components/checkbox.mdx "Edit this page on GitHub.")