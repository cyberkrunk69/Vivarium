# Radio Group

Source: https://headlessui.com/react/radio-group

---

React

[Vue](/v1/vue/radio-group)

# Radio Group

Radio groups give you the same functionality as native HTML radio inputs, without any of the styling. They're perfect
for building out custom UIs for selectors.

PreviewCode

## Installation

To get started, install Headless UI via npm:

```
npm install @headlessui/react
```

## Basic example

Radio groups are built using the `RadioGroup`, `Radio`, `Field`, and `Label` components.

```
import { Field, Label, Radio, RadioGroup } from '@headlessui/react'
import { useState } from 'react'

const plans = ['Startup', 'Business', 'Enterprise']

function Example() {
  let [selected, setSelected] = useState(plans[0])

  return (
    <RadioGroup value={selected} onChange={setSelected} aria-label="Server size">
      {plans.map((plan) => (
        <Field key={plan} className="flex items-center gap-2">
          <Radio
            value={plan}
            className="group flex size-5 items-center justify-center rounded-full border bg-white data-checked:bg-blue-400"
          >
            <span className="invisible size-2 rounded-full bg-white group-data-checked:visible" />
          </Radio>
          <Label>{plan}</Label>
        </Field>
      ))}
    </RadioGroup>
  )
}
```

## Styling

Headless UI keeps track of a lot of state about each component, like which radio group option is currently checked,
whether a popover is open or closed, or which item in a menu is currently focused via the keyboard.

But because the components are headless and completely unstyled out of the box, you can't see this information in your
UI until you provide the styles you want for each state yourself.

### Using data attributes

The easiest way to style the different states of a Headless UI component is using the `data-*` attributes that each
component exposes.

For example, the `Radio` component exposes a `data-checked` attribute, which tells you if the radio is currently
checked, and a `data-disabled` attribute, which tells you if the radio is currently disabled.

```
<!-- Rendered `Radio` -->
<span role="radio" data-checked data-disabled>
  <!-- ... -->
</span>
```

