# Avatar

Source: https://www.radix-ui.com/primitives/docs/components/avatar

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

# Avatar

An image element with a fallback for representing the user.

PD

index.jsxindex.jsxstyles.cssstyles.css

```
import * as React from "react";

import { Avatar } from "radix-ui";

import "./styles.css";

const AvatarDemo = () => (

<div style={{ display: "flex", gap: 20 }}>

<Avatar.Root className="AvatarRoot">

<Avatar.Image
				className="AvatarImage"
				src="https://images.unsplash.com/photo-1492633423870-43d1cd2775eb?&w=128&h=128&dpr=2&q=80"
				alt="Colm Tuite"
			/>

<Avatar.Fallback className="AvatarFallback" delayMs={600}>

CT

</Avatar.Fallback>

</Avatar.Root>

<Avatar.Root className="AvatarRoot">

<Avatar.Image
				className="AvatarImage"
				src="https://images.unsplash.com/photo-1511485977113-f34c92461ad9?ixlib=rb-1.2.1&w=128&h=128&dpr=2&q=80"
				alt="Pedro Duarte"
			/>

<Avatar.Fallback className="AvatarFallback" delayMs={600}>

JD

</Avatar.Fallback>

</Avatar.Root>

<Avatar.Root className="AvatarRoot">

<Avatar.Fallback className="AvatarFallback">PD</Avatar.Fallback>

</Avatar.Root>

</div>

);

export default AvatarDemo;

Expand code
```

## Features

Automatic and manual control over when the image renders.

Fallback part accepts any children.

Optionally delay fallback rendering to avoid content flashing.

## [Installation](#installation)

Install the component from your command line.

```
npm install @radix-ui/react-avatar
```

## [Anatomy](#anatomy)

Import all parts and piece them together.

```
import { Avatar } from "radix-ui";

export default () => (

<Avatar.Root>

<Avatar.Image />

<Avatar.Fallback />

</Avatar.Root>

);
```

## [API Reference](#api-reference)

### [Root](#root)

Contains all the parts of an avatar.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |

### [Image](#image)

The image to render. By default it will only render when it has loaded. You can use the `onLoadingStatusChange` handler if you need more control.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |
| `onLoadingStatusChange` Prop description | `function` See full type | No default value |

### [Fallback](#fallback)

An element that renders when the image hasn't loaded. This means whilst it's loading, or if there was an error. If you notice a flash during loading, you can provide a `delayMs` prop to delay its rendering so it only renders for those with slower connections. For more control, use the `onLoadingStatusChange` handler on `Avatar.Image`.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |
| `delayMs` Prop description | `number` | No default value |

## [Examples](#examples)

### [Clickable Avatar with tooltip](#clickable-avatar-with-tooltip)

You can compose the Avatar with a [Tooltip](/primitives/docs/components/tooltip) to display extra information.

```
import { Avatar, Tooltip } from "radix-ui";

export default () => (

<Tooltip.Root>

<Tooltip.Trigger>

<Avatar.Root>…</Avatar.Root>

</Tooltip.Trigger>

<Tooltip.Content side="top">

Tooltip content

<Tooltip.Arrow />

</Tooltip.Content>

</Tooltip.Root>

);
```

Previous[Aspect Ratio](/primitives/docs/components/aspect-ratio)

Next[Checkbox](/primitives/docs/components/checkbox)

[Edit this page on GitHub.](https://github.com/radix-ui/website/edit/main/data/primitives/docs/components/avatar.mdx "Edit this page on GitHub.")