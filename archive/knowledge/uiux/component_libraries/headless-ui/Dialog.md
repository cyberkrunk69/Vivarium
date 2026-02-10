# Dialog

Source: https://headlessui.com/react/dialog

---

React

[Vue](/v1/vue/dialog)

# Dialog

A fully-managed, renderless dialog component jam-packed with accessibility and keyboard features, perfect for building
completely custom dialogs and alerts.

PreviewCode

## Installation

To get started, install Headless UI via npm:

```
npm install @headlessui/react
```

## Basic example

Dialogs are built using the `Dialog`, `DialogPanel`, `DialogTitle`, and `Description` components:

```
import { Description, Dialog, DialogPanel, DialogTitle } from '@headlessui/react'
import { useState } from 'react'

function Example() {
  let [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <button onClick={() => setIsOpen(true)}>Open dialog</button>
      <Dialog open={isOpen} onClose={() => setIsOpen(false)} className="relative z-50">
        <div className="fixed inset-0 flex w-screen items-center justify-center p-4">
          <DialogPanel className="max-w-lg space-y-4 border bg-white p-12">
            <DialogTitle className="font-bold">Deactivate account</DialogTitle>
            <Description>This will permanently deactivate your account</Description>
            <p>Are you sure you want to deactivate your account? All of your data will be permanently removed.</p>
            <div className="flex gap-4">
              <button onClick={() => setIsOpen(false)}>Cancel</button>
              <button onClick={() => setIsOpen(false)}>Deactivate</button>
            </div>
          </DialogPanel>
        </div>
      </Dialog>
    </>
  )
}
```

How you open and close the dialog is entirely up to you. You open a dialog by passing `true` to the `open` prop, and
close it by passing `false`. An `onClose` callback is also required for when the dialog is dismissed by pressing the
`Esc` key or by clicking outside of the `DialogPanel`.

## Styling

Style the `Dialog` and `DialogPanel` components using the `className` or `style` props like you would with any other
element. You can also introduce additional elements if needed to achieve a particular design.

```
import { Dialog, DialogPanel, DialogTitle } from '@headlessui/react'
import { useState } from 'react'

function Example() {
  let [isOpen, setIsOpen] = useState(true)

  return (

<Dialog open={isOpen} onClose={() => setIsOpen(false)} className="relative z-50">

<div className="fixed inset-0 flex w-screen items-center justify-center p-4">

<DialogPanel className="max-w-lg space-y-4 border bg-white p-12">

          <DialogTitle>Deactivate account order</DialogTitle>

          {/* ... */}
        </DialogPanel>
      </div>
    </Dialog>
  )
}
```

Clicking outside the `DialogPanel` component will close the dialog, so keep that in mind when deciding which styles to
apply to which elements.

## Examples

### Showing/hiding the dialog

Dialogs are controlled components, meaning that you have to provide and manage the open state yourself using the `open`
prop and the `onClose` callback.

The `onClose` callback is called when an dialog is dismissed, which happens when the user presses the `Esc` key
or clicks outside the `DialogPanel`. In this callback set the `open` state back to `false` to close the dialog.

```
import { Description, Dialog, DialogPanel, DialogTitle } from '@headlessui/react'
import { useState } from 'react'

function Example() {
  // The open/closed state lives outside of the `Dialog` and is managed by you

let [isOpen, setIsOpen] = useState(true)

function async handleDeactivate() {
    await fetch('/deactivate-account', { method: 'POST' })

setIsOpen(false)

}

  return (
    /*
      Pass `isOpen` to the `open` prop, and use `onClose` to set
      the state back to `false` when the user clicks outside of
      the dialog or presses the escape key.
    */

<Dialog open={isOpen} onClose={() => setIsOpen(false)}>

      <DialogPanel>
        <DialogTitle>Deactivate account</DialogTitle>
        <Description>This will permanently deactivate your account</Description>
        <p>Are you sure you want to deactivate your account? All of your data will be permanently removed.</p>

        {/*
          You can render additional buttons to dismiss your
          dialog by setting `isOpen` to `false`.
        */}
        <button onClick={() => setIsOpen(false)}>Cancel</button>
        <button onClick={handleDeactivate}>Deactivate</button>
      </DialogPanel>

</Dialog>

)
}
```

For situations where you don't have easy access to your open/close state, Headless UI provides a `CloseButton` component
that will close the nearest dialog ancestor when clicked. You can use the `as` prop to customize which element is being
rendered:

```
import { CloseButton } from '@headlessui/react'
import { MyDialog } from './my-dialog'
import { MyButton } from './my-button'

function Example() {
  return (
    <MyDialog>
      {/* ... */}

<CloseButton as={MyButton}>Cancel</CloseButton>

    </MyDialog>
  )
}
```

