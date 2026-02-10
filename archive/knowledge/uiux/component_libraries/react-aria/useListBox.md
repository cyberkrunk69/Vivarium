# useListBox

Source: https://react-spectrum.adobe.com/react-aria/useListBox.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../ListBox).

# useListBox

Provides the behavior and accessibility implementation for a listbox component.
A listbox displays a list of options and allows a user to select one or more of them.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useListBox, useOption, useListBoxSection} from 'react-aria'` |

[View ARIA pattern

W3C](https://www.w3.org/WAI/ARIA/apg/patterns/listbox/ "View ARIA pattern")[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/listbox "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/listbox "View package")

## API[#](#api)

---

`useListBox<T>(
props: AriaListBoxOptions<T>,
state: ListState<T>,
ref: RefObject<HTMLElement
|Â  |Â null>
): ListBoxAria`
`useOption<T>(
props: AriaOptionProps,
state: ListState<T>,
ref: RefObject<FocusableElement
|Â  |Â null>
): OptionAria`
`useListBoxSection(
(props: AriaListBoxSectionProps
)): ListBoxSectionAria`

## Features[#](#features)

---

A listbox can be built using the [<select>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select)
and [<option>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/option) HTML elements, but this is
not possible to style consistently cross browser. `useListBox` helps achieve accessible
listbox components that can be styled as needed.

Note: `useListBox` only handles the list itself. For a dropdown similar to a `<select>`, see [useSelect](../Select/useSelect.html).

- Exposed to assistive technology as a `listbox` using ARIA
- Support for single, multiple, or no selection
- Support for disabled items
- Support for sections
- Labeling support for accessibility
- Support for mouse, touch, and keyboard interactions
- Tab stop focus management
- Keyboard navigation support including arrow keys, home/end, page up/down, select all, and clear
- Automatic scrolling support during keyboard navigation
- Typeahead to allow focusing options by typing text
- Support for use with virtualized lists

## Anatomy[#](#anatomy)

---

A listbox consists of a container element, with a list of options or groups inside.
`useListBox`, `useOption`, and `useListBoxSection` handle exposing this to assistive
technology using ARIA, along with handling keyboard, mouse, and interactions to support
selection and focus behavior.

`useListBox` returns props that you should spread onto the list container element,
along with props for an optional visual label:

| Name | Type | Description |
| --- | --- | --- |
| `listBoxProps` | `DOMAttributes` | Props for the listbox element. |
| `labelProps` | `DOMAttributes` | Props for the listbox's visual label element (if any). |

`useOption` returns props for an individual option and its children, along with states you can use for styling:

| Name | Type | Description |
| --- | --- | --- |
| `optionProps` | `DOMAttributes` | Props for the option element. |
| `labelProps` | `DOMAttributes` | Props for the main text element inside the option. |
| `descriptionProps` | `DOMAttributes` | Props for the description text element inside the option, if any. |
| `isFocused` | `boolean` | Whether the option is currently focused. |
| `isFocusVisible` | `boolean` | Whether the option is keyboard focused. |
| `isPressed` | `boolean` | Whether the item is currently in a pressed state. |
| `isSelected` | `boolean` | Whether the item is currently selected. |
| `isDisabled` | `boolean` | Whether the item is non-interactive, i.e. both selection and actions are disabled and the item may not be focused. Dependent on `disabledKeys` and `disabledBehavior`. |
| `allowsSelection` | `boolean` | Whether the item may be selected, dependent on `selectionMode`, `disabledKeys`, and `disabledBehavior`. |
| `hasAction` | `boolean` | Whether the item has an action, dependent on `onAction`, `disabledKeys`, and `disabledBehavior`. It may also change depending on the current selection state of the list (e.g. when selection is primary). This can be used to enable or disable hover styles or other visual indications of interactivity. |

`useListBoxSection` returns props for a section:

| Name | Type | Description |
| --- | --- | --- |
| `itemProps` | `DOMAttributes` | Props for the wrapper list item. |
| `headingProps` | `DOMAttributes` | Props for the heading element, if any. |
| `groupProps` | `DOMAttributes` | Props for the group element. |

State is managed by the `useListState`
hook from `@react-stately/list`. The state object should be passed as an option to
each of the above hooks.

If a listbox, options, or group does not have a visible label, an `aria-label` or `aria-labelledby`
prop must be passed instead to identify the element to assistive technology.

## State management[#](#state-management)

---

`useListBox` requires knowledge of the options in the listbox in order to handle keyboard
navigation and other interactions. It does this using
the `Collection`
interface, which is a generic interface to access sequential unique keyed data. You can
implement this interface yourself, e.g. by using a prop to pass a list of item objects,
but `useListState` from
`@react-stately/list` implements a JSX based interface for building collections instead.
See [Collection Components](https://react-spectrum.adobe.com/v3/collections.html) for more information.

In addition, `useListState`
manages the state necessary for multiple selection and exposes
a `SelectionManager`,
which makes use of the collection to provide an interface to update the selection state.
For more information, see [Selection](https://react-spectrum.adobe.com/v3/selection.html).

## Example[#](#example)

---

This example uses HTML `<ul>` and `<li>` elements to represent the list, and applies
props from `useListBox`
and `useOption`.
For each item in the collection in state, either an `Option` or `ListBoxSection` (defined [below](#sections))
is rendered according to the item's `type` property.

```
import type {AriaListBoxProps} from 'react-aria';
import {Item, useListState} from 'react-stately';
import {mergeProps, useFocusRing, useListBox, useOption} from 'react-aria';

function ListBox<T extends object>(props: AriaListBoxProps<T>) {
  // Create state based on the incoming props
  let state = useListState(props);

  // Get props for the listbox element
  let ref = React.useRef(null);
  let { listBoxProps, labelProps } = useListBox(props, state, ref);

  return (
    <>
      <div {...labelProps}>{props.label}</div>
      <ul {...listBoxProps} ref={ref}>
        {[...state.collection].map((item) => (
          item.type === 'section'
            ? <ListBoxSection key={item.key} section={item} state={state} />
            : <Option key={item.key} item={item} state={state} />
        ))}
      </ul>
    </>
  );
}

function Option({ item, state }) {
  // Get props for the option element
  let ref = React.useRef(null);
  let { optionProps } = useOption({ key: item.key }, state, ref);

  // Determine whether we should show a keyboard
  // focus ring for accessibility
  let { isFocusVisible, focusProps } = useFocusRing();

  return (
    <li
      {...mergeProps(optionProps, focusProps)}
      ref={ref}
      data-focus-visible={isFocusVisible}
    >
      {item.rendered}
    </li>
  );
}

<ListBox label="Alignment" selectionMode="single">
  <Item>Left</Item>
  <Item>Middle</Item>
  <Item>Right</Item>
</ListBox>
```

```
import type {AriaListBoxProps} from 'react-aria';
import {Item, useListState} from 'react-stately';
import {
  mergeProps,
  useFocusRing,
  useListBox,
  useOption
} from 'react-aria';

function ListBox<T extends object>(
  props: AriaListBoxProps<T>
) {
  // Create state based on the incoming props
  let state = useListState(props);

  // Get props for the listbox element
  let ref = React.useRef(null);
  let { listBoxProps, labelProps } = useListBox(
    props,
    state,
    ref
  );

  return (
    <>
      <div {...labelProps}>{props.label}</div>
      <ul {...listBoxProps} ref={ref}>
        {[...state.collection].map((item) => (
          item.type === 'section'
            ? (
              <ListBoxSection
                key={item.key}
                section={item}
                state={state}
              />
            )
            : (
              <Option
                key={item.key}
                item={item}
                state={state}
              />
            )
        ))}
      </ul>
    </>
  );
}

