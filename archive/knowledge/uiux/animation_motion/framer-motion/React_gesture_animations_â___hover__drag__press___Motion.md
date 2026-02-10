# React gesture animations â hover, drag, press | Motion

Source: https://www.framer.com/motion/gestures/

---

Motion extends React's basic set of event listeners with a simple yet powerful set of UI gestures.

The `motion` component currently has support for [**hover**](./react-hover-animation), **tap**, **pan**, **drag, focus** and [**inView**](./react-scroll-animations).

Each gesture has both a set of event listeners and a `while-` animation prop.

## [Animation props](#animation-props)

`motion` components provide multiple gesture animation props: `whileHover`, `whileTap`, `whileFocus`, `whileDrag` and `whileInView`. These can define animation targets to temporarily animate to while a gesture is active.

```
<motion.button
  whileHover={{
    scale: 1.2,
    transition: { duration: 1 },
  }}
  whileTap={{ scale: 0.9 }}
/>
```

All props can be set either as a target of values to animate to, or the name of any variants defined via the `variants` prop. Variants will flow down through children as normal.

```
<motion.button
  whileTap="tap"
  whileHover="hover"
  variants={buttonVariants}
>
  <svg>
    <motion.path variants={iconVariants} />
  </svg>
</motion.button>
```

## [Gestures](#gestures)

### [Hover](#hover)

The hover gesture detects when a pointer hovers over or leaves a component. [Learn more about hover animations.](./react-hover-animation)

```
<motion.a
  whileHover={{ scale: 1.2 }}
  onHoverStart={event => {}}
  onHoverEnd={event => {}}
/>
```

### [Tap](#tap)

The tap gesture detects when the **primary pointer** (like a left click or first touch point) presses down and releases on the same component.

```
<motion.button whileTap={{ scale: 0.9, rotate: 3 }} />
```

It will fire a `tap` event when the tap or click ends on the same component it started on, and a `tapCancel` event if the tap or click ends outside the component.

If the tappable component is a child of a draggable component, it'll automatically cancel the tap gesture if the pointer moves further than 3 pixels during the gesture.

#### [Accessibility](#accessibility)

Elements with tap events are keyboard-accessible.

Any element with a tap prop will be able to receive focus and `Enter` can be used to trigger tap events on focused elements.

- Pressing `Enter` down will trigger `onTapStart` and `whileTap`
- Releasing `Enter` will trigger `onTap`
- If the element loses focus before `Enter` is released, `onTapCancel` will fire.

### [Pan](#pan)

The pan gesture recognises when a pointer presses down on a component and moves further than 3 pixels. The pan gesture is ended when the pointer is released.

```
<motion.div onPan={(e, pointInfo) => {}} />
```

Pan doesn't currently have an associated `while-` prop.

For pan gestures to work correctly with touch input, the element needs touch scrolling to be disabled on either x/y or both axis with the `touch-action` CSS rule.

### [Drag](#drag)

The drag gesture applies pointer movement to the x and/or y axis of the component.

```
<motion.div drag whileDrag={{ scale: 1.2, backgroundColor: "#f00" }} />
```

[Learn more about drag animations](./react-drag).

### [Focus](#focus)

The focus gesture detects when a component gains or loses focus by the same rules as the [CSS :focus-visible selector](https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-visible).

Typically, this is when an `input` receives focus by any means, and when other elements receive focus by accessible means (like via keyboard navigation).

```
<motion.a whileFocus={{ scale: 1.2 }} href="#" />
```

## [Event propagation](#event-propagation)

Children can stop pointer events propagating to parent `motion` components using the `Capture` React props.

For instance, a child can stop drag and tap gestures and their related `while` animations from firing on parents by passing `e.stopPropagation()` to `onPointerDownCapture`.

```
<motion.div whileTap={{ scale: 2 }}>
  <button onPointerDownCapture={e => e.stopPropagation()} />
</motion.div>
```

## [Note: SVG filters](#note-svg-filters)

