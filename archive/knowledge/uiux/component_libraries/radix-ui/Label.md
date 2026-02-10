# Label

Source: https://www.radix-ui.com/primitives/docs/components/label

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

# Label

Renders an accessible label associated with controls.

First name

index.jsxindex.jsxstyles.cssstyles.css

```
import * as React from "react";

import { Label } from "radix-ui";

import "./styles.css";

const LabelDemo = () => (

<div
		style={{
			display: "flex",
			padding: "0 20px",
			flexWrap: "wrap",
			gap: 15,
			alignItems: "center",
		}}
	>

<Label.Root className="LabelRoot" htmlFor="firstName">

First name

</Label.Root>

<input
			className="Input"
			type="text"
			id="firstName"
			defaultValue="Pedro Duarte"
		/>

</div>

);

export default LabelDemo;

Expand code
```

## Features

Text selection is prevented when double clicking label.

Supports nested controls.

## [Installation](#installation)

Install the component from your command line.

```
npm install @radix-ui/react-label
```

## [Anatomy](#anatomy)

Import the component.

```
import { Label } from "radix-ui";

export default () => <Label.Root />;
```

## [API Reference](#api-reference)

### [Root](#root)

Contains the content for the label.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |
| `htmlFor` Prop description | `string` | No default value |

## [Accessibility](#accessibility)

This component is based on the native `label` element, it will automatically apply the correct labelling when wrapping controls or using the `htmlFor` attribute. For your own custom controls to work correctly, ensure they use native elements such as `button` or `input` as a base.

Previous[Hover Card](/primitives/docs/components/hover-card)

Next[Menubar](/primitives/docs/components/menubar)

[Edit this page on GitHub.](https://github.com/radix-ui/website/edit/main/data/primitives/docs/components/label.mdx "Edit this page on GitHub.")