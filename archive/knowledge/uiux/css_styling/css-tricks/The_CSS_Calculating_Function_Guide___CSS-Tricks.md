# The CSS Calculating Function Guide | CSS-Tricks

Source: https://css-tricks.com/a-complete-guide-to-calc-in-css/

---

CSS has a special `calc()` function for doing basic math. In this guide, let’s cover just about everything there is to know about this very useful function.

Here’s an [example](https://codepen.io/team/css-tricks/pen/MwPmVG):

```
.main-content {
  /* Subtract 80px from 100vh */
  height: calc(100vh - 80px);
}
```

In this guide, let’s cover just about everything there is to know about this very useful function.

### `calc()` is for values

The only place you can use the `calc()` function is in *values*. See these examples where we’re setting the value for a number of different properties.

```
.el {
  font-size: calc(3vw + 2px);
  width:     calc(100% - 20px);
  height:    calc(100vh - 20px);
  padding:   calc(1vw + 5px);
}
```

It could be used for only *part* of a property too, for example:

```
.el {
  margin: 10px calc(2vw + 5px);
  border-radius: 15px calc(15px / 3) 4px 2px;
  transition: transform calc(1s - 120ms);
}
```

It can even be a part of *another* function that forms a part of a property! For example, here’s `calc()` used within the color stops of a gradient

```
.el {
  background: #1E88E5 linear-gradient(
    to bottom,
    #1E88E5,
    #1E88E5 calc(50% - 10px),
    #3949AB calc(50% + 10px),
    #3949AB
  );
}
```

### `calc()` is for lengths and other *numeric* things

Notice all the examples above are essentially numbers-based. We’ll get to some of the caveats of how the numbers can be used (because sometimes you don’t need a unit), but this is for number math, not strings or anything like that.

```
.el {
  /* Nope! */
  counter-reset: calc("My " + "counter");
}
.el::before {
  /* Nope! */
  content: calc("Candyman " * 3);
}
```

There are many [lengths of CSS though](https://css-tricks.com/the-lengths-of-css/), and they can all be used with `calc()`:

- px
- %
- em
- rem
- in
- mm
- cm
- pt
- pc
- ex
- ch
- vh
- vw
- vmin
- vmax

Unit-less numbers are acceptable, too. For example `line-height: calc(1.2 * 1.2);` as well as angles like `transform: rotate(calc(10deg * 5));`.

You can also *not* perform any calculation and it is still valid:

```
.el {
  /* Little weird but OK */
  width: calc(20px);
}
```

### Nope on media queries

When `calc()` is used correctly (length units used as a value to a property), sadly, `calc()` won’t work when applied to media queries.

```
@media (max-width: 40rem) {
  /* Narrower or exactly 40rem */
}

/* Nope! */
@media (min-width: calc(40rem + 1px)) {
  /* Wider than 40rem */
}
```

It would be cool someday because you could do [mutually exclusive media queries](https://css-tricks.com/logic-in-media-queries/#article-header-id-4) in a fairly logical way (like above).

### Mixing units 🎉

This is perhaps the most valuable feature of `calc()`! Almost every example above has already done this, but just to put a point on it, here it is mixing different units:

```
/* Percentage units being mixed with pixel units */
width: calc(100% - 20px);
```

That’s saying: *As wide as the element is, minus 20 pixels.*

There is *literally no way* to pre-calculate that value in pixels alone in a fluid width situation. In other words, you can’t preprocess `calc()` with something like Sass as an attempt to complete a polyfill. Not that you need to, as the [browser support](#browser-support) is fine. But the point is that it has to be done in the browser (at “runtime”) when you mix units in this way, which is most of the value of `calc()`.

Here’s some other examples of mixing units:

```
transform: rotate(calc(1turn + 45deg));

animation-delay: calc(1s + 15ms);
```

Those probably could be preprocessed as they mix units that aren’t relative to anything that is determined at runtime.

### Comparison to preprocessor math

We just covered that you can’t preprocess the most useful things that `calc()` can do. But there is a smidge of overlap. For example, Sass has math built into it, so you can do things like:

```
$padding: 1rem;

.el[data-padding="extra"] {
  padding: $padding + 2rem; // processes to 3rem;
  margin-bottom: $padding * 2; // processes to 2rem; 
}
```

Even math with units is working there, adding same-unit values together or multiplying by unit-less numbers. But you can’t mix units and it has similar limitations to `calc()` (e.g. like multiplying and dividing must be with unit-less numbers).

### Show the math

Even you aren’t using a feature that is uniquely possible only with `calc()`, it can be used to [“show your work” inside CSS](https://css-tricks.com/keep-math-in-the-css/). For example, say you need to calculate exactly 1⁄7th the width of an element…

```
.el {
  /* This is easier to understand */
  width: calc(100% / 7);

  /* Than this is */
  width: 14.2857142857%;
}
```

That might pan out in some kind of self-created CSS API like:

```
[data-columns="7"] .col { width: calc(100% / 7); }
[data-columns="6"] .col { width: calc(100% / 6); }
[data-columns="5"] .col { width: calc(100% / 5); }
[data-columns="4"] .col { width: calc(100% / 4); }
[data-columns="3"] .col { width: calc(100% / 3); }
[data-columns="2"] .col { width: calc(100% / 2); }
```

### The Math operators of `calc()`

You’ve got `+`, `-`, `*`, and `/`. But they differ in how you are required to use them.

#### Addition (`+`) and subtraction (`-`) require both numbers to be lengths

```
.el {
  /* Valid 👍 */
  margin: calc(10px + 10px);

  /* Invalid 👎 */
  margin: calc(10px + 5);
}
```

Invalid values invalidate the whole individual declaration.

#### Division (`/`) requires the second number to be unitless

```
.el {
  /* Valid 👍 */
  margin: calc(30px / 3);

  /* Invalid 👎 */
  margin: calc(30px / 10px);

  /* Invalid 👎 (can't divide by 0) */
  margin: calc(30px / 0);
}
```

#### Multiplication (\*) requires one of the numbers to be unitless

```
.el {
  /* Valid 👍 */
  margin: calc(10px * 3);

  /* Valid 👍 */
  margin: calc(3 * 10px);

  /* Invalid 👎 */
  margin: calc(30px * 3px);
}
```

#### Whitespace matters

Well, it does for **addition** and **subtraction**.

```
.el {
  /* Valid 👍 */
  font-size: calc(3vw + 2px);

  /* Invalid 👎 */
  font-size: calc(3vw+2px);

  /* Valid 👍 */
  font-size: calc(3vw - 2px);

  /* Invalid 👎 */
  font-size: calc(3vw-2px);
}
```

Negative numbers are OK (e.g. `calc(5vw - -5px)`), but that’s an example of where the whitespace is not only required, but helpful too.

Tab Atkins tells me that the reason for the required spacing around `+` and `-` is actually because of parsing concerns. I can’t say I fully understand it, but for example, `2px-3px` is parsed as the number “2” and the unit “px-3px” which isn’t doing anybody any good, and the `+` has other issues like getting “consumed by the number syntax.” I would have guessed the whitespace would have had to do with the `--` syntax of custom properties, but nope!

Multiplication and division do not need the whitespace around the operators. But I’d think good general advice is to include the space for readability and muscle memory for the other operators.

Whitespace around the outsides doesn’t matter. You can even do line breaks if you’d like:

```
.el {
  /* Valid 👍 */
  width: calc(
    100%     /   3
  );
}
```

Careful about this, though: no spaces between `calc()` and the opening paren.

```
.el {
  /* Invalid 👎 */
  width: calc (100% / 3);
}
```

### Nesting `calc(calc());`

You can but it’s never necessary. It’s the same as using an extra set of parentheses without the `calc()` part. For example:

```
.el {
  width: calc(
    calc(100% / 3)
    -
    calc(1rem * 2)
  );
}
```

You don’t need those inside `calc()` because the parens work alone:

```
.el {
  width: calc(
   (100% / 3)
    -
   (1rem * 2)
  );
}
```

And in this case, the “order of operations” helps us even without the parentheses. That is, division and multiplication happen *first* (before addition and subtraction), so the parentheses aren’t needed at all. It could be written like this:

```
.el {
  width: calc(100% / 3 - 1rem * 2);
}
```

But feel free to use the parens if you feel like it adds clarity. If the order of operations doesn’t work in your favor (e.g. you really need to do the addition or subtraction first), you’ll need parens.

```
.el {
  /* This */
  width: calc(100% + 2rem / 2);

  /* Is very different from this */
  width: calc((100% + 2rem) / 2);
}
```

### CSS custom properties and `calc()` 🎉

Other than the amazing ability of `calc()` to mix units, the next most awesome thing about `calc()` is using it with custom properties. Custom properties can have values that you then use in a calculation:

```
html {
  --spacing: 10px;
}

.module {
  padding: calc(var(--spacing) * 2);
}
```

I’m sure you can imagine a CSS setup where a ton of configuration happens at the top by setting a bunch of CSS custom properties and then letting the rest of the CSS use them as needed.

Custom properties can also reference each other. Here’s an example where some math is used (note the *lack* of a `calc()` function at first) and then later applied. (It ultimately has to be inside of a `calc()`.)

```
html {
  --spacing: 10px;
  --spacing-L: var(--spacing) * 2;
  --spacing-XL: var(--spacing) * 3;
}

.module[data-spacing="XL"] {
  padding: calc(var(--spacing-XL));
}
```

You may not like that, as you need to remember the `calc()` where you use the property then, but it’s possible and potentially interesting from a readability perspective.

Custom properties can come from the HTML, which is a pretty darn cool and useful thing sometimes. (See how [Splitting.js](https://splitting.js.org/guide.html#basic-usage) adds indexes to words/characters as an example.)

```
<div style="--index: 1;"> ... </div>
<div style="--index: 2;"> ... </div>
<div style="--index: 3;"> ... </div>
```

```
div {
  /* Index value comes from the HTML (with a fallback) */
  animation-delay: calc(var(--index, 1) * 0.2s);
}
```

#### Adding units later

In case you’re in a situation where it’s easier to store numbers without units, or do math with unit-less numbers ahead of time, you can always wait until you apply the number to add the unit by multiplying by 1 *and the unit*.

```
html {
  --importantNumber: 2;
}

.el {
  /* Number stays 2, but it has a unit now */
  padding: calc(var(--importantNumber) * 1rem);
}
```

#### Messing with colors

Color format like RGB and HSL have numbers you can mess with using `calc()`. For example, setting some base HSL values and then altering them forming a system of your own creation ([example](https://codepen.io/chriscoyier/pen/dyoVXEj)):

```
html {
  --H: 100;
  --S: 100%;
  --L: 50%;
}

.el {
  background: hsl(
    calc(var(--H) + 20),
    calc(var(--S) - 10%),
    calc(var(--L) + 30%)
  )
}
```

#### You can’t combine calc() and attr()

The `attr()` function in CSS *looks* appealing, like you can pull attribute values out of HTML and use them. But…

```
<div data-color="red">...</div>
```

```
div {
  /* Nope */
  color: attr(data-color);
}
```

Unfortunately, there are no “types” in play here, so the only thing `attr()` is for are strings in conjunction with the `content` property. That means this works:

```
div::before {
  content: attr(data-color);
}
```

I mention this because it might be tempting to try to pull a number in that way to use in a calculation, like:

```
<div class="grid" data-columns="7" data-gap="2">...</div>
```

```
.grid {
  display: grid;

  /* Neither of these work */
  grid-template-columns: repeat(attr(data-columns), 1fr);
  grid-gap: calc(1rem * attr(data-gap));
}
```

Fortunately, it doesn’t matter much because custom properties in the HTML are [just as useful or more](https://css-tricks.com/css-attr-function-got-nothin-custom-properties/)!

```
<div class="grid" style="--columns: 7; --gap: 2rem;">...</div>
```

```
.grid {
  display: grid;

  /* Yep! */
  grid-template-columns: repeat(var(--columns), 1fr);
  grid-gap: calc(var(--gap));
}
```

### Browser tooling

Browser DevTools will tend you show you the `calc()` as you authored it in the stylesheet.

![](https://i0.wp.com/css-tricks.com/wp-content/uploads/2020/03/DevTools-rules.png?resize=461%2C248&ssl=1)

Firefox DevTools – Rules

If you need to figure out the computed value, there is a Computed tab (in all browser DevTools, at least the ones I know about) that will show it to you.

![](https://i0.wp.com/css-tricks.com/wp-content/uploads/2020/03/ChromeDevTools-computed.png?resize=410%2C383&ssl=1)

Chrome DevTools – Computed

### Browser support

This browser support data is from [Caniuse](http://caniuse.com/#feat=calc), which has more detail. A number indicates that browser supports the feature at that version and up.

#### Desktop

| Chrome | Firefox | IE | Edge | Safari |
| --- | --- | --- | --- | --- |
| 19\* | 4\* | 11 | 12 | 6\* |

#### Mobile / Tablet

| Android Chrome | Android Firefox | Android | iOS Safari |
| --- | --- | --- | --- |
| 144 | 147 | 144 | 6.0-6.1\* |

If you really needed to support super far back (e.g. IE 8 or Firefox 3.6), the usual trick is to add another property or value before the one that uses `calc()`:

```
.el {
  width: 92%; /* Fallback */
  width: calc(100% - 2rem);
}
```

There are quite a few known issues for `calc()` as well, but they are all for old browsers. [Can I use… lists 13 of them](https://caniuse.com/#feat=calc). Here’s a handful:

- Firefox <59 does not support `calc()` on color functions. Example: `color: hsl(calc(60 * 2), 100%, 50%)`.
- IE 9-11 will not render the `box-shadow` property when `calc()` is used for any of the values.
- Neither IE 9-11 nor Edge support `width: calc()` on table cells.

### Use-case party

I asked some CSS developers when they last used `calc()` so we could have a nice taste here for how others use it in their day-to-day work.

> I used it to create a full-bleed utility class: `.full-bleed { width: 100vw; margin-left: calc(50% - 50vw); }` I’d say `calc()` is in my top 3 CSS things.

> I used it to make space for a sticky footer.

> I used it to set some [fluid type](https://css-tricks.com/snippets/css/fluid-typography/) / [dynamic typography](https://rwt.io/typography-tips/digging-dynamic-typography)… a calculated `font-size` based on minimums, maxiums, and a rate of change from viewport units. Not just the `font-size`, but `line-height` too.

If you’re using `calc()` as part of a fluid type situation that involves viewport units and such, make sure that you include a unit that uses `rem` or `em` so that the user still has some control over bumping that font up or down by zooming in or out as they need to.

> One I really like is having a “content width” custom property and then using that to create the spacing that I need, like margins: `.margin { width: calc( (100vw - var(--content-width)) / 2); }`

> I used it to create a cross-browser drop-cap component. Here’s a part of it:  
>   
> `.drop-cap { --drop-cap-lines: 3; font-size: calc(1em * var(--drop-cap-lines) * var(--body-line-height)); }`

> I used it to make some images overflow their container on an article page.

> I used it to place a visualization correctly on the page by combining it with padding and `vw`/`vh` units.

> I use it to overcome limitations in `background-position`, but expecially limitations in positioning color stops in gradients. Like “stop `0.75em` short of the bottom”.

### Other trickery

- [A two-up grid that breaks into a single column](https://css-tricks.com/using-calc-to-fake-a-media-query/) with no media query
- An [aspect-ratio-ish hero component](https://css-tricks.com/fun-tip-use-calc-to-change-the-height-of-a-hero-component/)
- Enforcing [high-contrast colors](https://css-tricks.com/css-variables-calc-rgb-enforcing-high-contrast-colors/)
- [Help with the coordinates](https://css-tricks.com/notched-boxes/) of a percentage-based `clip-path`