Gestures aren't recognised on SVG `filter` components, as these elements don't have a physical presence and therefore don't receive events.

You can instead add `while-` props and event handlers to a parent and use variants to animate these elements.

```
const MyComponent = () => {
  return (
    <motion.svg whileHover="hover">
      <filter id="blur">
        <motion.feGaussianBlur
          stdDeviation={0}
          variants={{ hover: { stdDeviation: 2 } }}
        />
      </filter>
    </motion.svg>
  )
}
```

Motion extends React's basic set of event listeners with a simple yet powerful set of UI gestures.

The `motion` component currently has support for [**hover**](./react-hover-animation), **tap**, **pan**, **drag, focus** and [**inView**](./react-scroll-animations).

Each gesture has both a set of event listeners and a `while-` animation prop.

## [Animation props](#animation-props)

`motion` components provide multiple gesture animation props: `whileHover`, `whileTap`, `whileFocus`, `whileDrag` and `whileInView`. These can define animation targets to temporarily animate to while a gesture is active.

```
<motion.button
  whileHover={{
    scale: 1.2,
    transition: { duration: 1 },
  }}
  whileTap={{ scale: 0.9 }}
/>
```

All props can be set either as a target of values to animate to, or the name of any variants defined via the `variants` prop. Variants will flow down through children as normal.

```
<motion.button
  whileTap="tap"
  whileHover="hover"
  variants={buttonVariants}
>
  <svg>
    <motion.path variants={iconVariants} />
  </svg>
</motion.button>
```

## [Gestures](#gestures)

### [Hover](#hover)

The hover gesture detects when a pointer hovers over or leaves a component. [Learn more about hover animations.](./react-hover-animation)

```
<motion.a
  whileHover={{ scale: 1.2 }}
  onHoverStart={event => {}}
  onHoverEnd={event => {}}
/>
```

### [Tap](#tap)

The tap gesture detects when the **primary pointer** (like a left click or first touch point) presses down and releases on the same component.

```
<motion.button whileTap={{ scale: 0.9, rotate: 3 }} />
```

It will fire a `tap` event when the tap or click ends on the same component it started on, and a `tapCancel` event if the tap or click ends outside the component.

If the tappable component is a child of a draggable component, it'll automatically cancel the tap gesture if the pointer moves further than 3 pixels during the gesture.

#### [Accessibility](#accessibility)

Elements with tap events are keyboard-accessible.

Any element with a tap prop will be able to receive focus and `Enter` can be used to trigger tap events on focused elements.

- Pressing `Enter` down will trigger `onTapStart` and `whileTap`
- Releasing `Enter` will trigger `onTap`
- If the element loses focus before `Enter` is released, `onTapCancel` will fire.

### [Pan](#pan)

The pan gesture recognises when a pointer presses down on a component and moves further than 3 pixels. The pan gesture is ended when the pointer is released.

```
<motion.div onPan={(e, pointInfo) => {}} />
```

Pan doesn't currently have an associated `while-` prop.

For pan gestures to work correctly with touch input, the element needs touch scrolling to be disabled on either x/y or both axis with the `touch-action` CSS rule.

### [Drag](#drag)

The drag gesture applies pointer movement to the x and/or y axis of the component.

```
<motion.div drag whileDrag={{ scale: 1.2, backgroundColor: "#f00" }} />
```

[Learn more about drag animations](./react-drag).

### [Focus](#focus)

The focus gesture detects when a component gains or loses focus by the same rules as the [CSS :focus-visible selector](https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-visible).

Typically, this is when an `input` receives focus by any means, and when other elements receive focus by accessible means (like via keyboard navigation).

```
<motion.a whileFocus={{ scale: 1.2 }} href="#" />
```

## [Event propagation](#event-propagation)

Children can stop pointer events propagating to parent `motion` components using the `Capture` React props.

For instance, a child can stop drag and tap gestures and their related `while` animations from firing on parents by passing `e.stopPropagation()` to `onPointerDownCapture`.

