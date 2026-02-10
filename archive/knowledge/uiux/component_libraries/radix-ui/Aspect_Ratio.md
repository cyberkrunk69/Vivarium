# Aspect Ratio

Source: https://www.radix-ui.com/primitives/docs/components/aspect-ratio

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

# Aspect Ratio

Displays content within a desired ratio.

![Landscape photograph by Tobias Tullius](https://images.unsplash.com/photo-1535025183041-0991a977e25b?w=300&dpr=2&q=80)

index.jsxindex.jsxstyles.cssstyles.css

```
import * as React from "react";

import { AspectRatio } from "radix-ui";

import "./styles.css";

const AspectRatioDemo = () => (

<div className="Container">

<AspectRatio.Root ratio={16 / 9}>

<img
				className="Image"
				src="https://images.unsplash.com/photo-1535025183041-0991a977e25b?w=300&dpr=2&q=80"
				alt="Landscape photograph by Tobias Tullius"
			/>

</AspectRatio.Root>

</div>

);

export default AspectRatioDemo;

Expand code
```

## Features

Accepts any custom ratio.

## [Installation](#installation)

Install the component from your command line.

```
npm install @radix-ui/react-aspect-ratio
```

## [Anatomy](#anatomy)

Import the component.

```
import { AspectRatio } from "radix-ui";

export default () => <AspectRatio.Root />;
```

## [API Reference](#api-reference)

### [Root](#root)

Contains the content you want to constrain to a given ratio.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |
| `ratio` Prop description | `number` | `1` |

Previous[Alert Dialog](/primitives/docs/components/alert-dialog)

Next[Avatar](/primitives/docs/components/avatar)

[Edit this page on GitHub.](https://github.com/radix-ui/website/edit/main/data/primitives/docs/components/aspect-ratio.mdx "Edit this page on GitHub.")