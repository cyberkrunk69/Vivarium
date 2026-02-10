# useInView â React scroll-triggered state | Motion

Source: https://www.framer.com/motion/use-in-view/

---

`useInView` is a tiny (0.6kb) hook that detects when the provided element is within the viewport. It can be used with any React element.

```
const ref = useRef(null)
const isInView = useInView(ref)

return <div ref={ref} />
```

## [Usage](#usage)

Import `useInView` from Motion:

```
import { useInView } from "motion/react"
```

`useInView` can track the visibility of any HTML element. Pass a `ref` object to both `useInView` and the HTML element.

```
function Component() {
  const ref = useRef(null)
  const isInView = useInView(ref)

  return <div ref={ref} />
}
```

While the element is outside the viewport, `useInView` will return `false`. When it moves inside the view, it'll re-render the component and return `true`.

### [Effects](#effects)

`useInView` is vanilla React state, so firing functions when `isInView` changes is a matter of passing it to a `useEffect`.

```
useEffect(() => {
  console.log("Element is in view: ", isInView)
}, [isInView])
```

## [Options](#options)

`useInView` can accept options to define how the element is tracked within the viewport.

```
const isInView = useInView(ref, { once: true })
```

### [`root`](#root)

By default, `useInView` will track the visibility of an element as it enters/leaves the window viewport. Set `root` to be the ref of a scrollable parent, and it'll use that element to be the viewport instead.

```
function Carousel() {
  const container = useRef(null)
  const ref = useRef(null)
  const isInView = useInView(ref, { root: container })
  
  return (
    <div ref={container} style={{ overflow: "scroll" }}>
      <div ref={ref} />
    </div>
  )
}
```

### [`margin`](#margin)

**Default:** `"0px"`

A margin to add to the viewport to change the detection area. Use multiple values to adjust top/right/bottom/left, e.g. `"0px -20px 0px 100px"`.

```
const isInView = useInView({
  margin: "0px 100px -50px 0px"
})
```