```
<motion.div whileTap={{ scale: 2 }}>
  <button onPointerDownCapture={e => e.stopPropagation()} />
</motion.div>
```

## [Note: SVG filters](#note-svg-filters)

Gestures aren't recognised on SVG `filter` components, as these elements don't have a physical presence and therefore don't receive events.

You can instead add `while-` props and event handlers to a parent and use variants to animate these elements.

```
const MyComponent = () => {
  return (
    <motion.svg whileHover="hover">
      <filter id="blur">
        <motion.feGaussianBlur
          stdDeviation={0}
          variants={{ hover: { stdDeviation: 2 } }}
        />
      </filter>
    </motion.svg>
  )
}
```

Motion extends React's basic set of event listeners with a simple yet powerful set of UI gestures.

The `motion` component currently has support for [**hover**](./react-hover-animation), **tap**, **pan**, **drag, focus** and [**inView**](./react-scroll-animations).

Each gesture has both a set of event listeners and a `while-` animation prop.

## [Animation props](#animation-props)

`motion` components provide multiple gesture animation props: `whileHover`, `whileTap`, `whileFocus`, `whileDrag` and `whileInView`. These can define animation targets to temporarily animate to while a gesture is active.

```
<motion.button
  whileHover={{
    scale: 1.2,
    transition: { duration: 1 },
  }}
  whileTap={{ scale: 0.9 }}
/>
```

All props can be set either as a target of values to animate to, or the name of any variants defined via the `variants` prop. Variants will flow down through children as normal.

```
<motion.button
  whileTap="tap"
  whileHover="hover"
  variants={buttonVariants}
>
  <svg>
    <motion.path variants={iconVariants} />
  </svg>
</motion.button>
```

## [Gestures](#gestures)

### [Hover](#hover)

The hover gesture detects when a pointer hovers over or leaves a component. [Learn more about hover animations.](./react-hover-animation)

```
<motion.a
  whileHover={{ scale: 1.2 }}
  onHoverStart={event => {}}
  onHoverEnd={event => {}}
/>
```

### [Tap](#tap)

The tap gesture detects when the **primary pointer** (like a left click or first touch point) presses down and releases on the same component.

```
<motion.button whileTap={{ scale: 0.9, rotate: 3 }} />
```

It will fire a `tap` event when the tap or click ends on the same component it started on, and a `tapCancel` event if the tap or click ends outside the component.

If the tappable component is a child of a draggable component, it'll automatically cancel the tap gesture if the pointer moves further than 3 pixels during the gesture.

#### [Accessibility](#accessibility)

Elements with tap events are keyboard-accessible.

Any element with a tap prop will be able to receive focus and `Enter` can be used to trigger tap events on focused elements.

- Pressing `Enter` down will trigger `onTapStart` and `whileTap`
- Releasing `Enter` will trigger `onTap`
- If the element loses focus before `Enter` is released, `onTapCancel` will fire.

### [Pan](#pan)

The pan gesture recognises when a pointer presses down on a component and moves further than 3 pixels. The pan gesture is ended when the pointer is released.

```
<motion.div onPan={(e, pointInfo) => {}} />
```

Pan doesn't currently have an associated `while-` prop.

For pan gestures to work correctly with touch input, the element needs touch scrolling to be disabled on either x/y or both axis with the `touch-action` CSS rule.

### [Drag](#drag)

The drag gesture applies pointer movement to the x and/or y axis of the component.

```
<motion.div drag whileDrag={{ scale: 1.2, backgroundColor: "#f00" }} />
```

[Learn more about drag animations](./react-drag).

### [Focus](#focus)

The focus gesture detects when a component gains or loses focus by the same rules as the [CSS :focus-visible selector](https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-visible).

Typically, this is when an `input` receives focus by any means, and when other elements receive focus by accessible means (like via keyboard navigation).

```
<motion.a whileFocus={{ scale: 1.2 }} href="#" />
```

## [Event propagation](#event-propagation)

