# useGridList

Source: https://react-spectrum.adobe.com/react-aria/useGridList.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../GridList).

# useGridList

Provides the behavior and accessibility implementation for a list component with interactive children. A grid list displays data in a single column and enables a user to navigate its contents via directional navigation keys.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useGridList, useGridListItem, useGridListSelectionCheckbox} from 'react-aria'` |

[View ARIA pattern

W3C](https://www.w3.org/WAI/ARIA/apg/patterns/grid/ "View ARIA pattern")[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/gridlist "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/gridlist "View package")

## API[#](#api)

---

`useGridList<T>(
props: AriaGridListOptions<T>,
state: ListState<T>,
ref: RefObject<HTMLElement
|Â  |Â null>
): GridListAria`
`useGridListItem<T>(
props: AriaGridListItemOptions,
state: ListState<T>
|Â  |Â TreeState<T>,
ref: RefObject<FocusableElement
|Â  |Â null>
): GridListItemAria`
`useGridListSelectionCheckbox<T>(
(props: AriaGridSelectionCheckboxProps,
, state: ListState<T>
)): GridSelectionCheckboxAria`

## Features[#](#features)

---

A list can be built using [<ul>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/ul) or [<ol>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/ol) HTML elements, but does not support any user interactions.
HTML lists are meant for static content, rather than lists with rich interactions like focusable elements within rows, keyboard navigation, row selection, etc.
`useGridList` helps achieve accessible and interactive list components that can be styled as needed.

- **Item selection** â Single or multiple selection, with optional checkboxes, disabled rows, and both `toggle` and `replace` selection behaviors.
- **Interactive children** â List items may include interactive elements such as buttons, checkboxes, menus, etc.
- **Actions** â Items support optional row actions such as navigation via click, tap, double click, or `Enter` key.
- **Async loading** â Support for loading items asynchronously, with infinite and virtualized scrolling.
- **Keyboard navigation** â List items and focusable children can be navigated using the arrow keys, along with page up/down, home/end, etc. Typeahead, auto scrolling, and selection modifier keys are supported as well.
- **Touch friendly** â Selection and actions adapt their behavior depending on the device. For example, selection is activated via long press on touch when item actions are present.
- **Accessible** â Follows the [ARIA grid pattern](https://www.w3.org/WAI/ARIA/apg/patterns/grid/), with additional selection announcements via an ARIA live region. Extensively tested across many devices and [assistive technologies](../quality#supported-screen-readers) to ensure announcements and behaviors are consistent.

**Note**: Use `useGridList` when your list items may contain interactive elements such as buttons, checkboxes, menus, etc. within them. If your list items contain only static content such as text and images, then consider using [useListBox](../ListBox/useListBox.html) instead for a slightly better screen reader experience (especially on mobile).

## Anatomy[#](#anatomy)

---

A grid list consists of a container element, with rows of data inside. The rows within a list may contain focusable elements or plain text content.
If the list supports row selection, each row can optionally include a selection checkbox.

The `useGridList` and `useGridListItem` hooks handle keyboard, mouse, and other interactions to support
row selection, in list navigation, and overall focus behavior. Those hooks handle exposing the list and its contents to assistive technology using ARIA. `useGridListSelectionCheckbox` handles row selection and associating each checkbox with its respective rows
for assistive technology.

`useGridList` returns props that you should spread onto the list container element:

| Name | Type | Description |
| --- | --- | --- |
| `gridProps` | `DOMAttributes` | Props for the grid element. |

`useGridListItem` returns props for an individual option and its children, along with states you can use for styling:

| Name | Type | Description |
| --- | --- | --- |
| `rowProps` | `DOMAttributes` | Props for the list row element. |
| `gridCellProps` | `DOMAttributes` | Props for the grid cell element within the list row. |
| `descriptionProps` | `DOMAttributes` | Props for the list item description element, if any. |
| `isPressed` | `boolean` | Whether the item is currently in a pressed state. |
| `isSelected` | `boolean` | Whether the item is currently selected. |
| `isFocused` | `boolean` | Whether the item is currently focused. |
| `isDisabled` | `boolean` | Whether the item is non-interactive, i.e. both selection and actions are disabled and the item may not be focused. Dependent on `disabledKeys` and `disabledBehavior`. |
| `allowsSelection` | `boolean` | Whether the item may be selected, dependent on `selectionMode`, `disabledKeys`, and `disabledBehavior`. |
| `hasAction` | `boolean` | Whether the item has an action, dependent on `onAction`, `disabledKeys`, and `disabledBehavior`. It may also change depending on the current selection state of the list (e.g. when selection is primary). This can be used to enable or disable hover styles or other visual indications of interactivity. |

State is managed by the `useListState`
hook from `@react-stately/list`. The state object should be passed as an option to each of the above hooks where applicable.

Note that an `aria-label` or `aria-labelledby` must be passed to the list to identify the element to assistive technology.

## State management[#](#state-management)

---

`useGridList` requires knowledge of the rows in the list in order to handle keyboard
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

Lists are [collection components](https://react-spectrum.adobe.com/v3/collections.html) that include rows as child elements.
In this example, we'll use the standard HTML unordered list elements along with hooks from React
Aria for each child. You may also use other elements like `<div>` to render these components as appropriate.
We'll walk through creating the list container and list item, then add some additional behavior such as selection.

The `useGridList` hook will be used to render the outer most list element. It uses
the `useListState` hook to construct the list's collection of rows,
and manage state such as the focused row and row selection. We'll use the collection to iterate through
the rows of the List and render the relevant components, which we'll define below.

You may notice the extra `<div>` with `gridCellProps` in our example. This is needed because we are following the [ARIA grid pattern](https://www.w3.org/WAI/ARIA/apg/patterns/grid/), which does not allow rows without any child `gridcell` elements.

```
import {mergeProps, useFocusRing, useGridList, useGridListItem} from 'react-aria';
import {useListState} from 'react-stately';
import {useRef} from 'react';

