# Listbox

Source: https://headlessui.com/react/listbox

---

React

[Vue](/v1/vue/listbox)

# Listbox

Listboxes are a great foundation for building custom, accessible select menus for your app, complete with robust
support for keyboard navigation.

PreviewCode

## Installation

To get started, install Headless UI via npm:

```
npm install @headlessui/react
```

## Basic example

Listboxes are built using the `Listbox`, `ListboxButton`, `ListboxSelectedOption`, `ListboxOptions`, and `ListboxOption`
components.

The `ListboxButton` will automatically open/close the `ListboxOptions` when clicked, and when the listbox is open, the
list of options receives focus and is automatically navigable via the keyboard.

```
import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/react'
import { useState } from 'react'

const people = [
  { id: 1, name: 'Durward Reynolds' },
  { id: 2, name: 'Kenton Towne' },
  { id: 3, name: 'Therese Wunsch' },
  { id: 4, name: 'Benedict Kessler' },
  { id: 5, name: 'Katelyn Rohan' },
]

function Example() {
  const [selectedPerson, setSelectedPerson] = useState(people[0])

  return (
    <Listbox value={selectedPerson} onChange={setSelectedPerson}>
      <ListboxButton>{selectedPerson.name}</ListboxButton>
      <ListboxOptions anchor="bottom">
        {people.map((person) => (
          <ListboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
            {person.name}
          </ListboxOption>
        ))}
      </ListboxOptions>
    </Listbox>
  )
}
```

## Styling

Headless UI keeps track of a lot of state about each component, like which listbox option is currently selected, whether
a popover is open or closed, or which item in a menu is currently focused via the keyboard.

But because the components are headless and completely unstyled out of the box, you can't see this information in your
UI until you provide the styles you want for each state yourself.

### Using data attributes

The easiest way to style the different states of a Headless UI component is using the `data-*` attributes that each
component exposes.

For example, the `ListboxOption` component exposes a `data-focus` attribute, which tells you if the option is currently
focused via the mouse or keyboard, and a `data-selected` attribute, which tells you if that option matches the current
`value` of the `Listbox`.

```
<!-- Rendered `ListboxOption` -->
<div data-focus data-selected>Arlene Mccoy</div>
```