function Option({ item, state }) {
  // Get props for the option element
  let ref = React.useRef(null);
  let { optionProps } = useOption(
    { key: item.key },
    state,
    ref
  );

  // Determine whether we should show a keyboard
  // focus ring for accessibility
  let { isFocusVisible, focusProps } = useFocusRing();

  return (
    <li
      {...mergeProps(optionProps, focusProps)}
      ref={ref}
      data-focus-visible={isFocusVisible}
    >
      {item.rendered}
    </li>
  );
}

<ListBox label="Alignment" selectionMode="single">
  <Item>Left</Item>
  <Item>Middle</Item>
  <Item>Right</Item>
</ListBox>
```

```
import type {AriaListBoxProps} from 'react-aria';
import {
  Item,
  useListState
} from 'react-stately';
import {
  mergeProps,
  useFocusRing,
  useListBox,
  useOption
} from 'react-aria';

function ListBox<
  T extends object
>(
  props:
    AriaListBoxProps<T>
) {
  // Create state based on the incoming props
  let state =
    useListState(props);

  // Get props for the listbox element
  let ref = React.useRef(
    null
  );
  let {
    listBoxProps,
    labelProps
  } = useListBox(
    props,
    state,
    ref
  );

  return (
    <>
      <div
        {...labelProps}
      >
        {props.label}
      </div>
      <ul
        {...listBoxProps}
        ref={ref}
      >
        {[
          ...state
            .collection
        ].map((item) => (
          item.type ===
              'section'
            ? (
              <ListBoxSection
                key={item
                  .key}
                section={item}
                state={state}
              />
            )
            : (
              <Option
                key={item
                  .key}
                item={item}
                state={state}
              />
            )
        ))}
      </ul>
    </>
  );
}

function Option(
  { item, state }
) {
  // Get props for the option element
  let ref = React.useRef(
    null
  );
  let { optionProps } =
    useOption(
      { key: item.key },
      state,
      ref
    );

  // Determine whether we should show a keyboard
  // focus ring for accessibility
  let {
    isFocusVisible,
    focusProps
  } = useFocusRing();

  return (
    <li
      {...mergeProps(
        optionProps,
        focusProps
      )}
      ref={ref}
      data-focus-visible={isFocusVisible}
    >
      {item.rendered}
    </li>
  );
}

<ListBox
  label="Alignment"
  selectionMode="single"
>
  <Item>Left</Item>
  <Item>Middle</Item>
  <Item>Right</Item>
</ListBox>
```

 Show CSS

```
[role=listbox] {
  padding: 0;
  margin: 5px 0;
  list-style: none;
  border: 1px solid gray;
  max-width: 250px;
  max-height: 300px;
  overflow: auto;
}

[role=option] {
  display: block;
  padding: 2px 5px;
  outline: none;
  cursor: default;
  color: inherit;

  &[data-focus-visible=true] {
    outline: 2px solid orange;
  }

  &[aria-selected=true] {
    background: blueviolet;
    color: white;
  }

  &[aria-disabled] {
    color: #aaa;
  }
}
```

```
[role=listbox] {
  padding: 0;
  margin: 5px 0;
  list-style: none;
  border: 1px solid gray;
  max-width: 250px;
  max-height: 300px;
  overflow: auto;
}

[role=option] {
  display: block;
  padding: 2px 5px;
  outline: none;
  cursor: default;
  color: inherit;

  &[data-focus-visible=true] {
    outline: 2px solid orange;
  }

  &[aria-selected=true] {
    background: blueviolet;
    color: white;
  }

  &[aria-disabled] {
    color: #aaa;
  }
}
```

```
[role=listbox] {
  padding: 0;
  margin: 5px 0;
  list-style: none;
  border: 1px solid gray;
  max-width: 250px;
  max-height: 300px;
  overflow: auto;
}

[role=option] {
  display: block;
  padding: 2px 5px;
  outline: none;
  cursor: default;
  color: inherit;

  &[data-focus-visible=true] {
    outline: 2px solid orange;
  }

  &[aria-selected=true] {
    background: blueviolet;
    color: white;
  }

  &[aria-disabled] {
    color: #aaa;
  }
}
```

## Dynamic collections[#](#dynamic-collections)

---

`ListBox` follows the [Collection Components API](https://react-spectrum.adobe.com/v3/collections.html), accepting both static and dynamic collections.
The example above shows static collections, which can be used when the full list of options is known ahead of time. Dynamic collections,
as shown below, can be used when the options come from an external data source such as an API call, or update over time.

As seen below, an iterable list of options is passed to the ListBox using the `items` prop. Each item accepts a `key` prop, which
is passed to the `onSelectionChange` handler to identify the selected item. Alternatively, if the item objects contain an `id` property,
as shown in the example below, then this is used automatically and a `key` prop is not required.

```
function Example() {
  let options = [
    { id: 1, name: 'Aardvark' },
    { id: 2, name: 'Cat' },
    { id: 3, name: 'Dog' },
    { id: 4, name: 'Kangaroo' },
    { id: 5, name: 'Koala' },
    { id: 6, name: 'Penguin' },
    { id: 7, name: 'Snake' },
    { id: 8, name: 'Turtle' },
    { id: 9, name: 'Wombat' }
  ];

  return (
    <ListBox label="Animals" items={options} selectionMode="single">
      {(item) => <Item>{item.name}</Item>}
    </ListBox>
  );
}
```

```
function Example() {
  let options = [
    { id: 1, name: 'Aardvark' },
    { id: 2, name: 'Cat' },
    { id: 3, name: 'Dog' },
    { id: 4, name: 'Kangaroo' },
    { id: 5, name: 'Koala' },
    { id: 6, name: 'Penguin' },
    { id: 7, name: 'Snake' },
    { id: 8, name: 'Turtle' },
    { id: 9, name: 'Wombat' }
  ];

  return (
    <ListBox
      label="Animals"
      items={options}
      selectionMode="single"
    >
      {(item) => <Item>{item.name}</Item>}
    </ListBox>
  );
}
```

```
function Example() {
  let options = [
    {
      id: 1,
      name: 'Aardvark'
    },
    {
      id: 2,
      name: 'Cat'
    },
    {
      id: 3,
      name: 'Dog'
    },
    {
      id: 4,
      name: 'Kangaroo'
    },
    {
      id: 5,
      name: 'Koala'
    },
    {
      id: 6,
      name: 'Penguin'
    },
    {
      id: 7,
      name: 'Snake'
    },
    {
      id: 8,
      name: 'Turtle'
    },
    {
      id: 9,
      name: 'Wombat'
    }
  ];

  return (
    <ListBox
      label="Animals"
      items={options}
      selectionMode="single"
    >
      {(item) => (
        <Item>
          {item.name}
        </Item>
      )}
    </ListBox>
  );
}
```

## Selection[#](#selection)

---

ListBox supports multiple selection modes. By default, selection is disabled, however this can be changed using the `selectionMode` prop.
Use `defaultSelectedKeys` to provide a default set of selected items (uncontrolled) and `selectedKeys` to set the selected items (controlled). The value of the selected keys must match the `key` prop of the items.
See the `react-stately` [Selection docs](https://react-spectrum.adobe.com/v3/selection.html) for more details.

```
import type {Selection} from 'react-stately';

function Example() {
  let [selected, setSelected] = React.useState<Selection>(new Set(['cheese']));

  return (
    <>
      <ListBox
        label="Choose sandwich contents"
        selectionMode="multiple"
        selectedKeys={selected}
        onSelectionChange={setSelected}
      >
        <Item key="lettuce">Lettuce</Item>
        <Item key="tomato">Tomato</Item>
        <Item key="cheese">Cheese</Item>
        <Item key="tuna">Tuna Salad</Item>
        <Item key="egg">Egg Salad</Item>
        <Item key="ham">Ham</Item>
      </ListBox>
      <p>
        Current selection (controlled):{' '}
        {selected === 'all' ? 'all' : [...selected].join(', ')}
      </p>
    </>
  );
}
```

```
import type {Selection} from 'react-stately';

