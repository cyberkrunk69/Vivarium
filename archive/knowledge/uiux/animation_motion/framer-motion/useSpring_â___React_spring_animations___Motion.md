# useSpring â React spring animations | Motion

Source: https://www.framer.com/motion/use-spring/

---

`useSpring` creates [a motion value](./react-motion-value) that will animate to its latest target with a spring animation.

The target can either be set manually via `.set`, or automatically by passing in another motion value.

## [Usage](#usage)

Import `useSpring` from Motion:

```
import { useSpring } from "motion/react"
```

### [Direct control](#direct-control)

`useSpring` can be created with a number, or a unit-type (`px`, `%` etc) string:

```
const x = useSpring(0)
const y = useSpring("100vh")
```

Now, whenever this motion value is updated via `set()`, the value will animate to its new target with the defined spring.

```
x.set(100)
y.set("50vh")
```

It's also possible to update this value immediately, without a spring, with [the](./react-motion-value#jump) `jump()` [method](./react-motion-value#jump).

```
x.jump(50)
y.jump("0vh")
```

### [Track another motion value](#track-another-motion-value)

Its also possible to automatically spring towards the latest value of another motion value:

```
const x = useMotionValue(0)
const y = useSpring(x)
```

This source motion value must also be a number, or unit-type string.

### [Transition](#transition)

The type of `spring` can be defined with the usual [spring transition option](./react-transitions#spring).

```
useSpring(0, { stiffness: 300 })
```

`useSpring` creates [a motion value](./react-motion-value) that will animate to its latest target with a spring animation.

The target can either be set manually via `.set`, or automatically by passing in another motion value.

## [Usage](#usage)

Import `useSpring` from Motion:

```
import { useSpring } from "motion/react"
```

### [Direct control](#direct-control)

`useSpring` can be created with a number, or a unit-type (`px`, `%` etc) string:

```
const x = useSpring(0)
const y = useSpring("100vh")
```

Now, whenever this motion value is updated via `set()`, the value will animate to its new target with the defined spring.

```
x.set(100)
y.set("50vh")
```

It's also possible to update this value immediately, without a spring, with [the](./react-motion-value#jump) `jump()` [method](./react-motion-value#jump).

```
x.jump(50)
y.jump("0vh")
```

### [Track another motion value](#track-another-motion-value)

Its also possible to automatically spring towards the latest value of another motion value:

```
const x = useMotionValue(0)
const y = useSpring(x)
```

This source motion value must also be a number, or unit-type string.

### [Transition](#transition)

The type of `spring` can be defined with the usual [spring transition option](./react-transitions#spring).

```
useSpring(0, { stiffness: 300 })
```

`useSpring` creates [a motion value](./react-motion-value) that will animate to its latest target with a spring animation.

The target can either be set manually via `.set`, or automatically by passing in another motion value.

## [Usage](#usage)

Import `useSpring` from Motion:

```
import { useSpring } from "motion/react"
```

### [Direct control](#direct-control)

`useSpring` can be created with a number, or a unit-type (`px`, `%` etc) string:

```
const x = useSpring(0)
const y = useSpring("100vh")
```

Now, whenever this motion value is updated via `set()`, the value will animate to its new target with the defined spring.

```
x.set(100)
y.set("50vh")
```

It's also possible to update this value immediately, without a spring, with [the](./react-motion-value#jump) `jump()` [method](./react-motion-value#jump).

```
x.jump(50)
y.jump("0vh")
```

### [Track another motion value](#track-another-motion-value)

Its also possible to automatically spring towards the latest value of another motion value:

```
const x = useMotionValue(0)
const y = useSpring(x)
```

This source motion value must also be a number, or unit-type string.

### [Transition](#transition)

The type of `spring` can be defined with the usual [spring transition option](./react-transitions#spring).

```
useSpring(0, { stiffness: 300 })
```

## Related topics

- [### Motion values overview

  Composable animatable values that can updated styles without re-renders.](./react-motion-value)

  [### Motion values overview

  Composable animatable values that can updated styles without re-renders.](./react-motion-value)

  [### Motion values overview

  Composable animatable values that can updated styles without re-renders.](./react-motion-value)

- [### useSpring examples

  See all examples & tutorials, with full copy & paste source code.](https://motion.dev/examples?platform=react&search=usespring)

- [### useSpring examples

  See all examples & tutorials, with full copy & paste source code.](https://motion.dev/examples?platform=react&search=usespring)

- [### useSpring examples

  See all examples & tutorials, with full copy & paste source code.](https://motion.dev/examples?platform=react&search=usespring)

Previous

[useScroll](./react-use-scroll)

Next

[useTime](./react-use-time)

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