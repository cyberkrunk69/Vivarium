# useToast

Source: https://react-spectrum.adobe.com/react-aria/useToast.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../Toast).

# useToast

Provides the behavior and accessibility implementation for a toast component.
Toasts display brief, temporary notifications of actions, errors, or other events in an application.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useToastRegion, useToast} from 'react-aria'` |

[View ARIA pattern

W3C](https://www.w3.org/WAI/ARIA/apg/patterns/alertdialog/ "View ARIA pattern")[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/toast "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/toast "View package")

## API[#](#api)

---

`useToastRegion<T>(
props: AriaToastRegionProps,
state: ToastState<T>,
ref: RefObject<HTMLElement
|Â  |Â null>
): ToastRegionAria`
`useToast<T>(
props: AriaToastProps<T>,
state: ToastState<T>,
ref: RefObject<FocusableElement
|Â  |Â null>
): ToastAria`

## Features[#](#features)

---

There is no built in way to display toast notifications in HTML. `useToastRegion` and `useToast` help achieve accessible toasts that can be styled as needed.

- **Accessible** â Toasts follow the [ARIA alertdialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/alertdialog/). They are rendered in a [landmark region](https://www.w3.org/WAI/ARIA/apg/practices/landmark-regions/), which keyboard and screen reader users can easily jump to when an alert is announced.
- **Focus management** â When a toast unmounts, focus is moved to the next toast if any. Otherwise, focus is restored to where it was before navigating to the toast region. Tabbing through the Toast region will move from newest to oldest.

## Anatomy[#](#anatomy)

---

A toast region is an [ARIA landmark region](https://www.w3.org/WAI/ARIA/apg/practices/landmark-regions/) labeled "Notifications" by default. A toast region contains one or more visible toasts, in chronological order. When the limit is reached, additional toasts are queued until the user dismisses one. Each toast is a non-modal ARIA [alertdialog](https://www.w3.org/WAI/ARIA/apg/patterns/alertdialog/), containing the content of the notification and a close button.

Landmark regions including the toast container can be navigated using the keyboard by pressing the `F6` key to move forward, and the `Shift` + `F6` key to move backward. This provides an easy way for keyboard users to jump to the toasts from anywhere in the app. When the last toast is closed, keyboard focus is restored.

`useToastRegion` returns props that you should spread onto the toast container element:

| Name | Type | Description |
| --- | --- | --- |
| `regionProps` | `DOMAttributes` | Props for the landmark region element. |

`useToast` returns props that you should spread onto an individual toast and its child elements:

| Name | Type | Description |
| --- | --- | --- |
| `toastProps` | `DOMAttributes` | Props for the toast container, non-modal dialog element. |
| `contentProps` | `DOMAttributes` | Props for the toast content alert message. |
| `titleProps` | `DOMAttributes` | Props for the toast title element. |
| `descriptionProps` | `DOMAttributes` | Props for the toast description element, if any. |
| `closeButtonProps` | `AriaButtonProps` | Props for the toast close button. |

## Example[#](#example)

---

Toasts consist of three components. The first is a `ToastProvider` component which will manage the state for the toast queue with the `useToastState` hook. Alternatively, you could use a global toast queue ([see below](#global-toast-queue)).

```
import {useToastState} from 'react-stately';

function ToastProvider({ children, ...props }) {
  let state = useToastState({
    maxVisibleToasts: 5
  });

  return (
    <>
      {children(state)}
      {state.visibleToasts.length > 0 && (
        <ToastRegion {...props} state={state} />
      )}
    </>
  );
}
```

```
import {useToastState} from 'react-stately';

function ToastProvider({ children, ...props }) {
  let state = useToastState({
    maxVisibleToasts: 5
  });

  return (
    <>
      {children(state)}
      {state.visibleToasts.length > 0 && (
        <ToastRegion {...props} state={state} />
      )}
    </>
  );
}
```

```
import {useToastState} from 'react-stately';