function Example() {
  let [selected, setSelected] = React.useState<Selection>(
    new Set(['cheese'])
  );

  return (
    <>
      <ListBox
        label="Choose sandwich contents"
        selectionMode="multiple"
        selectedKeys={selected}
        onSelectionChange={setSelected}
      >
        <Item key="lettuce">Lettuce</Item>
        <Item key="tomato">Tomato</Item>
        <Item key="cheese">Cheese</Item>
        <Item key="tuna">Tuna Salad</Item>
        <Item key="egg">Egg Salad</Item>
        <Item key="ham">Ham</Item>
      </ListBox>
      <p>
        Current selection (controlled): {selected === 'all'
          ? 'all'
          : [...selected].join(', ')}
      </p>
    </>
  );
}
```

```
import type {Selection} from 'react-stately';

function Example() {
  let [
    selected,
    setSelected
  ] = React.useState<
    Selection
  >(new Set(['cheese']));

  return (
    <>
      <ListBox
        label="Choose sandwich contents"
        selectionMode="multiple"
        selectedKeys={selected}
        onSelectionChange={setSelected}
      >
        <Item key="lettuce">
          Lettuce
        </Item>
        <Item key="tomato">
          Tomato
        </Item>
        <Item key="cheese">
          Cheese
        </Item>
        <Item key="tuna">
          Tuna Salad
        </Item>
        <Item key="egg">
          Egg Salad
        </Item>
        <Item key="ham">
          Ham
        </Item>
      </ListBox>
      <p>
        Current selection
        (controlled):
        {' '}
        {selected ===
            'all'
          ? 'all'
          : [...selected]
            .join(', ')}
      </p>
    </>
  );
}
```

### Selection behavior[#](#selection-behavior)

By default, `useListBox` uses the `"toggle"` selection behavior, which behaves like a checkbox group: clicking, tapping, or pressing the `Space` or `Enter` keys toggles selection for the focused row. Using the arrow keys moves focus but does not change selection.

When `selectionBehavior` is set to `"replace"`, clicking a row with the mouse replaces the selection with only that row. Using the arrow keys moves both focus and selection. To select multiple rows, modifier keys such as `Ctrl`, `Cmd`, and `Shift` can be used. On touch screen devices, selection always behaves as toggle since modifier keys may not be available.

These selection behaviors are defined in [Aria Practices](https://www.w3.org/WAI/ARIA/apg/patterns/listbox/#keyboardinteraction).

```
<ListBox
  label="Choose sandwich contents"
  selectionMode="multiple"
  selectionBehavior="replace"
>
  <Item key="lettuce">Lettuce</Item>
  <Item key="tomato">Tomato</Item>
  <Item key="cheese">Cheese</Item>
  <Item key="tuna">Tuna Salad</Item>
  <Item key="egg">Egg Salad</Item>
  <Item key="ham">Ham</Item>
</ListBox>
```

```
<ListBox
  label="Choose sandwich contents"
  selectionMode="multiple"
  selectionBehavior="replace"
>
  <Item key="lettuce">Lettuce</Item>
  <Item key="tomato">Tomato</Item>
  <Item key="cheese">Cheese</Item>
  <Item key="tuna">Tuna Salad</Item>
  <Item key="egg">Egg Salad</Item>
  <Item key="ham">Ham</Item>
</ListBox>
```

```
<ListBox
  label="Choose sandwich contents"
  selectionMode="multiple"
  selectionBehavior="replace"
>
  <Item key="lettuce">
    Lettuce
  </Item>
  <Item key="tomato">
    Tomato
  </Item>
  <Item key="cheese">
    Cheese
  </Item>
  <Item key="tuna">
    Tuna Salad
  </Item>
  <Item key="egg">
    Egg Salad
  </Item>
  <Item key="ham">
    Ham
  </Item>
</ListBox>
```

## Sections[#](#sections)

---

ListBox supports sections with separators and headings in order to group options. Sections can be used by wrapping groups of Items in a `Section` component. Each `Section` takes a `title` and `key` prop.
To implement sections, implement the `ListBoxSection` component referenced above
using the `useListBoxSection` hook. It will include four extra elements:
an `<li>` between the sections to represent the separator, an `<li>` to contain the heading `<span>` element, and a
`<ul>` to contain the child items. This structure is necessary to ensure HTML semantics
are correct.

```
import {useListBoxSection} from 'react-aria';

function ListBoxSection({ section, state }) {
  let { itemProps, headingProps, groupProps } = useListBoxSection({
    heading: section.rendered,
    'aria-label': section['aria-label']
  });

  // If the section is not the first, add a separator element to provide visual separation.
  // The heading is rendered inside an <li> element, which contains
  // a <ul> with the child items.
  return (
    <>
      {section.key !== state.collection.getFirstKey() &&
        (
          <li
            role="presentation"
            style={{
              borderTop: '1px solid gray',
              margin: '2px 5px'
            }}
          />
        )}
      <li {...itemProps}>
        {section.rendered &&
          (
            <span
              {...headingProps}
              style={{
                fontWeight: 'bold',
                fontSize: '1.1em',
                padding: '2px 5px'
              }}
            >
              {section.rendered}
            </span>
          )}
        <ul
          {...groupProps}
          style={{
            padding: 0,
            listStyle: 'none'
          }}
        >
          {[...section.childNodes].map((node) => (
            <Option
              key={node.key}
              item={node}
              state={state}
            />
          ))}
        </ul>
      </li>
    </>
  );
}
```

```
import {useListBoxSection} from 'react-aria';

function ListBoxSection({ section, state }) {
  let { itemProps, headingProps, groupProps } =
    useListBoxSection({
      heading: section.rendered,
      'aria-label': section['aria-label']
    });

  // If the section is not the first, add a separator element to provide visual separation.
  // The heading is rendered inside an <li> element, which contains
  // a <ul> with the child items.
  return (
    <>
      {section.key !== state.collection.getFirstKey() &&
        (
          <li
            role="presentation"
            style={{
              borderTop: '1px solid gray',
              margin: '2px 5px'
            }}
          />
        )}
      <li {...itemProps}>
        {section.rendered &&
          (
            <span
              {...headingProps}
              style={{
                fontWeight: 'bold',
                fontSize: '1.1em',
                padding: '2px 5px'
              }}
            >
              {section.rendered}
            </span>
          )}
        <ul
          {...groupProps}
          style={{
            padding: 0,
            listStyle: 'none'
          }}
        >
          {[...section.childNodes].map((node) => (
            <Option
              key={node.key}
              item={node}
              state={state}
            />
          ))}
        </ul>
      </li>
    </>
  );
}
```

```
import {useListBoxSection} from 'react-aria';

function ListBoxSection(
  { section, state }
) {
  let {
    itemProps,
    headingProps,
    groupProps
  } = useListBoxSection({
    heading:
      section.rendered,
    'aria-label':
      section[
        'aria-label'
      ]
  });

  // If the section is not the first, add a separator element to provide visual separation.
  // The heading is rendered inside an <li> element, which contains
  // a <ul> with the child items.
  return (
    <>
      {section.key !==
          state
            .collection
            .getFirstKey() &&
        (
          <li
            role="presentation"
            style={{
              borderTop:
                '1px solid gray',
              margin:
                '2px 5px'
            }}
          />
        )}
      <li {...itemProps}>
        {section
          .rendered &&
          (
            <span
              {...headingProps}
              style={{
                fontWeight:
                  'bold',
                fontSize:
                  '1.1em',
                padding:
                  '2px 5px'
              }}
            >
              {section
                .rendered}
            </span>
          )}
        <ul
          {...groupProps}
          style={{
            padding: 0,
            listStyle:
              'none'
          }}
        >
          {[
            ...section
              .childNodes
          ].map(
            (node) => (
              <Option
                key={node
                  .key}
                item={node}
                state={state}
              />
            )
          )}
        </ul>
      </li>
    </>
  );
}
```

### Static items[#](#static-items)

With this in place, we can now render a static ListBox with multiple sections:

```
import {Section} from 'react-stately';

