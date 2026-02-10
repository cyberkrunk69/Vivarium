# useTagGroup

Source: https://react-spectrum.adobe.com/react-aria/useTagGroup.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../TagGroup).

# useTagGroup

Provides the behavior and accessibility implementation for a tag group component.
A tag group is a focusable list of labels, categories, keywords, filters, or other items, with support for keyboard navigation, selection, and removal.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useTagGroup} from 'react-aria'` |

[View ARIA pattern

W3C](https://www.w3.org/WAI/ARIA/apg/patterns/grid/ "View ARIA pattern")[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/tag "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/tag "View package")

## API[#](#api)

---

`useTagGroup<T>(
props: AriaTagGroupOptions<T>,
state: ListState<T>,
ref: RefObject<HTMLElement
|Â  |Â null>
): TagGroupAria`
`useTag<T>(
props: AriaTagProps<T>,
state: ListState<T>,
ref: RefObject<FocusableElement
|Â  |Â null>
): TagAria`

## Features[#](#features)

---

- Exposed to assistive technology as a grid using ARIA
- Keyboard navigation support including arrow keys, home/end, page up/down, and delete
- Keyboard focus management and cross browser normalization
- Labeling support for accessibility
- Support for mouse, touch, and keyboard interactions

## Anatomy[#](#anatomy)

---

A tag group consists of a list of tags.
If a visual label is not provided, then an `aria-label` or
`aria-labelledby` prop must be passed to identify the tag group to assistive technology.

Individual tags should include a visual label, and may optionally include icons or a remove button.

`useTagGroup` returns props for the group and its label, which you should spread
onto the appropriate element:

| Name | Type | Description |
| --- | --- | --- |
| `gridProps` | `DOMAttributes` | Props for the tag grouping element. |
| `labelProps` | `DOMAttributes` | Props for the tag group's visible label (if any). |
| `descriptionProps` | `DOMAttributes` | Props for the tag group description element, if any. |
| `errorMessageProps` | `DOMAttributes` | Props for the tag group error message element, if any. |

`useTag` returns props for an individual tag, along with states that you can use for styling:

| Name | Type | Description |
| --- | --- | --- |
| `rowProps` | `DOMAttributes` | Props for the tag row element. |
| `gridCellProps` | `DOMAttributes` | Props for the tag cell element. |
| `removeButtonProps` | `AriaButtonProps` | Props for the tag remove button. |
| `allowsRemoving` | `boolean` | Whether the tag can be removed. |
| `isPressed` | `boolean` | Whether the item is currently in a pressed state. |
| `isSelected` | `boolean` | Whether the item is currently selected. |
| `isFocused` | `boolean` | Whether the item is currently focused. |
| `isDisabled` | `boolean` | Whether the item is non-interactive, i.e. both selection and actions are disabled and the item may not be focused. Dependent on `disabledKeys` and `disabledBehavior`. |
| `allowsSelection` | `boolean` | Whether the item may be selected, dependent on `selectionMode`, `disabledKeys`, and `disabledBehavior`. |

In order to be correctly identified to assistive technologies and enable proper keyboard navigation, the tag group should use `gridProps` on its outer container.

Each individual tag should use `rowProps` on its outer container, and use `gridCellProps` on an inner container.

## Example[#](#example)

---

```
import type {ListState} from 'react-stately';
import type {AriaTagGroupProps, AriaTagProps} from 'react-aria';
import {Item, useListState} from 'react-stately';
import {useFocusRing, useTag, useTagGroup} from 'react-aria';

// Reuse the Button from your component library. See below for details.
import {Button} from 'your-component-library';

