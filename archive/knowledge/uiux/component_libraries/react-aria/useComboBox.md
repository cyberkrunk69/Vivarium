# useComboBox

Source: https://react-spectrum.adobe.com/react-aria/useComboBox.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../ComboBox).

# useComboBox

Provides the behavior and accessibility implementation for a combo box component.
A combo box combines a text input with a listbox, allowing users to filter a list of options to items matching a query.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useComboBox} from 'react-aria'` |

[View ARIA pattern

W3C](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/ "View ARIA pattern")[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/combobox "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/combobox "View package")

## API[#](#api)

---

`useComboBox<T>(
(props: AriaComboBoxOptions<T>,
, state: ComboBoxState<T>
)): ComboBoxAria<T>`

## Features[#](#features)

---

A combo box can be built using the [<datalist>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/datalist) HTML element, but this is very limited in functionality and difficult to style.
`useComboBox` helps achieve accessible combo box and autocomplete components that can be styled as needed.

- Support for filtering a list of options by typing
- Support for selecting a single option
- Support for disabled options
- Support for groups of items in sections
- Support for custom user input values
- Support for controlled and uncontrolled options, selection, input value, and open state
- Support for custom filter functions
- Async loading and infinite scrolling support
- Support for use with virtualized lists
- Exposed to assistive technology as a `combobox` with ARIA
- Labeling support for accessibility
- Required and invalid states exposed to assistive technology via ARIA
- Support for mouse, touch, and keyboard interactions
- Keyboard support for opening the combo box list box using the arrow keys, including automatically focusing
  the first or last item accordingly
- Support for opening the list box when typing, on focus, or manually
- Handles virtual clicks on the input from touch screen readers to toggle the list box
- Virtual focus management for combo box list box option navigation
- Hides elements outside the input and list box from assistive technology while the list box is open in a portal
- Custom localized announcements for option focusing, filtering, and selection using an ARIA live region to work around VoiceOver bugs
- Support for native HTML constraint validation with customizable UI, custom validation functions, realtime validation, and server-side validation errors

Read our [blog post](../blog/building-a-combobox) for more details about the interactions and accessibility features implemented by `useComboBox`.

## Anatomy[#](#anatomy)

---

A combo box consists of a label, an input which displays the current value, a list box popup, and an optional button
used to toggle the list box popup open state. Users can type within the input to filter the available options
within the list box. The list box popup may be opened by a variety of input field interactions specified
by the `menuTrigger` prop provided to `useComboBox`, or by clicking or touching the button. `useComboBox` handles exposing
the correct ARIA attributes for accessibility for each of the elements comprising the combo box. It should be combined
with [useListBox](../ListBox/useListBox.html), which handles the implementation of the popup list box,
and [useButton](../Button/useButton.html) which handles the button press interactions.

`useComboBox` also supports optional description and error message elements, which can be used
to provide more context about the field, and any validation messages. These are linked with the
input via the `aria-describedby` attribute.

`useComboBox` returns props that you should spread onto the appropriate elements:

| Name | Type | Description |
| --- | --- | --- |
| `labelProps` | `DOMAttributes` | Props for the label element. |
| `inputProps` | `InputHTMLAttributes<HTMLInputElement>` | Props for the combo box input element. |
| `listBoxProps` | `AriaListBoxOptions<T>` | Props for the list box, to be passed to `useListBox`. |
| `buttonProps` | `AriaButtonProps` | Props for the optional trigger button, to be passed to `useButton`. |
| `descriptionProps` | `DOMAttributes` | Props for the combo box description element, if any. |
| `errorMessageProps` | `DOMAttributes` | Props for the combo box error message element, if any. |
| `isInvalid` | `boolean` | Whether the input value is invalid. |
| `validationErrors` | `string[]` | The current error messages for the input if it is invalid, otherwise an empty array. |
| `validationDetails` | `ValidityState` | The native validation details for the input. |

State is managed by the `useComboBoxState` hook from `@react-stately/combobox`.
The state object should be passed as an option to `useComboBox`.

If the combo box does not have a visible label, an `aria-label` or `aria-labelledby` prop must be passed instead to
identify it to assistive technology.

## State management[#](#state-management)

---

`useComboBox` requires knowledge of the options in the combo box in order to handle keyboard
navigation and other interactions. It does this using the `Collection`
interface, which is a generic interface to access sequential unique keyed data. You can
implement this interface yourself, e.g. by using a prop to pass a list of item objects,
but `useComboBoxState` from
`@react-stately/combobox` implements a JSX based interface for building collections instead.
See [Collection Components](https://react-spectrum.adobe.com/v3/collections.html) for more information.

In addition, `useComboBoxState`
manages the state necessary for single selection and exposes
a `SelectionManager`,
which makes use of the collection to provide an interface to update the selection state.
It also holds state to track if the popup is open, if the combo box is focused, and the current input value.
For more information about selection, see [Selection](https://react-spectrum.adobe.com/v3/selection.html).

## Example[#](#example)

---

This example uses an `<input>` element for the combo box text input and a `<button>` element for the list box popup trigger. A `<span>`
is included within the `<button>` to display the dropdown arrow icon (hidden from screen readers with `aria-hidden`).
A "contains" filter function is obtained from `useFilter` and is passed to `useComboBoxState` so
that the list box can be filtered based on the option text and the current input text.

The same `Popover`, `ListBox`, and `Button` components created with [usePopover](../Popover/usePopover.html), [useListBox](../ListBox/useListBox.html),
and [useButton](../Button/useButton.html) that you may already have in your component library or application should be reused. These can be shared with other
components such as a `Select` created with [useSelect](../Select/useSelect.html) or a `Dialog` popover created with [useDialog](../Modal/useDialog.html).
The code for these components is also included below in the collapsed sections.

In addition, see [useListBox](../ListBox/useListBox.html) for examples of sections (option groups), and more complex
options. For an example of the description and error message elements, see [useTextField](../TextField/useTextField.html).

```
import {useButton, useComboBox, useFilter} from 'react-aria';
import {Item, useComboBoxState} from 'react-stately';

// Reuse the ListBox, Popover, and Button from your component library. See below for details.
import {Button, ListBox, Popover} from 'your-component-library';

