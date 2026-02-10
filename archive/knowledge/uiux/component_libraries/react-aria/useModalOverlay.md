# useModalOverlay

Source: https://react-spectrum.adobe.com/react-aria/useModalOverlay.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../Modal).

# useModalOverlay

Provides the behavior and accessibility implementation for a modal component.
A modal is an overlay element which blocks interaction with elements outside it.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useModalOverlay} from 'react-aria'` |

[View ARIA pattern

W3C](https://www.w3.org/WAI/ARIA/apg/patterns/dialogmodal/ "View ARIA pattern")[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/overlays "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/overlays "View package")

## API[#](#api)

---

`useModalOverlay(
props: AriaModalOverlayProps,
state: OverlayTriggerState,
ref: RefObject<HTMLElement
|Â  |Â null>
): ModalOverlayAria`

## Features[#](#features)

---

The HTML [<dialog>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dialog) element can be used to build modal overlays. However, it is not yet widely supported across browsers, and can be difficult to style and customize. `useModalOverlay`, helps achieve accessible modal overlays that can be styled as needed.

- **Accessible** â Content outside the modal is hidden from assistive technologies while it is open. The modal optionally closes when interacting outside, or pressing the `Escape` key.
- **Focus management** â Focus is moved into the modal on mount, and restored to the trigger element on unmount. While open, focus is contained within the modal, preventing the user from tabbing outside.
- **Scroll locking** â Scrolling the page behind the modal is prevented while it is open, including in mobile browsers.

**Note**: `useModalOverlay` only handles the overlay itself. It should be combined
with [useDialog](../Modal/useDialog.html) to create fully accessible modal dialogs. Other overlays
such as menus may also be placed in a modal overlay.

## Anatomy[#](#anatomy)

---

A modal overlay consists of an overlay container element, and an underlay. The overlay may contain a [dialog](../Modal/useDialog.html), or another element such as a [menu](../Menu/useMenu.html) or [listbox](../ListBox/useListBox.html) when used within a component such as a [select](../Select/useSelect.html) or [combobox](../ComboBox/useComboBox.html). The underlay is typically a partially transparent element that covers the rest of the screen behind the overlay, and prevents the user from interacting with the elements behind it.

`useModalOverlay` returns props that you should spread onto the overlay and underlay elements:

| Name | Type | Description |
| --- | --- | --- |
| `modalProps` | `DOMAttributes` | Props for the modal element. |
| `underlayProps` | `DOMAttributes` | Props for the underlay element. |

State is managed by the `useOverlayTriggerState`
hook in `@react-stately/overlays`. The state object should be passed as an argument to `useModalOverlay`.

## Example[#](#example)

---

This example shows how to build a typical modal dialog, by combining `useModalOverlay` with [useDialog](../Modal/useDialog.html). The `Dialog` component used in this example can also be reused within a [popover](../Popover/usePopover.html) or other types of overlays.

The `Modal` component uses an <`Overlay`> to render its contents in a React [Portal](https://reactjs.org/docs/portals.html) at the end of the document body, which ensures it is not clipped by other elements. It also acts as a focus scope, containing focus within the modal and restoring it to the trigger when it unmounts. `useModalOverlay` handles preventing page scrolling while the modal is open, hiding content outside the modal from screen readers, and optionally closing it when the user interacts outside or presses the `Escape` key.

```
import {Overlay, useModalOverlay, useViewportSize} from 'react-aria';

function Modal({ state, children, ...props }) {
  let ref = React.useRef(null);
  let { modalProps, underlayProps } = useModalOverlay(props, state, ref);

  return (
    <Overlay>
      <div
        style={{
          position: 'absolute',
          zIndex: 100,
          top: 0,
          left: 0,
          width: '100%',
          height: document.body.clientHeight,
          background: 'rgba(0, 0, 0, 0.5)'
        }}
        {...underlayProps}
      />
      <div
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100%',
          height: useViewportSize().height + 'px',
          zIndex: 101,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}
      >
        <div
          {...modalProps}
          ref={ref}
          style={{
            background: 'var(--page-background)',
            border: '1px solid gray'
          }}
        >
          {children}
        </div>
      </div>
    </Overlay>
  );
}
```

```
import {
  Overlay,
  useModalOverlay,
  useViewportSize
} from 'react-aria';