<ListBox label="Choose sandwich contents" selectionMode="multiple">
  <Section title="Veggies">
    <Item key="lettuce">Lettuce</Item>
    <Item key="tomato">Tomato</Item>
    <Item key="onion">Onion</Item>
  </Section>
  <Section title="Protein">
    <Item key="ham">Ham</Item>
    <Item key="tuna">Tuna</Item>
    <Item key="tofu">Tofu</Item>
  </Section>
  <Section title="Condiments">
    <Item key="mayo">Mayonaise</Item>
    <Item key="mustard">Mustard</Item>
    <Item key="ranch">Ranch</Item>
  </Section>
</ListBox>
```

```
import {Section} from 'react-stately';

<ListBox
  label="Choose sandwich contents"
  selectionMode="multiple"
>
  <Section title="Veggies">
    <Item key="lettuce">Lettuce</Item>
    <Item key="tomato">Tomato</Item>
    <Item key="onion">Onion</Item>
  </Section>
  <Section title="Protein">
    <Item key="ham">Ham</Item>
    <Item key="tuna">Tuna</Item>
    <Item key="tofu">Tofu</Item>
  </Section>
  <Section title="Condiments">
    <Item key="mayo">Mayonaise</Item>
    <Item key="mustard">Mustard</Item>
    <Item key="ranch">Ranch</Item>
  </Section>
</ListBox>
```

```
import {Section} from 'react-stately';

<ListBox
  label="Choose sandwich contents"
  selectionMode="multiple"
>
  <Section title="Veggies">
    <Item key="lettuce">
      Lettuce
    </Item>
    <Item key="tomato">
      Tomato
    </Item>
    <Item key="onion">
      Onion
    </Item>
  </Section>
  <Section title="Protein">
    <Item key="ham">
      Ham
    </Item>
    <Item key="tuna">
      Tuna
    </Item>
    <Item key="tofu">
      Tofu
    </Item>
  </Section>
  <Section title="Condiments">
    <Item key="mayo">
      Mayonaise
    </Item>
    <Item key="mustard">
      Mustard
    </Item>
    <Item key="ranch">
      Ranch
    </Item>
  </Section>
</ListBox>
```

### Dynamic items[#](#dynamic-items)

The above example shows sections with static items. Sections can also be populated from a hierarchical data structure.
Similarly to the props on ListBox, `<Section>` takes an array of data using the `items` prop.

```
import type {Selection} from 'react-stately';

function Example() {
  let options = [
    {name: 'Australian', children: [
      {id: 2, name: 'Koala'},
      {id: 3, name: 'Kangaroo'},
      {id: 4, name: 'Platypus'}
    ]},
    {name: 'American', children: [
      {id: 6, name: 'Bald Eagle'},
      {id: 7, name: 'Bison'},
      {id: 8, name: 'Skunk'}
    ]}
  ];
  let [selected, setSelected] = React.useState<Selection>(new Set());

  return (
    <ListBox
      label="Pick an animal"
      items={options}
      selectedKeys={selected}
      selectionMode="single"
      onSelectionChange={setSelected}>
      {item => (
        <Section key={item.name} items={item.children} title={item.name}>
          {item => <Item>{item.name}</Item>}
        </Section>
      )}
    </ListBox>
  );
}
```

```
import type {Selection} from 'react-stately';

function Example() {
  let options = [
    {
      name: 'Australian',
      children: [
        { id: 2, name: 'Koala' },
        { id: 3, name: 'Kangaroo' },
        { id: 4, name: 'Platypus' }
      ]
    },
    {
      name: 'American',
      children: [
        { id: 6, name: 'Bald Eagle' },
        { id: 7, name: 'Bison' },
        { id: 8, name: 'Skunk' }
      ]
    }
  ];
  let [selected, setSelected] = React.useState<Selection>(
    new Set()
  );

  return (
    <ListBox
      label="Pick an animal"
      items={options}
      selectedKeys={selected}
      selectionMode="single"
      onSelectionChange={setSelected}
    >
      {(item) => (
        <Section
          key={item.name}
          items={item.children}
          title={item.name}
        >
          {(item) => <Item>{item.name}</Item>}
        </Section>
      )}
    </ListBox>
  );
}
```

```
import type {Selection} from 'react-stately';

function Example() {
  let options = [
    {
      name: 'Australian',
      children: [
        {
          id: 2,
          name: 'Koala'
        },
        {
          id: 3,
          name:
            'Kangaroo'
        },
        {
          id: 4,
          name:
            'Platypus'
        }
      ]
    },
    {
      name: 'American',
      children: [
        {
          id: 6,
          name:
            'Bald Eagle'
        },
        {
          id: 7,
          name: 'Bison'
        },
        {
          id: 8,
          name: 'Skunk'
        }
      ]
    }
  ];
  let [
    selected,
    setSelected
  ] = React.useState<
    Selection
  >(new Set());

  return (
    <ListBox
      label="Pick an animal"
      items={options}
      selectedKeys={selected}
      selectionMode="single"
      onSelectionChange={setSelected}
    >
      {(item) => (
        <Section
          key={item.name}
          items={item
            .children}
          title={item
            .name}
        >
          {(item) => (
            <Item>
              {item.name}
            </Item>
          )}
        </Section>
      )}
    </ListBox>
  );
}
```

### Accessibility[#](#accessibility)

Sections without a `title` must provide an `aria-label` for accessibility.

## Complex options[#](#complex-options)

---

By default, options that only contain text will be labeled by the contents of the option.
For options that have more complex content (e.g. icons, multiple lines of text, etc.), use
`labelProps` and `descriptionProps` from `useOption`
as needed to apply to the main text element of the option and its description. This improves screen
reader announcement.

**NOTE: listbox options cannot contain interactive content (e.g. buttons, checkboxes, etc.).
For these cases, see [useGridList](../GridList/useGridList.html) instead.**

To implement this, we'll update the `Option` component to apply the ARIA properties
returned by `useOption` to the appropriate
elements. In this example, we'll pull them out of `props.children` and use `React.cloneElement`
to apply the props, but you may want to use a more robust approach (e.g. context).

```
function Option({ item, state }) {
  let ref = React.useRef(null);
  let { optionProps, labelProps, descriptionProps } = useOption(
    { key: item.key },
    state,
    ref
  );
  let { isFocusVisible, focusProps } = useFocusRing();

  // Pull out the two expected children. We will clone them
  // and add the necessary props for accessibility.
  let [title, description] = item.rendered;

  return (
    <li
      {...mergeProps(optionProps, focusProps)}
      ref={ref}
      data-focus-visible={isFocusVisible}
    >
      {React.cloneElement(title, labelProps)}
      {React.cloneElement(description, descriptionProps)}
    </li>
  );
}

<ListBox label="Text alignment" selectionMode="single">
  <Item textValue="Align Left">
    <div>
      <strong>Align Left</strong>
    </div>
    <div>Align the selected text to the left</div>
  </Item>
  <Item textValue="Align Center">
    <div>
      <strong>Align Center</strong>
    </div>
    <div>Align the selected text center</div>
  </Item>
  <Item textValue="Align Right">
    <div>
      <strong>Align Right</strong>
    </div>
    <div>Align the selected text to the right</div>
  </Item>
</ListBox>
```

```
function Option({ item, state }) {
  let ref = React.useRef(null);
  let { optionProps, labelProps, descriptionProps } =
    useOption({ key: item.key }, state, ref);
  let { isFocusVisible, focusProps } = useFocusRing();

  // Pull out the two expected children. We will clone them
  // and add the necessary props for accessibility.
  let [title, description] = item.rendered;

  return (
    <li
      {...mergeProps(optionProps, focusProps)}
      ref={ref}
      data-focus-visible={isFocusVisible}
    >
      {React.cloneElement(title, labelProps)}
      {React.cloneElement(description, descriptionProps)}
    </li>
  );
}