function ToastProvider(
  { children, ...props }
) {
  let state =
    useToastState({
      maxVisibleToasts: 5
    });

  return (
    <>
      {children(state)}
      {state
            .visibleToasts
            .length >
          0 && (
        <ToastRegion
          {...props}
          state={state}
        />
      )}
    </>
  );
}
```

The `ToastRegion` component will be rendered when there are toasts to display. It uses the `useToastRegion` hook to create a landmark region, allowing keyboard and screen reader users to easily navigate to it.

```
import type {ToastState} from 'react-stately';
import type {AriaToastRegionProps} from 'react-aria';
import {useToastRegion} from 'react-aria';

interface ToastRegionProps<T> extends AriaToastRegionProps {
  state: ToastState<T>;
}

function ToastRegion<T extends React.ReactNode>(
  { state, ...props }: ToastRegionProps<T>
) {
  let ref = React.useRef(null);
  let { regionProps } = useToastRegion(props, state, ref);

  return (
    <div {...regionProps} ref={ref} className="toast-region">
      {state.visibleToasts.map((toast) => (
        <Toast key={toast.key} toast={toast} state={state} />
      ))}
    </div>
  );
}
```

```
import type {ToastState} from 'react-stately';
import type {AriaToastRegionProps} from 'react-aria';
import {useToastRegion} from 'react-aria';

interface ToastRegionProps<T> extends AriaToastRegionProps {
  state: ToastState<T>;
}

function ToastRegion<T extends React.ReactNode>(
  { state, ...props }: ToastRegionProps<T>
) {
  let ref = React.useRef(null);
  let { regionProps } = useToastRegion(props, state, ref);

  return (
    <div
      {...regionProps}
      ref={ref}
      className="toast-region"
    >
      {state.visibleToasts.map((toast) => (
        <Toast
          key={toast.key}
          toast={toast}
          state={state}
        />
      ))}
    </div>
  );
}
```

```
import type {ToastState} from 'react-stately';
import type {AriaToastRegionProps} from 'react-aria';
import {useToastRegion} from 'react-aria';

interface ToastRegionProps<
  T
> extends
  AriaToastRegionProps {
  state: ToastState<T>;
}

function ToastRegion<
  T
    extends React.ReactNode
>(
  { state, ...props }:
    ToastRegionProps<T>
) {
  let ref = React.useRef(
    null
  );
  let { regionProps } =
    useToastRegion(
      props,
      state,
      ref
    );

  return (
    <div
      {...regionProps}
      ref={ref}
      className="toast-region"
    >
      {state
        .visibleToasts
        .map((toast) => (
          <Toast
            key={toast
              .key}
            toast={toast}
            state={state}
          />
        ))}
    </div>
  );
}
```

Finally, we need the `Toast` component to render an individual toast within a `ToastRegion`, built with `useToast`.

```
import type {AriaToastProps} from 'react-aria';
import {useToast} from 'react-aria';

// Reuse the Button from your component library. See below for details.
import {Button} from 'your-component-library';

interface ToastProps<T> extends AriaToastProps<T> {
  state: ToastState<T>;
}

function Toast<T extends React.ReactNode>({ state, ...props }: ToastProps<T>) {
  let ref = React.useRef(null);
  let { toastProps, contentProps, titleProps, closeButtonProps } = useToast(
    props,
    state,
    ref
  );

  return (
    <div {...toastProps} ref={ref} className="toast">
      <div {...contentProps}>
        <div {...titleProps}>{props.toast.content}</div>
      </div>
      <Button {...closeButtonProps}>x</Button>
    </div>
  );
}
```

```
import type {AriaToastProps} from 'react-aria';
import {useToast} from 'react-aria';

// Reuse the Button from your component library. See below for details.
import {Button} from 'your-component-library';

interface ToastProps<T> extends AriaToastProps<T> {
  state: ToastState<T>;
}

function Toast<T extends React.ReactNode>(
  { state, ...props }: ToastProps<T>
) {
  let ref = React.useRef(null);
  let {
    toastProps,
    contentProps,
    titleProps,
    closeButtonProps
  } = useToast(props, state, ref);

  return (
    <div {...toastProps} ref={ref} className="toast">
      <div {...contentProps}>
        <div {...titleProps}>{props.toast.content}</div>
      </div>
      <Button {...closeButtonProps}>x</Button>
    </div>
  );
}
```

```
import type {AriaToastProps} from 'react-aria';
import {useToast} from 'react-aria';

