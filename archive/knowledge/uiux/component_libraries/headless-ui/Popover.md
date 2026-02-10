# Popover

Source: https://headlessui.com/react/popover

---

React

[Vue](/v1/vue/popover)

# Popover

Popovers are perfect for floating panels with arbitrary content like navigation menus, mobile menus and flyout menus.

PreviewCode

## Installation

To get started, install Headless UI via npm:

```
npm install @headlessui/react
```

## Basic example

Popovers are built using the `Popover`, `PopoverButton`, and `PopoverPanel` components.

Clicking the `PopoverButton` will automatically open/close the `PopoverPanel`. When the panel is open, clicking anywhere
outside of its contents, pressing the `Escape` key, or tabbing away from it will close the popover.

```
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/react'

function Example() {
  return (
    <Popover className="relative">
      <PopoverButton>Solutions</PopoverButton>
      <PopoverPanel anchor="bottom" className="flex flex-col">
        <a href="/analytics">Analytics</a>
        <a href="/engagement">Engagement</a>
        <a href="/security">Security</a>
        <a href="/integrations">Integrations</a>
      </PopoverPanel>
    </Popover>
  )
}
```

## Styling

Headless UI keeps track of a lot of state about each component, like which listbox option is currently selected, whether
a popover is open or closed, or which item in a popover is currently focused via the keyboard.

But because the components are headless and completely unstyled out of the box, you can't see this information in your
UI until you provide the styles you want for each state yourself.

### Using data attributes

The easiest way to style the different states of a Headless UI component is using the `data-*` attributes that each
component exposes.

For example, the `Popover` component exposes a `data-open` attribute, which tells you if the popover is currently open.

```
<!-- Rendered `Popover` -->
<div data-open>
  <button data-open>Solutions</button>
  <div data-open>
    <a href="/insights">Insights</a>
    <a href="/automations">Automations</a>
    <a href="/reports">Reports</a>
  </div>
</div>
```

