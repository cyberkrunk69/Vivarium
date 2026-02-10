# useSelect

Source: https://react-spectrum.adobe.com/react-aria/useSelect.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../Select).

# useSelect

Provides the behavior and accessibility implementation for a select component.
A select displays a collapsible list of options and allows a user to select one of them.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useSelect} from 'react-aria'` |

[View ARIA pattern

W3C](https://www.w3.org/WAI/ARIA/apg/patterns/listbox/ "View ARIA pattern")[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/select "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/select "View package")

## API[#](#api)

---

`useSelect<T, M extends SelectionMode = 'single'>(
props: AriaSelectOptions<T, M>,
state: SelectState<T, M>,
ref: RefObject<HTMLElement
|Â  |Â null>
): SelectAria<T, M>`

## Features[#](#features)

---

A select can be built using the [<select>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select)
and [<option>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/option) HTML elements, but this is
not possible to style consistently cross browser, especially the options. `useSelect` helps achieve accessible
select components that can be styled as needed without compromising on high quality interactions.

- Exposed to assistive technology as a button with a `listbox` popup using ARIA (combined with [useListBox](../ListBox/useListBox.html))
- Support for selecting a single option
- Support for disabled options
- Support for sections
- Labeling support for accessibility
- Support for native HTML constraint validation with customizable UI, custom validation functions, realtime validation, and server-side validation errors
- Support for mouse, touch, and keyboard interactions
- Tab stop focus management
- Keyboard support for opening the listbox using the arrow keys, including automatically focusing
  the first or last item accordingly
- Typeahead to allow selecting options by typing text, even without opening the listbox
- Browser autofill integration via a hidden native `<select>` element
- Mobile screen reader listbox dismissal support

## Anatomy[#](#anatomy)

---

A select consists of a label, a button which displays a selected value, and a listbox, displayed in a
popup. Users can click, touch, or use the keyboard on the button to open the listbox popup. `useSelect`
handles exposing the correct ARIA attributes for accessibility and handles the interactions for the
select in its collapsed state. It should be combined with [useListBox](../ListBox/useListBox.html), which handles
the implementation of the popup listbox.

`useSelect` also supports optional description and error message elements, which can be used
to provide more context about the field, and any validation messages. These are linked with the
input via the `aria-describedby` attribute.

`useSelect` returns props that you should spread onto the appropriate element:

| Name | Type | Description |
| --- | --- | --- |
| `labelProps` | `DOMAttributes` | Props for the label element. |
| `triggerProps` | `AriaButtonProps` | Props for the popup trigger element. |
| `valueProps` | `DOMAttributes` | Props for the element representing the selected value. |
| `menuProps` | `AriaListBoxOptions<T>` | Props for the popup. |
| `descriptionProps` | `DOMAttributes` | Props for the select's description element, if any. |
| `errorMessageProps` | `DOMAttributes` | Props for the select's error message element, if any. |
| `hiddenSelectProps` | `HiddenSelectProps<T, SelectionMode>` | Props for the hidden select element. |
| `isInvalid` | `boolean` | Whether the input value is invalid. |
| `validationErrors` | `string[]` | The current error messages for the input if it is invalid, otherwise an empty array. |
| `validationDetails` | `ValidityState` | The native validation details for the input. |

State is managed by the `useSelectState`
hook from `@react-stately/select`. The state object should be passed as an option to `useSelect`

If a select does not have a visible label, an `aria-label` or `aria-labelledby`
prop must be passed instead to identify it to assistive technology.

## State management[#](#state-management)

---

`useSelect` requires knowledge of the options in the select in order to handle keyboard
navigation and other interactions. It does this using the `Collection`
interface, which is a generic interface to access sequential unique keyed data. You can
implement this interface yourself, e.g. by using a prop to pass a list of item objects,
but `useSelectState` from
`@react-stately/select` implements a JSX based interface for building collections instead.
See [Collection Components](https://react-spectrum.adobe.com/v3/collections.html) for more information.

In addition, `useSelectState`
manages the state necessary for multiple selection and exposes
a `SelectionManager`,
which makes use of the collection to provide an interface to update the selection state.
It also holds state to track if the popup is open.
For more information about selection, see [Selection](https://react-spectrum.adobe.com/v3/selection.html).

## Example[#](#example)

---

This example uses a `<button>` element for the trigger, with a `<span>` inside to hold the value,
and another for the dropdown arrow icon (hidden from screen readers with `aria-hidden`).
A <`HiddenSelect`> is used to render a hidden native
`<select>`, which enables browser form autofill support.

The same `Popover`, `ListBox`, and `Button` components created with [usePopover](../Popover/usePopover.html), [useListBox](../ListBox/useListBox.html),
and [useButton](../Button/useButton.html) that you may already have in your component library or application should be reused. These can be shared with other
components such as a `ComboBox` created with [useComboBox](../ComboBox/useComboBox.html) or a `Dialog` popover created with [useDialog](../Modal/useDialog.html).
The code for these components is also included below in the collapsed sections.

In addition, see [useListBox](../ListBox/useListBox.html) for examples of sections (option groups), and more complex
options. For an example of the description and error message elements, see [useTextField](../TextField/useTextField.html).

```
import {Item, useSelectState} from 'react-stately';
import {HiddenSelect, useSelect} from 'react-aria';

// Reuse the ListBox, Popover, and Button from your component library. See below for details.
import {Button, ListBox, Popover} from 'your-component-library';

