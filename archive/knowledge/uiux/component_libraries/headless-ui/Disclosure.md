# Disclosure

Source: https://headlessui.com/react/disclosure

---

React

[Vue](/v1/vue/disclosure)

# Disclosure

A simple, accessible foundation for building custom UIs that show and hide content, like togglable accordion panels.

PreviewCode

## Installation

To get started, install Headless UI via npm:

```
npm install @headlessui/react
```

## Basic example

Disclosures are built using the `Disclosure`, `DisclosureButton`, and `DisclosurePanel` components.

The button will automatically open/close the panel when clicked, and all components will receive the appropriate
`aria-*` related attributes like `aria-expanded` and `aria-controls`.

```
import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/react'

function Example() {
  return (
    <Disclosure>
      <DisclosureButton className="py-2">Is team pricing available?</DisclosureButton>
      <DisclosurePanel className="text-gray-500">
        Yes! You can purchase a license that you can share with your entire team.
      </DisclosurePanel>
    </Disclosure>
  )
}
```

## Styling

Headless UI keeps track of a lot of state about each component, like which listbox option is currently selected, whether
a popover is open or closed, or which item in a disclosure is currently focused via the keyboard.

But because the components are headless and completely unstyled out of the box, you can't see this information in your
UI until you provide the styles you want for each state yourself.

### Using data attributes

The easiest way to style the different states of a Headless UI component is using the `data-*` attributes that each
component exposes.

For example, the `DisclosureButton` component exposes a `data-open` attribute, which tells you if the disclosure is
currently open.

```
<!-- Rendered `Disclosure` -->
<button data-open>Do you offer technical support?</button>
<div data-open>No</div>
```