function TagGroup<T extends object>(props: AriaTagGroupProps<T>) {
  let { label, description, errorMessage } = props;
  let ref = React.useRef(null);

  let state = useListState(props);
  let {
    gridProps,
    labelProps,
    descriptionProps,
    errorMessageProps
  } = useTagGroup(props, state, ref);

  return (
    <div className="tag-group">
      <div {...labelProps}>{label}</div>
      <div {...gridProps} ref={ref}>
        {[...state.collection].map((item) => (
          <Tag
            key={item.key}
            item={item}
            state={state}
          />
        ))}
      </div>
      {description && (
        <div {...descriptionProps} className="description">
          {description}
        </div>
      )}
      {errorMessage && (
        <div {...errorMessageProps} className="error-message">
          {errorMessage}
        </div>
      )}
    </div>
  );
}

interface TagProps<T> extends AriaTagProps<T> {
  state: ListState<T>;
}

function Tag<T>(props: TagProps<T>) {
  let { item, state } = props;
  let ref = React.useRef(null);
  let { focusProps, isFocusVisible } = useFocusRing({ within: false });
  let { rowProps, gridCellProps, removeButtonProps, allowsRemoving } = useTag(
    props,
    state,
    ref
  );

  return (
    <div
      ref={ref}
      {...rowProps}
      {...focusProps}
      data-focus-visible={isFocusVisible}
    >
      <div {...gridCellProps}>
        {item.rendered}
        {allowsRemoving && <Button {...removeButtonProps}>â§</Button>}
      </div>
    </div>
  );
}

<TagGroup label="Categories">
  <Item key="news">News</Item>
  <Item key="travel">Travel</Item>
  <Item key="gaming">Gaming</Item>
  <Item key="shopping">Shopping</Item>
</TagGroup>
```

```
import type {ListState} from 'react-stately';
import type {
  AriaTagGroupProps,
  AriaTagProps
} from 'react-aria';
import {Item, useListState} from 'react-stately';
import {
  useFocusRing,
  useTag,
  useTagGroup
} from 'react-aria';

// Reuse the Button from your component library. See below for details.
import {Button} from 'your-component-library';

function TagGroup<T extends object>(
  props: AriaTagGroupProps<T>
) {
  let { label, description, errorMessage } = props;
  let ref = React.useRef(null);

  let state = useListState(props);
  let {
    gridProps,
    labelProps,
    descriptionProps,
    errorMessageProps
  } = useTagGroup(props, state, ref);

  return (
    <div className="tag-group">
      <div {...labelProps}>{label}</div>
      <div {...gridProps} ref={ref}>
        {[...state.collection].map((item) => (
          <Tag
            key={item.key}
            item={item}
            state={state}
          />
        ))}
      </div>
      {description && (
        <div {...descriptionProps} className="description">
          {description}
        </div>
      )}
      {errorMessage && (
        <div
          {...errorMessageProps}
          className="error-message"
        >
          {errorMessage}
        </div>
      )}
    </div>
  );
}

interface TagProps<T> extends AriaTagProps<T> {
  state: ListState<T>;
}

function Tag<T>(props: TagProps<T>) {
  let { item, state } = props;
  let ref = React.useRef(null);
  let { focusProps, isFocusVisible } = useFocusRing({
    within: false
  });
  let {
    rowProps,
    gridCellProps,
    removeButtonProps,
    allowsRemoving
  } = useTag(props, state, ref);

  return (
    <div
      ref={ref}
      {...rowProps}
      {...focusProps}
      data-focus-visible={isFocusVisible}
    >
      <div {...gridCellProps}>
        {item.rendered}
        {allowsRemoving && (
          <Button {...removeButtonProps}>â§</Button>
        )}
      </div>
    </div>
  );
}

<TagGroup label="Categories">
  <Item key="news">News</Item>
  <Item key="travel">Travel</Item>
  <Item key="gaming">Gaming</Item>
  <Item key="shopping">Shopping</Item>
</TagGroup>
```

```
import type {ListState} from 'react-stately';
import type {
  AriaTagGroupProps,
  AriaTagProps
} from 'react-aria';
import {
  Item,
  useListState
} from 'react-stately';
import {
  useFocusRing,
  useTag,
  useTagGroup
} from 'react-aria';