If you require more control, you can also use the `useClose` hook to imperatively close the dialog, say after running an
async action:

```
import { Dialog, useClose } from '@headlessui/react'

function MySearchForm() {

let close = useClose()

return (
    <form
      onSubmit={async (event) => {
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
    <Dialog>
      <MySearchForm />
      {/* ... */}
    </Dialog>
  )
}
```

The `useClose` hook must be used in a component that's nested within the `Dialog`, otherwise it will not work.

### Adding a backdrop

Use the `DialogBackdrop` component to add a backdrop behind your dialog panel. We recommend making the backdrop a
sibling to your panel container:

```
import { Description, Dialog, DialogBackdrop, DialogPanel, DialogTitle } from '@headlessui/react'
import { useState } from 'react'

function Example() {
  let [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <button onClick={() => setIsOpen(true)}>Open dialog</button>
      <Dialog open={isOpen} onClose={() => setIsOpen(false)} className="relative z-50">
        {/* The backdrop, rendered as a fixed sibling to the panel container */}

<DialogBackdrop className="fixed inset-0 bg-black/30" />

        {/* Full-screen container to center the panel */}
        <div className="fixed inset-0 flex w-screen items-center justify-center p-4">
          {/* The actual dialog panel  */}
          <DialogPanel className="max-w-lg space-y-4 bg-white p-12">
            <DialogTitle className="font-bold">Deactivate account</DialogTitle>
            <Description>This will permanently deactivate your account</Description>
            <p>Are you sure you want to deactivate your account? All of your data will be permanently removed.</p>
            <div className="flex gap-4">
              <button onClick={() => setIsOpen(false)}>Cancel</button>
              <button onClick={() => setIsOpen(false)}>Deactivate</button>
            </div>
          </DialogPanel>
        </div>
      </Dialog>
    </>
  )
}
```