// Reuse the Button from your component library. See below for details.
import {Button} from 'your-component-library';

interface ToastProps<T>
  extends
    AriaToastProps<T> {
  state: ToastState<T>;
}

function Toast<
  T
    extends React.ReactNode
>(
  { state, ...props }:
    ToastProps<T>
) {
  let ref = React.useRef(
    null
  );
  let {
    toastProps,
    contentProps,
    titleProps,
    closeButtonProps
  } = useToast(
    props,
    state,
    ref
  );

  return (
    <div
      {...toastProps}
      ref={ref}
      className="toast"
    >
      <div
        {...contentProps}
      >
        <div
          {...titleProps}
        >
          {props.toast
            .content}
        </div>
      </div>
      <Button
        {...closeButtonProps}
      >
        x
      </Button>
    </div>
  );
}
```

```
<ToastProvider>
  {state => (
    <Button onPress={() => state.add('Toast is done!')}>Show toast</Button>
  )}
</ToastProvider>
```

```
<ToastProvider>
  {(state) => (
    <Button onPress={() => state.add('Toast is done!')}>
      Show toast
    </Button>
  )}
</ToastProvider>
```

```
<ToastProvider>
  {(state) => (
    <Button
      onPress={() =>
        state.add(
          'Toast is done!'
        )}
    >
      Show toast
    </Button>
  )}
</ToastProvider>
```

 Show CSS

```
.toast-region {
  position: fixed;
  bottom: 16px;
  right: 16px;
  display: flex;
  flex-direction: column-reverse;
  gap: 8px;
}

.toast {
  display: flex;
  align-items: center;
  gap: 16px;
  background: slateblue;
  color: white;
  padding: 12px 16px;
  border-radius: 8px;
}

.toast button {
  background: none;
  border: none;
  appearance: none;
  border-radius: 50%;
  height: 32px;
  width: 32px;
  font-size: 16px;
  border: 1px solid white;
  color: white;
  padding: 0;
}

.toast button:focus-visible {
  outline: none;
  box-shadow: 0 0 0 2px slateblue, 0 0 0 4px white;
}

.toast button:active {
  background: rgba(255, 255, 255, 0.2);
}
```

```
.toast-region {
  position: fixed;
  bottom: 16px;
  right: 16px;
  display: flex;
  flex-direction: column-reverse;
  gap: 8px;
}

.toast {
  display: flex;
  align-items: center;
  gap: 16px;
  background: slateblue;
  color: white;
  padding: 12px 16px;
  border-radius: 8px;
}

.toast button {
  background: none;
  border: none;
  appearance: none;
  border-radius: 50%;
  height: 32px;
  width: 32px;
  font-size: 16px;
  border: 1px solid white;
  color: white;
  padding: 0;
}

.toast button:focus-visible {
  outline: none;
  box-shadow: 0 0 0 2px slateblue, 0 0 0 4px white;
}

.toast button:active {
  background: rgba(255, 255, 255, 0.2);
}
```

```
.toast-region {
  position: fixed;
  bottom: 16px;
  right: 16px;
  display: flex;
  flex-direction: column-reverse;
  gap: 8px;
}

.toast {
  display: flex;
  align-items: center;
  gap: 16px;
  background: slateblue;
  color: white;
  padding: 12px 16px;
  border-radius: 8px;
}

.toast button {
  background: none;
  border: none;
  appearance: none;
  border-radius: 50%;
  height: 32px;
  width: 32px;
  font-size: 16px;
  border: 1px solid white;
  color: white;
  padding: 0;
}

.toast button:focus-visible {
  outline: none;
  box-shadow: 0 0 0 2px slateblue, 0 0 0 4px white;
}

.toast button:active {
  background: rgba(255, 255, 255, 0.2);
}
```

### Button[#](#button)

The `Button` component is used in the above example to close a toast. It is built using the [useButton](../Button/useButton.html) hook, and can be shared with many other components.

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

The following examples show how to use the `ToastProvider` component created in the above example.

### Auto-dismiss[#](#auto-dismiss)

Toasts support a `timeout` option to automatically hide them after a certain amount of time. For accessibility, toasts should have a minimum timeout of 5 seconds to give users enough time to read them. If a toast includes action buttons or other interactive elements it should not auto dismiss. In addition, timers will automatically pause when the user focuses or hovers over a toast.

Be sure only to automatically dismiss toasts when the information is not important, or may be found elsewhere. Some users may require additional time to read a toast message, and screen zoom users may miss toasts entirely.

```
<ToastProvider>
  {state => (
    <Button onPress={() => state.add('Toast still toasting!', {timeout: 5000})}>      Show toast
    </Button>
  )}