<ListBox label="Text alignment" selectionMode="single">
  <Item textValue="Align Left">
    <div>
      <strong>Align Left</strong>
    </div>
    <div>Align the selected text to the left</div>
  </Item>
  <Item textValue="Align Center">
    <div>
      <strong>Align Center</strong>
    </div>
    <div>Align the selected text center</div>
  </Item>
  <Item textValue="Align Right">
    <div>
      <strong>Align Right</strong>
    </div>
    <div>Align the selected text to the right</div>
  </Item>
</ListBox>
```

```
function Option(
  { item, state }
) {
  let ref = React.useRef(
    null
  );
  let {
    optionProps,
    labelProps,
    descriptionProps
  } = useOption(
    { key: item.key },
    state,
    ref
  );
  let {
    isFocusVisible,
    focusProps
  } = useFocusRing();

  // Pull out the two expected children. We will clone them
  // and add the necessary props for accessibility.
  let [
    title,
    description
  ] = item.rendered;

  return (
    <li
      {...mergeProps(
        optionProps,
        focusProps
      )}
      ref={ref}
      data-focus-visible={isFocusVisible}
    >
      {React
        .cloneElement(
          title,
          labelProps
        )}
      {React
        .cloneElement(
          description,
          descriptionProps
        )}
    </li>
  );
}

<ListBox
  label="Text alignment"
  selectionMode="single"
>
  <Item textValue="Align Left">
    <div>
      <strong>
        Align Left
      </strong>
    </div>
    <div>
      Align the
      selected text to
      the left
    </div>
  </Item>
  <Item textValue="Align Center">
    <div>
      <strong>
        Align Center
      </strong>
    </div>
    <div>
      Align the
      selected text
      center
    </div>
  </Item>
  <Item textValue="Align Right">
    <div>
      <strong>
        Align Right
      </strong>
    </div>
    <div>
      Align the
      selected text to
      the right
    </div>
  </Item>
</ListBox>
```

## Asynchronous loading[#](#asynchronous-loading)

---

This example uses the [useAsyncList](../useAsyncList.html) hook to handle asynchronous loading
of data from a server. You may additionally want to display a spinner to indicate the loading
state to the user, or support features like infinite scroll to load more data.

```
import {useAsyncList} from 'react-stately';

interface Pokemon {
  name: string;
}

function AsyncLoadingExample() {
  let list = useAsyncList<Pokemon>({
    async load({ signal }) {
      let res = await fetch(
        `https://pokeapi.co/api/v2/pokemon`,
        { signal }
      );
      let json = await res.json();

      return {
        items: json.results
      };
    }
  });

  return (
    <ListBox label="Pick a Pokemon" items={list.items} selectionMode="single">
      {(item) => <Item key={item.name}>{item.name}</Item>}
    </ListBox>
  );
}
```

```
import {useAsyncList} from 'react-stately';

interface Pokemon {
  name: string;
}

function AsyncLoadingExample() {
  let list = useAsyncList<Pokemon>({
    async load({ signal }) {
      let res = await fetch(
        `https://pokeapi.co/api/v2/pokemon`,
        { signal }
      );
      let json = await res.json();

      return {
        items: json.results
      };
    }
  });

  return (
    <ListBox
      label="Pick a Pokemon"
      items={list.items}
      selectionMode="single"
    >
      {(item) => <Item key={item.name}>{item.name}</Item>}
    </ListBox>
  );
}
```

```
import {useAsyncList} from 'react-stately';

interface Pokemon {
  name: string;
}

function AsyncLoadingExample() {
  let list =
    useAsyncList<
      Pokemon
    >({
      async load(
        { signal }
      ) {
        let res =
          await fetch(
            `https://pokeapi.co/api/v2/pokemon`,
            { signal }
          );
        let json =
          await res
            .json();

        return {
          items:
            json.results
        };
      }
    });

  return (
    <ListBox
      label="Pick a Pokemon"
      items={list.items}
      selectionMode="single"
    >
      {(item) => (
        <Item
          key={item.name}
        >
          {item.name}
        </Item>
      )}
    </ListBox>
  );
}
```

## Links[#](#links)

---

By default, interacting with an item in a ListBox triggers `onSelectionChange`. Alternatively, items may be links to another page or website. This can be achieved by passing the `href` prop to the `<Item>` component.

This example shows how to update the `Option` component with support for rendering an `<a>` element if an `href` prop is passed to the item. Note that you'll also need to render the `ListBox` as a `<div>` instead of a `<ul>`, since an `<a>` inside a `<ul>` is not valid HTML.

```
function Option({item, state}) {
  let ref = React.useRef(null);
  let {optionProps} = useOption({key: item.key}, state, ref);
  let {isFocusVisible, focusProps} = useFocusRing();
  let ElementType: React.ElementType = item.props.href ? 'a' : 'div';
  return (
    <ElementType
      {...mergeProps(optionProps, focusProps)}
      ref={ref}
      data-focus-visible={isFocusVisible}>
      {item.rendered}
    </ElementType>
  );
}

<ListBox aria-label="Links">
  <Item href="https://adobe.com/" target="_blank">Adobe</Item>
  <Item href="https://apple.com/" target="_blank">Apple</Item>
  <Item href="https://google.com/" target="_blank">Google</Item>
  <Item href="https://microsoft.com/" target="_blank">Microsoft</Item>
</ListBox>
```

```
function Option({ item, state }) {
  let ref = React.useRef(null);
  let { optionProps } = useOption(
    { key: item.key },
    state,
    ref
  );
  let { isFocusVisible, focusProps } = useFocusRing();
  let ElementType: React.ElementType = item.props.href
    ? 'a'
    : 'div';
  return (
    <ElementType
      {...mergeProps(optionProps, focusProps)}
      ref={ref}
      data-focus-visible={isFocusVisible}
    >
      {item.rendered}
    </ElementType>
  );
}

<ListBox aria-label="Links">
  <Item href="https://adobe.com/" target="_blank">
    Adobe
  </Item>
  <Item href="https://apple.com/" target="_blank">
    Apple
  </Item>
  <Item href="https://google.com/" target="_blank">
    Google
  </Item>
  <Item href="https://microsoft.com/" target="_blank">
    Microsoft
  </Item>
</ListBox>
```

```
function Option(
  { item, state }
) {
  let ref = React.useRef(
    null
  );
  let { optionProps } =
    useOption(
      { key: item.key },
      state,
      ref
    );
  let {
    isFocusVisible,
    focusProps
  } = useFocusRing();
  let ElementType:
    React.ElementType =
      item.props.href
        ? 'a'
        : 'div';
  return (
    <ElementType
      {...mergeProps(
        optionProps,
        focusProps
      )}
      ref={ref}
      data-focus-visible={isFocusVisible}
    >
      {item.rendered}
    </ElementType>
  );
}

<ListBox aria-label="Links">
  <Item
    href="https://adobe.com/"
    target="_blank"
  >
    Adobe
  </Item>
  <Item
    href="https://apple.com/"
    target="_blank"
  >
    Apple
  </Item>
  <Item
    href="https://google.com/"
    target="_blank"
  >
    Google
  </Item>
  <Item
    href="https://microsoft.com/"
    target="_blank"
  >
    Microsoft
  </Item>
</ListBox>
```

By default, link items in a ListBox are not selectable, and only perform navigation when the user interacts with them. However, with the "replace" [selection behavior](#selection-behavior), items will be selected when single clicking or pressing the `Space` key, and navigate to the link when double clicking or pressing the `Enter` key.

```
<ListBox
  aria-label="Links"
  selectionMode="multiple"
  selectionBehavior="replace"
