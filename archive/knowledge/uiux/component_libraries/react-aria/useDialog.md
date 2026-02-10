# useDialog

Source: https://react-spectrum.adobe.com/react-aria/useDialog.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../Modal).

# useDialog

Provides the behavior and accessibility implementation for a dialog component.
A dialog is an overlay shown above other content in an application.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useDialog} from 'react-aria'` |

[View ARIA pattern

W3C](https://www.w3.org/WAI/ARIA/apg/patterns/dialogmodal/ "View ARIA pattern")[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/dialog "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/dialog "View package")

## API[#](#api)

---

`useDialog(
(props: AriaDialogProps,
, ref: RefObject<FocusableElement
|Â  |Â null>
)): DialogAria`

## Features[#](#features)

---

The HTML [<dialog>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dialog) element
can be used to build dialogs. However, it is not yet widely supported across browsers, and
building fully accessible custom dialogs from scratch is very difficult and error prone.
`useDialog` helps achieve accessible dialogs that can be styled as needed.

- **Flexible** â Dialogs can be used within a [modal](../Modal/useModalOverlay.html) or [popover](../Popover/usePopover.html) to create many types of overlay elements.
- **Accessible** â Exposed to assistive technology as a `dialog` or `alertdialog` with ARIA. The dialog is labeled by its title element, and content outside the dialog is hidden from assistive technologies while it is open.
- **Focus management** â Focus is moved into the dialog on mount, and restored to the trigger element on unmount. While open, focus is contained within the dialog, preventing the user from tabbing outside.

## Anatomy[#](#anatomy)

---

A dialog consists of a container element and an optional title. `useDialog` handles
exposing this to assistive technology using ARIA. It can be combined
with `useModalOverlay` or `usePopover`,
to create modal dialogs, popovers, and other types of overlays.

`useDialog` returns props that you should spread onto the appropriate element:

| Name | Type | Description |
| --- | --- | --- |
| `dialogProps` | `DOMAttributes` | Props for the dialog container element. |
| `titleProps` | `DOMAttributes` | Props for the dialog title element. |

If a dialog does not have a visible title element, an `aria-label` or `aria-labelledby`
prop must be passed instead to identify the element to assistive technology.

## Example[#](#example)

---

This example shows how to build a typical modal dialog, by combining `useDialog` with [useModalOverlay](../Modal/useModalOverlay.html). The code for the `Modal` component is available below. The `Dialog` component may also be used within a [popover](../Popover/usePopover.html). See the docs for more details on overlay containers.

```
import type {AriaDialogProps} from 'react-aria';
import {useDialog} from 'react-aria';

// Reuse the Button and Modal from your component library. See below for details.
import {Button, Modal, ModalTrigger} from 'your-component-library';

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

