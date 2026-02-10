# React scroll animation â scroll-linked & parallax | Motion

Source: https://www.framer.com/motion/scroll-animations/

---

Learn how to create scroll animations in React with Motion. This guide covers **scroll-linked** animations, **scroll-triggered** animations, **parallax**, **horizontal scrolling**, and more. All with live examples and copy-paste code.

## [Types of scroll animation](#types-of-scroll-animation)

There are two fundamental types of scroll animations:

- **Scroll-triggered:** An animation is triggered when an element enters or leaves the viewport. Common for fade-in effects and lazy-loading.
- **Scroll-linked:** Animation values are linked directly to scroll position. Used for parallax, progress bars, and interactive storytelling.

Motion supports both types of scroll animations with simple, performant APIs.

## [Scroll-triggered animations](#scroll-triggered-animations)

Scroll-triggered animations fire when an element enters or leaves the viewport, or scrolls to a specific point in the viewport.

Motion provides [the](./react-motion-component#whileinview) `whileInView` [prop](./react-motion-component#whileinview) to set an animation target.

```
<motion.div
  initial={{ opacity: 0 }}
  whileInView={{ opacity: 1 }}
/>
```

### [Animate once on scroll](#animate-once-on-scroll)

By default, elements will animate between `initial`/`animate`, and `whileInView`, as the element enters and leaves the viewport. Via [the](./react-motion-component#viewport-1) `viewport` [options](./react-motion-component#viewport-1), set `once: true` so an animation only plays the first time an element scrolls into view.

```
<motion.div
  initial="hidden"
  whileInView="visible"
  viewport={{ once: true }}
/>
```

### [Changing scroll container](#changing-scroll-container)

By default, animations will trigger based on the `window` viewport. To set a custom scroll container element, pass the `ref` of another scrollable element to the `root` option:

```
function Component() {
  const scrollRef = useRef(null)
  
  return (
    <div ref={scrollRef} style={{ overflow: "scroll" }}>
      <motion.div
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ root: scrollRef }}
      />
    </div>
  )
}
```

For more configuration options, checkout [the](./react-motion-component#viewport-1) `motion` [component](./react-motion-component#viewport-1) API reference.

### [Setting state](#setting-state)

It's also possible to set React state when any element (not just a `motion` component) enters and leaves the viewport with the `useInView` [hook](./react-use-in-view).

```
function Component() {
  const ref = useRef(null)
  const isInView = useInView(ref)

  return (
    <div ref={ref}>
      {isInView ? "Hello!" : "Bye..."}
    </div>
  )
}
```

## [Scroll-linked animations](#scroll-linked-animations)

Scroll-linked animations connect CSS styles directly to scroll position. In Motion, this is done with the `useScroll` [hook](./react-use-scroll).

`useScroll` returns four motion values:

- `scrollX`/`scrollY`: Scroll position in pixels
- `scrollXProgress`/`scrollYProgress`: Scroll progress from `0` to `1`

### [Scroll progress bar](#scroll-progress-bar)

Create a reading progress indicator by linking `scrollYProgress` to `scaleX`:

```
const { scrollYProgress } = useScroll();

return (
  <motion.div style={{ scaleX: scrollYProgress, originX: 0 }} />  
)
```

### [Detect scroll direction](#detect-scroll-direction)

It's possible to track scroll direction by using `useMotionValueEvent` on `scrollY`. With this, it's possible to animate items to different states, like a menu that only shows as we scroll down.

```
const { scrollY } = useScroll()
const [scrollDirection, setScrollDirection] = useState("down")

useMotionValueEvent(scrollY, "change", (current) => {
  const diff = current - scrollY.getPrevious()
  setScrollDirection(diff > 0 ? "down" : "up")
})
```

### [Smoothing scroll values](#smoothing-scroll-values)

Smooth changes to a scroll value by passing one through `useSpring`:

```
const { scrollYProgress } = useScroll();
const scaleX = useSpring(scrollYProgress, {
  stiffness: 100,
  damping: 30,
  restDelta: 0.001
})

return <motion.div style={{ scaleX }} />
```

### [Transform scroll position to any value](#transform-scroll-position-to-any-value)

Use the `useTransform` hook to map scroll progress to colours, positions, or any other CSS value:

```
const filter = useTransform(
  scrollYProgress,
  [0, 1],
  ["blur(0px)", "blur(10px)"]
)

return <motion.div style={{ filter }} />
```

### [Track element scroll position through viewport](#track-element-scroll-position-through-viewport)

By default, `useScroll` progress values will represent the overall viewport scroll (or element scroll).

By passing an element via the `target` option, `scrollYProgress` will return its progress through the visible space.

```
const ref = useRef(null)
const { scrollYProgress } = useScroll({
  target: ref,
  /*
    When the top of the target meets the bottom of the container
    to when the bottom of the target meets the top of the container
  */
  offset: ["start end", "end start"]
})
```

### [Parallax scrolling](#parallax-scrolling)

Parallax creates the illusion of depth by moving elements at different speeds. Background layers should move slower than foreground layers:

```
const { foregroundY, backgroundY } = useTransform(
  scrollY,
  [0, 1],
  {
    foregroundY: [0, 2], // move 2px for every 1 scroll px
    backgroundY: [0, 0.5] // move 0.5px for every 1 scroll px
  },
  { clamp: false }
)
```

### [Scroll image reveal effect](#scroll-image-reveal-effect)

By linking `clipPath` to `scrollYProgress`, you can have an image "reveal" itself as it scrolls into view.

```
const ref = useRef(null)
const { scrollYProgress } = useScroll({
  target: ref,
  offset: ["start end", "center center"]
})

const clipPath = useTransform(
  scrollYProgress,
  [0, 1],
  ["inset(0% 50% 0% 50%)", "inset(0% 0% 0% 0%)"]
)

return (
  <motion.div ref={ref} style={{ clipPath }}>
    <img src="/photo.jpg" alt="Revealed image" />
  </motion.div>
)
```

### [Horizontal scroll section](#horizontal-scroll-section)

You can make a horizontally-scrolling section by combining `useScroll`, a tall container section, and a wide `position: sticky` container.

```
const containerRef = useRef(null)
const { scrollYProgress } = useScroll({
  target: containerRef,
  offset: ["start start", "end end"]
})

const x = useTransform(scrollYProgress, [0, 1], ["0%", "-75%"])

return (
  <div ref={containerRef} style={{ height: "300vh" }}>
    <div style={{ position: "sticky", top: 0, height: "100vh", overflow: "hidden" }}>
      <motion.div style={{ x, display: "flex", gap: 20 }}>
        {items.map(item => (
          <div key={item.id} style={{ flexShrink: 0, width: 400 }}>
            {item.content}
          </div>
        ))}
      </motion.div>
    </div>
  </div>
)
```

The container should have a long viewport-relative measurement like `300vh`. Increasing this length will make the horizontal scrolling feel slower.

### [Text scroll](#text-scroll)

By combining `useScroll` with the Motion+ `Ticker` we can make this popular effect where blocks of text scroll horizontally as the page itself scrolls vertically.

By passing `scrollY` to `useTransform` and multiplying it by `-1` we get a [motion value](./react-motion-value) that moves in the opposite direction to the scroll.

```
const { scrollY } = useScroll()
const invertScroll = useTransform(() => scrollY.get() * -1)

const lines = [
    { text: "Creative", reverse: false },
    { text: "Design", reverse: true },
    { text: "Motion", reverse: false },
    { text: "Studio", reverse: true },
]
```

```
{lines.map((line, index) => (
  <Ticker
    key={line.text}
    className={`ticker-line ticker-${index}`}
    items={[
      <span className="text-solid">{line.text}</span>,
      <span className="text-outline">{line.text}</span>,
    ]}
    offset={line.reverse ? invertScroll : scrollY}
  />
))}
```

## [Examples](#examples)

#### [Track element scroll offset](#track-element-scroll-offset)

#### [Track element within viewport](#track-element-within-viewport)

#### [3D](#3d)

#### [Scroll velocity and direction](#scroll-velocity-and-direction)

Read the [full](./react-use-scroll) `useScroll` [docs](./react-use-scroll) to discover more about creating the above effects.

Learn how to create scroll animations in React with Motion. This guide covers **scroll-linked** animations, **scroll-triggered** animations, **parallax**, **horizontal scrolling**, and more. All with live examples and copy-paste code.

## [Types of scroll animation](#types-of-scroll-animation)

There are two fundamental types of scroll animations:

- **Scroll-triggered:** An animation is triggered when an element enters or leaves the viewport. Common for fade-in effects and lazy-loading.
- **Scroll-linked:** Animation values are linked directly to scroll position. Used for parallax, progress bars, and interactive storytelling.

Motion supports both types of scroll animations with simple, performant APIs.

## [Scroll-triggered animations](#scroll-triggered-animations)

Scroll-triggered animations fire when an element enters or leaves the viewport, or scrolls to a specific point in the viewport.

Motion provides [the](./react-motion-component#whileinview) `whileInView` [prop](./react-motion-component#whileinview) to set an animation target.

```
<motion.div
  initial={{ opacity: 0 }}
  whileInView={{ opacity: 1 }}
/>
```

### [Animate once on scroll](#animate-once-on-scroll)

By default, elements will animate between `initial`/`animate`, and `whileInView`, as the element enters and leaves the viewport. Via [the](./react-motion-component#viewport-1) `viewport` [options](./react-motion-component#viewport-1), set `once: true` so an animation only plays the first time an element scrolls into view.

```
<motion.div
  initial="hidden"
  whileInView="visible"
  viewport={{ once: true }}
/>
```

### [Changing scroll container](#changing-scroll-container)

By default, animations will trigger based on the `window` viewport. To set a custom scroll container element, pass the `ref` of another scrollable element to the `root` option:

```
function Component() {
  const scrollRef = useRef(null)
  
  return (
    <div ref={scrollRef} style={{ overflow: "scroll" }}>
      <motion.div
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ root: scrollRef }}
      />
    </div>
  )
}
```

For more configuration options, checkout [the](./react-motion-component#viewport-1) `motion` [component](./react-motion-component#viewport-1) API reference.

### [Setting state](#setting-state)

It's also possible to set React state when any element (not just a `motion` component) enters and leaves the viewport with the `useInView` [hook](./react-use-in-view).

```
function Component() {
  const ref = useRef(null)
  const isInView = useInView(ref)

  return (
    <div ref={ref}>
      {isInView ? "Hello!" : "Bye..."}
    </div>
  )
}
```

## [Scroll-linked animations](#scroll-linked-animations)

Scroll-linked animations connect CSS styles directly to scroll position. In Motion, this is done with the `useScroll` [hook](./react-use-scroll).

`useScroll` returns four motion values:

- `scrollX`/`scrollY`: Scroll position in pixels
- `scrollXProgress`/`scrollYProgress`: Scroll progress from `0` to `1`

### [Scroll progress bar](#scroll-progress-bar)

Create a reading progress indicator by linking `scrollYProgress` to `scaleX`:

```
const { scrollYProgress } = useScroll();

return (
  <motion.div style={{ scaleX: scrollYProgress, originX: 0 }} />  
)
```

### [Detect scroll direction](#detect-scroll-direction)

It's possible to track scroll direction by using `useMotionValueEvent` on `scrollY`. With this, it's possible to animate items to different states, like a menu that only shows as we scroll down.

```
const { scrollY } = useScroll()
const [scrollDirection, setScrollDirection] = useState("down")

useMotionValueEvent(scrollY, "change", (current) => {
  const diff = current - scrollY.getPrevious()
  setScrollDirection(diff > 0 ? "down" : "up")
})
```

### [Smoothing scroll values](#smoothing-scroll-values)

Smooth changes to a scroll value by passing one through `useSpring`:

```
const { scrollYProgress } = useScroll();
const scaleX = useSpring(scrollYProgress, {
  stiffness: 100,
  damping: 30,
  restDelta: 0.001
})

return <motion.div style={{ scaleX }} />
```

### [Transform scroll position to any value](#transform-scroll-position-to-any-value)

Use the `useTransform` hook to map scroll progress to colours, positions, or any other CSS value:

```
const filter = useTransform(
  scrollYProgress,
  [0, 1],
  ["blur(0px)", "blur(10px)"]
)

return <motion.div style={{ filter }} />
```

### [Track element scroll position through viewport](#track-element-scroll-position-through-viewport)

By default, `useScroll` progress values will represent the overall viewport scroll (or element scroll).

By passing an element via the `target` option, `scrollYProgress` will return its progress through the visible space.

```
const ref = useRef(null)
const { scrollYProgress } = useScroll({
  target: ref,
  /*
    When the top of the target meets the bottom of the container
    to when the bottom of the target meets the top of the container
  */
  offset: ["start end", "end start"]
})
```

### [Parallax scrolling](#parallax-scrolling)

Parallax creates the illusion of depth by moving elements at different speeds. Background layers should move slower than foreground layers:

```
const { foregroundY, backgroundY } = useTransform(
  scrollY,
  [0, 1],
  {
    foregroundY: [0, 2], // move 2px for every 1 scroll px
    backgroundY: [0, 0.5] // move 0.5px for every 1 scroll px
  },
  { clamp: false }
)
```

### [Scroll image reveal effect](#scroll-image-reveal-effect)

By linking `clipPath` to `scrollYProgress`, you can have an image "reveal" itself as it scrolls into view.

```
const ref = useRef(null)
const { scrollYProgress } = useScroll({
  target: ref,
  offset: ["start end", "center center"]
})

const clipPath = useTransform(
  scrollYProgress,
  [0, 1],
  ["inset(0% 50% 0% 50%)", "inset(0% 0% 0% 0%)"]
)

return (
  <motion.div ref={ref} style={{ clipPath }}>
    <img src="/photo.jpg" alt="Revealed image" />
  </motion.div>
)
```

### [Horizontal scroll section](#horizontal-scroll-section)

You can make a horizontally-scrolling section by combining `useScroll`, a tall container section, and a wide `position: sticky` container.

```
const containerRef = useRef(null)
const { scrollYProgress } = useScroll({
  target: containerRef,
  offset: ["start start", "end end"]
})

const x = useTransform(scrollYProgress, [0, 1], ["0%", "-75%"])

return (
  <div ref={containerRef} style={{ height: "300vh" }}>
    <div style={{ position: "sticky", top: 0, height: "100vh", overflow: "hidden" }}>
      <motion.div style={{ x, display: "flex", gap: 20 }}>
        {items.map(item => (
          <div key={item.id} style={{ flexShrink: 0, width: 400 }}>
            {item.content}
          </div>
        ))}
      </motion.div>
    </div>
  </div>
)
```

The container should have a long viewport-relative measurement like `300vh`. Increasing this length will make the horizontal scrolling feel slower.

### [Text scroll](#text-scroll)

By combining `useScroll` with the Motion+ `Ticker` we can make this popular effect where blocks of text scroll horizontally as the page itself scrolls vertically.

By passing `scrollY` to `useTransform` and multiplying it by `-1` we get a [motion value](./react-motion-value) that moves in the opposite direction to the scroll.

```
const { scrollY } = useScroll()
const invertScroll = useTransform(() => scrollY.get() * -1)

const lines = [
    { text: "Creative", reverse: false },
    { text: "Design", reverse: true },
    { text: "Motion", reverse: false },
    { text: "Studio", reverse: true },
]
```

```
{lines.map((line, index) => (
  <Ticker
    key={line.text}
    className={`ticker-line ticker-${index}`}
    items={[
      <span className="text-solid">{line.text}</span>,
      <span className="text-outline">{line.text}</span>,
    ]}
    offset={line.reverse ? invertScroll : scrollY}
  />
))}
```

## [Examples](#examples)

#### [Track element scroll offset](#track-element-scroll-offset)

#### [Track element within viewport](#track-element-within-viewport)

#### [3D](#3d)

#### [Scroll velocity and direction](#scroll-velocity-and-direction)

Read the [full](./react-use-scroll) `useScroll` [docs](./react-use-scroll) to discover more about creating the above effects.

Learn how to create scroll animations in React with Motion. This guide covers **scroll-linked** animations, **scroll-triggered** animations, **parallax**, **horizontal scrolling**, and more. All with live examples and copy-paste code.

## [Types of scroll animation](#types-of-scroll-animation)

There are two fundamental types of scroll animations:

- **Scroll-triggered:** An animation is triggered when an element enters or leaves the viewport. Common for fade-in effects and lazy-loading.
- **Scroll-linked:** Animation values are linked directly to scroll position. Used for parallax, progress bars, and interactive storytelling.

Motion supports both types of scroll animations with simple, performant APIs.

## [Scroll-triggered animations](#scroll-triggered-animations)

Scroll-triggered animations fire when an element enters or leaves the viewport, or scrolls to a specific point in the viewport.

Motion provides [the](./react-motion-component#whileinview) `whileInView` [prop](./react-motion-component#whileinview) to set an animation target.

```
<motion.div
  initial={{ opacity: 0 }}
  whileInView={{ opacity: 1 }}
/>
```

### [Animate once on scroll](#animate-once-on-scroll)

By default, elements will animate between `initial`/`animate`, and `whileInView`, as the element enters and leaves the viewport. Via [the](./react-motion-component#viewport-1) `viewport` [options](./react-motion-component#viewport-1), set `once: true` so an animation only plays the first time an element scrolls into view.

```
<motion.div
  initial="hidden"
  whileInView="visible"
  viewport={{ once: true }}
/>
```

### [Changing scroll container](#changing-scroll-container)

By default, animations will trigger based on the `window` viewport. To set a custom scroll container element, pass the `ref` of another scrollable element to the `root` option:

```
function Component() {
  const scrollRef = useRef(null)
  
  return (
    <div ref={scrollRef} style={{ overflow: "scroll" }}>
      <motion.div
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ root: scrollRef }}
      />
    </div>
  )
}
```

For more configuration options, checkout [the](./react-motion-component#viewport-1) `motion` [component](./react-motion-component#viewport-1) API reference.

### [Setting state](#setting-state)

It's also possible to set React state when any element (not just a `motion` component) enters and leaves the viewport with the `useInView` [hook](./react-use-in-view).

```
function Component() {
  const ref = useRef(null)
  const isInView = useInView(ref)

  return (
    <div ref={ref}>
      {isInView ? "Hello!" : "Bye..."}
    </div>
  )
}
```

## [Scroll-linked animations](#scroll-linked-animations)

Scroll-linked animations connect CSS styles directly to scroll position. In Motion, this is done with the `useScroll` [hook](./react-use-scroll).

`useScroll` returns four motion values:

- `scrollX`/`scrollY`: Scroll position in pixels
- `scrollXProgress`/`scrollYProgress`: Scroll progress from `0` to `1`

### [Scroll progress bar](#scroll-progress-bar)

Create a reading progress indicator by linking `scrollYProgress` to `scaleX`:

```
const { scrollYProgress } = useScroll();

return (
  <motion.div style={{ scaleX: scrollYProgress, originX: 0 }} />  
)
```

### [Detect scroll direction](#detect-scroll-direction)

It's possible to track scroll direction by using `useMotionValueEvent` on `scrollY`. With this, it's possible to animate items to different states, like a menu that only shows as we scroll down.

```
const { scrollY } = useScroll()
const [scrollDirection, setScrollDirection] = useState("down")

useMotionValueEvent(scrollY, "change", (current) => {
  const diff = current - scrollY.getPrevious()
  setScrollDirection(diff > 0 ? "down" : "up")
})
```

### [Smoothing scroll values](#smoothing-scroll-values)

Smooth changes to a scroll value by passing one through `useSpring`:

```
const { scrollYProgress } = useScroll();
const scaleX = useSpring(scrollYProgress, {
  stiffness: 100,
  damping: 30,
  restDelta: 0.001
})

return <motion.div style={{ scaleX }} />
```

### [Transform scroll position to any value](#transform-scroll-position-to-any-value)

Use the `useTransform` hook to map scroll progress to colours, positions, or any other CSS value:

```
const filter = useTransform(
  scrollYProgress,
  [0, 1],
  ["blur(0px)", "blur(10px)"]
)

return <motion.div style={{ filter }} />
```

### [Track element scroll position through viewport](#track-element-scroll-position-through-viewport)

By default, `useScroll` progress values will represent the overall viewport scroll (or element scroll).

By passing an element via the `target` option, `scrollYProgress` will return its progress through the visible space.

```
const ref = useRef(null)
const { scrollYProgress } = useScroll({
  target: ref,
  /*
    When the top of the target meets the bottom of the container
    to when the bottom of the target meets the top of the container
  */
  offset: ["start end", "end start"]
})
```

### [Parallax scrolling](#parallax-scrolling)

Parallax creates the illusion of depth by moving elements at different speeds. Background layers should move slower than foreground layers:

```
const { foregroundY, backgroundY } = useTransform(
  scrollY,
  [0, 1],
  {
    foregroundY: [0, 2], // move 2px for every 1 scroll px
    backgroundY: [0, 0.5] // move 0.5px for every 1 scroll px
  },
  { clamp: false }
)
```

### [Scroll image reveal effect](#scroll-image-reveal-effect)

By linking `clipPath` to `scrollYProgress`, you can have an image "reveal" itself as it scrolls into view.

```
const ref = useRef(null)
const { scrollYProgress } = useScroll({
  target: ref,
  offset: ["start end", "center center"]
})

const clipPath = useTransform(
  scrollYProgress,
  [0, 1],
  ["inset(0% 50% 0% 50%)", "inset(0% 0% 0% 0%)"]
)

return (
  <motion.div ref={ref} style={{ clipPath }}>
    <img src="/photo.jpg" alt="Revealed image" />
  </motion.div>
)
```

### [Horizontal scroll section](#horizontal-scroll-section)

You can make a horizontally-scrolling section by combining `useScroll`, a tall container section, and a wide `position: sticky` container.

```
const containerRef = useRef(null)
const { scrollYProgress } = useScroll({
  target: containerRef,
  offset: ["start start", "end end"]
})

const x = useTransform(scrollYProgress, [0, 1], ["0%", "-75%"])

return (
  <div ref={containerRef} style={{ height: "300vh" }}>
    <div style={{ position: "sticky", top: 0, height: "100vh", overflow: "hidden" }}>
      <motion.div style={{ x, display: "flex", gap: 20 }}>
        {items.map(item => (
          <div key={item.id} style={{ flexShrink: 0, width: 400 }}>
            {item.content}
          </div>
        ))}
      </motion.div>
    </div>
  </div>
)
```

The container should have a long viewport-relative measurement like `300vh`. Increasing this length will make the horizontal scrolling feel slower.

### [Text scroll](#text-scroll)

By combining `useScroll` with the Motion+ `Ticker` we can make this popular effect where blocks of text scroll horizontally as the page itself scrolls vertically.

By passing `scrollY` to `useTransform` and multiplying it by `-1` we get a [motion value](./react-motion-value) that moves in the opposite direction to the scroll.

```
const { scrollY } = useScroll()
const invertScroll = useTransform(() => scrollY.get() * -1)

const lines = [
    { text: "Creative", reverse: false },
    { text: "Design", reverse: true },
    { text: "Motion", reverse: false },
    { text: "Studio", reverse: true },
]
```

```
{lines.map((line, index) => (
  <Ticker
    key={line.text}
    className={`ticker-line ticker-${index}`}
    items={[
      <span className="text-solid">{line.text}</span>,
      <span className="text-outline">{line.text}</span>,
    ]}
    offset={line.reverse ? invertScroll : scrollY}
  />
))}
```

## [Examples](#examples)

#### [Track element scroll offset](#track-element-scroll-offset)

#### [Track element within viewport](#track-element-within-viewport)

#### [3D](#3d)

#### [Scroll velocity and direction](#scroll-velocity-and-direction)

Read the [full](./react-use-scroll) `useScroll` [docs](./react-use-scroll) to discover more about creating the above effects.

## Related topics

- [### useScroll

  Create scroll-linked animations like progress bars & parallax with the useScroll React hook.](./react-use-scroll)

  [### useScroll

  Create scroll-linked animations like progress bars & parallax with the useScroll React hook.](./react-use-scroll)

  [### useScroll

  Create scroll-linked animations like progress bars & parallax with the useScroll React hook.](./react-use-scroll)
- [### useInView

  Switch React state when an element enters/leaves the viewport.](./react-use-in-view)

  [### useInView

  Switch React state when an element enters/leaves the viewport.](./react-use-in-view)

  [### useInView

  Switch React state when an element enters/leaves the viewport.](./react-use-in-view)
- [Motion+

  ### Ticker

  Infinitely-scrolling ticker and marquee effects, driven by time, drag or scroll.](./react-ticker)

  [Motion+

  ### Ticker

  Infinitely-scrolling ticker and marquee effects, driven by time, drag or scroll.](./react-ticker)

  [Motion+

  ### Ticker

  Infinitely-scrolling ticker and marquee effects, driven by time, drag or scroll.](./react-ticker)

- [### Scroll animation examples

  See all examples & tutorials, with full copy & paste source code.](https://motion.dev/examples?platform=react&search=scroll|useScroll|useInView|whileInView)

- [### Scroll animation examples

  See all examples & tutorials, with full copy & paste source code.](https://motion.dev/examples?platform=react&search=scroll|useScroll|useInView|whileInView)

- [### Scroll animation examples

  See all examples & tutorials, with full copy & paste source code.](https://motion.dev/examples?platform=react&search=scroll|useScroll|useInView|whileInView)

- [Tutorial

  ### Parallax

  An example of creating a parallax effect using Motion for React's useScroll hook.](../tutorials/react-parallax)

- [Tutorial

  ### Parallax

  An example of creating a parallax effect using Motion for React's useScroll hook.](../tutorials/react-parallax)

- [Tutorial

  ### Parallax

  An example of creating a parallax effect using Motion for React's useScroll hook.](../tutorials/react-parallax)

Previous

[Layout animation](./react-layout-animations)

Next

[SVG animation](./react-svg-animation)

Motion+

Motion+

Motion+

## Level up your animations with Motion+

Mastered the basics of scroll-linked animations? The Motion+ vault contains dozens of exclusive examples showcasing advanced effects like parallax, scroll-triggered tickers, and more.

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