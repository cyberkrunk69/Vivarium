# useAnimate â Manual React animation controls | Motion

Source: https://www.framer.com/motion/use-animate/

---

`useAnimate` provides a way of using the `animate` [function](./animate) that is scoped to the elements within your component.

This allows you to use manual animation controls, timelines, selectors scoped to your component, and automatic cleanup.

It provides a `scope` ref, and an `animate` function where every DOM selector is scoped to this ref.

```
function Component() {
  const [scope, animate] = useAnimate()

  useEffect(() => {
    // This "li" selector will only select children
    // of the element that receives `scope`.
    animate("li", { opacity: 1 })
  })
  
  return <ul ref={scope}>{children}</ul>
}
```

Additionally, when the component calling `useAnimate` is removed, all animations started with its `animate` function will be cleaned up automatically.

## [Usage](#usage)

Import from Motion:

```
// Mini
import { useAnimate } from "motion/react-mini"

// Hybrid
import { useAnimate } from "motion/react"
```

`useAnimate` returns two arguments, a `scope` ref and an `animate` [function](./animate).

```
function Component() {
  const [scope, animate] = useAnimate()
```

This `scope` ref must be passed to either a regular HTML/SVG element or a `motion` component.

```
function Component({ children }) {
  const [scope, animate] = useAnimate()
  
  return <ul ref={scope}>{children}</ul>
}
```

This scoped `animate` function can now be used in effects and event handlers to animate elements.

We can either use the scoped element directly:

```
animate(scope.current, { opacity: 1 }, { duration: 1 })
```

Or by passing it a selector:

```
animate("li", { backgroundColor: "#000" }, { ease: "linear" })
```

This selector is `"li"`, but we're not selecting all `li` elements on the page, only those that are a child of the scoped element.

### [Scroll-triggered animations](#scroll-triggered-animations)

Animations can be triggered when the scope scrolls into view by combining `useAnimate` with `useInView`.

```
import { useAnimate, useInView } from "motion/react"

function Component() {
  const [scope, animate] = useAnimate()
  const isInView = useInView(scope)
  
  useEffect(() => {
     if (isInView) {
       animate(scope.current, { opacity: 1 })
     }
  }, [isInView])
  
  return (
    <ul ref={scope}>
      <li />
      <li />
      <li />
    </ul>
  )
}
```

### [Exit animations](#exit-animations)

It's possible to compose your own exit animations when a component is removed using `useAnimate` in conjunction with `usePresence`.

```
import { useAnimate, usePresence } from "framer-motion"

function Component() {
  const [isPresent, safeToRemove] = usePresence()
  const [scope, animate] = useAnimate()
  
  useEffect(() => {
     if (isPresent) {
       const enterAnimation = async () => {
         await animate(scope.current, { opacity: 1 })
         await animate("li", { opacity: 1, x: 0 })
       }
       enterAnimation()

     } else {
       const exitAnimation = async () => {
         await animate("li", { opacity: 0, x: -100 })
         await animate(scope.current, { opacity: 0 })
         safeToRemove()
       }
       
       exitAnimation()
     }
  }, [isPresent])
  
  return (
    <ul ref={scope}>
      <li />
      <li />
      <li />
    </ul>
  )
}
```

This component can now be conditionally rendered as a child of `AnimatePresence`.

```
<AnimatePresence>
  {show ? <Component key="dialog" /> : null}
</AnimatePresence>
```

`useAnimate` provides a way of using the `animate` [function](./animate) that is scoped to the elements within your component.

This allows you to use manual animation controls, timelines, selectors scoped to your component, and automatic cleanup.

It provides a `scope` ref, and an `animate` function where every DOM selector is scoped to this ref.

```
function Component() {
  const [scope, animate] = useAnimate()

  useEffect(() => {
    // This "li" selector will only select children
    // of the element that receives `scope`.
    animate("li", { opacity: 1 })
  })
  
  return <ul ref={scope}>{children}</ul>
}
```

Additionally, when the component calling `useAnimate` is removed, all animations started with its `animate` function will be cleaned up automatically.

## [Usage](#usage)

Import from Motion:

```
// Mini
import { useAnimate } from "motion/react-mini"

// Hybrid
import { useAnimate } from "motion/react"
```

`useAnimate` returns two arguments, a `scope` ref and an `animate` [function](./animate).

```
function Component() {
  const [scope, animate] = useAnimate()
```

This `scope` ref must be passed to either a regular HTML/SVG element or a `motion` component.

```
function Component({ children }) {
  const [scope, animate] = useAnimate()
  
  return <ul ref={scope}>{children}</ul>
}
```

This scoped `animate` function can now be used in effects and event handlers to animate elements.

We can either use the scoped element directly:

```
animate(scope.current, { opacity: 1 }, { duration: 1 })
```

Or by passing it a selector:

```
animate("li", { backgroundColor: "#000" }, { ease: "linear" })
```

This selector is `"li"`, but we're not selecting all `li` elements on the page, only those that are a child of the scoped element.

### [Scroll-triggered animations](#scroll-triggered-animations)

Animations can be triggered when the scope scrolls into view by combining `useAnimate` with `useInView`.

```
import { useAnimate, useInView } from "motion/react"

function Component() {
  const [scope, animate] = useAnimate()
  const isInView = useInView(scope)
  
  useEffect(() => {
     if (isInView) {
       animate(scope.current, { opacity: 1 })
     }
  }, [isInView])
  
  return (
    <ul ref={scope}>
      <li />
      <li />
      <li />
    </ul>
  )
}
```

### [Exit animations](#exit-animations)

It's possible to compose your own exit animations when a component is removed using `useAnimate` in conjunction with `usePresence`.

