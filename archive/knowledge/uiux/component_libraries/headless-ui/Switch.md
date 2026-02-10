# Switch

Source: https://headlessui.com/react/switch

---

React

[Vue](/v1/vue/switch)

# Switch

Switches are a pleasant interface for toggling a value between two states, and offer the same semantics and keyboard
navigation as native checkbox elements.

PreviewCode

## Installation

To get started, install Headless UI via npm:

```
npm install @headlessui/react
```

## Basic example

Switches are built using the `Switch` component. You can toggle your switch by clicking directly on the component, or by
pressing the spacebar while it's focused.

Toggling the switch calls the `onChange` function with a negated version of the `checked` value.

```
import { Switch } from '@headlessui/react'
import { useState } from 'react'

function Example() {
  const [enabled, setEnabled] = useState(false)

  return (
    <Switch
      checked={enabled}
      onChange={setEnabled}
      className="group inline-flex h-6 w-11 items-center rounded-full bg-gray-200 transition data-checked:bg-blue-600"
    >
      <span className="size-4 translate-x-1 rounded-full bg-white transition group-data-checked:translate-x-6" />
    </Switch>
  )
}
```

## Styling

Headless UI keeps track of a lot of state about each component, like whether or not a switch is checked, whether a
popover is open or closed, or which item in a menu is currently focused via the keyboard.

But because the components are headless and completely unstyled out of the box, you can't see this information in your
UI until you provide the styles you want for each state yourself.

### Using data attributes

The easiest way to style the different states of a Headless UI component is using the `data-*` attributes that each
component exposes.

For example, the `Switch` component exposes a `data-checked` attribute, which tells you if the switch is currently
checked, and a `data-disabled` attribute, which tells you if the switch is currently disabled.

```
<!-- Rendered `Switch` -->
<button data-checked data-disabled>
  <!-- ... -->
</button>
```

