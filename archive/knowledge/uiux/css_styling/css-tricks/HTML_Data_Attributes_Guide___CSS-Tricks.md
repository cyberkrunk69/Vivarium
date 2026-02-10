# HTML Data Attributes Guide | CSS-Tricks

Source: https://css-tricks.com/a-complete-guide-to-data-attributes/

---

#### Table of Contents

1. [Introduction](#intro)
2. [Syntax](#syntax)
3. [Styling with data attributes](#styling)
4. [Accessing data attributes in JavaScript](#attributes-javascript)

### Introduction

HTML elements can have attributes on them that are used for anything from accessibility information to stylistic control.

```
<!-- We can use the `class` for styling in CSS, and we've also make this into a landmark region -->
<div class="names" role="region" aria-label="Names"></div>
```

What is *discouraged* is *making up* your own attributes, or repurposing existing attributes for unrelated functionality.

```
<!-- `highlight` is not an HTML attribute -->
<div highlight="true"></div>
<!-- `large` is not a valid value of `width` -->
<div width="large">
```

There are a variety of reasons this is bad. Your HTML becomes invalid, which may not have any actual negative consequences, but robs you of that warm fuzzy valid HTML feeling. The most compelling reason is that HTML is a living language and just because attributes and values that don’t do anything today doesn’t mean they never will.

Good news though: you can make up your own attributes. You just need to prefix them with `data-*` and then you’re free to do what you please!

### Syntax

It can be awfully handy to be able to make up your own HTML attributes and put your own information inside them. Fortunately, you can! That’s exactly what **data attributes** are. They are like this:

```
<!-- They don't need a value -->
<div data-foo></div>
<!-- ...but they can have a value -->
<div data-size="large"></div>
<!-- You're in HTML here, so careful to escape code if you need to do something like put more HTML inside -->
<li data-prefix="Careful with HTML in here."><li>
<!-- You can keep dashing if you like -->
<aside data-some-long-attribute-name><aside>
```

Data attributes are often referred to as `data-*` attributes, as they are always formatted like that. The word `data`, then a dash `-`, then other text you can make up.

#### Can you use the `data` attribute alone?

```
<div data=""></div>
```

It’s probably not going to hurt anything, but you won’t get the JavaScript API we’ll cover later in this guide. You’re essentially making up an attribute for yourself, which as I mentioned in the intro, is discouraged.

#### What *not* to do with data attributes

Store content that should be accessible. If the content should be seen or read on a page, don’t only put them in data attributes, but make sure that content is in the HTML *content* somewhere.

```
<!-- This isn't accessible content -->
<div data-name="Chris Coyier"></div>
<!-- If you need programmatic access to it but shouldn't be seen, there are other ways... -->
<div>
  <span class="visually-hidden">Chris Coyier</span>
</div>
```

[Here’s more about hiding things.](https://css-tricks.com/inclusively-hidden/)

### Styling with data attributes

CSS can [select HTML elements based on attributes](https://css-tricks.com/almanac/selectors/a/attribute/) and their values.

```
/* Select any element with this data attribute and value */
[data-size="large"] {
  padding: 2rem;
  font-size: 125%;
}
/* You can scope it to an element or class or anything else */
button[data-type="download"] { }
.card[data-pad="extra"] { }
```

This can be compelling. The predominant styling hooks in HTML/CSS are classes, and while classes are great (they have medium specificity and nice JavaScript methods via `classList`) an element either *has it or it doesn’t* (essentially *on or off*). With `data-*` attributes, you get that on/off ability *plus* the ability to select based on the value it has at the same specificity level.

```
/* Selects if the attribute is present at all */
[data-size] { }
/* Selects if the attribute has a particular value */
[data-state="open"],
[aria-expanded="true"] { }
/* "Starts with" selector, meaning this would match "3" or anything starting with 3, like "3.14" */
[data-version^="3"] { }
/* "Contains" meaning if the value has the string anywhere inside it */
[data-company*="google"] { }
```

#### The specificity of attribute selectors

It’s the exact same as a class. We often think of specificity as a four-part value:

inline style, IDs, classes/attributes, tags

So a single attribute selector alone is **0, 0, 1, 0**. A selector like this:

```
div.card[data-foo="bar"] { }
```

…would be **0, 0, 2, 1**. The 2 is because there is one class (`.card`) and one attribute (`[data-foo="bar"]`), and the 1 is because there is one tag (`div`).

![Illustration of a CSS selector including a data attribute.](https://i0.wp.com/css-tricks.com/wp-content/uploads/2020/02/specificity-selector.png?fit=1024%2C386&ssl=1)

Attribute selectors have less specificity than an ID, more than an element/tag, and the same as a class.

#### Case-insensitive attribute values

In case you’re needing to correct for possible capitalization inconsistencies in your data attributes, the attribute selector has a case-insensitive variant for that.

```
/* Will match
<div data-state="open"></div>
<div data-state="Open"></div>
<div data-state="OPEN"></div>
<div data-state="oPeN"></div>
*/
[data-state="open" i] { }
```

It’s the little `i` within the bracketed selector.

#### Using data attributes visually

CSS allows you to yank out the data attribute value and display it if you need to.

```
/* <div data-emoji="✅"> */
[data-emoji]::before {
  content: attr(data-emoji); /* Returns '✅' */
  margin-right: 5px;
}
```

#### Example styling use-case

You could use data attributes to specify how many columns you want a grid container to have.

```
<div data-columns="2"></div>
<div data-columns="3"></div>
<div data-columns="4"></div>
```

### Accessing data attributes in JavaScript

Like any other attribute, you can access the value with the generic method `getAttribute`.

```
let value = el.getAttribute("data-state");
// You can set the value as well.
// Returns data-state="collapsed"
el.setAttribute("data-state", "collapsed");
```

But data attributes have their own special API as well. Say you have an element with multiple data attributes (which is totally fine):

```
<span 
  data-info="123" 
  data-index="2" 
  data-prefix="Dr. "
  data-emoji-icon="🏌️‍♀️"
></span>
```

If you have a reference to that element, you can set and get the attributes like:

```
// Get
span.dataset.info; // 123
span.dataset.index; // 2
// Set
span.dataset.prefix = "Mr. ";
span.dataset.emojiIcon = "🎪";
```

Note the camelCase usage on the last line there. It automatically converts kebab-style attributes in HTML, like `data-this-little-piggy`, to camelCase style in JavaScript, like `dataThisLittlePiggy`.

This API is arguably not quite as nice as [`classList`](https://developer.mozilla.org/en-US/docs/Web/API/Element/classList) with the clear `add`, `remove`, `toggle`, and `replace` methods, but it’s better than nothing.

You have access to inline datasets as well:

```
<img src="spaceship.png"
  data-ship-id="324" data-shields="72%"
  onclick="pewpew(this.dataset.shipId)">
</img>
```

#### JSON data inside data attributes

```
<ul>
  <li data-person='
    {
      "name": "Chris Coyier",
      "job": "Web Person"
    }
  '></li>
</ul>
```

Hey, why not? It’s just a string and it’s possible to format it as valid JSON (mind the quotes and such). You can yank that data and parse it as needed.

```
const el = document.querySelector("li");
let json = el.dataset.person;
let data = JSON.parse(json);
console.log(data.name); // Chris Coyier
console.log(data.job); // Web Person
```

#### JavaScript use-cases

The concept is that you can use data attributes to put information in HTML that JavaScript may need access to do certain things.

A common one would have to do with database functionality. Say you have a “Like” button:

```
<button data-id="435432343">♡</button>
```

That button could have a click handler on it which performs an Ajax request to the server to increment the number of likes in a database on click. It knows which record to update because it gets it from the data attribute.

### Specifications

- [Selectors Level 4](https://drafts.csswg.org/selectors-4/#attribute-selectors) (Working Draft)
- [Selectors Level 3](https://drafts.csswg.org/selectors-3/#attribute-selectors) (Recommended)
- [Selectors Level 2, Revision 1](https://www.w3.org/TR/CSS2/selector.html#attribute-selectors) (Initial Definition)

### Browser support

This browser support data is from [Caniuse](http://caniuse.com/#feat=dataset), which has more detail. A number indicates that browser supports the feature at that version and up.

#### Desktop

| Chrome | Firefox | IE | Edge | Safari |
| --- | --- | --- | --- | --- |
| 7 | 6 | 11 | 12 | 5.1 |

#### Mobile / Tablet

| Android Chrome | Android Firefox | Android | iOS Safari |
| --- | --- | --- | --- |
| 144 | 147 | 3 | 5.0-5.1 |