# useBreadcrumbs

Source: https://react-spectrum.adobe.com/react-aria/useBreadcrumbs.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../Breadcrumbs).

# useBreadcrumbs

Provides the behavior and accessibility implementation for a breadcrumbs component.
Breadcrumbs display a hierarchy of links to the current page or resource in an application.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useBreadcrumbs, useBreadcrumbItem} from 'react-aria'` |

[View ARIA pattern

W3C](https://www.w3.org/WAI/ARIA/apg/patterns/breadcrumb/ "View ARIA pattern")[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/breadcrumbs "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/breadcrumbs "View package")

## API[#](#api)

---

`useBreadcrumbs(
(props: AriaBreadcrumbsProps
)): BreadcrumbsAria`
`useBreadcrumbItem(
(props: AriaBreadcrumbItemProps,
, ref: RefObject<FocusableElement
|Â  |Â null>
)): BreadcrumbItemAria`

## Features[#](#features)

---

Breadcrumbs provide a list of links to parent pages of the current page in hierarchical order.
`useBreadcrumbs` and `useBreadcrumbItem` help implement these in an accessible way.

- Support for mouse, touch, and keyboard interactions on breadcrumbs
- Support for navigation links via `<a>` elements or custom element types via ARIA
- Localized ARIA labeling support for landmark navigation region
- Support for disabled breadcrumbs

## Anatomy[#](#anatomy)

---

Breadcrumbs consist of a navigation landmark element and a list of links, typically with a visual separator
icon between each item. The last link represents the current page in the hierarchy, with the previous links representing the
parent pages of the current page. Each of these parent links can be clicked, tapped, or
triggered via the `Enter` key to navigate to that page.

`useBreadcrumbs` returns props to be spread onto the navigation element:

| Name | Type | Description |
| --- | --- | --- |
| `navProps` | `DOMAttributes` | Props for the breadcrumbs navigation element. |

`useBreadcrumbItem` returns props to spread onto the individual breadcrumb links:

| Name | Type | Description |
| --- | --- | --- |
| `itemProps` | `DOMAttributes` | Props for the breadcrumb item link element. |

## Example[#](#example)

---

This example displays a basic list of breadcrumbs using an HTML
[<nav>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/nav)
element, and a [<ol>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/ol)
for the list of links. Each link is a span because we are handling the interactions
locally via `onPress`. `useBreadcrumbItem` automatically handles exposing these
spans as links to assistive technology.

The chevrons between each link are rendered using a span with `aria-hidden="true"` so that
screen readers do not pick them up. You could also render them similarly using SVG icons,
CSS `:after`, or other techniques.

The last link is non-interactive since it represents the current page. This is
passed to the last breadcrumb item by cloning the element and adding the `isCurrent`
prop.

```
import {useBreadcrumbItem, useBreadcrumbs} from 'react-aria';

function Breadcrumbs(props) {
  let { navProps } = useBreadcrumbs(props);
  let childCount = React.Children.count(props.children);

  return (
    <nav {...navProps}>
      <ol style={{ display: 'flex', listStyle: 'none', margin: 0, padding: 0 }}>
        {React.Children.map(props.children, (child, i) =>
          React.cloneElement(child, { isCurrent: i === childCount - 1 }))}
      </ol>
    </nav>
  );
}

function BreadcrumbItem(props) {
  let ref = React.useRef(null);
  let { itemProps } = useBreadcrumbItem({ ...props, elementType: 'span' }, ref);
  return (
    <li>
      <span
        {...itemProps}
        ref={ref}
        style={{
          color: props.isDisabled ? 'var(--gray)' : 'var(--blue)',
          textDecoration: props.isCurrent || props.isDisabled
            ? 'none'
            : 'underline',
          fontWeight: props.isCurrent ? 'bold' : null,
          cursor: props.isCurrent || props.isDisabled ? 'default' : 'pointer'
        }}
      >
        {props.children}
      </span>
      {!props.isCurrent &&
        <span aria-hidden="true" style={{ padding: '0 5px' }}>{'âº'}</span>}
    </li>
  );
}