// Reuse the Button from your component library. See below for details.
import {Button} from 'your-component-library';

function TagGroup<
  T extends object
>(
  props:
    AriaTagGroupProps<T>
) {
  let {
    label,
    description,
    errorMessage
  } = props;
  let ref = React.useRef(
    null
  );

  let state =
    useListState(props);
  let {
    gridProps,
    labelProps,
    descriptionProps,
    errorMessageProps
  } = useTagGroup(
    props,
    state,
    ref
  );

  return (
    <div className="tag-group">
      <div
        {...labelProps}
      >
        {label}
      </div>
      <div
        {...gridProps}
        ref={ref}
      >
        {[
          ...state
            .collection
        ].map((item) => (
          <Tag
            key={item
              .key}
            item={item}
            state={state}
          />
        ))}
      </div>
      {description && (
        <div
          {...descriptionProps}
          className="description"
        >
          {description}
        </div>
      )}
      {errorMessage && (
        <div
          {...errorMessageProps}
          className="error-message"
        >
          {errorMessage}
        </div>
      )}
    </div>
  );
}

interface TagProps<T>
  extends
    AriaTagProps<T> {
  state: ListState<T>;
}

function Tag<T>(
  props: TagProps<T>
) {
  let { item, state } =
    props;
  let ref = React.useRef(
    null
  );
  let {
    focusProps,
    isFocusVisible
  } = useFocusRing({
    within: false
  });
  let {
    rowProps,
    gridCellProps,
    removeButtonProps,
    allowsRemoving
  } = useTag(
    props,
    state,
    ref
  );

  return (
    <div
      ref={ref}
      {...rowProps}
      {...focusProps}
      data-focus-visible={isFocusVisible}
    >
      <div
        {...gridCellProps}
      >
        {item.rendered}
        {allowsRemoving &&
          (
            <Button
              {...removeButtonProps}
            >
              â§
            </Button>
          )}
      </div>
    </div>
  );
}

<TagGroup label="Categories">
  <Item key="news">
    News
  </Item>
  <Item key="travel">
    Travel
  </Item>
  <Item key="gaming">
    Gaming
  </Item>
  <Item key="shopping">
    Shopping
  </Item>