For browser security reasons, `margin` [won't take affect within cross-origin iframes](https://w3c.github.io/IntersectionObserver/#dom-intersectionobserver-rootmargin) unless `root` is explicitly defined.

### [`once`](#once)

**Default:** `false`

If `true`, once an element is in view, useInView will stop observing the element and always return `true`.

```
const isInView = useInView(ref, { once: true })
```

### [`initial`](#initial)

**Default:** `false`

Set an initial value to return until the element has been measured.

```
const isInView = useInView(ref, { initial: true })
```

### [`amount`](#amount)

**Default:** `"some"`

The amount of an element that should enter the viewport to be considered "entered". Either `"some"`, `"all"` or a number between `0` and `1`.

## [Example](#example)

`useInView` is a tiny (0.6kb) hook that detects when the provided element is within the viewport. It can be used with any React element.

```
const ref = useRef(null)
const isInView = useInView(ref)

return <div ref={ref} />
```

## [Usage](#usage)

Import `useInView` from Motion:

```
import { useInView } from "motion/react"
```

`useInView` can track the visibility of any HTML element. Pass a `ref` object to both `useInView` and the HTML element.

```
function Component() {
  const ref = useRef(null)
  const isInView = useInView(ref)

  return <div ref={ref} />
}
```

While the element is outside the viewport, `useInView` will return `false`. When it moves inside the view, it'll re-render the component and return `true`.

### [Effects](#effects)

`useInView` is vanilla React state, so firing functions when `isInView` changes is a matter of passing it to a `useEffect`.

```
useEffect(() => {
  console.log("Element is in view: ", isInView)
}, [isInView])
```

## [Options](#options)

`useInView` can accept options to define how the element is tracked within the viewport.

```
const isInView = useInView(ref, { once: true })
```

### [`root`](#root)

By default, `useInView` will track the visibility of an element as it enters/leaves the window viewport. Set `root` to be the ref of a scrollable parent, and it'll use that element to be the viewport instead.

```
function Carousel() {
  const container = useRef(null)
  const ref = useRef(null)
  const isInView = useInView(ref, { root: container })
  
  return (
    <div ref={container} style={{ overflow: "scroll" }}>
      <div ref={ref} />
    </div>
  )
}
```

### [`margin`](#margin)

**Default:** `"0px"`

A margin to add to the viewport to change the detection area. Use multiple values to adjust top/right/bottom/left, e.g. `"0px -20px 0px 100px"`.

```
const isInView = useInView({
  margin: "0px 100px -50px 0px"
})
```

For browser security reasons, `margin` [won't take affect within cross-origin iframes](https://w3c.github.io/IntersectionObserver/#dom-intersectionobserver-rootmargin) unless `root` is explicitly defined.

### [`once`](#once)

**Default:** `false`

If `true`, once an element is in view, useInView will stop observing the element and always return `true`.

```
const isInView = useInView(ref, { once: true })
```

### [`initial`](#initial)

**Default:** `false`

Set an initial value to return until the element has been measured.

```
const isInView = useInView(ref, { initial: true })
```

### [`amount`](#amount)

**Default:** `"some"`

The amount of an element that should enter the viewport to be considered "entered". Either `"some"`, `"all"` or a number between `0` and `1`.

## [Example](#example)

`useInView` is a tiny (0.6kb) hook that detects when the provided element is within the viewport. It can be used with any React element.

```
const ref = useRef(null)
const isInView = useInView(ref)

return <div ref={ref} />
```

## [Usage](#usage)

Import `useInView` from Motion:

```
import { useInView } from "motion/react"
```

`useInView` can track the visibility of any HTML element. Pass a `ref` object to both `useInView` and the HTML element.

```
function Component() {
  const ref = useRef(null)
  const isInView = useInView(ref)

  return <div ref={ref} />
}
```

While the element is outside the viewport, `useInView` will return `false`. When it moves inside the view, it'll re-render the component and return `true`.

### [Effects](#effects)

`useInView` is vanilla React state, so firing functions when `isInView` changes is a matter of passing it to a `useEffect`.

```
useEffect(() => {
  console.log("Element is in view: ", isInView)
}, [isInView])
```

## [Options](#options)

`useInView` can accept options to define how the element is tracked within the viewport.

```
const isInView = useInView(ref, { once: true })
```

### [`root`](#root)

By default, `useInView` will track the visibility of an element as it enters/leaves the window viewport. Set `root` to be the ref of a scrollable parent, and it'll use that element to be the viewport instead.

```
function Carousel() {
  const container = useRef(null)
  const ref = useRef(null)
  const isInView = useInView(ref, { root: container })
  
  return (
    <div ref={container} style={{ overflow: "scroll" }}>
      <div ref={ref} />
    </div>
  )
}
```

### [`margin`](#margin)

**Default:** `"0px"`

A margin to add to the viewport to change the detection area. Use multiple values to adjust top/right/bottom/left, e.g. `"0px -20px 0px 100px"`.

```
const isInView = useInView({
  margin: "0px 100px -50px 0px"
})
```

For browser security reasons, `margin` [won't take affect within cross-origin iframes](https://w3c.github.io/IntersectionObserver/#dom-intersectionobserver-rootmargin) unless `root` is explicitly defined.

### [`once`](#once)

**Default:** `false`

If `true`, once an element is in view, useInView will stop observing the element and always return `true`.

```
const isInView = useInView(ref, { once: true })
```

### [`initial`](#initial)

**Default:** `false`

Set an initial value to return until the element has been measured.

```
const isInView = useInView(ref, { initial: true })
```

### [`amount`](#amount)

**Default:** `"some"`

The amount of an element that should enter the viewport to be considered "entered". Either `"some"`, `"all"` or a number between `0` and `1`.

## [Example](#example)

## Related topics

- [### Scroll animation

  Create scroll-triggered and scroll-linked effects â parallax, progress and more.](./react-scroll-animations)

  [### Scroll animation

  Create scroll-triggered and scroll-linked effects â parallax, progress and more.](./react-scroll-animations)

  [### Scroll animation

  Create scroll-triggered and scroll-linked effects â parallax, progress and more.](./react-scroll-animations)
- [### useScroll

  Create scroll-linked animations like progress bars & parallax with the useScroll React hook.](./react-use-scroll)

  [### useScroll

  Create scroll-linked animations like progress bars & parallax with the useScroll React hook.](./react-use-scroll)

  [### useScroll

  Create scroll-linked animations like progress bars & parallax with the useScroll React hook.](./react-use-scroll)

Previous

[useDragControls](./react-use-drag-controls)

Next

[usePageInView](./react-use-page-in-view)

Motion+

Motion+

Motion+

## Level up your animations with Motion+

Unlock the full vault of 330+ Motion examples, 100+ tutorials, premium APIs, private Discord and GitHub, and powerful Motion Studio animation editing tools for your IDE.

[Get Motion+](../plus)

[Get Motion+](../plus)

[Get Motion+](../plus)

One-time payment, lifetime updates.

[![](https://framerusercontent.com/images/5efyyhcUoAlTBRRovqyx3jnMnEM.png?width=1568&height=1174)](https://framerusercontent.com/assets/MK7ot7xHs8BI3SZScC9oiKpURY4.mp4)

![](https://framerusercontent.com/images/dvcUQX74Mh8wmjKmhIoM2Yli4.png?width=2000&height=2000)

![](https://framerusercontent.com/images/dvcUQX74Mh8wmjKmhIoM2Yli4.png?width=2000&height=2000)

![](https://framerusercontent.com/images/dvcUQX74Mh8wmjKmhIoM2Yli4.png?width=2000&height=2000)

[![](https://framerusercontent.com/images/a6LWvnzoehr1qy4ywp7QSBDq5iQ.jpg?width=290&height=223)

AI-ready animations

Make your LLM an animation expert with 330+ pre-built examples available via MCP.](../plus)