</ToastProvider>
```

```
<ToastProvider>
  {(state) => (
    <Button
      onPress={() =>
        state.add('Toast still toasting!', {
          timeout: 5000
        })}
    >      Show toast
    </Button>
  )}
</ToastProvider>
```

```
<ToastProvider>
  {(state) => (
    <Button
      onPress={() =>
        state.add(
          'Toast still toasting!',
          {
            timeout:
              5000
          }
        )}
    >      Show toast
    </Button>
  )}
</ToastProvider>
```

### Programmatic dismissal[#](#programmatic-dismissal)

Toasts may be programmatically dismissed if they become irrelevant before the user manually closes them. `state.add` returns a key for the toast which may be passed to `state.close` to dismiss the toast.

```
function Example() {
  let [toastKey, setToastKey] = React.useState(null);

  return (
    <ToastProvider>
      {(state) => (
        <Button
          onPress={() => {
            if (!toastKey) {
              setToastKey(
                state.add('Unable to save', {
                  onClose: () => setToastKey(null)
                })
              );            } else {
              state.close(toastKey);            }
          }}
        >
          {toastKey ? 'Hide' : 'Show'} Toast
        </Button>
      )}
    </ToastProvider>
  );
}
```

```
function Example() {
  let [toastKey, setToastKey] = React.useState(null);

  return (
    <ToastProvider>
      {(state) => (
        <Button
          onPress={() => {
            if (!toastKey) {
              setToastKey(
                state.add('Unable to save', {
                  onClose: () => setToastKey(null)
                })
              );            } else {
              state.close(toastKey);            }
          }}
        >
          {toastKey ? 'Hide' : 'Show'} Toast
        </Button>
      )}
    </ToastProvider>
  );
}
```

```
function Example() {
  let [
    toastKey,
    setToastKey
  ] = React.useState(
    null
  );

  return (
    <ToastProvider>
      {(state) => (
        <Button
          onPress={() => {
            if (
              !toastKey
            ) {
              setToastKey(
                state
                  .add(
                    'Unable to save',
                    {
                      onClose:
                        () =>
                          setToastKey(
                            null
                          )
                    }
                  )
              );            } else {
              state
                .close(
                  toastKey
                );            }
          }}
        >
          {toastKey
            ? 'Hide'
            : 'Show'}
          {' '}
          Toast
        </Button>
      )}
    </ToastProvider>
  );
}
```

## Advanced topics[#](#advanced-topics)

---

### Global toast queue[#](#global-toast-queue)

In the above examples, each `ToastProvider` has a separate queue. This setup is simple, and fine for most cases where you can wrap the entire app in a single `ToastProvider`. However, in more complex situations, you may want to keep the toast queue outside the React tree so that toasts can be queued from anywhere. This can be done by creating your own `ToastQueue` and subscribing to it using the `useToastQueue` hook rather than `useToastState`.

```
import {ToastQueue, useToastQueue} from 'react-stately';
import {createPortal} from 'react-dom';

// Create a global toast queue.
const toastQueue = new ToastQueue({
  maxVisibleToasts: 5
});
function GlobalToastRegion(props) {
  // Subscribe to it.
  let state = useToastQueue(toastQueue);
  // Render toast region.
  return state.visibleToasts.length > 0
    ? createPortal(<ToastRegion {...props} state={state} />, document.body)
    : null;
}

// Render it somewhere in your app.
<GlobalToastRegion />
```

```
import {ToastQueue, useToastQueue} from 'react-stately';
import {createPortal} from 'react-dom';

// Create a global toast queue.
const toastQueue = new ToastQueue({
  maxVisibleToasts: 5
});
function GlobalToastRegion(props) {
  // Subscribe to it.
  let state = useToastQueue(toastQueue);
  // Render toast region.
  return state.visibleToasts.length > 0
    ? createPortal(
      <ToastRegion {...props} state={state} />,
      document.body
    )
    : null;
}