function Modal({ state, children, ...props }) {
  let ref = React.useRef(null);
  let { modalProps, underlayProps } = useModalOverlay(
    props,
    state,
    ref
  );

  return (
    <Overlay>
      <div
        style={{
          position: 'absolute',
          zIndex: 100,
          top: 0,
          left: 0,
          width: '100%',
          height: document.body.clientHeight,
          background: 'rgba(0, 0, 0, 0.5)'
        }}
        {...underlayProps}
      />
      <div
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100%',
          height: useViewportSize().height + 'px',
          zIndex: 101,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}
      >
        <div
          {...modalProps}
          ref={ref}
          style={{
            background: 'var(--page-background)',
            border: '1px solid gray'
          }}
        >
          {children}
        </div>
      </div>
    </Overlay>
  );
}
```

```
import {
  Overlay,
  useModalOverlay,
  useViewportSize
} from 'react-aria';

function Modal(
  {
    state,
    children,
    ...props
  }
) {
  let ref = React.useRef(
    null
  );
  let {
    modalProps,
    underlayProps
  } = useModalOverlay(
    props,
    state,
    ref
  );

  return (
    <Overlay>
      <div
        style={{
          position:
            'absolute',
          zIndex: 100,
          top: 0,
          left: 0,
          width: '100%',
          height:
            document.body
              .clientHeight,
          background:
            'rgba(0, 0, 0, 0.5)'
        }}
        {...underlayProps}
      />
      <div
        style={{
          position:
            'fixed',
          top: 0,
          left: 0,
          width: '100%',
          height:
            useViewportSize()
              .height +
            'px',
          zIndex: 101,
          display:
            'flex',
          alignItems:
            'center',
          justifyContent:
            'center'
        }}
      >
        <div
          {...modalProps}
          ref={ref}
          style={{
            background:
              'var(--page-background)',
            border:
              '1px solid gray'
          }}
        >
          {children}
        </div>
      </div>
    </Overlay>
  );
}
```

The below `ModalTrigger` component uses the `useOverlayTrigger` hook to show the modal when a button is pressed. It accepts a function as children, which is called with a callback that closes the modal. This can be used to implement a close button.

```
import {useOverlayTrigger} from 'react-aria';
import {useOverlayTriggerState} from 'react-stately';

// Reuse the Button from your component library. See below for details.
import {Button} from 'your-component-library';

function ModalTrigger({ label, children, ...props }) {
  let state = useOverlayTriggerState(props);
  let { triggerProps, overlayProps } = useOverlayTrigger(
    { type: 'dialog' },
    state
  );

  return (
    <>
      <Button {...triggerProps}>Open Dialog</Button>
      {state.isOpen &&
        (
          <Modal {...props} state={state}>
            {React.cloneElement(children(state.close), overlayProps)}
          </Modal>
        )}
    </>
  );
}
```

```
import {useOverlayTrigger} from 'react-aria';
import {useOverlayTriggerState} from 'react-stately';

// Reuse the Button from your component library. See below for details.
import {Button} from 'your-component-library';

function ModalTrigger({ label, children, ...props }) {
  let state = useOverlayTriggerState(props);
  let { triggerProps, overlayProps } = useOverlayTrigger({
    type: 'dialog'
  }, state);

  return (
    <>
      <Button {...triggerProps}>Open Dialog</Button>
      {state.isOpen &&
        (
          <Modal {...props} state={state}>
            {React.cloneElement(
              children(state.close),
              overlayProps
            )}
          </Modal>
        )}
    </>
  );
}
```

```
import {useOverlayTrigger} from 'react-aria';
import {useOverlayTriggerState} from 'react-stately';

// Reuse the Button from your component library. See below for details.
import {Button} from 'your-component-library';

function ModalTrigger(
  {
    label,
    children,
    ...props
  }
) {
  let state =
    useOverlayTriggerState(
      props
    );
  let {
    triggerProps,
    overlayProps
  } = useOverlayTrigger({
    type: 'dialog'
  }, state);

  return (
    <>
      <Button
        {...triggerProps}
      >
        Open Dialog
      </Button>
      {state.isOpen &&
        (
          <Modal
            {...props}
            state={state}
          >
            {React
              .cloneElement(
                children(
                  state
                    .close
                ),
                overlayProps
              )}
          </Modal>
        )}
    </>
  );
}
```

Now, we can render an example modal containing a dialog, with a button that closes it using the function provided by `ModalTrigger`.

```
// Reuse the Dialog from your component library. See below for details.
import {Dialog} from 'your-component-library';

<ModalTrigger label="Open Dialog">
  {close =>
    <Dialog title="Enter your name">
      <form style={{display: 'flex', flexDirection: 'column'}}>
        <label htmlFor="first-name">First Name:</label>
        <input id="first-name" />
        <label htmlFor="last-name">Last Name:</label>
        <input id="last-name" />
        <Button
          onPress={close}
          style={{marginTop: 10}}>
          Submit
        </Button>
      </form>
    </Dialog>
  }
</ModalTrigger>
```

```
// Reuse the Dialog from your component library. See below for details.
import {Dialog} from 'your-component-library';

