# svelte/animate • Svelte Docs

Source: https://svelte.dev/docs/svelte-animate

---

```
import { 

```
function flip(node: Element, { from, to }: {
    from: DOMRect;
    to: DOMRect;
}, params?: FlipParams): AnimationConfig
```

The flip function calculates the start and end position of an element and animates between them, translating the x and y values.
flip stands for First, Last, Invert, Play.

flip } from 'svelte/animate';
```

## flip

The flip function calculates the start and end position of an element and animates between them, translating the x and y values.
`flip` stands for [First, Last, Invert, Play](https://aerotwist.com/blog/flip-your-animations/).

```
function flip(
	node: Element,
	{
		from,
		to
	}: {
		from: DOMRect;
		to: DOMRect;
	},
	params?: FlipParams
): AnimationConfig;
```

## AnimationConfig

```
interface AnimationConfig {…}
```

```
delay?: number;
```

```
duration?: number;
```

```
easing?: (t: number) => number;
```

```
css?: (t: number, u: number) => string;
```

```
tick?: (t: number, u: number) => void;
```

## FlipParams

```
interface FlipParams {…}
```

```
delay?: number;
```

```
duration?: number | ((len: number) => number);
```

```
easing?: (t: number) => number;
```

[Edit this page on GitHub](https://github.com/sveltejs/svelte/edit/main/documentation/docs/98-reference/21-svelte-animate.md)  [llms.txt](/docs/svelte/svelte-animate/llms.txt)

previous next

[svelte/action](/docs/svelte/svelte-action) [svelte/attachments](/docs/svelte/svelte-attachments)