Use the [CSS attribute selector](https://developer.mozilla.org/en-US/docs/Web/CSS/Attribute_selectors) to conditionally
apply styles based on the presence of these data attributes. If you're using Tailwind CSS, the
[data attribute modifier](https://tailwindcss.com/docs/hover-focus-and-other-states#data-attributes) makes this easy:

```
import { Switch } from '@headlessui/react'
import { useState } from 'react'

function Example() {
  const [enabled, setEnabled] = useState(false)

  return (
    <Switch
      checked={enabled}
      onChange={setEnabled}

className="group inline-flex h-6 w-11 items-center rounded-full bg-gray-200 data-checked:bg-blue-600 data-disabled:cursor-not-allowed data-disabled:opacity-50"

>

<span className="size-4 translate-x-1 rounded-full bg-white transition group-data-checked:translate-x-6" />

    </Switch>
  )
}
```

See the [component API](#component-api) for a list of all the available data attributes.

### Using render props

Each component also exposes information about its current state via
[render props](https://reactjs.org/docs/render-props.html) that you can use to conditionally apply different styles or
render different content.

For example, the `Switch` component exposes a `checked` state, which tells you if the switch is currently checked, and a
`disabled` state, which tells you if the switch is currently disabled.

```
import { Switch } from '@headlessui/react'
import clsx from 'clsx'
import { Fragment, useState } from 'react'

function Example() {
  const [enabled, setEnabled] = useState(false)

  return (
    <Switch checked={enabled} onChange={setEnabled} as={Fragment}>

{({ checked, disabled }) => (

<button
          className={clsx(
            'group inline-flex h-6 w-11 items-center rounded-full',

checked ? 'bg-blue-600' : 'bg-gray-200',

disabled && 'cursor-not-allowed opacity-50'

)}
        >
          <span className="sr-only">Enable notifications</span>
          <span

className={clsx('size-4 rounded-full bg-white transition', checked ? 'translate-x-6' : 'translate-x-1')}

/>
        </button>

)}

    </Switch>
  )
}
```

See the [component API](#component-api) for a list of all the available render props.

## Examples

### Adding a label

Wrap a `Label` and `Switch` with the `Field` component to automatically associate them using a generated ID:

```
import { Field, Label, Switch } from '@headlessui/react'
import { useState } from 'react'

function Example() {
  const [enabled, setEnabled] = useState(false)

  return (

<Field>

<Label>Enable notifications</Label>

      <Switch
        checked={enabled}
        onChange={setEnabled}
        className="group inline-flex h-6 w-11 items-center rounded-full bg-gray-200 transition data-checked:bg-blue-600"
      >
        <span className="size-4 translate-x-1 rounded-full bg-white transition group-data-checked:translate-x-6" />
      </Switch>

</Field>

)
}
```

By default, clicking the `Label` will toggle the `Switch`, just like labels do for native HTML checkboxes. If you'd like
to make the `Label` non-clickable, you can add a `passive` prop to the `Label` component:

```
<Label passive>Enable beta features</Label>
```

### Adding a description

Use the `Description` component within a `Field` to automatically associate it with a `Switch` using the
`aria-describedby` attribute:

```
import { Description, Field, Label, Switch } from '@headlessui/react'
import { useState } from 'react'

function Example() {
  const [enabled, setEnabled] = useState(false)

  return (

<Field>

      <Label>Enable notifications</Label>

<Description>Get notified about important changes in your projects.</Description>

      <Switch
        checked={enabled}
        onChange={setEnabled}
        className="group inline-flex h-6 w-11 items-center rounded-full bg-gray-200 transition data-checked:bg-blue-600"
      >
        <span className="size-4 translate-x-1 rounded-full bg-white transition group-data-checked:translate-x-6" />
      </Switch>

</Field>

)
}
```

### Disabling a switch

Add the `disabled` prop to the `Field` component to disable a `Switch` and its associated `Label` and `Description`:

```
import { Description, Field, Label, Switch } from '@headlessui/react'
import { useState } from 'react'

function Example() {
  const [enabled, setEnabled] = useState(false)

  return (

<Field disabled>

      <Label className="data-disabled:opacity-50">Enable notifications</Label>
      <Description className="data-disabled:opacity-50">
        Get notified about important changes in your projects.
      </Description>
      <Switch
        checked={enabled}
        onChange={setEnabled}
        className="group inline-flex h-6 w-11 items-center rounded-full bg-gray-200 transition data-checked:bg-blue-600 data-disabled:cursor-not-allowed data-disabled:opacity-50"
      >
        <span className="size-4 translate-x-1 rounded-full bg-white transition group-data-checked:translate-x-6" />
      </Switch>
    </Field>
  )
}
```

You can also disable a switch outside of a `Field` by adding the disabled prop directly to the `Switch` itself.

### Using with HTML forms

If you add the `name` prop to your `Switch`, a hidden `input` element will be rendered and kept in sync with the switch
state.

```
import { Switch } from '@headlessui/react'
import { useState } from 'react'

function Example() {
  const [enabled, setEnabled] = useState(false)

  return (
    <form action="/accounts" method="post">
      <Switch
        checked={enabled}
        onChange={setEnabled}

name="terms-of-service"

className="group inline-flex h-6 w-11 items-center rounded-full bg-gray-200 transition data-checked:bg-blue-600"
      >
        <span className="size-4 translate-x-1 rounded-full bg-white transition group-data-checked:translate-x-6" />
      </Switch>
      <button>Submit</button>
    </form>
  )
}
```

This lets you use a switch inside a native HTML `<form>` and make traditional form submissions as if your switch was a
native HTML form control.

By default, the value will be `on` when the switch is checked, and not present when the switch is unchecked.

```
<!-- Rendered hidden input -->
<input type="hidden" name="terms-of-service" value="on" />
```

You can customize the value if needed by using the `value` prop:

```
import { Switch } from '@headlessui/react'
import { useState } from 'react'

function Example() {
  const [enabled, setEnabled] = useState(false)

  return (
    <form action="/accounts" method="post">
      <Switch
        checked={enabled}
        onChange={setEnabled}
        name="terms-of-service"

value="accept"

className="group inline-flex h-6 w-11 items-center rounded-full bg-gray-200 transition data-checked:bg-blue-600"
      >
        <span className="size-4 translate-x-1 rounded-full bg-white transition group-data-checked:translate-x-6" />
      </Switch>
      <button>Submit</button>
    </form>
  )
}
```

The hidden input will then use your custom value when the switch is checked:

```
<!-- Rendered hidden input -->
<input type="hidden" name="terms-of-service" value="accept" />
```

Basic values like strings will be rendered as a single hidden input containing that value, but complex values like
objects will be encoded into multiple inputs using a square bracket notation for the names.

### Using as uncontrolled

If you omit the `checked` prop, Headless UI will track its state internally for you, allowing you to use it as an
[uncontrolled component](https://reactjs.org/docs/uncontrolled-components.html).

When uncontrolled, you can check the `Switch` by default using the `defaultChecked` prop.

```
import { Switch } from '@headlessui/react'

function Example() {
  return (
    <form action="/accounts" method="post">
      <Switch

defaultChecked={true}

name="terms-of-service"
        className="group inline-flex h-6 w-11 items-center rounded-full bg-gray-200 transition data-checked:bg-blue-600"
      >
        <span className="size-4 translate-x-1 rounded-full bg-white transition group-data-checked:translate-x-6" />
      </Switch>
      <button>Submit</button>
    </form>
  )
}
```

This can simplify your code when using the switch [with HTML forms](#using-with-html-forms) or with form APIs that
collect their state using [FormData](https://developer.mozilla.org/en-US/docs/Web/API/FormData) instead of tracking it
using React state.

Any `onChange` prop you provide will still be called when the component's value changes in case you need to run any side
effects, but you won't need to use it to track the component's state yourself.

### Adding transitions

Because switches are typically always rendered to the DOM (rather than being mounted/unmounted like other components),
simple CSS transitions are often enough to animate your switch:

```
import { Switch } from '@headlessui/react'
import { useState } from 'react'

function Example() {
  const [enabled, setEnabled] = useState(false)

  return (
    <Switch
      checked={enabled}
      onChange={setEnabled}

className="group inline-flex h-6 w-11 items-center rounded-full bg-gray-200 transition data-checked:bg-blue-600"

>

<span className="size-4 translate-x-1 rounded-full bg-white transition group-data-checked:translate-x-6" />

    </Switch>
  )
}
```

Because they're renderless, Headless UI components also compose well with other animation libraries in the React
ecosystem like [Framer Motion](https://www.framer.com/motion/) and [React Spring](https://www.react-spring.io/).

### Rendering as different element

The `Switch` component renders a `button` by default.

Use the `as` prop to render the component as a different element or as your own custom component, making sure your
custom components [forward refs](https://react.dev/reference/react/forwardRef) so that Headless UI can wire things up
correctly.

```
import { Switch } from '@headlessui/react'
import { useState } from 'react'

function Example() {
  const [enabled, setEnabled] = useState(false)

  return (
    <Switch

as="div"

checked={enabled}
      onChange={setEnabled}
      className="group inline-flex h-6 w-11 items-center rounded-full bg-gray-200 transition data-checked:bg-blue-600"
    >
      <span className="size-4 translate-x-1 rounded-full bg-white transition group-data-checked:translate-x-6" />
    </Switch>
  )
}
```

## Keyboard interaction

|  |  |
| --- | --- |
| Command | Description |
| `Space`when a `Switch` is focused | Toggles the Switch |
| `Enter`when in a form | Submits the form |

## Component API

### Switch

The main switch component.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `button` | `String | Component`  The element or component the switch should render as. |
| `checked` | — | `Boolean`  Whether or not the switch is checked. |
| `defaultChecked` | — | `T`  The default checked value when using as an uncontrolled component. |
| `onChange` | — | `(value: Boolean) => void`  The function to call when the switch is toggled. |
| `name` | — | `String`  The name used when using the switch inside a form. |
| `form` | — | `String`  The id of the form that the switch belongs to.  If `name` is provided but `form` is not, the switch will add its state to the nearest ancestor `form` element. |
| `value` | — | `String`  The value used when using this component inside a form, if it is checked. |

|  |  |  |
| --- | --- | --- |
| Data Attribute | Render Prop | Description |
| `data-checked` | `checked` | `Boolean`  Whether or not the switch is checked. |
| `data-disabled` | `disabled` | `Boolean`  Whether or not the switch is disabled. |
| `data-focus` | `focus` | `Boolean`  Whether or not the switch is focused. |
| `data-hover` | `hover` | `Boolean`  Whether or not the switch is hovered. |
| `data-active` | `active` | `Boolean`  Whether or not the switch is in an active or pressed state. |
| `data-autofocus` | `autofocus` | `Boolean`  Whether or not the `autoFocus` prop was set to `true`. |
| `data-changing` | `changing` | `Boolean`  Whether or not the checked state is currently changing.  When the `checked` state changes, `changing` will be `true` for two animation frames, allowing you to fine-tune transitions. |

### Field

Groups a `Label`, `Description`, and form control together.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `div` | `String | Component`  The element or component the field should render as. |
| `disabled` | `false` | `Boolean`  Whether or not the field is disabled. |

|  |  |  |
| --- | --- | --- |
| Data Attribute | Render Prop | Description |
| `data-disabled` | `disabled` | `Boolean`  Whether or not the field is disabled. |

### Label

The `Label` component labels a form control.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `label` | `String | Component`  The element or component the label should render as. |
| `passive` | `false` | `Boolean`  When true, clicking the label won't focus the associated form control. |

|  |  |  |
| --- | --- | --- |
| Data Attribute | Render Prop | Description |
| `data-disabled` | `disabled` | `Boolean`  Whether or not the parent `Field` is disabled. |

### Description

The `Description` component describes a form control.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `p` | `String | Component`  The element or component the description should render as. |

|  |  |  |
| --- | --- | --- |
| Data Attribute | Render Prop | Description |
| `data-disabled` | `disabled` | `Boolean`  Whether or not the parent `Field` is disabled. |

## Styled examples

If you're interested in predesigned [Tailwind CSS toggle and switch examples](https://tailwindui.com/components/application-ui/forms/toggles) using Headless UI, check out **Tailwind Plus** — a collection of beautifully designed and expertly crafted components built by us.

It's a great way to support our work on open-source projects like this and makes it possible for us to improve them and keep them well-maintained.

[Explore more predesigned examples →](https://tailwindcss.com/plus)

[![Various components from Tailwind UI](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Ftailwind-plus.434a3ca6.png&w=3840&q=75)](https://tailwindcss.com/plus)

On this page