function List(props) {
  let state = useListState(props);
  let ref = useRef<HTMLUListElement | null>(null);
  let { gridProps } = useGridList(props, state, ref);

  return (
    <ul {...gridProps} ref={ref} className="list">
      {[...state.collection].map((item) => (
        <ListItem key={item.key} item={item} state={state} />
      ))}
    </ul>
  );
}

function ListItem({ item, state }) {
  let ref = React.useRef(null);
  let { rowProps, gridCellProps, isPressed } = useGridListItem(
    { node: item },
    state,
    ref
  );

  let { isFocusVisible, focusProps } = useFocusRing();
  let showCheckbox = state.selectionManager.selectionMode !== 'none' &&
    state.selectionManager.selectionBehavior === 'toggle';

  return (
    <li
      {...mergeProps(rowProps, focusProps)}
      ref={ref}
      className={`${isPressed ? 'pressed' : ''} ${
        isFocusVisible ? 'focus-visible' : ''
      }`}
    >
      <div {...gridCellProps}>
        {showCheckbox && <ListCheckbox item={item} state={state} />}
        {item.rendered}
      </div>
    </li>
  );
}
```

```
import {
  mergeProps,
  useFocusRing,
  useGridList,
  useGridListItem
} from 'react-aria';
import {useListState} from 'react-stately';
import {useRef} from 'react';

function List(props) {
  let state = useListState(props);
  let ref = useRef<HTMLUListElement | null>(null);
  let { gridProps } = useGridList(props, state, ref);

  return (
    <ul {...gridProps} ref={ref} className="list">
      {[...state.collection].map((item) => (
        <ListItem
          key={item.key}
          item={item}
          state={state}
        />
      ))}
    </ul>
  );
}

function ListItem({ item, state }) {
  let ref = React.useRef(null);
  let { rowProps, gridCellProps, isPressed } =
    useGridListItem(
      { node: item },
      state,
      ref
    );

  let { isFocusVisible, focusProps } = useFocusRing();
  let showCheckbox =
    state.selectionManager.selectionMode !== 'none' &&
    state.selectionManager.selectionBehavior === 'toggle';

  return (
    <li
      {...mergeProps(rowProps, focusProps)}
      ref={ref}
      className={`${isPressed ? 'pressed' : ''} ${
        isFocusVisible ? 'focus-visible' : ''
      }`}
    >
      <div {...gridCellProps}>
        {showCheckbox && (
          <ListCheckbox item={item} state={state} />
        )}
        {item.rendered}
      </div>
    </li>
  );
}
```

```
import {
  mergeProps,
  useFocusRing,
  useGridList,
  useGridListItem
} from 'react-aria';
import {useListState} from 'react-stately';
import {useRef} from 'react';

function List(props) {
  let state =
    useListState(props);
  let ref = useRef<
    | HTMLUListElement
    | null
  >(null);
  let { gridProps } =
    useGridList(
      props,
      state,
      ref
    );

  return (
    <ul
      {...gridProps}
      ref={ref}
      className="list"
    >
      {[
        ...state
          .collection
      ].map((item) => (
        <ListItem
          key={item.key}
          item={item}
          state={state}
        />
      ))}
    </ul>
  );
}

function ListItem(
  { item, state }
) {
  let ref = React.useRef(
    null
  );
  let {
    rowProps,
    gridCellProps,
    isPressed
  } = useGridListItem(
    { node: item },
    state,
    ref
  );

  let {
    isFocusVisible,
    focusProps
  } = useFocusRing();
  let showCheckbox =
    state
        .selectionManager
        .selectionMode !==
      'none' &&
    state
        .selectionManager
        .selectionBehavior ===
      'toggle';

  return (
    <li
      {...mergeProps(
        rowProps,
        focusProps
      )}
      ref={ref}
      className={`${
        isPressed
          ? 'pressed'
          : ''
      } ${
        isFocusVisible
          ? 'focus-visible'
          : ''
      }`}
    >
      <div
        {...gridCellProps}
      >
        {showCheckbox &&
          (
            <ListCheckbox
              item={item}
              state={state}
            />
          )}
        {item.rendered}
      </div>
    </li>
  );
}
```

Now we can render a basic example list, with multiple selection and interactive children in each item.

```
import {Item} from 'react-stately';

// Reuse the Button from your component library. See below.
import {Button} from 'your-component-library';

<List
  aria-label="Example List"
  selectionMode="multiple"
  selectionBehavior="replace"
>
  <Item textValue="Charizard">
    Charizard
    <Button onPress={() => alert(`Info for Charizard...`)}>Info</Button>
  </Item>
  <Item textValue="Blastoise">
    Blastoise
    <Button onPress={() => alert(`Info for Blastoise...`)}>Info</Button>
  </Item>
  <Item textValue="Venusaur">
    Venusaur
    <Button onPress={() => alert(`Info for Venusaur...`)}>Info</Button>
  </Item>
  <Item textValue="Pikachu">
    Pikachu
    <Button onPress={() => alert(`Info for Pikachu...`)}>Info</Button>
  </Item>
</List>
```

```
import {Item} from 'react-stately';

// Reuse the Button from your component library. See below.
import {Button} from 'your-component-library';

<List
  aria-label="Example List"
  selectionMode="multiple"
  selectionBehavior="replace"
>
  <Item textValue="Charizard">
    Charizard
    <Button
      onPress={() => alert(`Info for Charizard...`)}
    >
      Info
    </Button>
  </Item>
  <Item textValue="Blastoise">
    Blastoise
    <Button
      onPress={() => alert(`Info for Blastoise...`)}
    >
      Info
    </Button>
  </Item>
  <Item textValue="Venusaur">
    Venusaur
    <Button onPress={() => alert(`Info for Venusaur...`)}>
      Info
    </Button>
  </Item>
  <Item textValue="Pikachu">
    Pikachu
    <Button onPress={() => alert(`Info for Pikachu...`)}>
      Info
    </Button>
  </Item>
</List>
```

```
import {Item} from 'react-stately';

// Reuse the Button from your component library. See below.
import {Button} from 'your-component-library';

