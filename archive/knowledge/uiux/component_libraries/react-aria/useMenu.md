# useMenu

Source: https://react-spectrum.adobe.com/react-aria/useMenu.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../Menu).

# useMenu

Provides the behavior and accessibility implementation for a menu component.
A menu displays a list of actions or options that a user can choose.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useMenuTrigger, useMenu, useMenuItem, useMenuSection} from 'react-aria'` |

[View ARIA pattern

W3C](https://www.w3.org/WAI/ARIA/apg/patterns/menu/ "View ARIA pattern")[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/menu "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/menu "View package")

## API[#](#api)

---

`useMenuTrigger<T>(
props: AriaMenuTriggerProps,
state: MenuTriggerState,
ref: RefObject<Element
|Â  |Â null>
): MenuTriggerAria<T>`
`useMenu<T>(
props: AriaMenuOptions<T>,
state: TreeState<T>,
ref: RefObject<HTMLElement
|Â  |Â null>
): MenuAria`
`useMenuItem<T>(
props: AriaMenuItemProps,
state: TreeState<T>,
ref: RefObject<FocusableElement
|Â  |Â null>
): MenuItemAria`
`useMenuSection(
(props: AriaMenuSectionProps
)): MenuSectionAria`

## Features[#](#features)

---

There is no native element to implement a menu in HTML that is widely supported. `useMenuTrigger` and `useMenu`
help achieve accessible menu components that can be styled as needed.

- Exposed to assistive technology as a button with a `menu` using ARIA
- Support for single, multiple, or no selection
- Support for disabled items
- Support for sections
- Complex item labeling support for accessibility
- Keyboard navigation support including arrow keys, home/end, page up/down
- Automatic scrolling support during keyboard navigation
- Keyboard support for opening the menu using the arrow keys, including automatically focusing
  the first or last item accordingly
- Typeahead to allow focusing items by typing text
- Support for use with virtualized lists

## Anatomy[#](#anatomy)

---

A menu trigger consists of a button or other trigger element combined with a popup menu,
with a list of menu items or groups inside. `useMenuTrigger`, `useMenu`, `useMenuItem`,
and `useMenuSection` handle exposing this to assistive technology using ARIA, along with
handling keyboard, mouse, and interactions to support selection and focus behavior.

`useMenuTrigger` returns props that you should spread onto the appropriate element:

| Name | Type | Description |
| --- | --- | --- |
| `menuTriggerProps` | `AriaButtonProps` | Props for the menu trigger element. |
| `menuProps` | `AriaMenuOptions<T>` | Props for the menu. |

`useMenu` returns props that you should spread onto the menu container element:

| Name | Type | Description |
| --- | --- | --- |
| `menuProps` | `DOMAttributes` | Props for the menu element. |

`useMenuItem` returns props for an individual item and its children:

| Name | Type | Description |
| --- | --- | --- |
| `menuItemProps` | `DOMAttributes` | Props for the menu item element. |
| `labelProps` | `DOMAttributes` | Props for the main text element inside the menu item. |
| `descriptionProps` | `DOMAttributes` | Props for the description text element inside the menu item, if any. |
| `keyboardShortcutProps` | `DOMAttributes` | Props for the keyboard shortcut text element inside the item, if any. |
| `isFocused` | `boolean` | Whether the item is currently focused. |
| `isFocusVisible` | `boolean` | Whether the item is keyboard focused. |
| `isSelected` | `boolean` | Whether the item is currently selected. |
| `isPressed` | `boolean` | Whether the item is currently in a pressed state. |
| `isDisabled` | `boolean` | Whether the item is disabled. |

`useMenuSection` returns props for a section:

| Name | Type | Description |
| --- | --- | --- |
| `itemProps` | `DOMAttributes` | Props for the wrapper list item. |
| `headingProps` | `DOMAttributes` | Props for the heading element, if any. |
| `groupProps` | `DOMAttributes` | Props for the group element. |

State for the trigger is managed by the `useMenuTriggerState`
hook from `@react-stately/menu`. State for the menu itself is managed by the `useTreeState`
hook from `@react-stately/tree`. These state objects should be passed to the appropriate React Aria hooks.

If a menu, menu item, or group does not have a visible label, an `aria-label` or `aria-labelledby`
prop must be passed instead to identify the element to assistive technology.

## Example[#](#example)

---

A menu consists of several components: a menu button to toggle the menu popup, and the menu itself, which contains
items or sections of items. We'll go through each component one by one.

### MenuButton[#](#menubutton)

We'll start with the `MenuButton` component, which is what will trigger our menu to appear. This uses
the `useMenuTrigger` and `useMenuTriggerState` hooks.
The `Popover` and `Button` components used in this example are independent, and can be shared by many other components.
The code is available below, and documentation is available on the corresponding pages.

```
import type {MenuTriggerProps} from 'react-stately';
import {useMenuTrigger} from 'react-aria';
import {Item, useMenuTriggerState} from 'react-stately';

// Reuse the Popover, and Button from your component library. See below for details.
import {Button, Popover} from 'your-component-library';

interface MenuButtonProps<T> extends AriaMenuProps<T>, MenuTriggerProps {
  label?: string;
}

function MenuButton<T extends object>(props: MenuButtonProps<T>) {
  // Create state based on the incoming props
  let state = useMenuTriggerState(props);

  // Get props for the button and menu elements
  let ref = React.useRef(null);
  let { menuTriggerProps, menuProps } = useMenuTrigger<T>({}, state, ref);

  return (
    <>
      <Button
        {...menuTriggerProps}
        buttonRef={ref}
        style={{ height: 30, fontSize: 14 }}
      >
        {props.label}
        <span aria-hidden="true" style={{ paddingLeft: 5 }}>â¼</span>
      </Button>
      {state.isOpen &&
        (
          <Popover state={state} triggerRef={ref} placement="bottom start">
            <Menu
              {...props}
              {...menuProps}
            />
          </Popover>
        )}
    </>
  );
}
```

```
import type {MenuTriggerProps} from 'react-stately';
import {useMenuTrigger} from 'react-aria';
import {Item, useMenuTriggerState} from 'react-stately';