function Select(props) {
  // Create state based on the incoming props
  let state = useSelectState(props);

  // Get props for child elements from useSelect
  let ref = React.useRef(null);
  let {
    labelProps,
    triggerProps,
    valueProps,
    menuProps,
    hiddenSelectProps
  } = useSelect(props, state, ref);

  return (
    <div style={{ display: 'inline-block' }}>
      <div {...labelProps}>{props.label}</div>
      <HiddenSelect {...hiddenSelectProps} />
      <Button
        {...triggerProps}
        buttonRef={ref}
        style={{ height: 30, fontSize: 14 }}
      >
        <span {...valueProps}>
          {state.selectedItem
            ? state.selectedItem.rendered
            : 'Select an option'}
        </span>
        <span
          aria-hidden="true"
          style={{ paddingLeft: 5 }}
        >
          â¼
        </span>
      </Button>
      {state.isOpen &&
        (
          <Popover state={state} triggerRef={ref} placement="bottom start">
            <ListBox
              {...menuProps}
              state={state}
            />
          </Popover>
        )}
    </div>
  );
}

<Select label="Favorite Color">
  <Item>Red</Item>
  <Item>Orange</Item>
  <Item>Yellow</Item>
  <Item>Green</Item>
  <Item>Blue</Item>
  <Item>Purple</Item>
  <Item>Black</Item>
  <Item>White</Item>
  <Item>Lime</Item>
  <Item>Fushsia</Item>
</Select>
```

```
import {Item, useSelectState} from 'react-stately';
import {HiddenSelect, useSelect} from 'react-aria';

// Reuse the ListBox, Popover, and Button from your component library. See below for details.
import {
  Button,
  ListBox,
  Popover
} from 'your-component-library';

function Select(props) {
  // Create state based on the incoming props
  let state = useSelectState(props);

  // Get props for child elements from useSelect
  let ref = React.useRef(null);
  let {
    labelProps,
    triggerProps,
    valueProps,
    menuProps,
    hiddenSelectProps
  } = useSelect(props, state, ref);

  return (
    <div style={{ display: 'inline-block' }}>
      <div {...labelProps}>{props.label}</div>
      <HiddenSelect {...hiddenSelectProps} />
      <Button
        {...triggerProps}
        buttonRef={ref}
        style={{ height: 30, fontSize: 14 }}
      >
        <span {...valueProps}>
          {state.selectedItem
            ? state.selectedItem.rendered
            : 'Select an option'}
        </span>
        <span
          aria-hidden="true"
          style={{ paddingLeft: 5 }}
        >
          â¼
        </span>
      </Button>
      {state.isOpen &&
        (
          <Popover
            state={state}
            triggerRef={ref}
            placement="bottom start"
          >
            <ListBox
              {...menuProps}
              state={state}
            />
          </Popover>
        )}
    </div>
  );
}

<Select label="Favorite Color">
  <Item>Red</Item>
  <Item>Orange</Item>
  <Item>Yellow</Item>
  <Item>Green</Item>
  <Item>Blue</Item>
  <Item>Purple</Item>
  <Item>Black</Item>
  <Item>White</Item>
  <Item>Lime</Item>
  <Item>Fushsia</Item>
</Select>
```

```
import {
  Item,
  useSelectState
} from 'react-stately';
import {
  HiddenSelect,
  useSelect
} from 'react-aria';

// Reuse the ListBox, Popover, and Button from your component library. See below for details.
import {
  Button,
  ListBox,
  Popover
} from 'your-component-library';

function Select(props) {
  // Create state based on the incoming props
  let state =
    useSelectState(
      props
    );

  // Get props for child elements from useSelect
  let ref = React.useRef(
    null
  );
  let {
    labelProps,
    triggerProps,
    valueProps,
    menuProps,
    hiddenSelectProps
  } = useSelect(
    props,
    state,
    ref
  );

  return (
    <div
      style={{
        display:
          'inline-block'
      }}
    >
      <div
        {...labelProps}
      >
        {props.label}
      </div>
      <HiddenSelect
        {...hiddenSelectProps}
      />
      <Button
        {...triggerProps}
        buttonRef={ref}
        style={{
          height: 30,
          fontSize: 14
        }}
      >
        <span
          {...valueProps}
        >
          {state
              .selectedItem
            ? state
              .selectedItem
              .rendered
            : 'Select an option'}
        </span>
        <span
          aria-hidden="true"
          style={{
            paddingLeft:
              5
          }}
        >
          â¼
        </span>
      </Button>
      {state.isOpen &&
        (
          <Popover
            state={state}
            triggerRef={ref}
            placement="bottom start"
          >
            <ListBox
              {...menuProps}
              state={state}
            />
          </Popover>
        )}
    </div>
  );
}

<Select label="Favorite Color">
  <Item>Red</Item>
  <Item>Orange</Item>
  <Item>Yellow</Item>
  <Item>Green</Item>
  <Item>Blue</Item>
  <Item>Purple</Item>
  <Item>Black</Item>
  <Item>White</Item>
  <Item>Lime</Item>
  <Item>Fushsia</Item>
</Select>
```

### Popover[#](#popover)

The `Popover` component is used to contain the popup listbox for the Select.
It can be shared between many other components, including [ComboBox](../ComboBox/useComboBox.html),
[Menu](../Menu/useMenu.html), and others.
See [usePopover](../Popover/usePopover.html) for more examples of popovers.

 Show code

```
import {DismissButton, Overlay, usePopover} from 'react-aria';
import type {AriaPopoverProps} from 'react-aria';
import type {OverlayTriggerState} from 'react-stately';

interface PopoverProps extends Omit<AriaPopoverProps, 'popoverRef'> {
  children: React.ReactNode;
  state: OverlayTriggerState;
}

