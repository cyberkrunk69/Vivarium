# useScroll â React scroll-linked animations | Motion

Source: https://www.framer.com/motion/use-scroll/

---

`useScroll` is used to create scroll-linked animations, like progress indicators and parallax effects.

```
const { scrollYProgress } = useScroll()

return <motion.div style={{ scaleX: scrollYProgress }} />
```

## [Usage](#usage)

Import `useScroll` from Motion:

```
import { useScroll } from "motion/react"
```

`useScroll` returns four [motion values](./react-motion-value):

- `scrollX`/`Y`: The absolute scroll position, in pixels.
- `scrollXProgress`/`YProgress`: The scroll position between the defined offsets, as a value between `0` and `1`.

### [Page scroll](#page-scroll)

By default, useScroll tracks the page scroll.

```
const { scrollY } = useScroll()

useMotionValueEvent(scrollY, "change", (latest) => {
  console.log("Page scroll: ", latest)
})
```

For example, we could show a page scroll indicator by passing `scrollYProgress` straight to the `scaleX` style of a progress bar.

```
const { scrollYProgress } = useScroll()

return <motion.div style={{ scaleX: scrollYProgress }} />
```

As `useScroll` returns motion values, we can compose this scroll info with other motion value hooks like `useTransform` and `useSpring`:

```
const { scrollYProgress } = useScroll()
const scaleX = useSpring(scrollYProgress)

return <motion.div style={{ scaleX }} />
```