Use the [CSS attribute selector](https://developer.mozilla.org/en-US/docs/Web/CSS/Attribute_selectors) to conditionally
apply styles based on the presence of these data attributes. If you're using Tailwind CSS, the
[data attribute modifier](https://tailwindcss.com/docs/hover-focus-and-other-states#data-attributes) makes this easy:

```
import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/react'
import { CheckIcon } from '@heroicons/react/20/solid'
import { useState } from 'react'

const people = [
  { id: 1, name: 'Durward Reynolds' },
  { id: 2, name: 'Kenton Towne' },
  { id: 3, name: 'Therese Wunsch' },
  { id: 4, name: 'Benedict Kessler' },
  { id: 5, name: 'Katelyn Rohan' },
]

function Example() {
  const [selectedPerson, setSelectedPerson] = useState(people[0])

  return (
    <Listbox value={selectedPerson} onChange={setSelectedPerson}>
      <ListboxButton>{selectedPerson.name}</ListboxButton>
      <ListboxOptions anchor="bottom">
        {people.map((person) => (

<ListboxOption key={person.id} value={person} className="group flex gap-2 bg-white data-focus:bg-blue-100">

<CheckIcon className="invisible size-5 group-data-selected:visible" />

            {person.name}
          </ListboxOption>
        ))}
      </ListboxOptions>
    </Listbox>
  )
}
```

See the [component API](#component-api) for a list of all the available data attributes.

### Using render props

Each component also exposes information about its current state via
[render props](https://reactjs.org/docs/render-props.html) that you can use to conditionally apply different styles or
render different content.

For example, the `ListboxOption` component exposes a `focus` state, which tells you if the option is currently focused
via the mouse or keyboard, and a `selected` state, which tells you if that option matches the current `value` of the
`Listbox`.

```
import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/react'
import { CheckIcon } from '@heroicons/react/20/solid'
import clsx from 'clsx'
import { Fragment, useState } from 'react'

const people = [
  { id: 1, name: 'Durward Reynolds' },
  { id: 2, name: 'Kenton Towne' },
  { id: 3, name: 'Therese Wunsch' },
  { id: 4, name: 'Benedict Kessler' },
  { id: 5, name: 'Katelyn Rohan' },
]

function Example() {
  const [selectedPerson, setSelectedPerson] = useState(people[0])

  return (
    <Listbox value={selectedPerson} onChange={setSelectedPerson}>
      <ListboxButton>{selectedPerson.name}</ListboxButton>
      <ListboxOptions anchor="bottom">
        {people.map((person) => (

<ListboxOption key={person.id} value={person} as={Fragment}>

{({ focus, selected }) => (

<div className={clsx('flex gap-2', focus && 'bg-blue-100')}>

<CheckIcon className={clsx('size-5', !selected && 'invisible')} />

{person.name}

</div>

)}

</ListboxOption>

))}
      </ListboxOptions>
    </Listbox>
  )
}
```

See the [component API](#component-api) for a list of all the available render props.

## Examples

### Adding a label

Wrap a `Label` and `Listbox` with the `Field` component to automatically associate them using a generated ID:

```
import { Field, Label, Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/react'
import { useState } from 'react'

const people = [
  { id: 1, name: 'Durward Reynolds' },
  { id: 2, name: 'Kenton Towne' },
  { id: 3, name: 'Therese Wunsch' },
  { id: 4, name: 'Benedict Kessler' },
  { id: 5, name: 'Katelyn Rohan' },
]

function Example() {
  const [selectedPerson, setSelectedPerson] = useState(people[0])

  return (

<Field>

<Label>Assignee:</Label>

      <Listbox value={selectedPerson} onChange={setSelectedPerson}>
        <ListboxButton>{selectedPerson.name}</ListboxButton>
        <ListboxOptions anchor="bottom">
          {people.map((person) => (
            <ListboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
              {person.name}
            </ListboxOption>
          ))}
        </ListboxOptions>
      </Listbox>

</Field>

)
}
```

### Adding a description

Use the `Description` component within a `Field` to automatically associate it with a `Listbox` using the
`aria-describedby` attribute:

```
import { Description, Field, Label, Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/react'
import { useState } from 'react'

const people = [
  { id: 1, name: 'Durward Reynolds' },
  { id: 2, name: 'Kenton Towne' },
  { id: 3, name: 'Therese Wunsch' },
  { id: 4, name: 'Benedict Kessler' },
  { id: 5, name: 'Katelyn Rohan' },
]

function Example() {
  const [selectedPerson, setSelectedPerson] = useState(people[0])

  return (

<Field>

      <Label>Assignee:</Label>

<Description>This person will have full access to this project.</Description>

      <Listbox value={selectedPerson} onChange={setSelectedPerson}>
        <ListboxButton>{selectedPerson.name}</ListboxButton>
        <ListboxOptions anchor="bottom">
          {people.map((person) => (
            <ListboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
              {person.name}
            </ListboxOption>
          ))}
        </ListboxOptions>
      </Listbox>

</Field>

)
}
```

### Disabling a listbox

Add the `disabled` prop to the `Field` component to disable a `Listbox` and its associated `Label` and `Description`:

```
import { Description, Field, Label, Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/react'
import { useState } from 'react'

const people = [
  { id: 1, name: 'Durward Reynolds' },
  { id: 2, name: 'Kenton Towne' },
  { id: 3, name: 'Therese Wunsch' },
  { id: 4, name: 'Benedict Kessler' },
  { id: 5, name: 'Katelyn Rohan' },
]

function Example() {
  const [selectedPerson, setSelectedPerson] = useState(people[0])

  return (

<Field disabled>

      <Label>Assignee:</Label>
      <Description>This person will have full access to this project.</Description>
      <Listbox value={selectedPerson} onChange={setSelectedPerson}>
        <ListboxButton>{selectedPerson.name}</ListboxButton>
        <ListboxOptions anchor="bottom">
          {people.map((person) => (
            <ListboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
              {person.name}
            </ListboxOption>
          ))}
        </ListboxOptions>
      </Listbox>
    </Field>
  )
}
```

You can also disable a listbox outside of a `Field` by adding the disabled prop directly to the `Listbox` itself.

### Disabling a listbox option

Use the `disabled` prop to disable a `ListboxOption` and prevent it from being selected:

```
import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/react'
import { useState } from 'react'

const people = [
  { id: 1, name: 'Durward Reynolds', available: true },
  { id: 2, name: 'Kenton Towne', available: true },
  { id: 3, name: 'Therese Wunsch', available: true },

{ id: 4, name: 'Benedict Kessler', available: false },

{ id: 5, name: 'Katelyn Rohan', available: true },
]

function Example() {
  const [selectedPerson, setSelectedPerson] = useState(people[0])

  return (
    <Listbox value={selectedPerson} onChange={setSelectedPerson}>
      <ListboxButton>{selectedPerson.name}</ListboxButton>
      <ListboxOptions anchor="bottom">
        {people.map((person) => (
          <ListboxOption
            key={person.id}
            value={person}

disabled={!person.available}

className="data-disabled:opacity-50 data-focus:bg-blue-100"

>
            {person.name}
          </ListboxOption>
        ))}
      </ListboxOptions>
    </Listbox>
  )
}
```

### Using with HTML forms

If you add the `name` prop to your `Listbox`, a hidden `input` element will be rendered and kept in sync with the
listbox state.

```
import { Field, Label, Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/react'
import { useState } from 'react'

const people = [
  { id: 1, name: 'Durward Reynolds' },
  { id: 2, name: 'Kenton Towne' },
  { id: 3, name: 'Therese Wunsch' },
  { id: 4, name: 'Benedict Kessler' },
  { id: 5, name: 'Katelyn Rohan' },
]

function Example() {
  const [selectedPerson, setSelectedPerson] = useState(people[0])

  return (

<form action="/projects/1" method="post">

      <Field>
        <Label>Assignee:</Label>

<Listbox name="assignee" value={selectedPerson} onChange={setSelectedPerson}>

          <ListboxButton>{selectedPerson.name}</ListboxButton>
          <ListboxOptions anchor="bottom">
            {people.map((person) => (
              <ListboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
                {person.name}
              </ListboxOption>
            ))}
          </ListboxOptions>
        </Listbox>
      </Field>
      <button>Submit</button>

</form>

)
}
```

This lets you use a listbox inside a native HTML `<form>` and make traditional form submissions as if your listbox was a
native HTML form control.

Basic values like strings will be rendered as a single hidden input containing that value, but complex values like
objects will be encoded into multiple inputs using a square bracket notation for the names:

```
<!-- Rendered hidden inputs -->
<input type="hidden" name="assignee[id]" value="1" />
<input type="hidden" name="assignee[name]" value="Durward Reynolds" />
```

### Using as uncontrolled

If you omit the `value` prop, Headless UI will track its state internally for you, allowing you to use it as an
[uncontrolled component](https://reactjs.org/docs/uncontrolled-components.html).

When uncontrolled, use the `defaultValue` prop to provide an initial value to the `Listbox`.

```
import { Field, Label, Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/react'

const people = [
  { id: 1, name: 'Durward Reynolds' },
  { id: 2, name: 'Kenton Towne' },
  { id: 3, name: 'Therese Wunsch' },
  { id: 4, name: 'Benedict Kessler' },
  { id: 5, name: 'Katelyn Rohan' },
]

function Example() {
  return (
    <form action="/projects/1" method="post">
      <Field>
        <Label>Assignee:</Label>

<Listbox name="assignee" defaultValue={people[0]}>

          <ListboxButton>{({ value }) => value.name}</ListboxButton>
          <ListboxOptions anchor="bottom">
            {people.map((person) => (
              <ListboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
                {person.name}
              </ListboxOption>
            ))}
          </ListboxOptions>
        </Listbox>
      </Field>
      <button>Submit</button>
    </form>
  )
}
```

This can simplify your code when using the listbox [with HTML forms](#using-with-html-forms) or with form APIs that
collect their state using [FormData](https://developer.mozilla.org/en-US/docs/Web/API/FormData) instead of tracking it
using React state.

Any `onChange` prop you provide will still be called when the component's value changes in case you need to run any side
effects, but you won't need to use it to track the component's state yourself.

### Setting the dropdown width

The `ListboxOptions` dropdown has no width set by default, but you can add one using CSS:

```
import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/react'
import { useState } from 'react'

const people = [
  { id: 1, name: 'Durward Reynolds' },
  { id: 2, name: 'Kenton Towne' },
  { id: 3, name: 'Therese Wunsch' },
  { id: 4, name: 'Benedict Kessler' },
  { id: 5, name: 'Katelyn Rohan' },
]

function Example() {
  const [selectedPerson, setSelectedPerson] = useState(people[0])

  return (
    <Listbox value={selectedPerson} onChange={setSelectedPerson}>
      <ListboxButton>{selectedPerson.name}</ListboxButton>

<ListboxOptions anchor="bottom" className="w-52">

        {people.map((person) => (
          <ListboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
            {person.name}
          </ListboxOption>
        ))}
      </ListboxOptions>
    </Listbox>
  )
}
```

If you'd like the dropdown width to match the `ListboxButton` width, use the `--button-width` CSS variable that's
exposed on the `ListboxOptions` element:

```
import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/react'
import { useState } from 'react'

const people = [
  { id: 1, name: 'Durward Reynolds' },
  { id: 2, name: 'Kenton Towne' },
  { id: 3, name: 'Therese Wunsch' },
  { id: 4, name: 'Benedict Kessler' },
  { id: 5, name: 'Katelyn Rohan' },
]

function Example() {
  const [selectedPerson, setSelectedPerson] = useState(people[0])

  return (
    <Listbox value={selectedPerson} onChange={setSelectedPerson}>
      <ListboxButton>{selectedPerson.name}</ListboxButton>

<ListboxOptions anchor="bottom" className="w-(--button-width)">

        {people.map((person) => (
          <ListboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
            {person.name}
          </ListboxOption>
        ))}
      </ListboxOptions>
    </Listbox>
  )
}
```

### Positioning the dropdown

Add the `anchor` prop to the `ListboxOptions` to automatically position the dropdown relative to the `ListboxButton`:

```
import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/react'
import { useState } from 'react'

const people = [
  { id: 1, name: 'Durward Reynolds' },
  { id: 2, name: 'Kenton Towne' },
  { id: 3, name: 'Therese Wunsch' },
  { id: 4, name: 'Benedict Kessler' },
  { id: 5, name: 'Katelyn Rohan' },
]

function Example() {
  const [selectedPerson, setSelectedPerson] = useState(people[0])

  return (
    <Listbox value={selectedPerson} onChange={setSelectedPerson}>
      <ListboxButton>{selectedPerson.name}</ListboxButton>

<ListboxOptions anchor="bottom start">

        {people.map((person) => (
          <ListboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
            {person.name}
          </ListboxOption>
        ))}
      </ListboxOptions>
    </Listbox>
  )
}
```

Use the values `top`, `right`, `bottom`, or `left` to center the dropdown along the appropriate edge, or combine it with
`start` or `end` to align the dropdown to a specific corner, such as `top start` or `bottom end`.

To control the gap between the button and the dropdown, use the `--anchor-gap` CSS variable:

```
import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/react'
import { useState } from 'react'

const people = [
  { id: 1, name: 'Durward Reynolds' },
  { id: 2, name: 'Kenton Towne' },
  { id: 3, name: 'Therese Wunsch' },
  { id: 4, name: 'Benedict Kessler' },
  { id: 5, name: 'Katelyn Rohan' },
]

function Example() {
  const [selectedPerson, setSelectedPerson] = useState(people[0])

  return (
    <Listbox value={selectedPerson} onChange={setSelectedPerson}>
      <ListboxButton>{selectedPerson.name}</ListboxButton>

<ListboxOptions anchor="bottom start" className="[--anchor-gap:4px] sm:[--anchor-gap:8px]">

        {people.map((person) => (
          <ListboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
            {person.name}
          </ListboxOption>
        ))}
      </ListboxOptions>
    </Listbox>
  )
}
```

Additionally, you can use `--anchor-offset` to control the distance that the dropdown should be nudged from its original
position, and `--anchor-padding` to control the minimum space that should exist between the dropdown and the viewport.

The `anchor` prop also supports an object API that allows you to control the `gap`, `offset`, and `padding` values using
JavaScript:

```
import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/react'
import { useState } from 'react'

const people = [
  { id: 1, name: 'Durward Reynolds' },
  { id: 2, name: 'Kenton Towne' },
  { id: 3, name: 'Therese Wunsch' },
  { id: 4, name: 'Benedict Kessler' },
  { id: 5, name: 'Katelyn Rohan' },
]

function Example() {
  const [selectedPerson, setSelectedPerson] = useState(people[0])

  return (
    <Listbox value={selectedPerson} onChange={setSelectedPerson}>
      <ListboxButton>{selectedPerson.name}</ListboxButton>

<ListboxOptions anchor={{ to: 'bottom start', gap: '4px' }}>

        {people.map((person) => (
          <ListboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
            {person.name}
          </ListboxOption>
        ))}
      </ListboxOptions>
    </Listbox>
  )
}
```

See the [ListboxOptions API](#listbox-options) for more information about these options.

### Displaying options horizontally

If you've styled your `ListboxOptions` to appear horizontally, use the `horizontal` prop on the `Listbox` component to
enable navigating the options with the left and right arrow keys instead of up and down, and to update the
`aria-orientation` attribute for assistive technologies.

```
import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/react'
import { useState } from 'react'

const people = [
  { id: 1, name: 'Durward Reynolds' },
  { id: 2, name: 'Kenton Towne' },
  { id: 3, name: 'Therese Wunsch' },
  { id: 4, name: 'Benedict Kessler' },
  { id: 5, name: 'Katelyn Rohan' },
]

function Example() {
  const [selectedPerson, setSelectedPerson] = useState(people[0])

  return (

<Listbox horizontal value={selectedPerson} onChange={setSelectedPerson}>

      <ListboxButton>{selectedPerson.name}</ListboxButton>

<ListboxOptions anchor="bottom" className="flex flex-row">

        {people.map((person) => (
          <ListboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
            {person.name}
          </ListboxOption>
        ))}
      </ListboxOptions>
    </Listbox>
  )
}
```

### Adding transitions

To animate the opening and closing of the listbox dropdown, add the `transition` prop to the `ListboxOptions` component
and then use CSS to style the different stages of the transition:

```
import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/react'
import { useState } from 'react'

const people = [
  { id: 1, name: 'Durward Reynolds' },
  { id: 2, name: 'Kenton Towne' },
  { id: 3, name: 'Therese Wunsch' },
  { id: 4, name: 'Benedict Kessler' },
  { id: 5, name: 'Katelyn Rohan' },
]

function Example() {
  const [selectedPerson, setSelectedPerson] = useState(people[0])

  return (
    <Listbox value={selectedPerson} onChange={setSelectedPerson}>
      <ListboxButton>{selectedPerson.name}</ListboxButton>
      <ListboxOptions
        anchor="bottom"

transition

className="origin-top transition duration-200 ease-out data-closed:scale-95 data-closed:opacity-0"

>
        {people.map((person) => (
          <ListboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
            {person.name}
          </ListboxOption>
        ))}
      </ListboxOptions>
    </Listbox>
  )
}
```

Internally, the `transition` prop is implemented in the exact same way as the `Transition` component. See the
[Transition documentation](/react/transition) to learn more.

### Animating with Framer Motion

Headless UI also composes well with other animation libraries in the React ecosystem like
[Framer Motion](https://www.framer.com/motion/) and [React Spring](https://www.react-spring.io/). You just need to
expose some state to those libraries.

For example, to animate the listbox with Framer Motion, add the `static` prop to the `ListboxOptions` component and then
conditionally render it based on the `open` render prop:

```
import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/react'
import { AnimatePresence, motion } from 'framer-motion'
import { useState } from 'react'

const people = [
  { id: 1, name: 'Durward Reynolds' },
  { id: 2, name: 'Kenton Towne' },
  { id: 3, name: 'Therese Wunsch' },
  { id: 4, name: 'Benedict Kessler' },
  { id: 5, name: 'Katelyn Rohan' },
]

function Example() {
  const [selectedPerson, setSelectedPerson] = useState(people[0])

  return (
    <Listbox value={selectedPerson} onChange={setSelectedPerson}>

{({ open }) => (

<>
          <ListboxButton>{selectedPerson.name}</ListboxButton>
          <AnimatePresence>

{open && (

<ListboxOptions

static

as={motion.div}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                anchor="bottom"
                className="origin-top"
              >
                {people.map((person) => (
                  <ListboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
                    {person.name}
                  </ListboxOption>
                ))}
              </ListboxOptions>

)}

          </AnimatePresence>
        </>

)}

    </Listbox>
  )
}
```

### Binding objects as values

Unlike native HTML form controls, which only allow you to provide strings as values, Headless UI supports binding
complex objects as well.

```
import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/react'
import { useState } from 'react'

const people = [

{ id: 1, name: 'Durward Reynolds' },

{ id: 2, name: 'Kenton Towne' },

{ id: 3, name: 'Therese Wunsch' },

{ id: 4, name: 'Benedict Kessler' },

{ id: 5, name: 'Katelyn Rohan' },

]

function Example() {
  const [selectedPerson, setSelectedPerson] = useState(people[0])

  return (

<Listbox value={selectedPerson} onChange={setSelectedPerson}>

      <ListboxButton>{selectedPerson.name}</ListboxButton>
      <ListboxOptions anchor="bottom">
        {people.map((person) => (
          <ListboxOption key={person.id} value={person} className="data-focus:bg-blue-100">

{person.name}

          </ListboxOption>
        ))}
      </ListboxOptions>
    </Listbox>
  )
}
```

When binding objects as values, it's important to make sure that you use the *same instance* of the object as both the
`value` of the `Listbox` as well as the corresponding `ListboxOption`, otherwise they will fail to be equal and cause
the listbox to behave incorrectly.

To make it easier to work with different instances of the same object, you can use the `by` prop to compare the objects
by a particular field instead of comparing object identity.

When you pass an object to the `value` prop, `by` will default to `id` when present, but you can set it to any field you
like:

```
import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/react'

const departments = [
  { name: 'Marketing', contact: 'Durward Reynolds' },
  { name: 'HR', contact: 'Kenton Towne' },
  { name: 'Sales', contact: 'Therese Wunsch' },
  { name: 'Finance', contact: 'Benedict Kessler' },
  { name: 'Customer service', contact: 'Katelyn Rohan' },
]

function Example({ selectedDepartment, onChange }) {
  return (

<Listbox value={selectedDepartment} by="name" onChange={onChange}>

      <ListboxButton>{selectedDepartment.name}</ListboxButton>
      <ListboxOptions anchor="bottom">
        {departments.map((department) => (
          <ListboxOption key={department.name} value={department} className="data-focus:bg-blue-100">
            {department.name}
          </ListboxOption>
        ))}
      </ListboxOptions>
    </Listbox>
  )
}
```

You can also pass your own comparison function to the `by` prop if you'd like complete control over how objects are
compared:

```
import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/react'

const departments = [
  { id: 1, name: 'Marketing', contact: 'Durward Reynolds' },
  { id: 2, name: 'HR', contact: 'Kenton Towne' },
  { id: 3, name: 'Sales', contact: 'Therese Wunsch' },
  { id: 4, name: 'Finance', contact: 'Benedict Kessler' },
  { id: 5, name: 'Customer service', contact: 'Katelyn Rohan' },
]

function compareDepartments(a, b) {

return a.name.toLowerCase() === b.name.toLowerCase()

}

function Example({ selectedDepartment, onChange }) {
  return (

<Listbox value={selectedDepartment} by={compareDepartments} onChange={onChange}>

      <ListboxButton>{selectedDepartment.name}</ListboxButton>
      <ListboxOptions anchor="bottom">
        {departments.map((department) => (
          <ListboxOption key={department.id} value={department} className="data-focus:bg-blue-100">
            {department.name}
          </ListboxOption>
        ))}
      </ListboxOptions>
    </Listbox>
  )
}
```

### Selecting multiple values

To allow selecting multiple values in your listbox, use the `multiple` prop and pass an array to `value` instead of a
single option.

```
import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/react'
import { useState } from 'react'

const people = [
  { id: 1, name: 'Durward Reynolds' },
  { id: 2, name: 'Kenton Towne' },
  { id: 3, name: 'Therese Wunsch' },
  { id: 4, name: 'Benedict Kessler' },
  { id: 5, name: 'Katelyn Rohan' },
]

function Example() {

const [selectedPeople, setSelectedPeople] = useState([people[0], people[1]])

return (

<Listbox value={selectedPeople} onChange={setSelectedPeople} multiple>

      <ListboxButton>{selectedPeople.map((person) => person.name).join(', ')}</ListboxButton>
      <ListboxOptions anchor="bottom">
        {people.map((person) => (
          <ListboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
            {person.name}
          </ListboxOption>
        ))}
      </ListboxOptions>
    </Listbox>
  )
}
```

This will keep the listbox open when you are selecting options, and choosing an option will toggle it in place.

Your `onChange` handler will be called with an array containing all selected options any time an option is added or
removed.

### Rendering as different elements

By default, the `Listbox` and its subcomponents each render a default element that is sensible for that component.

For example, `ListboxButton` renders a `button`, `ListboxOptions` renders a `div`, and `ListboxOption` renders a `div`.
By contrast, `Listbox` *does not render an element*, and instead renders its children directly.

Use the `as` prop to render the component as a different element or as your own custom component, making sure your
custom components [forward refs](https://react.dev/reference/react/forwardRef) so that Headless UI can wire things up
correctly.

```
import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/react'
import { forwardRef, useState } from 'react'

const people = [
  { id: 1, name: 'Durward Reynolds' },
  { id: 2, name: 'Kenton Towne' },
  { id: 3, name: 'Therese Wunsch' },
  { id: 4, name: 'Benedict Kessler' },
  { id: 5, name: 'Katelyn Rohan' },
]

let MyCustomButton = forwardRef(function (props, ref) {

return <button className="..." ref={ref} {...props} />

})

function Example() {
  const [selectedPerson, setSelectedPerson] = useState(people[0])

  return (

<Listbox value={selectedPerson} onChange={setSelectedPerson}>

<ListboxButton as={MyCustomButton}>{selectedPerson.name}</ListboxButton>

      <ListboxOptions anchor="bottom" as="ul">
        {people.map((person) => (

<ListboxOption as="li" key={person.id} value={person} className="data-focus:bg-blue-100">

            {person.name}
          </ListboxOption>
        ))}
      </ListboxOptions>
    </Listbox>
  )
}
```

To tell an element to render its children directly with no wrapper element, use a `Fragment`.

```
import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/react'
import { Fragment, useState } from 'react'

const people = [
  { id: 1, name: 'Durward Reynolds' },
  { id: 2, name: 'Kenton Towne' },
  { id: 3, name: 'Therese Wunsch' },
  { id: 4, name: 'Benedict Kessler' },
  { id: 5, name: 'Katelyn Rohan' },
]

function Example() {
  const [selectedPerson, setSelectedPerson] = useState(people[0])

  return (
    <Listbox value={selectedPerson} onChange={setSelectedPerson}>

<ListboxButton as={Fragment}>

<button>{selectedPerson.name}</button>

</ListboxButton>

      <ListboxOptions anchor="bottom">
        {people.map((person) => (
          <ListboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
            {person.name}
          </ListboxOption>
        ))}
      </ListboxOptions>
    </Listbox>
  )
}
```

### Building a buttonless API

While the `ListboxButton` component is required when building custom listboxes, it's possible to build them in such a
way that the button is included by default and therefore not required each time you use your listbox. For example, an
API like this:

```
<MyListbox name="status">
  <MyListboxOption value="active">Active</MyListboxOption>
  <MyListboxOption value="paused">Paused</MyListboxOption>
  <MyListboxOption value="delayed">Delayed</MyListboxOption>
  <MyListboxOption value="canceled">Canceled</MyListboxOption>
</MyListbox>
```

To achieve this use the `ListboxSelectedOption` component within your `ListboxButton` to render the currently selected
listbox option.

For this to work you must pass the `children` of your custom listbox (all the `ListboxOption` instances) to both the
`ListboxOptions` as it's children as well as to the `ListboxSelectedOption` via the `options` prop.

Then, to style the `ListboxOption` based on whether it's being rendered in the `ListboxButton` or in the
`ListboxOptions`, use the `selectedOption` render prop to conditionally apply different styles or render different
content.

```
import { Listbox, ListboxButton, ListboxOption, ListboxOptions, ListboxSelectedOption } from '@headlessui/react'
import { Fragment, useState } from 'react'

const people = [
  { id: 1, name: 'Durward Reynolds' },
  { id: 2, name: 'Kenton Towne' },
  { id: 3, name: 'Therese Wunsch' },
  { id: 4, name: 'Benedict Kessler' },
  { id: 5, name: 'Katelyn Rohan' },
]

function Example() {
  const [selectedPerson, setSelectedPerson] = useState(people[0])

  return (
    <MyListbox value={selectedPerson} onChange={setSelectedPerson} placeholder="Select a person&hellip;">
      {people.map((person) => (
        <MyListboxOption key={person.id} value={person}>
          {person.name}
        </MyListboxOption>
      ))}
    </MyListbox>
  )
}

function MyListbox({ placeholder, children, ...props }) {
  return (
    <Listbox {...props}>
      <ListboxButton>

<ListboxSelectedOption options={children} placeholder={<span className="opacity-50">{placeholder}</span>} />

      </ListboxButton>

<ListboxOptions anchor="bottom">{children}</ListboxOptions>

    </Listbox>
  )
}

function MyListboxOption({ children, ...props }) {
  return (
    <ListboxOption as={Fragment} {...props}>

{({ selectedOption }) => {

return selectedOption ? children : <div className="data-focus:bg-blue-100">{children}</div>

}}

    </ListboxOption>
  )
}
```

The `ListboxSelectedOption` component also has a `placeholder` prop that you can use to render a placeholder when no
option is selected.

## Keyboard interaction

|  |  |
| --- | --- |
| Command | Description |
| `Space`, `ArrowDown`,  or `ArrowUp`when `ListboxButton` is focused | Opens listbox and focuses the selected item |
| `Enter`when `ListboxButton` is focused and `Listbox` is closed | Submit the parent form if it exists |
| `Esc`when listbox is open | Closes listbox |
| `ArrowDown` or `ArrowUp`when listbox is open | Focuses previous/next non-disabled item |
| `ArrowLeft` or `ArrowRight`when listbox is open and `horizontal` is set | Focuses previous/next non-disabled item |
| `Home` or `PageUp`when listbox is open | Focuses first non-disabled item |
| `End` or `PageDown`when listbox is open | Focuses last non-disabled item |
| `Enter` or `Space`when listbox is open | Selects the current item |
| `A–Z` or `a–z`when listbox is open | Focuses first item that matches keyboard input |

## Component API

### Listbox

The main listbox component.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `Fragment` | `String | Component`  The element or component the listbox should render as. |
| `invalid` | `false` | `Boolean`  Whether or not the listbox is invalid. |
| `disabled` | `false` | `Boolean`  Use this to disable the entire `Listbox` component & related children. |
| `value` | — | `T`  The selected value. |
| `defaultValue` | — | `T`  The default value when using as an uncontrolled component. |
| `by` | — | `keyof T | ((a: T, z: T) => boolean)`  Use this to compare objects by a particular field, or pass your own comparison function for complete control over how objects are compared.  When you pass an object to the `value` prop, `by` will default to`id` when present. |
| `onChange` | — | `(value: T) => void`  The function to call when a new option is selected. |
| `horizontal` | `false` | `Boolean`  When true, the orientation of the `ListboxOptions` will be `horizontal`, otherwise it will be `vertical`. |
| `multiple` | `false` | `Boolean`  Whether multiple options can be selected or not. |
| `name` | — | `String`  The name used when using the listbox inside a form. |
| `form` | — | `String`  The id of the form that the listbox belongs to.  If `name` is provided but `form` is not, the listbox will add its state to the nearest ancestor `form` element. |

|  |  |  |
| --- | --- | --- |
| Data Attribute | Render Prop | Description |
| — | `value` | `T`  The selected value. |
| `data-open` | `open` | `Boolean`  Whether or not the listbox is open. |
| `data-invalid` | `invalid` | `Boolean`  Whether or not the listbox is invalid. |
| `data-disabled` | `disabled` | `Boolean`  Whether or not the listbox is disabled. |

### ListboxButton

The Listbox's button.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `button` | `String | Component`  The element or component the listbox button should render as. |

|  |  |  |
| --- | --- | --- |
| Data Attribute | Render Prop | Description |
| — | `value` | `T`  The selected value. |
| `data-open` | `open` | `Boolean`  Whether or not the listbox is open. |
| `data-invalid` | `invalid` | `Boolean`  Whether or not the listbox is invalid. |
| `data-disabled` | `disabled` | `Boolean`  Whether or not the listbox button is disabled. |
| `data-focus` | `focus` | `Boolean`  Whether or not the listbox button is focused. |
| `data-hover` | `hover` | `Boolean`  Whether or not the listbox button is hovered. |
| `data-active` | `active` | `Boolean`  Whether or not the listbox button is in an active or pressed state. |
| `data-autofocus` | `autofocus` | `Boolean`  Whether or not the `autoFocus` prop was set to `true`. |

### ListboxSelectedOption

Renders the currently selected option, or a placeholder if no option is selected. Designed to be a child of
`ListboxButton`.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `Fragment` | `String | Component`  The element or component the listbox selected option should render as. |
| `placeholder` | — | `ReactNode`  The React element to render when no option is selected. |
| `options` | — | `ReactNode[]`  Your full array of `ListboxOption` React elements. `ListboxSelectedOption` will filter this list to find and render the currently selected option. |

### ListboxOptions

The component that directly wraps the list of options in your custom Listbox.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `div` | `String | Component`  The element or component the listbox options should render as. |
| `transition` | `false` | `Boolean`  Whether the element should render transition attributes like `data-closed`, `data-enter` and `data-leave`. |
| `anchor` | — | `Object`  Configures the way the dropdown is anchored to the button. |
| `anchor.to` | `bottom` | `String`  Where to position the listbox options relative to the trigger.  Use the values `top`, `right`, `bottom`, `left` to center the listbox options along the appropriate edge, or combine it with `start` or `end` to align the listbox options to a specific corner, such as `top start` or `bottom end`.  Alternatively, use the `selection` option to position the currently selected option directly above the listbox button. |
| `anchor.gap` | `0` | `Number | String`  The space between the listbox button and the listbox options.  Can also be controlled using the `--anchor-gap` CSS variable. |
| `anchor.offset` | `0` | `Number | String`  The distance the listbox options should be nudged from its original position.  Can also be controlled using the `--anchor-offset` CSS variable. |
| `anchor.padding` | `0` | `Number | String`  The minimum space between the listbox options and the viewport.  Can also be controlled using the `--anchor-padding` CSS variable. |
| `static` | `false` | `Boolean`  Whether the element should ignore the internally managed open/closed state. |
| `unmount` | `true` | `Boolean`  Whether the element should be unmounted or hidden based on the open/closed state. |
| `portal` | `false` | `Boolean`  Whether the element should be rendered in a portal.  Automatically set to `true` when `anchor` prop is set. |
| `modal` | `true` | `Boolean`  Whether to enable accessibility features like scroll locking, focus trapping, and making other elements `inert`. |

|  |  |  |
| --- | --- | --- |
| Data Attribute | Render Prop | Description |
| `data-open` | `open` | `Boolean`  Whether or not the listbox is open. |

### ListboxOption

Used to wrap each item within your Listbox.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `div` | `String | Component`  The element or component the listbox option should render as. |
| `value` | — | `T`  The option value. |
| `disabled` | `false` | `Boolean`  Whether or not the listbox option is disabled for keyboard navigation and ARIA purposes. |

|  |  |  |
| --- | --- | --- |
| Data Attribute | Render Prop | Description |
| `data-selected` | `selected` | `Boolean`  Whether or not the listbox option is selected. |
| `data-disabled` | `disabled` | `Boolean`  Whether or not the listbox option is disabled. |
| `data-focus` | `focus` | `Boolean`  Whether or not the listbox option is focused. |
| `data-selectedOption` | `selectedOption` | `Boolean`  Whether or not the listbox option is a child of `ListboxSelectedOption`. |

## Styled examples

If you're interested in predesigned [Tailwind CSS select menu and listbox examples](https://tailwindui.com/components/application-ui/forms/select-menus) using Headless UI, check out **Tailwind Plus** — a collection of beautifully designed and expertly crafted components built by us.

It's a great way to support our work on open-source projects like this and makes it possible for us to improve them and keep them well-maintained.

[Explore more predesigned examples →](https://tailwindcss.com/plus)

[![Various components from Tailwind UI](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Ftailwind-plus.434a3ca6.png&w=3840&q=75)](https://tailwindcss.com/plus)

On this page