function ComboBox(props) {
  // Setup filter function and state.
  let { contains } = useFilter({ sensitivity: 'base' });
  let state = useComboBoxState({ ...props, defaultFilter: contains });

  // Setup refs and get props for child elements.
  let buttonRef = React.useRef(null);
  let inputRef = React.useRef(null);
  let listBoxRef = React.useRef(null);
  let popoverRef = React.useRef(null);

  let { buttonProps, inputProps, listBoxProps, labelProps } = useComboBox(
    {
      ...props,
      inputRef,
      buttonRef,
      listBoxRef,
      popoverRef
    },
    state
  );

  return (
    <div style={{ display: 'inline-flex', flexDirection: 'column' }}>
      <label {...labelProps}>{props.label}</label>
      <div>
        <input
          {...inputProps}
          ref={inputRef}
          style={{
            height: 24,
            boxSizing: 'border-box',
            marginRight: 0,
            fontSize: 16
          }}
        />
        <Button
          {...buttonProps}
          buttonRef={buttonRef}
          style={{
            height: 24,
            marginLeft: 0
          }}
        >
          <span
            aria-hidden="true"
            style={{ padding: '0 2px' }}
          >
            â¼
          </span>
        </Button>
        {state.isOpen &&
          (
            <Popover
              state={state}
              triggerRef={inputRef}
              popoverRef={popoverRef}
              isNonModal
              placement="bottom start"
            >
              <ListBox
                {...listBoxProps}
                listBoxRef={listBoxRef}
                state={state}
              />
            </Popover>
          )}
      </div>
    </div>
  );
}

<ComboBox label="Favorite Animal">
  <Item key="red panda">Red Panda</Item>
  <Item key="cat">Cat</Item>
  <Item key="dog">Dog</Item>
  <Item key="aardvark">Aardvark</Item>
  <Item key="kangaroo">Kangaroo</Item>
  <Item key="snake">Snake</Item>
</ComboBox>
```

```
import {
  useButton,
  useComboBox,
  useFilter
} from 'react-aria';
import {Item, useComboBoxState} from 'react-stately';

// Reuse the ListBox, Popover, and Button from your component library. See below for details.
import {
  Button,
  ListBox,
  Popover
} from 'your-component-library';

function ComboBox(props) {
  // Setup filter function and state.
  let { contains } = useFilter({ sensitivity: 'base' });
  let state = useComboBoxState({
    ...props,
    defaultFilter: contains
  });

  // Setup refs and get props for child elements.
  let buttonRef = React.useRef(null);
  let inputRef = React.useRef(null);
  let listBoxRef = React.useRef(null);
  let popoverRef = React.useRef(null);

  let {
    buttonProps,
    inputProps,
    listBoxProps,
    labelProps
  } = useComboBox(
    {
      ...props,
      inputRef,
      buttonRef,
      listBoxRef,
      popoverRef
    },
    state
  );

  return (
    <div
      style={{
        display: 'inline-flex',
        flexDirection: 'column'
      }}
    >
      <label {...labelProps}>{props.label}</label>
      <div>
        <input
          {...inputProps}
          ref={inputRef}
          style={{
            height: 24,
            boxSizing: 'border-box',
            marginRight: 0,
            fontSize: 16
          }}
        />
        <Button
          {...buttonProps}
          buttonRef={buttonRef}
          style={{
            height: 24,
            marginLeft: 0
          }}
        >
          <span
            aria-hidden="true"
            style={{ padding: '0 2px' }}
          >
            â¼
          </span>
        </Button>
        {state.isOpen &&
          (
            <Popover
              state={state}
              triggerRef={inputRef}
              popoverRef={popoverRef}
              isNonModal
              placement="bottom start"
            >
              <ListBox
                {...listBoxProps}
                listBoxRef={listBoxRef}
                state={state}
              />
            </Popover>
          )}
      </div>
    </div>
  );
}

<ComboBox label="Favorite Animal">
  <Item key="red panda">Red Panda</Item>
  <Item key="cat">Cat</Item>
  <Item key="dog">Dog</Item>
  <Item key="aardvark">Aardvark</Item>
  <Item key="kangaroo">Kangaroo</Item>
  <Item key="snake">Snake</Item>
</ComboBox>
```

```
import {
  useButton,
  useComboBox,
  useFilter
} from 'react-aria';
import {
  Item,
  useComboBoxState
} from 'react-stately';

// Reuse the ListBox, Popover, and Button from your component library. See below for details.
import {
  Button,
  ListBox,
  Popover
} from 'your-component-library';

function ComboBox(
  props
) {
  // Setup filter function and state.
  let { contains } =
    useFilter({
      sensitivity: 'base'
    });
  let state =
    useComboBoxState({
      ...props,
      defaultFilter:
        contains
    });

  // Setup refs and get props for child elements.
  let buttonRef = React
    .useRef(null);
  let inputRef = React
    .useRef(null);
  let listBoxRef = React
    .useRef(null);
  let popoverRef = React
    .useRef(null);

  let {
    buttonProps,
    inputProps,
    listBoxProps,
    labelProps
  } = useComboBox(
    {
      ...props,
      inputRef,
      buttonRef,
      listBoxRef,
      popoverRef
    },
    state
  );

  return (
    <div
      style={{
        display:
          'inline-flex',
        flexDirection:
          'column'
      }}
    >
      <label
        {...labelProps}
      >
        {props.label}
      </label>
      <div>
        <input
          {...inputProps}
          ref={inputRef}
          style={{
            height: 24,
            boxSizing:
              'border-box',
            marginRight:
              0,
            fontSize: 16
          }}
        />
        <Button
          {...buttonProps}
          buttonRef={buttonRef}
          style={{
            height: 24,
            marginLeft: 0
          }}
        >
          <span
            aria-hidden="true"
            style={{
              padding:
                '0 2px'
            }}
          >
            â¼
          </span>
        </Button>
        {state.isOpen &&
          (
            <Popover
              state={state}
              triggerRef={inputRef}
              popoverRef={popoverRef}
              isNonModal
              placement="bottom start"
            >
              <ListBox
                {...listBoxProps}
                listBoxRef={listBoxRef}
                state={state}
              />
            </Popover>
          )}
      </div>
    </div>
  );
}