<Breadcrumbs>
  <BreadcrumbItem onPress={() => alert('Pressed Folder 1')}>
    Folder 1
  </BreadcrumbItem>
  <BreadcrumbItem onPress={() => alert('Pressed Folder 2')}>
    Folder 2
  </BreadcrumbItem>
  <BreadcrumbItem>Folder 3</BreadcrumbItem>
</Breadcrumbs>
```

```
import {
  useBreadcrumbItem,
  useBreadcrumbs
} from 'react-aria';

function Breadcrumbs(props) {
  let { navProps } = useBreadcrumbs(props);
  let childCount = React.Children.count(props.children);

  return (
    <nav {...navProps}>
      <ol
        style={{
          display: 'flex',
          listStyle: 'none',
          margin: 0,
          padding: 0
        }}
      >
        {React.Children.map(props.children, (child, i) =>
          React.cloneElement(child, {
            isCurrent: i === childCount - 1
          }))}
      </ol>
    </nav>
  );
}

function BreadcrumbItem(props) {
  let ref = React.useRef(null);
  let { itemProps } = useBreadcrumbItem({
    ...props,
    elementType: 'span'
  }, ref);
  return (
    <li>
      <span
        {...itemProps}
        ref={ref}
        style={{
          color: props.isDisabled
            ? 'var(--gray)'
            : 'var(--blue)',
          textDecoration:
            props.isCurrent || props.isDisabled
              ? 'none'
              : 'underline',
          fontWeight: props.isCurrent ? 'bold' : null,
          cursor: props.isCurrent || props.isDisabled
            ? 'default'
            : 'pointer'
        }}
      >
        {props.children}
      </span>
      {!props.isCurrent &&
        (
          <span
            aria-hidden="true"
            style={{ padding: '0 5px' }}
          >
            {'âº'}
          </span>
        )}
    </li>
  );
}

<Breadcrumbs>
  <BreadcrumbItem
    onPress={() => alert('Pressed Folder 1')}
  >
    Folder 1
  </BreadcrumbItem>
  <BreadcrumbItem
    onPress={() => alert('Pressed Folder 2')}
  >
    Folder 2
  </BreadcrumbItem>
  <BreadcrumbItem>Folder 3</BreadcrumbItem>
</Breadcrumbs>
```

```
import {
  useBreadcrumbItem,
  useBreadcrumbs
} from 'react-aria';

function Breadcrumbs(
  props
) {
  let { navProps } =
    useBreadcrumbs(
      props
    );
  let childCount = React
    .Children.count(
      props.children
    );

  return (
    <nav {...navProps}>
      <ol
        style={{
          display:
            'flex',
          listStyle:
            'none',
          margin: 0,
          padding: 0
        }}
      >
        {React.Children
          .map(
            props
              .children,
            (child, i) =>
              React
                .cloneElement(
                  child,
                  {
                    isCurrent:
                      i ===
                        childCount -
                          1
                  }
                )
          )}
      </ol>
    </nav>
  );
}

function BreadcrumbItem(
  props
) {
  let ref = React.useRef(
    null
  );
  let { itemProps } =
    useBreadcrumbItem({
      ...props,
      elementType: 'span'
    }, ref);
  return (
    <li>
      <span
        {...itemProps}
        ref={ref}
        style={{
          color:
            props
                .isDisabled
              ? 'var(--gray)'
              : 'var(--blue)',
          textDecoration:
            props
                .isCurrent ||
              props
                .isDisabled
              ? 'none'
              : 'underline',
          fontWeight:
            props
                .isCurrent
              ? 'bold'
              : null,
          cursor:
            props
                .isCurrent ||
              props
                .isDisabled
              ? 'default'
              : 'pointer'
        }}
      >
        {props.children}
      </span>
      {!props
        .isCurrent &&
        (
          <span
            aria-hidden="true"
            style={{
              padding:
                '0 5px'
            }}
          >
            {'âº'}
          </span>
        )}
    </li>
  );
}

