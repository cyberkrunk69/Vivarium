# Transition

Source: https://headlessui.com/react/transition

---

React

[Vue](/v1/vue/transition)

# Transition

Control the transition styles of conditionally rendered elements, including nested child transitions, using CSS
classes.

PreviewCode

## Installation

To get started, install Headless UI via npm:

```
npm install @headlessui/react
```

## Basic example

To transition a conditionally rendered element, wrap it in the `Transition` component and use the `show` prop to
indicate whether it is open or closed.

Then, use native CSS transition styles to apply an animation, specifying the element's closed styles by targeting the
`data-closed` attribute that the `Transition` component exposes.

```
import { Transition } from '@headlessui/react'
import { useState } from 'react'

function Example() {
  const [open, setOpen] = useState(false)

  return (
    <>
      <button onClick={() => setOpen((open) => !open)}>Toggle</button>
      <Transition show={open}>
        <div className="transition duration-300 ease-in data-closed:opacity-0">I will fade in and out</div>
      </Transition>
    </>
  )
}
```

Styles defined with the `data-closed` attribute will be used as the starting point when transitioning in as well as the
ending point when transitioning out.

For more complex transitions, you can also use the `data-enter`, `data-leave`, and `data-transition` attributes to apply
styles at the different stages of the transition.

## Examples

### Different enter/leave transitions

Use the `data-enter` and `data-leave` attributes to apply different transition styles when entering and leaving:

```
import { Transition } from '@headlessui/react'
import clsx from 'clsx'
import { useState } from 'react'

function Example() {
  const [open, setOpen] = useState(false)

  return (
    <div className="relative">
      <button onClick={() => setOpen((open) => !open)}>Toggle</button>
      <Transition show={open}>
        <div
          className={clsx([
            // Base styles
            'absolute w-48 border transition ease-in-out',
            // Shared closed styles
            'data-closed:opacity-0',
            // Entering styles
            'data-enter:duration-100 data-enter:data-closed:-translate-x-full',
            // Leaving styles
            'data-leave:duration-300 data-leave:data-closed:translate-x-full',
          ])}
        >
          I will enter from the left and leave to the right
        </div>
      </Transition>
    </div>
  )
}
```

This example combines the `data-enter` and `data-closed` attributes to specify the starting point of the enter
transition, and combines the `data-leave` and `data-closed` attributes to specify the ending point of the leave
transition.

It also uses the `data-enter` and `data-leave` attributes to specify different enter and leave durations.

### Coordinating multiple transitions

Sometimes you need to transition multiple elements with different animations but all based on the same state. For
example, say the user clicks a button to open a sidebar that slides over the screen, and you also need to fade-in a
backdrop at the same time.

You can do this by wrapping the related elements with a parent `Transition` component, and wrapping each child that
needs its own transition styles with a `TransitionChild` component, which will automatically communicate with the parent
`Transition` and inherit the parent's `open` state.

```
import { Transition, TransitionChild } from '@headlessui/react'
import { useState } from 'react'

function Example() {
  const [open, setOpen] = useState(false)

  return (
    <>
      <button onClick={() => setOpen(true)}>Open</button>
      {/* The `show` prop controls all nested `TransitionChild` components. */}

<Transition show={open}>

        {/* Backdrop */}

<TransitionChild>

          <div
            className="fixed inset-0 bg-black/30 transition duration-300 data-closed:opacity-0"
            onClick={() => setOpen(false)}
          />

</TransitionChild>

        {/* Slide-in sidebar */}

<TransitionChild>

          <div className="fixed inset-y-0 left-0 w-64 bg-white transition duration-300 data-closed:-translate-x-full">
            {/* ... */}

</div>

</TransitionChild>

      </Transition>
    </>
  )
}
```

The `TransitionChild` component has the exact same API as the `Transition` component, but with no `show` prop, since the
`show` value is controlled by the parent.

Parent `Transition` components will always automatically wait for all children to finish transitioning before
unmounting, so you don't need to manage any of that timing yourself.

### Transitioning on initial mount

If you want an element to transition the very first time it's rendered, set the `appear` prop to `true`.

This is useful if you want something to transition in on initial page load, or when its parent is conditionally
rendered.

```
import { Transition } from '@headlessui/react'
import { useState } from 'react'

function Example() {
  const [open, setOpen] = useState(true)

  return (
    <>
      <button onClick={() => setOpen((open) => !open)}>Toggle</button>

<Transition show={open} appear={true}>

        <div className="transition duration-300 ease-in data-closed:opacity-0">I will fade in on initial render</div>
      </Transition>
    </>
  )
}
```

## Component API

### Transition

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `Fragment` | `String | Component`  The element or component the transition should render as. |
| `show` | — | `Boolean`  Whether the children should be shown or hidden. |
| `appear` | `false` | `Boolean`  Whether the transition should run on initial mount. |
| `unmount` | `true` | `Boolean`  Whether the element should be unmounted or hidden based on the show state. |
| `beforeEnter` | — | `() => void`  Callback which is called before we start the enter transition. |
| `afterEnter` | — | `() => void`  Callback which is called after we finished the enter transition. |
| `beforeLeave` | — | `() => void`  Callback which is called before we start the leave transition. |
| `afterLeave` | — | `() => void`  Callback which is called after we finished the leave transition. |

### TransitionChild

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `Fragment` | `String | Component`  The element or component the transition child should render as. |
| `appear` | `false` | `Boolean`  Whether the transition should run on initial mount. |
| `unmount` | `true` | `Boolean`  Whether the element should be unmounted or hidden based on the show state. |
| `beforeEnter` | — | `() => void`  Callback which is called before we start the enter transition. |
| `afterEnter` | — | `() => void`  Callback which is called after we finished the enter transition. |
| `beforeLeave` | — | `() => void`  Callback which is called before we start the leave transition. |
| `afterLeave` | — | `() => void`  Callback which is called after we finished the leave transition. |

### Data attributes

|  |  |
| --- | --- |
| Attribute | Description |
| `data-closed` | Present before transitioning in, and when transitioning out. |
| `data-enter` | Present when transitioning in. |
| `data-leave` | Present when transitioning out. |
| `data-transition` | Present when transitioning in or out. |

## Styled examples

If you're interested in predesigned [Tailwind CSS component examples](https://tailwindui.com/components) using Headless UI, check out **Tailwind Plus** — a collection of beautifully designed and expertly crafted components built by us.

It's a great way to support our work on open-source projects like this and makes it possible for us to improve them and keep them well-maintained.

[Explore more predesigned examples →](https://tailwindcss.com/plus)

[![Various components from Tailwind UI](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Ftailwind-plus.434a3ca6.png&w=3840&q=75)](https://tailwindcss.com/plus)

On this page