# Styling

Source: https://www.radix-ui.com/primitives/docs/guides/styling

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

Guides

# Styling

Radix Primitives are unstyled—and compatible with any styling solution—giving
you complete control over styling.

## [Styling overview](#styling-overview)

### [Functional styles](#functional-styles)

You are in control of all aspects of styling, including functional styles. For example—by default—a [Dialog Overlay](/primitives/docs/components/dialog) won't cover the entire viewport. You're responsible for adding those styles, plus any presentation styles.

### [Classes](#classes)

All components and their parts accept a `className` prop. This class will be passed through to the DOM element. You can use it in CSS as expected.

### [Data attributes](#data-attributes)

When components are stateful, their state will be exposed in a `data-state` attribute. For example, when an [Accordion Item](/primitives/docs/components/accordion) is opened, it includes a `data-state="open"` attribute.

## [Styling with CSS](#styling-with-css)

### [Styling a part](#styling-a-part)

You can style a component part by targeting the `className` that you provide.

```
import * as React from "react";

import { Accordion } from "radix-ui";

import "./styles.css";

const AccordionDemo = () => (

<Accordion.Root>

<Accordion.Item className="AccordionItem" value="item-1" />

{/* … */}

</Accordion.Root>

);

export default AccordionDemo;
```

### [Styling a state](#styling-a-state)

You can style a component state by targeting its `data-state` attribute.

```
.AccordionItem {

border-bottom: 1px solid gainsboro;

}

.AccordionItem[data-state="open"] {

border-bottom-width: 2px;

}
```

## [Styling with CSS-in-JS](#styling-with-css-in-js)

The examples below are using [styled-components](https://styled-components.com/), but you can use any CSS-in-JS library of your choice.

### [Styling a part](#styling-a-part-1)

Most CSS-in-JS libraries export a function for passing components and their styles. You can provide the Radix primitive component directly.

```
import * as React from "react";

import { Accordion } from "radix-ui";

import styled from "styled-components";

const StyledItem = styled(Accordion.Item)`
  border-bottom: 1px solid gainsboro;
`;

const AccordionDemo = () => (

<Accordion.Root>

<StyledItem value="item-1" />

{/* … */}

</Accordion.Root>

);

export default AccordionDemo;
```

### [Styling a state](#styling-a-state-1)

You can style a component state by targeting its `data-state` attribute.

```
import { Accordion } from "radix-ui";

import styled from "styled-components";

const StyledItem = styled(Accordion.Item)`
	border-bottom: 1px solid gainsboro;

	&[data-state="open"] {
		border-bottom-width: 2px;
	}
`;
```

## [Extending a primitive](#extending-a-primitive)

Extending a primitive is done the same way you extend any React component.

```
import * as React from "react";

import { Accordion as AccordionPrimitive } from "radix-ui";

const AccordionItem = React.forwardRef<

React.ElementRef<typeof AccordionPrimitive.Item>,

React.ComponentPropsWithoutRef<typeof AccordionPrimitive.Item>

>((props, forwardedRef) => (

<AccordionPrimitive.Item {...props} ref={forwardedRef} />

));

AccordionItem.displayName = "AccordionItem";
```

## [Summary](#summary)

Radix Primitives were designed to encapsulate accessibility concerns and other complex functionalities, while ensuring you retain complete control over styling.

For convenience, stateful components include a `data-state` attribute.

Previous[Releases](/primitives/docs/overview/releases)

Next[Animation](/primitives/docs/guides/animation)

[Edit this page on GitHub.](https://github.com/radix-ui/website/edit/main/data/primitives/docs/guides/styling.mdx "Edit this page on GitHub.")