Use the [CSS attribute selector](https://developer.mozilla.org/en-US/docs/Web/CSS/Attribute_selectors) to conditionally
apply styles based on the presence of these data attributes. If you're using Tailwind CSS, the
[data attribute modifier](https://tailwindcss.com/docs/hover-focus-and-other-states#data-attributes) makes this easy:

```
import { Field, Label, Radio, RadioGroup } from '@headlessui/react'
import { useState } from 'react'

const plans = [
  { name: 'Startup', available: true },
  { name: 'Business', available: true },
  { name: 'Enterprise', available: false },
]

function Example() {
  let [selected, setSelected] = useState(plans[0])

  return (
    <RadioGroup value={selected} onChange={setSelected} aria-label="Server size">
      {plans.map((plan) => (
        <Field key={plan.name} disabled={!plan.available} className="flex items-center gap-2">
          <Radio
            value={plan}

className="group flex size-5 items-center justify-center rounded-full border bg-white data-checked:bg-blue-400 data-disabled:bg-gray-100"

>

<span className="invisible size-2 rounded-full bg-white group-data-checked:visible" />

          </Radio>

<Label className="data-disabled:opacity-50">{plan.name}</Label>

        </Field>
      ))}
    </RadioGroup>
  )
}
```

### Using render props

Each component also exposes information about its current state via
[render props](https://reactjs.org/docs/render-props.html) that you can use to conditionally apply different styles or
render different content.

For example, the `Radio` component exposes a `checked` state, which tells you if the radio is currently checked, and a
`disabled` state, which tells you if the radio is currently disabled.

```
import { Field, Label, Radio, RadioGroup } from '@headlessui/react'
import clsx from 'clsx'
import { Fragment, useState } from 'react'

const plans = [
  { name: 'Startup', available: true },
  { name: 'Business', available: true },
  { name: 'Enterprise', available: false },
]

function Example() {
  let [selected, setSelected] = useState(plans[0])

  return (
    <RadioGroup value={selected} onChange={setSelected} aria-label="Server size">
      {plans.map((plan) => (
        <Field key={plan.name} disabled={!plan.available} className="flex items-center gap-2">

<Radio as={Fragment} value={plan}>

{({ checked, disabled }) => (

<span
                className={clsx(
                  'group flex size-5 items-center justify-center rounded-full border',

checked ? 'bg-blue-400' : 'bg-white',

disabled && 'bg-gray-100'

)}
              >

{checked && <span className="size-2 rounded-full bg-white" />}

              </span>
            )}
          </Radio>

<Label as={Fragment}>

{({ disabled }) => <label className={disabled && 'opacity-50'}>{plan.name}</label>}

</Label>

        </Field>
      ))}
    </RadioGroup>
  )
}
```

See the [component API](#component-api) for a list of all the available render props.

## Examples

### Adding a description

Use the `Description` component within a `Field` to automatically associate it with a `Radio` using the
`aria-describedby` attribute:

```
import { Description, Field, Label, Radio, RadioGroup } from '@headlessui/react'
import { useState } from 'react'

const plans = [

{ name: 'Startup', description: '12GB, 6 CPUs, 256GB SSD disk' },

{ name: 'Business', description: '16GB, 8 CPUs, 512GB SSD disk' },

{ name: 'Enterprise', description: '32GB, 12 CPUs, 1TB SSD disk' },

]

function Example() {
  let [selected, setSelected] = useState(plans[0])

  return (
    <RadioGroup value={selected} onChange={setSelected} aria-label="Server size">
      {plans.map((plan) => (
        <Field key={plan} className="flex items-baseline gap-2">
          <Radio
            value={plan}
            className="group flex size-5 items-center justify-center rounded-full border bg-white data-checked:bg-blue-400"
          >
            <span className="invisible size-2 rounded-full bg-white group-data-checked:visible" />
          </Radio>
          <div>
            <Label>{plan.name}</Label>

<Description className="opacity-50">{plan.description}</Description>

          </div>
        </Field>
      ))}
    </RadioGroup>
  )
}
```

### Using with HTML forms

If you add the `name` prop to your `RadioGroup`, a hidden `input` element will be rendered and kept in sync with the
radio group state.

```
import { Field, Fieldset, Label, Legend, Radio, RadioGroup } from '@headlessui/react'
import { useState } from 'react'

const plans = ['Startup', 'Business', 'Enterprise']

function Example() {
  const [selected, setSelected] = useState(plans[0])

  return (

<form action="/plans" method="post">

      <Fieldset>
        <Legend>Server size</Legend>

<RadioGroup name="plan" value={selected} onChange={setSelected}>

          {plans.map((plan) => (
            <Field key={plan}>
              <Radio value={plan} />
              <Label>{plan}</Label>
            </Field>
          ))}
        </RadioGroup>
      </Fieldset>
      <button>Submit</button>

</form>

)
}
```

This lets you use a radio group inside a native HTML `<form>` and make traditional form submissions as if your radio
group was a native HTML form control.

Basic values like strings will be rendered as a single hidden input containing that value, but complex values like
objects will be encoded into multiple inputs using square bracket notation for the names.

```
<!-- Rendered hidden input -->
<input type="hidden" name="plan" value="startup" />
```

### Using as uncontrolled

If you omit the `value` prop, Headless UI will track its state internally for you, allowing you to use it as an
[uncontrolled component](https://reactjs.org/docs/uncontrolled-components.html).

When uncontrolled, use the `defaultValue` prop to provide an initial value to the `RadioGroup`.

```
import { useState } from 'react'
import { RadioGroup, Radio, Fieldset, Legend, Field, Label } from '@headlessui/react'

const plans = ['Startup', 'Business', 'Enterprise']

function Example() {
  return (
    <form action="/plans" method="post">
      <Fieldset>
        <Legend>Server size</Legend>

<RadioGroup name="plan" defaultValue={plans[0]}>

          {plans.map((plan) => (
            <Field key={plan}>
              <Radio value={plan} />
              <Label>{plan}</Label>
            </Field>
          ))}
        </RadioGroup>
      </Fieldset>
    </form>
  )
}
```

This can simplify your code when using the combobox [with HTML forms](#using-with-html-forms) or with form APIs that
collect their state using [FormData](https://developer.mozilla.org/en-US/docs/Web/API/FormData) instead of tracking it
using React state.

Any `onChange` prop you provide will still be called when the component's value changes in case you need to run any side
effects, but you won't need to use it to track the component's state yourself.

### Binding objects as values

Unlike native HTML form controls, which only allow you to provide strings as values, Headless UI supports binding
complex objects as well.

```
import { Field, Label, Radio, RadioGroup } from '@headlessui/react'
import { useState } from 'react'

const plans = [

{ id: 1, name: 'Startup', available: true },

{ id: 2, name: 'Business', available: true },

{ id: 3, name: 'Enterprise', available: false },

]

function Example() {
  const [selected, setSelected] = useState(plans[0])

  return (

<RadioGroup value={selected} onChange={setSelected} aria-label="Server size">

      {plans.map((plan) => (
        <Field key={plan.id}>

<Radio value={plan} disabled={!plan.available} />

          <Label>{plan.name}</Label>
        </Field>
      ))}
    </RadioGroup>
  )
}
```

When binding objects as values, it's important to make sure that you use the *same instance* of the object as both the
`value` of the `RadioGroup` as well as the corresponding `Radio`, otherwise they will fail to be equal and cause the
radio group to behave incorrectly.

To make it easier to work with different instances of the same object, you can use the `by` prop to compare the objects
by a particular field instead of comparing by object identity.

When you pass an object to the `value` prop, `by` will default to `id` when present, but you can set it to any field you
like:

```
import { Field, Label, Radio, RadioGroup } from '@headlessui/react'
import { useState } from 'react'

const plans = [
  { name: 'Startup', available: true },
  { name: 'Business', available: true },
  { name: 'Enterprise', available: false },
]

function Example() {
  const [selected, setSelected] = useState(plans[0])

  return (

<RadioGroup value={selected} by="name" onChange={setSelected} aria-label="Server size">

      {plans.map((plan) => (
        <Field key={plan.id}>
          <Radio value={plan} disabled={!plan.available} />
          <Label>{plan.name}</Label>
        </Field>
      ))}
    </RadioGroup>
  )
}
```

You can also pass your own comparison function to the `by` prop if you'd like complete control over how objects are
compared:

```
import { Field, Label, Radio, RadioGroup } from '@headlessui/react'
import { useState } from 'react'

const plans = [

{ id: 1, name: 'Startup', available: true },

{ id: 2, name: 'Business', available: true },

{ id: 3, name: 'Enterprise', available: false },

]

function comparePlans(a, b) {

return a.name.toLowerCase() === b.name.toLowerCase()

}

function Example() {
  const [selected, setSelected] = useState(plans[0])

  return (

<RadioGroup value={selected} by={comparePlans} onChange={setSelected} aria-label="Server size">

      {plans.map((plan) => (
        <Field key={plan.id}>
          <Radio value={plan} disabled={!plan.available} />
          <Label>{plan.name}</Label>
        </Field>
      ))}
    </RadioGroup>
  )
}
```

## Keyboard interaction

All interactions apply when a `Radio` component is focused.

|  |  |
| --- | --- |
| Command | Description |
| `ArrowDown` or `ArrowUp` or `ArrowLeft` or `ArrowRight` | Cycles through a `RadioGroup`'s options |
| `Space`when no option is selected yet | Selects the focused option |
| `Enter`when in a form | Submits the form |

## Component API

### RadioGroup

The main radio group component.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `div` | `String | Component`  The element or component the radio group should render as. |
| `value` | — | `T | undefined`  The current selected value in the `RadioGroup`. |
| `defaultValue` | — | `T`  The default value when using as an uncontrolled component. |
| `by` | — | `keyof T | ((a: T, z: T) => boolean)`  Use this to compare objects by a particular field, or pass your own comparison function for complete control over how objects are compared.  When you pass an object to the `value` prop, `by` will default to`id` when present. |
| `onChange` | — | `(value: T) => void`  The function called to update the `RadioGroup` value. |
| `disabled` | `false` | `boolean`  Use this to disable the radio group and all of its radios. |
| `name` | — | `String`  The name used when using the radio group inside a form. |
| `form` | — | `String`  The id of the form that the radio group belongs to.  If `name` is provided but `form` is not, the radio group will add its state to the nearest ancestor `form` element. |

|  |  |  |
| --- | --- | --- |
| Data Attribute | Render Prop | Description |
| — | `value` | `T`  The selected value. |

### Radio

The component for each selectable option.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `span` | `String | Component`  The element or component the radio should render as. |
| `value` | — | `T | undefined`  The value of this `Radio`. The type should match the type of the `value` in the `RadioGroup` component. |
| `disabled` | `false` | `Boolean`  Whether or not the radio is disabled. |
| `autoFocus` | `false` | `Boolean`  Whether or not the radio should receive focus when first rendered. |

|  |  |  |
| --- | --- | --- |
| Data Attribute | Render Prop | Description |
| `data-checked` | `checked` | `Boolean`  Whether or not the radio is checked. |
| `data-disabled` | `disabled` | `Boolean`  Whether or not the radio is disabled. |
| `data-focus` | `focus` | `Boolean`  Whether or not the radio is focused. |
| `data-hover` | `hover` | `Boolean`  Whether or not the radio is hovered. |
| `data-autofocus` | `autofocus` | `Boolean`  Whether or not the `autoFocus` prop was set to `true`. |

## Styled examples

If you're interested in predesigned [Tailwind CSS radio group examples](https://tailwindui.com/components/application-ui/forms/radio-groups) using Headless UI, check out **Tailwind Plus** — a collection of beautifully designed and expertly crafted components built by us.

It's a great way to support our work on open-source projects like this and makes it possible for us to improve them and keep them well-maintained.

[Explore more predesigned examples →](https://tailwindcss.com/plus)

[![Various components from Tailwind UI](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Ftailwind-plus.434a3ca6.png&w=3840&q=75)](https://tailwindcss.com/plus)

On this page