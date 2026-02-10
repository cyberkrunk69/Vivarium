# usePopover

Source: https://react-spectrum.adobe.com/react-aria/usePopover.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../Popover).

# usePopover

Provides the behavior and accessibility implementation for a popover component.
A popover is an overlay element positioned relative to a trigger.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {usePopover} from 'react-aria'` |

[View ARIA pattern

W3C](https://www.w3.org/WAI/ARIA/apg/patterns/dialogmodal/ "View ARIA pattern")[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/overlays "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/overlays "View package")

## API[#](#api)

---

`usePopover(
(props: AriaPopoverProps,
, state: OverlayTriggerState
)): PopoverAria`

## Features[#](#features)

---

There is no built in way to create popovers in
HTML. `usePopover`,
helps achieve accessible popovers that can be styled as needed.

- **Accessible** â The trigger and popover are automatically associated semantically via ARIA. Content outside the popover is hidden from assistive technologies while it is open. The popover closes when interacting outside, or pressing the `Escape` key.
- **Focus management** â Focus is moved into the popover on mount, and restored to the trigger element on unmount.
- **Positioning** â The popover is positioned relative to the trigger element, and automatically flips and adjusts to avoid overlapping with the edge of the browser window. Scrolling is prevented outside the popover to avoid unintentionally repositioning or closing it.

**Note**: `usePopover` only handles the overlay itself. It should be combined
with [useDialog](../Modal/useDialog.html) to create fully accessible popovers. Other overlays
such as menus may also be placed in a popover.

## Anatomy[#](#anatomy)

---

A popover consists of a trigger element (e.g. button) and an overlay, which is positioned relative to the trigger. The overlay may contain a [dialog](../Modal/useDialog.html), or another element such as a [menu](../Menu/useMenu.html) or [listbox](../ListBox/useListBox.html) when used within a component such as a [select](../Select/useSelect.html) or [combobox](../ComboBox/useComboBox.html).

`usePopover` returns props that you should spread onto the appropriate elements, as well as the computed placement of the popover relative to the trigger:

| Name | Type | Description |
| --- | --- | --- |
| `popoverProps` | `DOMAttributes` | Props for the popover element. |
| `arrowProps` | `DOMAttributes` | Props for the popover tip arrow if any. |
| `underlayProps` | `DOMAttributes` | Props to apply to the underlay element, if any. |
| `placement` | `PlacementAxis |Â null` | Placement of the popover with respect to the trigger. |
| `triggerAnchorPoint` | `{ x: number,  y: number } |Â null` | The origin of the target in the overlay's coordinate system. Useful for animations. |

State is managed by the `useOverlayTriggerState`
hook in `@react-stately/overlays`. The state object should be passed as an argument to `usePopover`.

## Example[#](#example)

---

This example shows how to build a typical popover overlay that is positioned relative to
a trigger button. The content of the popover is a dialog, built
with `useDialog`. The `Dialog` component used in this example can also be reused within a [modal](../Modal/useModalOverlay.html) or other types of overlays. The implementation is available below.

The `Popover` component uses an <`Overlay`> to render its contents in a React [Portal](https://reactjs.org/docs/portals.html) at the end of the document body, which ensures it is not clipped by other elements. It also acts as a focus scope, containing focus within the popover and restoring it to the trigger when it unmounts. `usePopover` handles positioning the popover relative to the trigger element, and closing it when the user interacts outside or presses the `Escape` key.

`usePopover` also hides content outside the popover from screen readers, which is important since the surrounding content won't be in context of the original trigger due to the portal. To allow screen reader users to dismiss the popover without a keyboard (e.g. on mobile), visually hidden <`DismissButton`> elements are added at the start and end of the popover. An underlay is also used to prevent scrolling and interacting with elements outside the popover with a pointer, to avoid unintentionally repositioning or closing it.

```
import {DismissButton, Overlay, usePopover} from 'react-aria';
import type {AriaPopoverProps} from 'react-aria';
import type {OverlayTriggerState} from 'react-stately';

interface PopoverProps extends Omit<AriaPopoverProps, 'popoverRef'> {
  children: React.ReactNode;
  state: OverlayTriggerState;
}

