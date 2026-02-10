# gap

Source: https://tailwindcss.com/docs/gap

---

| Class | Styles |
| --- | --- |
| `gap-<number>` | `gap: calc(var(--spacing) * <value>);` |
| `gap-(<custom-property>)` | `gap: var(<custom-property>);` |
| `gap-[<value>]` | `gap: <value>;` |
| `gap-x-<number>` | `column-gap: calc(var(--spacing) * <value>);` |
| `gap-x-(<custom-property>)` | `column-gap: var(<custom-property>);` |
| `gap-x-[<value>]` | `column-gap: <value>;` |
| `gap-y-<number>` | `row-gap: calc(var(--spacing) * <value>);` |
| `gap-y-(<custom-property>)` | `row-gap: var(<custom-property>);` |
| `gap-y-[<value>]` | `row-gap: <value>;` |

## [Examples](#examples)

### [Basic example](#basic-example)

Use `gap-<number>` utilities like `gap-2` and `gap-4` to change the gap between both rows and columns in grid and flexbox layouts:

01

02

03

04

```
<div class="grid grid-cols-2 gap-4">  <div>01</div>  <div>02</div>  <div>03</div>  <div>04</div></div>
```

### [Changing row and column gaps independently](#changing-row-and-column-gaps-independently)

Use `gap-x-<number>` or `gap-y-<number>` utilities like `gap-x-8` and `gap-y-4` to change the gap between columns and rows independently:

01

02

03

04

05

06

```
<div class="grid grid-cols-3 gap-x-8 gap-y-4">  <div>01</div>  <div>02</div>  <div>03</div>  <div>04</div>  <div>05</div>  <div>06</div></div>
```

### [Using a custom value](#using-a-custom-value)

Use utilities like `gap-[<value>]`,`gap-x-[<value>]`, and `gap-y-[<value>]` to set the gap based on a completely custom value:

```
<div class="gap-[10vw] ...">  <!-- ... --></div>
```

For CSS variables, you can also use the `gap-(<custom-property>)` syntax:

```
<div class="gap-(--my-gap) ...">  <!-- ... --></div>
```

This is just a shorthand for `gap-[var(<custom-property>)]` that adds the `var()` function for you automatically.

### [Responsive design](#responsive-design)

Prefix `gap`,`column-gap`, and `row-gap` utilities with a breakpoint variant like `md:` to only apply the utility at medium screen sizes and above:

```
<div class="grid gap-4 md:gap-6 ...">  <!-- ... --></div>
```

Learn more about using variants in the [variants documentation](/docs/hover-focus-and-other-states).