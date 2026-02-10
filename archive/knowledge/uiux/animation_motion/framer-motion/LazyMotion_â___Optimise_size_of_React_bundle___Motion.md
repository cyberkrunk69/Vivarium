# LazyMotion â Optimise size of React bundle | Motion

Source: https://www.framer.com/motion/lazy-motion/

---

For ease of use, the `motion` [component](./react-motion-component) comes pre-bundled with all of its features for a bundlesize of around 34kb.

With `LazyMotion` and the `m` component, we can reduce this to 4.6kb for the initial render and then sync or async load a subset of features.

```
import { LazyMotion, domAnimation } from "motion/react"
import * as m from "motion/react-m"

export const MyComponent = ({ isVisible }) => (
  <LazyMotion features={domAnimation}>
    <m.div animate={{ opacity: 1 }} />
  </LazyMotion>
)
```

Read the [Reduce bundle size](./react-reduce-bundle-size) guide for full usage instructions.

## [Props](#props)

### [`features`](#features)

Define a feature bundle to load sync or async.

#### [Sync loading](#sync-loading)

Synchronous loading is useful for defining a subset of functionality for a smaller bundlesize.

```
import { LazyMotion, domAnimation } from "motion/react"
import * as m from "motion/react-m"

export const MyComponent = ({ isVisible }) => (
  <LazyMotion features={domAnimation}>
    <m.div animate={{ opacity: 1 }} />
  </LazyMotion>
)
```

#### [Async loading](#async-loading)

Asynchronous loading can ensure your site is hydrated before loading in some or all animation functionality.

```
// features.js
import { domAnimation } from "motion/react"
export default domAnimations
  
// index.js
const loadFeatures = import("./features.js")
  .then(res => res.default)

function Component() {
  return (
    <LazyMotion features={loadFeatures}>
      <m.div animate={{ scale: 1.5 }} />
    </LazyMotion>
  )
}
```

### [`strict`](#strict)

**Default:** `false`

If `true`, will throw an error if a `motion` component renders within a `LazyMotion` component (thereby removing the bundlesize benefits of lazy-loading).

```
// This component will throw an error that explains using a motion component
// instead of the m component will break the benefits of code-splitting.
function Component() {
  return (
    <LazyMotion features={domAnimation} strict>
      <motion.div />
    </LazyMotion>
  )
}
```

For ease of use, the `motion` [component](./react-motion-component) comes pre-bundled with all of its features for a bundlesize of around 34kb.

With `LazyMotion` and the `m` component, we can reduce this to 4.6kb for the initial render and then sync or async load a subset of features.

```
import { LazyMotion, domAnimation } from "motion/react"
import * as m from "motion/react-m"

export const MyComponent = ({ isVisible }) => (
  <LazyMotion features={domAnimation}>
    <m.div animate={{ opacity: 1 }} />
  </LazyMotion>
)
```

Read the [Reduce bundle size](./react-reduce-bundle-size) guide for full usage instructions.

## [Props](#props)

### [`features`](#features)

Define a feature bundle to load sync or async.

#### [Sync loading](#sync-loading)

Synchronous loading is useful for defining a subset of functionality for a smaller bundlesize.

```
import { LazyMotion, domAnimation } from "motion/react"
import * as m from "motion/react-m"

export const MyComponent = ({ isVisible }) => (
  <LazyMotion features={domAnimation}>
    <m.div animate={{ opacity: 1 }} />
  </LazyMotion>
)
```

#### [Async loading](#async-loading)

Asynchronous loading can ensure your site is hydrated before loading in some or all animation functionality.

```
// features.js
import { domAnimation } from "motion/react"
export default domAnimations
  
// index.js
const loadFeatures = import("./features.js")
  .then(res => res.default)

function Component() {
  return (
    <LazyMotion features={loadFeatures}>
      <m.div animate={{ scale: 1.5 }} />
    </LazyMotion>
  )
}
```

### [`strict`](#strict)

**Default:** `false`

If `true`, will throw an error if a `motion` component renders within a `LazyMotion` component (thereby removing the bundlesize benefits of lazy-loading).

```
// This component will throw an error that explains using a motion component
// instead of the m component will break the benefits of code-splitting.
function Component() {
  return (
    <LazyMotion features={domAnimation} strict>
      <motion.div />
    </LazyMotion>
  )
}
```

For ease of use, the `motion` [component](./react-motion-component) comes pre-bundled with all of its features for a bundlesize of around 34kb.

With `LazyMotion` and the `m` component, we can reduce this to 4.6kb for the initial render and then sync or async load a subset of features.

```
import { LazyMotion, domAnimation } from "motion/react"
import * as m from "motion/react-m"

export const MyComponent = ({ isVisible }) => (
  <LazyMotion features={domAnimation}>
    <m.div animate={{ opacity: 1 }} />
  </LazyMotion>
)
```

Read the [Reduce bundle size](./react-reduce-bundle-size) guide for full usage instructions.

## [Props](#props)

### [`features`](#features)

Define a feature bundle to load sync or async.

#### [Sync loading](#sync-loading)

Synchronous loading is useful for defining a subset of functionality for a smaller bundlesize.

```
import { LazyMotion, domAnimation } from "motion/react"
import * as m from "motion/react-m"

export const MyComponent = ({ isVisible }) => (
  <LazyMotion features={domAnimation}>
    <m.div animate={{ opacity: 1 }} />
  </LazyMotion>
)
```

#### [Async loading](#async-loading)

Asynchronous loading can ensure your site is hydrated before loading in some or all animation functionality.

```
// features.js
import { domAnimation } from "motion/react"
export default domAnimations
  
// index.js
const loadFeatures = import("./features.js")
  .then(res => res.default)

function Component() {
  return (
    <LazyMotion features={loadFeatures}>
      <m.div animate={{ scale: 1.5 }} />
    </LazyMotion>
  )
}
```

### [`strict`](#strict)

**Default:** `false`

If `true`, will throw an error if a `motion` component renders within a `LazyMotion` component (thereby removing the bundlesize benefits of lazy-loading).

```
// This component will throw an error that explains using a motion component
// instead of the m component will break the benefits of code-splitting.
function Component() {
  return (
    <LazyMotion features={domAnimation} strict>
      <motion.div />
    </LazyMotion>
  )
}
```

## Related topics

- [### Reduce bundle size

  Reduce your Motion for React bundle size for faster loading and improved SEO.](./react-reduce-bundle-size)

  [### Reduce bundle size

  Reduce your Motion for React bundle size for faster loading and improved SEO.](./react-reduce-bundle-size)

  [### Reduce bundle size

  Reduce your Motion for React bundle size for faster loading and improved SEO.](./react-reduce-bundle-size)
- [### Motion component

  Animate elements with a declarative API. Supports variants, gestures, and layout animations.](./react-motion-component)

  [### Motion component

  Animate elements with a declarative API. Supports variants, gestures, and layout animations.](./react-motion-component)

  [### Motion component

  Animate elements with a declarative API. Supports variants, gestures, and layout animations.](./react-motion-component)

Previous

[LayoutGroup](./react-layout-group)

Next

[MotionConfig](./react-motion-config)

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