function Popover({ children, state, ...props }: PopoverProps) {
  let popoverRef = React.useRef(null);
  let { popoverProps, underlayProps } = usePopover({
    ...props,
    popoverRef
  }, state);

  return (
    <Overlay>
      <div {...underlayProps} style={{ position: 'fixed', inset: 0 }} />
      <div
        {...popoverProps}
        ref={popoverRef}
        style={{
          ...popoverProps.style,
          background: 'var(--page-background)',
          border: '1px solid gray'
        }}
      >
        <DismissButton onDismiss={state.close} />
        {children}
        <DismissButton onDismiss={state.close} />
      </div>
    </Overlay>
  );
}
```

```
import {
  DismissButton,
  Overlay,
  usePopover
} from 'react-aria';
import type {AriaPopoverProps} from 'react-aria';
import type {OverlayTriggerState} from 'react-stately';

interface PopoverProps
  extends Omit<AriaPopoverProps, 'popoverRef'> {
  children: React.ReactNode;
  state: OverlayTriggerState;
}

function Popover(
  { children, state, ...props }: PopoverProps
) {
  let popoverRef = React.useRef(null);
  let { popoverProps, underlayProps } = usePopover({
    ...props,
    popoverRef
  }, state);

  return (
    <Overlay>
      <div
        {...underlayProps}
        style={{ position: 'fixed', inset: 0 }}
      />
      <div
        {...popoverProps}
        ref={popoverRef}
        style={{
          ...popoverProps.style,
          background: 'var(--page-background)',
          border: '1px solid gray'
        }}
      >
        <DismissButton onDismiss={state.close} />
        {children}
        <DismissButton onDismiss={state.close} />
      </div>
    </Overlay>
  );
}
```

```
import {
  DismissButton,
  Overlay,
  usePopover
} from 'react-aria';
import type {AriaPopoverProps} from 'react-aria';
import type {OverlayTriggerState} from 'react-stately';

interface PopoverProps
  extends
    Omit<
      AriaPopoverProps,
      'popoverRef'
    > {
  children:
    React.ReactNode;
  state:
    OverlayTriggerState;
}

function Popover(
  {
    children,
    state,
    ...props
  }: PopoverProps
) {
  let popoverRef = React
    .useRef(null);
  let {
    popoverProps,
    underlayProps
  } = usePopover({
    ...props,
    popoverRef
  }, state);

  return (
    <Overlay>
      <div
        {...underlayProps}
        style={{
          position:
            'fixed',
          inset: 0
        }}
      />
      <div
        {...popoverProps}
        ref={popoverRef}
        style={{
          ...popoverProps
            .style,
          background:
            'var(--page-background)',
          border:
            '1px solid gray'
        }}
      >
        <DismissButton
          onDismiss={state
            .close}
        />
        {children}
        <DismissButton
          onDismiss={state
            .close}
        />
      </div>
    </Overlay>
  );
}
```

### ListBox[#](#listbox)

The `ListBox` and `Option` components are used to show the list of options.
They can also be shared with other components like a [ComboBox](../ComboBox/useComboBox.html). See
[useListBox](../ListBox/useListBox.html) for more examples, including sections and more complex items.

 Show code

```
import {useListBox, useOption} from 'react-aria';

function ListBox(props) {
  let ref = React.useRef(null);
  let { listBoxRef = ref, state } = props;
  let { listBoxProps } = useListBox(props, state, listBoxRef);

  return (
    <ul
      {...listBoxProps}
      ref={listBoxRef}
      style={{
        margin: 0,
        padding: 0,
        listStyle: 'none',
        maxHeight: 150,
        overflow: 'auto',
        minWidth: 100,
        background: 'lightgray'
      }}
    >
      {[...state.collection].map((item) => (
        <Option
          key={item.key}
          item={item}
          state={state}
        />
      ))}
    </ul>
  );
}

function Option({ item, state }) {
  let ref = React.useRef(null);
  let { optionProps, isSelected, isFocused, isDisabled } = useOption(
    { key: item.key },
    state,
    ref
  );

  return (
    <li
      {...optionProps}
      ref={ref}
      style={{
        background: isFocused ? 'gray' : 'transparent',
        color: isDisabled ? 'gray' : isFocused ? 'white' : 'black',
        padding: '2px 5px',
        outline: 'none',
        cursor: 'pointer',
        display: 'flex',
        justifyContent: 'space-between',
        gap: '10px'
      }}
    >
      {item.rendered}
      {isSelected ? <span>â</span> : null}
    </li>
  );
}
```

```
import {useListBox, useOption} from 'react-aria';

function ListBox(props) {
  let ref = React.useRef(null);
  let { listBoxRef = ref, state } = props;
  let { listBoxProps } = useListBox(
    props,
    state,
    listBoxRef
  );

  return (
    <ul
      {...listBoxProps}
      ref={listBoxRef}
      style={{
        margin: 0,
        padding: 0,
        listStyle: 'none',
        maxHeight: 150,
        overflow: 'auto',
        minWidth: 100,
        background: 'lightgray'
      }}
    >
      {[...state.collection].map((item) => (
        <Option
          key={item.key}
          item={item}
          state={state}
        />
      ))}
    </ul>
  );
}

function Option({ item, state }) {
  let ref = React.useRef(null);
  let { optionProps, isSelected, isFocused, isDisabled } =
    useOption({ key: item.key }, state, ref);

  return (
    <li
      {...optionProps}
      ref={ref}
      style={{
        background: isFocused ? 'gray' : 'transparent',
        color: isDisabled
          ? 'gray'
          : isFocused
          ? 'white'
          : 'black',
        padding: '2px 5px',
        outline: 'none',
        cursor: 'pointer',
        display: 'flex',
        justifyContent: 'space-between',
        gap: '10px'
      }}
    >
      {item.rendered}
      {isSelected ? <span>â</span> : null}
    </li>
  );
}
```

```
import {
  useListBox,
  useOption
} from 'react-aria';