<List
  aria-label="Example List"
  selectionMode="multiple"
  selectionBehavior="replace"
>
  <Item textValue="Charizard">
    Charizard
    <Button
      onPress={() =>
        alert(
          `Info for Charizard...`
        )}
    >
      Info
    </Button>
  </Item>
  <Item textValue="Blastoise">
    Blastoise
    <Button
      onPress={() =>
        alert(
          `Info for Blastoise...`
        )}
    >
      Info
    </Button>
  </Item>
  <Item textValue="Venusaur">
    Venusaur
    <Button
      onPress={() =>
        alert(
          `Info for Venusaur...`
        )}
    >
      Info
    </Button>
  </Item>
  <Item textValue="Pikachu">
    Pikachu
    <Button
      onPress={() =>
        alert(
          `Info for Pikachu...`
        )}
    >
      Info
    </Button>
  </Item>
</List>
```

 Show CSS

```
.list {
  padding: 0;
  list-style: none;
  background: var(--page-background);
  border: 1px solid var(--spectrum-global-color-gray-400);
  max-width: 400px;
  min-width: 200px;
  max-height: 250px;
  overflow: auto;
}

.list li {
  padding: 8px;
  outline: none;
  cursor: default;
}

.list li:nth-child(2n) {
  background: var(--spectrum-alias-highlight-hover);
}

.list li.pressed {
  background: var(--spectrum-global-color-gray-200);
}

.list li[aria-selected=true] {
  background: slateblue;
  color: white;
}

.list li.focus-visible {
  outline: 2px solid slateblue;
  outline-offset: -3px;
}

.list li.focus-visible[aria-selected=true] {
  outline-color: white;
}

.list li[aria-disabled] {
  opacity: 0.4;
}

.list [role=gridcell] {
  display: flex;
  align-items: center;
  gap: 4px;
}

.list li button {
  margin-left: auto;
}

/* iOS Safari has a bug that prevents accent-color: white from working. */
@supports not (-webkit-touch-callout: none) {
  .list li input[type=checkbox] {
    accent-color: white;
  }
}
```

```
.list {
  padding: 0;
  list-style: none;
  background: var(--page-background);
  border: 1px solid var(--spectrum-global-color-gray-400);
  max-width: 400px;
  min-width: 200px;
  max-height: 250px;
  overflow: auto;
}

.list li {
  padding: 8px;
  outline: none;
  cursor: default;
}

.list li:nth-child(2n) {
  background: var(--spectrum-alias-highlight-hover);
}

.list li.pressed {
  background: var(--spectrum-global-color-gray-200);
}

.list li[aria-selected=true] {
  background: slateblue;
  color: white;
}

.list li.focus-visible {
  outline: 2px solid slateblue;
  outline-offset: -3px;
}

.list li.focus-visible[aria-selected=true] {
  outline-color: white;
}

.list li[aria-disabled] {
  opacity: 0.4;
}

.list [role=gridcell] {
  display: flex;
  align-items: center;
  gap: 4px;
}

.list li button {
  margin-left: auto;
}

/* iOS Safari has a bug that prevents accent-color: white from working. */
@supports not (-webkit-touch-callout: none) {
  .list li input[type=checkbox] {
    accent-color: white;
  }
}
```

```
.list {
  padding: 0;
  list-style: none;
  background: var(--page-background);
  border: 1px solid var(--spectrum-global-color-gray-400);
  max-width: 400px;
  min-width: 200px;
  max-height: 250px;
  overflow: auto;
}

.list li {
  padding: 8px;
  outline: none;
  cursor: default;
}

.list li:nth-child(2n) {
  background: var(--spectrum-alias-highlight-hover);
}

.list li.pressed {
  background: var(--spectrum-global-color-gray-200);
}

.list li[aria-selected=true] {
  background: slateblue;
  color: white;
}

.list li.focus-visible {
  outline: 2px solid slateblue;
  outline-offset: -3px;
}

.list li.focus-visible[aria-selected=true] {
  outline-color: white;
}

.list li[aria-disabled] {
  opacity: 0.4;
}

.list [role=gridcell] {
  display: flex;
  align-items: center;
  gap: 4px;
}

.list li button {
  margin-left: auto;
}

/* iOS Safari has a bug that prevents accent-color: white from working. */
@supports not (-webkit-touch-callout: none) {
  .list li input[type=checkbox] {
    accent-color: white;
  }
}
```

### Adding selection checkboxes[#](#adding-selection-checkboxes)

Next, let's add support for selection checkboxes to allow the user to select items explicitly.
This is done using the `useGridListSelectionCheckbox`
hook. It is passed the `key` of the item it is contained within. When the user
checks or unchecks the checkbox, the row will be added or removed from the List's selection.

The `Checkbox` component used in this example is independent and can be used separately from `useGridList`. The code is available below.

```
import {useGridListSelectionCheckbox} from 'react-aria';

// Reuse the Checkbox from your component library. See below for details.
import {Checkbox} from 'your-component-library';

function ListCheckbox({ item, state }) {
  let { checkboxProps } = useGridListSelectionCheckbox(
    { key: item.key },
    state
  );
  return <Checkbox {...checkboxProps} />;
}
```

```
import {useGridListSelectionCheckbox} from 'react-aria';

// Reuse the Checkbox from your component library. See below for details.
import {Checkbox} from 'your-component-library';

function ListCheckbox({ item, state }) {
  let { checkboxProps } = useGridListSelectionCheckbox({
    key: item.key
  }, state);
  return <Checkbox {...checkboxProps} />;
}
```

```
import {useGridListSelectionCheckbox} from 'react-aria';

// Reuse the Checkbox from your component library. See below for details.
import {Checkbox} from 'your-component-library';