// Reuse the Popover, and Button from your component library. See below for details.
import {Button, Popover} from 'your-component-library';

interface MenuButtonProps<T>
  extends AriaMenuProps<T>, MenuTriggerProps {
  label?: string;
}

function MenuButton<T extends object>(
  props: MenuButtonProps<T>
) {
  // Create state based on the incoming props
  let state = useMenuTriggerState(props);

  // Get props for the button and menu elements
  let ref = React.useRef(null);
  let { menuTriggerProps, menuProps } = useMenuTrigger<T>(
    {},
    state,
    ref
  );

  return (
    <>
      <Button
        {...menuTriggerProps}
        buttonRef={ref}
        style={{ height: 30, fontSize: 14 }}
      >
        {props.label}
        <span aria-hidden="true" style={{ paddingLeft: 5 }}>
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
            <Menu
              {...props}
              {...menuProps}
            />
          </Popover>
        )}
    </>
  );
}
```

```
import type {MenuTriggerProps} from 'react-stately';
import {useMenuTrigger} from 'react-aria';
import {
  Item,
  useMenuTriggerState
} from 'react-stately';

// Reuse the Popover, and Button from your component library. See below for details.
import {
  Button,
  Popover
} from 'your-component-library';

interface MenuButtonProps<
  T
> extends
  AriaMenuProps<T>,
  MenuTriggerProps {
  label?: string;
}

function MenuButton<
  T extends object
>(
  props: MenuButtonProps<
    T
  >
) {
  // Create state based on the incoming props
  let state =
    useMenuTriggerState(
      props
    );

  // Get props for the button and menu elements
  let ref = React.useRef(
    null
  );
  let {
    menuTriggerProps,
    menuProps
  } = useMenuTrigger<T>(
    {},
    state,
    ref
  );

  return (
    <>
      <Button
        {...menuTriggerProps}
        buttonRef={ref}
        style={{
          height: 30,
          fontSize: 14
        }}
      >
        {props.label}
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
            <Menu
              {...props}
              {...menuProps}
            />
          </Popover>
        )}
    </>
  );
}
```

### Menu[#](#menu)

Next, let's implement the `Menu` component. This will appear inside the `Popover` when the user presses the button.
It is built using the `useMenu` and `useTreeState` hooks.
For each item in the collection in state, we render either a `MenuItem` or `MenuSection` (defined [below](#sections)) according to the item's `type` property.

```
import type {AriaMenuProps} from 'react-aria';
import {useTreeState} from 'react-stately';
import {useMenu} from 'react-aria';

function Menu<T extends object>(props: AriaMenuProps<T>) {
  // Create menu state based on the incoming props
  let state = useTreeState(props);

  // Get props for the menu element
  let ref = React.useRef(null);
  let { menuProps } = useMenu(props, state, ref);

  return (
    <ul {...menuProps} ref={ref}>
      {[...state.collection].map((item) => (
        item.type === 'section'
          ? <MenuSection key={item.key} section={item} state={state} />
          : <MenuItem key={item.key} item={item} state={state} />
      ))}
    </ul>
  );
}
```

```
import type {AriaMenuProps} from 'react-aria';
import {useTreeState} from 'react-stately';
import {useMenu} from 'react-aria';

function Menu<T extends object>(props: AriaMenuProps<T>) {
  // Create menu state based on the incoming props
  let state = useTreeState(props);

  // Get props for the menu element
  let ref = React.useRef(null);
  let { menuProps } = useMenu(props, state, ref);

  return (
    <ul {...menuProps} ref={ref}>
      {[...state.collection].map((item) => (
        item.type === 'section'
          ? (
            <MenuSection
              key={item.key}
              section={item}
              state={state}
            />
          )
          : (
            <MenuItem
              key={item.key}
              item={item}
              state={state}
            />
          )
      ))}
    </ul>
  );
}
```

```
import type {AriaMenuProps} from 'react-aria';
import {useTreeState} from 'react-stately';
import {useMenu} from 'react-aria';

function Menu<
  T extends object
>(
  props: AriaMenuProps<T>
) {
  // Create menu state based on the incoming props
  let state =
    useTreeState(props);

  // Get props for the menu element
  let ref = React.useRef(
    null
  );
  let { menuProps } =
    useMenu(
      props,
      state,
      ref
    );

  return (
    <ul
      {...menuProps}
      ref={ref}
    >
      {[
        ...state
          .collection
      ].map((item) => (
        item.type ===
            'section'
          ? (
            <MenuSection
              key={item
                .key}
              section={item}
              state={state}
            />
          )
          : (
            <MenuItem
              key={item
                .key}
              item={item}
              state={state}
            />
          )
      ))}
    </ul>
  );
}
```

### MenuItem[#](#menuitem)

Now let's implement `MenuItem`. This is built using `useMenuItem`,
and the `state` object passed via props from `Menu`.

```
import {useMenuItem} from 'react-aria';

function MenuItem({ item, state }) {
  // Get props for the menu item element
  let ref = React.useRef(null);
  let { menuItemProps, isSelected } = useMenuItem(
    { key: item.key },
    state,
    ref
  );

  return (
    <li {...menuItemProps} ref={ref}>
      {item.rendered}
      {isSelected && <span aria-hidden="true">â</span>}
    </li>
  );
}
```

```
import {useMenuItem} from 'react-aria';

function MenuItem({ item, state }) {
  // Get props for the menu item element
  let ref = React.useRef(null);
  let { menuItemProps, isSelected } = useMenuItem(
    { key: item.key },
    state,
    ref
  );

  return (
    <li {...menuItemProps} ref={ref}>
      {item.rendered}
      {isSelected && <span aria-hidden="true">â</span>}
    </li>
  );
}
```

```
import {useMenuItem} from 'react-aria';