Use the [CSS attribute selector](https://developer.mozilla.org/en-US/docs/Web/CSS/Attribute_selectors) to conditionally
apply styles based on the presence of these data attributes. If you're using Tailwind CSS, the
[data attribute modifier](https://tailwindcss.com/docs/hover-focus-and-other-states#data-attributes) makes this easy:

```
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/react'
import { ChevronDownIcon } from '@heroicons/react/20/solid'

function Example() {
  return (

<Popover className="group">

      <PopoverButton className="flex items-center gap-2">
        Solutions

<ChevronDownIcon className="size-5 group-data-open:rotate-180" />

      </PopoverButton>
      <PopoverPanel anchor="bottom" className="flex flex-col">
        <a href="/insights">Insights</a>
        <a href="/automations">Automations</a>
        <a href="/reports">Reports</a>
      </PopoverPanel>
    </Popover>
  )
}
```

See the [component API](#component-api) for a list of all the available data attributes.

### Using render props

Each component also exposes information about its current state via
[render props](https://reactjs.org/docs/render-props.html) that you can use to conditionally apply different styles or
render different content.

For example, the `Popover` component exposes an `open` state, which tells you if the popover is currently open.

```
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/react'
import { ChevronDownIcon } from '@heroicons/react/20/solid'
import clsx from 'clsx'

function Example() {
  return (
    <Popover>

{({ open }) => (

<>
          <PopoverButton className="flex items-center gap-2">
            Solutions

<ChevronDownIcon className={clsx('size-5', open && 'rotate-180')} />

          </PopoverButton>
          <PopoverPanel anchor="bottom" className="flex flex-col">
            <a href="/insights">Insights</a>
            <a href="/automations">Automations</a>
            <a href="/reports">Reports</a>
          </PopoverPanel>
        </>

)}

    </Popover>
  )
}
```

See the [component API](#component-api) for a list of all the available render props.

## Examples

### Grouping related popovers

When rendering several related popovers, for example in a site's header navigation, use the `PopoverGroup` component.
This ensures panels stay open while users are tabbing between popovers within a group, but closes any open panel once
the user tabs outside of the group:

```
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/react'

function Example() {
  return (

<PopoverGroup>

      <Popover>
        <PopoverButton>Product</PopoverButton>
        <PopoverPanel>{/* ... */}</PopoverPanel>
      </Popover>

      <Popover>
        <PopoverButton>Solutions</PopoverButton>
        <PopoverPanel>{/* ... */}</PopoverPanel>
      </Popover>

      <Popover>
        <PopoverButton>Pricing</PopoverButton>
        <PopoverPanel>{/* ... */}</PopoverPanel>
      </Popover>

</PopoverGroup>

)
}
```

### Setting the panel width

The `PopoverPanel` has no width set by default, but you can add one using CSS:

```
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/react'

function Example() {
  return (
    <Popover className="relative">
      <PopoverButton>Solutions</PopoverButton>

<PopoverPanel anchor="bottom" className="w-52">

        <a href="/analytics">Analytics</a>
        <a href="/engagement">Engagement</a>
        <a href="/security">Security</a>
        <a href="/integrations">Integrations</a>
      </PopoverPanel>
    </Popover>
  )
}
```

If you'd like the panel width to match the `PopoverButton` width, use the `--button-width` CSS variable that's exposed
on the `PopoverPanel` element:

```
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/react'

function Example() {
  return (
    <Popover className="relative">
      <PopoverButton>Solutions</PopoverButton>

<PopoverPanel anchor="bottom" className="flex w-(--button-width) flex-col">

        <a href="/analytics">Analytics</a>
        <a href="/engagement">Engagement</a>
        <a href="/security">Security</a>
        <a href="/integrations">Integrations</a>
      </PopoverPanel>
    </Popover>
  )
}
```

### Positioning the panel

Add the `anchor` prop to the `PopoverPanel` to automatically position the panel relative to the `PopoverButton`:

```
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/react'

function Example() {
  return (
    <Popover className="relative">
      <PopoverButton>Solutions</PopoverButton>

<PopoverPanel anchor="bottom start" className="flex flex-col">

        <a href="/analytics">Analytics</a>
        <a href="/engagement">Engagement</a>
        <a href="/security">Security</a>
        <a href="/integrations">Integrations</a>
      </PopoverPanel>
    </Popover>
  )
}
```

Use the values `top`, `right`, `bottom`, or `left` to center the panel along the appropriate edge, or combine it with
`start` or `end` to align the panel to a specific corner, such as `top start` or `bottom end`.

To control the gap between the button and the panel, use the `--anchor-gap` CSS variable:

```
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/react'

function Example() {
  return (
    <Popover className="relative">
      <PopoverButton>Solutions</PopoverButton>

<PopoverPanel anchor="bottom start" className="flex flex-col [--anchor-gap:4px] sm:[--anchor-gap:8px]">

        <a href="/analytics">Analytics</a>
        <a href="/engagement">Engagement</a>
        <a href="/security">Security</a>
        <a href="/integrations">Integrations</a>
      </PopoverPanel>
    </Popover>
  )
}
```

Additionally, you can use `--anchor-offset` to control the distance that the panel should be nudged from its original
position, and `--anchor-padding` to control the minimum space that should exist between the panel and the viewport.

The `anchor` prop also supports an object API that allows you to control the `gap`, `offset`, and `padding` values using
JavaScript:

```
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/react'

function Example() {
  return (
    <Popover className="relative">
      <PopoverButton>Solutions</PopoverButton>

<PopoverPanel anchor={{ to: 'bottom start', gap: '4px' }} className="flex flex-col">

        <a href="/analytics">Analytics</a>
        <a href="/engagement">Engagement</a>
        <a href="/security">Security</a>
        <a href="/integrations">Integrations</a>
      </PopoverPanel>
    </Popover>
  )
}
```

See the [PopoverPanel API](#popover-panel) for more information about these options.

### Adding a backdrop

If you'd like to style a backdrop over your application UI whenever you open a popover, use the `PopoverBackdrop`
component:

```
import { Popover, PopoverButton, PopoverBackdrop, PopoverPanel } from '@headlessui/react'

function Example() {
  return (
    <Popover className="relative">
      <PopoverButton>Solutions</PopoverButton>

<PopoverBackdrop className="fixed inset-0 bg-black/15" />

      <PopoverPanel anchor="bottom" className="flex flex-col bg-white">
        <a href="/analytics">Analytics</a>
        <a href="/engagement">Engagement</a>
        <a href="/security">Security</a>
        <a href="/integrations">Integrations</a>
      </PopoverPanel>
    </Popover>
  )
}
```

In this example, we put the `PopoverBackdrop` before the `Panel` in the DOM so that it doesn't cover up the panel's
contents.

But like all the other components, `PopoverBackdrop` is completely headless, so how you style it is up to you.

### Adding transitions

To animate the opening and closing of the popover panel, add the `transition` prop to the `PopoverPanel` component and
then use CSS to style the different stages of the transition:

```
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/react'

function Example() {
  return (
    <Popover>
      <PopoverButton>Solutions</PopoverButton>
      <PopoverPanel
        anchor="bottom"

transition

className="flex origin-top flex-col transition duration-200 ease-out data-closed:scale-95 data-closed:opacity-0"

>
        <a href="/analytics">Analytics</a>
        <a href="/engagement">Engagement</a>
        <a href="/security">Security</a>
        <a href="/integrations">Integrations</a>
      </PopoverPanel>
    </Popover>
  )
}
```

If have a backdrop, you can animate it independently of the panel by adding the `transition` prop to the
`PopoverBackdrop`:

```
import { Popover, PopoverBackdrop, PopoverButton, PopoverPanel } from '@headlessui/react'

function Example() {
  return (
    <Popover className="relative">
      <PopoverButton>Solutions</PopoverButton>
      <PopoverBackdrop

transition

className="fixed inset-0 bg-black/15 transition duration-100 ease-out data-closed:opacity-0"

/>
      <PopoverPanel
        anchor="bottom"

transition

className="flex origin-top flex-col bg-white transition duration-200 ease-out data-closed:scale-95 data-closed:opacity-0"

>
        <a href="/analytics">Analytics</a>
        <a href="/engagement">Engagement</a>
        <a href="/security">Security</a>
        <a href="/integrations">Integrations</a>
      </PopoverPanel>
    </Popover>
  )
}
```

Internally, the `transition` prop is implemented in the exact same way as the `Transition` component. See the
[Transition documentation](/react/transition) to learn more.

### Animating with Framer Motion

Headless UI also composes well with other animation libraries in the React ecosystem like
[Framer Motion](https://www.framer.com/motion/) and [React Spring](https://www.react-spring.io/). You just need to
expose some state to those libraries.

For example, to animate the popover with Framer Motion, add the `static` prop to the `PopoverPanel` component and then
conditionally render it based on the `open` render prop:

```
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/react'
import { AnimatePresence, motion } from 'framer-motion'

function Example() {
  return (
    <Popover>

{({ open }) => (

<>
          <PopoverButton>Solutions</PopoverButton>
          <AnimatePresence>

{open && (

<PopoverPanel

static

as={motion.div}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                anchor="bottom"
                className="flex origin-top flex-col"
              >
                <a href="/analytics">Analytics</a>
                <a href="/engagement">Engagement</a>
                <a href="/security">Security</a>
                <a href="/integrations">Integrations</a>
              </PopoverPanel>

)}

          </AnimatePresence>
        </>

)}

    </Popover>
  )
}
```

### Closing popovers manually

Since popovers can contain interactive content like form controls, we can't automatically close them when you click
something inside of them like we can with `Menu` components.

To close a popover manually when clicking a child of its panel, render that child as a `CloseButton`. You can use the
`as` prop to customize which element is being rendered.

```
import { CloseButton, Popover, PopoverButton, PopoverPanel } from '@headlessui/react'
import MyLink from './MyLink'

function Example() {
  return (
    <Popover>
      <PopoverButton>Solutions</PopoverButton>
      <PopoverPanel anchor="bottom">

<CloseButton as={MyLink} href="/insights">

Insights

</CloseButton>

        {/* ... */}
      </PopoverPanel>
    </Popover>
  )
}
```

The `Popover` and `PopoverPanel` also expose a `close` render prop which you can use to imperatively close the panel,
say after running an async action:

```
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/react'

function Example() {
  return (
    <Popover>
      <PopoverButton>Terms</PopoverButton>
      <PopoverPanel>

{({ close }) => (

<button

onClick={async () => {

await fetch('/accept-terms', { method: 'POST' })

close()

}}

>

Read and accept

</button>

)}

      </PopoverPanel>
    </Popover>
  )
}
```

By default the `PopoverButton` receives focus after calling `close`, but you can change this by passing a ref into
`close(ref)`.

Finally, Headless UI also provides a `useClose` hook that can be used to imperatively close the nearest popover ancestor
when you don't have easy access to the `close` render prop, such as in a nested component:

```
import { Popover, PopoverButton, PopoverPanel, useClose } from '@headlessui/react'

function MySearchForm() {

let close = useClose()

return (
    <form
      onSubmit={(event) => {
        event.preventDefault()
        /* Perform search... */

close()

}}
    >
      <input type="search" />
      <button type="submit">Submit</button>
    </form>
  )
}

function Example() {
  return (
    <Popover>
      <PopoverButton>Filters</PopoverButton>
      <PopoverPanel>
        <MySearchForm />
        {/* ... */}
      </PopoverPanel>
    </Popover>
  )
}
```

The `useClose` hook must be used in a component that's nested within the `Popover`, otherwise it will not work.

### Rendering as different elements

By default, the `Popover` and its subcomponents each render a default element that is sensible for that component.

The `Popover`, `PopoverBackdrop`, `PopoverPanel`, and `PopoverGroup` components all render a `<div>`, and the
`PopoverButton` component renders a `<button>`.

Use the `as` prop to render the component as a different element or as your own custom component, making sure your
custom components [forward refs](https://react.dev/reference/react/forwardRef) so that Headless UI can wire things up
correctly.

```
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/react'
import { forwardRef } from 'react'

let MyCustomButton = forwardRef(function (props, ref) {

return <button className="..." ref={ref} {...props} />

})

function Example() {
  return (

<Popover as="nav">

<PopoverButton as={MyCustomButton}>Solutions</PopoverButton>

<PopoverPanel as="form">{/* ... */}</PopoverPanel>

    </Popover>
  )
}
```

## Keyboard interaction

|  |  |
| --- | --- |
| Command | Description |
| `Enter` or `Space`when a `PopoverButton` is focused. | Toggle panel |
| `Esc` | Closes any open popovers |
| `Tab` | Cycle through an open panel's contents  Tabbing out of an open panel will close that panel, and tabbing from one open panel to a sibling popover's button (within a `PopoverGroup`) closes the first panel |
| `Shift` + `Tab` | Cycle backwards through the focus order |

## Component API

### Popover

The main popover component.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `div` | `String | Component`  The element or component the popover should render as. |

|  |  |  |
| --- | --- | --- |
| Data Attribute | Render Prop | Description |
| `data-open` | `open` | `Boolean`  Whether or not the popover is open. |
| — | `close` | `(ref) => void`  Closes the popover and refocuses `PopoverButton`. Optionally pass in a **ref** or **HTMLElement** to focus that element instead. |

### PopoverBackdrop

This can be used to create a backdrop for your popover component. Clicking on the backdrop will close the popover.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `div` | `String | Component`  The element or component the popover backdrop should render as. |
| `transition` | `false` | `Boolean`  Whether the element should render transition attributes like `data-closed`, `data-enter` and `data-leave`. |

|  |  |  |
| --- | --- | --- |
| Data Attribute | Render Prop | Description |
| `data-open` | `open` | `Boolean`  Whether or not the popover is open. |

### PopoverButton

This is the trigger component to toggle a popover.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `button` | `String | Component`  The element or component the popover button should render as. |
| `disabled` | `false` | `Boolean`  Whether or not the popover button is disabled. |
| `autoFocus` | `false` | `Boolean`  Whether or not the popover button should receive focus when first rendered. |

|  |  |  |
| --- | --- | --- |
| Data Attribute | Render Prop | Description |
| `data-open` | `open` | `Boolean`  Whether or not the popover is open. |
| `data-focus` | `focus` | `Boolean`  Whether or not the popover button is focused. |
| `data-hover` | `hover` | `Boolean`  Whether or not the popover button is hovered. |
| `data-active` | `active` | `Boolean`  Whether or not the popover button is in an active or pressed state. |
| `data-autofocus` | `autofocus` | `Boolean`  Whether or not the `autoFocus` prop was set to `true`. |

### PopoverPanel

This component contains the contents of your popover.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `div` | `String | Component`  The element or component the popover panel should render as. |
| `transition` | `false` | `Boolean`  Whether the element should render transition attributes like `data-closed`, `data-enter` and `data-leave`. |
| `anchor` | — | `Object`  Configures the way the panel is anchored to the button. |
| `anchor.to` | `bottom` | `String`  Where to position the popover panel relative to the trigger.  Use the values `top`, `right`, `bottom`, `left` to center the popover panel along the appropriate edge, or combine it with `start` or `end` to align the popover panel to a specific corner, such as `top start` or `bottom end`. |
| `anchor.gap` | `0` | `Number | String`  The space between the popover button and the popover panel.  Can also be controlled using the `--anchor-gap` CSS variable. |
| `anchor.offset` | `0` | `Number | String`  The distance the popover panel should be nudged from its original position.  Can also be controlled using the `--anchor-offset` CSS variable. |
| `anchor.padding` | `0` | `Number | String`  The minimum space between the popover panel and the viewport.  Can also be controlled using the `--anchor-padding` CSS variable. |
| `static` | `false` | `Boolean`  Whether the element should ignore the internally managed open/closed state. |
| `unmount` | `true` | `Boolean`  Whether the element should be unmounted or hidden based on the open/closed state. |
| `portal` | `false` | `Boolean`  Whether the element should be rendered in a portal.  Automatically set to `true` when `anchor` prop is set. |
| `modal` | `false` | `Boolean`  Whether to enable accessibility features like scroll locking. |
| `focus` | `false` | `Boolean`  This will force focus inside the `PopoverPanel` when the popover is open. It will also close the popover if focus left this component. |

|  |  |  |
| --- | --- | --- |
| Data Attribute | Render Prop | Description |
| `data-open` | `open` | `Boolean`  Whether or not the popover is open. |
| — | `close` | `(ref) => void`  Closes the popover and refocuses `PopoverButton`. Optionally pass in a **ref** or **HTMLElement** to focus that element instead. |

### PopoverGroup

Link related sibling popovers by wrapping them in a `PopoverGroup`. Tabbing out of one `PopoverPanel` will focus the
next popover's `PopoverButton`, and tabbing outside of the `PopoverGroup` completely will close all popovers inside the
group.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `div` | `String | Component`  The element or component the popover group should render as. |

### CloseButton

This button will close the nearest `PopoverPanel` ancestor when clicked. Alternatively, use the `useClose` hook to
imperatively close the popover panel.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `button` | `String | Component`  The element or component the close button should render as. |

## Styled examples

If you're interested in predesigned [Tailwind CSS popover component examples](https://tailwindui.com/components/marketing/elements/flyout-menus) using Headless UI, check out **Tailwind Plus** — a collection of beautifully designed and expertly crafted components built by us.

It's a great way to support our work on open-source projects like this and makes it possible for us to improve them and keep them well-maintained.

[Explore more predesigned examples →](https://tailwindcss.com/plus)

[![Various components from Tailwind UI](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Ftailwind-plus.434a3ca6.png&w=3840&q=75)](https://tailwindcss.com/plus)

On this page