```
import { useAnimate, usePresence } from "framer-motion"

function Component() {
  const [isPresent, safeToRemove] = usePresence()
  const [scope, animate] = useAnimate()
  
  useEffect(() => {
     if (isPresent) {
       const enterAnimation = async () => {
         await animate(scope.current, { opacity: 1 })
         await animate("li", { opacity: 1, x: 0 })
       }
       enterAnimation()

     } else {
       const exitAnimation = async () => {
         await animate("li", { opacity: 0, x: -100 })
         await animate(scope.current, { opacity: 0 })
         safeToRemove()
       }
       
       exitAnimation()
     }
  }, [isPresent])
  
  return (
    <ul ref={scope}>
      <li />
      <li />
      <li />
    </ul>
  )
}
```

This component can now be conditionally rendered as a child of `AnimatePresence`.

```
<AnimatePresence>
  {show ? <Component key="dialog" /> : null}
</AnimatePresence>
```

`useAnimate` provides a way of using the `animate` [function](./animate) that is scoped to the elements within your component.

This allows you to use manual animation controls, timelines, selectors scoped to your component, and automatic cleanup.

It provides a `scope` ref, and an `animate` function where every DOM selector is scoped to this ref.

```
function Component() {
  const [scope, animate] = useAnimate()

  useEffect(() => {
    // This "li" selector will only select children
    // of the element that receives `scope`.
    animate("li", { opacity: 1 })
  })
  
  return <ul ref={scope}>{children}</ul>
}
```

Additionally, when the component calling `useAnimate` is removed, all animations started with its `animate` function will be cleaned up automatically.

## [Usage](#usage)

Import from Motion:

```
// Mini
import { useAnimate } from "motion/react-mini"

// Hybrid
import { useAnimate } from "motion/react"
```

`useAnimate` returns two arguments, a `scope` ref and an `animate` [function](./animate).

```
function Component() {
  const [scope, animate] = useAnimate()
```

This `scope` ref must be passed to either a regular HTML/SVG element or a `motion` component.

```
function Component({ children }) {
  const [scope, animate] = useAnimate()
  
  return <ul ref={scope}>{children}</ul>
}
```

This scoped `animate` function can now be used in effects and event handlers to animate elements.

We can either use the scoped element directly:

```
animate(scope.current, { opacity: 1 }, { duration: 1 })
```

Or by passing it a selector:

```
animate("li", { backgroundColor: "#000" }, { ease: "linear" })
```

This selector is `"li"`, but we're not selecting all `li` elements on the page, only those that are a child of the scoped element.

### [Scroll-triggered animations](#scroll-triggered-animations)

Animations can be triggered when the scope scrolls into view by combining `useAnimate` with `useInView`.

```
import { useAnimate, useInView } from "motion/react"

function Component() {
  const [scope, animate] = useAnimate()
  const isInView = useInView(scope)
  
  useEffect(() => {
     if (isInView) {
       animate(scope.current, { opacity: 1 })
     }
  }, [isInView])
  
  return (
    <ul ref={scope}>
      <li />
      <li />
      <li />
    </ul>
  )
}
```

### [Exit animations](#exit-animations)

It's possible to compose your own exit animations when a component is removed using `useAnimate` in conjunction with `usePresence`.

```
import { useAnimate, usePresence } from "framer-motion"

function Component() {
  const [isPresent, safeToRemove] = usePresence()
  const [scope, animate] = useAnimate()
  
  useEffect(() => {
     if (isPresent) {
       const enterAnimation = async () => {
         await animate(scope.current, { opacity: 1 })
         await animate("li", { opacity: 1, x: 0 })
       }
       enterAnimation()

     } else {
       const exitAnimation = async () => {
         await animate("li", { opacity: 0, x: -100 })
         await animate(scope.current, { opacity: 0 })
         safeToRemove()
       }
       
       exitAnimation()
     }
  }, [isPresent])
  
  return (
    <ul ref={scope}>
      <li />
      <li />
      <li />
    </ul>
  )
}
```

This component can now be conditionally rendered as a child of `AnimatePresence`.

```
<AnimatePresence>
  {show ? <Component key="dialog" /> : null}
</AnimatePresence>
```

## Related topics

- [### Motion values overview

  Composable animatable values that can updated styles without re-renders.](./react-motion-value)

  [### Motion values overview

  Composable animatable values that can updated styles without re-renders.](./react-motion-value)

  [### Motion values overview

  Composable animatable values that can updated styles without re-renders.](./react-motion-value)
- [### Transitions

  Control timing with duration/easing, springs, delay and stagger.](./react-transitions)

  [### Transitions

  Control timing with duration/easing, springs, delay and stagger.](./react-transitions)

  [### Transitions

  Control timing with duration/easing, springs, delay and stagger.](./react-transitions)
- [### useInView

  Switch React state when an element enters/leaves the viewport.](./react-use-in-view)

  [### useInView

  Switch React state when an element enters/leaves the viewport.](./react-use-in-view)

  [### useInView

  Switch React state when an element enters/leaves the viewport.](./react-use-in-view)

- [### useAnimate examples

  See all examples & tutorials, with full copy & paste source code.](https://motion.dev/examples?platform=react&search=useanimate)

- [### useAnimate examples

  See all examples & tutorials, with full copy & paste source code.](https://motion.dev/examples?platform=react&search=useanimate)

- [### useAnimate examples

  See all examples & tutorials, with full copy & paste source code.](https://motion.dev/examples?platform=react&search=useanimate)

Previous

[Upgrade guide](./react-upgrade-guide)

Next

[useAnimationFrame](./react-use-animation-frame)

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