# React animation â Transforms, keyframes & transitions | Motion

Source: https://www.framer.com/motion/animation/

---

New to Motion? Start with the [Motion for React quickstart guide](./react)

[Motion for React](../) is a simple yet powerful animation library. Whether you're building hover effects, scroll-triggered animations, or complex animation sequences, this guide will provide an overview of all the ways you can animate in React with Motion.

## [What you'll learn](#what-you-ll-learn)

- How to create your first animation with the `<motion.div />` component.
- Which values and elements you can animate.
- How to customise your animations with transition options.
- How to animate elements as they enter and exit the DOM.
- How to orchestrate animations with variants.

If you haven't installed Motion already, hop over to the [quick start guide for full instructions](./react).

## [Animate with `<motion />`](#animate-with-motion)

Most animations in Motion are created with the`<motion />` [component](./react-motion-component). Import it from `"motion/react"`:

```
import { motion } from "motion/react"
```

Every HTML & SVG element can be defined with a `motion` component:

```
<motion.div />
```

```
<motion.a href="#" />
```

```
<motion.circle cx={0} />
```

These components are exactly the same as their normal static counterparts, except now they have access to a bunch of [special animation props](./react-motion-component#props).

The most common animation prop is `animate`. When values passed to `animate` change, the element will automatically animate to that value.

```
<motion.div animate={{ opacity: 1 }} />
```

### [Enter animations](#enter-animations)

We can set initial values for an element with the `initial` prop. So an element defined like this will fade in when it enters the DOM:

```
<motion.article
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
/>
```

## [Animatable values](#animatable-values)

**Motion can animate any CSS value**, like `opacity`, `filter` etc.

```
<motion.section
  initial={{ filter: "blur(10px)" }}
  animate={{ filter: "none" }}
/>
```

It can even animate values that aren't normally animatable by browsers, like `background-image` or `mask-image`:

```
<motion.nav
  initial={{ maskImage: "linear-gradient(to right, rgba(0,0,0,1) 90%, rgba(0,0,0,0) 100%)" }}
  animate={{ maskImage: "linear-gradient(to right, rgba(0,0,0,1) 90%, rgba(0,0,0,1) 100%)" }}
/>
```

### [Transforms](#transforms)

Unlike CSS, Motion can animate every transform axis independently.

```
<motion.div animate={{ x: 100 }} />
```

It supports the following special transform values:

- Translate: `x`, `y`, `z`
- Scale: `scale`, `scaleX`, `scaleY`
- Rotate: `rotate`, `rotateX`, `rotateY`, `rotateZ`
- Skew: `skewX`, `skewY`
- Perspective: `transformPerspective`

`motion` components also have enhanced `style` props, allowing you to use these shorthands statically:

```
<motion.section style={{ x: -20 }} />
```

Animating transforms independently provides great flexibility, especially when animating different transforms with gestures:

```
<motion.button
  initial={{ y: 10 }}
  animate={{ y: 0 }}
  whileHover={{ scale: 1.1 }}
  whileTap={{ scale: 0.9 }}
/>
```

Independent transforms already perform great, but Motion uniquely offers hardware acceleration when setting `transform` directly.

```
<motion.li
  initial={{ transform: "translateX(-100px)" }}
  animate={{ transform: "translateX(0px)" }}
  transition={{ type: "spring" }}
/>
```

For SVG components, `x` and `y` **attributes** can be set using `attrX` and `attrY`. [Learn more about SVG animations in React](./react-svg-animation).

### [Supported value types](#supported-value-types)

Motion can animate any of the following value types:

- Numbers: `0`, `100` etc.
- Strings containing numbers: `"0vh"`, `"10px"` etc.
- Colors: Hex, RGBA, HSLA.
- Complex strings containing multiple numbers and/or colors (like `box-shadow`).
- `display: "none"/"block"` and `visibility: "hidden"/"visible"`.

### [Value type conversion](#value-type-conversion)

In general, values can only be animated between two of the same type (i.e `"0px"` to `"100px"`).

Colors can be freely animated between hex, RGBA and HSLA types.

Additionally, `x`, `y`, `width`, `height`, `top`, `left`, `right` and `bottom` can animate between different value types.

```
<motion.div
  initial={{ x: "100%" }}
  animate={{ x: "calc(100vw - 50%)" }}
/>
```

It's also possible to animate `width` and `height` in to/out of `"auto"`.

```
<motion.div
  initial={{ height: 0 }}
  animate={{ height: "auto" }}
/>
```

If animating `height: auto` while also animating `display` in to/out of `"none"`, replace this with `visibility` `"hidden"` as elements with `display: none` can't be measured.

### [Transform origin](#transform-origin)

`transform-origin` has three shortcut values that can be set and animated individually:

- `originX`
- `originY`
- `originZ`

If set as numbers, `originX` and `Y` default to a progress value between `0` and `1`. `originZ` defaults to pixels.

```
<motion.div style={{ originX: 0.5 }} />
```

### [CSS variables](#css-variables)

Motion for React can animate CSS variables, and also use CSS variable definitions as animation targets.

#### [Animating CSS variables](#animating-css-variables)

Sometimes it's convenient to be able to animate a CSS variable to animate many children:

```
<motion.ul
  initial={{ '--rotate': '0deg' }}
  animate={{ '--rotate': '360deg' }}
  transition={{ duration: 2, repeat: Infinity }}
>
  <li style={{ transform: 'rotate(var(--rotate))' }} />
  <li style={{ transform: 'rotate(var(--rotate))' }} />
  <li style={{ transform: 'rotate(var(--rotate))' }} />
</motion.ul>
```

Animating the value of a CSS variable **always triggers paint**, therefore it can be more performant to use `MotionValue`[s](./react-motion-value) to setup this kind of animation. [Learn more about web animation performance](../magazine/web-animation-performance-tier-list).

### [CSS variables as animation targets](#css-variables-as-animation-targets)

HTML `motion` components accept animation targets with CSS variables:

```
<motion.li animate={{ backgroundColor: "var(--action-bg)" }} />
```

## [Transitions](#transitions)

By default, Motion will create appropriate transitions for snappy animations based on the type of value being animated.

For instance, physical properties like `x` or `scale` are animated with spring physics, whereas values like `opacity` or `color` are animated with duration-based easing curves.

However, you can define your own animations via [the](./react-transitions) `transition` [prop](./react-transitions).

```
<motion.div
  animate={{ x: 100 }}
  transition={{ ease: "easeOut", duration: 2 }}
/>
```

A default `transition` can be set for many components with the `MotionConfig` [component](./react-motion-config):

```
<MotionConfig transition={{ duration: 0.3 }}>
  <motion.div animate={{ opacity: 1 }} />
```

Or you can set a specific `transition` on any animation prop:

```
<motion.div
  animate={{ opacity: 1 }}
  whileHover={{
    opacity: 0.7,
    // Specific transitions override default transitions
    transition: { duration: 0.3 }
  }}
  transition={{ duration: 0.5 }}
/>
```

## [Enter animations](#enter-animations-1)

When a `motion` component is first created, it'll automatically animate to the values in `animate` if they're different from those initially rendered, which you can either do via CSS or via [the](./react-motion-value) `initial` [prop.](./react-motion-value)

```
<motion.li
  initial={{ opacity: 0, scale: 0 }}
  animate={{ opacity: 1, scale: 1 }}
/>
```

You can also disable the enter animation entirely by setting `initial={false}`. This will make the element render with the values defined in `animate`.

```
<motion.div initial={false} animate={{ y: 100 }} />
```

## [Exit animations](#exit-animations)

Motion for React can animate elements as they're removed from the DOM.

In React, when a component is removed, it's usually removed instantly. Motion provides [the](./react-animate-presence) `AnimatePresence` [component](./react-animate-presence) which keeps elements in the DOM while they perform an animation defined with the `exit` prop.

```
<AnimatePresence>
  {isVisible && (
    <motion.div
      key="modal"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    />
  )}
</AnimatePresence>
```

## [Keyframes](#keyframes)

So far, we've set animation props like `animate` and `exit` to single values, like `opacity: 0`.

This is great when we want to animate from the current value to a new value. But sometimes we want to animate through a **series of values**. In animation terms, these are called **keyframes**.

All animation props can accept keyframe arrays:

```
<motion.div animate={{ x: [0, 100, 0] }} />
```

When we animate to an array of values, the element will animate through each of these values in sequence.

In the previous example, we explicitly set the initial value as `0`. But we can also say "use the current value" by setting the first value to `null`.

```
<motion.div animate={{ x: [null, 100, 0] }} />
```

This way, if a keyframe animation is interrupting another animation, the transition will feel more natural.

### [Wildcard keyframes](#wildcard-keyframes)

This `null` keyframe is called a **wildcard keyframe**. A wildcard keyframe simply takes the value before it (or the current value, if this is the first keyframe in the array).

Wildcard keyframes can be useful for holding a value mid-animation without having to repeat values.

```
<motion.div
  animate={{ x: [0, 100, null, 0 ] }}
  // same as x: [0, 100, 100, 0] but easier to maintain
/>
```

### [Keyframe timing](#keyframe-timing)

By default, each keyframe is spaced evenly throughout the animation. You can override this by setting [the](./react-transitions#times) `times` [option](./react-transitions#times) via `transition`.

`times` is an array of progress values between `0` and `1`, defining where in the animation each keyframe should be positioned.

```
<motion.circle
  cx={500}
  animate={{
    cx: [null, 100, 200],
    transition: { duration: 3, times: [0, 0.2, 1] }
  }}
/>
```

`0` is the start of the animation, and `1` is the end of the animation. Therefore, `0.2` places this keyframe somewhere towards the start of the animation.

## [Gesture animations](#gesture-animations)

Motion for React has animation props that can define how an element animates when it [recognises a gesture](./react-gestures).

Supported gestures are:

- `whileHover`
- `whileTap`
- `whileFocus`
- `whileDrag`
- `whileInView`

When a gesture starts, it animates to the values defined in `while-`, and then when the gesture ends it animates back to the values in `initial` or `animate`.

```
<motion.button
  initial={{ opacity: 0 }}
  whileHover={{ backgroundColor: "rgba(220, 220, 220, 1)" }}
  whileTap={{ backgroundColor: "rgba(255, 255, 255, 1)" }}
  whileInView={{ opacity: 1 }}
/>
```

The [custom Cursor component](../) available in [Motion+](../plus) takes this a step further with magnetic and target-morphing effects as a user hovers clickable targets (like buttons and links):

```
<Cursor magnetic />
```

## [Variants](#variants)

Setting `animate` as a target is useful for simple, single-element animations. It's also possible to orchestrate animations that propagate throughout the DOM. We can do so with variants.

Variants are a set of named targets. These names can be anything.

```
const variants = {
  visible: { opacity: 1 },
  hidden: { opacity: 0 },
}
```

Variants are passed to `motion` components via the `variants` prop:

```
<motion.div variants={variants} />
```

These variants can now be referred to by a label, wherever you can define an animation target:

```
<motion.div
  variants={variants}
  initial="hidden"
  whileInView="visible"
  exit="hidden"
/>
```

You can also define multiple variants via an array:

```
animate={["visible", "danger"]}
```

### [Propagation](#propagation)

Variants are useful for reusing and combining animation targets. But it becomes powerful for orchestrating animations throughout trees.

Variants will flow down through `motion` components. So in this example when the `ul` enters the viewport, all of its children with a "visible" variant will also animate in:

```
const list = {
  visible: { opacity: 1 },
  hidden: { opacity: 0 },
}

const item = {
  visible: { opacity: 1, x: 0 },
  hidden: { opacity: 0, x: -100 },
}

return (
  <motion.ul
    initial="hidden"
    whileInView="visible"
    variants={list}
  >
    <motion.li variants={item} />
    <motion.li variants={item} />
    <motion.li variants={item} />
  </motion.ul>
)
```

### [Orchestration](#orchestration)

By default, this children animations will start simultaneously with the parent. But with variants we gain access to new `transition` props `when` [and](./react-transitions#orchestration) `delayChildren`.

```
const list = {
  visible: {
    opacity: 1,
    transition: {
      when: "beforeChildren",
      delayChildren: stagger(0.3), // Stagger children by .3 seconds
    },
  },
  hidden: {
    opacity: 0,
    transition: {
      when: "afterChildren",
    },
  },
}
```

### [Dynamic variants](#dynamic-variants)

Each variant can be defined as a function that resolves when a variant is made active.

```
const variants = {
  hidden: { opacity: 0 },
  visible: (index) => ({
    opacity: 1,
    transition: { delay: index * 0.3 }
  })
}
```

These functions are provided a single argument, which is passed via the `custom` prop:

```
items.map((item, index) => <motion.div custom={index} variants={variants} />)
```

This way, variants can be resolved differently for each animating element.

## [Animation controls](#animation-controls)

Declarative animations are ideal for most UI interactions. But sometimes we need to take manual control over animation playback.

The `useAnimate` [hook](./react-use-animate) can be used for:

- Animating any HTML/SVG element (not just `motion` components).
- Complex animation sequences.
- Controlling animations with `time`, `speed`, `play()`, `pause()` and other playback controls.

```
function MyComponent() {
  const [scope, animate] = useAnimate()

  useEffect(() => {
    const controls = animate([
      [scope.current, { x: "100%" }],
      ["li", { opacity: 1 }]
    ])

    controls.speed = 0.8

    return () => controls.stop()
  }, [])

  return (
    <ul ref={scope}>
      <li />
      <li />
      <li />
    </ul>
  )
}
```

## [Animate content](#animate-content)

By passing [a](./react-motion-value) `MotionValue` as the child of a `motion` component, it will render its latest value in the HTML.

```
import { useMotionValue, motion, animate } from "motion/react"

function Counter() {
  const count = useMotionValue(0)

  useEffect(() => {
    const controls = animate(count, 100, { duration: 5 })
    return () => controls.stop()
  }, [])

  return <motion.pre>{count}</motion.pre>
}
```

This is more performant than setting React state as the `motion` component will set `innerHTML` directly.

It's also possible to [animate numbers](../) with a ticking counter effect using the `AnimateNumber` component in [Motion+](../plus) by passing them directly to the component:

```
<AnimateNumber>{value}</AnimateNumber>
```

## [Next](#next)

In this guide we've covered the basic kinds of animations we can perform in Motion using its **animation props**. However, there's much more to discover.

Most of the examples on this page have used HTML elements, but Motion also has unique [SVG animation](./react-svg-animation) features, like its simple line drawing API.

We've also only covered time-based animations, but Motion also provides powerful [scroll animation](./react-scroll-animations) features like `useScroll` and `whileInView`.

It also provides a powerful [layout animation](./react-layout-animations) engine, that can animate between any two layouts using performant transforms.

Finally, there's also a whole [Fundamentals examples category](https://motion.dev/examples?platform=react#fundamentals) that covers all the basics of animating with Motion for React with live demos and copy-paste code.

[Motion for React](../) is a simple yet powerful animation library. Whether you're building hover effects, scroll-triggered animations, or complex animation sequences, this guide will provide an overview of all the ways you can animate in React with Motion.

## [What you'll learn](#what-you-ll-learn)

- How to create your first animation with the `<motion.div />` component.
- Which values and elements you can animate.
- How to customise your animations with transition options.
- How to animate elements as they enter and exit the DOM.
- How to orchestrate animations with variants.

If you haven't installed Motion already, hop over to the [quick start guide for full instructions](./react).

## [Animate with `<motion />`](#animate-with-motion)

Most animations in Motion are created with the`<motion />` [component](./react-motion-component). Import it from `"motion/react"`:

```
import { motion } from "motion/react"
```

Every HTML & SVG element can be defined with a `motion` component:

```
<motion.div />
```

```
<motion.a href="#" />
```

```
<motion.circle cx={0} />
```

These components are exactly the same as their normal static counterparts, except now they have access to a bunch of [special animation props](./react-motion-component#props).

The most common animation prop is `animate`. When values passed to `animate` change, the element will automatically animate to that value.

```
<motion.div animate={{ opacity: 1 }} />
```

### [Enter animations](#enter-animations)

We can set initial values for an element with the `initial` prop. So an element defined like this will fade in when it enters the DOM:

```
<motion.article
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
/>
```

## [Animatable values](#animatable-values)

**Motion can animate any CSS value**, like `opacity`, `filter` etc.

```
<motion.section
  initial={{ filter: "blur(10px)" }}
  animate={{ filter: "none" }}
/>
```

It can even animate values that aren't normally animatable by browsers, like `background-image` or `mask-image`:

```
<motion.nav
  initial={{ maskImage: "linear-gradient(to right, rgba(0,0,0,1) 90%, rgba(0,0,0,0) 100%)" }}
  animate={{ maskImage: "linear-gradient(to right, rgba(0,0,0,1) 90%, rgba(0,0,0,1) 100%)" }}
/>
```

### [Transforms](#transforms)

Unlike CSS, Motion can animate every transform axis independently.

```
<motion.div animate={{ x: 100 }} />
```

It supports the following special transform values:

- Translate: `x`, `y`, `z`
- Scale: `scale`, `scaleX`, `scaleY`
- Rotate: `rotate`, `rotateX`, `rotateY`, `rotateZ`
- Skew: `skewX`, `skewY`
- Perspective: `transformPerspective`

`motion` components also have enhanced `style` props, allowing you to use these shorthands statically:

```
<motion.section style={{ x: -20 }} />
```

Animating transforms independently provides great flexibility, especially when animating different transforms with gestures:

```
<motion.button
  initial={{ y: 10 }}
  animate={{ y: 0 }}
  whileHover={{ scale: 1.1 }}
  whileTap={{ scale: 0.9 }}
/>
```

Independent transforms already perform great, but Motion uniquely offers hardware acceleration when setting `transform` directly.

```
<motion.li
  initial={{ transform: "translateX(-100px)" }}
  animate={{ transform: "translateX(0px)" }}
  transition={{ type: "spring" }}
/>
```

For SVG components, `x` and `y` **attributes** can be set using `attrX` and `attrY`. [Learn more about SVG animations in React](./react-svg-animation).

### [Supported value types](#supported-value-types)

Motion can animate any of the following value types:

- Numbers: `0`, `100` etc.
- Strings containing numbers: `"0vh"`, `"10px"` etc.
- Colors: Hex, RGBA, HSLA.
- Complex strings containing multiple numbers and/or colors (like `box-shadow`).
- `display: "none"/"block"` and `visibility: "hidden"/"visible"`.

### [Value type conversion](#value-type-conversion)

In general, values can only be animated between two of the same type (i.e `"0px"` to `"100px"`).

Colors can be freely animated between hex, RGBA and HSLA types.

Additionally, `x`, `y`, `width`, `height`, `top`, `left`, `right` and `bottom` can animate between different value types.

```
<motion.div
  initial={{ x: "100%" }}
  animate={{ x: "calc(100vw - 50%)" }}
/>
```

It's also possible to animate `width` and `height` in to/out of `"auto"`.

```
<motion.div
  initial={{ height: 0 }}
  animate={{ height: "auto" }}
/>
```

If animating `height: auto` while also animating `display` in to/out of `"none"`, replace this with `visibility` `"hidden"` as elements with `display: none` can't be measured.

### [Transform origin](#transform-origin)

`transform-origin` has three shortcut values that can be set and animated individually:

- `originX`
- `originY`
- `originZ`

If set as numbers, `originX` and `Y` default to a progress value between `0` and `1`. `originZ` defaults to pixels.

```
<motion.div style={{ originX: 0.5 }} />
```

### [CSS variables](#css-variables)

Motion for React can animate CSS variables, and also use CSS variable definitions as animation targets.

#### [Animating CSS variables](#animating-css-variables)

Sometimes it's convenient to be able to animate a CSS variable to animate many children:

```
<motion.ul
  initial={{ '--rotate': '0deg' }}
  animate={{ '--rotate': '360deg' }}
  transition={{ duration: 2, repeat: Infinity }}
>
  <li style={{ transform: 'rotate(var(--rotate))' }} />
  <li style={{ transform: 'rotate(var(--rotate))' }} />
  <li style={{ transform: 'rotate(var(--rotate))' }} />
</motion.ul>
```

Animating the value of a CSS variable **always triggers paint**, therefore it can be more performant to use `MotionValue`[s](./react-motion-value) to setup this kind of animation. [Learn more about web animation performance](../magazine/web-animation-performance-tier-list).

### [CSS variables as animation targets](#css-variables-as-animation-targets)

HTML `motion` components accept animation targets with CSS variables:

```
<motion.li animate={{ backgroundColor: "var(--action-bg)" }} />
```

## [Transitions](#transitions)

By default, Motion will create appropriate transitions for snappy animations based on the type of value being animated.

For instance, physical properties like `x` or `scale` are animated with spring physics, whereas values like `opacity` or `color` are animated with duration-based easing curves.

However, you can define your own animations via [the](./react-transitions) `transition` [prop](./react-transitions).

```
<motion.div
  animate={{ x: 100 }}
  transition={{ ease: "easeOut", duration: 2 }}
/>
```

A default `transition` can be set for many components with the `MotionConfig` [component](./react-motion-config):

```
<MotionConfig transition={{ duration: 0.3 }}>
  <motion.div animate={{ opacity: 1 }} />
```

Or you can set a specific `transition` on any animation prop:

```
<motion.div
  animate={{ opacity: 1 }}
  whileHover={{
    opacity: 0.7,
    // Specific transitions override default transitions
    transition: { duration: 0.3 }
  }}
  transition={{ duration: 0.5 }}
/>
```

## [Enter animations](#enter-animations-1)

When a `motion` component is first created, it'll automatically animate to the values in `animate` if they're different from those initially rendered, which you can either do via CSS or via [the](./react-motion-value) `initial` [prop.](./react-motion-value)

```
<motion.li
  initial={{ opacity: 0, scale: 0 }}
  animate={{ opacity: 1, scale: 1 }}
/>
```

You can also disable the enter animation entirely by setting `initial={false}`. This will make the element render with the values defined in `animate`.

```
<motion.div initial={false} animate={{ y: 100 }} />
```

## [Exit animations](#exit-animations)

Motion for React can animate elements as they're removed from the DOM.

In React, when a component is removed, it's usually removed instantly. Motion provides [the](./react-animate-presence) `AnimatePresence` [component](./react-animate-presence) which keeps elements in the DOM while they perform an animation defined with the `exit` prop.

```
<AnimatePresence>
  {isVisible && (
    <motion.div
      key="modal"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    />
  )}
</AnimatePresence>
```

## [Keyframes](#keyframes)

So far, we've set animation props like `animate` and `exit` to single values, like `opacity: 0`.

This is great when we want to animate from the current value to a new value. But sometimes we want to animate through a **series of values**. In animation terms, these are called **keyframes**.

All animation props can accept keyframe arrays:

```
<motion.div animate={{ x: [0, 100, 0] }} />
```

When we animate to an array of values, the element will animate through each of these values in sequence.

In the previous example, we explicitly set the initial value as `0`. But we can also say "use the current value" by setting the first value to `null`.

```
<motion.div animate={{ x: [null, 100, 0] }} />
```

This way, if a keyframe animation is interrupting another animation, the transition will feel more natural.

### [Wildcard keyframes](#wildcard-keyframes)

This `null` keyframe is called a **wildcard keyframe**. A wildcard keyframe simply takes the value before it (or the current value, if this is the first keyframe in the array).

Wildcard keyframes can be useful for holding a value mid-animation without having to repeat values.

```
<motion.div
  animate={{ x: [0, 100, null, 0 ] }}
  // same as x: [0, 100, 100, 0] but easier to maintain
/>
```

### [Keyframe timing](#keyframe-timing)

By default, each keyframe is spaced evenly throughout the animation. You can override this by setting [the](./react-transitions#times) `times` [option](./react-transitions#times) via `transition`.

`times` is an array of progress values between `0` and `1`, defining where in the animation each keyframe should be positioned.

```
<motion.circle
  cx={500}
  animate={{
    cx: [null, 100, 200],
    transition: { duration: 3, times: [0, 0.2, 1] }
  }}
/>
```

`0` is the start of the animation, and `1` is the end of the animation. Therefore, `0.2` places this keyframe somewhere towards the start of the animation.

## [Gesture animations](#gesture-animations)

Motion for React has animation props that can define how an element animates when it [recognises a gesture](./react-gestures).

Supported gestures are:

- `whileHover`
- `whileTap`
- `whileFocus`
- `whileDrag`
- `whileInView`

When a gesture starts, it animates to the values defined in `while-`, and then when the gesture ends it animates back to the values in `initial` or `animate`.

```
<motion.button
  initial={{ opacity: 0 }}
  whileHover={{ backgroundColor: "rgba(220, 220, 220, 1)" }}
  whileTap={{ backgroundColor: "rgba(255, 255, 255, 1)" }}
  whileInView={{ opacity: 1 }}
/>
```

The [custom Cursor component](../) available in [Motion+](../plus) takes this a step further with magnetic and target-morphing effects as a user hovers clickable targets (like buttons and links):

```
<Cursor magnetic />
```

## [Variants](#variants)

Setting `animate` as a target is useful for simple, single-element animations. It's also possible to orchestrate animations that propagate throughout the DOM. We can do so with variants.

Variants are a set of named targets. These names can be anything.

```
const variants = {
  visible: { opacity: 1 },
  hidden: { opacity: 0 },
}
```

Variants are passed to `motion` components via the `variants` prop:

```
<motion.div variants={variants} />
```

These variants can now be referred to by a label, wherever you can define an animation target:

```
<motion.div
  variants={variants}
  initial="hidden"
  whileInView="visible"
  exit="hidden"
/>
```

You can also define multiple variants via an array:

```
animate={["visible", "danger"]}
```

### [Propagation](#propagation)

Variants are useful for reusing and combining animation targets. But it becomes powerful for orchestrating animations throughout trees.

Variants will flow down through `motion` components. So in this example when the `ul` enters the viewport, all of its children with a "visible" variant will also animate in:

```
const list = {
  visible: { opacity: 1 },
  hidden: { opacity: 0 },
}

const item = {
  visible: { opacity: 1, x: 0 },
  hidden: { opacity: 0, x: -100 },
}

return (
  <motion.ul
    initial="hidden"
    whileInView="visible"
    variants={list}
  >
    <motion.li variants={item} />
    <motion.li variants={item} />
    <motion.li variants={item} />
  </motion.ul>
)
```

### [Orchestration](#orchestration)

By default, this children animations will start simultaneously with the parent. But with variants we gain access to new `transition` props `when` [and](./react-transitions#orchestration) `delayChildren`.

```
const list = {
  visible: {
    opacity: 1,
    transition: {
      when: "beforeChildren",
      delayChildren: stagger(0.3), // Stagger children by .3 seconds
    },
  },
  hidden: {
    opacity: 0,
    transition: {
      when: "afterChildren",
    },
  },
}
```

### [Dynamic variants](#dynamic-variants)

Each variant can be defined as a function that resolves when a variant is made active.

```
const variants = {
  hidden: { opacity: 0 },
  visible: (index) => ({
    opacity: 1,
    transition: { delay: index * 0.3 }
  })
}
```

These functions are provided a single argument, which is passed via the `custom` prop:

```
items.map((item, index) => <motion.div custom={index} variants={variants} />)
```

This way, variants can be resolved differently for each animating element.

## [Animation controls](#animation-controls)

Declarative animations are ideal for most UI interactions. But sometimes we need to take manual control over animation playback.

The `useAnimate` [hook](./react-use-animate) can be used for:

- Animating any HTML/SVG element (not just `motion` components).
- Complex animation sequences.
- Controlling animations with `time`, `speed`, `play()`, `pause()` and other playback controls.

```
function MyComponent() {
  const [scope, animate] = useAnimate()

  useEffect(() => {
    const controls = animate([
      [scope.current, { x: "100%" }],
      ["li", { opacity: 1 }]
    ])

    controls.speed = 0.8

    return () => controls.stop()
  }, [])

  return (
    <ul ref={scope}>
      <li />
      <li />
      <li />
    </ul>
  )
}
```

## [Animate content](#animate-content)

By passing [a](./react-motion-value) `MotionValue` as the child of a `motion` component, it will render its latest value in the HTML.

```
import { useMotionValue, motion, animate } from "motion/react"

function Counter() {
  const count = useMotionValue(0)

  useEffect(() => {
    const controls = animate(count, 100, { duration: 5 })
    return () => controls.stop()
  }, [])

  return <motion.pre>{count}</motion.pre>
}
```

This is more performant than setting React state as the `motion` component will set `innerHTML` directly.

It's also possible to [animate numbers](../) with a ticking counter effect using the `AnimateNumber` component in [Motion+](../plus) by passing them directly to the component:

```
<AnimateNumber>{value}</AnimateNumber>
```

## [Next](#next)

In this guide we've covered the basic kinds of animations we can perform in Motion using its **animation props**. However, there's much more to discover.

Most of the examples on this page have used HTML elements, but Motion also has unique [SVG animation](./react-svg-animation) features, like its simple line drawing API.

We've also only covered time-based animations, but Motion also provides powerful [scroll animation](./react-scroll-animations) features like `useScroll` and `whileInView`.

It also provides a powerful [layout animation](./react-layout-animations) engine, that can animate between any two layouts using performant transforms.

Finally, there's also a whole [Fundamentals examples category](https://motion.dev/examples?platform=react#fundamentals) that covers all the basics of animating with Motion for React with live demos and copy-paste code.

[Motion for React](../) is a simple yet powerful animation library. Whether you're building hover effects, scroll-triggered animations, or complex animation sequences, this guide will provide an overview of all the ways you can animate in React with Motion.

## [What you'll learn](#what-you-ll-learn)

- How to create your first animation with the `<motion.div />` component.
- Which values and elements you can animate.
- How to customise your animations with transition options.
- How to animate elements as they enter and exit the DOM.
- How to orchestrate animations with variants.

If you haven't installed Motion already, hop over to the [quick start guide for full instructions](./react).

## [Animate with `<motion />`](#animate-with-motion)

Most animations in Motion are created with the`<motion />` [component](./react-motion-component). Import it from `"motion/react"`:

```
import { motion } from "motion/react"
```

Every HTML & SVG element can be defined with a `motion` component:

```
<motion.div />
```

```
<motion.a href="#" />
```

```
<motion.circle cx={0} />
```

These components are exactly the same as their normal static counterparts, except now they have access to a bunch of [special animation props](./react-motion-component#props).

The most common animation prop is `animate`. When values passed to `animate` change, the element will automatically animate to that value.

```
<motion.div animate={{ opacity: 1 }} />
```

### [Enter animations](#enter-animations)

We can set initial values for an element with the `initial` prop. So an element defined like this will fade in when it enters the DOM:

```
<motion.article
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
/>
```

## [Animatable values](#animatable-values)

**Motion can animate any CSS value**, like `opacity`, `filter` etc.

```
<motion.section
  initial={{ filter: "blur(10px)" }}
  animate={{ filter: "none" }}
/>
```

It can even animate values that aren't normally animatable by browsers, like `background-image` or `mask-image`:

```
<motion.nav
  initial={{ maskImage: "linear-gradient(to right, rgba(0,0,0,1) 90%, rgba(0,0,0,0) 100%)" }}
  animate={{ maskImage: "linear-gradient(to right, rgba(0,0,0,1) 90%, rgba(0,0,0,1) 100%)" }}
/>
```

### [Transforms](#transforms)

Unlike CSS, Motion can animate every transform axis independently.

```
<motion.div animate={{ x: 100 }} />
```

It supports the following special transform values:

- Translate: `x`, `y`, `z`
- Scale: `scale`, `scaleX`, `scaleY`
- Rotate: `rotate`, `rotateX`, `rotateY`, `rotateZ`
- Skew: `skewX`, `skewY`
- Perspective: `transformPerspective`

`motion` components also have enhanced `style` props, allowing you to use these shorthands statically:

```
<motion.section style={{ x: -20 }} />
```

Animating transforms independently provides great flexibility, especially when animating different transforms with gestures:

```
<motion.button
  initial={{ y: 10 }}
  animate={{ y: 0 }}
  whileHover={{ scale: 1.1 }}
  whileTap={{ scale: 0.9 }}
/>
```

Independent transforms already perform great, but Motion uniquely offers hardware acceleration when setting `transform` directly.

```
<motion.li
  initial={{ transform: "translateX(-100px)" }}
  animate={{ transform: "translateX(0px)" }}
  transition={{ type: "spring" }}
/>
```

For SVG components, `x` and `y` **attributes** can be set using `attrX` and `attrY`. [Learn more about SVG animations in React](./react-svg-animation).

### [Supported value types](#supported-value-types)

Motion can animate any of the following value types:

- Numbers: `0`, `100` etc.
- Strings containing numbers: `"0vh"`, `"10px"` etc.
- Colors: Hex, RGBA, HSLA.
- Complex strings containing multiple numbers and/or colors (like `box-shadow`).
- `display: "none"/"block"` and `visibility: "hidden"/"visible"`.

### [Value type conversion](#value-type-conversion)

In general, values can only be animated between two of the same type (i.e `"0px"` to `"100px"`).

Colors can be freely animated between hex, RGBA and HSLA types.

Additionally, `x`, `y`, `width`, `height`, `top`, `left`, `right` and `bottom` can animate between different value types.

```
<motion.div
  initial={{ x: "100%" }}
  animate={{ x: "calc(100vw - 50%)" }}
/>
```

It's also possible to animate `width` and `height` in to/out of `"auto"`.

```
<motion.div
  initial={{ height: 0 }}
  animate={{ height: "auto" }}
/>
```

If animating `height: auto` while also animating `display` in to/out of `"none"`, replace this with `visibility` `"hidden"` as elements with `display: none` can't be measured.

### [Transform origin](#transform-origin)

`transform-origin` has three shortcut values that can be set and animated individually:

- `originX`
- `originY`
- `originZ`

If set as numbers, `originX` and `Y` default to a progress value between `0` and `1`. `originZ` defaults to pixels.

```
<motion.div style={{ originX: 0.5 }} />
```

### [CSS variables](#css-variables)

Motion for React can animate CSS variables, and also use CSS variable definitions as animation targets.

#### [Animating CSS variables](#animating-css-variables)

Sometimes it's convenient to be able to animate a CSS variable to animate many children:

```
<motion.ul
  initial={{ '--rotate': '0deg' }}
  animate={{ '--rotate': '360deg' }}
  transition={{ duration: 2, repeat: Infinity }}
>
  <li style={{ transform: 'rotate(var(--rotate))' }} />
  <li style={{ transform: 'rotate(var(--rotate))' }} />
  <li style={{ transform: 'rotate(var(--rotate))' }} />
</motion.ul>
```

Animating the value of a CSS variable **always triggers paint**, therefore it can be more performant to use `MotionValue`[s](./react-motion-value) to setup this kind of animation. [Learn more about web animation performance](../magazine/web-animation-performance-tier-list).

### [CSS variables as animation targets](#css-variables-as-animation-targets)

HTML `motion` components accept animation targets with CSS variables:

```
<motion.li animate={{ backgroundColor: "var(--action-bg)" }} />
```

## [Transitions](#transitions)

By default, Motion will create appropriate transitions for snappy animations based on the type of value being animated.

For instance, physical properties like `x` or `scale` are animated with spring physics, whereas values like `opacity` or `color` are animated with duration-based easing curves.

However, you can define your own animations via [the](./react-transitions) `transition` [prop](./react-transitions).

```
<motion.div
  animate={{ x: 100 }}
  transition={{ ease: "easeOut", duration: 2 }}
/>
```

A default `transition` can be set for many components with the `MotionConfig` [component](./react-motion-config):

```
<MotionConfig transition={{ duration: 0.3 }}>
  <motion.div animate={{ opacity: 1 }} />
```

Or you can set a specific `transition` on any animation prop:

```
<motion.div
  animate={{ opacity: 1 }}
  whileHover={{
    opacity: 0.7,
    // Specific transitions override default transitions
    transition: { duration: 0.3 }
  }}
  transition={{ duration: 0.5 }}
/>
```

## [Enter animations](#enter-animations-1)

When a `motion` component is first created, it'll automatically animate to the values in `animate` if they're different from those initially rendered, which you can either do via CSS or via [the](./react-motion-value) `initial` [prop.](./react-motion-value)

```
<motion.li
  initial={{ opacity: 0, scale: 0 }}
  animate={{ opacity: 1, scale: 1 }}
/>
```

You can also disable the enter animation entirely by setting `initial={false}`. This will make the element render with the values defined in `animate`.

```
<motion.div initial={false} animate={{ y: 100 }} />
```

## [Exit animations](#exit-animations)

Motion for React can animate elements as they're removed from the DOM.

In React, when a component is removed, it's usually removed instantly. Motion provides [the](./react-animate-presence) `AnimatePresence` [component](./react-animate-presence) which keeps elements in the DOM while they perform an animation defined with the `exit` prop.

```
<AnimatePresence>
  {isVisible && (
    <motion.div
      key="modal"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    />
  )}
</AnimatePresence>
```

## [Keyframes](#keyframes)

So far, we've set animation props like `animate` and `exit` to single values, like `opacity: 0`.

This is great when we want to animate from the current value to a new value. But sometimes we want to animate through a **series of values**. In animation terms, these are called **keyframes**.

All animation props can accept keyframe arrays:

```
<motion.div animate={{ x: [0, 100, 0] }} />
```

When we animate to an array of values, the element will animate through each of these values in sequence.

In the previous example, we explicitly set the initial value as `0`. But we can also say "use the current value" by setting the first value to `null`.

```
<motion.div animate={{ x: [null, 100, 0] }} />
```

This way, if a keyframe animation is interrupting another animation, the transition will feel more natural.

### [Wildcard keyframes](#wildcard-keyframes)

This `null` keyframe is called a **wildcard keyframe**. A wildcard keyframe simply takes the value before it (or the current value, if this is the first keyframe in the array).

Wildcard keyframes can be useful for holding a value mid-animation without having to repeat values.

```
<motion.div
  animate={{ x: [0, 100, null, 0 ] }}
  // same as x: [0, 100, 100, 0] but easier to maintain
/>
```

### [Keyframe timing](#keyframe-timing)

By default, each keyframe is spaced evenly throughout the animation. You can override this by setting [the](./react-transitions#times) `times` [option](./react-transitions#times) via `transition`.

`times` is an array of progress values between `0` and `1`, defining where in the animation each keyframe should be positioned.

```
<motion.circle
  cx={500}
  animate={{
    cx: [null, 100, 200],
    transition: { duration: 3, times: [0, 0.2, 1] }
  }}
/>
```

`0` is the start of the animation, and `1` is the end of the animation. Therefore, `0.2` places this keyframe somewhere towards the start of the animation.

## [Gesture animations](#gesture-animations)

Motion for React has animation props that can define how an element animates when it [recognises a gesture](./react-gestures).

Supported gestures are:

- `whileHover`
- `whileTap`
- `whileFocus`
- `whileDrag`
- `whileInView`

When a gesture starts, it animates to the values defined in `while-`, and then when the gesture ends it animates back to the values in `initial` or `animate`.

```
<motion.button
  initial={{ opacity: 0 }}
  whileHover={{ backgroundColor: "rgba(220, 220, 220, 1)" }}
  whileTap={{ backgroundColor: "rgba(255, 255, 255, 1)" }}
  whileInView={{ opacity: 1 }}
/>
```

The [custom Cursor component](../) available in [Motion+](../plus) takes this a step further with magnetic and target-morphing effects as a user hovers clickable targets (like buttons and links):

```
<Cursor magnetic />
```

## [Variants](#variants)

Setting `animate` as a target is useful for simple, single-element animations. It's also possible to orchestrate animations that propagate throughout the DOM. We can do so with variants.

Variants are a set of named targets. These names can be anything.

```
const variants = {
  visible: { opacity: 1 },
  hidden: { opacity: 0 },
}
```

Variants are passed to `motion` components via the `variants` prop:

```
<motion.div variants={variants} />
```

These variants can now be referred to by a label, wherever you can define an animation target:

```
<motion.div
  variants={variants}
  initial="hidden"
  whileInView="visible"
  exit="hidden"
/>
```

You can also define multiple variants via an array:

```
animate={["visible", "danger"]}
```

### [Propagation](#propagation)

Variants are useful for reusing and combining animation targets. But it becomes powerful for orchestrating animations throughout trees.

Variants will flow down through `motion` components. So in this example when the `ul` enters the viewport, all of its children with a "visible" variant will also animate in:

```
const list = {
  visible: { opacity: 1 },
  hidden: { opacity: 0 },
}

const item = {
  visible: { opacity: 1, x: 0 },
  hidden: { opacity: 0, x: -100 },
}

return (
  <motion.ul
    initial="hidden"
    whileInView="visible"
    variants={list}
  >
    <motion.li variants={item} />
    <motion.li variants={item} />
    <motion.li variants={item} />
  </motion.ul>
)
```

### [Orchestration](#orchestration)

By default, this children animations will start simultaneously with the parent. But with variants we gain access to new `transition` props `when` [and](./react-transitions#orchestration) `delayChildren`.

```
const list = {
  visible: {
    opacity: 1,
    transition: {
      when: "beforeChildren",
      delayChildren: stagger(0.3), // Stagger children by .3 seconds
    },
  },
  hidden: {
    opacity: 0,
    transition: {
      when: "afterChildren",
    },
  },
}
```

### [Dynamic variants](#dynamic-variants)

Each variant can be defined as a function that resolves when a variant is made active.

```
const variants = {
  hidden: { opacity: 0 },
  visible: (index) => ({
    opacity: 1,
    transition: { delay: index * 0.3 }
  })
}
```

These functions are provided a single argument, which is passed via the `custom` prop:

```
items.map((item, index) => <motion.div custom={index} variants={variants} />)
```

This way, variants can be resolved differently for each animating element.

## [Animation controls](#animation-controls)

Declarative animations are ideal for most UI interactions. But sometimes we need to take manual control over animation playback.

The `useAnimate` [hook](./react-use-animate) can be used for:

- Animating any HTML/SVG element (not just `motion` components).
- Complex animation sequences.
- Controlling animations with `time`, `speed`, `play()`, `pause()` and other playback controls.

```
function MyComponent() {
  const [scope, animate] = useAnimate()

  useEffect(() => {
    const controls = animate([
      [scope.current, { x: "100%" }],
      ["li", { opacity: 1 }]
    ])

    controls.speed = 0.8

    return () => controls.stop()
  }, [])

  return (
    <ul ref={scope}>
      <li />
      <li />
      <li />
    </ul>
  )
}
```

## [Animate content](#animate-content)

By passing [a](./react-motion-value) `MotionValue` as the child of a `motion` component, it will render its latest value in the HTML.

```
import { useMotionValue, motion, animate } from "motion/react"

function Counter() {
  const count = useMotionValue(0)

  useEffect(() => {
    const controls = animate(count, 100, { duration: 5 })
    return () => controls.stop()
  }, [])

  return <motion.pre>{count}</motion.pre>
}
```

This is more performant than setting React state as the `motion` component will set `innerHTML` directly.

It's also possible to [animate numbers](../) with a ticking counter effect using the `AnimateNumber` component in [Motion+](../plus) by passing them directly to the component:

```
<AnimateNumber>{value}</AnimateNumber>
```

## [Next](#next)

In this guide we've covered the basic kinds of animations we can perform in Motion using its **animation props**. However, there's much more to discover.

Most of the examples on this page have used HTML elements, but Motion also has unique [SVG animation](./react-svg-animation) features, like its simple line drawing API.

We've also only covered time-based animations, but Motion also provides powerful [scroll animation](./react-scroll-animations) features like `useScroll` and `whileInView`.

It also provides a powerful [layout animation](./react-layout-animations) engine, that can animate between any two layouts using performant transforms.

Finally, there's also a whole [Fundamentals examples category](https://motion.dev/examples?platform=react#fundamentals) that covers all the basics of animating with Motion for React with live demos and copy-paste code.

## Related topics

- [### AI Context

  Turn your LLM into an animation expert with access to the latest Motion documentation & examples.](./studio-ai-context)

  [### AI Context

  Turn your LLM into an animation expert with access to the latest Motion documentation & examples.](./studio-ai-context)

  [### AI Context

  Turn your LLM into an animation expert with access to the latest Motion documentation & examples.](./studio-ai-context)
- [### Motion component

  Animate elements with a declarative API. Supports variants, gestures, and layout animations.](./react-motion-component)

  [### Motion component

  Animate elements with a declarative API. Supports variants, gestures, and layout animations.](./react-motion-component)

  [### Motion component

  Animate elements with a declarative API. Supports variants, gestures, and layout animations.](./react-motion-component)
- [### Scroll animation

  Create scroll-triggered and scroll-linked effects â parallax, progress and more.](./react-scroll-animations)

  [### Scroll animation

  Create scroll-triggered and scroll-linked effects â parallax, progress and more.](./react-scroll-animations)

  [### Scroll animation

  Create scroll-triggered and scroll-linked effects â parallax, progress and more.](./react-scroll-animations)
- [Motion+

  ### Cursor

  Create custom cursor and follow-along effects in React.](./cursor)

  [Motion+

  ### Cursor

  Create custom cursor and follow-along effects in React.](./cursor)

  [Motion+

  ### Cursor

  Create custom cursor and follow-along effects in React.](./cursor)

- [Tutorial

  ### Transition options

  An example of setting transition options in Motion for React.](../tutorials/react-transition)

- [Tutorial

  ### Transition options

  An example of setting transition options in Motion for React.](../tutorials/react-transition)

- [Tutorial

  ### Transition options

  An example of setting transition options in Motion for React.](../tutorials/react-transition)

Previous

[Get started with Motion for React](./react)

Next

[Layout animation](./react-layout-animations)

Motion+

Motion+

Motion+

## Ready for the next step?

Learn more by unlocking the full vault of Motion+ pre-built animation examples. Ready to copy-paste directly into your project.

[See Motion+ features & pricing](../plus)

[See Motion+ features & pricing](../plus)

[See Motion+ features & pricing](../plus)

One-time payment, lifetime updates.

[![](https://framerusercontent.com/images/5efyyhcUoAlTBRRovqyx3jnMnEM.png?width=1568&height=1174)](https://framerusercontent.com/assets/MK7ot7xHs8BI3SZScC9oiKpURY4.mp4)

![](https://framerusercontent.com/images/dvcUQX74Mh8wmjKmhIoM2Yli4.png?width=2000&height=2000)

![](https://framerusercontent.com/images/dvcUQX74Mh8wmjKmhIoM2Yli4.png?width=2000&height=2000)

![](https://framerusercontent.com/images/dvcUQX74Mh8wmjKmhIoM2Yli4.png?width=2000&height=2000)

[![](https://framerusercontent.com/images/a6LWvnzoehr1qy4ywp7QSBDq5iQ.jpg?width=290&height=223)

AI-ready animations

Make your LLM an animation expert with 330+ pre-built examples available via MCP.](../plus)