Children can stop pointer events propagating to parent `motion` components using the `Capture` React props.

For instance, a child can stop drag and tap gestures and their related `while` animations from firing on parents by passing `e.stopPropagation()` to `onPointerDownCapture`.

```
<motion.div whileTap={{ scale: 2 }}>
  <button onPointerDownCapture={e => e.stopPropagation()} />
</motion.div>
```

## [Note: SVG filters](#note-svg-filters)

Gestures aren't recognised on SVG `filter` components, as these elements don't have a physical presence and therefore don't receive events.

You can instead add `while-` props and event handlers to a parent and use variants to animate these elements.

```
const MyComponent = () => {
  return (
    <motion.svg whileHover="hover">
      <filter id="blur">
        <motion.feGaussianBlur
          stdDeviation={0}
          variants={{ hover: { stdDeviation: 2 } }}
        />
      </filter>
    </motion.svg>
  )
}
```

## Related topics

- [### useDragControls

  Manually start/stop drag gestures. Supports snap to cursor and more.](./react-use-drag-controls)

  [### useDragControls

  Manually start/stop drag gestures. Supports snap to cursor and more.](./react-use-drag-controls)

  [### useDragControls

  Manually start/stop drag gestures. Supports snap to cursor and more.](./react-use-drag-controls)
- [Motion+

  ### Cursor

  Create custom cursor and follow-along effects in React.](./cursor)

  [Motion+

  ### Cursor

  Create custom cursor and follow-along effects in React.](./cursor)

  [Motion+

  ### Cursor

  Create custom cursor and follow-along effects in React.](./cursor)

- [### Gesture animation examples

  See all examples & tutorials, with full copy & paste source code.](https://motion.dev/examples?platform=react&search=drag|whileTap|whileDrag|whileHover)

- [### Gesture animation examples

  See all examples & tutorials, with full copy & paste source code.](https://motion.dev/examples?platform=react&search=drag|whileTap|whileDrag|whileHover)

- [### Gesture animation examples

  See all examples & tutorials, with full copy & paste source code.](https://motion.dev/examples?platform=react&search=drag|whileTap|whileDrag|whileHover)

- [Tutorial

  ### Gestures

  An example of using gestures to animate an element using Motion for React's simple whileTap and whileHover props.](../tutorials/react-gestures)

- [Tutorial

  ### Gestures

  An example of using gestures to animate an element using Motion for React's simple whileTap and whileHover props.](../tutorials/react-gestures)

- [Tutorial

  ### Gestures

  An example of using gestures to animate an element using Motion for React's simple whileTap and whileHover props.](../tutorials/react-gestures)

Previous

[Transitions](./react-transitions)

Next

[Hover animation](./react-hover-animation)

Motion+

Motion+

Motion+

## Mastered gestures?

Take your interactive animations to the next level. The premium Cursor component in Motion+ creates custom cursor and cursor-follow effects that build on the gesture concepts you've just learned.

[See all features](../plus)

[See all features](../plus)

[See all features](../plus)

One-time payment, lifetime updates.

[![](https://framerusercontent.com/images/5efyyhcUoAlTBRRovqyx3jnMnEM.png?width=1568&height=1174)](https://framerusercontent.com/assets/MK7ot7xHs8BI3SZScC9oiKpURY4.mp4)

![](https://framerusercontent.com/images/dvcUQX74Mh8wmjKmhIoM2Yli4.png?width=2000&height=2000)

![](https://framerusercontent.com/images/dvcUQX74Mh8wmjKmhIoM2Yli4.png?width=2000&height=2000)

![](https://framerusercontent.com/images/dvcUQX74Mh8wmjKmhIoM2Yli4.png?width=2000&height=2000)

[![](https://framerusercontent.com/images/a6LWvnzoehr1qy4ywp7QSBDq5iQ.jpg?width=290&height=223)

AI-ready animations

Make your LLM an animation expert with 330+ pre-built examples available via MCP.](../plus)