function MenuItem(
  { item, state }
) {
  // Get props for the menu item element
  let ref = React.useRef(
    null
  );
  let {
    menuItemProps,
    isSelected
  } = useMenuItem(
    { key: item.key },
    state,
    ref
  );

  return (
    <li
      {...menuItemProps}
      ref={ref}
    >
      {item.rendered}
      {isSelected && (
        <span aria-hidden="true">
          â
        </span>
      )}
    </li>
  );
}
```

Now we can render a simple menu with actionable items:

```
<MenuButton label="Actions" onAction={alert}>
  <Item key="copy">Copy</Item>
  <Item key="cut">Cut</Item>
  <Item key="paste">Paste</Item>
</MenuButton>
```

```
<MenuButton label="Actions" onAction={alert}>
  <Item key="copy">Copy</Item>
  <Item key="cut">Cut</Item>
  <Item key="paste">Paste</Item>
</MenuButton>
```

```
<MenuButton
  label="Actions"
  onAction={alert}
>
  <Item key="copy">
    Copy
  </Item>
  <Item key="cut">
    Cut
  </Item>
  <Item key="paste">
    Paste
  </Item>
</MenuButton>
```

 Show CSS

```
[role=menu] {
  margin: 0;
  padding: 0;
  list-style: none;
  width: 200px;
}

[role=menuitem],
[role=menuitemradio],
[role=menuitemcheckbox] {
  padding: 2px 5px;
  outline: none;
  cursor: default;
  display: flex;
  justify-content: space-between;
  color: black;

  &:focus {
    background: gray;
    color: white;
  }

  &[aria-disabled] {
    color: gray;
  }
}
```

```
[role=menu] {
  margin: 0;
  padding: 0;
  list-style: none;
  width: 200px;
}

[role=menuitem],
[role=menuitemradio],
[role=menuitemcheckbox] {
  padding: 2px 5px;
  outline: none;
  cursor: default;
  display: flex;
  justify-content: space-between;
  color: black;

  &:focus {
    background: gray;
    color: white;
  }

  &[aria-disabled] {
    color: gray;
  }
}
```

```
[role=menu] {
  margin: 0;
  padding: 0;
  list-style: none;
  width: 200px;
}

[role=menuitem],
[role=menuitemradio],
[role=menuitemcheckbox] {
  padding: 2px 5px;
  outline: none;
  cursor: default;
  display: flex;
  justify-content: space-between;
  color: black;

  &:focus {
    background: gray;
    color: white;
  }

  &[aria-disabled] {
    color: gray;
  }
}
```

### Popover[#](#popover)

The `Popover` component is used to contain the menu.
It can be shared between many other components, including [ComboBox](../ComboBox/useComboBox.html),
[Select](../Select/useSelect.html), and others.
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
          background: 'lightgray',
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
          background: 'lightgray',
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
            'lightgray',
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

### Button[#](#button)

The `Button` component is used in the above example to toggle the menu. It is built using the [useButton](../Button/useButton.html) hook, and can be shared with many other components.

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

[![](/tailwind.05c39dc7.png)

Tailwind CSS

An example of styling a Menu with Tailwind.](https://codesandbox.io/s/awesome-boyd-c0gbv5?file=/src/Menu.tsx)

## Dynamic collections[#](#dynamic-collections)

---

`Menu` follows the [Collection Components API](https://react-spectrum.adobe.com/v3/collections.html), accepting both static and dynamic collections.
The examples above show static collections, which can be used when the full list of options is known ahead of time. Dynamic collections,
as shown below, can be used when the options come from an external data source such as an API call, or update over time.

As seen below, an iterable list of options is passed to the ComboBox using the `items` prop. Each item accepts a `key` prop, which
is passed to the `onSelectionChange` handler to identify the selected item. Alternatively, if the item objects contain an `id` property,
as shown in the example below, then this is used automatically and a `key` prop is not required.

```
function Example() {
  let items = [
    {id: 1, name: 'New'},
    {id: 2, name: 'Open'},
    {id: 3, name: 'Close'},
    {id: 4, name: 'Save'},
    {id: 5, name: 'Duplicate'},
    {id: 6, name: 'Rename'},
    {id: 7, name: 'Move'}
  ];

  return (
    <MenuButton label="Actions" items={items} onAction={alert}>
      {(item) => <Item>{item.name}</Item>}
    </MenuButton>
  );
}
```

```
function Example() {
  let items = [
    { id: 1, name: 'New' },
    { id: 2, name: 'Open' },
    { id: 3, name: 'Close' },
    { id: 4, name: 'Save' },
    { id: 5, name: 'Duplicate' },
    { id: 6, name: 'Rename' },
    { id: 7, name: 'Move' }
  ];

  return (
    <MenuButton
      label="Actions"
      items={items}
      onAction={alert}
    >
      {(item) => <Item>{item.name}</Item>}
    </MenuButton>
  );
}
```

```
function Example() {
  let items = [
    {
      id: 1,
      name: 'New'
    },
    {
      id: 2,
      name: 'Open'
    },
    {
      id: 3,
      name: 'Close'
    },
    {
      id: 4,
      name: 'Save'
    },
    {
      id: 5,
      name: 'Duplicate'
    },
    {
      id: 6,
      name: 'Rename'
    },
    {
      id: 7,
      name: 'Move'
    }
  ];

  return (
    <MenuButton
      label="Actions"
      items={items}
      onAction={alert}
    >
      {(item) => (
        <Item>
          {item.name}
        </Item>
      )}
    </MenuButton>
  );
}
```

## Selection[#](#selection)

---

Menu supports multiple selection modes. By default, selection is disabled, however this can be changed using the `selectionMode` prop.
Use `defaultSelectedKeys` to provide a default set of selected items (uncontrolled) and `selectedKeys` to set the selected items (controlled). The value of the selected keys must match the `key` prop of the items.
See the `react-stately` [Selection docs](https://react-spectrum.adobe.com/v3/selection.html) for more details.

```
import type {Selection} from 'react-stately';