>
  <Item href="https://adobe.com/" target="_blank">Adobe</Item>
  <Item href="https://apple.com/" target="_blank">Apple</Item>
  <Item href="https://google.com/" target="_blank">Google</Item>
  <Item href="https://microsoft.com/" target="_blank">Microsoft</Item>
</ListBox>
```

```
<ListBox
  aria-label="Links"
  selectionMode="multiple"
  selectionBehavior="replace"
>
  <Item href="https://adobe.com/" target="_blank">
    Adobe
  </Item>
  <Item href="https://apple.com/" target="_blank">
    Apple
  </Item>
  <Item href="https://google.com/" target="_blank">
    Google
  </Item>
  <Item href="https://microsoft.com/" target="_blank">
    Microsoft
  </Item>
</ListBox>
```

```
<ListBox
  aria-label="Links"
  selectionMode="multiple"
  selectionBehavior="replace"
>
  <Item
    href="https://adobe.com/"
    target="_blank"
  >
    Adobe
  </Item>
  <Item
    href="https://apple.com/"
    target="_blank"
  >
    Apple
  </Item>
  <Item
    href="https://google.com/"
    target="_blank"
  >
    Google
  </Item>
  <Item
    href="https://microsoft.com/"
    target="_blank"
  >
    Microsoft
  </Item>
</ListBox>
```

### Client side routing[#](#client-side-routing)

The `<Item>` component works with frameworks and client side routers like [Next.js](https://nextjs.org/) and [React Router](https://reactrouter.com/en/main). As with other React Aria components that support links, this works via the `RouterProvider` component at the root of your app. See the [framework setup guide](../frameworks) to learn how to set this up.

## Disabled items[#](#disabled-items)

---

`useListBox` supports marking items as disabled using the `disabledKeys` prop. Each key in this list
corresponds with the `key` prop passed to the `Item` component, or automatically derived from the values passed
to the `items` prop. See [Collections](https://react-spectrum.adobe.com/v3/collections.html) for more details.

Disabled items are not focusable, selectable, or keyboard navigable. The `isDisabled` property returned by
`useOption` can be used to style the item appropriately.

```
<ListBox
  label="Choose sandwich contents"
  selectionMode="multiple"
  disabledKeys={['tuna']}
>
  <Item key="lettuce">Lettuce</Item>
  <Item key="tomato">Tomato</Item>
  <Item key="cheese">Cheese</Item>
  <Item key="tuna">Tuna Salad</Item>
  <Item key="egg">Egg Salad</Item>
  <Item key="ham">Ham</Item>
</ListBox>
```

```
<ListBox
  label="Choose sandwich contents"
  selectionMode="multiple"
  disabledKeys={['tuna']}
>
  <Item key="lettuce">Lettuce</Item>
  <Item key="tomato">Tomato</Item>
  <Item key="cheese">Cheese</Item>
  <Item key="tuna">Tuna Salad</Item>
  <Item key="egg">Egg Salad</Item>
  <Item key="ham">Ham</Item>
</ListBox>
```

```
<ListBox
  label="Choose sandwich contents"
  selectionMode="multiple"
  disabledKeys={[
    'tuna'
  ]}
>
  <Item key="lettuce">
    Lettuce
  </Item>
  <Item key="tomato">
    Tomato
  </Item>
  <Item key="cheese">
    Cheese
  </Item>
  <Item key="tuna">
    Tuna Salad
  </Item>
  <Item key="egg">
    Egg Salad
  </Item>
  <Item key="ham">
    Ham
  </Item>
