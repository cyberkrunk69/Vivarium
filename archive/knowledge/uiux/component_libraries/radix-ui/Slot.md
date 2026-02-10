# Slot

Source: https://www.radix-ui.com/primitives/docs/utilities/slot

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

Utilities

# Slot

Merges its props onto its immediate child.

## Features

Can be used to support your own `asChild` prop.

## [Installation](#installation)

Install the component from your command line.

```
npm install @radix-ui/react-slot
```

## [Anatomy](#anatomy)

Import the component.

```
import { Slot } from "radix-ui";

export default () => (

<Slot.Root>

<div>Hello</div>

</Slot.Root>

);
```

## [Basic example](#basic-example)

Use to create your own `asChild` API.

When your component has a single children element:

```
// your-button.jsx

import * as React from "react";

import { Slot } from "radix-ui";

function Button({ asChild, ...props }) {

const Comp = asChild ? Slot.Root : "button";

return <Comp {...props} />;

}
```

Use `Slottable` when your component has multiple children to pass the props to the correct element:

```
// your-button.jsx

import * as React from "react";

import { Slot } from "radix-ui";

function Button({ asChild, children, leftElement, rightElement, ...props }) {

const Comp = asChild ? Slot.Root : "button";

return (

<Comp {...props}>

{leftElement}

<Slot.Slottable>{children}</Slot.Slottable>

{rightElement}

</Comp>

);

}
```

### [Usage](#usage)

```
import { Button } from "./your-button";

export default () => (

<Button asChild>

<a href="/contact">Contact</a>

</Button>

);
```

### [Event handlers](#event-handlers)

Any prop that starts with `on` (e.g., `onClick`) is considered an event handler.

When merging event handlers, `Slot` will create a new function where the child handler takes precedence over the slot handler.

If one of the event handlers relies on `event.defaultPrevented` make sure that the order is correct.

```
import { Slot } from "radix-ui";

export default () => (

<Slot.Root
		onClick={(event) => {
			if (!event.defaultPrevented)
				console.log("Not logged because default is prevented.");
		}}
	>

<button onClick={(event) => event.preventDefault()} />

</Slot.Root>

);
```

Previous[Portal](/primitives/docs/utilities/portal)

Next[Visually Hidden](/primitives/docs/utilities/visually-hidden)

[Edit this page on GitHub.](https://github.com/radix-ui/website/edit/main/data/primitives/docs/utilities/slot.mdx "Edit this page on GitHub.")