function Example() {
  let [selected, setSelected] = React.useState<Selection>(
    new Set(['sidebar', 'console'])
  );

  return (
    <>
      <MenuButton
        label="View"
        selectionMode="multiple"
        selectedKeys={selected}
        onSelectionChange={setSelected}
      >
        <Item key="sidebar">Sidebar</Item>
        <Item key="searchbar">Searchbar</Item>
        <Item key="tools">Tools</Item>
        <Item key="console">Console</Item>
      </MenuButton>
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
    new Set(['sidebar', 'console'])
  );

  return (
    <>
      <MenuButton
        label="View"
        selectionMode="multiple"
        selectedKeys={selected}
        onSelectionChange={setSelected}
      >
        <Item key="sidebar">Sidebar</Item>
        <Item key="searchbar">Searchbar</Item>
        <Item key="tools">Tools</Item>
        <Item key="console">Console</Item>
      </MenuButton>
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
  >(
    new Set([
      'sidebar',
      'console'
    ])
  );

  return (
    <>
      <MenuButton
        label="View"
        selectionMode="multiple"
        selectedKeys={selected}
        onSelectionChange={setSelected}
      >
        <Item key="sidebar">
          Sidebar
        </Item>
        <Item key="searchbar">
          Searchbar
        </Item>
        <Item key="tools">
          Tools
        </Item>
        <Item key="console">
          Console
        </Item>
      </MenuButton>
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

## Sections[#](#sections)

---

Menu supports sections with separators and headings in order to group options. Sections can be used by wrapping groups of Items in a `Section` component. Each `Section` takes a `title` and `key` prop.
To implement sections, implement the `ListBoxSection` component referenced above
using the `useMenuSection` hook. It will include four extra elements:
an `<li>` between the sections to represent the separator, an `<li>` to contain the heading `<span>` element, and a
`<ul>` to contain the child items. This structure is necessary to ensure HTML
semantics are correct.

```
import {useMenuSection, useSeparator} from 'react-aria';

function MenuSection({ section, state }) {
  let { itemProps, headingProps, groupProps } = useMenuSection({
    heading: section.rendered,
    'aria-label': section['aria-label']
  });

  let { separatorProps } = useSeparator({
    elementType: 'li'
  });

  // If the section is not the first, add a separator element.
  // The heading is rendered inside an <li> element, which contains
  // a <ul> with the child items.
  return (
    <>
      {section.key !== state.collection.getFirstKey() &&
        (
          <li
            {...separatorProps}
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
            <MenuItem
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
import {useMenuSection, useSeparator} from 'react-aria';

function MenuSection({ section, state }) {
  let { itemProps, headingProps, groupProps } =
    useMenuSection({
      heading: section.rendered,
      'aria-label': section['aria-label']
    });

  let { separatorProps } = useSeparator({
    elementType: 'li'
  });

  // If the section is not the first, add a separator element.
  // The heading is rendered inside an <li> element, which contains
  // a <ul> with the child items.
  return (
    <>
      {section.key !== state.collection.getFirstKey() &&
        (
          <li
            {...separatorProps}
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
            <MenuItem
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
import {
  useMenuSection,
  useSeparator
} from 'react-aria';

function MenuSection(
  { section, state }
) {
  let {
    itemProps,
    headingProps,
    groupProps
  } = useMenuSection({
    heading:
      section.rendered,
    'aria-label':
      section[
        'aria-label'
      ]
  });

  let {
    separatorProps
  } = useSeparator({
    elementType: 'li'
  });

  // If the section is not the first, add a separator element.
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
            {...separatorProps}
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
              <MenuItem
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

With this in place, we can now render a static menu with multiple sections:

```
import {Section} from 'react-stately';

<MenuButton label="Actions" onAction={alert}>
  <Section title="Styles">
    <Item key="bold">Bold</Item>
    <Item key="underline">Underline</Item>
  </Section>
  <Section title="Align">
    <Item key="left">Left</Item>
    <Item key="middle">Middle</Item>
    <Item key="right">Right</Item>
  </Section>
</MenuButton>
```

```
import {Section} from 'react-stately';

<MenuButton label="Actions" onAction={alert}>
  <Section title="Styles">
    <Item key="bold">Bold</Item>
    <Item key="underline">Underline</Item>
  </Section>
  <Section title="Align">
    <Item key="left">Left</Item>
    <Item key="middle">Middle</Item>
    <Item key="right">Right</Item>
  </Section>
</MenuButton>
```

```
import {Section} from 'react-stately';

<MenuButton
  label="Actions"
  onAction={alert}
>
  <Section title="Styles">
    <Item key="bold">
      Bold
    </Item>
    <Item key="underline">
      Underline
    </Item>
  </Section>
  <Section title="Align">
    <Item key="left">
      Left
    </Item>
    <Item key="middle">
      Middle
    </Item>
    <Item key="right">
      Right
    </Item>
  </Section>
</MenuButton>
```

### Dynamic items[#](#dynamic-items)

The above example shows sections with static items. Sections can also be populated from a hierarchical data structure.
Similarly to the props on Menu, `<Section>` takes an array of data using the `items` prop.

```
import type {Selection} from 'react-stately';

function Example() {
  let [selected, setSelected] = React.useState<Selection>(new Set([1,3]));
  let openWindows = [
    {
      name: 'Left Panel',
      id: 'left',
      children: [
        {id: 1, name: 'Final Copy (1)'}
      ]
    },
    {
      name: 'Right Panel',
      id: 'right',
      children: [
        {id: 2, name: 'index.ts'},
        {id: 3, name: 'package.json'},
        {id: 4, name: 'license.txt'}
      ]
    }
  ];

  return (
    <MenuButton
      label="Window"
      items={openWindows}
      selectionMode="multiple"
      selectedKeys={selected}
      onSelectionChange={setSelected}>
      {item => (
        <Section items={item.children} title={item.name}>
          {item => <Item>{item.name}</Item>}
        </Section>
      )}
    </MenuButton>
  );
}
```

```
import type {Selection} from 'react-stately';

function Example() {
  let [selected, setSelected] = React.useState<Selection>(
    new Set([1, 3])
  );
  let openWindows = [
    {
      name: 'Left Panel',
      id: 'left',
      children: [
        { id: 1, name: 'Final Copy (1)' }
      ]
    },
    {
      name: 'Right Panel',
      id: 'right',
      children: [
        { id: 2, name: 'index.ts' },
        { id: 3, name: 'package.json' },
        { id: 4, name: 'license.txt' }
      ]
    }
  ];

  return (
    <MenuButton
      label="Window"
      items={openWindows}
      selectionMode="multiple"
      selectedKeys={selected}
      onSelectionChange={setSelected}
    >
      {(item) => (
        <Section items={item.children} title={item.name}>
          {(item) => <Item>{item.name}</Item>}
        </Section>
      )}
    </MenuButton>
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
  >(new Set([1, 3]));
  let openWindows = [
    {
      name: 'Left Panel',
      id: 'left',
      children: [
        {
          id: 1,
          name:
            'Final Copy (1)'
        }
      ]
    },
    {
      name:
        'Right Panel',
      id: 'right',
      children: [
        {
          id: 2,
          name:
            'index.ts'
        },
        {
          id: 3,
          name:
            'package.json'
        },
        {
          id: 4,
          name:
            'license.txt'
        }
      ]
    }
  ];

  return (
    <MenuButton
      label="Window"
      items={openWindows}
      selectionMode="multiple"
      selectedKeys={selected}
      onSelectionChange={setSelected}
    >
      {(item) => (
        <Section
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
    </MenuButton>
  );
}
```

### Accessibility[#](#accessibility)

Sections without a `title` must provide an `aria-label` for accessibility.

## Complex menu items[#](#complex-menu-items)

---

By default, menu items that only contain text will be labeled by the contents of the item.
For items that have more complex content (e.g. icons, multiple lines of text, keyboard shortcuts, etc.),
use `labelProps`, `descriptionProps`, and `keyboardShortcutProps`
from `useMenuItem`
as needed to apply to the main text element of the menu item, its description, and keyboard
shortcut text. This improves screen reader announcement.

**NOTE: menu items cannot contain interactive content (e.g. buttons, checkboxes, etc.).**

To implement this, we'll update the `MenuItem` component to apply the ARIA properties
returned by `useMenuItem` to the appropriate
elements. In this example, we'll pull them out of `props.children` and use `React.cloneElement`
to apply the props, but you may want to use a more robust approach (e.g. context).

```
function MenuItem({item, state}) {
  // Get props for the menu item element and child elements
  let ref = React.useRef(null);
  let {
    menuItemProps,
    labelProps,
    descriptionProps,
    keyboardShortcutProps
  } = useMenuItem({key: item.key}, state, ref);

  // Pull out the three expected children. We will clone them
  // and add the necessary props for accessibility.
  let [title, description, shortcut] = item.rendered;

  return (
    <li {...menuItemProps} ref={ref}>
      <div>
        {React.cloneElement(title, labelProps)}
        {React.cloneElement(description, descriptionProps)}
      </div>
      {React.cloneElement(shortcut, keyboardShortcutProps)}
    </li>
  );
}

<MenuButton label="Actions" onAction={alert}>
  <Item textValue="Copy" key="copy">
    <div><strong>Copy</strong></div>
    <div>Copy the selected text</div>
    <kbd>âC</kbd>
  </Item>
  <Item textValue="Cut" key="cut">
    <div><strong>Cut</strong></div>
    <div>Cut the selected text</div>
    <kbd>âX</kbd>
  </Item>
  <Item textValue="Paste" key="paste">
    <div><strong>Paste</strong></div>
    <div>Paste the copied text</div>
    <kbd>âV</kbd>
  </Item>
</MenuButton>
```

```
function MenuItem({ item, state }) {
  // Get props for the menu item element and child elements
  let ref = React.useRef(null);
  let {
    menuItemProps,
    labelProps,
    descriptionProps,
    keyboardShortcutProps
  } = useMenuItem({ key: item.key }, state, ref);

  // Pull out the three expected children. We will clone them
  // and add the necessary props for accessibility.
  let [title, description, shortcut] = item.rendered;

  return (
    <li {...menuItemProps} ref={ref}>
      <div>
        {React.cloneElement(title, labelProps)}
        {React.cloneElement(description, descriptionProps)}
      </div>
      {React.cloneElement(shortcut, keyboardShortcutProps)}
    </li>
  );
}

<MenuButton label="Actions" onAction={alert}>
  <Item textValue="Copy" key="copy">
    <div>
      <strong>Copy</strong>
    </div>
    <div>Copy the selected text</div>
    <kbd>âC</kbd>
  </Item>
  <Item textValue="Cut" key="cut">
    <div>
      <strong>Cut</strong>
    </div>
    <div>Cut the selected text</div>
    <kbd>âX</kbd>
  </Item>
  <Item textValue="Paste" key="paste">
    <div>
      <strong>Paste</strong>
    </div>
    <div>Paste the copied text</div>
    <kbd>âV</kbd>
  </Item>
</MenuButton>
```

```
function MenuItem(
  { item, state }
) {
  // Get props for the menu item element and child elements
  let ref = React.useRef(
    null
  );
  let {
    menuItemProps,
    labelProps,
    descriptionProps,
    keyboardShortcutProps
  } = useMenuItem(
    { key: item.key },
    state,
    ref
  );

  // Pull out the three expected children. We will clone them
  // and add the necessary props for accessibility.
  let [
    title,
    description,
    shortcut
  ] = item.rendered;

  return (
    <li
      {...menuItemProps}
      ref={ref}
    >
      <div>
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
      </div>
      {React
        .cloneElement(
          shortcut,
          keyboardShortcutProps
        )}
    </li>
  );
}

<MenuButton
  label="Actions"
  onAction={alert}
>
  <Item
    textValue="Copy"
    key="copy"
  >
    <div>
      <strong>
        Copy
      </strong>
    </div>
    <div>
      Copy the selected
      text
    </div>
    <kbd>âC</kbd>
  </Item>
  <Item
    textValue="Cut"
    key="cut"
  >
    <div>
      <strong>
        Cut
      </strong>
    </div>
    <div>
      Cut the selected
      text
    </div>
    <kbd>âX</kbd>
  </Item>
  <Item
    textValue="Paste"
    key="paste"
  >
    <div>
      <strong>
        Paste
      </strong>
    </div>
    <div>
      Paste the copied
      text
    </div>
    <kbd>âV</kbd>
  </Item>
</MenuButton>
```

## Disabled items[#](#disabled-items)

---

`useMenu` supports marking items as disabled using the `disabledKeys` prop. Each key in this list
corresponds with the `key` prop passed to the `Item` component, or automatically derived from the values passed
to the `items` prop. See [Collections](https://react-spectrum.adobe.com/v3/collections.html) for more details.

Disabled items are not focusable or keyboard navigable, and do not trigger `onAction` or `onSelectionChange`.
The `isDisabled` property returned by `useMenuItem` can be used to style the item appropriately.

```
<MenuButton label="Actions" onAction={alert} disabledKeys={['paste']}>
  <Item key="copy">Copy</Item>
  <Item key="cut">Cut</Item>
  <Item key="paste">Paste</Item>
</MenuButton>
```

```
<MenuButton
  label="Actions"
  onAction={alert}
  disabledKeys={['paste']}
>
  <Item key="copy">Copy</Item>
  <Item key="cut">Cut</Item>
  <Item key="paste">Paste</Item>
</MenuButton>
```

```
<MenuButton
  label="Actions"
  onAction={alert}
  disabledKeys={[
    'paste'
  ]}
>
  <Item key="copy">
    Copy
  </Item>
  <Item key="cut">
    Cut
  </Item>
  <Item key="paste">
    Paste
  </Item>
</MenuButton>
```

## Links[#](#links)

---

By default, interacting with an item in a Menu triggers `onAction` and optionally `onSelectionChange` depending on the `selectionMode`. Alternatively, items may be links to another page or website. This can be achieved by passing the `href` prop to the `<Item>` component. Link items in a menu are not selectable.

This example shows how to update the `MenuItem` component with support for rendering an `<a>` element if an `href` prop is passed to the item. Note that you'll also need to render the `Menu` as a `<div>` instead of a `<ul>`, since an `<a>` inside a `<ul>` is not valid HTML.

```
function MenuItem({item, state}) {
  // Get props for the menu item element and child elements
  let ref = React.useRef(null);
  let {menuItemProps} = useMenuItem({key: item.key}, state, ref);
  let ElementType: React.ElementType = item.props.href ? 'a' : 'div';
  return (
    <ElementType {...menuItemProps} ref={ref}>
      {item.rendered}
    </ElementType>
  );
}

<MenuButton label="Links">
  <Item href="https://adobe.com/" target="_blank">Adobe</Item>
  <Item href="https://apple.com/" target="_blank">Apple</Item>
  <Item href="https://google.com/" target="_blank">Google</Item>
  <Item href="https://microsoft.com/" target="_blank">Microsoft</Item>
</MenuButton>
```

```
function MenuItem({ item, state }) {
  // Get props for the menu item element and child elements
  let ref = React.useRef(null);
  let { menuItemProps } = useMenuItem(
    { key: item.key },
    state,
    ref
  );
  let ElementType: React.ElementType = item.props.href
    ? 'a'
    : 'div';
  return (
    <ElementType {...menuItemProps} ref={ref}>
      {item.rendered}
    </ElementType>
  );
}

<MenuButton label="Links">
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
</MenuButton>
```

```
function MenuItem(
  { item, state }
) {
  // Get props for the menu item element and child elements
  let ref = React.useRef(
    null
  );
  let { menuItemProps } =
    useMenuItem(
      { key: item.key },
      state,
      ref
    );
  let ElementType:
    React.ElementType =
      item.props.href
        ? 'a'
        : 'div';
  return (
    <ElementType
      {...menuItemProps}
      ref={ref}
    >
      {item.rendered}
    </ElementType>
  );
}

<MenuButton label="Links">
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
</MenuButton>
```

### Client side routing[#](#client-side-routing)

The `<Item>` component works with frameworks and client side routers like [Next.js](https://nextjs.org/) and [React Router](https://reactrouter.com/en/main). As with other React Aria components that support links, this works via the `RouterProvider` component at the root of your app. See the [framework setup guide](../frameworks) to learn how to set this up.

## Controlled open state[#](#controlled-open-state)

---

The open state of the menu can be controlled via the `defaultOpen` and `isOpen` props

```
function Example() {
  let [open, setOpen] = React.useState(false);

  return (
    <>
      <p>Menu is {open ? 'open' : 'closed'}</p>
      <MenuButton
        label="View"
        isOpen={open}
        onOpenChange={setOpen}>
        <Item key="side">Side bar</Item>
        <Item key="options">Page options</Item>
        <Item key="edit">Edit Panel</Item>
      </MenuButton>
    </>
  );
}
```

```
function Example() {
  let [open, setOpen] = React.useState(false);

  return (
    <>
      <p>Menu is {open ? 'open' : 'closed'}</p>
      <MenuButton
        label="View"
        isOpen={open}
        onOpenChange={setOpen}>
        <Item key="side">Side bar</Item>
        <Item key="options">Page options</Item>
        <Item key="edit">Edit Panel</Item>
      </MenuButton>
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
        Menu is {open
          ? 'open'
          : 'closed'}
      </p>
      <MenuButton
        label="View"
        isOpen={open}
        onOpenChange={setOpen}
      >
        <Item key="side">
          Side bar
        </Item>
        <Item key="options">
          Page options
        </Item>
        <Item key="edit">
          Edit Panel
        </Item>
      </MenuButton>
    </>
  );
}
```

## Internationalization[#](#internationalization)

---

`useMenu` handles some aspects of internationalization automatically.
For example, type to select is implemented with an
[Intl.Collator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Collator)
for internationalized string matching. You are responsible for localizing all menu item labels for
content that is passed into the menu.

### RTL[#](#rtl)

In right-to-left languages, the menu button should be mirrored. The arrow should be on the left,
and the label should be on the right. In addition, the content of menu items should
flip. Ensure that your CSS accounts for this.

| Name | Type | Description |
| --- | --- | --- |
| `type` | `'menu' |Â 'listbox'` | The type of menu that the menu trigger opens. |
| `isDisabled` | `boolean` | Whether menu trigger is disabled. |
| `trigger` | `MenuTriggerType` | How menu is triggered. |

`'press' |Â 'longPress'`

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `focusStrategy` | `FocusStrategy |Â null` | Controls which item will be auto focused when the menu opens. |
| `isOpen` | `boolean` | Whether the overlay is currently open. |

### Methods

| Method | Description |
| --- | --- |
| `open( (focusStrategy?: FocusStrategy |Â  |Â null )): void` | Opens the menu. |
| `toggle( (focusStrategy?: FocusStrategy |Â  |Â null )): void` | Toggles the menu. |
| `setOpen( (isOpen: boolean )): void` | Sets whether the overlay is open. |
| `close(): void` | Closes the overlay. |

`'first' |Â 'last'`

| Name | Type | Description |
| --- | --- | --- |
| `current` | `T` |  |

| Name | Type | Description |
| --- | --- | --- |
| `menuTriggerProps` | `AriaButtonProps` | Props for the menu trigger element. |
| `menuProps` | `AriaMenuOptions<T>` | Props for the menu. |

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

Any focusable element, including both HTML and SVG elements.

**Extends**: `Element, HTMLOrSVGElement`

`BaseEvent<ReactKeyboardEvent<any>>`

`SyntheticEvent &Â {

stopPropagation: () => void,

continuePropagation: () => void

}`

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `isVirtualized` | `boolean` | â | Whether the menu uses virtual scrolling. |
| `keyboardDelegate` | `KeyboardDelegate` | â | An optional keyboard delegate implementation for type to select, to override the default. |
| `shouldUseVirtualFocus` | `boolean` | â | Whether the menu items should use virtual focus instead of being focused directly. |
| `escapeKeyBehavior` | `'clearSelection' |Â 'none'` | `'clearSelection'` | Whether pressing the escape key should clear selection in the menu or not.  Most experiences should not modify this option as it eliminates a keyboard user's ability to easily clear selection. Only use if the escape key is being handled externally or should not trigger selection clearing contextually. |
| `autoFocus` | `boolean |Â FocusStrategy` | â | Where the focus should be set. |
| `shouldFocusWrap` | `boolean` | â | Whether keyboard navigation is circular. |
| `onAction` | `( (key: Key )) => void` | â | Handler that is called when an item is selected. |
| `onClose` | `() => void` | â | Handler that is called when the menu should close after selecting an item. |
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
| `onKeyDown` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is pressed. |
| `onKeyUp` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is released. |

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

`'none'
|Â 'single'
|Â 'multiple'`

`'all' |Â Set<Key>`

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
| `menuProps` | `DOMAttributes` | Props for the menu element. |

All DOM attributes supported across both HTML and SVG elements.

**Extends**: `AriaAttributes, ReactDOMAttributes`

| Name | Type | Description |
| --- | --- | --- |
| `id` | `string |Â undefined` |  |
| `role` | `AriaRole |Â undefined` |  |
| `tabIndex` | `number |Â undefined` |  |
| `style` | `CSSProperties |Â undefined` |  |
| `className` | `string |Â undefined` |  |

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `key` | `Key` | â | The unique key for the menu item. |
| `aria-label` | `string` | â | A screen reader only label for the menu item. |
| `closeOnSelect` | `boolean` | `true` | Whether the menu should close when the menu item is selected. |
| `isVirtualized` | `boolean` | â | Whether the menu item is contained in a virtual scrolling menu. |
| `aria-haspopup` | `'menu' |Â 'dialog'` | â | What kind of popup the item opens. |
| `aria-expanded` | `boolean |Â 'true' |Â 'false'` | â | Indicates whether the menu item's popup element is expanded or collapsed. |
| `aria-controls` | `string` | â | Identifies the menu item's popup element whose contents or presence is controlled by the menu item. |
| `selectionManager` | `SelectionManager` | â | Override of the selection manager. By default, `state.selectionManager` is used. |
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `onPress` | `( (e: PressEvent )) => void` | â | Handler that is called when the press is released over the target. |
| `onPressStart` | `( (e: PressEvent )) => void` | â | Handler that is called when a press interaction starts. |
| `onPressEnd` | `( (e: PressEvent )) => void` | â | Handler that is called when a press interaction ends, either over the target or when the pointer leaves the target. |
| `onPressChange` | `( (isPressed: boolean )) => void` | â | Handler that is called when the press state changes. |
| `onPressUp` | `( (e: PressEvent )) => void` | â | Handler that is called when a press is released over the target, regardless of whether it started on the target or not. |
| `onClick` | `( (e: MouseEvent<FocusableElement> )) => void` | â | **Not recommended â use `onPress` instead.** `onClick` is an alias for `onPress` provided for compatibility with other libraries. `onPress` provides additional event details for non-mouse interactions. |
| `onHoverStart` | `( (e: HoverEvent )) => void` | â | Handler that is called when a hover interaction starts. |
| `onHoverEnd` | `( (e: HoverEvent )) => void` | â | Handler that is called when a hover interaction ends. |
| `onHoverChange` | `( (isHovering: boolean )) => void` | â | Handler that is called when the hover state changes. |
| `onKeyDown` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is pressed. |
| `onKeyUp` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is released. |
| `onFocus` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | â | Handler that is called when the element's focus status changes. |

| Name | Type | Description |
| --- | --- | --- |
| `type` | `'hoverstart' |Â 'hoverend'` | The type of hover event being fired. |
| `pointerType` | `'mouse' |Â 'pen'` | The pointer type that triggered the hover event. |
| `target` | `HTMLElement` | The target element of the hover event. |

| Name | Type | Description |
| --- | --- | --- |
| `menuItemProps` | `DOMAttributes` | Props for the menu item element. |
| `labelProps` | `DOMAttributes` | Props for the main text element inside the menu item. |
| `descriptionProps` | `DOMAttributes` | Props for the description text element inside the menu item, if any. |
| `keyboardShortcutProps` | `DOMAttributes` | Props for the keyboard shortcut text element inside the item, if any. |
| `isFocused` | `boolean` | Whether the item is currently focused. |
| `isFocusVisible` | `boolean` | Whether the item is keyboard focused. |
| `isSelected` | `boolean` | Whether the item is currently selected. |
| `isPressed` | `boolean` | Whether the item is currently in a pressed state. |
| `isDisabled` | `boolean` | Whether the item is disabled. |

| Name | Type | Description |
| --- | --- | --- |
| `heading` | `ReactNode` | The heading for the section. |
| `aria-label` | `string` | An accessibility label for the section. Required if `heading` is not present. |

| Name | Type | Description |
| --- | --- | --- |
| `itemProps` | `DOMAttributes` | Props for the wrapper list item. |
| `headingProps` | `DOMAttributes` | Props for the heading element, if any. |
| `groupProps` | `DOMAttributes` | Props for the group element. |

Manages state for a menu trigger. Tracks whether the menu is currently open,
and controls which item will receive focus when it opens. Also tracks the open submenus within
the menu tree via their trigger keys.

`useMenuTriggerState(
(props: MenuTriggerProps
)): RootMenuTriggerState`

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `trigger` | `MenuTriggerType` | `'press'` | How the menu is triggered. |
| `isOpen` | `boolean` | â | Whether the overlay is open by default (controlled). |
| `defaultOpen` | `boolean` | â | Whether the overlay is open by default (uncontrolled). |
| `onOpenChange` | `( (isOpen: boolean )) => void` | â | Handler that is called when the overlay's open state changes. |

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `openSubmenu` | `( (triggerKey: Key, , level: number )) => void` | Opens a specific submenu tied to a specific menu item at a specific level. |
| `closeSubmenu` | `( (triggerKey: Key, , level: number )) => void` | Closes a specific submenu tied to a specific menu item at a specific level. |
| `expandedKeysStack` | `Key[]` | An array of open submenu trigger keys within the menu tree. The index of key within array matches the submenu level in the tree. |
| `close` | `() => void` | Closes the menu and all submenus in the menu tree. |
| `focusStrategy` | `FocusStrategy |Â null` | Controls which item will be auto focused when the menu opens. |
| `isOpen` | `boolean` | Whether the overlay is currently open. |

### Methods

| Method | Description |
| --- | --- |
| `open( (focusStrategy?: FocusStrategy |Â  |Â null )): void` | Opens the menu. |
| `toggle( (focusStrategy?: FocusStrategy |Â  |Â null )): void` | Toggles the menu. |
| `setOpen( (isOpen: boolean )): void` | Sets whether the overlay is open. |

Provides state management for tree-like components. Handles building a collection
of items from props, item expanded state, and manages multiple selection state.

`useTreeState<T extends object>(
(props: TreeProps<T>
)): TreeState<T>`

| Name | Type | Description |
| --- | --- | --- |
| `disabledBehavior` | `DisabledBehavior` | Whether `disabledKeys` applies to all interactions, or only selection. |
| `collection` | `Collection<Node<T>>` | A pre-constructed collection to use instead of building one from items and children. |
| `expandedKeys` | `Iterable<Key>` | The currently expanded keys in the collection (controlled). |
| `defaultExpandedKeys` | `Iterable<Key>` | The initial expanded keys in the collection (uncontrolled). |
| `onExpandedChange` | `( (keys: Set<Key> )) => any` | Handler that is called when items are expanded or collapsed. |
| `selectionMode` | `SelectionMode` | The type of selection that is allowed in the collection. |
| `disallowEmptySelection` | `boolean` | Whether the collection allows empty selection. |
| `selectedKeys` | `'all' |Â Iterable<Key>` | The currently selected keys in the collection (controlled). |
| `defaultSelectedKeys` | `'all' |Â Iterable<Key>` | The initial selected keys in the collection (uncontrolled). |
| `onSelectionChange` | `( (keys: Selection )) => void` | Handler that is called when the selection changes. |
| `disabledKeys` | `Iterable<Key>` | The currently disabled keys in the collection (controlled). |

Provides the behavior and accessibility implementation for a menu trigger.

`useMenuTrigger<T>(
props: AriaMenuTriggerProps,
state: MenuTriggerState,
ref: RefObject<Element
|Â  |Â null>
): MenuTriggerAria<T>`

Provides the behavior and accessibility implementation for a menu component.
A menu displays a list of actions or options that a user can choose.

`useMenu<T>(
props: AriaMenuOptions<T>,
state: TreeState<T>,
ref: RefObject<HTMLElement
|Â  |Â null>
): MenuAria`

Provides the behavior and accessibility implementation for an item in a menu.
See `useMenu` for more details about menus.

`useMenuItem<T>(
props: AriaMenuItemProps,
state: TreeState<T>,
ref: RefObject<FocusableElement
|Â  |Â null>
): MenuItemAria`

Provides the behavior and accessibility implementation for a section in a menu.
See `useMenu` for more details about menus.

`useMenuSection(
(props: AriaMenuSectionProps
)): MenuSectionAria`

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