Use the [CSS attribute selector](https://developer.mozilla.org/en-US/docs/Web/CSS/Attribute_selectors) to conditionally
apply styles based on the presence of these data attributes. If you're using Tailwind CSS, the
[data attribute modifier](https://tailwindcss.com/docs/hover-focus-and-other-states#data-attributes) makes this easy:

```
import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/react'
import { ChevronDownIcon } from '@heroicons/react/20/solid'

function Example() {
  return (
    <Disclosure>
      <DisclosureButton className="group flex items-center gap-2">
        Do you offer technical support?

<ChevronDownIcon className="w-5 group-data-open:rotate-180" />

      </DisclosureButton>
      <DisclosurePanel>No</DisclosurePanel>
    </Disclosure>
  )
}
```

See the [component API](#component-api) for a list of all the available data attributes.

### Using render props

Each component also exposes information about its current state via
[render props](https://reactjs.org/docs/render-props.html) that you can use to conditionally apply different styles or
render different content.

For example, the `DisclosureButton` component exposes an `open` state, which tells you if the disclosure is currently
open.

```
import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/react'
import { ChevronDownIcon } from '@heroicons/react/20/solid'
import clsx from 'clsx'

function Example() {
  return (
    <Disclosure>

{({ open }) => (

<>
          <DisclosureButton className="flex items-center gap-2">
            Do you offer technical support?

<ChevronDownIcon className={clsx('w-5', open && 'rotate-180')} />

          </DisclosureButton>
          <DisclosurePanel>No</DisclosurePanel>
        </>

)}

    </Disclosure>
  )
}
```

See the [component API](#component-api) for a list of all the available render props.

## Examples

### Adding transitions

To animate the opening and closing of the disclosure panel, add the `transition` prop to the `DisclosurePanel` component
and then use CSS to style the different stages of the transition:

```
import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/react'

function Example() {
  return (
    <Disclosure as="div" className="w-full max-w-md">
      <DisclosureButton className="w-full border-b pb-2 text-left">Is team pricing available?</DisclosureButton>
      <div className="overflow-hidden py-2">
        <DisclosurePanel

transition

className="origin-top transition duration-200 ease-out data-closed:-translate-y-6 data-closed:opacity-0"

>
          Yes! You can purchase a license that you can share with your entire team.
        </DisclosurePanel>
      </div>
    </Disclosure>
  )
}
```

Internally, the `transition` prop is implemented in the exact same way as the `Transition` component. See the
[Transition documentation](/react/transition) to learn more.

### Animating with Framer Motion

Headless UI also composes well with other animation libraries in the React ecosystem like
[Framer Motion](https://www.framer.com/motion/) and [React Spring](https://www.react-spring.io/). You just need to
expose some state to those libraries.

For example, to animate the menu with Framer Motion, add the `static` prop to the `DisclosurePanel` component and then
conditionally render it based on the `open` render prop:

```
import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/react'
import { AnimatePresence, easeOut, motion } from 'framer-motion'
import { Fragment } from 'react'

function Example() {
  return (

<Disclosure as="div" className="w-full max-w-md">

      {({ open }) => (
        <>
          <DisclosureButton className="w-full border-b pb-2 text-left">Is team pricing available?</DisclosureButton>
          <div className="overflow-hidden py-2">
            <AnimatePresence>
              {open && (

<DisclosurePanel static as={Fragment}>

                  <motion.div
                    initial={{ opacity: 0, y: -24 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -24 }}
                    transition={{ duration: 0.2, ease: easeOut }}
                    className="origin-top"
                  >
                    Yes! You can purchase a license that you can share with your entire team.
                  </motion.div>
                </DisclosurePanel>
              )}
            </AnimatePresence>
          </div>

</>

)}
    </Disclosure>
  )
}
```

### Closing disclosures manually

To close a disclosure manually when clicking a child of its panel, render that child as a `CloseButton`. You can use the
`as` prop to customize which element is being rendered.

```
import { CloseButton, Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/react'
import MyLink from './MyLink'

function Example() {
  return (
    <Disclosure>
      <DisclosureButton>Open mobile menu</DisclosureButton>
      <DisclosurePanel>

<CloseButton as={MyLink} href="/home">

Home

</CloseButton>

      </DisclosurePanel>
    </Disclosure>
  )
}
```

This is especially useful when using disclosures for things like mobile menus that contain links where you want the
disclosure to close when navigating to the next page.

The `Disclosure` and `DisclosurePanel` also expose a `close` render prop which you can use to imperatively close the
panel, say after running an async action:

```
import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/react'

function Example() {
  return (
    <Disclosure>
      <DisclosureButton>Terms</DisclosureButton>
      <DisclosurePanel>

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

      </DisclosurePanel>
    </Disclosure>
  )
}
```

By default the `DisclosureButton` receives focus after calling `close`, but you can change this by passing a ref into
`close(ref)`.

Finally, Headless UI also provides a `useClose` hook that can be used to imperatively close the nearest disclosure
ancestor when you don't have easy access to the `close` render prop, such as in a nested component:

```
import { Disclosure, DisclosureButton, DisclosurePanel, useClose } from '@headlessui/react'

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
    <Disclosure>
      <DisclosureButton>Filters</DisclosureButton>
      <DisclosurePanel>
        <MySearchForm />
        {/* ... */}
      </DisclosurePanel>
    </Disclosure>
  )
}
```

The `useClose` hook must be used in a component that's nested within the `Disclosure`, otherwise it will not work.

### Rendering as different elements

`Disclosure` and its subcomponents each render a default element that is sensible for that component: the `Button`
renders a `<button>`, `Panel` renders a `<div>`. By contrast, the root `Disclosure` component *does not render an
element*, and instead renders its children directly by default.

Use the `as` prop to render the component as a different element or as your own custom component, making sure your
custom components [forward refs](https://react.dev/reference/react/forwardRef) so that Headless UI can wire things up
correctly.

```
import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/react'
import { forwardRef } from 'react'

let MyCustomButton = forwardRef(function (props, ref) {

return <button className="..." ref={ref} {...props} />

})

function Example() {
  return (

<Disclosure as="div">

<DisclosureButton as={MyCustomButton}>What languages do you support?</DisclosureButton>

<DisclosurePanel as="ul">

        <li>HTML</li>
        <li>CSS</li>
        <li>JavaScript</li>
      </DisclosurePanel>
    </Disclosure>
  )
}
```

## Keyboard interaction

|  |  |
| --- | --- |
| Command | Description |
| `Enter` or `Space`when a `DisclosureButton` is focused. | Toggles panel |

## Component API

### Disclosure

The main disclosure component.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `Fragment` | `String | Component`  The element or component the disclosure should render as. |
| `defaultOpen` | `false` | `Boolean`  Whether or not the `Disclosure` component should be open by default. |

|  |  |  |
| --- | --- | --- |
| Data Attribute | Render Prop | Description |
| `data-open` | `open` | `Boolean`  Whether or not the disclosure is open. |
| — | `close` | `(ref) => void`  Closes the disclosure and refocuses `DisclosureButton`. Optionally pass in a **ref** or **HTMLElement** to focus that element instead. |

### DisclosureButton

The trigger component that toggles a Disclosure.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `button` | `String | Component`  The element or component the disclosure button should render as. |
| `autoFocus` | `false` | `Boolean`  Whether or not the disclosure button should receive focus when first rendered. |

|  |  |  |
| --- | --- | --- |
| Data Attribute | Render Prop | Description |
| `data-open` | `open` | `Boolean`  Whether or not the disclosure is open. |
| `data-focus` | `focus` | `Boolean`  Whether or not the disclosure button is focused. |
| `data-hover` | `hover` | `Boolean`  Whether or not the disclosure button is hovered. |
| `data-active` | `active` | `Boolean`  Whether or not the disclosure button is in an active or pressed state. |
| `data-autofocus` | `autofocus` | `Boolean`  Whether or not the `autoFocus` prop was set to `true`. |

### DisclosurePanel

This component contains the contents of your disclosure.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `div` | `String | Component`  The element or component the disclosure panel should render as. |
| `transition` | `false` | `Boolean`  Whether the element should render transition attributes like `data-closed`, `data-enter` and `data-leave`. |
| `static` | `false` | `Boolean`  Whether the element should ignore the internally managed open/closed state. |
| `unmount` | `true` | `Boolean`  Whether the element should be unmounted or hidden based on the open/closed state. |

|  |  |  |
| --- | --- | --- |
| Data Attribute | Render Prop | Description |
| `data-open` | `open` | `Boolean`  Whether or not the disclosure is open. |
| — | `close` | `(ref) => void`  Closes the disclosure and refocuses `DisclosureButton`. Optionally pass in a **ref** or **HTMLElement** to focus that element instead. |

### CloseButton

This button will close the nearest `DisclosurePanel` ancestor when clicked. Alternatively, use the `useClose` hook to
imperatively close the disclosure panel.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `button` | `String | Component`  The element or component the close button should render as. |

## Styled examples

If you're interested in predesigned [Tailwind CSS disclosure component examples](https://tailwindui.com/components/marketing/sections/faq-sections) using Headless UI, check out **Tailwind Plus** — a collection of beautifully designed and expertly crafted components built by us.

It's a great way to support our work on open-source projects like this and makes it possible for us to improve them and keep them well-maintained.

[Explore more predesigned examples →](https://tailwindcss.com/plus)

[![Various components from Tailwind UI](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Ftailwind-plus.434a3ca6.png&w=3840&q=75)](https://tailwindcss.com/plus)

On this page