<ModalTrigger label="Open Dialog">
  {(close) => (
    <Dialog title="Enter your name">
      <form style={{ display: 'flex', flexDirection: 'column' }}>
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
import type {AriaDialogProps} from 'react-aria';
import {useDialog} from 'react-aria';

// Reuse the Button and Modal from your component library. See below for details.
import {
  Button,
  Modal,
  ModalTrigger
} from 'your-component-library';

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
import type {AriaDialogProps} from 'react-aria';
import {useDialog} from 'react-aria';

// Reuse the Button and Modal from your component library. See below for details.
import {
  Button,
  Modal,
  ModalTrigger
} from 'your-component-library';

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

### Modal[#](#modal)

The `Modal` and `ModalTrigger` components render the dialog within a typical modal container with a partially transparent underlay. See [useModalOverlay](../Modal/useModalOverlay.html) for more details.

 Show code

```
import {Overlay, useModalOverlay, useOverlayTrigger, useViewportSize} from 'react-aria';
import {useOverlayTriggerState} from 'react-stately';

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

function ModalTrigger({ label, children, ...props }) {
  let state = useOverlayTriggerState(props);
  let { triggerProps, overlayProps } = useOverlayTrigger(
    { type: 'dialog' },
    state
  );

  return (
    <>
      <Button {...triggerProps}>{label}</Button>
      {state.isOpen &&
        (
          <Modal state={state}>
            {React.cloneElement(children(state.close), overlayProps)}
          </Modal>
        )}
    </>
  );
}
```

```
import {
  Overlay,
  useModalOverlay,
  useOverlayTrigger,
  useViewportSize
} from 'react-aria';
import {useOverlayTriggerState} from 'react-stately';

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

function ModalTrigger({ label, children, ...props }) {
  let state = useOverlayTriggerState(props);
  let { triggerProps, overlayProps } = useOverlayTrigger({
    type: 'dialog'
  }, state);

  return (
    <>
      <Button {...triggerProps}>{label}</Button>
      {state.isOpen &&
        (
          <Modal state={state}>
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
import {
  Overlay,
  useModalOverlay,
  useOverlayTrigger,
  useViewportSize
} from 'react-aria';
import {useOverlayTriggerState} from 'react-stately';

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
        {label}
      </Button>
      {state.isOpen &&
        (
          <Modal
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

### Button[#](#button)

The `Button` component is used in the above example to open and close the dialog. It is built using the [useButton](../Button/useButton.html) hook, and can be shared with many other components.

 Show code

```
import {useButton} from 'react-aria';

function Button(props) {
  let ref = React.useRef(null);
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
  let ref = React.useRef(null);
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
      style={props.style}
    >
      {props.children}
    </button>
  );
}
```

## Styled examples[#](#styled-examples)

---

[![](/tailwind.00f5d4bb.png)

Tailwind CSS

An animated alert dialog using Tailwind and react-transition-group.](https://codesandbox.io/s/delicate-hill-j4p5vs?file=/src/AlertDialog.tsx)

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `role` | `'dialog' |Â 'alertdialog'` | `'dialog'` | The accessibility role for the dialog. |
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `aria-label` | `string` | â | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |

| Name | Type | Description |
| --- | --- | --- |
| `current` | `T` |  |

| Name | Type | Description |
| --- | --- | --- |
| `dialogProps` | `DOMAttributes` | Props for the dialog container element. |
| `titleProps` | `DOMAttributes` | Props for the dialog title element. |

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

Provides the behavior and accessibility implementation for a modal component.
A modal is an overlay element which blocks interaction with elements outside it.

`useModalOverlay(
props: AriaModalOverlayProps,
state: OverlayTriggerState,
ref: RefObject<HTMLElement
|Â  |Â null>
): ModalOverlayAria`

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
| `modalProps` | `DOMAttributes` | Props for the modal element. |
| `underlayProps` | `DOMAttributes` | Props for the underlay element. |

Provides the behavior and accessibility implementation for a popover component.
A popover is an overlay element positioned relative to a trigger.

`usePopover(
(props: AriaPopoverProps,
, state: OverlayTriggerState
)): PopoverAria`

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `triggerRef` | `RefObject<Element |Â null>` | â | The ref for the element which the popover positions itself with respect to. |
| `popoverRef` | `RefObject<Element |Â null>` | â | The ref for the popover element. |
| `arrowRef` | `RefObject<Element |Â null>` | â | A ref for the popover arrow element. |
| `groupRef` | `RefObject<Element |Â null>` | â | An optional ref for a group of popovers, e.g. submenus. When provided, this element is used to detect outside interactions and hiding elements from assistive technologies instead of the popoverRef. |
| `isNonModal` | `boolean` | â | Whether the popover is non-modal, i.e. elements outside the popover may be interacted with by assistive technologies.  Most popovers should not use this option as it may negatively impact the screen reader experience. Only use with components such as combobox, which are designed to handle this situation carefully. |
| `isKeyboardDismissDisabled` | `boolean` | `false` | Whether pressing the escape key to close the popover should be disabled.  Most popovers should not use this option. When set to true, an alternative way to close the popover with a keyboard must be provided. |
| `shouldCloseOnInteractOutside` | `( (element: Element )) => boolean` | â | When user interacts with the argument element outside of the popover ref, return true if onClose should be called. This gives you a chance to filter out interaction with elements that should not dismiss the popover. By default, onClose will always be called on interaction outside the popover ref. |
| `arrowSize` | `number` | `0` | Cross size of the overlay arrow in pixels. |
| `boundaryElement` | `Element` | `document.body` | Element that that serves as the positioning boundary. |
| `scrollRef` | `RefObject<Element |Â null>` | `overlayRef` | A ref for the scrollable region within the overlay. |
| `shouldUpdatePosition` | `boolean` | `true` | Whether the overlay should update its position automatically. |
| `maxHeight` | `number` | â | The maxHeight specified for the overlay element. By default, it will take all space up to the current viewport height. |
| `arrowBoundaryOffset` | `number` | `0` | The minimum distance the arrow's edge should be from the edge of the overlay element. |
| `placement` | `Placement` | `'bottom'` | The placement of the element with respect to its anchor element. |
| `containerPadding` | `number` | `12` | The placement padding that should be applied between the element and its surrounding container. |
| `offset` | `number` | `0` | The additional offset applied along the main axis between the element and its anchor element. |
| `crossOffset` | `number` | `0` | The additional offset applied along the cross axis between the element and its anchor element. |
| `shouldFlip` | `boolean` | `true` | Whether the element should flip its orientation (e.g. top to bottom or left to right) when there is insufficient room for it to render completely. |

`'bottom'
|Â 'bottom left'
|Â 'bottom right'
|Â 'bottom start'
|Â 'bottom end'
|Â 'top'
|Â 'top left'
|Â 'top right'
|Â 'top start'
|Â 'top end'
|Â 'left'
|Â 'left top'
|Â 'left bottom'
|Â 'start'
|Â 'start top'
|Â 'start bottom'
|Â 'right'
|Â 'right top'
|Â 'right bottom'
|Â 'end'
|Â 'end top'
|Â 'end bottom'`

| Name | Type | Description |
| --- | --- | --- |
| `popoverProps` | `DOMAttributes` | Props for the popover element. |
| `arrowProps` | `DOMAttributes` | Props for the popover tip arrow if any. |
| `underlayProps` | `DOMAttributes` | Props to apply to the underlay element, if any. |
| `placement` | `PlacementAxis |Â null` | Placement of the popover with respect to the trigger. |
| `triggerAnchorPoint` | `{ x: number,  y: number } |Â null` | The origin of the target in the overlay's coordinate system. Useful for animations. |

`Axis |Â 'center'`

`'top'
|Â 'bottom'
|Â 'left'
|Â 'right'`