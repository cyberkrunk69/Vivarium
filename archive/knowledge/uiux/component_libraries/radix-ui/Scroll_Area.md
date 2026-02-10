# Scroll Area

Source: https://www.radix-ui.com/primitives/docs/components/scroll-area

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

# Scroll Area

Augments native scroll functionality for custom, cross-browser styling.

Tags

v1.2.0-beta.50

v1.2.0-beta.49

v1.2.0-beta.48

v1.2.0-beta.47

v1.2.0-beta.46

v1.2.0-beta.45

v1.2.0-beta.44

v1.2.0-beta.43

v1.2.0-beta.42

v1.2.0-beta.41

v1.2.0-beta.40

v1.2.0-beta.39

v1.2.0-beta.38

v1.2.0-beta.37

v1.2.0-beta.36

v1.2.0-beta.35

v1.2.0-beta.34

v1.2.0-beta.33

v1.2.0-beta.32

v1.2.0-beta.31

v1.2.0-beta.30

v1.2.0-beta.29

v1.2.0-beta.28

v1.2.0-beta.27

v1.2.0-beta.26

v1.2.0-beta.25

v1.2.0-beta.24

v1.2.0-beta.23

v1.2.0-beta.22

v1.2.0-beta.21

v1.2.0-beta.20

v1.2.0-beta.19

v1.2.0-beta.18

v1.2.0-beta.17

v1.2.0-beta.16

v1.2.0-beta.15

v1.2.0-beta.14

v1.2.0-beta.13

v1.2.0-beta.12

v1.2.0-beta.11

v1.2.0-beta.10

v1.2.0-beta.9

v1.2.0-beta.8

v1.2.0-beta.7

v1.2.0-beta.6

v1.2.0-beta.5

v1.2.0-beta.4

v1.2.0-beta.3

v1.2.0-beta.2

v1.2.0-beta.1

index.jsxindex.jsxstyles.cssstyles.css

```
import * as React from "react";

import { ScrollArea } from "radix-ui";

import "./styles.css";

const TAGS = Array.from({ length: 50 }).map(

(_, i, a) => `v1.2.0-beta.${a.length - i}`,

);

const ScrollAreaDemo = () => (

<ScrollArea.Root className="ScrollAreaRoot">

<ScrollArea.Viewport className="ScrollAreaViewport">

<div style={{ padding: "15px 20px" }}>

<div className="Text">Tags</div>

{TAGS.map((tag) => (

<div className="Tag" key={tag}>

{tag}

</div>

))}

</div>

</ScrollArea.Viewport>

<ScrollArea.Scrollbar
			className="ScrollAreaScrollbar"
			orientation="vertical"
		>

<ScrollArea.Thumb className="ScrollAreaThumb" />

</ScrollArea.Scrollbar>

<ScrollArea.Scrollbar
			className="ScrollAreaScrollbar"
			orientation="horizontal"
		>

<ScrollArea.Thumb className="ScrollAreaThumb" />

</ScrollArea.Scrollbar>

<ScrollArea.Corner className="ScrollAreaCorner" />

</ScrollArea.Root>

);

export default ScrollAreaDemo;

Expand code
```

## Features

Scrollbar sits on top of the scrollable content, taking up no space.

Scrolling is native; no underlying position movements via CSS transformations.

Shims pointer behaviors only when interacting with the controls, so keyboard controls are unaffected.

Supports Right to Left direction.

## [Installation](#installation)

Install the component from your command line.

```
npm install @radix-ui/react-scroll-area
```

## [Anatomy](#anatomy)

Import all parts and piece them together.

```
import { ScrollArea } from "radix-ui";

export default () => (

<ScrollArea.Root>

<ScrollArea.Viewport />

<ScrollArea.Scrollbar orientation="horizontal">

<ScrollArea.Thumb />

</ScrollArea.Scrollbar>

<ScrollArea.Scrollbar orientation="vertical">

<ScrollArea.Thumb />

</ScrollArea.Scrollbar>

<ScrollArea.Corner />

</ScrollArea.Root>

);
```

## [API Reference](#api-reference)

### [Root](#root)

Contains all the parts of a scroll area.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |
| `type` Prop description | `enum` See full type | `"hover"` |
| `scrollHideDelay` Prop description | `number` | `600` |
| `dir` Prop description | `enum` See full type | No default value |
| `nonce` Prop description | `string` | No default value |

### [Viewport](#viewport)

The viewport area of the scroll area.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |

### [Scrollbar](#scrollbar)

The vertical scrollbar. Add a second `Scrollbar` with an `orientation` prop to enable horizontal scrolling.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |
| `forceMount` Prop description | `boolean` | No default value |
| `orientation` Prop description | `enum` See full type | `vertical` |

| Data attribute | Values |
| --- | --- |
| `[data-state]` | `"visible" | "hidden"` |
| `[data-orientation]` | `"vertical" | "horizontal"` |

### [Thumb](#thumb)

The thumb to be used in `ScrollArea.Scrollbar`.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |

| Data attribute | Values |
| --- | --- |
| `[data-state]` | `"visible" | "hidden"` |

### [Corner](#corner)

The corner where both vertical and horizontal scrollbars meet.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |

## [Accessibility](#accessibility)

In most cases, it's best to rely on native scrolling and work with the customization options available in CSS. When that isn't enough, `ScrollArea` provides additional customizability while maintaining the browser's native scroll behavior (as well as accessibility features, like keyboard scrolling).

### [Keyboard Interactions](#keyboard-interactions)

Scrolling via keyboard is supported by default because the component relies on native scrolling. Specific keyboard interactions may differ between platforms, so we do not specify them here or add specific event listeners to handle scrolling via key events.

Previous[Radio Group](/primitives/docs/components/radio-group)

Next[Select](/primitives/docs/components/select)

[Edit this page on GitHub.](https://github.com/radix-ui/website/edit/main/data/primitives/docs/components/scroll-area.mdx "Edit this page on GitHub.")