function ListBox(props) {
  let ref = React.useRef(
    null
  );
  let {
    listBoxRef = ref,
    state
  } = props;
  let { listBoxProps } =
    useListBox(
      props,
      state,
      listBoxRef
    );

  return (
    <ul
      {...listBoxProps}
      ref={listBoxRef}
      style={{
        margin: 0,
        padding: 0,
        listStyle:
          'none',
        maxHeight: 150,
        overflow: 'auto',
        minWidth: 100,
        background:
          'lightgray'
      }}
    >
      {[
        ...state
          .collection
      ].map((item) => (
        <Option
          key={item.key}
          item={item}
          state={state}
        />
      ))}
    </ul>
  );
}

function Option(
  { item, state }
) {
  let ref = React.useRef(
    null
  );
  let {
    optionProps,
    isSelected,
    isFocused,
    isDisabled
  } = useOption(
    { key: item.key },
    state,
    ref
  );

  return (
    <li
      {...optionProps}
      ref={ref}
      style={{
        background:
          isFocused
            ? 'gray'
            : 'transparent',
        color: isDisabled
          ? 'gray'
          : isFocused
          ? 'white'
          : 'black',
        padding:
          '2px 5px',
        outline: 'none',
        cursor:
          'pointer',
        display: 'flex',
        justifyContent:
          'space-between',
        gap: '10px'
      }}
    >
      {item.rendered}
      {isSelected
        ? <span>â</span>
        : null}
    </li>
  );
}
```

### Button[#](#button)

The `Button` component is used in the above example to toggle the listbox popup. It is built using the [useButton](../Button/useButton.html) hook, and can be shared with many other components.

 Show code

```
import {useButton} from 'react-aria';

function Button(props) {
  let ref = props.buttonRef;
  let { buttonProps } = useButton(props, ref);
  return (
    <button {...buttonProps} ref={ref} style={props.style}>
      {props.children}
    </button>
  );
}
```

```
import {useButton} from 'react-aria';

function Button(props) {
  let ref = props.buttonRef;
  let { buttonProps } = useButton(props, ref);
  return (
    <button {...buttonProps} ref={ref} style={props.style}>
      {props.children}
    </button>
  );
}
```

```
import {useButton} from 'react-aria';

function Button(props) {
  let ref =
    props.buttonRef;
  let { buttonProps } =
    useButton(
      props,
      ref
    );
  return (
    <button
      {...buttonProps}
      ref={ref}
      style={props.style}
    >
      {props.children}
    </button>
  );
}
```

## Styled examples[#](#styled-examples)

---

[![](/example.ec784921.png)

Tailwind CSS

An example of styling a Select with Tailwind.](https://codesandbox.io/s/hardcore-moon-xzc4r?file=/src/ComboBox.tsx)
[![](/styled-components.0d9c5316.png)

Styled Components

A Select with complex item content built with Styled Components.](https://codesandbox.io/s/sharp-sun-e3fgd?file=/src/Select.tsx)
[![](/popup-example.0076b2f2.png)

Popup positioning

A Select with custom macOS-style popup positioning.](https://codesandbox.io/s/heuristic-margulis-uz3d4d?file=/src/Select.tsx)

## Usage[#](#usage)

---

The following examples show how to use the Select component created in the above example.

### Dynamic collections[#](#dynamic-collections)

`Select` follows the [Collection Components API](https://react-spectrum.adobe.com/v3/collections.html), accepting both static and dynamic collections.
The examples above show static collections, which can be used when the full list of options is known ahead of time. Dynamic collections,
as shown below, can be used when the options come from an external data source such as an API call, or update over time.

As seen below, an iterable list of options is passed to the Select using the `items` prop. Each item accepts a `key` prop, which
is passed to the `onSelectionChange` handler to identify the selected item. Alternatively, if the item objects contain an `id` property,
as shown in the example below, then this is used automatically and a `key` prop is not required.

```
function Example() {
  let options = [
    {id: 1, name: 'Aerospace'},
    {id: 2, name: 'Mechanical'},
    {id: 3, name: 'Civil'},
    {id: 4, name: 'Biomedical'},
    {id: 5, name: 'Nuclear'},
    {id: 6, name: 'Industrial'},
    {id: 7, name: 'Chemical'},
    {id: 8, name: 'Agricultural'},
    {id: 9, name: 'Electrical'}
  ];

  return (
    <>
      <Select label="Pick an engineering major" items={options}>
        {(item) => <Item>{item.name}</Item>}
      </Select>
    </>
  );
}
```

```
function Example() {
  let options = [
    { id: 1, name: 'Aerospace' },
    { id: 2, name: 'Mechanical' },
    { id: 3, name: 'Civil' },
    { id: 4, name: 'Biomedical' },
    { id: 5, name: 'Nuclear' },
    { id: 6, name: 'Industrial' },
    { id: 7, name: 'Chemical' },
    { id: 8, name: 'Agricultural' },
    { id: 9, name: 'Electrical' }
  ];

  return (
    <>
      <Select
        label="Pick an engineering major"
        items={options}
      >
        {(item) => <Item>{item.name}</Item>}
      </Select>
    </>
  );
}
```

```
function Example() {
  let options = [
    {
      id: 1,
      name: 'Aerospace'
    },
    {
      id: 2,
      name: 'Mechanical'
    },
    {
      id: 3,
      name: 'Civil'
    },
    {
      id: 4,
      name: 'Biomedical'
    },
    {
      id: 5,
      name: 'Nuclear'
    },
    {
      id: 6,
      name: 'Industrial'
    },
    {
      id: 7,
      name: 'Chemical'
    },
    {
      id: 8,
      name:
        'Agricultural'
    },
    {
      id: 9,
      name: 'Electrical'
    }
  ];

  return (
    <>
      <Select
        label="Pick an engineering major"
        items={options}
      >
        {(item) => (
          <Item>
            {item.name}
          </Item>
        )}
      </Select>
    </>
  );
}
```

### Controlled selection[#](#controlled-selection)

Setting a selected option can be done by using the `defaultSelectedKey` or `selectedKey` prop. The selected key corresponds to the `key` of an item.
When `Select` is used with a dynamic collection as described above, the key of each item is derived from the data.
See the `react-stately` [Selection docs](https://react-spectrum.adobe.com/v3/selection.html) for more details.

```
function Example() {
  let options = [
    {name: 'Koala'},
    {name: 'Kangaroo'},
    {name: 'Platypus'},
    {name: 'Bald Eagle'},
    {name: 'Bison'},
    {name: 'Skunk'}
  ];
  let [animal, setAnimal] = React.useState("Bison");

  return (
    <Select
      label="Pick an animal (controlled)"
      items={options}
      selectedKey={animal}
      onSelectionChange={selected => setAnimal(selected)}>
      {item => <Item key={item.name}>{item.name}</Item>}
    </Select>
  );
}
```

```
function Example() {
  let options = [
    {name: 'Koala'},
    {name: 'Kangaroo'},
    {name: 'Platypus'},
    {name: 'Bald Eagle'},
    {name: 'Bison'},
    {name: 'Skunk'}
  ];
  let [animal, setAnimal] = React.useState("Bison");

  return (
    <Select
      label="Pick an animal (controlled)"
      items={options}
      selectedKey={animal}
      onSelectionChange={selected => setAnimal(selected)}>
      {item => <Item key={item.name}>{item.name}</Item>}
    </Select>
  );
}
```

```
function Example() {
  let options = [
    { name: 'Koala' },
    { name: 'Kangaroo' },
    { name: 'Platypus' },
    {
      name: 'Bald Eagle'
    },
    { name: 'Bison' },
    { name: 'Skunk' }
  ];
  let [
    animal,
    setAnimal
  ] = React.useState(
    'Bison'
  );

  return (
    <Select
      label="Pick an animal (controlled)"
      items={options}
      selectedKey={animal}
      onSelectionChange={(selected) =>
        setAnimal(
          selected
        )}
    >
      {(item) => (
        <Item
          key={item.name}
        >
          {item.name}
        </Item>
      )}
    </Select>
  );
}
```

### Asynchronous loading[#](#asynchronous-loading)

This example uses the [useAsyncList](../useAsyncList.html) hook to handle asynchronous loading
of data from a server. You may additionally want to display a spinner to indicate the loading
state to the user, or support features like infinite scroll to load more data.

```
import {useAsyncList} from 'react-stately';