function ListCheckbox(
  { item, state }
) {
  let { checkboxProps } =
    useGridListSelectionCheckbox(
      { key: item.key },
      state
    );
  return (
    <Checkbox
      {...checkboxProps}
    />
  );
}
```

The following example shows an example list with multiple selection using checkboxes and the default `toggle` [selection behavior](#selection-behavior).

```
<List aria-label="List with selection" selectionMode="multiple">
  <Item textValue="Charizard">
    Charizard
    <Button onPress={() => alert(`Info for Charizard...`)}>Info</Button>
  </Item>
  <Item textValue="Blastoise">
    Blastoise
    <Button onPress={() => alert(`Info for Blastoise...`)}>Info</Button>
  </Item>
  <Item textValue="Venusaur">
    Venusaur
    <Button onPress={() => alert(`Info for Venusaur...`)}>Info</Button>
  </Item>
  <Item textValue="Pikachu">
    Pikachu
    <Button onPress={() => alert(`Info for Pikachu...`)}>Info</Button>
  </Item>
</List>
```

```
<List
  aria-label="List with selection"
  selectionMode="multiple"
>
  <Item textValue="Charizard">
    Charizard
    <Button
      onPress={() => alert(`Info for Charizard...`)}
    >
      Info
    </Button>
  </Item>
  <Item textValue="Blastoise">
    Blastoise
    <Button
      onPress={() => alert(`Info for Blastoise...`)}
    >
      Info
    </Button>
  </Item>
  <Item textValue="Venusaur">
    Venusaur
    <Button onPress={() => alert(`Info for Venusaur...`)}>
      Info
    </Button>
  </Item>
  <Item textValue="Pikachu">
    Pikachu
    <Button onPress={() => alert(`Info for Pikachu...`)}>
      Info
    </Button>
  </Item>
</List>
```

```
<List
  aria-label="List with selection"
  selectionMode="multiple"
>
  <Item textValue="Charizard">
    Charizard
    <Button
      onPress={() =>
        alert(
          `Info for Charizard...`
        )}
    >
      Info
    </Button>
  </Item>
  <Item textValue="Blastoise">
    Blastoise
    <Button
      onPress={() =>
        alert(
          `Info for Blastoise...`
        )}
    >
      Info
    </Button>
  </Item>
  <Item textValue="Venusaur">
    Venusaur
    <Button
      onPress={() =>
        alert(
          `Info for Venusaur...`
        )}
    >
      Info
    </Button>
  </Item>
  <Item textValue="Pikachu">
    Pikachu
    <Button
      onPress={() =>
        alert(
          `Info for Pikachu...`
        )}
    >
      Info
    </Button>
  </Item>
</List>
```

And that's it! We now have a fully interactive List component that can support keyboard navigation, single or multiple selection.
In addition, it is fully accessible for screen readers and other assistive technology. See below for more
examples of how to use the List component that we've built.

### Checkbox[#](#checkbox)

The `Checkbox` component is used in the above example for row selection. It is built using the [useCheckbox](../Checkbox/useCheckbox.html) hook, and can be shared with many other components.

 Show code

```
import {useToggleState} from 'react-stately';
import {useCheckbox} from 'react-aria';

function Checkbox(props) {
  let inputRef = useRef(null);
  let { inputProps } = useCheckbox(
    props,
    useToggleState(props),
    inputRef
  );
  return <input {...inputProps} ref={inputRef} />;
}
```

```
import {useToggleState} from 'react-stately';
import {useCheckbox} from 'react-aria';

function Checkbox(props) {
  let inputRef = useRef(null);
  let { inputProps } = useCheckbox(
    props,
    useToggleState(props),
    inputRef
  );
  return <input {...inputProps} ref={inputRef} />;
}
```

```
import {useToggleState} from 'react-stately';
import {useCheckbox} from 'react-aria';

function Checkbox(
  props
) {
  let inputRef = useRef(
    null
  );
  let { inputProps } =
    useCheckbox(
      props,
      useToggleState(
        props
      ),
      inputRef
    );
  return (
    <input
      {...inputProps}
      ref={inputRef}
    />
  );
}
```

### Button[#](#button)

The `Button` component is used in the above example to show how rows can contain interactive elements. It is built using the [useButton](../Button/useButton.html) hook, and can be shared with many other components.

 Show code

```
import {useButton} from 'react-aria';

function Button(props) {
  let ref = React.useRef(null);
  let { buttonProps } = useButton(props, ref);
  return <button {...buttonProps} ref={ref}>{props.children}</button>;
}
```

```
import {useButton} from 'react-aria';

function Button(props) {
  let ref = React.useRef(null);
  let { buttonProps } = useButton(props, ref);
  return (
    <button {...buttonProps} ref={ref}>
      {props.children}
    </button>
  );
}
```

```
import {useButton} from 'react-aria';