function Popover({ children, state, offset = 8, ...props }: PopoverProps) {
  let popoverRef = React.useRef(null);
  let { popoverProps, underlayProps, arrowProps, placement } = usePopover({
    ...props,
    offset,
    popoverRef
  }, state);

  return (
    <Overlay>
      <div {...underlayProps} className="underlay" />
      <div
        {...popoverProps}
        ref={popoverRef}
        className="popover"
      >
        <svg
          {...arrowProps}
          className="arrow"
          data-placement={placement}
          viewBox="0 0 12 12"
        >
          <path d="M0 0 L6 6 L12 0" />
        </svg>
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
  { children, state, offset = 8, ...props }: PopoverProps
) {
  let popoverRef = React.useRef(null);
  let {
    popoverProps,
    underlayProps,
    arrowProps,
    placement
  } = usePopover({
    ...props,
    offset,
    popoverRef
  }, state);

  return (
    <Overlay>
      <div {...underlayProps} className="underlay" />
      <div
        {...popoverProps}
        ref={popoverRef}
        className="popover"
      >
        <svg
          {...arrowProps}
          className="arrow"
          data-placement={placement}
          viewBox="0 0 12 12"
        >
          <path d="M0 0 L6 6 L12 0" />
        </svg>
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
    offset = 8,
    ...props
  }: PopoverProps
) {
  let popoverRef = React
    .useRef(null);
  let {
    popoverProps,
    underlayProps,
    arrowProps,
    placement
  } = usePopover({
    ...props,
    offset,
    popoverRef
  }, state);

  return (
    <Overlay>
      <div
        {...underlayProps}
        className="underlay"
      />
      <div
        {...popoverProps}
        ref={popoverRef}
        className="popover"
      >
        <svg
          {...arrowProps}
          className="arrow"
          data-placement={placement}
          viewBox="0 0 12 12"
        >
          <path d="M0 0 L6 6 L12 0" />
        </svg>
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

The above `Popover` component can be used as part of many different patterns, such as [ComboBox](../ComboBox/useComboBox.html), [Select](../Select/useSelect.html), and [DatePicker](../DatePicker/useDatePicker.html). To use it standalone, we need a trigger element. The below `PopoverTrigger` component uses the `useOverlayTrigger` hook to trigger the popover when a button is pressed. This hook also ensures that the button and popover are semantically connected via ARIA.

```
import {useOverlayTrigger} from 'react-aria';
import {useOverlayTriggerState} from 'react-stately';

// Reuse the Button from your component library. See below for details.
import {Button} from 'your-component-library';

function PopoverTrigger({ label, children, ...props }) {
  let ref = React.useRef(null);
  let state = useOverlayTriggerState(props);
  let { triggerProps, overlayProps } = useOverlayTrigger(
    { type: 'dialog' },
    state,
    ref
  );

  return (
    <>
      <Button {...triggerProps} buttonRef={ref}>{label}</Button>
      {state.isOpen &&
        (
          <Popover {...props} triggerRef={ref} state={state}>
            {React.cloneElement(children, overlayProps)}
          </Popover>
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

function PopoverTrigger({ label, children, ...props }) {
  let ref = React.useRef(null);
  let state = useOverlayTriggerState(props);
  let { triggerProps, overlayProps } = useOverlayTrigger(
    { type: 'dialog' },
    state,
    ref
  );

  return (
    <>
      <Button {...triggerProps} buttonRef={ref}>
        {label}
      </Button>
      {state.isOpen &&
        (
          <Popover
            {...props}
            triggerRef={ref}
            state={state}
          >
            {React.cloneElement(children, overlayProps)}
          </Popover>
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

function PopoverTrigger(
  {
    label,
    children,
    ...props
  }
) {
  let ref = React.useRef(
    null
  );
  let state =
    useOverlayTriggerState(
      props
    );
  let {
    triggerProps,
    overlayProps
  } = useOverlayTrigger(
    { type: 'dialog' },
    state,
    ref
  );

  return (
    <>
      <Button
        {...triggerProps}
        buttonRef={ref}
      >
        {label}
      </Button>
      {state.isOpen &&
        (
          <Popover
            {...props}
            triggerRef={ref}
            state={state}
          >
            {React
              .cloneElement(
                children,
                overlayProps
              )}
          </Popover>
        )}
    </>
  );
}
```

Now, we can render an example popover containing a dialog.

```
// Reuse the Dialog from your component library. See below for details.
import {Dialog} from 'your-component-library';

<PopoverTrigger label="Open Popover">
  <Dialog title="Popover title">
    This is the content of the popover.
  </Dialog>
</PopoverTrigger>
```

```
// Reuse the Dialog from your component library. See below for details.
import {Dialog} from 'your-component-library';

<PopoverTrigger label="Open Popover">
  <Dialog title="Popover title">
    This is the content of the popover.
  </Dialog>
</PopoverTrigger>
```

```
// Reuse the Dialog from your component library. See below for details.
import {Dialog} from 'your-component-library';

<PopoverTrigger label="Open Popover">
  <Dialog title="Popover title">
    This is the content
    of the popover.
  </Dialog>
</PopoverTrigger>
```

 Show CSS

```
.underlay {
  position: fixed;
  inset: 0;
}

.popover {
  background: var(--page-background);
  border: 1px solid var(--spectrum-global-color-gray-400);
  box-shadow: 0 8px 20px rgba(0 0 0 / 0.1);
  border-radius: 6px;
}

.arrow {
  position: absolute;
  fill: var(--page-background);
  stroke: var(--spectrum-global-color-gray-400);
  stroke-width: 1px;
  width: 12px;
  height: 12px;
}

.arrow[data-placement=top] {
  top: 100%;
  transform: translateX(-50%);
}

.arrow[data-placement=bottom] {
  bottom: 100%;
  transform: translateX(-50%) rotate(180deg);
}

.arrow[data-placement=left] {
  left: 100%;
  transform: translateY(-50%) rotate(-90deg);
}

.arrow[data-placement=right] {
  right: 100%;
  transform: translateY(-50%) rotate(90deg);
}
```

```
.underlay {
  position: fixed;
  inset: 0;
}

.popover {
  background: var(--page-background);
  border: 1px solid var(--spectrum-global-color-gray-400);
  box-shadow: 0 8px 20px rgba(0 0 0 / 0.1);
  border-radius: 6px;
}

.arrow {
  position: absolute;
  fill: var(--page-background);
  stroke: var(--spectrum-global-color-gray-400);
  stroke-width: 1px;
  width: 12px;
  height: 12px;
}

.arrow[data-placement=top] {
  top: 100%;
  transform: translateX(-50%);
}

.arrow[data-placement=bottom] {
  bottom: 100%;
  transform: translateX(-50%) rotate(180deg);
}

.arrow[data-placement=left] {
  left: 100%;
  transform: translateY(-50%) rotate(-90deg);
}

.arrow[data-placement=right] {
  right: 100%;
  transform: translateY(-50%) rotate(90deg);
}
```

```
.underlay {
  position: fixed;
  inset: 0;
}

.popover {
  background: var(--page-background);
  border: 1px solid var(--spectrum-global-color-gray-400);
  box-shadow: 0 8px 20px rgba(0 0 0 / 0.1);
  border-radius: 6px;
}

.arrow {
  position: absolute;
  fill: var(--page-background);
  stroke: var(--spectrum-global-color-gray-400);
  stroke-width: 1px;
  width: 12px;
  height: 12px;
}

.arrow[data-placement=top] {
  top: 100%;
  transform: translateX(-50%);
}

.arrow[data-placement=bottom] {
  bottom: 100%;
  transform: translateX(-50%) rotate(180deg);
}

.arrow[data-placement=left] {
  left: 100%;
  transform: translateY(-50%) rotate(-90deg);
}

.arrow[data-placement=right] {
  right: 100%;
  transform: translateY(-50%) rotate(90deg);
}
```

### Dialog[#](#dialog)

The `Dialog` component is rendered within the `Popover` component. It is built using the [useDialog](../Modal/useDialog.html) hook, and can also be used in other overlay containers such as [modals](../Modal/useModalOverlay.html).

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
    <div
      {...dialogProps}
      ref={ref}
      style={{ padding: 30, maxWidth: 200, outline: 'none' }}
    >
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
    <div
      {...dialogProps}
      ref={ref}
      style={{
        padding: 30,
        maxWidth: 200,
        outline: 'none'
      }}
    >
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
        padding: 30,
        maxWidth: 200,
        outline: 'none'
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

The following examples show how to use the `Popover` and `PopoverTrigger` components created in the above example.

### Placement[#](#placement)

The popover's placement with respect to its anchor element can be adjusted using the `placement`
prop. See `Placement` for a full list of available placement combinations.

```
<div style={{ display: 'flex', gap: 8 }}>
  <PopoverTrigger placement="start" label="â¬ï¸">
    <Dialog>
      In left-to-right, this is on the left. In right-to-left, this is on the
      right.
    </Dialog>
  </PopoverTrigger>
  <PopoverTrigger placement="top" label="â¬ï¸">
    <Dialog>This popover is above the button.</Dialog>
  </PopoverTrigger>
  <PopoverTrigger placement="bottom" label="â¬ï¸">
    <Dialog>This popover is below the button.</Dialog>
  </PopoverTrigger>
  <PopoverTrigger placement="end" label="â¡ï¸">
    <Dialog>
      In left-to-right, this is on the right. In right-to-left, this is on the
      left.
    </Dialog>
  </PopoverTrigger>
</div>
```

```
<div style={{ display: 'flex', gap: 8 }}>
  <PopoverTrigger placement="start" label="â¬ï¸">
    <Dialog>
      In left-to-right, this is on the left. In
      right-to-left, this is on the right.
    </Dialog>
  </PopoverTrigger>
  <PopoverTrigger placement="top" label="â¬ï¸">
    <Dialog>This popover is above the button.</Dialog>
  </PopoverTrigger>
  <PopoverTrigger placement="bottom" label="â¬ï¸">
    <Dialog>This popover is below the button.</Dialog>
  </PopoverTrigger>
  <PopoverTrigger placement="end" label="â¡ï¸">
    <Dialog>
      In left-to-right, this is on the right. In
      right-to-left, this is on the left.
    </Dialog>
  </PopoverTrigger>
</div>
```

```
<div
  style={{
    display: 'flex',
    gap: 8
  }}
>
  <PopoverTrigger
    placement="start"
    label="â¬ï¸"
  >
    <Dialog>
      In left-to-right,
      this is on the
      left. In
      right-to-left,
      this is on the
      right.
    </Dialog>
  </PopoverTrigger>
  <PopoverTrigger
    placement="top"
    label="â¬ï¸"
  >
    <Dialog>
      This popover is
      above the button.
    </Dialog>
  </PopoverTrigger>
  <PopoverTrigger
    placement="bottom"
    label="â¬ï¸"
  >
    <Dialog>
      This popover is
      below the button.
    </Dialog>
  </PopoverTrigger>
  <PopoverTrigger
    placement="end"
    label="â¡ï¸"
  >
    <Dialog>
      In left-to-right,
      this is on the
      right. In
      right-to-left,
      this is on the
      left.
    </Dialog>
  </PopoverTrigger>
</div>
```

### Offset and cross offset[#](#offset-and-cross-offset)

The popover's offset with respect to its anchor element can be adjusted using the `offset` and
`crossOffset` props. The `offset` prop controls the spacing applied along the main axis between the element and its
anchor element whereas the `crossOffset` prop handles the spacing applied along the cross axis.

Below is a popover offset by an additional 50px above the trigger.

```
<PopoverTrigger placement="top" offset={50} label="Trigger">
  <Dialog>
    Offset by an additional 50px.
  </Dialog>
</PopoverTrigger>
```

```
<PopoverTrigger placement="top" offset={50} label="Trigger">
  <Dialog>
    Offset by an additional 50px.
  </Dialog>
</PopoverTrigger>
```

```
<PopoverTrigger
  placement="top"
  offset={50}
  label="Trigger"
>
  <Dialog>
    Offset by an
    additional 50px.
  </Dialog>
</PopoverTrigger>
```

Below is a popover cross offset by an additional 100px to the right of the trigger.

```
<PopoverTrigger placement="top" crossOffset={100} label="Trigger">
  <Dialog>
    Offset by an additional 100px.
  </Dialog>
</PopoverTrigger>
```

```
<PopoverTrigger
  placement="top"
  crossOffset={100}
  label="Trigger"
>
  <Dialog>
    Offset by an additional 100px.
  </Dialog>
</PopoverTrigger>
```

```
<PopoverTrigger
  placement="top"
  crossOffset={100}
  label="Trigger"
>
  <Dialog>
    Offset by an
    additional 100px.
  </Dialog>
</PopoverTrigger>
```

### Flipping[#](#flipping)

By default, `usePopover` attempts to flip popovers on the main axis in situations where the original placement
would cause it to render out of view. This can be overridden by setting `shouldFlip={false}`.
To see the difference between the two options, scroll this page so that the example below is near the bottom of the window.

```
<PopoverTrigger placement="bottom" label="Default">
  <Dialog>
    This is a popover that will flip if it can't fully render below the button.
  </Dialog>
</PopoverTrigger>

<PopoverTrigger placement="bottom" shouldFlip={false} label="shouldFlip=false">
  <Dialog>
    This is a popover that won't flip if it can't fully render below the button.
  </Dialog>
</PopoverTrigger>
```

```
<PopoverTrigger placement="bottom" label="Default">
  <Dialog>
    This is a popover that will flip if it can't fully
    render below the button.
  </Dialog>
</PopoverTrigger>
 <PopoverTrigger
  placement="bottom"
  shouldFlip={false}
  label="shouldFlip=false"
>
  <Dialog>
    This is a popover that won't flip if it can't fully
    render below the button.
  </Dialog>
</PopoverTrigger>
```

```
<PopoverTrigger
  placement="bottom"
  label="Default"
>
  <Dialog>
    This is a popover
    that will flip if
    it can't fully
    render below the
    button.
  </Dialog>
</PopoverTrigger>
 <PopoverTrigger
  placement="bottom"
  shouldFlip={false}
  label="shouldFlip=false"
>
  <Dialog>
    This is a popover
    that won't flip if
    it can't fully
    render below the
    button.
  </Dialog>
</PopoverTrigger>
```

### Container padding[#](#container-padding)

You can control the minimum padding required between the popover and the
surrounding container via the `containerPadding` prop. This affects the positioning
breakpoints that determine when it will attempt to flip.

The example below will maintain at least 50px between the popover and the edge of the browser window.

```
<PopoverTrigger placement="top" containerPadding={50} label="Trigger">
  <Dialog>
    This is a popover.
  </Dialog>
</PopoverTrigger>
```

```
<PopoverTrigger
  placement="top"
  containerPadding={50}
  label="Trigger"
>
  <Dialog>
    This is a popover.
  </Dialog>
</PopoverTrigger>
```

```
<PopoverTrigger
  placement="top"
  containerPadding={50}
  label="Trigger"
>
  <Dialog>
    This is a popover.
  </Dialog>
</PopoverTrigger>
```

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

| Name | Type | Description |
| --- | --- | --- |
| `current` | `T` |  |

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
| `popoverProps` | `DOMAttributes` | Props for the popover element. |
| `arrowProps` | `DOMAttributes` | Props for the popover tip arrow if any. |
| `underlayProps` | `DOMAttributes` | Props to apply to the underlay element, if any. |
| `placement` | `PlacementAxis |Â null` | Placement of the popover with respect to the trigger. |
| `triggerAnchorPoint` | `{ x: number,  y: number } |Â null` | The origin of the target in the overlay's coordinate system. Useful for animations. |

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

`Axis |Â 'center'`

`'top'
|Â 'bottom'
|Â 'left'
|Â 'right'`

Provides the behavior and accessibility implementation for a popover component.
A popover is an overlay element positioned relative to a trigger.

`usePopover(
(props: AriaPopoverProps,
, state: OverlayTriggerState
)): PopoverAria`

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

Provides the behavior and accessibility implementation for a dialog component.
A dialog is an overlay shown above other content in an application.

`useDialog(
(props: AriaDialogProps,
, ref: RefObject<FocusableElement
|Â  |Â null>
)): DialogAria`

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
| `dialogProps` | `DOMAttributes` | Props for the dialog container element. |
| `titleProps` | `DOMAttributes` | Props for the dialog title element. |

A container which renders an overlay such as a popover or modal in a portal,
and provides a focus scope for the child elements.

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `children` | `ReactNode` | â | The overlay to render in the portal. |
| `portalContainer` | `Element` | `document.body` | The container element in which the overlay portal will be placed. |
| `disableFocusManagement` | `boolean` | â | Disables default focus management for the overlay, including containment and restoration. This option should be used very carefully. When focus management is disabled, you must implement focus containment and restoration to ensure the overlay is keyboard accessible. |
| `shouldContainFocus` | `boolean` | â | Whether to contain focus within the overlay. |
| `isExiting` | `boolean` | â | Whether the overlay is currently performing an exit animation. When true, focus is allowed to move outside. |

A visually hidden button that can be used to allow screen reader
users to dismiss a modal or popup when there is no visual
affordance to do so.

| Name | Type | Description |
| --- | --- | --- |
| `onDismiss` | `() => void` | Called when the dismiss button is activated. |
| `aria-label` | `string` | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | Identifies the element (or elements) that provide a detailed, extended description for the object. |
| `id` | `string` | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |

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