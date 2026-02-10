# CSS Custom Properties Guide | CSS-Tricks

Source: https://css-tricks.com/a-complete-guide-to-custom-properties/

---

A custom property is most commonly thought of as a **variable** in CSS.

```
.card {
  --spacing: 1.2rem;
  padding: var(--spacing);
  margin-bottom: var(--spacing);
}
```

Above, `--spacing` is the custom property with `1.2rem` as the value and `var(--spacing)` is the variable in use.

Perhaps the most valuable reason to use them: not repeating yourself (DRY code). In the example above, I can change the **value** `1.2rem` in *one* place and have it affect *two* things. This brings something programming languages do to CSS.

There is a good bit to know about custom properties, so let’s get into it.

## Why care about CSS Custom Properties?

1. They help DRY up your CSS. That is “Don’t Repeat Yourself.” Custom properties can make code easier to maintain because you can update one value and have it reflected in multiple places. Careful though, overdoing abstraction can make have the opposite effect and make code less understandable.
2. They are particularly helpful for things like creating **color themes** on a website.
3. They unlock interesting possibilities in CSS. In no small part because they cascade.
4. The fact that they can be updated in JavaScript opens up even more interesting possibilities.

### Table of contents

- [Why care about CSS Custom Properties?](#h-why-care-about-css-custom-properties)
  - [Naming custom properties](#h-naming-custom-properties)
    - [Properties as properties](#h-properties-as-properties)
  - [Valid values for custom properties](#h-valid-values-for-custom-properties)
  - [Breaking up values](#h-breaking-up-values)
    - [Splitting colors](#h-splitting-colors)
    - [Shadows](#h-shadows)
    - [Gradients](#h-gradients)
    - [Comma-separated values (like backgrounds)](#h-comma-separated-values-like-backgrounds)
    - [Grids](#h-grids)
    - [Transforms](#h-transforms)
    - [Concatenation of unit types](#h-concatenation-of-unit-types)
  - [Using the cascade](#h-using-the-cascade)
    - [The :root thing](#h-the-root-thing)
  - [Combining with !important](#h-combining-with-important)
  - [Custom property fallbacks](#h-custom-property-fallbacks)
  - [Using calc() and custom properties](#h-using-calc-and-custom-properties)
    - [Deferring the calc()](#h-deferring-the-calc)
  - [@property](#h-property)
  - [Commas in values](#h-commas-in-values)
  - [Advanced usage](#h-advanced-usage)
    - [The initial and whitespace trick](#h-the-initial-and-whitespace-trick)
    - [Inline styles](#h-inline-styles)
    - [Hovers and pseudos](#h-hovers-and-pseudos)
  - [Custom properties and JavaScript](#h-custom-properties-and-javascript)
  - [Custom properties are different than preprocessor variables](#h-custom-properties-are-different-than-preprocessor-variables)
    - [Can you preprocess custom properties?](#h-can-you-preprocess-custom-properties)
    - [Availiability](#h-availiability)
  - [Custom properties and Web Components (Shadow DOM)](#h-custom-properties-and-web-components-shadow-dom)
  - [Browser support](#h-browser-support)
    - [@supports](#h-supports)
  - [Related posts](#h-related-posts)
  - [Credit](#h-credit)

### Naming custom properties

Custom properties *must* be within a selector and start with two dashes (`--`):

```
/* Nope, not within a selector */
--foo: 1;

body {
  /* No, 0 or 1 dash won't work */
  foo: 1;
  -foo: 1; 

  /* Yep! */
  --foo: 1;

  /* OK, but they're different properties */
  --FOO: 1;
  --Foo: 1;
  
  /* Totally fine */
  --mainColor: red;
  --main-color: red;

  /* Special characters are a no */
  --color@home: red;
  --black&blue: black;
  --black^2: black;
}
```

Best to stick with letters, numbers, and dashes while making sure the custom property is defined inside of a valid selector.

#### Properties as properties

You can set the value of a custom property with another custom property:

```
html {
  --red: #a24e34;
  --green: #01f3e6;
  --yellow: #f0e765;

  --error: var(--red);
  --errorBorder: 1px dashed var(--red);
  --ok: var(--green);
  --warning: var(--yellow);
}
```

Some people like doing it this way because it allows the name of a custom property to be descriptive and then used in another property with a more functional name, again helping keep things DRY. It can even help make the functional names more readable and understandable.

[There is a big gotcha](https://css-tricks.com/the-big-gotcha-with-custom-properties/) with custom properties that use other custom properties you should be aware of.

### Valid values for custom properties

![](https://css-tricks.com/wp-content/uploads/2021/04/lightbulb-icon-happy.svg)

Custom properties are surprisingly tolerant when it comes to the values they accept.

Here are some basic examples that you’d expect to work, and do.

```
body {
  --brand-color: #990000;
  --transparent-black: rgba(0, 0, 0, 0.5);
  
  --spacing: 0.66rem;
  --max-reading-length: 70ch;
  --brandAngle: 22deg;

  --visibility: hidden;
  --my-name: "Chris Coyier";
}
```

See that? They can be hex values, color functions, units of all kinds, and even strings of text.

[custom properties](https://css-tricks.com/tag/custom-properties/)

**Article**
on
Oct 9, 2019 

### [Patterns for Practical CSS Custom Properties Use](https://css-tricks.com/patterns-for-practical-css-custom-properties-use/)

[![](https://i0.wp.com/css-tricks.com/wp-content/cache/breeze-extra/gravatars/tyler-80x80.jpg?resize=80%2C80&ssl=1)](https://css-tricks.com/author/tylerchilds/) 
[Tyler Childs](https://css-tricks.com/author/tylerchilds/)

[css variables](https://css-tricks.com/tag/css-variables/) [custom properties](https://css-tricks.com/tag/custom-properties/)

**Link**
on
May 16, 2018 

### [A Strategy Guide To CSS Custom Properties](https://css-tricks.com/a-strategy-guide-to-css-custom-properties/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

**Link**
on
Sep 1, 2014 

### [Advantages to Native CSS Variables](https://css-tricks.com/advantages-native-css-variables/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

[custom properties](https://css-tricks.com/tag/custom-properties/) [state](https://css-tricks.com/tag/state/)

**Article**
on
Jan 5, 2021 

### [Custom Properties as State](https://css-tricks.com/custom-properties-as-state/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

But custom properties don’t have to be complete values like that. Let’s look at how useful it can be to break up valid CSS values into parts we can shove into custom properties.

### Breaking up values

![](https://css-tricks.com/wp-content/uploads/2021/04/lightbulb-icon-happy.svg)

You can use custom properties to break up multi-part values.

Let’s imagine you’re using a color function, say `rgba()`. Each color channel value in there can be its own custom property. That opens up a ton of possibilities, like changing the alpha value for a specific use case, or perhaps creating color themes.

#### Splitting colors

Take HSL color, for example. We can split it up into parts, then very easily adjust the parts where we want. Maybe we’re working with the background color of a button. We can update specific parts of its HSL makeup when the button is hovered, in focus, or disabled, without declaring `background` on any of those states at all.

```
button {
  --h: 100;
  --s: 50%;
  --l: 50%;
  --a: 1;

  background: hsl(var(--h) var(--s) var(--l) / var(--a));
}
button:hover { /* Change the lightness on hover */
  --l: 75%;
}
button:focus { /* Change the saturation on focus */
  --s: 75%;
}
button[disabled] {  /* Make look disabled */
  --s: 0%;
  --a: 0.5;
}
```

By breaking apart values like that, we can [control *parts* of them](https://css-tricks.com/now-css-custom-properties-thing-value-parts-can-changed-individually/) in a way we never could before. Just look at how we didn’t need to declare all of the HSL arguments to style the hover, focus and disabled state of a button. We simply overrode specific HSL values when we needed to. Pretty cool stuff!

#### Shadows

`box-shadow` doesn’t have a shorthand property for controlling the shadow’s spread on its own. But we could break out the `box-shadow` spread value and control it as a custom property ([demo](https://codepen.io/team/css-tricks/pen/PoWdVOw)).

```
button {
  --spread: 5px;
  box-shadow: 0 0 20px var(--spread) black;
}
button:hover {
  --spread: 10px;
}
```

#### Gradients

There is no such thing as a `background-gradient-angle` (or the like) shorthand for gradients. With custom properties, we can change just change that part as if there was such a thing.

```
body {
  --angle: 180deg;
  background: linear-gradient(var(--angle), red, blue);
}
body.sideways {
  --angle: 90deg;
}
```

#### Comma-separated values (like backgrounds)

Any property that supports multiple comma-separated values might be a good candidate for splitting values too, since there is no such thing as targeting just one value of a comma-separated list and changing it alone.

```
/* Lots of backgrounds! */
background-image:
  url(./img/angles-top-left.svg),
  url(./img/angles-top-right.svg),
  url(./img/angles-bottom-right.svg),
  url(./img/angles-bottom-left.svg),
  url(./img/bonus-background.svg);
```

Say you wanted to remove [just one of many multiple backgrounds](https://css-tricks.com/managing-multiple-backgrounds-with-custom-properties/) at a media query. You could do that with custom properties like this, making it a trivial task to swap or override backgrounds.

```
body {
  --bg1: url(./img/angles-top-left.svg);
  --bg2: url(./img/angles-top-right.svg);
  --bg3: url(./img/angles-bottom-right.svg);
  --bg4: url(./img/angles-bottom-left.svg);
  --bg5: url(./img/bonus-background.svg);
  
  background-image: var(--bg1), var(--bg2), var(--bg3), var(--bg4);
}
@media (min-width: 1500px) {
  body {
    background-image: var(--bg1), var(--bg2), var(--bg3), var(--bg4), var(--bg5);
  }
}
```

#### Grids

We’re on a roll here, so we might as well do a few more examples. Like, hey, we can take the `grid-template-columns` property and abstract its values into custom properties to make a super flexible grid system:

```
.grid {
  display: grid;
  --edge: 10px;
  grid-template-columns: var(--edge) 1fr var(--edge);
}
@media (min-width: 1000px) {
  .grid {
     --edge: 15%;
   }
}
```

#### Transforms

CSS will soon get [individual transforms](https://drafts.csswg.org/css-transforms-2/#individual-transforms) but we can get it sooner with custom properties. The idea is to apply all the transforms an element might get up front, then control them individually as needed:

```
button {
  transform: var(--scale, scale(1)) var(--translate, translate(0));
}
button:active {
  --translate: translate(0, 2px);
}
button:hover {
  --scale: scale(0.9);
}
```

#### Concatenation of unit types

There are times when combining parts of values doesn’t work quite how you might hope. For example, you can’t make `24px` by smashing `24` and `px` together. It can be done though, by *multiplying* the raw number by a number value with a unit.

```
body {
  --value: 24;
  --unit: px;
  
  /* Nope */
  font-size: var(--value) + var(--unit);
  
  /* Yep */
  font-size: calc(var(--value) * 1px);

  /* Yep */
  --pixel_converter: 1px;
  font-size: calc(var(--value) * var(--pixel_converter));
}
```

[custom properties](https://css-tricks.com/tag/custom-properties/)

**Article**
on
Aug 14, 2019 

### [Contextual Utility Classes for Color with Custom Properties](https://css-tricks.com/contextual-utility-classes-for-color-with-custom-properties/)

[![](https://i0.wp.com/css-tricks.com/wp-content/cache/breeze-extra/gravatars/pp-80x80.jpg?resize=80%2C80&ssl=1)](https://css-tricks.com/author/chriskirknielsen/) 
[Christopher Kirk-Nielsen](https://css-tricks.com/author/chriskirknielsen/)

[calc](https://css-tricks.com/tag/calc/) [css variables](https://css-tricks.com/tag/css-variables/) [custom properties](https://css-tricks.com/tag/custom-properties/)

**Article**
on
May 10, 2017 

### [Making Custom Properties (CSS Variables) More Dynamic](https://css-tricks.com/making-custom-properties-css-variables-dynamic/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/a67045612bf576547f970b04448f13c1f3d7c7299fea8bd5d54b28cb0afcb7c0)](https://css-tricks.com/author/dancwilson/) 
[Dan Wilson](https://css-tricks.com/author/dancwilson/)

**Article**
on
Aug 11, 2017 

### [More CSS Charts, with Grid & Custom Properties](https://css-tricks.com/css-charts-grid-custom-properties/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/ae0467bce26cf281ae92243a6000639eb4efaed23b953798bf4bdf7cdb1f3778)](https://css-tricks.com/author/miriam/) 
[Miriam Suzanne](https://css-tricks.com/author/miriam/)

[calc](https://css-tricks.com/tag/calc/) [css variables](https://css-tricks.com/tag/css-variables/) [responsive](https://css-tricks.com/tag/responsive/)

**Article**
on
Feb 25, 2019 

### [Responsive Designs and CSS Custom Properties: Defining Variables and Breakpoints](https://css-tricks.com/responsive-designs-and-css-custom-properties-defining-variables-and-breakpoints/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/2c333cae8e6a602109f0f8ae44c2a38ab8b05de3042f47859e3628c55d92e565)](https://css-tricks.com/author/mikolajdobrucki/) 
[Mikolaj Dobrucki](https://css-tricks.com/author/mikolajdobrucki/)

[css animation](https://css-tricks.com/tag/css-animation/) [gradients](https://css-tricks.com/tag/gradients/) [keyframes](https://css-tricks.com/tag/keyframes/) [transition](https://css-tricks.com/tag/transition/)

**Article**
on
Jun 1, 2018 

### [The State of Changing Gradients with CSS Transitions and Animations](https://css-tricks.com/the-state-of-changing-gradients-with-css-transitions-and-animations/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/3a2e2f1da40ff7880e4ab0efbf2082f5deffc43b8e7a5f2ed42f4c386a8fd932)](https://css-tricks.com/author/thebabydino/) 
[Ana Tudor](https://css-tricks.com/author/thebabydino/)

[dark](https://css-tricks.com/tag/dark/) [variable fonts](https://css-tricks.com/tag/variable-fonts/)

**Article**
on
Dec 10, 2020 

### [Using CSS Custom Properties to Adjust Variable Font Weights in Dark Mode](https://css-tricks.com/using-css-custom-properties-to-adjust-variable-font-weights-in-dark-mode/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/1e269e5dfba188eaa262c057e15c0bdcb45515386e775e7f67f09498f3908216)](https://css-tricks.com/author/greg-gibson/) 
[Greg Gibson](https://css-tricks.com/author/greg-gibson/)

### Using the cascade

![](https://css-tricks.com/wp-content/uploads/2021/04/lightbulb-icon-happy.svg)

The fact that custom properties use [the cascade](https://css-tricks.com/the-c-in-css-the-cascade/) is one of the most useful things about them.

You’ve already seen it in action in many of the examples we’ve covered, but let’s put a point on it. Say we have a custom property set pretty “high up” (on the body), and then set again on a specific class. We use it on a specific component.

```
body {
  --background: white;
}
.sidebar {
  --background: gray;
}
.module {
  background: var(--background);
}
```

Then say we’ve got practical HTML like this:

```
<body> <!-- --background: white -->

  <main>
    <div class="module">
      I will have a white background.
    </div>
  <main>

  <aside class="sidebar"> <!-- --background: gray -->
    <div class="module">
      I will have a gray background.
    </div>
  </aside>

</body>
```

![Three CSS rulesets, one for a body, sidebar and module. the background custom property is defined as white on body and gray on sidebar. The module calls the custom property and shows an orange arrow pointing to the custom property defined in the sidebar since it is the nearest ancestor.](https://i0.wp.com/css-tricks.com/wp-content/uploads/2021/04/custom-property-cascade-inherit.jpg?resize=1245%2C741&ssl=1)

For the second module, `.sidebar` is a closer ancestor than `body`, thus `--background` resolves to `gray` there, but white in other places.

The “module” in the sidebar has a gray background because custom properties (like many other CSS properties) **inherit** through the HTML structure. Each module takes the `--background` value from the nearest “ancestor” where it’s been defined in CSS.

So, we have *one* CSS declaration but it’s doing different things in different contexts, thanks to the cascade. That’s just cool.

This plays out in other ways:

```
button {
  --foo: Default;
}
button:hover {
  --foo: I win, when hovered;
  /* This is a more specific selector, so re-setting 
     custom properties here will override those in `button` */
}
```

Media queries don’t change specificity, but they often come *later* (or lower) in the CSS file than where the original selector sets a value, which also means a custom property will be overridden inside the media query:

```
body {
  --size: 16px;
  font-size: var(--size);
}
@media (max-width: 600px) {
  body {
    --size: 14px;
  } 
}
```

[Media queries](https://css-tricks.com/a-complete-guide-to-css-media-queries/) aren’t only for screen sizes. They can be used for things like accessibility preferences. For example, [dark mode](https://css-tricks.com/a-complete-guide-to-dark-mode-on-the-web/):

```
body {
  --bg-color: white; 
  --text-color: black;

  background-color: var(--bg-color);
  color: var(--text-color);
}

/* If the user's preferred color scheme is dark */
@media screen and (prefers-color-scheme: dark) {
  body {
    --bg-color: black;
    --text-color: white;
  }
}
```

#### The `:root` thing

You’ll often see custom properties being set “at the root.” Here’s what that means:

```
:root {
  --color: red;
}

/* ...is largely the same as writing: */
html {
  --color: red;
}

/* ...except :root has higher specificity, so remember that! */
```

There is no particularly compelling reason to define custom properties like that. It’s just a way of setting custom properties *as high up as they can go*. If you like that, that’s totally fine. I find it somehow more normal-feeling to apply them to the `html` or `body` selectors when setting properties I intend to make available globally, or everywhere.

There is also no reason you *need* to set variables at this broad of a scope. It can be just as useful, and perhaps more readable and understandable, to set them right at the level you are going to use them (or fairly close in the DOM tree).

```
.module {
  --module-spacing: 1rem;
  --module-border-width: 2px;

  border: var(--module-border-width) solid black;
}

.module + .module {
  margin-top: var(--module-spacing);
}
```

Note that setting a custom property on the module itself means that property will no longer inherit from an ancestor (unless we set the value to `inherit`). Like other inherited properties, there are sometimes reasons to specify them in place (at the global level), and other times we want to inherit them from context (at the component level). Both are useful. What’s cool about custom properties is that we can define them in one place, inherit them *behind the scenes*and apply them **somewhere completely different**. We take control of the cascade!

[css variables](https://css-tricks.com/tag/css-variables/) [custom properties](https://css-tricks.com/tag/custom-properties/)

**Link**
on
May 16, 2018 

### [A Strategy Guide To CSS Custom Properties](https://css-tricks.com/a-strategy-guide-to-css-custom-properties/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

[custom properties](https://css-tricks.com/tag/custom-properties/) [global scope](https://css-tricks.com/tag/global-scope/) [themes](https://css-tricks.com/tag/themes/)

**Link**
on
Jun 30, 2020 

### [Global and Component Style Settings with CSS Variables](https://css-tricks.com/global-and-component-style-settings-with-css-variables/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

[css variables](https://css-tricks.com/tag/css-variables/) [custom properties](https://css-tricks.com/tag/custom-properties/)

**Article**
on
Mar 27, 2019 

### [Breaking CSS Custom Properties out of :root Might Be a Good Idea](https://css-tricks.com/breaking-css-custom-properties-out-of-root-might-be-a-good-idea/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/74a367d66afe7156f03614b6844f16fee23078fd5a5c90cd1d552baae04b6646)](https://css-tricks.com/author/kevinpowell/) 
[Kevin Powell](https://css-tricks.com/author/kevinpowell/)

### Combining with `!important`

![](https://css-tricks.com/wp-content/uploads/2021/04/lightbulb-icon-happy.svg)

You can make an `!important` modifier within or outside of a variable.

```
.override-red {
  /* this works */
  --color: red !important;  
  color: var(--color);

  /* this works, too */
  --border: red;
  border: 1px solid var(--border) !important;
}
```

Applying `!important` to the `--color` variable, makes it difficult to override the value of the `--color` variable, but we can still ignore it by changing the `color` property.

The behavior of `!important` inside the values of custom properties is quite unusual. [Stefan Judis documents it well](https://www.stefanjudis.com/today-i-learned/the-surprising-behavior-of-important-css-custom-properties/), but the gist is:

1. Ultimately, `!important` is stripped from the value of the custom property.
2. But it is used when determining which value wins when it is set in multiple places.

```
div {
  --color: red !important;
}
#id {
  --color: yellow;
}
```

If both of those selectors apply to an element, you might think the `#id` value would win because of the higher specificity, but really `red` will win because of the `!important`, but then ultimately be applied without the `!important`. It’s a little funky to wrap your head around.

If applying the `!important` *outside* of the custom property, like the 2nd example two code blocks up, our `--border` variable remains low-specificity (easy to override), but it’s hard to change how that value will be applied to the `border` itself because the entire declaration retains `!important`.

### Custom property fallbacks

![](https://css-tricks.com/wp-content/uploads/2021/04/lightbulb-icon-happy.svg)

The `var()` function is what allows for fallback values in custom properties.

Here we’re setting a `scale()` transform function to a custom property, but there is a **comma-separated** second value of `1.2`. That `1.2` value will be used if `--scale` is not set.

```
.bigger {
  transform: scale(var(--scale, 1.2));
}
```

After the first comma, any additional commas are part of the fallback value. That allows us to create fallbacks with comma-separated values inside them. For example, we can have one variable fall back to an entire stack of fonts:

```
html {
  font-family: var(--fonts, Helvetica, Arial, sans-serif);
}
```

We can also provide a series of variable fallbacks (as many as we want), but we have to nest them for that to work:

```
.bigger {
  transform: scale(var(--scale, var(--second-fallback, 1.2));
}
```

If `--scale` is undefined, we try the `--second-fallback`. If that is also undefined, we finally fall back to `1.2`.

### Using `calc()` and custom properties

![](https://css-tricks.com/wp-content/uploads/2021/04/lightbulb-icon-happy.svg)

Even more power of custom properties is unlocked when we combine them with math!

This kind of thing is common:

```
main {
  --spacing: 2rem;
}

.module {
  padding: var(--spacing);
}

.module.tight {
  /* divide the amount of spacing in half */
  padding: calc(var(--spacing) / 2)); 
}
```

We could also use that to calculate the hue of a complementary color:

```
html {
  --brand-hue: 320deg;
  --brand-color: hsl(var(--brand-hue), 50%, 50%);
  --complement: hsl(calc(var(--brand-hue) + 180deg), 50%, 50%);
}
```

`calc()` can even be used with multiple custom properties:

```
.slider {
  width: calc(var(--number-of-boxes) * var(--width-of-box));
}
```

#### Deferring the `calc()`

It might look weird to see calculous-like math without a `calc()`:

```
body {
  /* Valid, but the math isn't actually performed just yet ... */
  --font-size: var(--base-font-size) * var(--modifier);

  /* ... so this isn't going to work */
  font-size: var(--font-size);
}
```

The trick is that as long as you eventually put it in a `calc()` function, it works fine:

```
body {
  --base-font-size: 16px;
  --modifier: 2;
  --font-size: var(--base-font-size) * var(--modifier);

  /* The calc() is "deferred" down to here, which works */
  font-size: calc(var(--font-size));
}
```

This might be useful if you’re doing quite a bit of math on your variables, and the `calc()` wrapper becomes distracting or noisy in the code.

### @property

![](https://css-tricks.com/wp-content/uploads/2021/04/lightbulb-icon-happy.svg)

The `@property` “at-rule” in CSS allows you to declare the type of a custom property, as well its as initial value and whether it inherits or not.

It’s sort of like you’re creating an actual CSS property and have the ability to define what it’s called, it’s syntax, how it interacts with the cascade, and its initial value.

```
@property --x {
  syntax: '<number>';
  inherits: false;
  initial-value: 42;
}
```

Valid Types 

- `length`
- `number`
- `percentage`
- `length-percentage`
- `color`
- `image`
- `url`
- `integer`
- `angle`
- `time`
- `resolution`
- `transform-list`
- `transform-function`
- `custom-ident` (a custom identifier string)

This means that the browser knows what kind of value it is dealing with, rather than assuming everything is a string. That means you can animate things in ways you couldn’t otherwise.

For example, say you have a star-shaped icon that you want to spin around with `@keyframes` and rotate with a `transform`. So you do this:

```
.star {
  --r: 0deg;
  transform: rotate(var(--r));
  animation: spin 1s linear infinite;
}

@keyframes spin {
  100% {
    --r: 360deg;
  }
}
```

That actually won’t work, as the browser doesn’t know that `0deg` and `360deg` are valid angle values. You have to define them as an `<angle>` type with `@property` for that to work.

```
@property --r {
  syntax: '<angle>';
  initial-value: 0deg;
  inherits: false;
}

.star {
  --r: 0deg;
  transform: rotate(var(--r));
  animation: spin 1s linear infinite;
}

@keyframes spin {
  100% {
    --r: 360deg;
  }
}
```

Demo 

[@property](https://css-tricks.com/tag/property/) [custom properties](https://css-tricks.com/tag/custom-properties/)

**Article**
on
Apr 25, 2020 

### [@property](https://css-tricks.com/property/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

[@property](https://css-tricks.com/tag/property/) [custom properties](https://css-tricks.com/tag/custom-properties/)

**Article**
on
Sep 2, 2020 

### [Using @property for CSS Custom Properties](https://css-tricks.com/using-property-for-css-custom-properties/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

[@property](https://css-tricks.com/tag/property/) [css animation](https://css-tricks.com/tag/css-animation/) [custom properties](https://css-tricks.com/tag/custom-properties/)

**Article**
on
Mar 4, 2021 

### [Exploring @property and its Animating Powers](https://css-tricks.com/exploring-property-and-its-animating-powers/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/88f05a8f8ee43ecf0e6752ed506b28f9ba34e86e3e0d887fba2c4c596a2c9531)](https://css-tricks.com/author/jheytompkins/) 
[Jhey Tompkins](https://css-tricks.com/author/jheytompkins/)

**Article**
on
Mar 8, 2021 

### [241: The @property is magic](https://css-tricks.com/newsletter/241-the-property-is-magic/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/a8e040142716a4b44d014d80fbcf99c635b1d8faabfe469b6954a8ef2f168595)](https://css-tricks.com/author/geoffgraham/) 
[Geoff Graham](https://css-tricks.com/author/geoffgraham/)

### Commas in values

This can be a smidge confusing. Maybe not so much this:

```
html {
  --list: 1, 2, 3;
}
```

But below, you’ll need a sharp eye to realize the fallback value is actually `1.2, 2`. The first comma separates the fallback, but all the rest is part of the value.

```
html {
  transform: scale(var(--scale, 1.2, 2));
}
```

[Learn more about fallbacks above ⮑](#h-custom-property-fallbacks)

### Advanced usage

![](https://css-tricks.com/wp-content/uploads/2021/04/lightbulb-icon-happy.svg)

[The Raven](https://css-tricks.com/the-raven-technique-one-step-closer-to-container-queries/) is a technique that emulates container queries using math and custom properties. Be prepared, this goes from 0-100 in complexity right out of the gate!

Demo 

Resize this demo to see a grid of inline-block elements change number of columns from 4 to 3 to 1.

Here’s a few more favorite examples that show off advanced usage of custom properties:

[css animation](https://css-tricks.com/tag/css-animation/) [custom properties](https://css-tricks.com/tag/custom-properties/)

**Article**
on
Sep 12, 2019 

### [Using Custom Properties to Wrangle Variations in Keyframe Animations](https://css-tricks.com/using-custom-properties-to-wrangle-variations-in-keyframe-animations/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/741487c88e0ca546f3bb24cb907636de2d6e64219edecef0727a7abd5377c494)](https://css-tricks.com/author/sandrinapereira/) 
[Sandrina Pereira](https://css-tricks.com/author/sandrinapereira/)

[css variables](https://css-tricks.com/tag/css-variables/) [custom properties](https://css-tricks.com/tag/custom-properties/)

**Article**
on
Nov 27, 2019 

### [The Power (and Fun) of Scope with CSS Custom Properties](https://css-tricks.com/the-power-and-fun-of-scope-with-css-custom-properties/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/88f05a8f8ee43ecf0e6752ed506b28f9ba34e86e3e0d887fba2c4c596a2c9531)](https://css-tricks.com/author/jheytompkins/) 
[Jhey Tompkins](https://css-tricks.com/author/jheytompkins/)

[animation](https://css-tricks.com/tag/animation/) [custom properties](https://css-tricks.com/tag/custom-properties/) [details/summary](https://css-tricks.com/tag/details-summary/) [IntersectionObserver](https://css-tricks.com/tag/intersectionobserver/) [keyframes](https://css-tricks.com/tag/keyframes/)

**Article**
on
Jan 21, 2021 

### [How to Play and Pause CSS Animations with CSS Custom Properties](https://css-tricks.com/how-to-play-and-pause-css-animations-with-css-custom-properties/)

[![](https://i0.wp.com/css-tricks.com/wp-content/cache/breeze-extra/gravatars/xfKShH2E_400x400-80x80.jpg?resize=80%2C80&ssl=1)](https://css-tricks.com/author/madsstoumann/) 
[Mads Stoumann](https://css-tricks.com/author/madsstoumann/)

[custom properties](https://css-tricks.com/tag/custom-properties/)

**Link**
on
Aug 4, 2020 

### [The Cicada Principle, revisited with CSS variables](https://css-tricks.com/the-cicada-principle-revisited-with-css-variables/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

#### The `initial` and whitespace trick

Think of `@media` queries and how when **one** thing changes (e.g. the width of the page) you can control **multiple** things. That’s kind of the idea with this trick. You change **one** custom property and control **multiple** things.

The trick is that the value of `initial` for a custom property will trigger a fallback, while an empty whitespace value will not. For the sake of explanation, it let’s define two globally-scoped custom properties, `ON` and `OFF`:

```
:root {
  --ON: initial;
  --OFF: ;
}
```

Say we have a “dark” variation class which sets a number of different properties. The default is `--OFF`, but can be flipped to `--ON` whenever:

```
.module {
  --dark: var(--OFF);
}

.dark { /* could be a media query or whatever */
  --dark: var(--ON);
}
```

Now you can use `--dark` to conditinally set values that apply only when you’ve flipped `--dark` to `--ON`. Demo:

[Lea Verou has a great writeup](https://lea.verou.me/2020/10/the-var-space-hack-to-toggle-multiple-values-with-one-custom-property/?) that covers all of this.

#### Inline styles

It’s totally legit to set a custom property in HTML with an inline style.

```
<div style="--color: red;"></div>
```

That will, like any inline style, have a very high level of specificity.

This can be super useful for when the HTML might have access to some useful styling information that would be too weird/difficult to put into a static CSS file. A good example of that is maintaining the aspect ratio of an element:

```
<div style="--aspect-ratio: 16 / 9;"></div>
```

Now I can set up some CSS to make a box of that exact size wherever I need to. [The full writeup on that is here](https://css-tricks.com/aspect-ratio-boxes/#using-custom-properties), but here’s CSS that uses trickery like the [ol’ padded box](https://daverupert.com/2012/04/uncle-daves-ol-padded-box/) applied to a pseudo element which pushes the box to the desired size:

```
[style*="--aspect-ratio"] > :first-child {
  width: 100%;
}
[style*="--aspect-ratio"] > img {  
  height: auto;
} 
@supports (--custom: property) {
  [style*="--aspect-ratio"] {
    position: relative;
  }
  [style*="--aspect-ratio"]::before {
    content: "";
    display: block;
    padding-bottom: calc(100% / (var(--aspect-ratio)));
  }  
  [style*="--aspect-ratio"] > :first-child {
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
  }  
}
```

But hey, these days, we have a native `aspect-ratio` property in CSS, so setting that in the inline style might make more sense going forward.

```
<div style="aspect-ratio: 16 / 9;"></div>
```

#### Hovers and pseudos

There is no way to apply a `:hover` style (or other pseudo classes/elements) with inline styles. That is, [unless we get tricky with custom properties](https://css-tricks.com/want-to-write-a-hover-effect-with-inline-css-use-css-variables/). Say we want custom hover colors on some boxes — we can pass that information in as a custom property:

```
<div style="--hover-color: red;"><div>
<div style="--hover-color: blue;"><div>
<div style="--hover-color: yellow;"><div>
```

Then use it in CSS which, of course, can style a link’s hover state:

```
div:hover {
  background-color: var(--hover-color);
}

/* And use in other pseudos! */
div:hover::after {
  content: "I am " attr(style);
  border-color: var(--hover-color);
}
```

### Custom properties and JavaScript

![](https://css-tricks.com/wp-content/uploads/2021/04/lightbulb-icon-happy.svg)

JavaScript can set the value of a custom property.

```
element.style.setProperty('--x', value);
```

Here’s an example of a red square that is positioned with custom properties, and JavaScript updates those custom property values with the mouse position:

Typically you think of JavaScript passing values to CSS to use, which is probably 99% of usage here, but note that you can pass things from CSS to JavaScript as well. [As we’ve seen](#valid-values-for-custom-properties), the value of a custom property can be fairly permissive. That means you could pass it a logical statement. For example:

```
html {
  --logic: if (x > 5) document.body.style.background = "blue";
}
```

Then grab that value and execute it in JavaScript:

```
const x = 10;

const logic = getComputedStyle(document.documentElement).getPropertyValue(
  "--logic"
);

eval(logic);
```

### Custom properties are different than preprocessor variables

![](https://css-tricks.com/wp-content/uploads/2021/04/lightbulb-icon-happy.svg)

Say you’re already using Sass, Less, or Stylus. All those CSS preprocessors offer variables and it’s one of the main reasons to have them as part of your build process.

```
// Variable usage in Sass (SCSS)
$brandColor: red;

.marketing {
  color: $brandColor;
}
```

So, **do you even need to bother with native CSS custom properties then?** Yes, you should. Here’s why in a nutshell:

- **Native CSS custom properties are more powerful then preprocessor variables.** Their integration with the **cascade** in the DOM is something that preprocessor variables will never be able to do.
- **Native CSS custom properties are dynamic.** When they change (perhaps via JavaScript, or with a media query), the browser repaints what it needs to. Preprocessor variables resolve to a value when they’re compiled and stay at that value.
- **Going with a native feature is good for the longevity of your code.** You don’t need to preprocess native CSS.

I cover this in much more detail in the article [“What is the difference between CSS variables and preprocessor variables?”](https://css-tricks.com/difference-between-types-of-css-variables/)

To be totally fair, there are little things that preprocessor variables can do that are hard or impossible with custom properties. Say you wanted to strip the units off a value for example. [You can do that in Sass](https://css-tricks.com/snippets/sass/strip-unit-function/) but you’ll have a much harder time with custom properties in CSS alone.

#### Can you preprocess custom properties?

Kinda. You can do this, with Sass just to pick one popular preprocessor:

```
$brandColor: red;
body {
--brandColor: #{$brandColor};
}
```

All that’s doing is moving a Sass variable to a custom property. That could be useful sometimes, but not terribly. Sass will just make `--brandColor: red;` there, not process the custom property away.

If a browser doesn’t support custom properties, that’s that. You can’t *force* a browser to do what custom properties do by CSS syntax transformations alone. There might be some kind of JavaScript polyfill that parses your CSS and replicates it, but I really don’t suggest that.

The [PostCSS Custom Properties](https://github.com/postcss/postcss-custom-properties) plugin, though, does do CSS syntax transforms to help. What it does is figure out the value to the best of it’s ability, and outputs that along with the custom property. So like:

```
:root {
  --brandColor: red;
}
body {
  color: var(--brandColor);
}
```

Will output like this:

```
:root {
  --brandColor: red;
}
body {
  color: red;
  color: var(--brandColor);
}
```

That means you get a value that hopefully doesn’t seem broken in browsers that lack custom property support, but does not support any of the fancy things you can do with custom properties and will not even attempt to try. I’m a bit dubious about how useful that is, but I think this is about the best you can do and I like the spirit of attempting to not break things in older browsers *or* newer browsers.

#### Availiability

Another thing that is worth noting about the difference between is that with a CSS preprocessor, the variables are available *only* as you’re processing. Something like `$brandColor` is meaningless in your HTML or JavaScript. But when you have custom properties in use, you can set inline styles that use those custom properties and they will work. Or you can use JavaScript to figure out their current values (in context), if needed.

Aside from some somewhat esoteric features of preprocessor variables (e.g. some math possibilities), custom properties are more capable and useful.

### Custom properties and Web Components (Shadow DOM)

![](https://css-tricks.com/wp-content/uploads/2021/04/lightbulb-icon-happy.svg)

One of the most common and practical ways to style of Web Components (e.g. a `<custom-component>` with shadow DOM) is by using custom properties as styling hooks.

The main point of the shadow DOM is that it doesn’t “leak” styles in or out of it, offering style isolation in a way that nothing else offers, short of an `<iframe>`. Styles do still *cascade* their way inside, I just can’t select my way inside. This means custom properties will slide right in there.

Here’s an example:

Another common occurrence of the shadow DOM is with SVG and the `<use>` element.

Video: [“CSS Custom Properties Penetrate the Shadow DOM”](https://css-tricks.com/video-screencasts/190-css-custom-properties-penetrate-the-shadow-dom/)

### Browser support

This browser support data is from [Caniuse](http://caniuse.com/#feat=css-variables), which has more detail. A number indicates that browser supports the feature at that version and up.

#### Desktop

| Chrome | Firefox | IE | Edge | Safari |
| --- | --- | --- | --- | --- |
| 49 | 31 | No | 16 | 10 |

#### Mobile / Tablet

| Android Chrome | Android Firefox | Android | iOS Safari |
| --- | --- | --- | --- |
| 144 | 147 | 144 | 10.0-10.2 |

You can [preprocess for deeper browser support](#h-can-you-preprocess-custom-properties), with heavy limitations.

#### @supports

If you would like to write conditional CSS for when a browser supports custom properties or not:

```
@supports (--custom: property) {
  /* Isolated CSS for browsers that DOES support custom properties, assuming it DOES support @supports */
}

@supports not (--custom: property) {
  /* Isolated CSS for browsers that DON'T support custom properties, assuming it DOES support @supports */
}
```

### Related posts

**Article**
on
Mar 17, 2011 

### [currentcolor](https://css-tricks.com/currentcolor/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

[custom properties](https://css-tricks.com/tag/custom-properties/) [state](https://css-tricks.com/tag/state/)

**Article**
on
Jan 5, 2021 

### [Custom Properties as State](https://css-tricks.com/custom-properties-as-state/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

[@property](https://css-tricks.com/tag/property/) [custom properties](https://css-tricks.com/tag/custom-properties/)

**Article**
on
Sep 2, 2020 

### [Using @property for CSS Custom Properties](https://css-tricks.com/using-property-for-css-custom-properties/)

[![](https://css-tricks.com/wp-content/cache/breeze-extra/gravatars/41a6f9778d12dfedcc7ec3727d64a12491d75d9a65d4b9323feb075391ae6795)](https://css-tricks.com/author/chriscoyier/) 
[Chris Coyier](https://css-tricks.com/author/chriscoyier/)

### Credit

Thanks to Miriam Suzanne for co-authoring this with me!