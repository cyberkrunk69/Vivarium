# Composition

Source: https://www.radix-ui.com/primitives/docs/guides/composition

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

# Composition

Use the `asChild` prop to compose Radix's functionality onto alternative
element types or your own React components.

All Radix primitive parts that render a DOM element accept an `asChild` prop. When `asChild` is set to `true`, Radix will not render a default DOM element, instead cloning the part's child and passing it the props and behavior required to make it functional.

## [Changing the element type](#changing-the-element-type)

In the majority of cases you shouldn’t need to modify the element type as Radix has been designed to provide the most appropriate defaults. However, there are cases where it is helpful to do so.

A good example is with `Tooltip.Trigger`. By default this part is rendered as a `button`, though you may want to add a tooltip to a link (`a` tag) as well. Let's see how you can achieve this using `asChild`:

```
import * as React from "react";

import { Tooltip } from "radix-ui";

export default () => (

<Tooltip.Root>

<Tooltip.Trigger asChild>

<a href="https://www.radix-ui.com/">Radix UI</a>

</Tooltip.Trigger>

<Tooltip.Portal>…</Tooltip.Portal>

</Tooltip.Root>

);
```

> If you do decide to change the underlying element type, it is your responsibility to ensure it remains accessible and functional. In the case of `Tooltip.Trigger` for example, it must be a focusable element that can respond to pointer and keyboard events. If you were to switch it to a `div`, it would no longer be accessible.

In reality, you will rarely modify the underlying DOM element like we've seen above. Instead it's more common to use your own React components. This is especially true for most `Trigger` parts, as you usually want to compose the functionality with the custom buttons and links in your design system.

## [Composing with your own React components](#composing-with-your-own-react-components)

This works exactly the same as above, you pass `asChild` to the part and then wrap your own component with it.
However, there are a few gotchas to be aware of.

### [Your component must spread props](#your-component-must-spread-props)

When Radix clones your component, it will pass its own props and event handlers to make it functional and accessible. If your component doesn't support those props, it will break.

This is done by spreading all of the props onto the underlying DOM node.

```
// before

const MyButton = () => <button />;

// after

const MyButton = (props) => <button {...props} />;
```

We recommend always doing this so that you are not concerned with implementation details (ie. which props/events to accept). We find this is good practice for "leaf" components in general.

> Similarly to when changing the element type directly, it is your responsibility to ensure the element type rendered by your custom component remains accessible and functional.

### [Your component must forward ref](#your-component-must-forward-ref)

Additionally, Radix will sometimes need to attach a `ref` to your component (for example to measure its size). If your component doesn't accept a `ref`, then it will break.

This is done using `React.forwardRef` (read more on [react.dev](https://react.dev/reference/react/forwardRef)).

```
// before

const MyButton = (props) => <button {...props} />;

// after

const MyButton = React.forwardRef((props, forwardedRef) => (

<button {...props} ref={forwardedRef} />

));
```

Whilst this isn't necessary for **all** parts, we recommend always doing it so that you are not concerned with implementation details. This is also generally good practice anyway for leaf components.

## [Composing multiple primitives](#composing-multiple-primitives)

`asChild` can be used as deeply as you need to. This means it is a great way to compose multiple primitive's behavior together.
Here is an example of how you can compose `Tooltip.Trigger` and `Dialog.Trigger` together with your own button:

```
import * as React from "react";

import { Dialog, Tooltip } from "radix-ui";

const MyButton = React.forwardRef((props, forwardedRef) => (

<button {...props} ref={forwardedRef} />

));

export default () => {

return (

<Dialog.Root>

<Tooltip.Root>

<Tooltip.Trigger asChild>

<Dialog.Trigger asChild>

<MyButton>Open dialog</MyButton>

</Dialog.Trigger>

</Tooltip.Trigger>

<Tooltip.Portal>…</Tooltip.Portal>

</Tooltip.Root>

<Dialog.Portal>...</Dialog.Portal>

</Dialog.Root>

);

};
```

Previous[Animation](/primitives/docs/guides/animation)

Next[Server-side rendering](/primitives/docs/guides/server-side-rendering)

[Edit this page on GitHub.](https://github.com/radix-ui/website/edit/main/data/primitives/docs/guides/composition.mdx "Edit this page on GitHub.")