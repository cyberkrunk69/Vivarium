# useLink

Source: https://react-spectrum.adobe.com/react-aria/useLink.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../Link).

# useLink

Provides the behavior and accessibility implementation for a link component.
A link allows a user to navigate to another page or resource within a web page
or application.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useLink} from 'react-aria'` |

[View ARIA pattern

W3C](https://www.w3.org/WAI/ARIA/apg/patterns/link/ "View ARIA pattern")[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/link "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/link "View package")

## API[#](#api)

---

`useLink(
(props: AriaLinkOptions,
, ref: RefObject<FocusableElement
|Â  |Â null>
)): LinkAria`

## Features[#](#features)

---

Links can be created in HTML with the [<a>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a)
element with an `href` attribute. However, if the link does not have an href, and is
handled client side with JavaScript instead, it will not be exposed to assistive technology properly.
`useLink` helps achieve accessible links with either native HTML elements or custom element types.

- Support for mouse, touch, and keyboard interactions
- Support for navigation links via `<a>` elements or custom element types via ARIA
- Support for disabled links

## Anatomy[#](#anatomy)

---

A link consists of a pressable area usually containing a textual label or an icon
that users can click or tap to navigate to another page or resource. In addition,
keyboard users may activate links using the `Enter` key.

`useLink` returns props to be spread onto the link element:

| Name | Type | Description |
| --- | --- | --- |
| `linkProps` | `DOMAttributes` | Props for the link element. |
| `isPressed` | `boolean` | Whether the link is currently pressed. |

If a visual label is not provided (e.g. an icon or image only link), then an `aria-label` or
`aria-labelledby` prop must be passed to identify the link to assistive technology.

## Example[#](#example)

---

This example shows a basic link using a native `<a>` element.

```
import {useLink} from 'react-aria';

function Link(props) {
  let ref = React.useRef(null);
  let { linkProps } = useLink(props, ref);

  return (
    <a
      {...linkProps}
      ref={ref}
      style={{ color: 'var(--blue)' }}
    >
      {props.children}
    </a>
  );
}

<Link href="https://adobe.com" target="_blank">Adobe</Link>
```

```
import {useLink} from 'react-aria';

function Link(props) {
  let ref = React.useRef(null);
  let { linkProps } = useLink(props, ref);

  return (
    <a
      {...linkProps}
      ref={ref}
      style={{ color: 'var(--blue)' }}
    >
      {props.children}
    </a>
  );
}

<Link href="https://adobe.com" target="_blank">
  Adobe
</Link>
```

```
import {useLink} from 'react-aria';

function Link(props) {
  let ref = React.useRef(
    null
  );
  let { linkProps } =
    useLink(props, ref);

  return (
    <a
      {...linkProps}
      ref={ref}
      style={{
        color:
          'var(--blue)'
      }}
    >
      {props.children}
    </a>
  );
}

<Link
  href="https://adobe.com"
  target="_blank"
>
  Adobe
</Link>
```

## Client handled links[#](#client-handled-links)

---

This example shows a client handled link using press events. It sets `elementType` to `span`
so that `useLink` returns the proper ARIA attributes to expose the element as a link to
assistive technology.

In addition, this example shows usage of the `isPressed` value returned by `useLink` to properly
style the links's active state. You could use the CSS `:active` pseudo class for this, but `isPressed`
properly handles when the user drags their pointer off of the link, along with keyboard support and better
touch screen support.

```
function Link(props) {
  let ref = React.useRef(null);
  let { linkProps, isPressed } = useLink(
    { ...props, elementType: 'span' },
    ref
  );

  return (
    <span
      {...linkProps}
      ref={ref}
      style={{
        color: isPressed
          ? 'var(--blue)'
          : 'var(--spectrum-global-color-blue-700)',
        textDecoration: 'underline',
        cursor: 'pointer'
      }}
    >
      {props.children}
    </span>
  );
}

<Link onPress={() => alert('Pressed link')}>Adobe</Link>
```

```
function Link(props) {
  let ref = React.useRef(null);
  let { linkProps, isPressed } = useLink(
    { ...props, elementType: 'span' },
    ref
  );

  return (
    <span
      {...linkProps}
      ref={ref}
      style={{
        color: isPressed
          ? 'var(--blue)'
          : 'var(--spectrum-global-color-blue-700)',
        textDecoration: 'underline',
        cursor: 'pointer'
      }}
    >
      {props.children}
    </span>
  );
}

<Link onPress={() => alert('Pressed link')}>Adobe</Link>
```

```
function Link(props) {
  let ref = React.useRef(
    null
  );
  let {
    linkProps,
    isPressed
  } = useLink({
    ...props,
    elementType: 'span'
  }, ref);

  return (
    <span
      {...linkProps}
      ref={ref}
      style={{
        color: isPressed
          ? 'var(--blue)'
          : 'var(--spectrum-global-color-blue-700)',
        textDecoration:
          'underline',
        cursor: 'pointer'
      }}
    >
      {props.children}
    </span>
  );
}

<Link
  onPress={() =>
    alert(
      'Pressed link'
    )}
>
  Adobe
</Link>
```

## Disabled links[#](#disabled-links)

---

A link can be disabled by passing the `isDisabled` property. This will work with both native
link elements as well as client handled links. Native navigation will be disabled, and the `onPress`
event will not be fired. The link will be exposed as disabled to assistive technology with ARIA.

```
function Link(props) {
  let ref = React.useRef(null);
  let { linkProps } = useLink(props, ref);

  return (
    <a
      {...linkProps}
      ref={ref}
      style={{
        color: props.isDisabled ? 'var(--gray)' : 'var(--blue)',
        cursor: props.isDisabled ? 'default' : 'pointer'
      }}
    >
      {props.children}
    </a>
  );
}

<Link href="https://adobe.com" target="_blank" isDisabled>Disabled link</Link>
```

```
function Link(props) {
  let ref = React.useRef(null);
  let { linkProps } = useLink(props, ref);

  return (
    <a
      {...linkProps}
      ref={ref}
      style={{
        color: props.isDisabled
          ? 'var(--gray)'
          : 'var(--blue)',
        cursor: props.isDisabled ? 'default' : 'pointer'
      }}
    >
      {props.children}
    </a>
  );
}

<Link href="https://adobe.com" target="_blank" isDisabled>
  Disabled link
</Link>
```

```
function Link(props) {
  let ref = React.useRef(
    null
  );
  let { linkProps } =
    useLink(props, ref);

  return (
    <a
      {...linkProps}
      ref={ref}
      style={{
        color:
          props
              .isDisabled
            ? 'var(--gray)'
            : 'var(--blue)',
        cursor:
          props
              .isDisabled
            ? 'default'
            : 'pointer'
      }}
    >
      {props.children}
    </a>
  );
}

<Link
  href="https://adobe.com"
  target="_blank"
  isDisabled
>
  Disabled link
</Link>
```

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `isDisabled` | `boolean` | â | Whether the link is disabled. |
| `elementType` | `string` | `'a'` | The HTML element used to render the link, e.g. 'a', or 'span'. |
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
| `linkProps` | `DOMAttributes` | Props for the link element. |
| `isPressed` | `boolean` | Whether the link is currently pressed. |

All DOM attributes supported across both HTML and SVG elements.

**Extends**: `AriaAttributes, ReactDOMAttributes`

| Name | Type | Description |
| --- | --- | --- |
| `id` | `string |Â undefined` |  |
| `role` | `AriaRole |Â undefined` |  |
| `tabIndex` | `number |Â undefined` |  |
| `style` | `CSSProperties |Â undefined` |  |
| `className` | `string |Â undefined` |  |