This lets you [transition](#transitions) the backdrop and panel independently with their own animations, and rendering
it as a sibling ensures that it doesn't interfere with your ability to scroll long dialogs.

### Scrollable dialogs

Making a dialog scrollable is handled entirely in CSS, and the specific implementation depends on the design you are
trying to achieve.

Here's an example where the entire panel container is scrollable, and the panel itself moves as you scroll:

```
import { Description, Dialog, DialogPanel, DialogTitle } from '@headlessui/react'
import { useState } from 'react'

function Example() {
  let [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <button onClick={() => setIsOpen(true)}>Open dialog</button>
      <Dialog open={isOpen} onClose={() => setIsOpen(false)} className="relative z-50">

<div className="fixed inset-0 w-screen overflow-y-auto p-4">

<div className="flex min-h-full items-center justify-center">

            <DialogPanel className="max-w-lg space-y-4 border bg-white p-12">
              <DialogTitle className="font-bold">Deactivate account</DialogTitle>
              <Description>This will permanently deactivate your account</Description>
              <p>Are you sure you want to deactivate your account? All of your data will be permanently removed.</p>
              <div className="flex gap-4">
                <button onClick={() => setIsOpen(false)}>Cancel</button>
                <button onClick={() => setIsOpen(false)}>Deactivate</button>
              </div>
            </DialogPanel>

</div>

</div>

      </Dialog>
    </>
  )
}
```

When creating a scrollable dialog with a backdrop, make sure the backdrop is rendered *behind* the scrollable container,
otherwise the scroll wheel won't work when hovering over the backdrop, and the backdrop may obscure the scrollbar and
prevent users from clicking it with their mouse.

### Managing initial focus

By default, the `Dialog` component will focus the dialog element itself when opened, and pressing the `Tab` key
will cycle through any focusable elements within the dialog.

Focus is trapped within the dialog as long as it is rendered, so tabbing to the end will start cycling back through the
beginning again. All other application elements outside of the dialog will be marked as inert and thus not focusable.

If you'd like something other than the dialog's root element to receive focus when your dialog is opened, you can add
the `autoFocus` prop to any Headless UI form control:

```
import { Checkbox, Dialog, DialogPanel, DialogTitle, Field, Label } from '@headlessui/react'
import { useState } from 'react'

function Example() {
  let [isOpen, setIsOpen] = useState(true)
  let [isGift, setIsGift] = useState(false)

  function completeOrder() {
    // ...
  }

  return (
    <Dialog open={isOpen} onClose={() => setIsOpen(false)}>
      <DialogPanel>
        <DialogTitle>Complete your order</DialogTitle>

        <p>Your order is all ready!</p>

        <Field>

<Checkbox autoFocus value={isGift} onChange={setIsGift} />

          <Label>This order is a gift</Label>
        </Field>
        <button onClick={() => setIsOpen(false)}>Cancel</button>
        <button onClick={completeOrder}>Complete order</button>
      </DialogPanel>
    </Dialog>
  )
}
```

If the element you want to focus is not a Headless UI form control, you can add the `data-autofocus` attribute instead:

```
import { Dialog, DialogPanel, DialogTitle } from '@headlessui/react'
import { useState } from 'react'

function Example() {
  let [isOpen, setIsOpen] = useState(true)

  function completeOrder() {
    // ...
  }

  return (
    <Dialog open={isOpen} onClose={() => setIsOpen(false)}>
      <DialogPanel>
        <DialogTitle>Complete your order</DialogTitle>

        <p>Your order is all ready!</p>

        <button onClick={() => setIsOpen(false)}>Cancel</button>

<button data-autofocus onClick={completeOrder}>

          Complete order
        </button>
      </DialogPanel>
    </Dialog>
  )
}
```

### Rendering to a portal

Because of accessibility concerns, the `Dialog` component is automatically rendered in a
[portal](https://reactjs.org/docs/portals.html) under-the-hood.

Since dialogs and their backdrops take up the full page, you typically want to render them as a sibling to the root-most
node of your React application. That way you can rely on natural DOM ordering to ensure that their content is rendered
on top of your existing application UI.

It renders something like this:

```
<body>
  <div id="your-app">
    <!-- ... -->
  </div>
  <div id="headlessui-portal-root">
    <!-- Rendered `Dialog` -->
  </div>
</body>
```

This also makes it easy to apply scroll-locking to the rest of your application, as well as ensure that your dialog's
contents and backdrop are unobstructed to receive focus and click events.

### Adding transitions

To animate the opening and closing of the dialog, add the `transition` prop to the `Dialog` component and then use CSS
to style the different stages of the transition:

```
import { Description, Dialog, DialogPanel, DialogTitle } from '@headlessui/react'
import { useState } from 'react'

function Example() {
  let [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <button onClick={() => setIsOpen(true)}>Open dialog</button>
      <Dialog
        open={isOpen}
        onClose={() => setIsOpen(false)}

transition

className="fixed inset-0 flex w-screen items-center justify-center bg-black/30 p-4 transition duration-300 ease-out data-closed:opacity-0"

>
        <DialogPanel className="max-w-lg space-y-4 bg-white p-12">
          <DialogTitle className="font-bold">Deactivate account</DialogTitle>
          <Description>This will permanently deactivate your account</Description>
          <p>Are you sure you want to deactivate your account? All of your data will be permanently removed.</p>
          <div className="flex gap-4">
            <button onClick={() => setIsOpen(false)}>Cancel</button>
            <button onClick={() => setIsOpen(false)}>Deactivate</button>
          </div>
        </DialogPanel>
      </Dialog>
    </>
  )
}
```

To animate your backdrop and panel separately, add the `transition` prop to the `DialogBackdrop` and `DialogPanel`
components directly:

```
import { Description, Dialog, DialogBackdrop, DialogPanel, DialogTitle } from '@headlessui/react'
import { useState } from 'react'

function Example() {
  let [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <button onClick={() => setIsOpen(true)}>Open dialog</button>
      <Dialog open={isOpen} onClose={() => setIsOpen(false)} className="relative z-50">
        <DialogBackdrop transition className="fixed inset-0 bg-black/30 duration-300 ease-out data-closed:opacity-0" />

<div className="fixed inset-0 flex w-screen items-center justify-center p-4">

<DialogPanel

transition
            className="max-w-lg space-y-4 bg-white p-12 duration-300 ease-out data-closed:scale-95 data-closed:opacity-0"
          >

<DialogTitle className="text-lg font-bold">Deactivate account</DialogTitle>

<Description>This will permanently deactivate your account</Description>

            <p>Are you sure you want to deactivate your account? All of your data will be permanently removed.</p>
            <div className="flex gap-4">
              <button onClick={() => setIsOpen(false)}>Cancel</button>
              <button onClick={() => setIsOpen(false)}>Deactivate</button>
            </div>
          </DialogPanel>
        </div>
      </Dialog>
    </>
  )
}
```

Internally, the `transition` prop is implemented in the exact same way as the `Transition` component. See the
[Transition documentation](/react/transition) to learn more.

### Animating with Framer Motion

Headless UI also composes well with other animation libraries in the React ecosystem like
[Framer Motion](https://www.framer.com/motion/) and [React Spring](https://www.react-spring.io/). You just need to
expose some state to those libraries.

For example, to animate the dialog with Framer Motion, add the `static` prop to the `Dialog` component and then
conditionally render it based on the `open` state:

```
import { Description, Dialog, DialogPanel, DialogTitle } from '@headlessui/react'
import { AnimatePresence, motion } from 'framer-motion'
import { useState } from 'react'

function Example() {
  let [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <button onClick={() => setIsOpen(true)}>Open dialog</button>
      <AnimatePresence>

{isOpen && (

<Dialog static open={isOpen} onClose={() => setIsOpen(false)} className="relative z-50">

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black/30"
            />
            <div className="fixed inset-0 flex w-screen items-center justify-center p-4">
              <DialogPanel
                as={motion.div}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className="max-w-lg space-y-4 bg-white p-12"
              >
                <DialogTitle className="text-lg font-bold">Deactivate account</DialogTitle>
                <Description>This will permanently deactivate your account</Description>
                <p>Are you sure you want to deactivate your account? All of your data will be permanently removed.</p>
                <div className="flex gap-4">
                  <button onClick={() => setIsOpen(false)}>Cancel</button>
                  <button onClick={() => setIsOpen(false)}>Deactivate</button>
                </div>
              </DialogPanel>
            </div>

</Dialog>

)}

      </AnimatePresence>
    </>
  )
}
```

The `open` prop is still used to manage scroll-locking and focus trapping, but as long as `static` is present, the
actual element will always be rendered regardless of the `open` value, which allows you to control it yourself
externally.

## Keyboard interaction

|  |  |
| --- | --- |
| Command | Description |
| `Esc` | Closes any open Dialogs |
| `Tab` | Cycles through an open Dialog's contents |
| `Shift` + `Tab` | Cycles backwards through an open Dialog's contents |

## Component API

### Dialog

The main dialog component.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `open` | — | `Boolean`  Whether the `Dialog` is open or not. |
| `onClose` | — | `(false) => void`  Called when the `Dialog` is dismissed (via outside click of the `DialogPanel` or by pressing the `Esc` key). Typically used to close the dialog by setting `open` to false. |
| `as` | `div` | `String | Component`  The element or component the dialog should render as. |
| `autoFocus` | `false` | `Boolean`  Whether or not the dialog should receive focus when first rendered. |
| `transition` | `false` | `Boolean`  Whether the element should render transition attributes like `data-closed`, `data-enter` and `data-leave`. |
| `static` | `false` | `Boolean`  Whether the element should ignore the internally managed open/closed state. |
| `unmount` | `true` | `Boolean`  Whether the element should be unmounted or hidden based on the open/closed state. |
| `role` | `dialog` | `'dialog' | 'alertdialog'`  The `role` to apply to the dialog root element. |

|  |  |  |
| --- | --- | --- |
| Data Attribute | Render Prop | Description |
| `data-open` | `open` | `Boolean`  Whether or not the dialog is open. |

### DialogBackdrop

The visual backdrop behind your dialog panel.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `div` | `String | Component`  The element or component the dialog backdrop should render as. |
| `transition` | `false` | `Boolean`  Whether the element should render transition attributes like `data-closed`, `data-enter` and `data-leave`. |

|  |  |  |
| --- | --- | --- |
| Data Attribute | Render Prop | Description |
| `data-open` | `open` | `Boolean`  Whether or not the dialog is open. |

### DialogPanel

The main content area of your dialog. Clicking outside of this component will trigger the `onClose` of the `Dialog`
component.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `div` | `String | Component`  The element or component the dialog panel should render as. |
| `transition` | `false` | `Boolean`  Whether the element should render transition attributes like `data-closed`, `data-enter` and `data-leave`. |

|  |  |  |
| --- | --- | --- |
| Data Attribute | Render Prop | Description |
| `data-open` | `open` | `Boolean`  Whether or not the dialog is open. |

### DialogTitle

This is the title for your dialog. When this is used, it will set the `aria-labelledby` on the dialog.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `h2` | `String | Component`  The element or component the dialog title should render as. |

|  |  |  |
| --- | --- | --- |
| Data Attribute | Render Prop | Description |
| `data-open` | `open` | `Boolean`  Whether or not the dialog is open. |

### CloseButton

This button will close the nearest `Dialog` ancestor when clicked. Alternatively, use the `useClose` hook to
imperatively close the dialog.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `button` | `String | Component`  The element or component the close button should render as. |

## Styled examples

If you're interested in predesigned [Tailwind CSS modal and dialog component examples](https://tailwindui.com/components/application-ui/overlays/dialogs) using Headless UI, check out **Tailwind Plus** — a collection of beautifully designed and expertly crafted components built by us.

It's a great way to support our work on open-source projects like this and makes it possible for us to improve them and keep them well-maintained.

[Explore more predesigned examples →](https://tailwindcss.com/plus)

[![Various components from Tailwind UI](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Ftailwind-plus.434a3ca6.png&w=3840&q=75)](https://tailwindcss.com/plus)

On this page