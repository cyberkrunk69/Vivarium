# svelte/transition • Svelte Docs

Source: https://svelte.dev/docs/svelte-transition

---

```
import {
	function blur(node: Element, { delay, duration, easing, amount, opacity }?: BlurParams | undefined): TransitionConfig

Animates a blur filter alongside an element’s opacity.

blur,
	

```
function crossfade({ fallback, ...defaults }: CrossfadeParams & {
    fallback?: (node: Element, params: CrossfadeParams, intro: boolean) => TransitionConfig;
}): [(node: any, params: CrossfadeParams & {
    key: any;
}) => () => TransitionConfig, (node: any, params: CrossfadeParams & {
    key: any;
}) => () => TransitionConfig]
```

The crossfade function creates a pair of transitions called send and receive. When an element is ‘sent’, it looks for a corresponding element being ‘received’, and generates a transition that transforms the element to its counterpart’s position and fades it out. When an element is ‘received’, the reverse happens. If there is no counterpart, the fallback transition is used.

crossfade,
	

```
function draw(node: SVGElement & {
    getTotalLength(): number;
}, { delay, speed, duration, easing }?: DrawParams | undefined): TransitionConfig
```

Animates the stroke of an SVG element, like a snake in a tube. in transitions begin with the path invisible and draw the path to the screen over time. out transitions start in a visible state and gradually erase the path. draw only works with elements that have a getTotalLength method, like &#x3C;path> and &#x3C;polyline>.

draw,
	function fade(node: Element, { delay, duration, easing }?: FadeParams | undefined): TransitionConfig

Animates the opacity of an element from 0 to the current opacity for in transitions and from the current opacity to 0 for out transitions.

fade,
	function fly(node: Element, { delay, duration, easing, x, y, opacity }?: FlyParams | undefined): TransitionConfig

Animates the x and y positions and the opacity of an element. in transitions animate from the provided values, passed as parameters to the element’s default values. out transitions animate from the element’s default values to the provided values.

fly,
	function scale(node: Element, { delay, duration, easing, start, opacity }?: ScaleParams | undefined): TransitionConfig

Animates the opacity and scale of an element. in transitions animate from the provided values, passed as parameters, to an element’s current (default) values. out transitions animate from an element’s default values to the provided values.

scale,
	function slide(node: Element, { delay, duration, easing, axis }?: SlideParams | undefined): TransitionConfig

Slides an element in and out.

slide
} from 'svelte/transition';
```

## blur

Animates a `blur` filter alongside an element’s opacity.

```
function blur(
	node: Element,
	{
		delay,
		duration,
		easing,
		amount,
		opacity
	}?: BlurParams | undefined
): TransitionConfig;
```

## crossfade

The `crossfade` function creates a pair of [transitions](/docs/svelte/transition) called `send` and `receive`. When an element is ‘sent’, it looks for a corresponding element being ‘received’, and generates a transition that transforms the element to its counterpart’s position and fades it out. When an element is ‘received’, the reverse happens. If there is no counterpart, the `fallback` transition is used.

```
function crossfade({
	fallback,
	...defaults
}: CrossfadeParams & {
	fallback?: (
		node: Element,
		params: CrossfadeParams,
		intro: boolean
	) => TransitionConfig;
}): [
	(
		node: any,
		params: CrossfadeParams & {
			key: any;
		}
	) => () => TransitionConfig,
	(
		node: any,
		params: CrossfadeParams & {
			key: any;
		}
	) => () => TransitionConfig
];
```

## draw

Animates the stroke of an SVG element, like a snake in a tube. `in` transitions begin with the path invisible and draw the path to the screen over time. `out` transitions start in a visible state and gradually erase the path. `draw` only works with elements that have a `getTotalLength` method, like `<path>` and `<polyline>`.

```
function draw(
	node: SVGElement & {
		getTotalLength(): number;
	},
	{
		delay,
		speed,
		duration,
		easing
	}?: DrawParams | undefined
): TransitionConfig;
```

## fade

Animates the opacity of an element from 0 to the current opacity for `in` transitions and from the current opacity to 0 for `out` transitions.

```
function fade(
	node: Element,
	{ delay, duration, easing }?: FadeParams | undefined
): TransitionConfig;
```

## fly

Animates the x and y positions and the opacity of an element. `in` transitions animate from the provided values, passed as parameters to the element’s default values. `out` transitions animate from the element’s default values to the provided values.

```
function fly(
	node: Element,
	{
		delay,
		duration,
		easing,
		x,
		y,
		opacity
	}?: FlyParams | undefined
): TransitionConfig;
```

## scale

Animates the opacity and scale of an element. `in` transitions animate from the provided values, passed as parameters, to an element’s current (default) values. `out` transitions animate from an element’s default values to the provided values.

```
function scale(
	node: Element,
	{
		delay,
		duration,
		easing,
		start,
		opacity
	}?: ScaleParams | undefined
): TransitionConfig;
```

## slide

Slides an element in and out.

```
function slide(
	node: Element,
	{
		delay,
		duration,
		easing,
		axis
	}?: SlideParams | undefined
): TransitionConfig;
```

## BlurParams

```
interface BlurParams {…}
```

```
delay?: number;
```

```
duration?: number;
```

```
easing?: EasingFunction;
```

```
amount?: number | string;
```

```
opacity?: number;
```

## CrossfadeParams

```
interface CrossfadeParams {…}
```

```
delay?: number;
```

```
duration?: number | ((len: number) => number);
```

```
easing?: EasingFunction;
```

## DrawParams

```
interface DrawParams {…}
```

```
delay?: number;
```

```
speed?: number;
```

```
duration?: number | ((len: number) => number);
```

```
easing?: EasingFunction;
```

## EasingFunction

```
type EasingFunction = (t: number) => number;
```

## FadeParams

```
interface FadeParams {…}
```

```
delay?: number;
```

```
duration?: number;
```

```
easing?: EasingFunction;
```

## FlyParams

```
interface FlyParams {…}
```

```
delay?: number;
```

```
duration?: number;
```

```
easing?: EasingFunction;
```

```
x?: number | string;
```

```
y?: number | string;
```

```
opacity?: number;
```

## ScaleParams

```
interface ScaleParams {…}
```

```
delay?: number;
```

```
duration?: number;
```

```
easing?: EasingFunction;
```

```
start?: number;
```

```
opacity?: number;
```

## SlideParams

```
interface SlideParams {…}
```

```
delay?: number;
```

```
duration?: number;
```

```
easing?: EasingFunction;
```

```
axis?: 'x' | 'y';
```

## TransitionConfig

```
interface TransitionConfig {…}
```

```
delay?: number;
```

```
duration?: number;
```

```
easing?: EasingFunction;
```

```
css?: (t: number, u: number) => string;
```

```
tick?: (t: number, u: number) => void;
```

[Edit this page on GitHub](https://github.com/sveltejs/svelte/edit/main/documentation/docs/98-reference/21-svelte-transition.md)  [llms.txt](/docs/svelte/svelte-transition/llms.txt)

previous next

[svelte/store](/docs/svelte/svelte-store) [Compiler errors](/docs/svelte/compiler-errors)