// Render it somewhere in your app.
<GlobalToastRegion />
```

```
import {
  ToastQueue,
  useToastQueue
} from 'react-stately';
import {createPortal} from 'react-dom';

// Create a global toast queue.
const toastQueue =
  new ToastQueue({
    maxVisibleToasts: 5
  });
function GlobalToastRegion(
  props
) {
  // Subscribe to it.
  let state =
    useToastQueue(
      toastQueue
    );
  // Render toast region.
  return state
      .visibleToasts
      .length > 0
    ? createPortal(
      <ToastRegion
        {...props}
        state={state}
      />,
      document.body
    )
    : null;
}

// Render it somewhere in your app.
<GlobalToastRegion />
```

Now you can queue a toast from anywhere:

```
<Button onPress={() => toastQueue.add('Toast is done!')}>Show toast</Button>
```

```
<Button onPress={() => toastQueue.add('Toast is done!')}>
  Show toast
</Button>
```

```
<Button
  onPress={() =>
    toastQueue.add(
      'Toast is done!'
    )}
>
  Show toast
</Button>
```

### TypeScript[#](#typescript)

A `ToastQueue` and `useToastState` use a generic type to represent toast content. The examples so far have used strings, but you can type this however you want to enable passing custom objects or options. This example uses a custom object to support toasts with both a title and description.

```
import type {QueuedToast} from 'react-stately';

interface MyToast {
  title: string;
  description: string;
}
function ToastProvider() {
  let state = useToastState<MyToast>();
  // ...
}

interface ToastProps {
  toast: QueuedToast<MyToast>;}

function Toast(props: ToastProps) {
  // ...

  let { toastProps, titleProps, descriptionProps, closeButtonProps } = useToast(
    props,
    state,
    ref
  );

  return (
    <div {...toastProps} ref={ref} className="toast">
      <div>
        <div {...titleProps}>{props.toast.content.title}</div>
        <div {...descriptionProps}>{props.toast.content.description}</div>      </div>
      <Button {...closeButtonProps}>x</Button>
    </div>
  );
}

// Queuing a toast
state.add({ title: 'Success!', description: 'Toast is done.' });
```

```
import type {QueuedToast} from 'react-stately';

interface MyToast {
  title: string;
  description: string;
}
function ToastProvider() {
  let state = useToastState<MyToast>();
  // ...
}

interface ToastProps {
  toast: QueuedToast<MyToast>;}

function Toast(props: ToastProps) {
  // ...

  let {
    toastProps,
    titleProps,
    descriptionProps,
    closeButtonProps
  } = useToast(props, state, ref);

  return (
    <div {...toastProps} ref={ref} className="toast">
      <div>
        <div {...titleProps}>
          {props.toast.content.title}
        </div>
        <div {...descriptionProps}>
          {props.toast.content.description}
        </div>      </div>
      <Button {...closeButtonProps}>x</Button>
    </div>
  );
}

// Queuing a toast
state.add({
  title: 'Success!',
  description: 'Toast is done.'
});
```

```
import type {QueuedToast} from 'react-stately';

interface MyToast {
  title: string;
  description: string;
}
function ToastProvider() {
  let state =
    useToastState<
      MyToast
    >();
  // ...
}

interface ToastProps {
  toast: QueuedToast<
    MyToast
  >;}

function Toast(
  props: ToastProps
) {
  // ...

  let {
    toastProps,
    titleProps,
    descriptionProps,
    closeButtonProps
  } = useToast(
    props,
    state,
    ref
  );

  return (
    <div
      {...toastProps}
      ref={ref}
      className="toast"
    >
      <div>
        <div
          {...titleProps}
        >
          {props.toast
            .content
            .title}
        </div>
        <div
          {...descriptionProps}
        >
          {props.toast
            .content
            .description}
        </div>      </div>
      <Button
        {...closeButtonProps}
      >
        x
      </Button>
    </div>
  );
}