<Breadcrumbs>
  <BreadcrumbItem
    onPress={() =>
      alert(
        'Pressed Folder 1'
      )}
  >
    Folder 1
  </BreadcrumbItem>
  <BreadcrumbItem
    onPress={() =>
      alert(
        'Pressed Folder 2'
      )}
  >
    Folder 2
  </BreadcrumbItem>
  <BreadcrumbItem>
    Folder 3
  </BreadcrumbItem>
</Breadcrumbs>
```

## Navigation links[#](#navigation-links)

---

To render breadcrumbs that navigate to other pages rather than handle events via `onPress`, use an `<a>` element
for each BreadcrumbItem. This is the default `elementType`, so the option can be omitted from `useBreadcrumbItem`.

```
function BreadcrumbItem(props) {
  let ref = React.useRef(null);
  let { itemProps } = useBreadcrumbItem(props, ref);
  return (
    <li>
      <a
        {...itemProps}
        ref={ref}
        href={props.href}
        style={{
          color: props.isDisabled ? 'var(--gray)' : 'var(--blue)',
          textDecoration: props.isCurrent || props.isDisabled
            ? 'none'
            : 'underline',
          fontWeight: props.isCurrent ? 'bold' : null,
          cursor: props.isCurrent || props.isDisabled ? 'default' : 'pointer'
        }}
      >
        {props.children}
      </a>
      {!props.isCurrent &&
        <span aria-hidden="true" style={{ padding: '0 5px' }}>{'âº'}</span>}
    </li>
  );
}

<Breadcrumbs>
  <BreadcrumbItem href="#">Home</BreadcrumbItem>
  <BreadcrumbItem href="#">React Aria</BreadcrumbItem>
  <BreadcrumbItem>useBreadcrumbs</BreadcrumbItem>
</Breadcrumbs>
```

```
function BreadcrumbItem(props) {
  let ref = React.useRef(null);
  let { itemProps } = useBreadcrumbItem(props, ref);
  return (
    <li>
      <a
        {...itemProps}
        ref={ref}
        href={props.href}
        style={{
          color: props.isDisabled
            ? 'var(--gray)'
            : 'var(--blue)',
          textDecoration:
            props.isCurrent || props.isDisabled
              ? 'none'
              : 'underline',
          fontWeight: props.isCurrent ? 'bold' : null,
          cursor: props.isCurrent || props.isDisabled
            ? 'default'
            : 'pointer'
        }}
      >
        {props.children}
      </a>
      {!props.isCurrent &&
        (
          <span
            aria-hidden="true"
            style={{ padding: '0 5px' }}
          >
            {'âº'}
          </span>
        )}
    </li>
  );
}

<Breadcrumbs>
  <BreadcrumbItem href="#">Home</BreadcrumbItem>
  <BreadcrumbItem href="#">React Aria</BreadcrumbItem>
  <BreadcrumbItem>useBreadcrumbs</BreadcrumbItem>
</Breadcrumbs>
```

```
function BreadcrumbItem(
  props
) {
  let ref = React.useRef(
    null
  );
  let { itemProps } =
    useBreadcrumbItem(
      props,
      ref
    );
  return (
    <li>
      <a
        {...itemProps}
        ref={ref}
        href={props.href}
        style={{
          color:
            props
                .isDisabled
              ? 'var(--gray)'
              : 'var(--blue)',
          textDecoration:
            props
                .isCurrent ||
              props
                .isDisabled
              ? 'none'
              : 'underline',
          fontWeight:
            props
                .isCurrent
              ? 'bold'
              : null,
          cursor:
            props
                .isCurrent ||
              props
                .isDisabled
              ? 'default'
              : 'pointer'
        }}
      >
        {props.children}
      </a>
      {!props
        .isCurrent &&
        (
          <span
            aria-hidden="true"
            style={{
              padding:
                '0 5px'
            }}
          >
            {'âº'}
          </span>
        )}
    </li>
  );
}

<Breadcrumbs>
  <BreadcrumbItem href="#">
    Home
  </BreadcrumbItem>
  <BreadcrumbItem href="#">
    React Aria
  </BreadcrumbItem>
  <BreadcrumbItem>
    useBreadcrumbs
  </BreadcrumbItem>
