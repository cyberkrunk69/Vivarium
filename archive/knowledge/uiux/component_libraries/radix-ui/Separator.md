# Separator

Source: https://www.radix-ui.com/primitives/docs/components/separator

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

# Separator

Visually or semantically separates content.

Radix Primitives

An open-source UI component library.

Blog

Docs

Source

index.jsxindex.jsxstyles.cssstyles.css

```
import * as React from "react";

import { Separator } from "radix-ui";

import "./styles.css";

const SeparatorDemo = () => (

<div style={{ width: "100%", maxWidth: 300, margin: "0 15px" }}>

<div className="Text" style={{ fontWeight: 500 }}>

Radix Primitives

</div>

<div className="Text">An open-source UI component library.</div>

<Separator.Root className="SeparatorRoot" style={{ margin: "15px 0" }} />

<div style={{ display: "flex", height: 20, alignItems: "center" }}>

<div className="Text">Blog</div>

<Separator.Root
				className="SeparatorRoot"
				decorative
				orientation="vertical"
				style={{ margin: "0 15px" }}
			/>

<div className="Text">Docs</div>

<Separator.Root
				className="SeparatorRoot"
				decorative
				orientation="vertical"
				style={{ margin: "0 15px" }}
			/>

<div className="Text">Source</div>

</div>

</div>

);

export default SeparatorDemo;

Expand code
```

## Features

Supports horizontal and vertical orientations.

## [Installation](#installation)

Install the component from your command line.

```
npm install @radix-ui/react-separator
```

## [Anatomy](#anatomy)

Import all parts and piece them together.

```
import { Separator } from "radix-ui";

export default () => <Separator.Root />;
```

## [API Reference](#api-reference)

### [Root](#root)

The separator.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |
| `orientation` Prop description | `enum` See full type | `"horizontal"` |
| `decorative` Prop description | `boolean` | No default value |

| Data attribute | Values |
| --- | --- |
| `[data-orientation]` | `"vertical" | "horizontal"` |

## [Accessibility](#accessibility)

Adheres to the [`separator` role requirements](https://www.w3.org/TR/wai-aria-1.2/#separator).

Previous[Select](/primitives/docs/components/select)

Next[Slider](/primitives/docs/components/slider)

[Edit this page on GitHub.](https://github.com/radix-ui/website/edit/main/data/primitives/docs/components/separator.mdx "Edit this page on GitHub.")