</TagGroup>
```

 Show CSS

```
.tag-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.tag-group [role="grid"] {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.tag-group [role="row"] {
  border: 1px solid gray;
  forced-color-adjust: none;
  border-radius: 4px;
  padding: 2px 8px;
  font-size: 0.929rem;
  outline: none;
  cursor: default;
  display: flex;
  align-items: center;
  transition: border-color 200ms;

  &[data-focus-visible=true] {
    outline: 2px solid slateblue;
    outline-offset: 2px;
  }

  &[aria-selected=true] {
    background: var(--spectrum-gray-900);
    border-color: var(--spectrum-gray-900);
    color: var(--spectrum-gray-50);
  }

  &[aria-disabled] {
    opacity: 0.4;
  }
}

.tag-group [role="gridcell"] {
  display: contents;
}

.tag-group [role="row"] button {
  background: none;
  border: none;
  padding: 0;
  margin-left: 4px;
  outline: none;
  font-size: 0.95em;
  border-radius: 100%;
  aspect-ratio: 1/1;
  height: 100%;

  &[data-focus-visible=true] {
    outline: 2px solid slateblue;
    outline-offset: -1px;
  }
}

.tag-group .description {
  font-size: 12px;
}

.tag-group .error-message {
  color: red;
  font-size: 12px;
}
```

```
.tag-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.tag-group [role="grid"] {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.tag-group [role="row"] {
  border: 1px solid gray;
  forced-color-adjust: none;
  border-radius: 4px;
  padding: 2px 8px;
  font-size: 0.929rem;
  outline: none;
  cursor: default;
  display: flex;
  align-items: center;
  transition: border-color 200ms;

  &[data-focus-visible=true] {
    outline: 2px solid slateblue;
    outline-offset: 2px;
  }

  &[aria-selected=true] {
    background: var(--spectrum-gray-900);
    border-color: var(--spectrum-gray-900);
    color: var(--spectrum-gray-50);
  }

  &[aria-disabled] {
    opacity: 0.4;
  }
}

.tag-group [role="gridcell"] {
  display: contents;
}

.tag-group [role="row"] button {
  background: none;
  border: none;
  padding: 0;
  margin-left: 4px;
  outline: none;
  font-size: 0.95em;
  border-radius: 100%;
  aspect-ratio: 1/1;
  height: 100%;

  &[data-focus-visible=true] {
    outline: 2px solid slateblue;
    outline-offset: -1px;
  }
}

.tag-group .description {
  font-size: 12px;
}

.tag-group .error-message {
  color: red;
  font-size: 12px;
}
```

```
.tag-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.tag-group [role="grid"] {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.tag-group [role="row"] {
  border: 1px solid gray;
  forced-color-adjust: none;
  border-radius: 4px;
  padding: 2px 8px;
  font-size: 0.929rem;
  outline: none;
  cursor: default;
  display: flex;
  align-items: center;
  transition: border-color 200ms;

  &[data-focus-visible=true] {
    outline: 2px solid slateblue;
    outline-offset: 2px;
  }

  &[aria-selected=true] {
    background: var(--spectrum-gray-900);
    border-color: var(--spectrum-gray-900);
    color: var(--spectrum-gray-50);
  }

  &[aria-disabled] {
    opacity: 0.4;
  }
}

.tag-group [role="gridcell"] {
  display: contents;
}

.tag-group [role="row"] button {
  background: none;
  border: none;
  padding: 0;
  margin-left: 4px;
  outline: none;
  font-size: 0.95em;
  border-radius: 100%;
  aspect-ratio: 1/1;
  height: 100%;

  &[data-focus-visible=true] {
    outline: 2px solid slateblue;
    outline-offset: -1px;
  }
}

.tag-group .description {
  font-size: 12px;
}

.tag-group .error-message {
  color: red;
  font-size: 12px;
}
```

### Button[#](#button)

The `Button` component is used in the above example to remove a tag. It is built using the [useButton](../Button/useButton.html) hook, and can be shared with many other components.

 Show code

```
import {mergeProps, useButton} from 'react-aria';

function Button(props) {
  let ref = React.useRef(null);
  let { buttonProps } = useButton(props, ref);
  let { focusProps, isFocusVisible } = useFocusRing({ within: false });
  return (
    <button
      {...mergeProps(buttonProps, focusProps)}
      ref={ref}
      data-focus-visible={isFocusVisible}
    >
      {props.children}
    </button>
  );
}
```

```
import {mergeProps, useButton} from 'react-aria';

function Button(props) {
  let ref = React.useRef(null);
  let { buttonProps } = useButton(props, ref);
  let { focusProps, isFocusVisible } = useFocusRing({
    within: false
  });
  return (
    <button
      {...mergeProps(buttonProps, focusProps)}
      ref={ref}
      data-focus-visible={isFocusVisible}
    >
      {props.children}
    </button>
  );
}
```

```
import {
  mergeProps,
  useButton
} from 'react-aria';

function Button(props) {
  let ref = React.useRef(
    null
  );
  let { buttonProps } =
    useButton(
      props,
      ref
    );
  let {
    focusProps,
    isFocusVisible
  } = useFocusRing({
    within: false
  });
  return (
    <button
      {...mergeProps(
        buttonProps,
        focusProps
      )}
      ref={ref}
      data-focus-visible={isFocusVisible}
    >
      {props.children}
    </button>
  );
}
```

## Styled examples[#](#styled-examples)

---

[![](/tailwind.8c98c56d.png)

Tailwind CSS

A TagGroup built with Tailwind.](https://codesandbox.io/s/usetaggroup-with-tailwind-css-zxxrpv)

## Usage[#](#usage)

---

### Remove tags[#](#remove-tags)

The `onRemove` prop can be used to include a remove button which can be used to remove a tag. This allows the user to press the remove button, or press the backspace key while the tag is focused to remove the tag from the group. Additionally, when [selection](#selection) is enabled, all selected items will be deleted when pressing the backspace key on a selected tag.

```
import {useListData} from 'react-stately';

function Example() {
  let list = useListData({
    initialItems: [
      { id: 1, name: 'News' },
      { id: 2, name: 'Travel' },
      { id: 3, name: 'Gaming' },
      { id: 4, name: 'Shopping' }
    ]
  });

  return (
    <TagGroup
      label="Categories"
      items={list.items}
      onRemove={(keys) => list.remove(...keys)}
    >
      {(item) => <Item>{item.name}</Item>}
    </TagGroup>
  );
}
```

```
import {useListData} from 'react-stately';

function Example() {
  let list = useListData({
    initialItems: [
      { id: 1, name: 'News' },
      { id: 2, name: 'Travel' },
      { id: 3, name: 'Gaming' },
      { id: 4, name: 'Shopping' }
    ]
  });

  return (
    <TagGroup
      label="Categories"
      items={list.items}
      onRemove={(keys) => list.remove(...keys)}
    >
      {(item) => <Item>{item.name}</Item>}
    </TagGroup>
  );
}
```

```
import {useListData} from 'react-stately';

function Example() {
  let list = useListData(
    {
      initialItems: [
        {
          id: 1,
          name: 'News'
        },
        {
          id: 2,
          name: 'Travel'
        },
        {
          id: 3,
          name: 'Gaming'
        },
        {
          id: 4,
          name:
            'Shopping'
        }
      ]
    }
  );

  return (
    <TagGroup
      label="Categories"
      items={list.items}
      onRemove={(keys) =>
        list.remove(
          ...keys
        )}
    >
      {(item) => (
        <Item>
          {item.name}
        </Item>
      )}
    </TagGroup>
  );
}
```

### Selection[#](#selection)

TagGroup supports multiple selection modes. By default, selection is disabled, however this can be changed using the `selectionMode` prop.
Use `defaultSelectedKeys` to provide a default set of selected items (uncontrolled) and `selectedKeys` to set the selected items (controlled). The value of the selected keys must match the `key` prop of the items.
See the `react-stately` [Selection docs](https://react-spectrum.adobe.com/v3/selection.html) for more details.

```
import type {Selection} from 'react-stately';

function Example() {
  let [selected, setSelected] = React.useState<Selection>(new Set(['parking']));

  return (
    <>
      <TagGroup
        label="Amenities"
        selectionMode="multiple"
        selectedKeys={selected}
        onSelectionChange={setSelected}
      >
        <Item key="laundry">Laundry</Item>
        <Item key="fitness">Fitness center</Item>
        <Item key="parking">Parking</Item>
        <Item key="pool">Swimming pool</Item>
        <Item key="breakfast">Breakfast</Item>
      </TagGroup>
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
    new Set(['parking'])
  );

  return (
    <>
      <TagGroup
        label="Amenities"
        selectionMode="multiple"
        selectedKeys={selected}
        onSelectionChange={setSelected}
      >
        <Item key="laundry">Laundry</Item>
        <Item key="fitness">Fitness center</Item>
        <Item key="parking">Parking</Item>
        <Item key="pool">Swimming pool</Item>
        <Item key="breakfast">Breakfast</Item>
      </TagGroup>
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
    new Set(['parking'])
  );

  return (
    <>
      <TagGroup
        label="Amenities"
        selectionMode="multiple"
        selectedKeys={selected}
        onSelectionChange={setSelected}
      >
        <Item key="laundry">
          Laundry
        </Item>
        <Item key="fitness">
          Fitness center
        </Item>
        <Item key="parking">
          Parking
        </Item>
        <Item key="pool">
          Swimming pool
        </Item>
        <Item key="breakfast">
          Breakfast
        </Item>
      </TagGroup>
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

### Links[#](#links)

Tags may be links to another page or website. This can be achieved by passing the `href` prop to the `<Item>` component. Tags with an `href` are not selectable.

```
<TagGroup label="Links">
  <Item href="https://adobe.com/" target="_blank">Adobe</Item>
  <Item href="https://apple.com/" target="_blank">Apple</Item>
  <Item href="https://google.com/" target="_blank">Google</Item>
  <Item href="https://microsoft.com/" target="_blank">Microsoft</Item>
</TagGroup>
```

```
<TagGroup label="Links">
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
</TagGroup>
```

```
<TagGroup label="Links">
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
</TagGroup>
```

#### Client side routing[#](#client-side-routing)

The `<Item>` component works with frameworks and client side routers like [Next.js](https://nextjs.org/) and [React Router](https://reactrouter.com/en/main). As with other React Aria components that support links, this works via the `RouterProvider` component at the root of your app. See the [framework setup guide](../frameworks) to learn how to set this up.

### Disabled tags[#](#disabled-tags)

TagGroup supports marking items as disabled using the `disabledKeys` prop. Each key in this list
corresponds with the `key` prop passed to the `Item` component, or automatically derived from the values passed
to the `items` prop. Disabled items are not focusable, selectable, or keyboard navigable.
See [Collections](https://react-spectrum.adobe.com/v3/collections.html) for more details.

```
<TagGroup
  label="Sandwich contents"
  selectionMode="multiple"
  disabledKeys={['tuna']}
>
  <Item key="lettuce">Lettuce</Item>
  <Item key="tomato">Tomato</Item>
  <Item key="cheese">Cheese</Item>
  <Item key="tuna">Tuna Salad</Item>
  <Item key="egg">Egg Salad</Item>
  <Item key="ham">Ham</Item>
</TagGroup>
```

```
<TagGroup
  label="Sandwich contents"
  selectionMode="multiple"
  disabledKeys={['tuna']}
>
  <Item key="lettuce">Lettuce</Item>
  <Item key="tomato">Tomato</Item>
  <Item key="cheese">Cheese</Item>
  <Item key="tuna">Tuna Salad</Item>
  <Item key="egg">Egg Salad</Item>
  <Item key="ham">Ham</Item>
</TagGroup>
```

```
<TagGroup
  label="Sandwich contents"
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
</TagGroup>
```

### Description[#](#description)

The `description` prop can be used to associate additional help text with a tag group.

```
<TagGroup label="Categories" description="Your selected categories.">
  <Item key="news">News</Item>
  <Item key="travel">Travel</Item>
  <Item key="gaming">Gaming</Item>
  <Item key="shopping">Shopping</Item>
</TagGroup>
```

```
<TagGroup
  label="Categories"
  description="Your selected categories."
>
  <Item key="news">News</Item>
  <Item key="travel">Travel</Item>
  <Item key="gaming">Gaming</Item>
  <Item key="shopping">Shopping</Item>
</TagGroup>
```

```
<TagGroup
  label="Categories"
  description="Your selected categories."
>
  <Item key="news">
    News
  </Item>
  <Item key="travel">
    Travel
  </Item>
  <Item key="gaming">
    Gaming
  </Item>
  <Item key="shopping">
    Shopping
  </Item>
</TagGroup>
```

### Error message[#](#error-message)

The `errorMessage` prop can be used to help the user fix a validation error.

```
<TagGroup label="Categories" errorMessage="Invalid set of categories.">
  <Item key="news">News</Item>
  <Item key="travel">Travel</Item>
  <Item key="gaming">Gaming</Item>
  <Item key="shopping">Shopping</Item>
</TagGroup>
```

```
<TagGroup
  label="Categories"
  errorMessage="Invalid set of categories."
>
  <Item key="news">News</Item>
  <Item key="travel">Travel</Item>
  <Item key="gaming">Gaming</Item>
  <Item key="shopping">Shopping</Item>
</TagGroup>
```

```
<TagGroup
  label="Categories"
  errorMessage="Invalid set of categories."
>
  <Item key="news">
    News
  </Item>
  <Item key="travel">
    Travel
  </Item>
  <Item key="gaming">
    Gaming
  </Item>
  <Item key="shopping">
    Shopping
  </Item>
</TagGroup>
```

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `keyboardDelegate` | `KeyboardDelegate` | â | An optional keyboard delegate to handle arrow key navigation, to override the default. |
| `selectionBehavior` | `SelectionBehavior` | â | How multiple selection should behave in the collection. |
| `shouldSelectOnPressUp` | `boolean` | â | Whether selection should occur on press up instead of press down. |
| `onRemove` | `( (keys: Set<Key> )) => void` | â | Handler that is called when a user deletes a tag. |
| `errorMessage` | `ReactNode` | â | An error message for the field. |
| `escapeKeyBehavior` | `'clearSelection' |Â 'none'` | `'clearSelection'` | Whether pressing the escape key should clear selection in the TagGroup or not.  Most experiences should not modify this option as it eliminates a keyboard user's ability to easily clear selection. Only use if the escape key is being handled externally or should not trigger selection clearing contextually. |
| `items` | `Iterable<T>` | â | Item objects in the collection. |
| `disabledKeys` | `Iterable<Key>` | â | The item keys that are disabled. These items cannot be selected, focused, or otherwise interacted with. |
| `selectionMode` | `SelectionMode` | â | The type of selection that is allowed in the collection. |
| `disallowEmptySelection` | `boolean` | â | Whether the collection allows empty selection. |
| `selectedKeys` | `'all' |Â Iterable<Key>` | â | The currently selected keys in the collection (controlled). |
| `defaultSelectedKeys` | `'all' |Â Iterable<Key>` | â | The initial selected keys in the collection (uncontrolled). |
| `onSelectionChange` | `( (keys: Selection )) => void` | â | Handler that is called when the selection changes. |
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `label` | `ReactNode` | â | The content to display as the label. |
| `aria-label` | `string` | â | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |
| `description` | `ReactNode` | â | A description for the field. Provides a hint such as specific requirements for what to choose. |

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

`'toggle' |Â 'replace'`

`string |Â number`

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

`'first' |Â 'last'`

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
| `gridProps` | `DOMAttributes` | Props for the tag grouping element. |
| `labelProps` | `DOMAttributes` | Props for the tag group's visible label (if any). |
| `descriptionProps` | `DOMAttributes` | Props for the tag group description element, if any. |
| `errorMessageProps` | `DOMAttributes` | Props for the tag group error message element, if any. |

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
| `item` | `Node<T>` | An object representing the tag. Contains all the relevant information that makes up the tag. |

| Name | Type | Description |
| --- | --- | --- |
| `rowProps` | `DOMAttributes` | Props for the tag row element. |
| `gridCellProps` | `DOMAttributes` | Props for the tag cell element. |
| `removeButtonProps` | `AriaButtonProps` | Props for the tag remove button. |
| `allowsRemoving` | `boolean` | Whether the tag can be removed. |
| `isPressed` | `boolean` | Whether the item is currently in a pressed state. |
| `isSelected` | `boolean` | Whether the item is currently selected. |
| `isFocused` | `boolean` | Whether the item is currently focused. |
| `isDisabled` | `boolean` | Whether the item is non-interactive, i.e. both selection and actions are disabled and the item may not be focused. Dependent on `disabledKeys` and `disabledBehavior`. |
| `allowsSelection` | `boolean` | Whether the item may be selected, dependent on `selectionMode`, `disabledKeys`, and `disabledBehavior`. |

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

`BaseEvent<ReactKeyboardEvent<any>>`

`SyntheticEvent &Â {

stopPropagation: () => void,

continuePropagation: () => void

}`

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