function AsyncLoadingExample() {
  let list = useAsyncList({
    async load({ signal, filterText }) {
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
    <Select label="Pick a Pokemon" items={list.items} selectionMode="single">
      {(item) => <Item key={item.name}>{item.name}</Item>}
    </Select>
  );
}
```

```
import {useAsyncList} from 'react-stately';

function AsyncLoadingExample() {
  let list = useAsyncList({
    async load({ signal, filterText }) {
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
    <Select
      label="Pick a Pokemon"
      items={list.items}
      selectionMode="single"
    >
      {(item) => <Item key={item.name}>{item.name}</Item>}
    </Select>
  );
}
```

```
import {useAsyncList} from 'react-stately';

function AsyncLoadingExample() {
  let list =
    useAsyncList({
      async load(
        {
          signal,
          filterText
        }
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
    <Select
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
    </Select>
  );
}
```

### Disabled[#](#disabled)

A Select can be fully disabled using the `isDisabled` prop.

```
<Select label="Choose frequency" isDisabled>
  <Item key="rarely">Rarely</Item>
  <Item key="sometimes">Sometimes</Item>
  <Item key="always">Always</Item>
</Select>
```

```
<Select label="Choose frequency" isDisabled>
  <Item key="rarely">Rarely</Item>
  <Item key="sometimes">Sometimes</Item>
  <Item key="always">Always</Item>
</Select>
```

```
<Select
  label="Choose frequency"
  isDisabled
>
  <Item key="rarely">
    Rarely
  </Item>
  <Item key="sometimes">
    Sometimes
  </Item>
  <Item key="always">
    Always
  </Item>
</Select>
```

### Disabled options[#](#disabled-options)

`useSelect` supports marking items as disabled using the `disabledKeys` prop. Each key in this list
corresponds with the `key` prop passed to the `Item` component, or automatically derived from the values passed
to the `items` prop. See [Collections](https://react-spectrum.adobe.com/v3/collections.html) for more details.

Disabled items are not focusable, selectable, or keyboard navigable. The `isDisabled` property returned by
`useOption` can be used to style the item appropriately.

```
<Select label="Favorite Animal" disabledKeys={['cat', 'kangaroo']}>
  <Item key="red panda">Red Panda</Item>
  <Item key="cat">Cat</Item>
  <Item key="dog">Dog</Item>
  <Item key="aardvark">Aardvark</Item>
  <Item key="kangaroo">Kangaroo</Item>
  <Item key="snake">Snake</Item>
</Select>
```

```
<Select
  label="Favorite Animal"
  disabledKeys={['cat', 'kangaroo']}
>
  <Item key="red panda">Red Panda</Item>
  <Item key="cat">Cat</Item>
  <Item key="dog">Dog</Item>
  <Item key="aardvark">Aardvark</Item>
  <Item key="kangaroo">Kangaroo</Item>
  <Item key="snake">Snake</Item>
</Select>
```

```
<Select
  label="Favorite Animal"
  disabledKeys={[
    'cat',
    'kangaroo'
  ]}
>
  <Item key="red panda">
    Red Panda
  </Item>
  <Item key="cat">
    Cat
  </Item>
  <Item key="dog">
    Dog
  </Item>
  <Item key="aardvark">
    Aardvark
  </Item>
  <Item key="kangaroo">
    Kangaroo
  </Item>
  <Item key="snake">
    Snake
  </Item>
</Select>
```

### Controlled open state[#](#controlled-open-state)

The open state of the select can be controlled via the `defaultOpen` and `isOpen` props

```
function Example() {
  let [open, setOpen] = React.useState(false);

  return (
    <>
      <p>Select is {open ? 'open' : 'closed'}</p>
      <Select label="Choose frequency" isOpen={open} onOpenChange={setOpen}>
        <Item key="rarely">Rarely</Item>
        <Item key="sometimes">Sometimes</Item>
        <Item key="always">Always</Item>
      </Select>
    </>
  );
}
```

```
function Example() {
  let [open, setOpen] = React.useState(false);

  return (
    <>
      <p>Select is {open ? 'open' : 'closed'}</p>
      <Select
        label="Choose frequency"
        isOpen={open}
        onOpenChange={setOpen}
      >
        <Item key="rarely">Rarely</Item>
        <Item key="sometimes">Sometimes</Item>
        <Item key="always">Always</Item>
      </Select>
    </>
  );
}
```

```
function Example() {
  let [open, setOpen] =
    React.useState(
      false
    );

  return (
    <>
      <p>
        Select is {open
          ? 'open'
          : 'closed'}
      </p>
      <Select
        label="Choose frequency"
        isOpen={open}
        onOpenChange={setOpen}
      >
        <Item key="rarely">
          Rarely
        </Item>
        <Item key="sometimes">
          Sometimes
        </Item>
        <Item key="always">
          Always
        </Item>
      </Select>
    </>
  );
}
```

### Links[#](#links)

By default, interacting with an item in a Select triggers `onSelectionChange`. Alternatively, items may be links to another page or website. This can be achieved by passing the `href` prop to the `<Item>` component. Link items in a `Select` are not selectable. See the [links](../ListBox/useListBox.html#links) section in the `useListBox` docs for details on how to support this.

## Internationalization[#](#internationalization)

---

`useSelect` and `useListBox` handle some aspects of internationalization automatically.
For example, type to select is implemented with an
[Intl.Collator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Collator)
for internationalized string matching. You are responsible for localizing all labels and option
content that is passed into the select.

### RTL[#](#rtl)

In right-to-left languages, the select should be mirrored. The arrow should be on the left,
and the selected value should be on the right. In addition, the content of list options should
flip. Ensure that your CSS accounts for this.

`'single' |Â 'multiple'`

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `keyboardDelegate` | `KeyboardDelegate` | â | An optional keyboard delegate implementation for type to select, to override the default. |
| `autoComplete` | `string` | â | Describes the type of autocomplete functionality the input should provide if any. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefautocomplete). |
| `name` | `string` | â | The name of the input, used when submitting an HTML form. |
| `form` | `string` | â | The `<form>` element to associate the input with. The value of this attribute must be the id of a `<form>` in the same document. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input#form). |
| `selectionMode` | `SelectionMode` | `'single'` | Whether single or multiple selection is enabled. |
| `isOpen` | `boolean` | â | Sets the open state of the menu. |
| `defaultOpen` | `boolean` | â | Sets the default open state of the menu. |
| `onOpenChange` | `( (isOpen: boolean )) => void` | â | Method that is called when the open state of the menu changes. |
| `allowsEmptyCollection` | `boolean` | â | Whether the select should be allowed to be open when the collection is empty. |
| `items` | `Iterable<T>` | â | Item objects in the collection. |
| `disabledKeys` | `Iterable<Key>` | â | The item keys that are disabled. These items cannot be selected, focused, or otherwise interacted with. |
| `isDisabled` | `boolean` | â | Whether the input is disabled. |
| `value` | `ValueType<SelectionMode>` | â | The current value (controlled). |
| `defaultValue` | `ValueType<SelectionMode>` | â | The default value (uncontrolled). |
| `onChange` | `( (value: T )) => void` | â | Handler that is called when the value changes. |
| `isRequired` | `boolean` | â | Whether user input is required on the input before form submission. |
| `isInvalid` | `boolean` | â | Whether the input value is invalid. |
| `validationBehavior` | `'aria' |Â 'native'` | `'aria'` | Whether to use native HTML form validation to prevent form submission when the value is missing or invalid, or mark the field as required or invalid via ARIA. |
| `validate` | `( (value: ValidationType<SelectionMode> )) => ValidationError |Â true |Â null |Â undefined` | â | A function that returns an error message if a given value is invalid. Validation errors are displayed to the user when the form is submitted if `validationBehavior="native"`. For realtime validation, use the `isInvalid` prop instead. |
| `description` | `ReactNode` | â | A description for the field. Provides a hint such as specific requirements for what to choose. |
| `errorMessage` | `ReactNode |Â ( (v: ValidationResult )) => ReactNode` | â | An error message for the field. |
| `label` | `ReactNode` | â | The content to display as the label. |
| `placeholder` | `string` | â | Temporary text that occupies the text input when it is empty. |
| `autoFocus` | `boolean` | â | Whether the element should receive focus on render. |
| `onFocus` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | â | Handler that is called when the element's focus status changes. |
| `onKeyDown` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is pressed. |
| `onKeyUp` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is released. |
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `aria-label` | `string` | â | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |
| `excludeFromTabOrder` | `boolean` | â | Whether to exclude the element from the sequential tab order. If true, the element will not be focusable via the keyboard by tabbing. This should be avoided except in rare scenarios where an alternative means of accessing the element or its functionality via the keyboard is available. |

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

`string |Â number`

`SelectionMode extends 'single' ? Key |Â null : Key[]`

`'valid' |Â 'invalid'`

`SelectionMode extends 'single' ? Key : Key[]`

`string |Â string[]`

| Name | Type | Description |
| --- | --- | --- |
| `isInvalid` | `boolean` | Whether the input value is invalid. |
| `validationErrors` | `string[]` | The current error messages for the input if it is invalid, otherwise an empty array. |
| `validationDetails` | `ValidityState` | The native validation details for the input. |

`BaseEvent<ReactKeyboardEvent<any>>`

`SyntheticEvent &Â {

stopPropagation: () => void,

continuePropagation: () => void

}`

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `value` | `ValueType<SelectionMode>` | The current select value. |
| `defaultValue` | `ValueType<SelectionMode>` | The default select value. |
| `selectedItems` | `Node<T>[]` | The value of the selected items. |
| `isFocused` | `boolean` | Whether the select is currently focused. |
| `focusStrategy` | `FocusStrategy |Â null` | Controls which item will be auto focused when the menu opens. |
| `collection` | `Collection<Node<T>>` | A collection of items in the list. |
| `disabledKeys` | `Set<Key>` | A set of items that are disabled. |
| `selectionManager` | `SelectionManager` | A selection manager to read and update multiple selection state. |
| `isOpen` | `boolean` | Whether the overlay is currently open. |
| `realtimeValidation` | `ValidationResult` | Realtime validation results, updated as the user edits the value. |
| `displayValidation` | `ValidationResult` | Currently displayed validation results, updated when the user commits their changes. |

### Methods

| Method | Description |
| --- | --- |
| `setValue( (value: Key |Â Key[] |Â null )): void` | Sets the select value. |
| `setFocused( (isFocused: boolean )): void` | Sets whether the select is focused. |
| `open( (focusStrategy?: FocusStrategy |Â  |Â null )): void` | Opens the menu. |
| `toggle( (focusStrategy?: FocusStrategy |Â  |Â null )): void` | Toggles the menu. |
| `setOpen( (isOpen: boolean )): void` | Sets whether the overlay is open. |
| `close(): void` | Closes the overlay. |
| `updateValidation( (result: ValidationResult )): void` | Updates the current validation result. Not displayed to the user until `commitValidation` is called. |
| `resetValidation(): void` | Resets the displayed validation state to valid when the user resets the form. |
| `commitValidation(): void` | Commits the realtime validation so it is displayed to the user. |

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

`'first' |Â 'last'`

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

`'none'
|Â 'single'
|Â 'multiple'`

`'toggle' |Â 'replace'`

`'all' |Â Set<Key>`

`'selection' |Â 'all'`

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
| `labelProps` | `DOMAttributes` | Props for the label element. |
| `triggerProps` | `AriaButtonProps` | Props for the popup trigger element. |
| `valueProps` | `DOMAttributes` | Props for the element representing the selected value. |
| `menuProps` | `AriaListBoxOptions<T>` | Props for the popup. |
| `descriptionProps` | `DOMAttributes` | Props for the select's description element, if any. |
| `errorMessageProps` | `DOMAttributes` | Props for the select's error message element, if any. |
| `hiddenSelectProps` | `HiddenSelectProps<T, SelectionMode>` | Props for the hidden select element. |
| `isInvalid` | `boolean` | Whether the input value is invalid. |
| `validationErrors` | `string[]` | The current error messages for the input if it is invalid, otherwise an empty array. |
| `validationDetails` | `ValidityState` | The native validation details for the input. |

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

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `isDisabled` | `boolean` | â | Whether the button is disabled. |
| `children` | `ReactNode` | â | The content to display in the button. |
| `onPress` | `( (e: PressEvent )) => void` | â | Handler that is called when the press is released over the target. |
| `onPressStart` | `( (e: PressEvent )) => void` | â | Handler that is called when a press interaction starts. |
| `onPressEnd` | `( (e: PressEvent )) => void` | â | Handler that is called when a press interaction ends, either over the target or when the pointer leaves the target. |
| `onPressChange` | `( (isPressed: boolean )) => void` | â | Handler that is called when the press state changes. |
| `onPressUp` | `( (e: PressEvent )) => void` | â | Handler that is called when a press is released over the target, regardless of whether it started on the target or not. |
| `onClick` | `( (e: MouseEvent<FocusableElement> )) => void` | â | **Not recommended â use `onPress` instead.** `onClick` is an alias for `onPress` provided for compatibility with other libraries. `onPress` provides additional event details for non-mouse interactions. |
| `autoFocus` | `boolean` | â | Whether the element should receive focus on render. |
| `onFocus` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | â | Handler that is called when the element's focus status changes. |
| `onKeyDown` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is pressed. |
| `onKeyUp` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is released. |
| `href` | `string` | â | A URL to link to if elementType="a". |
| `target` | `string` | â | The target window for the link. |
| `rel` | `string` | â | The relationship between the linked resource and the current page. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/rel). |
| `elementType` | `ElementType |Â JSXElementConstructor<any>` | `'button'` | The HTML element or React element used to render the button, e.g. 'div', 'a', or `RouterLink`. |
| `aria-disabled` | `boolean |Â 'true' |Â 'false'` | â | Indicates whether the element is disabled to users of assistive technology. |
| `aria-expanded` | `boolean |Â 'true' |Â 'false'` | â | Indicates whether the element, or another grouping element it controls, is currently expanded or collapsed. |
| `aria-haspopup` | `boolean |Â 'menu' |Â 'listbox' |Â 'tree' |Â 'grid' |Â 'dialog' |Â 'true' |Â 'false'` | â | Indicates the availability and type of interactive popup element, such as menu or dialog, that can be triggered by an element. |
| `aria-controls` | `string` | â | Identifies the element (or elements) whose contents or presence are controlled by the current element. |
| `aria-pressed` | `boolean |Â 'true' |Â 'false' |Â 'mixed'` | â | Indicates the current "pressed" state of toggle buttons. |
| `aria-current` | `boolean |Â 'true' |Â 'false' |Â 'page' |Â 'step' |Â 'location' |Â 'date' |Â 'time'` | â | Indicates whether this element represents the current item within a container or set of related elements. |
| `type` | `'button' |Â 'submit' |Â 'reset'` | `'button'` | The behavior of the button when used in an HTML form. |
| `preventFocusOnPress` | `boolean` | â | Whether to prevent focus from moving to the button when pressing it.  Caution, this can make the button inaccessible and should only be used when alternative keyboard interaction is provided, such as ComboBox's MenuTrigger or a NumberField's increment/decrement control. |
| `form` | `string` | â | The `<form>` element to associate the button with. The value of this attribute must be the id of a `<form>` in the same document. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/button#form). |
| `formAction` | `string` | â | The URL that processes the information submitted by the button. Overrides the action attribute of the button's form owner. |
| `formEncType` | `string` | â | Indicates how to encode the form data that is submitted. |
| `formMethod` | `string` | â | Indicates the HTTP method used to submit the form. |
| `formNoValidate` | `boolean` | â | Indicates that the form is not to be validated when it is submitted. |
| `formTarget` | `string` | â | Overrides the target attribute of the button's form owner. |
| `name` | `string` | â | Submitted as a pair with the button's value as part of the form data. |
| `value` | `string` | â | The value associated with the button's name when it's submitted with the form data. |
| `excludeFromTabOrder` | `boolean` | â | Whether to exclude the element from the sequential tab order. If true, the element will not be focusable via the keyboard by tabbing. This should be avoided except in rare scenarios where an alternative means of accessing the element or its functionality via the keyboard is available. |
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `aria-label` | `string` | â | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |

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

| Name | Type | Description |
| --- | --- | --- |
| `state` | `SelectState<T, SelectionMode>` | State for the select. |
| `triggerRef` | `RefObject<FocusableElement |Â null>` | A ref to the trigger element. |
| `autoComplete` | `string` | Describes the type of autocomplete functionality the input should provide if any. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefautocomplete). |
| `label` | `ReactNode` | The text label for the select. |
| `name` | `string` | HTML form input name. |
| `form` | `string` | The `<form>` element to associate the input with. The value of this attribute must be the id of a `<form>` in the same document. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input#form). |
| `isDisabled` | `boolean` | Sets the disabled state of the select and input. |

Provides state management for a select component. Handles building a collection
of items from props, handles the open state for the popup menu, and manages
multiple selection state.

`useSelectState<T extends object, M extends SelectionMode = 'single'>(
(props: SelectStateOptions<T, M>
)): SelectState<T, M>`

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `selectionMode` | `SelectionMode` | `'single'` | Whether single or multiple selection is enabled. |
| `isOpen` | `boolean` | â | Sets the open state of the menu. |
| `defaultOpen` | `boolean` | â | Sets the default open state of the menu. |
| `onOpenChange` | `( (isOpen: boolean )) => void` | â | Method that is called when the open state of the menu changes. |
| `allowsEmptyCollection` | `boolean` | â | Whether the select should be allowed to be open when the collection is empty. |
| `items` | `Iterable<T>` | â | Item objects in the collection. |
| `disabledKeys` | `Iterable<Key>` | â | The item keys that are disabled. These items cannot be selected, focused, or otherwise interacted with. |
| `isDisabled` | `boolean` | â | Whether the input is disabled. |
| `value` | `ValueType<SelectionMode>` | â | The current value (controlled). |
| `defaultValue` | `ValueType<SelectionMode>` | â | The default value (uncontrolled). |
| `onChange` | `( (value: T )) => void` | â | Handler that is called when the value changes. |
| `isRequired` | `boolean` | â | Whether user input is required on the input before form submission. |
| `isInvalid` | `boolean` | â | Whether the input value is invalid. |
| `validationBehavior` | `'aria' |Â 'native'` | `'aria'` | Whether to use native HTML form validation to prevent form submission when the value is missing or invalid, or mark the field as required or invalid via ARIA. |
| `validate` | `( (value: ValidationType<SelectionMode> )) => ValidationError |Â true |Â null |Â undefined` | â | A function that returns an error message if a given value is invalid. Validation errors are displayed to the user when the form is submitted if `validationBehavior="native"`. For realtime validation, use the `isInvalid` prop instead. |
| `description` | `ReactNode` | â | A description for the field. Provides a hint such as specific requirements for what to choose. |
| `errorMessage` | `ReactNode |Â ( (v: ValidationResult )) => ReactNode` | â | An error message for the field. |
| `label` | `ReactNode` | â | The content to display as the label. |
| `placeholder` | `string` | â | Temporary text that occupies the text input when it is empty. |
| `autoFocus` | `boolean` | â | Whether the element should receive focus on render. |
| `onFocus` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | â | Handler that is called when the element's focus status changes. |
| `onKeyDown` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is pressed. |
| `onKeyUp` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is released. |
| `collection` | `Collection<Node<T>>` | â | A pre-constructed collection to use instead of building one from items and children. |

Renders a hidden native `<select>` element, which can be used to support browser
form autofill, mobile form navigation, and native form submission.

| Name | Type | Description |
| --- | --- | --- |
| `state` | `SelectState<T, SelectionMode>` | State for the select. |
| `triggerRef` | `RefObject<FocusableElement |Â null>` | A ref to the trigger element. |
| `autoComplete` | `string` | Describes the type of autocomplete functionality the input should provide if any. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefautocomplete). |
| `label` | `ReactNode` | The text label for the select. |
| `name` | `string` | HTML form input name. |
| `form` | `string` | The `<form>` element to associate the input with. The value of this attribute must be the id of a `<form>` in the same document. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input#form). |
| `isDisabled` | `boolean` | Sets the disabled state of the select and input. |