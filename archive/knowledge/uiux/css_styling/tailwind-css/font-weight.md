# font-weight

Source: https://tailwindcss.com/docs/font-weight

---

| Class | Styles |
| --- | --- |
| `font-thin` | `font-weight: 100;` |
| `font-extralight` | `font-weight: 200;` |
| `font-light` | `font-weight: 300;` |
| `font-normal` | `font-weight: 400;` |
| `font-medium` | `font-weight: 500;` |
| `font-semibold` | `font-weight: 600;` |
| `font-bold` | `font-weight: 700;` |
| `font-extrabold` | `font-weight: 800;` |
| `font-black` | `font-weight: 900;` |
| `font-(<custom-property>)` | `font-weight: var(<custom-property>);` |
| `font-[<value>]` | `font-weight: <value>;` |

## [Examples](#examples)

### [Basic example](#basic-example)

Use utilities like `font-thin` and `font-bold` to set the font weight of an element:

font-light

The quick brown fox jumps over the lazy dog.

font-normal

The quick brown fox jumps over the lazy dog.

font-medium

The quick brown fox jumps over the lazy dog.

font-semibold

The quick brown fox jumps over the lazy dog.

font-bold

The quick brown fox jumps over the lazy dog.

```
<p class="font-light ...">The quick brown fox ...</p><p class="font-normal ...">The quick brown fox ...</p><p class="font-medium ...">The quick brown fox ...</p><p class="font-semibold ...">The quick brown fox ...</p><p class="font-bold ...">The quick brown fox ...</p>
```

### [Using a custom value](#using-a-custom-value)

Use the `font-[<value>]` syntax to set the font weight based on a completely custom value:

```
<p class="font-[1000] ...">  Lorem ipsum dolor sit amet...</p>
```

For CSS variables, you can also use the `font-(weight:<custom-property>)` syntax:

```
<p class="font-(weight:--my-font-weight) ...">  Lorem ipsum dolor sit amet...</p>
```

This is just a shorthand for `font-[weight:var(<custom-property>)]` that adds the `var()` function for you automatically.

### [Responsive design](#responsive-design)

Prefix a `font-weight` utility with a breakpoint variant like `md:` to only apply the utility at medium screen sizes and above:

```
<p class="font-normal md:font-bold ...">  Lorem ipsum dolor sit amet...</p>
```

Learn more about using variants in the [variants documentation](/docs/hover-focus-and-other-states).

## [Customizing your theme](#customizing-your-theme)

Use the `--font-weight-*` theme variables to customize the font weight utilities in your project:

```
@theme {  --font-weight-extrablack: 1000; }
```

Now the `font-extrablack` utility can be used in your markup:

```
<div class="font-extrablack">  <!-- ... --></div>
```

Learn more about customizing your theme in the [theme documentation](/docs/theme#customizing-your-theme).