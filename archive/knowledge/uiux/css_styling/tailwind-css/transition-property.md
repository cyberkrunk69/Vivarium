# transition-property

Source: https://tailwindcss.com/docs/transition-property

---

| Class | Styles |
| --- | --- |
| `transition` | `transition-property: color, background-color, border-color, outline-color, text-decoration-color, fill, stroke, --tw-gradient-from, --tw-gradient-via, --tw-gradient-to, opacity, box-shadow, transform, translate, scale, rotate, filter, -webkit-backdrop-filter, backdrop-filter, display, content-visibility, overlay, pointer-events; transition-timing-function: var(--default-transition-timing-function); /* cubic-bezier(0.4, 0, 0.2, 1) */ transition-duration: var(--default-transition-duration); /* 150ms */` |
| `transition-all` | `transition-property: all; transition-timing-function: var(--default-transition-timing-function); /* cubic-bezier(0.4, 0, 0.2, 1) */ transition-duration: var(--default-transition-duration); /* 150ms */` |
| `transition-colors` | `transition-property: color, background-color, border-color, outline-color, text-decoration-color, fill, stroke, --tw-gradient-from, --tw-gradient-via, --tw-gradient-to; transition-timing-function: var(--default-transition-timing-function); /* cubic-bezier(0.4, 0, 0.2, 1) */ transition-duration: var(--default-transition-duration); /* 150ms */` |
| `transition-opacity` | `transition-property: opacity; transition-timing-function: var(--default-transition-timing-function); /* cubic-bezier(0.4, 0, 0.2, 1) */ transition-duration: var(--default-transition-duration); /* 150ms */` |
| `transition-shadow` | `transition-property: box-shadow; transition-timing-function: var(--default-transition-timing-function); /* cubic-bezier(0.4, 0, 0.2, 1) */ transition-duration: var(--default-transition-duration); /* 150ms */` |
| `transition-transform` | `transition-property: transform, translate, scale, rotate; transition-timing-function: var(--default-transition-timing-function); /* cubic-bezier(0.4, 0, 0.2, 1) */ transition-duration: var(--default-transition-duration); /* 150ms */` |
| `transition-none` | `transition-property: none;` |
| `transition-(<custom-property>)` | `transition-property: var(<custom-property>); transition-timing-function: var(--default-transition-timing-function); /* cubic-bezier(0.4, 0, 0.2, 1) */ transition-duration: var(--default-transition-duration); /* 150ms */` |
| `transition-[<value>]` | `transition-property: <value>; transition-timing-function: var(--default-transition-timing-function); /* cubic-bezier(0.4, 0, 0.2, 1) */ transition-duration: var(--default-transition-duration); /* 150ms */` |

## [Examples](#examples)

### [Basic example](#basic-example)

Use utilities like `transition` and `transition-colors` to specify which properties should transition when they change:

Hover the button to see the expected behavior

Save Changes

```
<button class="bg-blue-500 transition delay-150 duration-300 ease-in-out hover:-translate-y-1 hover:scale-110 hover:bg-indigo-500 ...">  Save Changes</button>
```

### [Supporting reduced motion](#supporting-reduced-motion)

For situations where the user has specified that they prefer reduced motion, you can conditionally apply animations and transitions using the `motion-safe` and `motion-reduce` variants:

```
<button class="transform transition hover:-translate-y-1 motion-reduce:transition-none motion-reduce:hover:transform-none ...">  <!-- ... --></button>
```

### [Using a custom value](#using-a-custom-value)

Use the `transition-[<value>]` syntax to set the transition properties based on a completely custom value:

```
<button class="transition-[height] ...">  <!-- ... --></button>
```

For CSS variables, you can also use the `transition-(<custom-property>)` syntax:

```
<button class="transition-(--my-properties) ...">  <!-- ... --></button>
```

This is just a shorthand for `transition-[var(<custom-property>)]` that adds the `var()` function for you automatically.

### [Responsive design](#responsive-design)

Prefix a `transition-property` utility with a breakpoint variant like `md:` to only apply the utility at medium screen sizes and above:

```
<button class="transition-none md:transition-all ...">  <!-- ... --></button>
```

Learn more about using variants in the [variants documentation](/docs/hover-focus-and-other-states).