// Queuing a toast
state.add({
  title: 'Success!',
  description:
    'Toast is done.'
});
```

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `aria-label` | `string` | `"Notifications"` | An accessibility label for the toast region. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `visibleToasts` | `QueuedToast<T>[]` | The visible toasts. |

### Methods

| Method | Description |
| --- | --- |
| `add( (content: T, , options?: ToastOptions )): string` | Adds a new toast to the queue. |
| `close( (key: string )): void` | Closes a toast. |
| `pauseAll(): void` | Pauses the timers for all visible toasts. |
| `resumeAll(): void` | Resumes the timers for all visible toasts. |

| Name | Type | Description |
| --- | --- | --- |
| `onClose` | `() => void` | Handler that is called when the toast is closed, either by the user or after a timeout. |
| `timeout` | `number` | A timeout to automatically close the toast after, in milliseconds. |

| Name | Type | Description |
| --- | --- | --- |
| `content` | `T` | The content of the toast. |
| `key` | `string` | A unique key for the toast. |
| `timer` | `Timer` | A timer for the toast, if a timeout was set. |
| `onClose` | `() => void` | Handler that is called when the toast is closed, either by the user or after a timeout. |
| `timeout` | `number` | A timeout to automatically close the toast after, in milliseconds. |

| Method | Description |
| --- | --- |
| `constructor( (callback: () => void, , delay: number )): void` |  |
| `reset( (delay: number )): void` |  |
| `pause(): void` |  |
| `resume(): void` |  |

| Name | Type | Description |
| --- | --- | --- |
| `current` | `T` |  |

| Name | Type | Description |
| --- | --- | --- |
| `regionProps` | `DOMAttributes` | Props for the landmark region element. |

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
| `toast` | `QueuedToast<T>` | The toast object. |
| `aria-label` | `string` | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | Identifies the element (or elements) that provide a detailed, extended description for the object. |

| Name | Type | Description |
| --- | --- | --- |
| `toastProps` | `DOMAttributes` | Props for the toast container, non-modal dialog element. |
| `contentProps` | `DOMAttributes` | Props for the toast content alert message. |
| `titleProps` | `DOMAttributes` | Props for the toast title element. |
| `descriptionProps` | `DOMAttributes` | Props for the toast description element, if any. |
| `closeButtonProps` | `AriaButtonProps` | Props for the toast close button. |

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

Provides the behavior and accessibility implementation for a toast region containing one or more toasts.
Toasts display brief, temporary notifications of actions, errors, or other events in an application.

`useToastRegion<T>(
props: AriaToastRegionProps,
state: ToastState<T>,
ref: RefObject<HTMLElement
|Â  |Â null>
): ToastRegionAria`

Provides the behavior and accessibility implementation for a toast component.
Toasts display brief, temporary notifications of actions, errors, or other events in an application.

`useToast<T>(
props: AriaToastProps<T>,
state: ToastState<T>,
ref: RefObject<FocusableElement
|Â  |Â null>
): ToastAria`

Provides state management for a toast queue. Toasts display brief, temporary notifications
of actions, errors, or other events in an application.

`useToastState<T>(
(props: ToastStateProps
)): ToastState<T>`

| Name | Type | Description |
| --- | --- | --- |
| `maxVisibleToasts` | `number` | The maximum number of toasts to display at a time. |
| `wrapUpdate` | `( (fn: () => void, , action: ToastAction )) => void` | Function to wrap updates in (i.e. document.startViewTransition()). |

`'add'
|Â 'remove'
|Â 'clear'`

A ToastQueue manages the order of toasts.

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `visibleToasts` | `QueuedToast<T>[]` | The currently visible toasts. |

### Methods

| Method | Description |
| --- | --- |
| `constructor( (options?: ToastStateProps )): void` |  |
| `subscribe( (fn: () => void )): () => void` | Subscribes to updates to the visible toasts. |
| `add( (content: T, , options: ToastOptions )): string` | Adds a new toast to the queue. |
| `close( (key: string )): void` | Closes a toast. |
| `pauseAll(): void` | Pauses the timers for all visible toasts. |
| `resumeAll(): void` | Resumes the timers for all visible toasts. |
| `clear(): void` |  |

Subscribes to a provided toast queue and provides methods to update it.

`useToastQueue<T>(
(queue: ToastQueue<T>
)): ToastState<T>`