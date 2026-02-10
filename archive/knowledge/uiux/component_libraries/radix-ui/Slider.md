# Slider

Source: https://www.radix-ui.com/primitives/docs/components/slider

---

[Radix Homepage](/)[Made by WorkOS](https://workos.com)

[Radix Homepage](/)[Made by WorkOS](https://workos.com)

[ThemesThemes](/)[PrimitivesPrimitives](/primitives)[IconsIcons](/icons)[ColorsColors](/colors)

[Documentation](/primitives/docs)[Case studies](/primitives/case-studies)[Blog](/blog)

Search

`/`

#### Overview

[Introduction](/primitives/docs/overview/introduction)[Getting started](/primitives/docs/overview/getting-started)[Accessibility](/primitives/docs/overview/accessibility)[Releases](/primitives/docs/overview/releases)

#### Guides

[Styling](/primitives/docs/guides/styling)[Animation](/primitives/docs/guides/animation)[Composition](/primitives/docs/guides/composition)[Server-side rendering](/primitives/docs/guides/server-side-rendering)

#### Components

[Accordion](/primitives/docs/components/accordion)[Alert Dialog](/primitives/docs/components/alert-dialog)[Aspect Ratio](/primitives/docs/components/aspect-ratio)[Avatar](/primitives/docs/components/avatar)[Checkbox](/primitives/docs/components/checkbox)[Collapsible](/primitives/docs/components/collapsible)[Context Menu](/primitives/docs/components/context-menu)[Dialog](/primitives/docs/components/dialog)[Dropdown Menu](/primitives/docs/components/dropdown-menu)[Form

Preview](/primitives/docs/components/form)[Hover Card](/primitives/docs/components/hover-card)[Label](/primitives/docs/components/label)[Menubar](/primitives/docs/components/menubar)[Navigation Menu](/primitives/docs/components/navigation-menu)[One-Time Password Field

Preview](/primitives/docs/components/one-time-password-field)[Password Toggle Field

Preview](/primitives/docs/components/password-toggle-field)[Popover](/primitives/docs/components/popover)[Progress](/primitives/docs/components/progress)[Radio Group](/primitives/docs/components/radio-group)[Scroll Area](/primitives/docs/components/scroll-area)[Select](/primitives/docs/components/select)[Separator](/primitives/docs/components/separator)[Slider](/primitives/docs/components/slider)[Switch](/primitives/docs/components/switch)[Tabs](/primitives/docs/components/tabs)[Toast](/primitives/docs/components/toast)[Toggle](/primitives/docs/components/toggle)[Toggle Group](/primitives/docs/components/toggle-group)[Toolbar](/primitives/docs/components/toolbar)[Tooltip](/primitives/docs/components/tooltip)

#### Utilities

[Accessible Icon](/primitives/docs/utilities/accessible-icon)[Direction Provider](/primitives/docs/utilities/direction-provider)[Portal](/primitives/docs/utilities/portal)[Slot](/primitives/docs/utilities/slot)[Visually Hidden](/primitives/docs/utilities/visually-hidden)

Components

# Slider

An input where the user selects a value from within a given range.

index.jsxindex.jsxstyles.cssstyles.css

```
import * as React from "react";

import { Slider } from "radix-ui";

import "./styles.css";

const SliderDemo = () => (

<form>

<Slider.Root className="SliderRoot" defaultValue={[50]} max={100} step={1}>

<Slider.Track className="SliderTrack">

<Slider.Range className="SliderRange" />

</Slider.Track>

<Slider.Thumb className="SliderThumb" aria-label="Volume" />

</Slider.Root>

</form>

);

export default SliderDemo;

Expand code
```

## Features

Can be controlled or uncontrolled.

Supports multiple thumbs.

Supports a minimum value between thumbs.

Supports touch or click on track to update value.

Supports Right to Left direction.

Full keyboard navigation.

## [Installation](#installation)

Install the component from your command line.

```
npm install @radix-ui/react-slider
```

## [Anatomy](#anatomy)

Import all parts and piece them together.

```
import { Slider } from "radix-ui";

export default () => (

<Slider.Root>

<Slider.Track>

<Slider.Range />

</Slider.Track>

<Slider.Thumb />

</Slider.Root>

);
```

## [API Reference](#api-reference)

### [Root](#root)

Contains all the parts of a slider. It will render an `input` for each thumb when used within a `form` to ensure events propagate correctly.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |
| `defaultValue` Prop description | `number[]` | No default value |
| `value` Prop description | `number[]` | No default value |
| `onValueChange` Prop description | `function` See full type | No default value |
| `onValueCommit` Prop description | `function` See full type | No default value |
| `name` Prop description | `string` | No default value |
| `disabled` Prop description | `boolean` | `false` |
| `orientation` Prop description | `enum` See full type | `"horizontal"` |
| `dir` Prop description | `enum` See full type | No default value |
| `inverted` Prop description | `boolean` | `false` |
| `min` Prop description | `number` | `0` |
| `max` Prop description | `number` | `100` |
| `step` Prop description | `number` | `1` |
| `minStepsBetweenThumbs` Prop description | `number` | `0` |
| `form` Prop description | `string` | No default value |

| Data attribute | Values |
| --- | --- |
| `[data-disabled]` | Present when disabled |
| `[data-orientation]` | `"vertical" | "horizontal"` |

### [Track](#track)

The track that contains the `Slider.Range`.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |

| Data attribute | Values |
| --- | --- |
| `[data-disabled]` | Present when disabled |
| `[data-orientation]` | `"vertical" | "horizontal"` |

### [Range](#range)

The range part. Must live inside `Slider.Track`.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |

| Data attribute | Values |
| --- | --- |
| `[data-disabled]` | Present when disabled |
| `[data-orientation]` | `"vertical" | "horizontal"` |

### [Thumb](#thumb)

A draggable thumb. You can render multiple thumbs.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |

| Data attribute | Values |
| --- | --- |
| `[data-disabled]` | Present when disabled |
| `[data-orientation]` | `"vertical" | "horizontal"` |

## [Examples](#examples)

### [Vertical orientation](#vertical-orientation)

Use the `orientation` prop to create a vertical slider.

```
// index.jsx

import { Slider } from "radix-ui";

import "./styles.css";

export default () => (

<Slider.Root
		className="SliderRoot"
		defaultValue={[50]}
		orientation="vertical"
	>

<Slider.Track className="SliderTrack">

<Slider.Range className="SliderRange" />

</Slider.Track>

<Slider.Thumb className="SliderThumb" />

</Slider.Root>

);
```

```
/* styles.css */

.SliderRoot {

position: relative;

display: flex;

align-items: center;

}

.SliderRoot[data-orientation="vertical"] {

flex-direction: column;

width: 20px;

height: 100px;

}

.SliderTrack {

position: relative;

flex-grow: 1;

background-color: grey;

}

.SliderTrack[data-orientation="vertical"] {

width: 3px;

}

.SliderRange {

position: absolute;

background-color: black;

}

.SliderRange[data-orientation="vertical"] {

width: 100%;

}

.SliderThumb {

display: block;

width: 20px;

height: 20px;

background-color: black;

}
```

### [Create a range](#create-a-range)

Add multiple thumbs and values to create a range slider.

```
import { Slider } from "radix-ui";

export default () => (

<Slider.Root defaultValue={[25, 75]}>

<Slider.Track>

<Slider.Range />

</Slider.Track>

<Slider.Thumb />

<Slider.Thumb />

</Slider.Root>

);
```

### [Define step size](#define-step-size)

Use the `step` prop to increase the stepping interval.

```
import { Slider } from "radix-ui";

export default () => (

<Slider.Root defaultValue={[50]} step={10}>

<Slider.Track>

<Slider.Range />

</Slider.Track>

<Slider.Thumb />

</Slider.Root>

);
```

### [Prevent thumb overlap](#prevent-thumb-overlap)

Use `minStepsBetweenThumbs` to avoid thumbs with equal values.

```
import { Slider } from "radix-ui";

export default () => (

<Slider.Root defaultValue={[25, 75]} step={10} minStepsBetweenThumbs={1}>

<Slider.Track>

<Slider.Range />

</Slider.Track>

<Slider.Thumb />

<Slider.Thumb />

</Slider.Root>

);
```

## [Accessibility](#accessibility)

Adheres to the [Slider WAI-ARIA design pattern](https://www.w3.org/WAI/ARIA/apg/patterns/slider-multithumb).

### [Keyboard Interactions](#keyboard-interactions)

| Key | Description |
| --- | --- |
| `ArrowRight` | Increments/decrements by the `step` value depending on `orientation`. |
| `ArrowLeft` | Increments/decrements by the `step` value depending on `orientation`. |
| `ArrowUp` | Increases the value by the `step` amount. |
| `ArrowDown` | Decreases the value by the `step` amount. |
| `PageUp` | Increases the value by a larger `step`. |
| `PageDown` | Decreases the value by a larger `step`. |
| `Shift + ArrowUp` | Increases the value by a larger `step`. |
| `Shift + ArrowDown` | Decreases the value by a larger `step`. |
| `Home` | Sets the value to its minimum. |
| `End` | Sets the value to its maximum. |

## [Custom APIs](#custom-apis)

Create your own API by abstracting the primitive parts into your own component.

### [Abstract all parts](#abstract-all-parts)

This example abstracts all of the `Slider` parts so it can be used as a self closing element.

#### Usage

```
import { Slider } from "./your-slider";

export default () => <Slider defaultValue={[25]} />;
```

#### Implementation

```
// your-slider.jsx

import { Slider as SliderPrimitive } from "radix-ui";

export const Slider = React.forwardRef((props, forwardedRef) => {

const value = props.value || props.defaultValue;

return (

<SliderPrimitive.Slider {...props} ref={forwardedRef}>

<SliderPrimitive.Track>

<SliderPrimitive.Range />

</SliderPrimitive.Track>

{value.map((_, i) => (

<SliderPrimitive.Thumb key={i} />

))}

</SliderPrimitive.Slider>

);

});
```

## [Caveats](#caveats)

### [Mouse events are not fired](#mouse-events-are-not-fired)

Because of [a limitation](https://github.com/radix-ui/primitives/blob/83a8c13bf66f3d9f17d77caeb187a69eb146930b/packages/react/slider/src/Slider.tsx#L383-L384) we faced during implementation, the following example won't work as expected and the `onMouseDown` and `onMouseUp` event handlers won't be fired:

```
<Slider.Root
	onMouseDown={() => console.log("onMouseDown")}
	onMouseUp={() => console.log("onMouseUp")}
>

…

</Slider.Root>
```

We recommend using pointer events instead (eg. `onPointerDown`, `onPointerUp`). Regardless of the above limitation, these events are better suited for cross-platform/device handling as they are fired for all pointer input types (mouse, touch, pen, etc.).

Previous[Separator](/primitives/docs/components/separator)

Next[Switch](/primitives/docs/components/switch)

[Edit this page on GitHub.](https://github.com/radix-ui/website/edit/main/data/primitives/docs/components/slider.mdx "Edit this page on GitHub.")