<ComboBox label="Favorite Animal">
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
</ComboBox>
```

### Popover[#](#popover)

The `Popover` component is used to contain the popup listbox for the ComboBox.
It can be shared between many other components, including [Select](../Select/useSelect.html),
[Menu](../Menu/useMenu.html), and others.
See [usePopover](../Popover/usePopover.html) for more examples of popovers.

 Show code

```
import {DismissButton, Overlay, usePopover} from 'react-aria';
import type {AriaPopoverProps} from 'react-aria';
import type {OverlayTriggerState} from 'react-stately';

interface PopoverProps extends AriaPopoverProps {
  children: React.ReactNode;
  state: OverlayTriggerState;
}

function Popover({ children, state, ...props }: PopoverProps) {
  let { popoverProps } = usePopover(props, state);

  return (
    <Overlay>
      <div
        {...popoverProps}
        ref={props.popoverRef as React.RefObject<HTMLDivElement>}
        style={{
          ...popoverProps.style,
          background: 'lightgray',
          border: '1px solid gray'
        }}
      >
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

interface PopoverProps extends AriaPopoverProps {
  children: React.ReactNode;
  state: OverlayTriggerState;
}

function Popover(
  { children, state, ...props }: PopoverProps
) {
  let { popoverProps } = usePopover(props, state);

  return (
    <Overlay>
      <div
        {...popoverProps}
        ref={props.popoverRef as React.RefObject<
          HTMLDivElement
        >}
        style={{
          ...popoverProps.style,
          background: 'lightgray',
          border: '1px solid gray'
        }}
      >
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
    AriaPopoverProps {
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
  let { popoverProps } =
    usePopover(
      props,
      state
    );

  return (
    <Overlay>
      <div
        {...popoverProps}
        ref={props
          .popoverRef as React.RefObject<
            HTMLDivElement
          >}
        style={{
          ...popoverProps
            .style,
          background:
            'lightgray',
          border:
            '1px solid gray'
        }}
      >
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

The `ListBox` and `Option` components are used to show the filtered list of options as the
user types in the ComboBox. They can also be shared with other components like a [Select](../Select/useSelect.html). See
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
        minWidth: 200
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

  let backgroundColor;
  let color = 'black';

  if (isSelected) {
    backgroundColor = 'blueviolet';
    color = 'white';
  } else if (isFocused) {
    backgroundColor = 'gray';
  } else if (isDisabled) {
    backgroundColor = 'transparent';
    color = 'gray';
  }

  return (
    <li
      {...optionProps}
      ref={ref}
      style={{
        background: backgroundColor,
        color: color,
        padding: '2px 5px',
        outline: 'none',
        cursor: 'pointer'
      }}
    >
      {item.rendered}
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
        minWidth: 200
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

  let backgroundColor;
  let color = 'black';

  if (isSelected) {
    backgroundColor = 'blueviolet';
    color = 'white';
  } else if (isFocused) {
    backgroundColor = 'gray';
  } else if (isDisabled) {
    backgroundColor = 'transparent';
    color = 'gray';
  }

  return (
    <li
      {...optionProps}
      ref={ref}
      style={{
        background: backgroundColor,
        color: color,
        padding: '2px 5px',
        outline: 'none',
        cursor: 'pointer'
      }}
    >
      {item.rendered}
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
        minWidth: 200
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

  let backgroundColor;
  let color = 'black';

  if (isSelected) {
    backgroundColor =
      'blueviolet';
    color = 'white';
  } else if (isFocused) {
    backgroundColor =
      'gray';
  } else if (
    isDisabled
  ) {
    backgroundColor =
      'transparent';
    color = 'gray';
  }

  return (
    <li
      {...optionProps}
      ref={ref}
      style={{
        background:
          backgroundColor,
        color: color,
        padding:
          '2px 5px',
        outline: 'none',
        cursor: 'pointer'
      }}
    >
      {item.rendered}
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

[![](/example.efd4cd78.png)

Tailwind CSS

An example of styling a ComboBox with Tailwind.](https://codesandbox.io/s/hardcore-moon-xzc4r?file=/src/ComboBox.tsx)
[![](/search.70c2985b.png)

Search autocomplete

A search autocomplete with multiple sections, styled with Tailwind.](https://codesandbox.io/s/hardcore-moon-xzc4r?file=/src/SearchAutocomplete.tsx)
[![](/styled-components.3c9aeeb2.png)

Styled Components

A ComboBox with complex item content built with Styled Components.](https://codesandbox.io/s/sharp-sun-e3fgd?file=/src/ComboBox.tsx)
[![](/material.6182513f.png)

Material UI

An example ComboBox built with Material UI and React Aria.](https://codesandbox.io/s/falling-http-u37en?file=/src/ComboBox.js)
[![](/chakra.991b27a7.png)

Chakra UI

An async loading and infinite scrolling autocomplete built with Chakra UI.](https://codesandbox.io/s/dreamy-burnell-3i2jy?file=/src/App.tsx)

## Usage[#](#usage)

---

The following examples show how to use the ComboBox component created in the above example.

### Uncontrolled[#](#uncontrolled)

The following example shows how you would create an uncontrolled ComboBox. The input value, selected option, and open state is completely
uncontrolled, with the default input text set by the `defaultInputValue` prop.

```
<ComboBox label="Favorite Animal" defaultInputValue="red">
  <Item key="red panda">Red Panda</Item>
  <Item key="cat">Cat</Item>
  <Item key="dog">Dog</Item>
  <Item key="aardvark">Aardvark</Item>
  <Item key="kangaroo">Kangaroo</Item>
  <Item key="snake">Snake</Item>
</ComboBox>
```

```
<ComboBox label="Favorite Animal" defaultInputValue="red">
  <Item key="red panda">Red Panda</Item>
  <Item key="cat">Cat</Item>
  <Item key="dog">Dog</Item>
  <Item key="aardvark">Aardvark</Item>
  <Item key="kangaroo">Kangaroo</Item>
  <Item key="snake">Snake</Item>
</ComboBox>
```

```
<ComboBox
  label="Favorite Animal"
  defaultInputValue="red"
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
</ComboBox>
```

### Dynamic collections[#](#dynamic-collections)

ComboBox follows the [Collection Components API](https://react-spectrum.adobe.com/v3/collections.html), accepting both static and dynamic collections.
The examples above show static collections, which can be used when the full list of options is known ahead of time. Dynamic collections,
as shown below, can be used when the options come from an external data source such as an API call, or update over time.

As seen below, an iterable list of options is passed to the ComboBox using the `defaultItems` prop. Each item accepts a `key` prop, which
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
  let [majorId, setMajorId] = React.useState(null);

  return (
    <>
      <ComboBox
        label="Pick a engineering major"
        defaultItems={options}
        onSelectionChange={setMajorId}>
        {(item) => <Item>{item.name}</Item>}
      </ComboBox>
      <p>Selected topic id: {majorId}</p>
    </>
  );
}
```

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
  let [majorId, setMajorId] = React.useState(null);

  return (
    <>
      <ComboBox
        label="Pick a engineering major"
        defaultItems={options}
        onSelectionChange={setMajorId}>
        {(item) => <Item>{item.name}</Item>}
      </ComboBox>
      <p>Selected topic id: {majorId}</p>
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
  let [
    majorId,
    setMajorId
  ] = React.useState(
    null
  );

  return (
    <>
      <ComboBox
        label="Pick a engineering major"
        defaultItems={options}
        onSelectionChange={setMajorId}
      >
        {(item) => (
          <Item>
            {item.name}
          </Item>
        )}
      </ComboBox>
      <p>
        Selected topic
        id: {majorId}
      </p>
    </>
  );
}
```

### Allow custom values[#](#allow-custom-values)

By default, `useComboBoxState` doesn't allow users to specify a value that doesn't exist in the list of options and will revert the input value to
the current selected value on blur. By specifying `allowsCustomValue`, this behavior is suppressed and the user is free to enter
any value within the field.

```
<ComboBox label="Favorite Animal" allowsCustomValue>
  <Item key="red panda">Red Panda</Item>
  <Item key="cat">Cat</Item>
  <Item key="dog">Dog</Item>
  <Item key="aardvark">Aardvark</Item>
  <Item key="kangaroo">Kangaroo</Item>
  <Item key="snake">Snake</Item>
</ComboBox>
```

```
<ComboBox label="Favorite Animal" allowsCustomValue>
  <Item key="red panda">Red Panda</Item>
  <Item key="cat">Cat</Item>
  <Item key="dog">Dog</Item>
  <Item key="aardvark">Aardvark</Item>
  <Item key="kangaroo">Kangaroo</Item>
  <Item key="snake">Snake</Item>
</ComboBox>
```

```
<ComboBox
  label="Favorite Animal"
  allowsCustomValue
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
</ComboBox>
```

### Custom filtering[#](#custom-filtering)

By default, `useComboBoxState` uses the filter function passed to the `defaultFilter` prop (in the above example, a
"contains" function from `useFilter`). The filter function can be overridden by users of the `ComboBox` component by
using the `items` prop to control the filtered list. When `items` is provided rather than `defaultItems`, `useComboBoxState`
does no filtering of its own.

The following example makes the `inputValue` controlled, and updates the filtered list that is passed to the `items`
prop when the input changes value.

```
function Example() {
  let options = [
    {id: 1, email: 'fake@email.com'},
    {id: 2, email: 'anotherfake@email.com'},
    {id: 3, email: 'bob@email.com'},
    {id: 4, email: 'joe@email.com'},
    {id: 5, email: 'yourEmail@email.com'},
    {id: 6, email: 'valid@email.com'},
    {id: 7, email: 'spam@email.com'},
    {id: 8, email: 'newsletter@email.com'},
    {id: 9, email: 'subscribe@email.com'}
  ];

  let {startsWith} = useFilter({sensitivity: 'base'});
  let [filterValue, setFilterValue] = React.useState('');
  let filteredItems = React.useMemo(
    () => options.filter((item) => startsWith(item.email, filterValue)),
    [options, filterValue]
  );

  return (
    <ComboBox
      label="To:"
      items={filteredItems}
      inputValue={filterValue}
      onInputChange={setFilterValue}
      allowsCustomValue>
      {(item) => <Item>{item.email}</Item>}
    </ComboBox>
  );
}
```

```
function Example() {
  let options = [
    { id: 1, email: 'fake@email.com' },
    { id: 2, email: 'anotherfake@email.com' },
    { id: 3, email: 'bob@email.com' },
    { id: 4, email: 'joe@email.com' },
    { id: 5, email: 'yourEmail@email.com' },
    { id: 6, email: 'valid@email.com' },
    { id: 7, email: 'spam@email.com' },
    { id: 8, email: 'newsletter@email.com' },
    { id: 9, email: 'subscribe@email.com' }
  ];

  let { startsWith } = useFilter({ sensitivity: 'base' });
  let [filterValue, setFilterValue] = React.useState('');
  let filteredItems = React.useMemo(
    () =>
      options.filter((item) =>
        startsWith(item.email, filterValue)
      ),
    [options, filterValue]
  );

  return (
    <ComboBox
      label="To:"
      items={filteredItems}
      inputValue={filterValue}
      onInputChange={setFilterValue}
      allowsCustomValue
    >
      {(item) => <Item>{item.email}</Item>}
    </ComboBox>
  );
}
```

```
function Example() {
  let options = [
    {
      id: 1,
      email:
        'fake@email.com'
    },
    {
      id: 2,
      email:
        'anotherfake@email.com'
    },
    {
      id: 3,
      email:
        'bob@email.com'
    },
    {
      id: 4,
      email:
        'joe@email.com'
    },
    {
      id: 5,
      email:
        'yourEmail@email.com'
    },
    {
      id: 6,
      email:
        'valid@email.com'
    },
    {
      id: 7,
      email:
        'spam@email.com'
    },
    {
      id: 8,
      email:
        'newsletter@email.com'
    },
    {
      id: 9,
      email:
        'subscribe@email.com'
    }
  ];

  let { startsWith } =
    useFilter({
      sensitivity: 'base'
    });
  let [
    filterValue,
    setFilterValue
  ] = React.useState('');
  let filteredItems =
    React.useMemo(
      () =>
        options.filter((
          item
        ) =>
          startsWith(
            item.email,
            filterValue
          )
        ),
      [
        options,
        filterValue
      ]
    );

  return (
    <ComboBox
      label="To:"
      items={filteredItems}
      inputValue={filterValue}
      onInputChange={setFilterValue}
      allowsCustomValue
    >
      {(item) => (
        <Item>
          {item.email}
        </Item>
      )}
    </ComboBox>
  );
}
```

### Fully controlled[#](#fully-controlled)

The following example shows how you would create a controlled ComboBox, controlling everything from the selected value (`selectedKey`)
to the combobox options (`items`). By passing in `inputValue`, `selectedKey`, and `items` to the `ComboBox` you can control
exactly what your ComboBox should display. For example, note that the item filtering for the controlled ComboBox below now follows a "starts with"
filter strategy, accomplished by controlling the exact set of items available to the ComboBox whenever the input value updates.

It is important to note that you don't have to control every single aspect of a ComboBox. If you decide to only control a single property of the
ComboBox, be sure to provide the change handler for that prop as well e.g. controlling `selectedKey` would require `onSelectionChange` to be passed to `useComboBox` as well.

```
function ControlledComboBox() {
  let optionList = [
    { name: 'Red Panda', id: '1' },
    { name: 'Cat', id: '2' },
    { name: 'Dog', id: '3' },
    { name: 'Aardvark', id: '4' },
    { name: 'Kangaroo', id: '5' },
    { name: 'Snake', id: '6' }
  ];

  // Store ComboBox input value, selected option, open state, and items
  // in a state tracker
  let [fieldState, setFieldState] = React.useState({
    selectedKey: '',
    inputValue: '',
    items: optionList
  });

  // Implement custom filtering logic and control what items are
  // available to the ComboBox.
  let { startsWith } = useFilter({ sensitivity: 'base' });

  // Specify how each of the ComboBox values should change when an
  // option is selected from the list box
  let onSelectionChange = (key) => {
    setFieldState((prevState) => {
      let selectedItem = prevState.items.find((option) => option.id === key);
      return ({
        inputValue: selectedItem?.name ?? '',
        selectedKey: key,
        items: optionList.filter((item) =>
          startsWith(item.name, selectedItem?.name ?? '')
        )
      });
    });
  };

  // Specify how each of the ComboBox values should change when the input
  // field is altered by the user
  let onInputChange = (value) => {
    setFieldState((prevState) => ({
      inputValue: value,
      selectedKey: value === '' ? null : prevState.selectedKey,
      items: optionList.filter((item) => startsWith(item.name, value))
    }));
  };

  // Show entire list if user opens the menu manually
  let onOpenChange = (isOpen, menuTrigger) => {
    if (menuTrigger === 'manual' && isOpen) {
      setFieldState((prevState) => ({
        inputValue: prevState.inputValue,
        selectedKey: prevState.selectedKey,
        items: optionList
      }));
    }
  };

  // Pass each controlled prop to useComboBox along with their
  // change handlers
  return (
    <ComboBox
      label="Favorite Animal"
      items={fieldState.items}
      selectedKey={fieldState.selectedKey}
      inputValue={fieldState.inputValue}
      onOpenChange={onOpenChange}
      onSelectionChange={onSelectionChange}
      onInputChange={onInputChange}
    >
      {(item) => <Item>{item.name}</Item>}
    </ComboBox>
  );
}

<ControlledComboBox />
```

```
function ControlledComboBox() {
  let optionList = [
    { name: 'Red Panda', id: '1' },
    { name: 'Cat', id: '2' },
    { name: 'Dog', id: '3' },
    { name: 'Aardvark', id: '4' },
    { name: 'Kangaroo', id: '5' },
    { name: 'Snake', id: '6' }
  ];

  // Store ComboBox input value, selected option, open state, and items
  // in a state tracker
  let [fieldState, setFieldState] = React.useState({
    selectedKey: '',
    inputValue: '',
    items: optionList
  });

  // Implement custom filtering logic and control what items are
  // available to the ComboBox.
  let { startsWith } = useFilter({ sensitivity: 'base' });

  // Specify how each of the ComboBox values should change when an
  // option is selected from the list box
  let onSelectionChange = (key) => {
    setFieldState((prevState) => {
      let selectedItem = prevState.items.find((option) =>
        option.id === key
      );
      return ({
        inputValue: selectedItem?.name ?? '',
        selectedKey: key,
        items: optionList.filter((item) =>
          startsWith(item.name, selectedItem?.name ?? '')
        )
      });
    });
  };

  // Specify how each of the ComboBox values should change when the input
  // field is altered by the user
  let onInputChange = (value) => {
    setFieldState((prevState) => ({
      inputValue: value,
      selectedKey: value === ''
        ? null
        : prevState.selectedKey,
      items: optionList.filter((item) =>
        startsWith(item.name, value)
      )
    }));
  };

  // Show entire list if user opens the menu manually
  let onOpenChange = (isOpen, menuTrigger) => {
    if (menuTrigger === 'manual' && isOpen) {
      setFieldState((prevState) => ({
        inputValue: prevState.inputValue,
        selectedKey: prevState.selectedKey,
        items: optionList
      }));
    }
  };

  // Pass each controlled prop to useComboBox along with their
  // change handlers
  return (
    <ComboBox
      label="Favorite Animal"
      items={fieldState.items}
      selectedKey={fieldState.selectedKey}
      inputValue={fieldState.inputValue}
      onOpenChange={onOpenChange}
      onSelectionChange={onSelectionChange}
      onInputChange={onInputChange}
    >
      {(item) => <Item>{item.name}</Item>}
    </ComboBox>
  );
}

<ControlledComboBox />
```

```
function ControlledComboBox() {
  let optionList = [
    {
      name: 'Red Panda',
      id: '1'
    },
    {
      name: 'Cat',
      id: '2'
    },
    {
      name: 'Dog',
      id: '3'
    },
    {
      name: 'Aardvark',
      id: '4'
    },
    {
      name: 'Kangaroo',
      id: '5'
    },
    {
      name: 'Snake',
      id: '6'
    }
  ];

  // Store ComboBox input value, selected option, open state, and items
  // in a state tracker
  let [
    fieldState,
    setFieldState
  ] = React.useState({
    selectedKey: '',
    inputValue: '',
    items: optionList
  });

  // Implement custom filtering logic and control what items are
  // available to the ComboBox.
  let { startsWith } =
    useFilter({
      sensitivity: 'base'
    });

  // Specify how each of the ComboBox values should change when an
  // option is selected from the list box
  let onSelectionChange =
    (key) => {
      setFieldState(
        (prevState) => {
          let selectedItem =
            prevState
              .items
              .find(
                (option) =>
                  option
                    .id ===
                    key
              );
          return ({
            inputValue:
              selectedItem
                ?.name ??
                '',
            selectedKey:
              key,
            items:
              optionList
                .filter(
                  (item) =>
                    startsWith(
                      item
                        .name,
                      selectedItem
                        ?.name ??
                        ''
                    )
                )
          });
        }
      );
    };

  // Specify how each of the ComboBox values should change when the input
  // field is altered by the user
  let onInputChange = (
    value
  ) => {
    setFieldState(
      (prevState) => ({
        inputValue:
          value,
        selectedKey:
          value === ''
            ? null
            : prevState
              .selectedKey,
        items: optionList
          .filter(
            (item) =>
              startsWith(
                item
                  .name,
                value
              )
          )
      })
    );
  };

  // Show entire list if user opens the menu manually
  let onOpenChange = (
    isOpen,
    menuTrigger
  ) => {
    if (
      menuTrigger ===
        'manual' &&
      isOpen
    ) {
      setFieldState(
        (prevState) => ({
          inputValue:
            prevState
              .inputValue,
          selectedKey:
            prevState
              .selectedKey,
          items:
            optionList
        })
      );
    }
  };

  // Pass each controlled prop to useComboBox along with their
  // change handlers
  return (
    <ComboBox
      label="Favorite Animal"
      items={fieldState
        .items}
      selectedKey={fieldState
        .selectedKey}
      inputValue={fieldState
        .inputValue}
      onOpenChange={onOpenChange}
      onSelectionChange={onSelectionChange}
      onInputChange={onInputChange}
    >
      {(item) => (
        <Item>
          {item.name}
        </Item>
      )}
    </ComboBox>
  );
}

<ControlledComboBox />
```

### Menu trigger behavior[#](#menu-trigger-behavior)

`useComboBoxState` supports three different `menuTrigger` prop values:

- `input` (default): ComboBox menu opens when the user edits the input text.
- `focus`: ComboBox menu opens when the user focuses the ComboBox input.
- `manual`: ComboBox menu only opens when the user presses the trigger button or uses the arrow keys.

The example below has `menuTrigger` set to `focus`.

```
<ComboBox label="Favorite Animal" menuTrigger="focus">
  <Item key="red panda">Red Panda</Item>
  <Item key="cat">Cat</Item>
  <Item key="dog">Dog</Item>
  <Item key="aardvark">Aardvark</Item>
  <Item key="kangaroo">Kangaroo</Item>
  <Item key="snake">Snake</Item>
</ComboBox>
```

```
<ComboBox label="Favorite Animal" menuTrigger="focus">
  <Item key="red panda">Red Panda</Item>
  <Item key="cat">Cat</Item>
  <Item key="dog">Dog</Item>
  <Item key="aardvark">Aardvark</Item>
  <Item key="kangaroo">Kangaroo</Item>
  <Item key="snake">Snake</Item>
</ComboBox>
```

```
<ComboBox
  label="Favorite Animal"
  menuTrigger="focus"
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
</ComboBox>
```

### Disabled options[#](#disabled-options)

You can disable specific options by providing an array of keys to `useComboBoxState`
via the `disabledKeys` prop. This will prevent options with matching keys from being pressable and
receiving keyboard focus as shown in the example below. Note that you are responsible for the styling of disabled options.

```
<ComboBox label="Favorite Animal" disabledKeys={['cat', 'kangaroo']}>
  <Item key="red panda">Red Panda</Item>
  <Item key="cat">Cat</Item>
  <Item key="dog">Dog</Item>
  <Item key="aardvark">Aardvark</Item>
  <Item key="kangaroo">Kangaroo</Item>
  <Item key="snake">Snake</Item>
</ComboBox>
```

```
<ComboBox
  label="Favorite Animal"
  disabledKeys={['cat', 'kangaroo']}
>
  <Item key="red panda">Red Panda</Item>
  <Item key="cat">Cat</Item>
  <Item key="dog">Dog</Item>
  <Item key="aardvark">Aardvark</Item>
  <Item key="kangaroo">Kangaroo</Item>
  <Item key="snake">Snake</Item>
</ComboBox>
```

```
<ComboBox
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
</ComboBox>
```

### Asynchronous loading[#](#asynchronous-loading)

This example uses the [useAsyncList](../useAsyncList.html) hook to handle asynchronous loading
and filtering of data from a server. You may additionally want to display a spinner to indicate the loading
state to the user, or support features like infinite scroll to load more data. See
[this CodeSandbox](https://codesandbox.io/s/dreamy-burnell-3i2jy?file=/src/Autocomplete.tsx) for an example
of a ComboBox supporting those features.

```
import {useAsyncList} from 'react-stately';

function AsyncLoadingExample() {
  let list = useAsyncList({
    async load({ signal, filterText }) {
      let res = await fetch(
        `https://swapi.py4e.com/api/people/?search=${filterText}`,
        { signal }
      );
      let json = await res.json();

      return {
        items: json.results
      };
    }
  });

  return (
    <ComboBox
      label="Star Wars Character Lookup"
      items={list.items}
      inputValue={list.filterText}
      onInputChange={list.setFilterText}
    >
      {(item) => <Item key={item.name}>{item.name}</Item>}
    </ComboBox>
  );
}
```

```
import {useAsyncList} from 'react-stately';

function AsyncLoadingExample() {
  let list = useAsyncList({
    async load({ signal, filterText }) {
      let res = await fetch(
        `https://swapi.py4e.com/api/people/?search=${filterText}`,
        { signal }
      );
      let json = await res.json();

      return {
        items: json.results
      };
    }
  });

  return (
    <ComboBox
      label="Star Wars Character Lookup"
      items={list.items}
      inputValue={list.filterText}
      onInputChange={list.setFilterText}
    >
      {(item) => <Item key={item.name}>{item.name}</Item>}
    </ComboBox>
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
            `https://swapi.py4e.com/api/people/?search=${filterText}`,
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
    <ComboBox
      label="Star Wars Character Lookup"
      items={list.items}
      inputValue={list
        .filterText}
      onInputChange={list
        .setFilterText}
    >
      {(item) => (
        <Item
          key={item.name}
        >
          {item.name}
        </Item>
      )}
    </ComboBox>
  );
}
```

### Links[#](#links)

By default, interacting with an item in a ComboBox selects it and updates the input value. Alternatively, items may be links to another page or website. This can be achieved by passing the `href` prop to the `<Item>` component. Interacting with link items navigates to the provided URL and does not update the selection or input value. See the [links](../ListBox/useListBox.html#links) section in the `useListBox` docs for details on how to support this.

## Internationalization[#](#internationalization)

---

`useComboBox` handles some aspects of internationalization automatically.
For example, the item focus, count, and selection VoiceOver announcements are localized.
You are responsible for localizing all labels and option
content that is passed into the combo box.

### RTL[#](#rtl)

In right-to-left languages, the ComboBox should be mirrored. The trigger button should be on the left,
and the input element should be on the right. In addition, the content of ComboBox options should
flip. Ensure that your CSS accounts for this.

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `inputRef` | `RefObject<HTMLInputElement |Â null>` | â | The ref for the input element. |
| `popoverRef` | `RefObject<Element |Â null>` | â | The ref for the list box popover. |
| `listBoxRef` | `RefObject<HTMLElement |Â null>` | â | The ref for the list box. |
| `buttonRef` | `RefObject<Element |Â null>` | â | The ref for the optional list box popup trigger button. |
| `keyboardDelegate` | `KeyboardDelegate` | â | An optional keyboard delegate implementation, to override the default. |
| `layoutDelegate` | `LayoutDelegate` | â | A delegate object that provides layout information for items in the collection. By default this uses the DOM, but this can be overridden to implement things like virtualized scrolling. |
| `shouldFocusWrap` | `boolean` | â | Whether keyboard navigation is circular. |
| `defaultItems` | `Iterable<T>` | â | The list of ComboBox items (uncontrolled). |
| `items` | `Iterable<T>` | â | The list of ComboBox items (controlled). |
| `onOpenChange` | `( (isOpen: boolean, , menuTrigger?: MenuTriggerAction )) => void` | â | Method that is called when the open state of the menu changes. Returns the new open state and the action that caused the opening of the menu. |
| `onSelectionChange` | `( (key: Key |Â  |Â null )) => void` | â | Handler that is called when the selection changes. |
| `inputValue` | `string` | â | The value of the ComboBox input (controlled). |
| `defaultInputValue` | `string` | â | The default value of the ComboBox input (uncontrolled). |
| `onInputChange` | `( (value: string )) => void` | â | Handler that is called when the ComboBox input value changes. |
| `allowsCustomValue` | `boolean` | â | Whether the ComboBox allows a non-item matching input value to be set. |
| `menuTrigger` | `MenuTriggerAction` | `'input'` | The interaction required to display the ComboBox menu. |
| `disabledKeys` | `Iterable<Key>` | â | The item keys that are disabled. These items cannot be selected, focused, or otherwise interacted with. |
| `selectedKey` | `Key |Â null` | â | The currently selected key in the collection (controlled). |
| `defaultSelectedKey` | `Key` | â | The initial selected key in the collection (uncontrolled). |
| `isDisabled` | `boolean` | â | Whether the input is disabled. |
| `isReadOnly` | `boolean` | â | Whether the input can be selected but not changed by the user. |
| `placeholder` | `string` | â | Temporary text that occupies the text input when it is empty. |
| `isRequired` | `boolean` | â | Whether user input is required on the input before form submission. |
| `isInvalid` | `boolean` | â | Whether the input value is invalid. |
| `validationBehavior` | `'aria' |Â 'native'` | `'aria'` | Whether to use native HTML form validation to prevent form submission when the value is missing or invalid, or mark the field as required or invalid via ARIA. |
| `validate` | `( (value: ComboBoxValidationValue )) => ValidationError |Â true |Â null |Â undefined` | â | A function that returns an error message if a given value is invalid. Validation errors are displayed to the user when the form is submitted if `validationBehavior="native"`. For realtime validation, use the `isInvalid` prop instead. |
| `autoFocus` | `boolean` | â | Whether the element should receive focus on render. |
| `onFocus` | `( (e: FocusEvent<HTMLInputElement> )) => void` | â | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<HTMLInputElement> )) => void` | â | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | â | Handler that is called when the element's focus status changes. |
| `onKeyDown` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is pressed. |
| `onKeyUp` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is released. |
| `label` | `ReactNode` | â | The content to display as the label. |
| `description` | `ReactNode` | â | A description for the field. Provides a hint such as specific requirements for what to choose. |
| `errorMessage` | `ReactNode |Â ( (v: ValidationResult )) => ReactNode` | â | An error message for the field. |
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `name` | `string` | â | The name of the input element, used when submitting an HTML form. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefname). |
| `form` | `string` | â | The `<form>` element to associate the input with. The value of this attribute must be the id of a `<form>` in the same document. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input#form). |
| `aria-label` | `string` | â | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |

| Name | Type | Description |
| --- | --- | --- |
| `current` | `T` |  |

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

`'focus'
|Â 'input'
|Â 'manual'`

`string |Â number`

`'valid' |Â 'invalid'`

| Name | Type | Description |
| --- | --- | --- |
| `selectedKey` | `Key |Â null` | The selected key in the ComboBox. |
| `inputValue` | `string` | The value of the ComboBox input. |

`string |Â string[]`

`BaseEvent<ReactKeyboardEvent<any>>`

`SyntheticEvent &Â {

stopPropagation: () => void,

continuePropagation: () => void

}`

| Name | Type | Description |
| --- | --- | --- |
| `isInvalid` | `boolean` | Whether the input value is invalid. |
| `validationErrors` | `string[]` | The current error messages for the input if it is invalid, otherwise an empty array. |
| `validationDetails` | `ValidityState` | The native validation details for the input. |

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `defaultSelectedKey` | `Key |Â null` | The default selected key. |
| `inputValue` | `string` | The current value of the combo box input. |
| `defaultInputValue` | `string` | The default value of the combo box input. |
| `focusStrategy` | `FocusStrategy |Â null` | Controls which item will be auto focused when the menu opens. |
| `isFocused` | `boolean` | Whether the select is currently focused. |
| `selectedKey` | `Key |Â null` | The key for the currently selected item. |
| `selectedItem` | `Node<T> |Â null` | The value of the currently selected item. |
| `collection` | `Collection<Node<T>>` | A collection of items in the list. |
| `disabledKeys` | `Set<Key>` | A set of items that are disabled. |
| `selectionManager` | `SelectionManager` | A selection manager to read and update multiple selection state. |
| `isOpen` | `boolean` | Whether the overlay is currently open. |
| `realtimeValidation` | `ValidationResult` | Realtime validation results, updated as the user edits the value. |
| `displayValidation` | `ValidationResult` | Currently displayed validation results, updated when the user commits their changes. |

### Methods

| Method | Description |
| --- | --- |
| `setInputValue( (value: string )): void` | Sets the value of the combo box input. |
| `commit(): void` | Selects the currently focused item and updates the input value. |
| `setFocused( (isFocused: boolean )): void` | Sets whether the select is focused. |
| `open( (focusStrategy?: FocusStrategy |Â  |Â null, , trigger?: MenuTriggerAction )): void` | Opens the menu. |
| `toggle( (focusStrategy?: FocusStrategy |Â  |Â null, , trigger?: MenuTriggerAction )): void` | Toggles the menu. |
| `revert(): void` | Resets the input value to the previously selected item's text if any and closes the menu. |
| `setSelectedKey( (key: Key |Â  |Â null )): void` | Sets the selected key. |
| `setOpen( (isOpen: boolean )): void` | Sets whether the overlay is open. |
| `close(): void` | Closes the overlay. |
| `updateValidation( (result: ValidationResult )): void` | Updates the current validation result. Not displayed to the user until `commitValidation` is called. |
| `resetValidation(): void` | Resets the displayed validation state to valid when the user resets the form. |
| `commitValidation(): void` | Commits the realtime validation so it is displayed to the user. |

`'first' |Â 'last'`

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
| `labelProps` | `DOMAttributes` | Props for the label element. |
| `inputProps` | `InputHTMLAttributes<HTMLInputElement>` | Props for the combo box input element. |
| `listBoxProps` | `AriaListBoxOptions<T>` | Props for the list box, to be passed to `useListBox`. |
| `buttonProps` | `AriaButtonProps` | Props for the optional trigger button, to be passed to `useButton`. |
| `descriptionProps` | `DOMAttributes` | Props for the combo box description element, if any. |
| `errorMessageProps` | `DOMAttributes` | Props for the combo box error message element, if any. |
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

Provides state management for a combo box component. Handles building a collection
of items from props and manages the option selection state of the combo box. In addition, it tracks the input value,
focus state, and other properties of the combo box.

`useComboBoxState<T extends object>(
(props: ComboBoxStateOptions<T>
)): ComboBoxState<T>`

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `defaultFilter` | `FilterFn` | â | The filter function used to determine if a option should be included in the combo box list. |
| `allowsEmptyCollection` | `boolean` | â | Whether the combo box allows the menu to be open when the collection is empty. |
| `shouldCloseOnBlur` | `boolean` | â | Whether the combo box menu should close on blur. |
| `defaultItems` | `Iterable<T>` | â | The list of ComboBox items (uncontrolled). |
| `items` | `Iterable<T>` | â | The list of ComboBox items (controlled). |
| `onOpenChange` | `( (isOpen: boolean, , menuTrigger?: MenuTriggerAction )) => void` | â | Method that is called when the open state of the menu changes. Returns the new open state and the action that caused the opening of the menu. |
| `onSelectionChange` | `( (key: Key |Â  |Â null )) => void` | â | Handler that is called when the selection changes. |
| `inputValue` | `string` | â | The value of the ComboBox input (controlled). |
| `defaultInputValue` | `string` | â | The default value of the ComboBox input (uncontrolled). |
| `onInputChange` | `( (value: string )) => void` | â | Handler that is called when the ComboBox input value changes. |
| `allowsCustomValue` | `boolean` | â | Whether the ComboBox allows a non-item matching input value to be set. |
| `menuTrigger` | `MenuTriggerAction` | `'input'` | The interaction required to display the ComboBox menu. |
| `disabledKeys` | `Iterable<Key>` | â | The item keys that are disabled. These items cannot be selected, focused, or otherwise interacted with. |
| `selectedKey` | `Key |Â null` | â | The currently selected key in the collection (controlled). |
| `defaultSelectedKey` | `Key` | â | The initial selected key in the collection (uncontrolled). |
| `isDisabled` | `boolean` | â | Whether the input is disabled. |
| `isReadOnly` | `boolean` | â | Whether the input can be selected but not changed by the user. |
| `placeholder` | `string` | â | Temporary text that occupies the text input when it is empty. |
| `isRequired` | `boolean` | â | Whether user input is required on the input before form submission. |
| `isInvalid` | `boolean` | â | Whether the input value is invalid. |
| `validationBehavior` | `'aria' |Â 'native'` | `'aria'` | Whether to use native HTML form validation to prevent form submission when the value is missing or invalid, or mark the field as required or invalid via ARIA. |
| `validate` | `( (value: ComboBoxValidationValue )) => ValidationError |Â true |Â null |Â undefined` | â | A function that returns an error message if a given value is invalid. Validation errors are displayed to the user when the form is submitted if `validationBehavior="native"`. For realtime validation, use the `isInvalid` prop instead. |
| `autoFocus` | `boolean` | â | Whether the element should receive focus on render. |
| `onFocus` | `( (e: FocusEvent<HTMLInputElement> )) => void` | â | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<HTMLInputElement> )) => void` | â | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | â | Handler that is called when the element's focus status changes. |
| `onKeyDown` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is pressed. |
| `onKeyUp` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is released. |
| `label` | `ReactNode` | â | The content to display as the label. |
| `description` | `ReactNode` | â | A description for the field. Provides a hint such as specific requirements for what to choose. |
| `errorMessage` | `ReactNode |Â ( (v: ValidationResult )) => ReactNode` | â | An error message for the field. |
| `collection` | `Collection<Node<T>>` | â | A pre-constructed collection to use instead of building one from items and children. |

`(
(textValue: string,
, inputValue: string
)) => boolean`

Provides localized string search functionality that is useful for filtering or matching items
in a list. Options can be provided to adjust the sensitivity to case, diacritics, and other parameters.

`useFilter(
(options?: Intl.CollatorOptions
)): Filter`

| Method | Description |
| --- | --- |
| `startsWith( (string: string, , substring: string )): boolean` | Returns whether a string starts with a given substring. |
| `endsWith( (string: string, , substring: string )): boolean` | Returns whether a string ends with a given substring. |
| `contains( (string: string, , substring: string )): boolean` | Returns whether a string contains a given substring. |