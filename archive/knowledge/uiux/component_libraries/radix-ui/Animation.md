# Animation

Source: https://www.radix-ui.com/primitives/docs/guides/animation

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

# Animation

Animate Radix Primitives with CSS keyframes or the JavaScript animation
library of your choice.

Adding animation to Radix Primitives should feel similar to any other component, but there are some caveats noted here in regards to exiting animations with JS animation libraries.

## [Animating with CSS animation](#animating-with-css-animation)

The simplest way to animate Primitives is with CSS.

You can use CSS animation to animate both mount and unmount phases. The latter is possible because the Radix Primitives will suspend unmount while your animation plays out.

```
@keyframes fadeIn {

from {

opacity: 0;

}

to {

opacity: 1;

}

}

@keyframes fadeOut {

from {

opacity: 1;

}

to {

opacity: 0;

}

}

.DialogOverlay[data-state="open"],
.DialogContent[data-state="open"] {

animation: fadeIn 300ms ease-out;

}

.DialogOverlay[data-state="closed"],
.DialogContent[data-state="closed"] {

animation: fadeOut 300ms ease-in;

}
```

## [Delegating unmounting for JavaScript Animation](#delegating-unmounting-for-javascript-animation)

When many stateful Primitives are hidden from view, they are actually removed from the React Tree, and their elements removed from the DOM. JavaScript animation libraries need control of the unmounting phase, so we provide the `forceMount` prop on many components to allow consumers to delegate the mounting and unmounting of children based on the animation state determined by those libraries.

For example, if you want to use React Spring to animate a `Dialog`, you would do so by conditionally rendering the dialog `Overlay` and `Content` parts based on the animation state from one of its hooks like `useTransition`:

```
import { Dialog } from "radix-ui";

import { useTransition, animated, config } from "react-spring";

function Example() {

const [open, setOpen] = React.useState(false);

const transitions = useTransition(open, {

from: { opacity: 0, y: -10 },

enter: { opacity: 1, y: 0 },

leave: { opacity: 0, y: 10 },

config: config.stiff,

});

return (

<Dialog.Root open={open} onOpenChange={setOpen}>

<Dialog.Trigger>Open Dialog</Dialog.Trigger>

{transitions((styles, item) =>

item ? (

<>

<Dialog.Overlay forceMount asChild>

<animated.div
								style={{
									opacity: styles.opacity,
								}}
							/>

</Dialog.Overlay>

<Dialog.Content forceMount asChild>

<animated.div style={styles}>

<h1>Hello from inside the Dialog!</h1>

<Dialog.Close>close</Dialog.Close>

</animated.div>

</Dialog.Content>

</>

) : null,

)}

</Dialog.Root>

);

}
```

Previous[Styling](/primitives/docs/guides/styling)

Next[Composition](/primitives/docs/guides/composition)

[Edit this page on GitHub.](https://github.com/radix-ui/website/edit/main/data/primitives/docs/guides/animation.mdx "Edit this page on GitHub.")