function Button(props) {
  let ref = React.useRef(
    null
  );
  let { buttonProps } =
    useButton(
      props,
      ref
    );
  return (
    <button
      {...buttonProps}
      ref={ref}
    >
      {props.children}
    </button>
  );
}
```

## Usage[#](#usage)

---

### Dynamic collections[#](#dynamic-collections)

So far, our examples have shown static collections, where the data is hard coded.
Dynamic collections, as shown below, can be used when the data comes from an external data source such as an API, or updates over time.
In the example below, the rows are provided to the List via a render function.

```
function ExampleList(props) {
  let rows = [
    { id: 1, name: 'Games' },
    { id: 2, name: 'Program Files' },
    { id: 3, name: 'bootmgr' },
    { id: 4, name: 'log.txt' }
  ];

  return (
    <List
      aria-label="Example dynamic collection List"
      selectionMode="multiple"
      items={rows}
      {...props}
    >
      {(item) => (
        <Item textValue={item.name}>
          {item.name}
          <Button onPress={() => alert(`Info for ${item.name}...`)}>
            Info
          </Button>
        </Item>
      )}
    </List>
  );
}
```

```
function ExampleList(props) {
  let rows = [
    { id: 1, name: 'Games' },
    { id: 2, name: 'Program Files' },
    { id: 3, name: 'bootmgr' },
    { id: 4, name: 'log.txt' }
  ];

  return (
    <List
      aria-label="Example dynamic collection List"
      selectionMode="multiple"
      items={rows}
      {...props}
    >
      {(item) => (
        <Item textValue={item.name}>
          {item.name}
          <Button
            onPress={() =>
              alert(`Info for ${item.name}...`)}
          >
            Info
          </Button>
        </Item>
      )}
    </List>
  );
}
```

```
function ExampleList(
  props
) {
  let rows = [
    {
      id: 1,
      name: 'Games'
    },
    {
      id: 2,
      name:
        'Program Files'
    },
    {
      id: 3,
      name: 'bootmgr'
    },
    {
      id: 4,
      name: 'log.txt'
    }
  ];

  return (
    <List
      aria-label="Example dynamic collection List"
      selectionMode="multiple"
      items={rows}
      {...props}
    >
      {(item) => (
        <Item
          textValue={item
            .name}
        >
          {item.name}
          <Button
            onPress={() =>
              alert(
                `Info for ${item.name}...`
              )}
          >
            Info
          </Button>
        </Item>
      )}
    </List>
  );
}
```

### Single selection[#](#single-selection)

By default, `useListState` doesn't allow row selection but this can be enabled using the `selectionMode` prop. Use `defaultSelectedKeys` to provide a default set of selected rows.
Note that the value of the selected keys must match the `key` prop of the row.

The example below enables single selection mode, and uses `defaultSelectedKeys` to select the row with key equal to "2".
A user can click on a different row to change the selection, or click on the same row again to deselect it entirely.

```
// Using the example above
<ExampleList
  aria-label="List with single selection"
  selectionMode="single"
  selectionBehavior="replace"
  defaultSelectedKeys={[2]}
/>
```

```
// Using the example above
<ExampleList
  aria-label="List with single selection"
  selectionMode="single"
  selectionBehavior="replace"
  defaultSelectedKeys={[2]}
/>
```

```
// Using the example above
<ExampleList
  aria-label="List with single selection"
  selectionMode="single"
  selectionBehavior="replace"
  defaultSelectedKeys={[
    2
  ]}
/>
```

### Multiple selection[#](#multiple-selection)

Multiple selection can be enabled by setting `selectionMode` to `multiple`.

```
<ExampleList
  aria-label="List with multiple selection"
  selectionMode="multiple"
  defaultSelectedKeys={[2, 4]}
/>
```

```
<ExampleList
  aria-label="List with multiple selection"
  selectionMode="multiple"
  defaultSelectedKeys={[2, 4]}
/>
```

```
<ExampleList
  aria-label="List with multiple selection"
  selectionMode="multiple"
  defaultSelectedKeys={[
    2,
    4
  ]}
/>
```

### Disallow empty selection[#](#disallow-empty-selection)

`useGridList` also supports a `disallowEmptySelection` prop which forces the user to have at least one row in the List selected at all times.
In this mode, if a single row is selected and the user presses it, it will not be deselected.

```
<ExampleList
  aria-label="List with disallowed empty selection"
  selectionMode="multiple"
  defaultSelectedKeys={[2]}
  disallowEmptySelection
/>
```

```
<ExampleList
  aria-label="List with disallowed empty selection"
  selectionMode="multiple"
  defaultSelectedKeys={[2]}
  disallowEmptySelection
/>
```

```
<ExampleList
  aria-label="List with disallowed empty selection"
  selectionMode="multiple"
  defaultSelectedKeys={[
    2
  ]}
  disallowEmptySelection
/>
```

### Controlled selection[#](#controlled-selection)

To programmatically control row selection, use the `selectedKeys` prop paired with the `onSelectionChange` callback. The `key` prop from the selected rows will
be passed into the callback when the row is pressed, allowing you to update state accordingly.

```
function PokemonList(props) {
  let rows = [
    { id: 1, name: 'Charizard' },
    { id: 2, name: 'Blastoise' },
    { id: 3, name: 'Venusaur' },
    { id: 4, name: 'Pikachu' }
  ];

  let [selectedKeys, setSelectedKeys] = React.useState(new Set([2]));

  return (
    <List
      aria-label="List with controlled selection"
      items={rows}
      selectionMode="multiple"
      selectedKeys={selectedKeys}
      onSelectionChange={setSelectedKeys}
      {...props}
    >
      {(item) => <Item>{item.name}</Item>}
    </List>
  );
}
```

```
function PokemonList(props) {
  let rows = [
    { id: 1, name: 'Charizard' },
    { id: 2, name: 'Blastoise' },
    { id: 3, name: 'Venusaur' },
    { id: 4, name: 'Pikachu' }
  ];

  let [selectedKeys, setSelectedKeys] = React.useState(
    new Set([2])
  );

  return (
    <List
      aria-label="List with controlled selection"
      items={rows}
      selectionMode="multiple"
      selectedKeys={selectedKeys}
      onSelectionChange={setSelectedKeys}
      {...props}
    >
      {(item) => <Item>{item.name}</Item>}
    </List>
  );
}
```

```
function PokemonList(
  props
) {
  let rows = [
    {
      id: 1,
      name: 'Charizard'
    },
    {
      id: 2,
      name: 'Blastoise'
    },
    {
      id: 3,
      name: 'Venusaur'
    },
    {
      id: 4,
      name: 'Pikachu'
    }
  ];

  let [
    selectedKeys,
    setSelectedKeys
  ] = React.useState(
    new Set([2])
  );

  return (
    <List
      aria-label="List with controlled selection"
      items={rows}
      selectionMode="multiple"
      selectedKeys={selectedKeys}
      onSelectionChange={setSelectedKeys}
      {...props}
    >
      {(item) => (
        <Item>
          {item.name}
        </Item>
      )}
    </List>
  );
}
```

### Disabled rows[#](#disabled-rows)

You can disable specific rows by providing an array of keys to `useListState` via the `disabledKeys` prop. This will disable all interactions on disabled rows,
unless the `disabledBehavior` prop is used to change this behavior.
Note that you are responsible for the styling of disabled rows, however, the selection checkbox will be automatically disabled.

```
// Using the example above
<PokemonList
  aria-label="List with disabled rows"
  selectionMode="multiple"
  disabledKeys={[3]}