<ModalTrigger label="Open Dialog">
  {(close) => (
    <Dialog title="Enter your name">
      <form
        style={{
          display: 'flex',
          flexDirection: 'column'
        }}
      >
        <label htmlFor="first-name">First Name:</label>
        <input id="first-name" />
        <label htmlFor="last-name">Last Name:</label>
        <input id="last-name" />
        <Button
          onPress={close}
          style={{ marginTop: 10 }}
        >
          Submit
        </Button>
      </form>
    </Dialog>
  )}
</ModalTrigger>
```

```
// Reuse the Dialog from your component library. See below for details.
import {Dialog} from 'your-component-library';

<ModalTrigger label="Open Dialog">
  {(close) => (
    <Dialog title="Enter your name">
      <form
        style={{
          display:
            'flex',
          flexDirection:
            'column'
        }}
      >
        <label htmlFor="first-name">
          First Name:
        </label>
        <input id="first-name" />
        <label htmlFor="last-name">
          Last Name:
        </label>
        <input id="last-name" />
        <Button
          onPress={close}
          style={{
            marginTop:
              10
          }}
        >
          Submit
        </Button>
      </form>
    </Dialog>
  )}
</ModalTrigger>
```

### Dialog[#](#dialog)

The `Dialog` component is rendered within the `ModalOverlay` component. It is built using the [useDialog](../Modal/useDialog.html) hook, and can also be used in other overlay containers such as [popovers](../Popover/usePopover.html).

 Show code

```
import type {AriaDialogProps} from 'react-aria';
import {useDialog} from 'react-aria';

interface DialogProps extends AriaDialogProps {
  title?: React.ReactNode;
  children: React.ReactNode;
}

function Dialog({ title, children, ...props }: DialogProps) {
  let ref = React.useRef(null);
  let { dialogProps, titleProps } = useDialog(props, ref);

  return (
    <div {...dialogProps} ref={ref} style={{ padding: 30 }}>
      {title &&
        (
          <h3 {...titleProps} style={{ marginTop: 0 }}>
            {title}
          </h3>
        )}
      {children}
    </div>
  );
}
```

```
import type {AriaDialogProps} from 'react-aria';
import {useDialog} from 'react-aria';

interface DialogProps extends AriaDialogProps {
  title?: React.ReactNode;
  children: React.ReactNode;
}

function Dialog(
  { title, children, ...props }: DialogProps
) {
  let ref = React.useRef(null);
  let { dialogProps, titleProps } = useDialog(props, ref);

  return (
    <div {...dialogProps} ref={ref} style={{ padding: 30 }}>
      {title &&
        (
          <h3 {...titleProps} style={{ marginTop: 0 }}>
            {title}
          </h3>
        )}
      {children}
    </div>
  );
}
```

```
import type {AriaDialogProps} from 'react-aria';
import {useDialog} from 'react-aria';

interface DialogProps
  extends
    AriaDialogProps {
  title?:
    React.ReactNode;
  children:
    React.ReactNode;
}

function Dialog(
  {
    title,
    children,
    ...props
  }: DialogProps
) {
  let ref = React.useRef(
    null
  );
  let {
    dialogProps,
    titleProps
  } = useDialog(
    props,
    ref
  );

  return (
    <div
      {...dialogProps}
      ref={ref}
      style={{
        padding: 30
      }}
    >
      {title &&
        (
          <h3
            {...titleProps}
            style={{
              marginTop:
                0
            }}
          >
            {title}
          </h3>
        )}
      {children}
    </div>
  );
}
```

### Button[#](#button)

The `Button` component is used in the above example to toggle the popover. It is built using the [useButton](../Button/useButton.html) hook, and can be shared with many other components.

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

## Usage[#](#usage)

---

The following examples show how to use the `Modal` and `ModalTrigger` components created in the above example.

### Dismissable[#](#dismissable)

If your modal doesn't require the user to make a confirmation, you can set `isDismissable`
on the `Modal`. This allows the user to click outside to close the dialog.

```
<ModalTrigger isDismissable label="Open Dialog">
  {() =>
    <Dialog title="Notice">
      Click outside to close this dialog.
    </Dialog>
  }
</ModalTrigger>
```

```
<ModalTrigger isDismissable label="Open Dialog">
  {() =>
    <Dialog title="Notice">
      Click outside to close this dialog.
    </Dialog>
  }
</ModalTrigger>
```

```
<ModalTrigger
  isDismissable
  label="Open Dialog"
>
  {() => (
    <Dialog title="Notice">
      Click outside to
      close this
      dialog.
    </Dialog>
  )}