</Breadcrumbs>
```

## Usage[#](#usage)

---

The following examples show how to use the `Breadcrumbs` component created in the above examples.

### Disabled[#](#disabled)

Breadcrumbs can be disabled using the `isDisabled` prop, passed to each disabled BreadcrumbItem. This indicates that navigation is not currently available. When a breadcrumb is disabled, `onPress` will not be triggered, navigation will not occur, and links will be marked as `aria-disabled` for assistive technologies.

```
<Breadcrumbs>
  <BreadcrumbItem href="#" isDisabled>Home</BreadcrumbItem>
  <BreadcrumbItem href="#">React Aria</BreadcrumbItem>
  <BreadcrumbItem>useBreadcrumbs</BreadcrumbItem>
</Breadcrumbs>
```

```
<Breadcrumbs>
  <BreadcrumbItem href="#" isDisabled>Home</BreadcrumbItem>
  <BreadcrumbItem href="#">React Aria</BreadcrumbItem>
  <BreadcrumbItem>useBreadcrumbs</BreadcrumbItem>
</Breadcrumbs>
```

```
<Breadcrumbs>
  <BreadcrumbItem
    href="#"
    isDisabled
  >
    Home
  </BreadcrumbItem>
  <BreadcrumbItem href="#">
    React Aria
  </BreadcrumbItem>
  <BreadcrumbItem>
    useBreadcrumbs
  </BreadcrumbItem>
</Breadcrumbs>
```

| Name | Type | Description |
| --- | --- | --- |
| `id` | `string` | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `aria-label` | `string` | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | Identifies the element (or elements) that provide a detailed, extended description for the object. |

| Name | Type | Description |
| --- | --- | --- |
| `navProps` | `DOMAttributes` | Props for the breadcrumbs navigation element. |

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
| `children` | `ReactNode` | â | The contents of the breadcrumb item. |
| `elementType` | `string` | `'a'` | The HTML element used to render the breadcrumb link, e.g. 'a', or 'span'. |
| `isCurrent` | `boolean` | â | Whether the breadcrumb item represents the current page. |
| `aria-current` | `'page' |Â 'step' |Â 'location' |Â 'date' |Â 'time' |Â boolean |Â 'true' |Â 'false'` | `'page'` | The type of current location the breadcrumb item represents, if `isCurrent` is true. |
| `isDisabled` | `boolean` | â | Whether the breadcrumb item is disabled. |
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
| `href` | `Href` | â | A URL to link to. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a#href). |
| `hrefLang` | `string` | â | Hints at the human language of the linked URL. See[MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a#hreflang). |
| `target` | `HTMLAttributeAnchorTarget` | â | The target window for the link. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a#target). |
| `rel` | `string` | â | The relationship between the linked resource and the current page. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/rel). |
| `download` | `boolean |Â string` | â | Causes the browser to download the linked URL. A string may be provided to suggest a file name. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a#download). |
| `ping` | `string` | â | A space-separated list of URLs to ping when the link is followed. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a#ping). |
| `referrerPolicy` | `HTMLAttributeReferrerPolicy` | â | How much of the referrer to send when following the link. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a#referrerpolicy). |
| `routerOptions` | `RouterOptions` | â | Options for the configured client side router. |
| `aria-label` | `string` | â | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |

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

`BaseEvent<ReactKeyboardEvent<any>>`

`SyntheticEvent &Â {

stopPropagation: () => void,

continuePropagation: () => void

}`

`RouterConfig extends {

href: any

} ? H : string`

This type allows configuring link props with router options and type-safe URLs via TS module augmentation.
By default, this is an empty type. Extend with `href` and `routerOptions` properties to configure your router.

`RouterConfig extends {

routerOptions: any

} ? O : never`

| Name | Type | Description |
| --- | --- | --- |
| `current` | `T` |  |

| Name | Type | Description |
| --- | --- | --- |
| `itemProps` | `DOMAttributes` | Props for the breadcrumb item link element. |