/>
```

```
// Using the example above
<PokemonList
  aria-label="List with disabled rows"
  selectionMode="multiple"
  disabledKeys={[3]}
/>
```

```
// Using the example above
<PokemonList
  aria-label="List with disabled rows"
  selectionMode="multiple"
  disabledKeys={[3]}
/>
```

When `disabledBehavior` is set to `selection`, interactions such as focus, dragging, or actions can still be performed on disabled rows.

```
<PokemonList
  aria-label="List with selection disabled for disabled rows"
  selectionMode="multiple"
  disabledKeys={[3]}
  disabledBehavior="selection"
/>
```

```
<PokemonList
  aria-label="List with selection disabled for disabled rows"
  selectionMode="multiple"
  disabledKeys={[3]}
  disabledBehavior="selection"
/>
```

```
<PokemonList
  aria-label="List with selection disabled for disabled rows"
  selectionMode="multiple"
  disabledKeys={[3]}
  disabledBehavior="selection"
/>
```

### Selection behavior[#](#selection-behavior)

By default, `useGridList` uses the `"toggle"` selection behavior, which behaves like a checkbox group: clicking, tapping, or pressing the `Space` or `Enter` keys toggles selection for the focused row. Using the arrow keys moves focus but does not change selection. The `"toggle"` selection mode is often paired with a checkbox in each row as an explicit affordance for selection.

When `selectionBehavior` is set to `"replace"`, clicking a row with the mouse replaces the selection with only that row. Using the arrow keys moves both focus and selection. To select multiple rows, modifier keys such as `Ctrl`, `Cmd`, and `Shift` can be used. On touch screen devices, selection always behaves as toggle since modifier keys may not be available.

These selection styles implement the behaviors defined in [Aria Practices](https://www.w3.org/WAI/ARIA/apg/patterns/listbox/#keyboardinteraction).

```
<PokemonList
  aria-label="List with replace selection behavior"
  selectionMode="multiple"
  selectionBehavior="replace"
/>
```

```
<PokemonList
  aria-label="List with replace selection behavior"
  selectionMode="multiple"
  selectionBehavior="replace"
/>
```

```
<PokemonList
  aria-label="List with replace selection behavior"
  selectionMode="multiple"
  selectionBehavior="replace"
/>
```

### Row actions[#](#row-actions)

`useGridList` supports row actions via the `onAction` prop, which is useful for functionality such as navigation. When nothing is selected, the list performs actions by default when clicking or tapping a row.
Items may be selected using the checkbox, or by long pressing on touch devices. When at least one item is selected, the list is in selection mode, and clicking or tapping a row toggles the selection. Actions may also
be triggered via the `Enter` key, and selection using the `Space` key.

This behavior is slightly different when `selectionBehavior="replace"`, where single clicking selects the row and actions are performed via double click. Touch and keyboard behaviors are unaffected.

```
<div style={{ display: 'flex', flexWrap: 'wrap', gap: 24 }}>
  <ExampleList
    aria-label="Checkbox selection list with row actions"
    selectionMode="multiple"
    selectionBehavior="toggle"
    onAction={(key) => alert(`Opening item ${key}...`)}
  />
  <ExampleList
    aria-label="Highlight selection list with row actions"
    selectionMode="multiple"
    selectionBehavior="replace"
    onAction={(key) => alert(`Opening item ${key}...`)}
  />
</div>
```

```
<div style={{ display: 'flex', flexWrap: 'wrap', gap: 24 }}>
  <ExampleList
    aria-label="Checkbox selection list with row actions"
    selectionMode="multiple"
    selectionBehavior="toggle"
    onAction={(key) => alert(`Opening item ${key}...`)}
  />
  <ExampleList
    aria-label="Highlight selection list with row actions"
    selectionMode="multiple"
    selectionBehavior="replace"
    onAction={(key) => alert(`Opening item ${key}...`)}
  />
</div>
```

```
<div
  style={{
    display: 'flex',
    flexWrap: 'wrap',
    gap: 24
  }}
>
  <ExampleList
    aria-label="Checkbox selection list with row actions"
    selectionMode="multiple"
    selectionBehavior="toggle"
    onAction={(key) =>
      alert(
        `Opening item ${key}...`
      )}
  />
  <ExampleList
    aria-label="Highlight selection list with row actions"
    selectionMode="multiple"
    selectionBehavior="replace"
    onAction={(key) =>
      alert(
        `Opening item ${key}...`
      )}
  />
</div>
```

### Links[#](#links)

Items in a GridList may also be links to another page or website. This can be achieved by passing the `href` prop to the `<Item>` component. Links behave the same way as described above for row actions depending on the `selectionMode` and `selectionBehavior`.

```
<List aria-label="Links" selectionMode="multiple">
  <Item href="https://adobe.com/" target="_blank">Adobe</Item>
  <Item href="https://apple.com/" target="_blank">Apple</Item>
  <Item href="https://google.com/" target="_blank">Google</Item>
  <Item href="https://microsoft.com/" target="_blank">Microsoft</Item>
</List>
```

```
<List aria-label="Links" selectionMode="multiple">
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
</List>
```

```
<List
  aria-label="Links"
  selectionMode="multiple"
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
</List>
```

#### Client side routing[#](#client-side-routing)

The `<Item>` component works with frameworks and client side routers like [Next.js](https://nextjs.org/) and [React Router](https://reactrouter.com/en/main). As with other React Aria components that support links, this works via the `RouterProvider` component at the root of your app. See the [framework setup guide](../frameworks) to learn how to set this up.

### Asynchronous loading[#](#asynchronous-loading)

This example uses the [useAsyncList](../useAsyncList.html) hook to handle asynchronous loading of data from a server. You may additionally want to display a spinner to indicate the loading state to the user, or support features like infinite scroll to load more data.

```
import {useAsyncList} from 'react-stately';