</ListBox>
```

## Internationalization[#](#internationalization)

---

`useListBox` handles some aspects of internationalization automatically.
For example, type to select is implemented with an
[Intl.Collator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Collator)
for internationalized string matching. You are responsible for localizing all labels and option
content that is passed into the listbox.

### RTL[#](#rtl)

In right-to-left languages, the listbox options should be mirrored. The text content should be
aligned to the right. Ensure that your CSS accounts for this.

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `isVirtualized` | `boolean` | â | Whether the listbox uses virtual scrolling. |
| `keyboardDelegate` | `KeyboardDelegate` | â | An optional keyboard delegate implementation for type to select, to override the default. |
| `layoutDelegate` | `LayoutDelegate` | â | A delegate object that provides layout information for items in the collection. By default this uses the DOM, but this can be overridden to implement things like virtualized scrolling. |
| `shouldUseVirtualFocus` | `boolean` | â | Whether the listbox items should use virtual focus instead of being focused directly. |
| `linkBehavior` | `'action' |Â 'selection' |Â 'override'` | `'override'` | The behavior of links in the collection. - 'action': link behaves like onAction. - 'selection': link follows selection interactions (e.g. if URL drives selection). - 'override': links override all other interactions (link items are not selectable). |
| `label` | `ReactNode` | â | An optional visual label for the listbox. |
| `selectionBehavior` | `SelectionBehavior` | â | How multiple selection should behave in the collection. |
| `shouldSelectOnPressUp` | `boolean` | â | Whether selection should occur on press up instead of press down. |
| `shouldFocusOnHover` | `boolean` | â | Whether options should be focused when the user hovers over them. |
| `onAction` | `( (key: Key )) => void` | â | Handler that is called when a user performs an action on an item. The exact user event depends on the collection's `selectionBehavior` prop and the interaction modality. |
| `escapeKeyBehavior` | `'clearSelection' |Â 'none'` | `'clearSelection'` | Whether pressing the escape key should clear selection in the listbox or not.  Most experiences should not modify this option as it eliminates a keyboard user's ability to easily clear selection. Only use if the escape key is being handled externally or should not trigger selection clearing contextually. |
| `autoFocus` | `boolean |Â FocusStrategy` | â | Whether to auto focus the listbox or an option. |
| `shouldFocusWrap` | `boolean` | â | Whether focus should wrap around when the end/start is reached. |
| `items` | `Iterable<T>` | â | Item objects in the collection. |
| `disabledKeys` | `Iterable<Key>` | â | The item keys that are disabled. These items cannot be selected, focused, or otherwise interacted with. |
| `selectionMode` | `SelectionMode` | â | The type of selection that is allowed in the collection. |
| `disallowEmptySelection` | `boolean` | â | Whether the collection allows empty selection. |
| `selectedKeys` | `'all' |Â Iterable<Key>` | â | The currently selected keys in the collection (controlled). |
| `defaultSelectedKeys` | `'all' |Â Iterable<Key>` | â | The initial selected keys in the collection (uncontrolled). |
| `onSelectionChange` | `( (keys: Selection )) => void` | â | Handler that is called when the selection changes. |
| `onFocus` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | â | Handler that is called when the element's focus status changes. |
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `aria-label` | `string` | â | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |

| Method | Description |
| --- | --- |
| `getKeyBelow( (key: Key )): Key |Â null` | Returns the key visually below the given one, or `null` for none. |
| `getKeyAbove( (key: Key )): Key |Â null` | Returns the key visually above the given one, or `null` for none. |
| `getKeyLeftOf( (key: Key )): Key |Â null` | Returns the key visually to the left of the given one, or `null` for none. |
| `getKeyRightOf( (key: Key )): Key |Â null` | Returns the key visually to the right of the given one, or `null` for none. |
| `getKeyPageBelow( (key: Key )): Key |Â null` | Returns the key visually one page below the given one, or `null` for none. |
| `getKeyPageAbove( (key: Key )): Key |Â null` | Returns the key visually one page above the given one, or `null` for none. |
| `getFirstKey( (key?: Key |Â  |Â null, , global?: boolean )): Key |Â null` | Returns the first key, or `null` for none. |
| `getLastKey( (key?: Key |Â  |Â null, , global?: boolean )): Key |Â null` | Returns the last key, or `null` for none. |
| `getKeyForSearch( (search: string, , fromKey?: Key |Â  |Â null )): Key |Â null` | Returns the next key after `fromKey` that matches the given search string, or `null` for none. |

A LayoutDelegate provides layout information for collection items.

| Method | Description |
| --- | --- |
| `getItemRect( (key: Key )): Rect |Â null` | Returns a rectangle for the item with the given key. |
| `getVisibleRect(): Rect` | Returns the visible rectangle of the collection. |
| `getContentSize(): Size` | Returns the size of the scrollable content in the collection. |
| `getKeyRange( (from: Key, , to: Key )): Key[]` | Returns a list of keys between `from` and `to`. |

| Name | Type | Description |
| --- | --- | --- |
| `x` | `number` |  |
| `y` | `number` |  |
| `width` | `number` |  |
| `height` | `number` |  |

| Name | Type | Description |
| --- | --- | --- |
| `width` | `number` |  |
| `height` | `number` |  |

`'toggle' |Â 'replace'`

`string |Â number`

`'first' |Â 'last'`

`'none'
|Â 'single'
|Â 'multiple'`

`'all' |Â Set<Key>`

| Name | Type | Description |
| --- | --- | --- |
| `collection` | `Collection<Node<T>>` | A collection of items in the list. |
| `disabledKeys` | `Set<Key>` | A set of items that are disabled. |
| `selectionManager` | `SelectionManager` | A selection manager to read and update multiple selection state. |

A generic interface to access a readonly sequential
collection of unique keyed items.

**Extends**: `Iterable`

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `size` | `number` | The number of items in the collection. |

### Methods

| Method | Description |
| --- | --- |
| `getKeys(): Iterable<Key>` | Iterate over all keys in the collection. |
| `getItem( (key: Key )): T |Â null` | Get an item by its key. |
| `at( (idx: number )): T |Â null` | Get an item by the index of its key. |
| `getKeyBefore( (key: Key )): Key |Â null` | Get the key that comes before the given key in the collection. |
| `getKeyAfter( (key: Key )): Key |Â null` | Get the key that comes after the given key in the collection. |
| `getFirstKey(): Key |Â null` | Get the first key in the collection. |
| `getLastKey(): Key |Â null` | Get the last key in the collection. |
| `getChildren( (key: Key )): Iterable<T>` | Iterate over the child items of the given key. |
| `getTextValue( (key: Key )): string` | Returns a string representation of the item's contents. |
| `filter( (filterFn: ( (nodeValue: string, , node: T )) => boolean )): Collection<T>` | Filters the collection using the given function. |

| Name | Type | Description |
| --- | --- | --- |
| `type` | `string` | The type of item this node represents. |
| `key` | `Key` | A unique key for the node. |
| `value` | `T |Â null` | The object value the node was created from. |
| `level` | `number` | The level of depth this node is at in the hierarchy. |
| `hasChildNodes` | `boolean` | Whether this item has children, even if not loaded yet. |
| `rendered` | `ReactNode` | The rendered contents of this node (e.g. JSX). |
| `textValue` | `string` | A string value for this node, used for features like typeahead. |
| `index` | `number` | The index of this node within its parent. |
| `aria-label` | `string` | An accessibility label for this node. |
| `wrapper` | `( (element: ReactElement )) => ReactElement` | A function that should be called to wrap the rendered node. |
| `parentKey` | `Key |Â null` | The key of the parent node. |
| `prevKey` | `Key |Â null` | The key of the node before this node. |
| `nextKey` | `Key |Â null` | The key of the node after this node. |
| `props` | `any` | Additional properties specific to a particular node type. |
| `render` | `( (node: Node<any> )) => ReactElement` | A function that renders this node to a React Element in the DOM. |

An interface for reading and updating multiple selection state.

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `collection` | `Collection<Node<unknown>>` |  |
| `selectionMode` | `SelectionMode` | The type of selection that is allowed in the collection. |
| `disallowEmptySelection` | `boolean` | Whether the collection allows empty selection. |
| `selectionBehavior` | `SelectionBehavior` | The selection behavior for the collection. |
| `isFocused` | `boolean` | Whether the collection is currently focused. |
| `focusedKey` | `Key |Â null` | The current focused key in the collection. |
| `childFocusStrategy` | `FocusStrategy |Â null` | Whether the first or last child of the focused key should receive focus. |
| `selectedKeys` | `Set<Key>` | The currently selected keys in the collection. |
| `rawSelection` | `Selection` | The raw selection value for the collection. Either 'all' for select all, or a set of keys. |
| `isEmpty` | `boolean` | Whether the selection is empty. |
| `isSelectAll` | `boolean` | Whether all items in the collection are selected. |
| `firstSelectedKey` | `Key |Â null` |  |
| `lastSelectedKey` | `Key |Â null` |  |
| `disabledKeys` | `Set<Key>` |  |
| `disabledBehavior` | `DisabledBehavior` |  |

### Methods

| Method | Description |
| --- | --- |
| `constructor( collection: Collection<Node<unknown>>, state: MultipleSelectionState, options?: SelectionManagerOptions ): void` |  |
| `setSelectionBehavior( (selectionBehavior: SelectionBehavior )): void` | Sets the selection behavior for the collection. |
| `setFocused( (isFocused: boolean )): void` | Sets whether the collection is focused. |
| `setFocusedKey( (key: Key |Â  |Â null, , childFocusStrategy?: FocusStrategy )): void` | Sets the focused key. |
| `isSelected( (key: Key )): boolean` | Returns whether a key is selected. |
| `extendSelection( (toKey: Key )): void` | Extends the selection to the given key. |
| `toggleSelection( (key: Key )): void` | Toggles whether the given key is selected. |
| `replaceSelection( (key: Key )): void` | Replaces the selection with only the given key. |
| `setSelectedKeys( (keys: Iterable<Key> )): void` | Replaces the selection with the given keys. |
| `selectAll(): void` | Selects all items in the collection. |
| `clearSelection(): void` | Removes all keys from the selection. |
| `toggleSelectAll(): void` | Toggles between select all and an empty selection. |
| `select( (key: Key, , e?: PressEvent |Â LongPressEvent |Â PointerEvent )): void` |  |
| `isSelectionEqual( (selection: Set<Key> )): boolean` | Returns whether the current selection is equal to the given selection. |
| `canSelectItem( (key: Key )): boolean` |  |
| `isDisabled( (key: Key )): boolean` |  |
| `isLink( (key: Key )): boolean` |  |
| `getItemProps( (key: Key )): any` |  |
| `withCollection( (collection: Collection<Node<unknown>> )): SelectionManager` |  |

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `selectionMode` | `SelectionMode` | The type of selection that is allowed in the collection. |
| `selectionBehavior` | `SelectionBehavior` | The selection behavior for the collection. |
| `disallowEmptySelection` | `boolean` | Whether the collection allows empty selection. |
| `selectedKeys` | `Selection` | The currently selected keys in the collection. |
| `disabledKeys` | `Set<Key>` | The currently disabled keys in the collection. |
| `disabledBehavior` | `DisabledBehavior` | Whether `disabledKeys` applies to selection, actions, or both. |
| `isFocused` | `boolean` | Whether the collection is currently focused. |
| `focusedKey` | `Key |Â null` | The current focused key in the collection. |
| `childFocusStrategy` | `FocusStrategy |Â null` | Whether the first or last child of the focused key should receive focus. |

### Methods

| Method | Description |
| --- | --- |
| `setSelectionBehavior( (selectionBehavior: SelectionBehavior )): void` | Sets the selection behavior for the collection. |
| `setSelectedKeys( (keys: Selection )): void` | Sets the selected keys in the collection. |
| `setFocused( (isFocused: boolean )): void` | Sets whether the collection is focused. |
| `setFocusedKey( (key: Key |Â  |Â null, , child?: FocusStrategy )): void` | Sets the focused key, and optionally, whether the first or last child of that key should receive focus. |

`'selection' |Â 'all'`

| Name | Type | Description |
| --- | --- | --- |
| `allowsCellSelection` | `boolean` |  |
| `layoutDelegate` | `LayoutDelegate` |  |

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `type` | `'pressstart' |Â 'pressend' |Â 'pressup' |Â 'press'` | The type of press event being fired. |
| `pointerType` | `PointerType` | The pointer type that triggered the press event. |
| `target` | `Element` | The target element of the press event. |
| `shiftKey` | `boolean` | Whether the shift keyboard modifier was held during the press event. |
| `ctrlKey` | `boolean` | Whether the ctrl keyboard modifier was held during the press event. |
| `metaKey` | `boolean` | Whether the meta keyboard modifier was held during the press event. |
| `altKey` | `boolean` | Whether the alt keyboard modifier was held during the press event. |
| `x` | `number` | X position relative to the target. |
| `y` | `number` | Y position relative to the target. |

### Methods

| Method | Description |
| --- | --- |
| `continuePropagation(): void` | By default, press events stop propagation to parent elements. In cases where a handler decides not to handle a specific event, it can call `continuePropagation()` to allow a parent to handle it. |

`'mouse'
|Â 'pen'
|Â 'touch'
|Â 'keyboard'
|Â 'virtual'`

| Name | Type | Description |
| --- | --- | --- |
| `type` | `'longpressstart' |Â 'longpressend' |Â 'longpress'` | The type of long press event being fired. |
| `pointerType` | `PointerType` | The pointer type that triggered the press event. |
| `target` | `Element` | The target element of the press event. |
| `shiftKey` | `boolean` | Whether the shift keyboard modifier was held during the press event. |
| `ctrlKey` | `boolean` | Whether the ctrl keyboard modifier was held during the press event. |
| `metaKey` | `boolean` | Whether the meta keyboard modifier was held during the press event. |
| `altKey` | `boolean` | Whether the alt keyboard modifier was held during the press event. |
| `x` | `number` | X position relative to the target. |
| `y` | `number` | Y position relative to the target. |

| Name | Type | Description |
| --- | --- | --- |
| `current` | `T` |  |

| Name | Type | Description |
| --- | --- | --- |
| `listBoxProps` | `DOMAttributes` | Props for the listbox element. |
| `labelProps` | `DOMAttributes` | Props for the listbox's visual label element (if any). |

All DOM attributes supported across both HTML and SVG elements.

**Extends**: `AriaAttributes, ReactDOMAttributes`

| Name | Type | Description |
| --- | --- | --- |
| `id` | `string |Â undefined` |  |
| `role` | `AriaRole |Â undefined` |  |
| `tabIndex` | `number |Â undefined` |  |
| `style` | `CSSProperties |Â undefined` |  |
| `className` | `string |Â undefined` |  |

Any focusable element, including both HTML and SVG elements.

**Extends**: `Element, HTMLOrSVGElement`

| Name | Type | Description |
| --- | --- | --- |
| `key` | `Key` | The unique key for the option. |
| `aria-label` | `string` | A screen reader only label for the option. |

| Name | Type | Description |
| --- | --- | --- |
| `optionProps` | `DOMAttributes` | Props for the option element. |
| `labelProps` | `DOMAttributes` | Props for the main text element inside the option. |
| `descriptionProps` | `DOMAttributes` | Props for the description text element inside the option, if any. |
| `isFocused` | `boolean` | Whether the option is currently focused. |
| `isFocusVisible` | `boolean` | Whether the option is keyboard focused. |
| `isPressed` | `boolean` | Whether the item is currently in a pressed state. |
| `isSelected` | `boolean` | Whether the item is currently selected. |
| `isDisabled` | `boolean` | Whether the item is non-interactive, i.e. both selection and actions are disabled and the item may not be focused. Dependent on `disabledKeys` and `disabledBehavior`. |
| `allowsSelection` | `boolean` | Whether the item may be selected, dependent on `selectionMode`, `disabledKeys`, and `disabledBehavior`. |
| `hasAction` | `boolean` | Whether the item has an action, dependent on `onAction`, `disabledKeys`, and `disabledBehavior`. It may also change depending on the current selection state of the list (e.g. when selection is primary). This can be used to enable or disable hover styles or other visual indications of interactivity. |

| Name | Type | Description |
| --- | --- | --- |
| `heading` | `ReactNode` | The heading for the section. |
| `aria-label` | `string` | An accessibility label for the section. Required if `heading` is not present. |

| Name | Type | Description |
| --- | --- | --- |
| `itemProps` | `DOMAttributes` | Props for the wrapper list item. |
| `headingProps` | `DOMAttributes` | Props for the heading element, if any. |
| `groupProps` | `DOMAttributes` | Props for the group element. |

Provides state management for list-like components. Handles building a collection
of items from props, and manages multiple selection state.

`useListState<T extends object>(
(props: ListProps<T>
)): ListState<T>`

| Name | Type | Description |
| --- | --- | --- |
| `filter` | `( (nodes: Iterable<Node<T>> )) => Iterable<Node<T>>` | Filter function to generate a filtered list of nodes. |
| `layoutDelegate` | `LayoutDelegate` | A delegate object that provides layout information for items in the collection. This can be used to override the behavior of shift selection. |
| `collection` | `Collection<Node<T>>` | A pre-constructed collection to use instead of building one from items and children. |
| `selectionBehavior` | `SelectionBehavior` | How multiple selection should behave in the collection. |
| `allowDuplicateSelectionEvents` | `boolean` | Whether onSelectionChange should fire even if the new set of keys is the same as the last. |
| `disabledBehavior` | `DisabledBehavior` | Whether `disabledKeys` applies to all interactions, or only selection. |
| `selectionMode` | `SelectionMode` | The type of selection that is allowed in the collection. |
| `disallowEmptySelection` | `boolean` | Whether the collection allows empty selection. |
| `selectedKeys` | `'all' |Â Iterable<Key>` | The currently selected keys in the collection (controlled). |
| `defaultSelectedKeys` | `'all' |Â Iterable<Key>` | The initial selected keys in the collection (uncontrolled). |
| `onSelectionChange` | `( (keys: Selection )) => void` | Handler that is called when the selection changes. |
| `disabledKeys` | `Iterable<Key>` | The currently disabled keys in the collection (controlled). |

Provides the behavior and accessibility implementation for a listbox component.
A listbox displays a list of options and allows a user to select one or more of them.

`useListBox<T>(
props: AriaListBoxOptions<T>,
state: ListState<T>,
ref: RefObject<HTMLElement
|Â  |Â null>
): ListBoxAria`

Provides the behavior and accessibility implementation for an option in a listbox.
See `useListBox` for more details about listboxes.

`useOption<T>(
props: AriaOptionProps,
state: ListState<T>,
ref: RefObject<FocusableElement
|Â  |Â null>
): OptionAria`

Provides the behavior and accessibility implementation for a section in a listbox.
See `useListBox` for more details about listboxes.

`useListBoxSection(
(props: AriaListBoxSectionProps
)): ListBoxSectionAria`

A RouterProvider accepts a `navigate` function from a framework or client side router,
and provides it to all nested React Aria links to enable client side navigation.

| Name | Type | Description |
| --- | --- | --- |
| `navigate` | `( (path: Href, , routerOptions: RouterOptions |Â  |Â undefined )) => void` |  |
| `children` | `ReactNode` |  |
| `useHref` | `( (href: Href )) => string` |  |

`RouterConfig extends {

href: any

} ? H : string`

This type allows configuring link props with router options and type-safe URLs via TS module augmentation.
By default, this is an empty type. Extend with `href` and `routerOptions` properties to configure your router.

`RouterConfig extends {

routerOptions: any

} ? O : never`