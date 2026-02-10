# Motion for React â Install & first React animation | Motion

Source: https://www.framer.com/motion/introduction/

---

Presented byâ¦

Sponsor this page

Sponsor this page

Sponsor this page

**Motion for React** is a React animation library for building smooth, production-grade UI animations. You can start with simple prop-based animations before growing to layout, gesture and scroll animations.

Motion's unique **hybrid engine** combines the performance of native browser animations with the flexibility of JavaScript. It's also trusted by companies like [Framer](https://framer.com) and [Figma](https://figma.com) to power their amazing no-code animations and gestures.

In this guide, we'll learn **why** and **when** you should use Motion, how to **install** it, and then take a whirlwind tour of its main features.

## [Why Motion for React?](#why-motion-for-react)

React gives you the power to build dynamic user interfaces, but orchestrating complex, performant animations can be a challenge. Motion is a production-ready library designed to solve this, making it simple to create everything from beautiful micro-interactions to complex, gesture-driven animations.

```
<motion.button animate={{ opacity: 1 }} />
```

### [Key advantages](#key-advantages)

Hereâs when itâs the right choice for your project.

- **Built for React.** While other animation libraries are messy to integrate, Motion's declarative API feels like a natural extension of React. Animations can be linked directly to state and props.
- **Hardware-acceleration.** Motion leverages the same high-performance browser animations as pure CSS, ensuring your UIs stay smooth and snappy. You get the power of 120fps animations with a much simpler and more expressive API.
- **Animate anything.** CSS has hard limits. There's values you can't animate, keyframes you can't interrupt, staggers that must be hardcoded. Motion provides a single, consistent API that handles everything from simple transitions to advanced scroll, layout, and gesture-driven effects.
- **App-like gestures.** Standard CSS `:hover` events are unreliable on touch devices. Motion provides robust, cross-device gesture recognisers for tap, drag, and hover, making it easy to build interactions that feel native and intuitive on any device.

### [When is CSS a better choice?](#when-is-css-a-better-choice)

For simple, self-contained effects (like a color change on hover) a standard CSS transition is a lightweight solution. The strength of Motion is that it can do these simple kinds of animations but also scale to anything you can imagine. All with the same easy to write and maintain API.

## [Install](#install)

Motion is available via [npm](https://www.npmjs.com/package/motion):

```
npm install motion
```

Features can now be imported via `"motion/react"`:

```
import { motion } from "motion/react"
```

Prefer to install via CDN, or looking for framework-specific instructions? Check out our [full installation guide](./react-installation).

## [Your first animation](#your-first-animation)

The `<motion />` component is the core API in Motion for React. It's a DOM element, supercharged with animation capabilities.

```
<motion.ul animate={{ rotate: 360 }} />
```

When values in `animate` change, the component will animate. Motion has intuitive defaults, but animations can of course be configured via [the](./react-transitions) `transition` [prop](./react-transitions).

```
<motion.div
  animate={{
    scale: 2,
    transition: { duration: 2 }
  }}
/>
```

[Learn more about React animation](./react-animation)

## [Enter animation](#enter-animation)

When a component enters the page, it will automatically animate to the values defined in the `animate` prop.

You can provide values to animate from via the `initial` prop (otherwise these will be read from the DOM).

```
<motion.button initial={{ scale: 0 }} animate={{ scale: 1 }} />
```

Or disable this initial animation entirely by setting `initial` to `false`.

```
<motion.button initial={false} animate={{ scale: 1 }} />
```

## [Hover & tap animation](#hover-tap-animation)

`<motion />` extends React's event system with powerful [gesture animations](./react-gestures). It currently supports hover, tap, focus, and drag.

```
<motion.button
  whileHover={{ scale: 1.1 }}
  whileTap={{ scale: 0.95 }}
  onHoverStart={() => console.log('hover started!')}
/>
```

Motion's gestures are designed to feel better than using CSS or JavaScript events alone.

## [Scroll animation](#scroll-animation)

Motion supports both types of [scroll animations](./react-scroll-animations): **Scroll-triggered** and **scroll-linked**.

To trigger an animation on scroll, the `whileInView` prop defines a state to animate to/from when an element enters/leaves the viewport:

```
<motion.div
  initial={{ backgroundColor: "rgb(0, 255, 0)", opacity: 0 }}
  whileInView={{ backgroundColor: "rgb(255, 0, 0)", opacity: 1 }}
/>
```

Whereas to link a value directly to scroll position, it's possible to use `MotionValue`s via `useScroll`.

```
const { scrollYProgress } = useScroll()

return <motion.div style={{ scaleX: scrollYProgress }} />
```

## [Layout animation](#layout-animation)

Motion has an industry-leading [layout animation](./react-layout-animations) engine that supports animating between changes in layout using transforms.

It's as easy as applying the `layout` prop.

```
<motion.div layout />
```

Or to animate between completely different elements, a `layoutId`:

```
<motion.div layoutId="underline" />
```

## [Exit animations](#exit-animations)

By wrapping `motion` components with `<AnimatePresence>` we gain access to [exit animations](./react-animate-presence). This allows us to animate elements as they're removed from the DOM.

```
<AnimatePresence>
  {show ? <motion.div key="box" exit={{ opacity: 0 }} /> : null}
</AnimatePresence>
```

## [Development tools](#development-tools)

[Motion Studio](../studio) provides visual and AI animation editing directly inside your code editor. Enhance your workflow tools like the Codex, an AI-searchable examples database, CSS spring generation, a CSS and Motion bezier editor, and more.

### Install Motion Studio

One-click install for Cursor:

[Add Extension](cursor:extension/motion.motion-vscode-extension)

[Add MCP](https://cursor.com/en-US/install-mcp?name=motion&config=eyJjb21tYW5kIjoibnB4IC15IGh0dHBzOi8vYXBpLm1vdGlvbi5kZXYvcmVnaXN0cnkudGd6P3BhY2thZ2U9bW90aW9uLXN0dWRpby1tY3AmdmVyc2lvbj1sYXRlc3QifQ%3D%3D)

Motion Studio is also compatible with VS Code, Google Antigravity and more. [See full installation guide](./studio-install).

## [Learn next](#learn-next)

That's a very quick overview of Motion for React's basic features. But there's a lot more to learn!

Next, we recommend starting with the [React animation](./react-animation) guide. Here, you'll learn more about the different types of animations you can build with Motion.

Or, you can learn by doing, diving straight into our collection of [Fundamentals examples](https://motion.dev/examples?platform=react#fundamentals). Each comes complete with full source code that you can copy-paste into your project.

**Motion for React** is a React animation library for building smooth, production-grade UI animations. You can start with simple prop-based animations before growing to layout, gesture and scroll animations.

Motion's unique **hybrid engine** combines the performance of native browser animations with the flexibility of JavaScript. It's also trusted by companies like [Framer](https://framer.com) and [Figma](https://figma.com) to power their amazing no-code animations and gestures.

In this guide, we'll learn **why** and **when** you should use Motion, how to **install** it, and then take a whirlwind tour of its main features.

## [Why Motion for React?](#why-motion-for-react)

React gives you the power to build dynamic user interfaces, but orchestrating complex, performant animations can be a challenge. Motion is a production-ready library designed to solve this, making it simple to create everything from beautiful micro-interactions to complex, gesture-driven animations.

```
<motion.button animate={{ opacity: 1 }} />
```

### [Key advantages](#key-advantages)

Hereâs when itâs the right choice for your project.

- **Built for React.** While other animation libraries are messy to integrate, Motion's declarative API feels like a natural extension of React. Animations can be linked directly to state and props.
- **Hardware-acceleration.** Motion leverages the same high-performance browser animations as pure CSS, ensuring your UIs stay smooth and snappy. You get the power of 120fps animations with a much simpler and more expressive API.
- **Animate anything.** CSS has hard limits. There's values you can't animate, keyframes you can't interrupt, staggers that must be hardcoded. Motion provides a single, consistent API that handles everything from simple transitions to advanced scroll, layout, and gesture-driven effects.
- **App-like gestures.** Standard CSS `:hover` events are unreliable on touch devices. Motion provides robust, cross-device gesture recognisers for tap, drag, and hover, making it easy to build interactions that feel native and intuitive on any device.

### [When is CSS a better choice?](#when-is-css-a-better-choice)

For simple, self-contained effects (like a color change on hover) a standard CSS transition is a lightweight solution. The strength of Motion is that it can do these simple kinds of animations but also scale to anything you can imagine. All with the same easy to write and maintain API.

## [Install](#install)

Motion is available via [npm](https://www.npmjs.com/package/motion):

```
npm install motion
```

Features can now be imported via `"motion/react"`:

```
import { motion } from "motion/react"
```

Prefer to install via CDN, or looking for framework-specific instructions? Check out our [full installation guide](./react-installation).

## [Your first animation](#your-first-animation)

The `<motion />` component is the core API in Motion for React. It's a DOM element, supercharged with animation capabilities.

```
<motion.ul animate={{ rotate: 360 }} />
```

When values in `animate` change, the component will animate. Motion has intuitive defaults, but animations can of course be configured via [the](./react-transitions) `transition` [prop](./react-transitions).

```
<motion.div
  animate={{
    scale: 2,
    transition: { duration: 2 }
  }}
/>
```

[Learn more about React animation](./react-animation)

## [Enter animation](#enter-animation)

When a component enters the page, it will automatically animate to the values defined in the `animate` prop.

You can provide values to animate from via the `initial` prop (otherwise these will be read from the DOM).

```
<motion.button initial={{ scale: 0 }} animate={{ scale: 1 }} />
```

Or disable this initial animation entirely by setting `initial` to `false`.

```
<motion.button initial={false} animate={{ scale: 1 }} />
```

## [Hover & tap animation](#hover-tap-animation)

`<motion />` extends React's event system with powerful [gesture animations](./react-gestures). It currently supports hover, tap, focus, and drag.

```
<motion.button
  whileHover={{ scale: 1.1 }}
  whileTap={{ scale: 0.95 }}
  onHoverStart={() => console.log('hover started!')}
/>
```

Motion's gestures are designed to feel better than using CSS or JavaScript events alone.

## [Scroll animation](#scroll-animation)

Motion supports both types of [scroll animations](./react-scroll-animations): **Scroll-triggered** and **scroll-linked**.

To trigger an animation on scroll, the `whileInView` prop defines a state to animate to/from when an element enters/leaves the viewport:

```
<motion.div
  initial={{ backgroundColor: "rgb(0, 255, 0)", opacity: 0 }}
  whileInView={{ backgroundColor: "rgb(255, 0, 0)", opacity: 1 }}
/>
```

Whereas to link a value directly to scroll position, it's possible to use `MotionValue`s via `useScroll`.

```
const { scrollYProgress } = useScroll()

return <motion.div style={{ scaleX: scrollYProgress }} />
```

## [Layout animation](#layout-animation)

Motion has an industry-leading [layout animation](./react-layout-animations) engine that supports animating between changes in layout using transforms.

It's as easy as applying the `layout` prop.

```
<motion.div layout />
```

Or to animate between completely different elements, a `layoutId`:

```
<motion.div layoutId="underline" />
```

## [Exit animations](#exit-animations)

By wrapping `motion` components with `<AnimatePresence>` we gain access to [exit animations](./react-animate-presence). This allows us to animate elements as they're removed from the DOM.

```
<AnimatePresence>
  {show ? <motion.div key="box" exit={{ opacity: 0 }} /> : null}
</AnimatePresence>
```

## [Development tools](#development-tools)

[Motion Studio](../studio) provides visual and AI animation editing directly inside your code editor. Enhance your workflow tools like the Codex, an AI-searchable examples database, CSS spring generation, a CSS and Motion bezier editor, and more.

### Install Motion Studio

One-click install for Cursor:

[Add Extension](cursor:extension/motion.motion-vscode-extension)

[Add MCP](https://cursor.com/en-US/install-mcp?name=motion&config=eyJjb21tYW5kIjoibnB4IC15IGh0dHBzOi8vYXBpLm1vdGlvbi5kZXYvcmVnaXN0cnkudGd6P3BhY2thZ2U9bW90aW9uLXN0dWRpby1tY3AmdmVyc2lvbj1sYXRlc3QifQ%3D%3D)

Motion Studio is also compatible with VS Code, Google Antigravity and more. [See full installation guide](./studio-install).

## [Learn next](#learn-next)

That's a very quick overview of Motion for React's basic features. But there's a lot more to learn!

Next, we recommend starting with the [React animation](./react-animation) guide. Here, you'll learn more about the different types of animations you can build with Motion.

Or, you can learn by doing, diving straight into our collection of [Fundamentals examples](https://motion.dev/examples?platform=react#fundamentals). Each comes complete with full source code that you can copy-paste into your project.

**Motion for React** is a React animation library for building smooth, production-grade UI animations. You can start with simple prop-based animations before growing to layout, gesture and scroll animations.

Motion's unique **hybrid engine** combines the performance of native browser animations with the flexibility of JavaScript. It's also trusted by companies like [Framer](https://framer.com) and [Figma](https://figma.com) to power their amazing no-code animations and gestures.

In this guide, we'll learn **why** and **when** you should use Motion, how to **install** it, and then take a whirlwind tour of its main features.

## [Why Motion for React?](#why-motion-for-react)

React gives you the power to build dynamic user interfaces, but orchestrating complex, performant animations can be a challenge. Motion is a production-ready library designed to solve this, making it simple to create everything from beautiful micro-interactions to complex, gesture-driven animations.

```
<motion.button animate={{ opacity: 1 }} />
```

### [Key advantages](#key-advantages)

Hereâs when itâs the right choice for your project.

- **Built for React.** While other animation libraries are messy to integrate, Motion's declarative API feels like a natural extension of React. Animations can be linked directly to state and props.
- **Hardware-acceleration.** Motion leverages the same high-performance browser animations as pure CSS, ensuring your UIs stay smooth and snappy. You get the power of 120fps animations with a much simpler and more expressive API.
- **Animate anything.** CSS has hard limits. There's values you can't animate, keyframes you can't interrupt, staggers that must be hardcoded. Motion provides a single, consistent API that handles everything from simple transitions to advanced scroll, layout, and gesture-driven effects.
- **App-like gestures.** Standard CSS `:hover` events are unreliable on touch devices. Motion provides robust, cross-device gesture recognisers for tap, drag, and hover, making it easy to build interactions that feel native and intuitive on any device.

### [When is CSS a better choice?](#when-is-css-a-better-choice)

For simple, self-contained effects (like a color change on hover) a standard CSS transition is a lightweight solution. The strength of Motion is that it can do these simple kinds of animations but also scale to anything you can imagine. All with the same easy to write and maintain API.

## [Install](#install)

Motion is available via [npm](https://www.npmjs.com/package/motion):

```
npm install motion
```

Features can now be imported via `"motion/react"`:

```
import { motion } from "motion/react"
```

Prefer to install via CDN, or looking for framework-specific instructions? Check out our [full installation guide](./react-installation).

## [Your first animation](#your-first-animation)

The `<motion />` component is the core API in Motion for React. It's a DOM element, supercharged with animation capabilities.

```
<motion.ul animate={{ rotate: 360 }} />
```

When values in `animate` change, the component will animate. Motion has intuitive defaults, but animations can of course be configured via [the](./react-transitions) `transition` [prop](./react-transitions).

```
<motion.div
  animate={{
    scale: 2,
    transition: { duration: 2 }
  }}
/>
```

[Learn more about React animation](./react-animation)

## [Enter animation](#enter-animation)

When a component enters the page, it will automatically animate to the values defined in the `animate` prop.

You can provide values to animate from via the `initial` prop (otherwise these will be read from the DOM).

```
<motion.button initial={{ scale: 0 }} animate={{ scale: 1 }} />
```

Or disable this initial animation entirely by setting `initial` to `false`.

```
<motion.button initial={false} animate={{ scale: 1 }} />
```

## [Hover & tap animation](#hover-tap-animation)

`<motion />` extends React's event system with powerful [gesture animations](./react-gestures). It currently supports hover, tap, focus, and drag.

```
<motion.button
  whileHover={{ scale: 1.1 }}
  whileTap={{ scale: 0.95 }}
  onHoverStart={() => console.log('hover started!')}
/>
```

Motion's gestures are designed to feel better than using CSS or JavaScript events alone.

## [Scroll animation](#scroll-animation)

Motion supports both types of [scroll animations](./react-scroll-animations): **Scroll-triggered** and **scroll-linked**.

To trigger an animation on scroll, the `whileInView` prop defines a state to animate to/from when an element enters/leaves the viewport:

```
<motion.div
  initial={{ backgroundColor: "rgb(0, 255, 0)", opacity: 0 }}
  whileInView={{ backgroundColor: "rgb(255, 0, 0)", opacity: 1 }}
/>
```

Whereas to link a value directly to scroll position, it's possible to use `MotionValue`s via `useScroll`.

```
const { scrollYProgress } = useScroll()

return <motion.div style={{ scaleX: scrollYProgress }} />
```

## [Layout animation](#layout-animation)

Motion has an industry-leading [layout animation](./react-layout-animations) engine that supports animating between changes in layout using transforms.

It's as easy as applying the `layout` prop.

```
<motion.div layout />
```

Or to animate between completely different elements, a `layoutId`:

```
<motion.div layoutId="underline" />
```

## [Exit animations](#exit-animations)

By wrapping `motion` components with `<AnimatePresence>` we gain access to [exit animations](./react-animate-presence). This allows us to animate elements as they're removed from the DOM.

```
<AnimatePresence>
  {show ? <motion.div key="box" exit={{ opacity: 0 }} /> : null}
</AnimatePresence>
```

## [Development tools](#development-tools)

[Motion Studio](../studio) provides visual and AI animation editing directly inside your code editor. Enhance your workflow tools like the Codex, an AI-searchable examples database, CSS spring generation, a CSS and Motion bezier editor, and more.

### Install Motion Studio

One-click install for Cursor:

[Add Extension](cursor:extension/motion.motion-vscode-extension)

[Add MCP](https://cursor.com/en-US/install-mcp?name=motion&config=eyJjb21tYW5kIjoibnB4IC15IGh0dHBzOi8vYXBpLm1vdGlvbi5kZXYvcmVnaXN0cnkudGd6P3BhY2thZ2U9bW90aW9uLXN0dWRpby1tY3AmdmVyc2lvbj1sYXRlc3QifQ%3D%3D)

Motion Studio is also compatible with VS Code, Google Antigravity and more. [See full installation guide](./studio-install).

## [Learn next](#learn-next)

That's a very quick overview of Motion for React's basic features. But there's a lot more to learn!

Next, we recommend starting with the [React animation](./react-animation) guide. Here, you'll learn more about the different types of animations you can build with Motion.

Or, you can learn by doing, diving straight into our collection of [Fundamentals examples](https://motion.dev/examples?platform=react#fundamentals). Each comes complete with full source code that you can copy-paste into your project.

## Sponsor this page

Reach 600k unique visitors by sponsoring this page.

Choose from a footer slot with logo and link, or an exclusive "Presented byâ¦" slot between the page header and site content.

Contact us

Contact us

Contact us

## Related topics

- [### AI Context

  Turn your LLM into an animation expert with access to the latest Motion documentation & examples.](./studio-ai-context)

  [### AI Context

  Turn your LLM into an animation expert with access to the latest Motion documentation & examples.](./studio-ai-context)

  [### AI Context

  Turn your LLM into an animation expert with access to the latest Motion documentation & examples.](./studio-ai-context)
- [### React animation

  Create React animation with Motion components. Learn variants, gestures, and keyframes.](./react-animation)

  [### React animation

  Create React animation with Motion components. Learn variants, gestures, and keyframes.](./react-animation)

  [### React animation

  Create React animation with Motion components. Learn variants, gestures, and keyframes.](./react-animation)
- [### Scroll animation

  Create scroll-triggered and scroll-linked effects â parallax, progress and more.](./react-scroll-animations)

  [### Scroll animation

  Create scroll-triggered and scroll-linked effects â parallax, progress and more.](./react-scroll-animations)

  [### Scroll animation

  Create scroll-triggered and scroll-linked effects â parallax, progress and more.](./react-scroll-animations)
- [### Layout animation

  Smoothly animate layout changes and create shared element animations.](./react-layout-animations)

  [### Layout animation

  Smoothly animate layout changes and create shared element animations.](./react-layout-animations)

  [### Layout animation

  Smoothly animate layout changes and create shared element animations.](./react-layout-animations)

- [Tutorial

  ### Rotate

  An example of animation the rotation of an element with Motion for React](../tutorials/react-rotate)

- [Tutorial

  ### Rotate

  An example of animation the rotation of an element with Motion for React](../tutorials/react-rotate)

- [Tutorial

  ### Rotate

  An example of animation the rotation of an element with Motion for React](../tutorials/react-rotate)

Next

[React animation](./react-animation)

[![](https://framerusercontent.com/images/a6LWvnzoehr1qy4ywp7QSBDq5iQ.jpg?width=290&height=223)

AI-ready animations

Make your LLM an animation expert with 330+ pre-built examples available via MCP.](../plus)