function AsyncList() {
  let list = useAsyncList({
    async load({ signal, cursor }) {
      if (cursor) {
        cursor = cursor.replace(/^http:\/\//i, 'https://');
      }

      let res = await fetch(
        cursor || `https://swapi.py4e.com/api/people/?search=`,
        { signal }
      );
      let json = await res.json();

      return {
        items: json.results,
        cursor: json.next
      };
    }
  });

  return (
    <List
      selectionMode="multiple"
      aria-label="Async loading ListView example"
      items={list.items}
    >
      {(item) => <Item key={item.name}>{item.name}</Item>}
    </List>
  );
}
```

```
import {useAsyncList} from 'react-stately';

function AsyncList() {
  let list = useAsyncList({
    async load({ signal, cursor }) {
      if (cursor) {
        cursor = cursor.replace(/^http:\/\//i, 'https://');
      }

      let res = await fetch(
        cursor ||
          `https://swapi.py4e.com/api/people/?search=`,
        { signal }
      );
      let json = await res.json();

      return {
        items: json.results,
        cursor: json.next
      };
    }
  });

  return (
    <List
      selectionMode="multiple"
      aria-label="Async loading ListView example"
      items={list.items}
    >
      {(item) => <Item key={item.name}>{item.name}</Item>}
    </List>
  );
}
```

```
import {useAsyncList} from 'react-stately';

function AsyncList() {
  let list =
    useAsyncList({
      async load(
        {
          signal,
          cursor
        }
      ) {
        if (cursor) {
          cursor = cursor
            .replace(
              /^http:\/\//i,
              'https://'
            );
        }

        let res =
          await fetch(
            cursor ||
              `https://swapi.py4e.com/api/people/?search=`,
            { signal }
          );
        let json =
          await res
            .json();

        return {
          items:
            json.results,
          cursor:
            json.next
        };
      }
    });

  return (
    <List
      selectionMode="multiple"
      aria-label="Async loading ListView example"
      items={list.items}
    >
      {(item) => (
        <Item
          key={item.name}
        >
          {item.name}
        </Item>
      )}
    </List>
  );
}
```

## Internationalization[#](#internationalization)

---

`useGridList` handles some aspects of internationalization automatically.
For example, type to select is implemented with an
[Intl.Collator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Collator)
for internationalized string matching, and keyboard navigation is mirrored in right-to-left languages.
You are responsible for localizing all text content within the List.

### RTL[#](#rtl)

In right-to-left languages, the list layout should be mirrored. The row contents should be ordered from right to left and the row's text alignment should be inverted. Ensure that your CSS accounts for this.

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `isVirtualized` | `boolean` | â | Whether the list uses virtual scrolling. |
| `disallowTypeAhead` | `boolean` | `false` | Whether typeahead navigation is disabled. |
| `keyboardDelegate` | `KeyboardDelegate` | â | An optional keyboard delegate implementation for type to select, to override the default. |
| `layoutDelegate` | `LayoutDelegate` | â | A delegate object that provides layout information for items in the collection. By default this uses the DOM, but this can be overridden to implement things like virtualized scrolling. |
| `shouldFocusWrap` | `boolean` | `false` | Whether focus should wrap around when the end/start is reached. |
| `linkBehavior` | `'action' |Â 'selection' |Â 'override'` | `'action'` | The behavior of links in the collection. - 'action': link behaves like onAction. - 'selection': link follows selection interactions (e.g. if URL drives selection). - 'override': links override all other interactions (link items are not selectable). |
| `keyboardNavigationBehavior` | `'arrow' |Â 'tab'` | `'arrow'` | Whether keyboard navigation to focusable elements within grid list items is via the left/right arrow keys or the tab key. |
| `escapeKeyBehavior` | `'clearSelection' |Â 'none'` | `'clearSelection'` | Whether pressing the escape key should clear selection in the grid list or not.  Most experiences should not modify this option as it eliminates a keyboard user's ability to easily clear selection. Only use if the escape key is being handled externally or should not trigger selection clearing contextually. |
| `autoFocus` | `boolean |Â FocusStrategy` | â | Whether to auto focus the gridlist or an option. |
| `onAction` | `( (key: Key )) => void` | â | Handler that is called when a user performs an action on an item. The exact user event depends on the collection's `selectionBehavior` prop and the interaction modality. |
| `disabledBehavior` | `DisabledBehavior` | `"all"` | Whether `disabledKeys` applies to all interactions, or only selection. |
| `shouldSelectOnPressUp` | `boolean` | â | Whether selection should occur on press up instead of press down. |
| `items` | `Iterable<T>` | â | Item objects in the collection. |
| `disabledKeys` | `Iterable<Key>` | â | The item keys that are disabled. These items cannot be selected, focused, or otherwise interacted with. |
| `selectionMode` | `SelectionMode` | â | The type of selection that is allowed in the collection. |
| `disallowEmptySelection` | `boolean` | â | Whether the collection allows empty selection. |
| `selectedKeys` | `'all' |Â Iterable<Key>` | â | The currently selected keys in the collection (controlled). |
| `defaultSelectedKeys` | `'all' |Â Iterable<Key>` | â | The initial selected keys in the collection (uncontrolled). |
| `onSelectionChange` | `( (keys: Selection )) => void` | â | Handler that is called when the selection changes. |
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

`'first' |Â 'last'`

`string |Â number`

`'selection' |Â 'all'`

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

`'toggle' |Â 'replace'`

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
| `gridProps` | `DOMAttributes` | Props for the grid element. |

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
| `node` | `Node<unknown>` | An object representing the list item. Contains all the relevant information that makes up the list row. |
| `isVirtualized` | `boolean` | Whether the list row is contained in a virtual scroller. |
| `shouldSelectOnPressUp` | `boolean` | Whether selection should occur on press up instead of press down. |
| `hasChildItems` | `boolean` | Whether this item has children, even if not loaded yet. |

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `collection` | `Collection<Node<T>>` | A collection of items in the tree. |
| `disabledKeys` | `Set<Key>` | A set of keys for items that are disabled. |
| `expandedKeys` | `Set<Key>` | A set of keys for items that are expanded. |
| `selectionManager` | `SelectionManager` | A selection manager to read and update multiple selection state. |

### Methods

| Method | Description |
| --- | --- |
| `toggleKey( (key: Key )): void` | Toggles the expanded state for an item by its key. |
| `setExpandedKeys( (keys: Set<Key> )): void` | Replaces the set of expanded keys. |

| Name | Type | Description |
| --- | --- | --- |
| `rowProps` | `DOMAttributes` | Props for the list row element. |
| `gridCellProps` | `DOMAttributes` | Props for the grid cell element within the list row. |
| `descriptionProps` | `DOMAttributes` | Props for the list item description element, if any. |
| `isPressed` | `boolean` | Whether the item is currently in a pressed state. |
| `isSelected` | `boolean` | Whether the item is currently selected. |
| `isFocused` | `boolean` | Whether the item is currently focused. |
| `isDisabled` | `boolean` | Whether the item is non-interactive, i.e. both selection and actions are disabled and the item may not be focused. Dependent on `disabledKeys` and `disabledBehavior`. |
| `allowsSelection` | `boolean` | Whether the item may be selected, dependent on `selectionMode`, `disabledKeys`, and `disabledBehavior`. |
| `hasAction` | `boolean` | Whether the item has an action, dependent on `onAction`, `disabledKeys`, and `disabledBehavior`. It may also change depending on the current selection state of the list (e.g. when selection is primary). This can be used to enable or disable hover styles or other visual indications of interactivity. |

| Name | Type | Description |
| --- | --- | --- |
| `key` | `Key` | A unique key for the checkbox. |

| Name | Type | Description |
| --- | --- | --- |
| `checkboxProps` | `AriaCheckboxProps` | Props for the row selection checkbox element. |

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `isIndeterminate` | `boolean` | â | Indeterminism is presentational only. The indeterminate visual representation remains regardless of user interaction. |
| `children` | `ReactNode` | â | The label for the element. |
| `value` | `string` | â | The value of the input element, used when submitting an HTML form. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefvalue). |
| `defaultSelected` | `boolean` | â | Whether the element should be selected (uncontrolled). |
| `isSelected` | `boolean` | â | Whether the element should be selected (controlled). |
| `onChange` | `( (isSelected: boolean )) => void` | â | Handler that is called when the element's selection state changes. |
| `isDisabled` | `boolean` | â | Whether the input is disabled. |
| `isReadOnly` | `boolean` | â | Whether the input can be selected but not changed by the user. |
| `isRequired` | `boolean` | â | Whether user input is required on the input before form submission. |
| `isInvalid` | `boolean` | â | Whether the input value is invalid. |
| `validationBehavior` | `'aria' |Â 'native'` | `'aria'` | Whether to use native HTML form validation to prevent form submission when the value is missing or invalid, or mark the field as required or invalid via ARIA. |
| `validate` | `( (value: boolean )) => ValidationError |Â true |Â null |Â undefined` | â | A function that returns an error message if a given value is invalid. Validation errors are displayed to the user when the form is submitted if `validationBehavior="native"`. For realtime validation, use the `isInvalid` prop instead. |
| `autoFocus` | `boolean` | â | Whether the element should receive focus on render. |
| `onFocus` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | â | Handler that is called when the element's focus status changes. |
| `onKeyDown` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is pressed. |
| `onKeyUp` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is released. |
| `name` | `string` | â | The name of the input element, used when submitting an HTML form. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefname). |
| `form` | `string` | â | The `<form>` element to associate the input with. The value of this attribute must be the id of a `<form>` in the same document. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input#form). |
| `aria-controls` | `string` | â | Identifies the element (or elements) whose contents or presence are controlled by the current element. |
| `excludeFromTabOrder` | `boolean` | â | Whether to exclude the element from the sequential tab order. If true, the element will not be focusable via the keyboard by tabbing. This should be avoided except in rare scenarios where an alternative means of accessing the element or its functionality via the keyboard is available. |
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `aria-label` | `string` | â | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |
| `aria-errormessage` | `string` | â | Identifies the element that provides an error message for the object. |
| `onPress` | `( (e: PressEvent )) => void` | â | Handler that is called when the press is released over the target. |
| `onPressStart` | `( (e: PressEvent )) => void` | â | Handler that is called when a press interaction starts. |
| `onPressEnd` | `( (e: PressEvent )) => void` | â | Handler that is called when a press interaction ends, either over the target or when the pointer leaves the target. |
| `onPressChange` | `( (isPressed: boolean )) => void` | â | Handler that is called when the press state changes. |
| `onPressUp` | `( (e: PressEvent )) => void` | â | Handler that is called when a press is released over the target, regardless of whether it started on the target or not. |
| `onClick` | `( (e: MouseEvent<FocusableElement> )) => void` | â | **Not recommended â use `onPress` instead.** `onClick` is an alias for `onPress` provided for compatibility with other libraries. `onPress` provides additional event details for non-mouse interactions. |

`'valid' |Â 'invalid'`

`string |Â string[]`

`BaseEvent<ReactKeyboardEvent<any>>`

`SyntheticEvent &Â {

stopPropagation: () => void,

continuePropagation: () => void

}`

Provides the behavior and accessibility implementation for a list component with interactive children.
A grid list displays data in a single column and enables a user to navigate its contents via directional navigation keys.

`useGridList<T>(
props: AriaGridListOptions<T>,
state: ListState<T>,
ref: RefObject<HTMLElement
|Â  |Â null>
): GridListAria`

Provides the behavior and accessibility implementation for a row in a grid list.

`useGridListItem<T>(
props: AriaGridListItemOptions,
state: ListState<T>
|Â  |Â TreeState<T>,
ref: RefObject<FocusableElement
|Â  |Â null>
): GridListItemAria`

Provides the behavior and accessibility implementation for a selection checkbox in a grid list.

`useGridListSelectionCheckbox<T>(
(props: AriaGridSelectionCheckboxProps,
, state: ListState<T>
)): GridSelectionCheckboxAria`

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