> Since `scrollY` is a `MotionValue`, there's a neat trick you can use to tell when the user's scroll direction changes:
>
> ```
> const { scrollY } = useScroll()
> const [scrollDirection, setScrollDirection] = useState("down")
>
> useMotionValueEvent(scrollY, "change", (current) => {
>   const diff = current - scrollY.getPrevious()
>   setScrollDirection(diff > 0 ? "down" : "up")
> })
> ```
>
> Perfect for triggering a sticky header animation!
>
> ~ Sam Selikoff, [Motion for React Recipes](https://buildui.com/courses/framer-motion-recipes)

### [Element scroll](#element-scroll)

To track the scroll position of a scrollable element we can pass the element's `ref` to `useScroll`'s `container` option:

```
const carouselRef = useRef(null)
const { scrollX } = useScroll({
  container: carouselRef
})

return (
  <div ref={carouselRef} style={{ overflow: "scroll" }}>
    {children}
  </div>
)
```

### [Element position](#element-position)

We can track the progress of an element as it moves within a container by passing its `ref` to the `target` option.

```
const ref = useRef(null)
const { scrollYProgress } = useScroll({
  target: ref,
  offset: ["start end", "end end"]
})

return <div ref={ref}>
```

In this example, each item has its own progress indicator.

### [Scroll offsets](#scroll-offsets)

With [the](./react-use-scroll#offset) `offset` [option](./react-use-scroll#offset) we can define which parts of the element we want to track with the viewport, for instance track elements as they enter in from the bottom, leave at the top, or travel throughout the whole viewport.

## [Options](#options)

`useScroll` accepts the following options.

### [`container`](#container)

**Default**: Viewport

The scrollable container to track the scroll position of. By default, this is the browser viewport. By passing a ref to a scrollable element, that element can be used instead.

```
const containerRef = useRef(null)
const { scrollYProgress } = useScroll({ container: containerRef })
```

### [`target`](#target)

`useScroll` tracks the progress of the `target` within the `container`. By default, the `target` is the scrollable area of the `container`. It can additionally be set as another element, to track its progress within the `container`.

```
const targetRef = useRef(null)
const { scrollYProgress } = useScroll({ target: targetRef })
```

### [`axis`](#axis)

**Default:** `"y"`

The tracked axis for the defined `offset`.

### [`offset`](#offset)

**Default:** `["start start", "end end"]`

`offset` describes intersections, points where the `target` and `container` meet.

For example, the intersection `"start end"` means when the **start of the target** on the tracked axis meets the **end of the container.**

So if the target is an element, the container is the window, and we're tracking the vertical axis then `"start end"` is where the **top of the element** meets **the bottom of the viewport**.

#### [Accepted intersections](#accepted-intersections)

Both target and container points can be defined as:

- **Number:** A value where `0` represents the start of the axis and `1` represents the end. So to define the top of the target with the middle of the container you could define `"0 0.5"`. Values outside this range are permitted.
- **Names:** `"start"`, `"center"` and `"end"` can be used as clear shortcuts for `0`, `0.5` and `1` respectively.
- **Pixels:** Pixel values like `"100px"`, `"-50px"` will be defined as that number of pixels from the start of the target/container.
- **Percent:** Same as raw numbers but expressed as `"0%"` to `"100%"`.
- **Viewport:** `"vh"` and `"vw"` units are accepted.

```
// Track an element as it enters from the bottom
const { scrollYProgress } = useScroll({
  target: targetRef,
  offset: ["start end", "end end"]
})

// Track an element as it moves out the top
const { scrollYProgress } = useScroll({
  target: targetRef,
  offset: ["start start", "end start"]
})
```

### [`trackContentSize`](#trackcontentsize)

**Default:** `false`

When the size of a page or element's content changes, its scrollable area can change too. But, because browsers don't provide a callback for changes in content size, by default `useScroll()` will not update until the next `"scroll"` event.

Content size tracking is disabled by default because most of the time, scrollable area remains stable, and tracking changes to it involves a small overhead.

`useScroll` can automatically track changes to content size by setting `trackContentSize` to `true`.

```
useScroll({ trackContentSize: true })
```

`useScroll` is used to create scroll-linked animations, like progress indicators and parallax effects.

```
const { scrollYProgress } = useScroll()

return <motion.div style={{ scaleX: scrollYProgress }} />
```

## [Usage](#usage)

Import `useScroll` from Motion:

```
import { useScroll } from "motion/react"
```

`useScroll` returns four [motion values](./react-motion-value):

- `scrollX`/`Y`: The absolute scroll position, in pixels.
- `scrollXProgress`/`YProgress`: The scroll position between the defined offsets, as a value between `0` and `1`.

### [Page scroll](#page-scroll)

By default, useScroll tracks the page scroll.

```
const { scrollY } = useScroll()

useMotionValueEvent(scrollY, "change", (latest) => {
  console.log("Page scroll: ", latest)
})
```

For example, we could show a page scroll indicator by passing `scrollYProgress` straight to the `scaleX` style of a progress bar.

```
const { scrollYProgress } = useScroll()

return <motion.div style={{ scaleX: scrollYProgress }} />
```

As `useScroll` returns motion values, we can compose this scroll info with other motion value hooks like `useTransform` and `useSpring`:

```
const { scrollYProgress } = useScroll()
const scaleX = useSpring(scrollYProgress)

return <motion.div style={{ scaleX }} />
```

> Since `scrollY` is a `MotionValue`, there's a neat trick you can use to tell when the user's scroll direction changes:
>
> ```
> const { scrollY } = useScroll()
> const [scrollDirection, setScrollDirection] = useState("down")
>
> useMotionValueEvent(scrollY, "change", (current) => {
>   const diff = current - scrollY.getPrevious()
>   setScrollDirection(diff > 0 ? "down" : "up")
> })
> ```
>
> Perfect for triggering a sticky header animation!
>
> ~ Sam Selikoff, [Motion for React Recipes](https://buildui.com/courses/framer-motion-recipes)

### [Element scroll](#element-scroll)

To track the scroll position of a scrollable element we can pass the element's `ref` to `useScroll`'s `container` option:

```
const carouselRef = useRef(null)
const { scrollX } = useScroll({
  container: carouselRef
})

return (
  <div ref={carouselRef} style={{ overflow: "scroll" }}>
    {children}
  </div>
)
```

### [Element position](#element-position)

We can track the progress of an element as it moves within a container by passing its `ref` to the `target` option.

```
const ref = useRef(null)
const { scrollYProgress } = useScroll({
  target: ref,
  offset: ["start end", "end end"]
})

return <div ref={ref}>
```

In this example, each item has its own progress indicator.

### [Scroll offsets](#scroll-offsets)

With [the](./react-use-scroll#offset) `offset` [option](./react-use-scroll#offset) we can define which parts of the element we want to track with the viewport, for instance track elements as they enter in from the bottom, leave at the top, or travel throughout the whole viewport.

## [Options](#options)

`useScroll` accepts the following options.

### [`container`](#container)

**Default**: Viewport

The scrollable container to track the scroll position of. By default, this is the browser viewport. By passing a ref to a scrollable element, that element can be used instead.

```
const containerRef = useRef(null)
const { scrollYProgress } = useScroll({ container: containerRef })
```

### [`target`](#target)

`useScroll` tracks the progress of the `target` within the `container`. By default, the `target` is the scrollable area of the `container`. It can additionally be set as another element, to track its progress within the `container`.

```
const targetRef = useRef(null)
const { scrollYProgress } = useScroll({ target: targetRef })
```

### [`axis`](#axis)

**Default:** `"y"`

The tracked axis for the defined `offset`.

### [`offset`](#offset)

**Default:** `["start start", "end end"]`

`offset` describes intersections, points where the `target` and `container` meet.

For example, the intersection `"start end"` means when the **start of the target** on the tracked axis meets the **end of the container.**

So if the target is an element, the container is the window, and we're tracking the vertical axis then `"start end"` is where the **top of the element** meets **the bottom of the viewport**.

#### [Accepted intersections](#accepted-intersections)

Both target and container points can be defined as:

- **Number:** A value where `0` represents the start of the axis and `1` represents the end. So to define the top of the target with the middle of the container you could define `"0 0.5"`. Values outside this range are permitted.
- **Names:** `"start"`, `"center"` and `"end"` can be used as clear shortcuts for `0`, `0.5` and `1` respectively.
- **Pixels:** Pixel values like `"100px"`, `"-50px"` will be defined as that number of pixels from the start of the target/container.
- **Percent:** Same as raw numbers but expressed as `"0%"` to `"100%"`.
- **Viewport:** `"vh"` and `"vw"` units are accepted.

```
// Track an element as it enters from the bottom
const { scrollYProgress } = useScroll({
  target: targetRef,
  offset: ["start end", "end end"]
})

// Track an element as it moves out the top
const { scrollYProgress } = useScroll({
  target: targetRef,
  offset: ["start start", "end start"]
})
```

### [`trackContentSize`](#trackcontentsize)

**Default:** `false`

When the size of a page or element's content changes, its scrollable area can change too. But, because browsers don't provide a callback for changes in content size, by default `useScroll()` will not update until the next `"scroll"` event.

Content size tracking is disabled by default because most of the time, scrollable area remains stable, and tracking changes to it involves a small overhead.

`useScroll` can automatically track changes to content size by setting `trackContentSize` to `true`.

```
useScroll({ trackContentSize: true })
```

`useScroll` is used to create scroll-linked animations, like progress indicators and parallax effects.

```
const { scrollYProgress } = useScroll()

return <motion.div style={{ scaleX: scrollYProgress }} />
```

## [Usage](#usage)

Import `useScroll` from Motion:

```
import { useScroll } from "motion/react"
```

`useScroll` returns four [motion values](./react-motion-value):

- `scrollX`/`Y`: The absolute scroll position, in pixels.
- `scrollXProgress`/`YProgress`: The scroll position between the defined offsets, as a value between `0` and `1`.

### [Page scroll](#page-scroll)

By default, useScroll tracks the page scroll.

```
const { scrollY } = useScroll()

useMotionValueEvent(scrollY, "change", (latest) => {
  console.log("Page scroll: ", latest)
})
```

For example, we could show a page scroll indicator by passing `scrollYProgress` straight to the `scaleX` style of a progress bar.

```
const { scrollYProgress } = useScroll()

return <motion.div style={{ scaleX: scrollYProgress }} />
```

As `useScroll` returns motion values, we can compose this scroll info with other motion value hooks like `useTransform` and `useSpring`:

```
const { scrollYProgress } = useScroll()
const scaleX = useSpring(scrollYProgress)

return <motion.div style={{ scaleX }} />
```

> Since `scrollY` is a `MotionValue`, there's a neat trick you can use to tell when the user's scroll direction changes:
>
> ```
> const { scrollY } = useScroll()
> const [scrollDirection, setScrollDirection] = useState("down")
>
> useMotionValueEvent(scrollY, "change", (current) => {
>   const diff = current - scrollY.getPrevious()
>   setScrollDirection(diff > 0 ? "down" : "up")
> })
> ```
>
> Perfect for triggering a sticky header animation!
>
> ~ Sam Selikoff, [Motion for React Recipes](https://buildui.com/courses/framer-motion-recipes)

### [Element scroll](#element-scroll)

To track the scroll position of a scrollable element we can pass the element's `ref` to `useScroll`'s `container` option:

```
const carouselRef = useRef(null)
const { scrollX } = useScroll({
  container: carouselRef
})

return (
  <div ref={carouselRef} style={{ overflow: "scroll" }}>
    {children}
  </div>
)
```

### [Element position](#element-position)

We can track the progress of an element as it moves within a container by passing its `ref` to the `target` option.

```
const ref = useRef(null)
const { scrollYProgress } = useScroll({
  target: ref,
  offset: ["start end", "end end"]
})

return <div ref={ref}>
```

In this example, each item has its own progress indicator.

### [Scroll offsets](#scroll-offsets)

With [the](./react-use-scroll#offset) `offset` [option](./react-use-scroll#offset) we can define which parts of the element we want to track with the viewport, for instance track elements as they enter in from the bottom, leave at the top, or travel throughout the whole viewport.

## [Options](#options)

`useScroll` accepts the following options.

### [`container`](#container)

**Default**: Viewport

The scrollable container to track the scroll position of. By default, this is the browser viewport. By passing a ref to a scrollable element, that element can be used instead.

```
const containerRef = useRef(null)
const { scrollYProgress } = useScroll({ container: containerRef })
```

### [`target`](#target)

`useScroll` tracks the progress of the `target` within the `container`. By default, the `target` is the scrollable area of the `container`. It can additionally be set as another element, to track its progress within the `container`.

```
const targetRef = useRef(null)
const { scrollYProgress } = useScroll({ target: targetRef })
```

### [`axis`](#axis)

**Default:** `"y"`

The tracked axis for the defined `offset`.

### [`offset`](#offset)

**Default:** `["start start", "end end"]`

`offset` describes intersections, points where the `target` and `container` meet.

For example, the intersection `"start end"` means when the **start of the target** on the tracked axis meets the **end of the container.**

So if the target is an element, the container is the window, and we're tracking the vertical axis then `"start end"` is where the **top of the element** meets **the bottom of the viewport**.

#### [Accepted intersections](#accepted-intersections)

Both target and container points can be defined as:

- **Number:** A value where `0` represents the start of the axis and `1` represents the end. So to define the top of the target with the middle of the container you could define `"0 0.5"`. Values outside this range are permitted.
- **Names:** `"start"`, `"center"` and `"end"` can be used as clear shortcuts for `0`, `0.5` and `1` respectively.
- **Pixels:** Pixel values like `"100px"`, `"-50px"` will be defined as that number of pixels from the start of the target/container.
- **Percent:** Same as raw numbers but expressed as `"0%"` to `"100%"`.
- **Viewport:** `"vh"` and `"vw"` units are accepted.

```
// Track an element as it enters from the bottom
const { scrollYProgress } = useScroll({
  target: targetRef,
  offset: ["start end", "end end"]
})

// Track an element as it moves out the top
const { scrollYProgress } = useScroll({
  target: targetRef,
  offset: ["start start", "end start"]
})
```

### [`trackContentSize`](#trackcontentsize)

**Default:** `false`

When the size of a page or element's content changes, its scrollable area can change too. But, because browsers don't provide a callback for changes in content size, by default `useScroll()` will not update until the next `"scroll"` event.

Content size tracking is disabled by default because most of the time, scrollable area remains stable, and tracking changes to it involves a small overhead.

`useScroll` can automatically track changes to content size by setting `trackContentSize` to `true`.

```
useScroll({ trackContentSize: true })
```

## Related topics

- [### Scroll animation

  Create scroll-triggered and scroll-linked effects â parallax, progress and more.](./react-scroll-animations)

  [### Scroll animation

  Create scroll-triggered and scroll-linked effects â parallax, progress and more.](./react-scroll-animations)

  [### Scroll animation

  Create scroll-triggered and scroll-linked effects â parallax, progress and more.](./react-scroll-animations)
- [### Motion values overview

  Composable animatable values that can updated styles without re-renders.](./react-motion-value)

  [### Motion values overview

  Composable animatable values that can updated styles without re-renders.](./react-motion-value)

  [### Motion values overview

  Composable animatable values that can updated styles without re-renders.](./react-motion-value)
- [### React animation

  Create React animation with Motion components. Learn variants, gestures, and keyframes.](./react-animation)

  [### React animation

  Create React animation with Motion components. Learn variants, gestures, and keyframes.](./react-animation)

  [### React animation

  Create React animation with Motion components. Learn variants, gestures, and keyframes.](./react-animation)

- [### useScroll examples

  See all examples & tutorials, with full copy & paste source code.](https://motion.dev/examples?platform=react&search=useScroll)

- [### useScroll examples

  See all examples & tutorials, with full copy & paste source code.](https://motion.dev/examples?platform=react&search=useScroll)

- [### useScroll examples

  See all examples & tutorials, with full copy & paste source code.](https://motion.dev/examples?platform=react&search=useScroll)

Previous

[useMotionValueEvent](./react-use-motion-value-event)

Next

[useSpring](./react-use-spring)

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