</ModalTrigger>
```

### Keyboard dismiss disabled[#](#keyboard-dismiss-disabled)

By default, modals can be closed by pressing the `Escape` key. This can be disabled with the `isKeyboardDismissDisabled` prop.

```
<ModalTrigger isKeyboardDismissDisabled label="Open Dialog">
  {close =>
    <Dialog title="Notice">
      <p>You must close this dialog using the button below.</p>
      <Button onPress={close}>Close</Button>
    </Dialog>
  }
</ModalTrigger>
```

```
<ModalTrigger
  isKeyboardDismissDisabled
  label="Open Dialog"
>
  {(close) => (
    <Dialog title="Notice">
      <p>
        You must close this dialog using the button below.
      </p>
      <Button onPress={close}>Close</Button>
    </Dialog>
  )}
</ModalTrigger>
```

```
<ModalTrigger
  isKeyboardDismissDisabled
  label="Open Dialog"
>
  {(close) => (
    <Dialog title="Notice">
      <p>
        You must close
        this dialog
        using the
        button below.
      </p>
      <Button
        onPress={close}
      >
        Close
      </Button>
    </Dialog>
  )}
</ModalTrigger>
```

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `isDismissable` | `boolean` | `false` | Whether to close the modal when the user interacts outside it. |
| `isKeyboardDismissDisabled` | `boolean` | `false` | Whether pressing the escape key to close the modal should be disabled. |
| `shouldCloseOnInteractOutside` | `( (element: Element )) => boolean` | â | When user interacts with the argument element outside of the overlay ref, return true if onClose should be called. This gives you a chance to filter out interaction with elements that should not dismiss the overlay. By default, onClose will always be called on interaction outside the overlay ref. |

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `isOpen` | `boolean` | Whether the overlay is currently open. |

### Methods

| Method | Description |
| --- | --- |
| `setOpen( (isOpen: boolean )): void` | Sets whether the overlay is open. |
| `open(): void` | Opens the overlay. |
| `close(): void` | Closes the overlay. |
| `toggle(): void` | Toggles the overlay's visibility. |

| Name | Type | Description |
| --- | --- | --- |
| `current` | `T` |  |

| Name | Type | Description |
| --- | --- | --- |
| `modalProps` | `DOMAttributes` | Props for the modal element. |
| `underlayProps` | `DOMAttributes` | Props for the underlay element. |

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

Manages state for an overlay trigger. Tracks whether the overlay is open, and provides
methods to toggle this state.

`useOverlayTriggerState(
(props: OverlayTriggerProps
)): OverlayTriggerState`

| Name | Type | Description |
| --- | --- | --- |
| `isOpen` | `boolean` | Whether the overlay is open by default (controlled). |
| `defaultOpen` | `boolean` | Whether the overlay is open by default (uncontrolled). |
| `onOpenChange` | `( (isOpen: boolean )) => void` | Handler that is called when the overlay's open state changes. |

A container which renders an overlay such as a popover or modal in a portal,
and provides a focus scope for the child elements.

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `children` | `ReactNode` | â | The overlay to render in the portal. |
| `portalContainer` | `Element` | `document.body` | The container element in which the overlay portal will be placed. |
| `disableFocusManagement` | `boolean` | â | Disables default focus management for the overlay, including containment and restoration. This option should be used very carefully. When focus management is disabled, you must implement focus containment and restoration to ensure the overlay is keyboard accessible. |
| `shouldContainFocus` | `boolean` | â | Whether to contain focus within the overlay. |
| `isExiting` | `boolean` | â | Whether the overlay is currently performing an exit animation. When true, focus is allowed to move outside. |

Provides the behavior and accessibility implementation for a modal component.
A modal is an overlay element which blocks interaction with elements outside it.

`useModalOverlay(
props: AriaModalOverlayProps,
state: OverlayTriggerState,
ref: RefObject<HTMLElement
|Â  |Â null>
): ModalOverlayAria`

Handles the behavior and accessibility for an overlay trigger, e.g. a button
that opens a popover, menu, or other overlay that is positioned relative to the trigger.

`useOverlayTrigger(
props: OverlayTriggerProps,
state: OverlayTriggerState,
ref?: RefObject<Element
|Â  |Â null>
): OverlayTriggerAria`

| Name | Type | Description |
| --- | --- | --- |
| `type` | `'dialog' |Â 'menu' |Â 'listbox' |Â 'tree' |Â 'grid'` | Type of overlay that is opened by the trigger. |

| Name | Type | Description |
| --- | --- | --- |
| `triggerProps` | `AriaButtonProps` | Props for the trigger element. |
| `overlayProps` | `DOMProps` | Props for the overlay container element. |

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

`BaseEvent<ReactKeyboardEvent<any>>`

`SyntheticEvent &Â {

stopPropagation: () => void,

continuePropagation: () => void

}`

| Name | Type | Description |
| --- | --- | --- |
| `id` | `string` | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |