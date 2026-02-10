# Combobox

Source: https://headlessui.com/react/combobox

---

React

[Vue](/v1/vue/combobox)

# Combobox

Comboboxes are the foundation of accessible autocompletes and command palettes for your app, complete with robust
support for keyboard navigation.

PreviewCode

## Installation

To get started, install Headless UI via npm:

```
npm install @headlessui/react
```

## Basic example

Comboboxes are built using the `Combobox`, `ComboboxInput`, `ComboboxButton`, `ComboboxOptions`, and `ComboboxOption`
components.

You are completely in charge of how you filter the results, whether it be with a fuzzy search library client-side or by
making server-side requests to an API. In this example we will keep the logic simple for demo purposes.

```
import { Combobox, ComboboxInput, ComboboxOption, ComboboxOptions } from '@headlessui/react'
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
  const [query, setQuery] = useState('')

  const filteredPeople =
    query === ''
      ? people
      : people.filter((person) => {
          return person.name.toLowerCase().includes(query.toLowerCase())
        })

  return (
    <Combobox value={selectedPerson} onChange={setSelectedPerson} onClose={() => setQuery('')}>
      <ComboboxInput
        aria-label="Assignee"
        displayValue={(person) => person?.name}
        onChange={(event) => setQuery(event.target.value)}
      />
      <ComboboxOptions anchor="bottom" className="border empty:invisible">
        {filteredPeople.map((person) => (
          <ComboboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
            {person.name}
          </ComboboxOption>
        ))}
      </ComboboxOptions>
    </Combobox>
  )
}
```

## Styling

Headless UI keeps track of a lot of state about each component, like which combobox option is currently selected,
whether a popover is open or closed, or which item in a menu is currently focused via the keyboard.

But because the components are headless and completely unstyled out of the box, you can't see this information in your
UI until you provide the styles you want for each state yourself.

### Using data attributes

The easiest way to style the different states of a Headless UI component is using the `data-*` attributes that each
component exposes.

For example, the `ComboboxOption` component exposes a `data-focus` attribute, which tells you if the option is currently
focused via the mouse or keyboard, and a `data-selected` attribute, which tells you if that option matches the current
`value` of the `Combobox`.

```
<!-- Rendered `ComboboxOptions` -->
<div data-open>
  <div>Wade Cooper</div>
  <div data-focus data-selected>Arlene Mccoy</div>
  <div>Devon Webb</div>
</div>
```

Use the [CSS attribute selector](https://developer.mozilla.org/en-US/docs/Web/CSS/Attribute_selectors) to conditionally
apply styles based on the presence of these data attributes. If you're using Tailwind CSS, the
[data attribute modifier](https://tailwindcss.com/docs/hover-focus-and-other-states#data-attributes) makes this easy:

```
import { Combobox, ComboboxInput, ComboboxOption, ComboboxOptions } from '@headlessui/react'
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
  const [query, setQuery] = useState('')

  const filteredPeople =
    query === ''
      ? people
      : people.filter((person) => {
          return person.name.toLowerCase().includes(query.toLowerCase())
        })

  return (
    <Combobox value={selectedPerson} onChange={setSelectedPerson} onClose={() => setQuery('')}>
      <ComboboxInput
        aria-label="Assignee"
        displayValue={(person) => person?.name}
        onChange={(event) => setQuery(event.target.value)}
      />
      <ComboboxOptions anchor="bottom" className="border empty:invisible">
        {filteredPeople.map((person) => (

<ComboboxOption key={person.id} value={person} className="group flex gap-2 bg-white data-focus:bg-blue-100">

<CheckIcon className="invisible size-5 group-data-selected:visible" />

            {person.name}
          </ComboboxOption>
        ))}
      </ComboboxOptions>
    </Combobox>
  )
}
```

See the [component API](#component-api) for a list of all the available data attributes.

### Using render props

Each component also exposes information about its current state via
[render props](https://reactjs.org/docs/render-props.html) that you can use to conditionally apply different styles or
render different content.

For example, the `ComboboxOption` component exposes a `focus` state, which tells you if the option is currently focused
via the mouse or keyboard, and a `selected` state, which tells you if that option matches the current `value` of the
`Combobox`.

```
import { Combobox, ComboboxInput, ComboboxOption, ComboboxOptions } from '@headlessui/react'
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
  const [query, setQuery] = useState('')

  const filteredPeople =
    query === ''
      ? people
      : people.filter((person) => {
          return person.name.toLowerCase().includes(query.toLowerCase())
        })

  return (
    <Combobox value={selectedPerson} onChange={setSelectedPerson} onClose={() => setQuery('')}>
      <ComboboxInput
        aria-label="Assignee"
        displayValue={(person) => person?.name}
        onChange={(event) => setQuery(event.target.value)}
      />
      <ComboboxOptions anchor="bottom" className="border empty:invisible">
        {filteredPeople.map((person) => (

<ComboboxOption as={Fragment} key={person.id} value={person} className="data-focus:bg-blue-100">

{({ focus, selected }) => (

<div className={clsx('group flex gap-2', focus && 'bg-blue-100')}>

{selected && <CheckIcon className="size-5" />}

{person.name}

</div>

)}

</ComboboxOption>

))}
      </ComboboxOptions>
    </Combobox>
  )
}
```

See the [component API](#component-api) for a list of all the available render props.

## Examples

### Adding a label

Wrap a `Label` and `Combobox` with the `Field` component to automatically associate them using a generated ID:

```
import { Combobox, ComboboxInput, ComboboxOption, ComboboxOptions, Field, Label } from '@headlessui/react'
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
  const [query, setQuery] = useState('')

  const filteredPeople =
    query === ''
      ? people
      : people.filter((person) => {
          return person.name.toLowerCase().includes(query.toLowerCase())
        })

  return (

<Field>

<Label>Assignee:</Label>

      <Combobox value={selectedPerson} onChange={setSelectedPerson} onClose={() => setQuery('')}>
        <ComboboxInput displayValue={(person) => person?.name} onChange={(event) => setQuery(event.target.value)} />
        <ComboboxOptions anchor="bottom" className="border empty:invisible">
          {filteredPeople.map((person) => (
            <ComboboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
              {person.name}
            </ComboboxOption>
          ))}
        </ComboboxOptions>
      </Combobox>

</Field>

)
}
```

### Adding a description

Use the `Description` component within a `Field` to automatically associate it with a `Combobox` using the
`aria-describedby` attribute:

```
import { Combobox, ComboboxInput, ComboboxOption, ComboboxOptions, Description, Field, Label } from '@headlessui/react'
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
  const [query, setQuery] = useState('')

  const filteredPeople =
    query === ''
      ? people
      : people.filter((person) => {
          return person.name.toLowerCase().includes(query.toLowerCase())
        })

  return (

<Field>

      <Label>Assignee:</Label>

<Description>This person will have full access to this project.</Description>

      <Combobox value={selectedPerson} onChange={setSelectedPerson} onClose={() => setQuery('')}>
        <ComboboxInput displayValue={(person) => person?.name} onChange={(event) => setQuery(event.target.value)} />
        <ComboboxOptions anchor="bottom" className="border empty:invisible">
          {filteredPeople.map((person) => (
            <ComboboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
              {person.name}
            </ComboboxOption>
          ))}
        </ComboboxOptions>
      </Combobox>

</Field>

)
}
```

### Disabling a combobox

Add the `disabled` prop to the `Field` component to disable a `Combobox` and its associated `Label` and `Description`:

```
import { Combobox, ComboboxInput, ComboboxOption, ComboboxOptions, Field, Label } from '@headlessui/react'
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
  const [query, setQuery] = useState('')

  const filteredPeople =
    query === ''
      ? people
      : people.filter((person) => {
          return person.name.toLowerCase().includes(query.toLowerCase())
        })

  return (

<Field disabled>

      <Label>Assignee:</Label>
      <Combobox value={selectedPerson} onChange={setSelectedPerson} onClose={() => setQuery('')}>
        <ComboboxInput displayValue={(person) => person?.name} onChange={(event) => setQuery(event.target.value)} />
        <ComboboxOptions anchor="bottom" className="border empty:invisible">
          {filteredPeople.map((person) => (
            <ComboboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
              {person.name}
            </ComboboxOption>
          ))}
        </ComboboxOptions>
      </Combobox>
    </Field>
  )
}
```

You can also disable a combobox outside of a `Field` by adding the disabled prop directly to the `Combobox` itself.

### Disabling a combobox option

Use the `disabled` prop to disable a `ComboboxOption` and prevent it from being selected:

```
import { Combobox, ComboboxInput, ComboboxOption, ComboboxOptions } from '@headlessui/react'
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
  const [query, setQuery] = useState('')

  const filteredPeople =
    query === ''
      ? people
      : people.filter((person) => {
          return person.name.toLowerCase().includes(query.toLowerCase())
        })

  return (
    <Combobox value={selectedPerson} onChange={setSelectedPerson} onClose={() => setQuery('')}>
      <ComboboxInput
        aria-label="Assignee"
        displayValue={(person) => person?.name}
        onChange={(event) => setQuery(event.target.value)}
      />
      <ComboboxOptions anchor="bottom" className="border empty:invisible">
        {filteredPeople.map((person) => (
          <ComboboxOption
            key={person.id}
            value={person}

disabled={!person.available}

className="data-disabled:opacity-50 data-focus:bg-blue-100"

>
            {person.name}
          </ComboboxOption>
        ))}
      </ComboboxOptions>
    </Combobox>
  )
}
```

### Allowing custom values

You can allow users to enter their own value that doesn't exist in the list by including a dynamic `ComboboxOption`
based on the `query` value.

```
import { Combobox, ComboboxInput, ComboboxOption, ComboboxOptions } from '@headlessui/react'
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
  const [query, setQuery] = useState('')

  const filteredPeople =
    query === ''
      ? people
      : people.filter((person) => {
          return person.name.toLowerCase().includes(query.toLowerCase())
        })

  return (
    <Combobox value={selectedPerson} onChange={setSelectedPerson} onClose={() => setQuery('')}>
      <ComboboxInput
        aria-label="Assignee"
        displayValue={(person) => person?.name}
        onChange={(event) => setQuery(event.target.value)}
      />
      <ComboboxOptions anchor="bottom" className="border empty:invisible">

{query.length > 0 && (

<ComboboxOption value={{ id: null, name: query }} className="data-focus:bg-blue-100">

Create <span className="font-bold">"{query}"</span>

</ComboboxOption>

)}

        {filteredPeople.map((person) => (
          <ComboboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
            {person.name}
          </ComboboxOption>
        ))}
      </ComboboxOptions>
    </Combobox>
  )
}
```

### Using with HTML forms

If you add the `name` prop to your `Combobox`, a hidden `input` element will be rendered and kept in sync with the
combobox state.

```
import { Combobox, ComboboxInput, ComboboxOption, ComboboxOptions } from '@headlessui/react'
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
  const [query, setQuery] = useState('')

  const filteredPeople =
    query === ''
      ? people
      : people.filter((person) => {
          return person.name.toLowerCase().includes(query.toLowerCase())
        })

  return (
    <form action="/projects/1/assignee" method="post">

<Combobox name="assignee" value={selectedPerson} onChange={setSelectedPerson} onClose={() => setQuery('')}>

        <ComboboxInput
          aria-label="Assignee"
          displayValue={(person) => person?.name}
          onChange={(event) => setQuery(event.target.value)}
        />
        <ComboboxOptions anchor="bottom" className="border empty:invisible">
          {filteredPeople.map((person) => (
            <ComboboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
              {person.name}
            </ComboboxOption>
          ))}
        </ComboboxOptions>
      </Combobox>
      <button>Submit</button>
    </form>
  )
}
```

This lets you use a combobox inside a native HTML `<form>` and make traditional form submissions as if your combobox was
a native HTML form control.

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

When uncontrolled, use the `defaultValue` prop to provide an initial value to the `Combobox`.

```
import { Combobox, ComboboxInput, ComboboxOption, ComboboxOptions } from '@headlessui/react'
import { useState } from 'react'

const people = [
  { id: 1, name: 'Durward Reynolds' },
  { id: 2, name: 'Kenton Towne' },
  { id: 3, name: 'Therese Wunsch' },
  { id: 4, name: 'Benedict Kessler' },
  { id: 5, name: 'Katelyn Rohan' },
]

function Example() {
  const [query, setQuery] = useState('')

  const filteredPeople =
    query === ''
      ? people
      : people.filter((person) => {
          return person.name.toLowerCase().includes(query.toLowerCase())
        })

  return (
    <form action="/projects/1/assignee" method="post">

<Combobox name="assignee" defaultValue={people[0]} onClose={() => setQuery('')}>

        <ComboboxInput
          aria-label="Assignee"
          displayValue={(person) => person?.name}
          onChange={(event) => setQuery(event.target.value)}
        />
        <ComboboxOptions anchor="bottom" className="border empty:invisible">
          {filteredPeople.map((person) => (
            <ComboboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
              {person.name}
            </ComboboxOption>
          ))}
        </ComboboxOptions>
      </Combobox>
      <button>Submit</button>
    </form>
  )
}
```

This can simplify your code when using the combobox [with HTML forms](#using-with-html-forms) or with form APIs that
collect their state using [FormData](https://developer.mozilla.org/en-US/docs/Web/API/FormData) instead of tracking it
using React state.

Any `onChange` prop you provide will still be called when the component's value changes in case you need to run any side
effects, but you won't need to use it to track the component's state yourself.

### Positioning the dropdown

Add the `anchor` prop to the `ComboboxOptions` to automatically position the dropdown relative to the `ComboboxInput`:

```
import { Combobox, ComboboxInput, ComboboxOption, ComboboxOptions } from '@headlessui/react'
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
  const [query, setQuery] = useState('')

  const filteredPeople =
    query === ''
      ? people
      : people.filter((person) => {
          return person.name.toLowerCase().includes(query.toLowerCase())
        })

  return (
    <Combobox value={selectedPerson} onChange={setSelectedPerson} onClose={() => setQuery('')}>
      <ComboboxInput
        aria-label="Assignee"
        displayValue={(person) => person?.name}
        onChange={(event) => setQuery(event.target.value)}
      />

<ComboboxOptions anchor="bottom start" className="border empty:invisible">

        {filteredPeople.map((person) => (
          <ComboboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
            {person.name}
          </ComboboxOption>
        ))}
      </ComboboxOptions>
    </Combobox>
  )
}
```

Use the values `top`, `right`, `bottom`, or `left` to center the dropdown along the appropriate edge, or combine it with
`start` or `end` to align the dropdown to a specific corner, such as `top start` or `bottom end`.

To control the gap between the input and the dropdown, use the `--anchor-gap` CSS variable:

```
import { Combobox, ComboboxInput, ComboboxOption, ComboboxOptions } from '@headlessui/react'
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
  const [query, setQuery] = useState('')

  const filteredPeople =
    query === ''
      ? people
      : people.filter((person) => {
          return person.name.toLowerCase().includes(query.toLowerCase())
        })

  return (
    <Combobox value={selectedPerson} onChange={setSelectedPerson} onClose={() => setQuery('')}>
      <ComboboxInput
        aria-label="Assignee"
        displayValue={(person) => person?.name}
        onChange={(event) => setQuery(event.target.value)}
      />

<ComboboxOptions

anchor="bottom start"
        className="border [--anchor-gap:4px] empty:invisible sm:[--anchor-gap:8px]"
      >
        {filteredPeople.map((person) => (
          <ComboboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
            {person.name}
          </ComboboxOption>
        ))}
      </ComboboxOptions>
    </Combobox>
  )
}
```

Additionally, you can use `--anchor-offset` to control the distance that the dropdown should be nudged from its original
position, and `--anchor-padding` to control the minimum space that should exist between the dropdown and the viewport.

The `anchor` prop also supports an object API that allows you to control the `gap`, `offset`, and `padding` values using
JavaScript:

```
import { Combobox, ComboboxInput, ComboboxOption, ComboboxOptions } from '@headlessui/react'
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
  const [query, setQuery] = useState('')

  const filteredPeople =
    query === ''
      ? people
      : people.filter((person) => {
          return person.name.toLowerCase().includes(query.toLowerCase())
        })

  return (
    <Combobox value={selectedPerson} onChange={setSelectedPerson} onClose={() => setQuery('')}>
      <ComboboxInput
        aria-label="Assignee"
        displayValue={(person) => person?.name}
        onChange={(event) => setQuery(event.target.value)}
      />

<ComboboxOptions anchor={{ to: 'bottom start', gap: '4px' }} className="border empty:invisible">

        {filteredPeople.map((person) => (
          <ComboboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
            {person.name}
          </ComboboxOption>
        ))}
      </ComboboxOptions>
    </Combobox>
  )
}
```

See the [ComboboxOptions API](#combobox-options) for more information about these options.

### Setting the dropdown width

The `ComboboxOptions` dropdown has no width set by default, but you can add one using CSS:

```
import { Combobox, ComboboxInput, ComboboxOption, ComboboxOptions } from '@headlessui/react'
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
  const [query, setQuery] = useState('')

  const filteredPeople =
    query === ''
      ? people
      : people.filter((person) => {
          return person.name.toLowerCase().includes(query.toLowerCase())
        })

  return (
    <Combobox value={selectedPerson} onChange={setSelectedPerson} onClose={() => setQuery('')}>
      <ComboboxInput
        aria-label="Assignee"
        displayValue={(person) => person?.name}
        onChange={(event) => setQuery(event.target.value)}
      />

<ComboboxOptions anchor="bottom" className="w-52 border empty:invisible">

        {filteredPeople.map((person) => (
          <ComboboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
            {person.name}
          </ComboboxOption>
        ))}
      </ComboboxOptions>
    </Combobox>
  )
}
```

If you'd like the dropdown width to match the `ComboboxInput` or `ComboboxButton` widths, use the `--input-width` and
`--button-width` CSS variables that are exposed on the `ComboboxOptions` element:

```
import { Combobox, ComboboxInput, ComboboxOption, ComboboxOptions } from '@headlessui/react'
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
  const [query, setQuery] = useState('')

  const filteredPeople =
    query === ''
      ? people
      : people.filter((person) => {
          return person.name.toLowerCase().includes(query.toLowerCase())
        })

  return (
    <Combobox value={selectedPerson} onChange={setSelectedPerson} onClose={() => setQuery('')}>
      <ComboboxInput
        aria-label="Assignee"
        displayValue={(person) => person?.name}
        onChange={(event) => setQuery(event.target.value)}
      />

<ComboboxOptions anchor="bottom" className="w-(--input-width) border empty:invisible">

        {filteredPeople.map((person) => (
          <ComboboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
            {person.name}
          </ComboboxOption>
        ))}
      </ComboboxOptions>
    </Combobox>
  )
}
```

### Adding transitions

To animate the opening and closing of the combobox panel, add the `transition` prop to the `ComboboxOptions` component
and then use CSS to style the different stages of the transition:

```
import { Combobox, ComboboxInput, ComboboxOption, ComboboxOptions } from '@headlessui/react'
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
  const [query, setQuery] = useState('')

  const filteredPeople =
    query === ''
      ? people
      : people.filter((person) => {
          return person.name.toLowerCase().includes(query.toLowerCase())
        })

  return (
    <Combobox value={selectedPerson} onChange={setSelectedPerson} onClose={() => setQuery('')}>
      <ComboboxInput
        aria-label="Assignee"
        displayValue={(person) => person?.name}
        onChange={(event) => setQuery(event.target.value)}
      />
      <ComboboxOptions
        anchor="bottom"

transition

className="origin-top border transition duration-200 ease-out empty:invisible data-closed:scale-95 data-closed:opacity-0"

>
        {filteredPeople.map((person) => (
          <ComboboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
            {person.name}
          </ComboboxOption>
        ))}
      </ComboboxOptions>
    </Combobox>
  )
}
```

Internally, the `transition` prop is implemented in the exact same way as the `Transition` component. See the
[Transition documentation](/react/transition) to learn more.

### Animating with Framer Motion

Headless UI also composes well with other animation libraries in the React ecosystem like
[Framer Motion](https://www.framer.com/motion/) and [React Spring](https://www.react-spring.io/). You just need to
expose some state to those libraries.

For example, to animate the combobox with Framer Motion, add the `static` prop to the `ComboboxOptions` component and
then conditionally render it based on the `open` render prop:

```
import { Combobox, ComboboxInput, ComboboxOption, ComboboxOptions } from '@headlessui/react'
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
  const [query, setQuery] = useState('')

  const filteredPeople =
    query === ''
      ? people
      : people.filter((person) => {
          return person.name.toLowerCase().includes(query.toLowerCase())
        })

  return (
    <Combobox value={selectedPerson} onChange={setSelectedPerson}>

{({ open }) => (

<>
          <ComboboxInput
            aria-label="Assignee"
            displayValue={(person) => person?.name}
            onChange={(event) => setQuery(event.target.value)}
          />
          <AnimatePresence>

{open && (

<ComboboxOptions

static

as={motion.div}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                anchor="bottom"
                className="origin-top border empty:invisible"
                onAnimationComplete={() => setQuery('')}
              >
                {filteredPeople.map((person) => (
                  <ComboboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
                    {person.name}
                  </ComboboxOption>
                ))}
              </ComboboxOptions>

)}

          </AnimatePresence>
        </>

)}

    </Combobox>
  )
}
```

### Binding objects as values

Unlike native HTML form controls, which only allow you to provide strings as values, Headless UI supports binding
complex objects as well.

When binding objects, make sure to set the `displayValue` on your `ComboboxInput` so that a string representation of the
selected option can be rendered in the input:

```
import { Combobox, ComboboxInput, ComboboxOption, ComboboxOptions } from '@headlessui/react'
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
  const [query, setQuery] = useState('')

  const filteredPeople =
    query === ''
      ? people
      : people.filter((person) => {
          return person.name.toLowerCase().includes(query.toLowerCase())
        })

  return (

<Combobox value={selectedPerson} onChange={setSelectedPerson} onClose={() => setQuery('')}>

      <ComboboxInput
        aria-label="Assignee"

displayValue={(person) => person?.name}

onChange={(event) => setQuery(event.target.value)}
      />
      <ComboboxOptions anchor="bottom" className="border empty:invisible">
        {filteredPeople.map((person) => (
          <ComboboxOption key={person.id} value={person} className="data-focus:bg-blue-100">

{person.name}

          </ComboboxOption>
        ))}
      </ComboboxOptions>
    </Combobox>
  )
}
```

When binding objects as values, it's important to make sure that you use the *same instance* of the object as both the
`value` of the `Combobox` as well as the corresponding `ComboboxOption`, otherwise they will fail to be equal and cause
the combobox to behave incorrectly.

To make it easier to work with different instances of the same object, you can use the `by` prop to compare the objects
by a particular field instead of comparing object identity.

When you pass an object to the `value` prop, `by` will default to `id` when present, but you can set it to any field you
like:

```
import { Combobox, ComboboxInput, ComboboxOption, ComboboxOptions } from '@headlessui/react'
import { useState } from 'react'

const departments = [
  { name: 'Marketing', contact: 'Durward Reynolds' },
  { name: 'HR', contact: 'Kenton Towne' },
  { name: 'Sales', contact: 'Therese Wunsch' },
  { name: 'Finance', contact: 'Benedict Kessler' },
  { name: 'Customer service', contact: 'Katelyn Rohan' },
]

function DepartmentPicker({ selectedDepartment, onChange }) {

const [query, setQuery] = useState('')

  const filteredDepartments =
    query === ''
      ? departments
      : departments.filter((department) => {
          return department.name.toLowerCase().includes(query.toLowerCase())
        })

  return (

<Combobox value={selectedDepartment} by="name" onChange={onChange} onClose={() => setQuery('')}>

      <ComboboxInput
        aria-label="Department"
        displayValue={(department) => department?.name}
        onChange={(event) => setQuery(event.target.value)}
      />
      <ComboboxOptions anchor="bottom" className="border empty:invisible">
        {filteredDepartments.map((department) => (
          <ComboboxOption key={department.id} value={department} className="data-focus:bg-blue-100">
            {department.name}
          </ComboboxOption>
        ))}
      </ComboboxOptions>
    </Combobox>
  )
}
```

You can also pass your own comparison function to the `by` prop if you'd like complete control over how objects are
compared:

```
import { Combobox, ComboboxInput, ComboboxOption, ComboboxOptions } from '@headlessui/react'
import { useState } from 'react'

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

function DepartmentPicker({ selectedDepartment, onChange }) {
  const [query, setQuery] = useState('')

  const filteredDepartments =
    query === ''
      ? departments
      : departments.filter((department) => {
          return department.name.toLowerCase().includes(query.toLowerCase())
        })

  return (

<Combobox value={selectedDepartment} by={compareDepartments} onChange={onChange} onClose={() => setQuery('')}>

      <ComboboxInput
        aria-label="Department"
        displayValue={(department) => department?.name}
        onChange={(event) => setQuery(event.target.value)}
      />
      <ComboboxOptions anchor="bottom" className="border empty:invisible">
        {filteredDepartments.map((department) => (
          <ComboboxOption key={department.id} value={department} className="data-focus:bg-blue-100">
            {department.name}
          </ComboboxOption>
        ))}
      </ComboboxOptions>
    </Combobox>
  )
}
```

### Binding strings as values

While it's very common to [bind objects as values](#binding-objects-as-values), you can also provide simple string
values.

When doing this you can omit the `displayValue` prop from the `ComboboxInput`.

```
import { Combobox, ComboboxInput, ComboboxOption, ComboboxOptions } from '@headlessui/react'
import { useState } from 'react'

const people = ['Durward Reynolds', 'Kenton Towne', 'Therese Wunsch', 'Benedict Kessler', 'Katelyn Rohan']

function Example() {
  const [selectedPerson, setSelectedPerson] = useState(people[0])
  const [query, setQuery] = useState('')

  const filteredPeople =
    query === ''
      ? people
      : people.filter((person) => {
          return person.toLowerCase().includes(query.toLowerCase())
        })

  return (
    <Combobox value={selectedPerson} onChange={setSelectedPerson} onClose={() => setQuery('')}>
      <ComboboxInput aria-label="Assignee" onChange={(event) => setQuery(event.target.value)} />
      <ComboboxOptions anchor="bottom" className="border empty:invisible">
        {filteredPeople.map((person) => (

<ComboboxOption key={person} value={person} className="data-focus:bg-blue-100">

{person}

</ComboboxOption>

))}
      </ComboboxOptions>
    </Combobox>
  )
}
```

### Selecting multiple values

To allow selecting multiple values in your combobox, use the `multiple` prop and pass an array to `value` instead of a
single option.

```
import { Combobox, ComboboxInput, ComboboxOption, ComboboxOptions } from '@headlessui/react'
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

const [query, setQuery] = useState('')

  const filteredPeople =
    query === ''
      ? people
      : people.filter((person) => {
          return person.name.toLowerCase().includes(query.toLowerCase())
        })

  return (

<Combobox multiple value={selectedPeople} onChange={setSelectedPeople} onClose={() => setQuery('')}>

      {selectedPeople.length > 0 && (
        <ul>
          {selectedPeople.map((person) => (
            <li key={person.id}>{person.name}</li>
          ))}
        </ul>
      )}
      <ComboboxInput aria-label="Assignees" onChange={(event) => setQuery(event.target.value)} />
      <ComboboxOptions anchor="bottom" className="border empty:invisible">
        {filteredPeople.map((person) => (
          <ComboboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
            {person.name}
          </ComboboxOption>
        ))}
      </ComboboxOptions>
    </Combobox>
  )
}
```

Your `onChange` handler will be called with an array containing all selected options any time an option is added or
removed.

### Opening the dropdown on focus

Use the `immediate` prop to immediately open the combobox options when the combobox input is focused.

```
import { Combobox, ComboboxInput, ComboboxOption, ComboboxOptions } from '@headlessui/react'
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
  const [query, setQuery] = useState('')

  const filteredPeople =
    query === ''
      ? people
      : people.filter((person) => {
          return person.name.toLowerCase().includes(query.toLowerCase())
        })

  return (

<Combobox immediate value={selectedPerson} onChange={setSelectedPerson} onClose={() => setQuery('')}>

      <ComboboxInput
        aria-label="Assignee"
        displayValue={(person) => person?.name}
        onChange={(event) => setQuery(event.target.value)}
      />
      <ComboboxOptions anchor="bottom" className="border empty:invisible">
        {filteredPeople.map((person) => (
          <ComboboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
            {person.name}
          </ComboboxOption>
        ))}
      </ComboboxOptions>
    </Combobox>
  )
}
```

### Rendering as different elements

By default, the `Combobox` and its subcomponents each render a default element that is sensible for that component.

For example, `ComboboxInput` renders an `input`, `ComboboxButton` renders a `button`, `ComboboxOptions` renders a `div`,
and `ComboboxOption` renders a `div`. By contrast, `Combobox` *does not render an element*, and instead renders its
children directly.

Use the `as` prop to render the component as a different element or as your own custom component, making sure your
custom components [forward refs](https://react.dev/reference/react/forwardRef) so that Headless UI can wire things up
correctly.

```
import { Combobox, ComboboxButton, ComboboxInput, ComboboxOption, ComboboxOptions } from '@headlessui/react'
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
  const [query, setQuery] = useState('')

  const filteredPeople =
    query === ''
      ? people
      : people.filter((person) => {
          return person.name.toLowerCase().includes(query.toLowerCase())
        })

  return (

<Combobox value={selectedPerson} onChange={setSelectedPerson} onClose={() => setQuery('')}>

      <ComboboxInput
        aria-label="Assignee"
        displayValue={(person) => person?.name}
        onChange={(event) => setQuery(event.target.value)}
      />
      <ComboboxButton as={MyCustomButton}>Open</ComboboxButton>

<ComboboxOptions as="ul" anchor="bottom" className="border empty:invisible">

        {filteredPeople.map((person) => (

<ComboboxOption as="li" key={person.id} value={person} className="data-focus:bg-blue-100">

            {person.name}
          </ComboboxOption>
        ))}
      </ComboboxOptions>
    </Combobox>
  )
}
```

To tell an element to render its children directly with no wrapper element, use a `Fragment`.

```
import { Combobox, ComboboxInput, ComboboxOption, ComboboxOptions } from '@headlessui/react'
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
  const [query, setQuery] = useState('')

  const filteredPeople =
    query === ''
      ? people
      : people.filter((person) => {
          return person.name.toLowerCase().includes(query.toLowerCase())
        })

  return (
    <Combobox value={selectedPerson} onChange={setSelectedPerson} onClose={() => setQuery('')}>
      <ComboboxInput

as={Fragment}

aria-label="Assignee"
        displayValue={(person) => person?.name}
        onChange={(event) => setQuery(event.target.value)}
      >
        <input />
      </ComboboxInput>
      <ComboboxOptions anchor="bottom" className="border empty:invisible">
        {filteredPeople.map((person) => (
          <ComboboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
            {person.name}
          </ComboboxOption>
        ))}
      </ComboboxOptions>
    </Combobox>
  )
}
```

### Rendering active option details

Depending on what you're building it can sometimes make sense to render additional information about the active option
outside of the `ComboboxOptions`. For example, a preview of the active option within the context of a command palette.
In these situations you can read the `activeOption` render prop argument to access this information.

```
import { Combobox, ComboboxInput, ComboboxOption, ComboboxOptions } from '@headlessui/react'
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
  const [query, setQuery] = useState('')

  const filteredPeople =
    query === ''
      ? people
      : people.filter((person) => {
          return person.name.toLowerCase().includes(query.toLowerCase())
        })

  return (
    <Combobox value={selectedPerson} onChange={setSelectedPerson} onClose={() => setQuery('')}>

{({ activeOption }) => (

<>
          <ComboboxInput
            aria-label="Assignee"
            displayValue={(person) => person?.name}
            onChange={(event) => setQuery(event.target.value)}
          />
          <ComboboxOptions anchor="bottom" className="border empty:invisible">
            {filteredPeople.map((person) => (
              <ComboboxOption key={person.id} value={person} className="data-focus:bg-blue-100">
                {person.name}
              </ComboboxOption>
            ))}
          </ComboboxOptions>

{activeOption && <div>The currently focused user is: {activeOption.name}</div>}

        </>
      )}
    </Combobox>
  )
}
```

The `activeOption` will be the `value` of the currently focused `ComboboxOption`.

### Virtual scrolling

By default the `Combobox` renders all its options into the DOM. While this is a good default, this can cause performance
issues when given a really large number of options. For these situations we provide a virtual scrolling API.

To enable virtual scrolling, provide a list of options to the `Combobox` via the `virtual.options` prop, as well as a
render prop to the `ComboboxOptions`, which acts as a template for each option:

```
import { Combobox, ComboboxInput, ComboboxOption, ComboboxOptions } from '@headlessui/react'
import { useState } from 'react'

const people = [
  { id: 1, name: 'Durward Reynolds' },
  { id: 2, name: 'Kenton Towne' },
  { id: 3, name: 'Therese Wunsch' },
  { id: 4, name: 'Benedict Kessler' },
  { id: 5, name: 'Katelyn Rohan' },
  // +1000 more people
]

function Example() {
  const [selectedPerson, setSelectedPerson] = useState(people[0])
  const [query, setQuery] = useState('')

  const filteredPeople =
    query === ''
      ? people
      : people.filter((person) => {
          return person.name.toLowerCase().includes(query.toLowerCase())
        })

  return (
    <Combobox
      value={selectedPerson}

virtual={{ options: filteredPeople }}

onChange={setSelectedPerson}
      onClose={() => setQuery('')}
    >
      <ComboboxInput
        aria-label="Assignee"
        displayValue={(person) => person?.name}
        onChange={(event) => setQuery(event.target.value)}
      />
      <ComboboxOptions anchor="bottom" className="w-(--input-width) border empty:invisible">

{({ option: person }) => (

<ComboboxOption value={person} className="data-focus:bg-blue-100">

{person.name}

</ComboboxOption>

)}

      </ComboboxOptions>
    </Combobox>
  )
}
```

To specify whether a given option is disabled, provide a callback to the `virtual.disabled` prop:

```
import { Combobox, ComboboxInput, ComboboxOption, ComboboxOptions } from '@headlessui/react'
import { useState } from 'react'

const people = [
  { id: 1, name: 'Durward Reynolds', available: true },
  { id: 2, name: 'Kenton Towne', available: true },
  { id: 3, name: 'Therese Wunsch', available: true },

{ id: 4, name: 'Benedict Kessler', available: false },

{ id: 5, name: 'Katelyn Rohan', available: true },
  // +1000 more people
]

function Example() {
  const [selectedPerson, setSelectedPerson] = useState(people[0])
  const [query, setQuery] = useState('')

  const filteredPeople =
    query === ''
      ? people
      : people.filter((person) => {
          return person.name.toLowerCase().includes(query.toLowerCase())
        })

  return (
    <Combobox
      value={selectedPerson}
      virtual={{
        options: filteredPeople,

disabled: (person) => !person.available,

}}
      onChange={setSelectedPerson}
      onClose={() => setQuery('')}
    >
      <ComboboxInput
        aria-label="Assignee"
        displayValue={(person) => person?.name}
        onChange={(event) => setQuery(event.target.value)}
      />
      <ComboboxOptions anchor="bottom" className="w-(--input-width) border empty:invisible">
        {({ option: person }) => (

<ComboboxOption value={person} className="data-disabled:opacity-50 data-focus:bg-blue-100">

            {person.name}
          </ComboboxOption>
        )}
      </ComboboxOptions>
    </Combobox>
  )
}
```

## Keyboard interaction

|  |  |
| --- | --- |
| Command | Description |
| `ArrowDown`,  or `ArrowUp`when `ComboboxInput` is focused | Opens combobox and focuses the selected item |
| `Enter`, `Space`, `ArrowDown`,  or `ArrowUp`when `ComboboxButton` is focused | Opens combobox, focuses the input and selects the selected item |
| `Esc`when combobox is open | Closes combobox and restores the selected item in the input field |
| `ArrowDown` or `ArrowUp`when combobox is open | Focuses previous/next non-disabled item |
| `Home` or `PageUp`when combobox is open | Focuses first non-disabled item |
| `End` or `PageDown`when combobox is open | Focuses last non-disabled item |
| `Enter`when combobox is open | Selects the current item |
| `Enter`when combobox is closed and in a form | Submits the form |
| `Tab`when combobox is open | Selects the currently focused item and closes the combobox |
| `A–Z` or `a–z`when combobox is open | Calls the `onChange` which allows you to filter the list |

## Component API

### Combobox

The main combobox component.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `Fragment` | `String | Component`  The element or component the combobox should render as. |
| `invalid` | `false` | `Boolean`  Whether or not the combobox is invalid. |
| `disabled` | `false` | `Boolean`  Use this to disable the entire combobox component & related children. |
| `value` | — | `T`  The selected value. |
| `defaultValue` | — | `T`  The default value when using as an uncontrolled component. |
| `by` | — | `keyof T | ((a: T, z: T) => boolean)`  Use this to compare objects by a particular field, or pass your own comparison function for complete control over how objects are compared.  When you pass an object to the `value` prop, `by` will default to`id` when present. |
| `onChange` | — | `(value: T | null) => void`  The function to call when a new option is selected. |
| `onClose` | — | `() => void`  The function to call when the dropdown closes. |
| `multiple` | `false` | `Boolean`  Whether multiple options can be selected or not. |
| `name` | — | `String`  The name used when using the combobox inside a form. |
| `form` | — | `String`  The id of the form that the combobox belongs to.  If `name` is provided but `form` is not, the combobox will add its state to the nearest ancestor `form` element. |
| `immediate` | `false` | `Boolean`  Whether or not the combobox should immediately open its options when the combobox input is focused. |
| `virtual` | `null` | `Object`  Configures virtual scrolling. |
| `virtual.options` | — | `Array`  A collection of options to display when in virtual scrolling mode. |
| `virtual.disabled` | `null` | `(value: T) => boolean`  A callback to determine whether a given option is disabled when in virtual scrolling mode. |

|  |  |  |
| --- | --- | --- |
| Data Attribute | Render Prop | Description |
| — | `value` | `T`  The selected value. |
| `data-open` | `open` | `Boolean`  Whether or not the combobox is open. |
| — | `activeOption` | `T | null`  The focused option, or `null` if none is focused. |
| `data-invalid` | `invalid` | `Boolean`  Whether or not the combobox is invalid. |
| `data-disabled` | `disabled` | `Boolean`  Whether or not the combobox is disabled. |
| — | `activeIndex` | `Number | null`  The index of the focused option, or `null` if none is focused. |

### ComboboxInput

The Combobox's input.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `input` | `String | Component`  The element or component the combobox input should render as. |
| `displayValue` | — | `(item: T) => string`  The string representation of your `value`. |
| `onChange` | — | `(event: Event) => void`  The function to call when the input value changes. |
| `autoFocus` | `false` | `Boolean`  Whether or not the combobox input should receive focus when first rendered. |

|  |  |  |
| --- | --- | --- |
| Data Attribute | Render Prop | Description |
| `data-open` | `open` | `Boolean`  Whether or not the combobox is open. |
| `data-disabled` | `disabled` | `Boolean`  Whether or not the combobox is disabled. |
| `data-invalid` | `invalid` | `Boolean`  Whether or not the combobox input is invalid. |
| `data-focus` | `focus` | `Boolean`  Whether or not the combobox input is focused. |
| `data-hover` | `hover` | `Boolean`  Whether or not the combobox input is hovered. |
| `data-autofocus` | `autofocus` | `Boolean`  Whether or not the `autoFocus` prop was set to `true`. |

### ComboboxButton

The Combobox's button.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `button` | `String | Component`  The element or component the combobox button should render as. |
| `autoFocus` | `false` | `Boolean`  Whether or not the combobox button should receive focus when first rendered. |

|  |  |  |
| --- | --- | --- |
| Data Attribute | Render Prop | Description |
| — | `value` | `T`  The selected value. |
| `data-open` | `open` | `Boolean`  Whether or not the combobox is open. |
| `data-invalid` | `invalid` | `Boolean`  Whether or not the combobox button is invalid. |
| `data-disabled` | `disabled` | `Boolean`  Whether or not the combobox button is disabled. |
| `data-focus` | `focus` | `Boolean`  Whether or not the combobox button is focused. |
| `data-hover` | `hover` | `Boolean`  Whether or not the combobox button is hovered. |
| `data-active` | `active` | `Boolean`  Whether or not the combobox button is in an active or pressed state. |

### ComboboxOptions

The component that directly wraps the list of options in your custom Combobox.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `div` | `String | Component`  The element or component the combobox options should render as. |
| `transition` | `false` | `Boolean`  Whether the element should render transition attributes like `data-closed`, `data-enter` and `data-leave`. |
| `anchor` | — | `Object`  Configures the way the dropdown is anchored to the input. |
| `anchor.to` | `bottom` | `String`  Where to position the combobox options relative to the trigger.  Use the values `top`, `right`, `bottom`, `left` to center the combobox options along the appropriate edge, or combine it with `start` or `end` to align the combobox options to a specific corner, such as `top start` or `bottom end`. |
| `anchor.gap` | `0` | `Number | String`  The space between the combobox input and the combobox options.  Can also be controlled using the `--anchor-gap` CSS variable. |
| `anchor.offset` | `0` | `Number | String`  The distance the combobox options should be nudged from its original position.  Can also be controlled using the `--anchor-offset` CSS variable. |
| `anchor.padding` | `0` | `Number | String`  The minimum space between the combobox options and the viewport.  Can also be controlled using the `--anchor-padding` CSS variable. |
| `static` | `false` | `Boolean`  Whether the element should ignore the internally managed open/closed state. |
| `unmount` | `true` | `Boolean`  Whether the element should be unmounted or hidden based on the open/closed state. |
| `portal` | `false` | `Boolean`  Whether the element should be rendered in a portal.  Automatically set to `true` when `anchor` prop is set. |
| `modal` | `true` | `Boolean`  Whether to enable accessibility features like scroll locking, focus trapping, and making other elements `inert`. |

|  |  |  |
| --- | --- | --- |
| Data Attribute | Render Prop | Description |
| `data-open` | `open` | `Boolean`  Whether or not the combobox is open. |

### ComboboxOption

Used to wrap each item within your Combobox.

|  |  |  |
| --- | --- | --- |
| Prop | Default | Description |
| `as` | `div` | `String | Component`  The element or component the combobox option should render as. |
| `value` | — | `T`  The option value. |
| `disabled` | `false` | `Boolean`  Whether or not the combobox option is disabled for keyboard navigation and ARIA purposes. |
| `order` | — | `Number`  The order of the option in the list of options, used for performance improvements.  Not relevant when using virtual scrolling. |

|  |  |  |
| --- | --- | --- |
| Data Attribute | Render Prop | Description |
| `data-selected` | `selected` | `Boolean`  Whether or not the combobox option is selected. |
| `data-disabled` | `disabled` | `Boolean`  Whether or not the combobox option is disabled. |
| `data-focus` | `focus` | `Boolean`  Whether or not the combobox option is focused. |

## Styled examples

If you're interested in predesigned [Tailwind CSS combobox component examples](https://tailwindui.com/components/application-ui/forms/comboboxes) using Headless UI, check out **Tailwind Plus** — a collection of beautifully designed and expertly crafted components built by us.

It's a great way to support our work on open-source projects like this and makes it possible for us to improve them and keep them well-maintained.

[Explore more predesigned examples →](https://tailwindcss.com/plus)

[![Various components from Tailwind UI](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Ftailwind-plus.434a3ca6.png&w=3840&q=75)](https://tailwindcss.com/plus)

On this page