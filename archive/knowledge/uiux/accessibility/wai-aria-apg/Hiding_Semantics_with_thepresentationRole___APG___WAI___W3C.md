# Hiding Semantics with thepresentationRole | APG | WAI | W3C

Source: https://www.w3.org/WAI/ARIA/apg/practices/hiding-semantics/

---

Hiding Semantics with the Presentation Role

## Introduction

While ARIA is primarily used to express semantics, there are some situations where hiding an element’s semantics from assistive technologies is helpful.
This is done with the [presentation](https://w3c.github.io/aria/#presentation) role, which declares that an element is being used only for presentation and therefore does not have any accessibility semantics.
The ARIA 1.1 specification also includes role [none](https://w3c.github.io/aria/#none), which serves as a synonym for `presentation`.

For example, consider a tabs widget built using an HTML `ul` element.

```
<ul role="tablist">
  <li role="presentation">
    <a role="tab" href="#">Tab 1</a>
  </li>
  <li role="presentation">
    <a role="tab" href="#">Tab 2</a>
  </li>
  <li role="presentation">
    <a role="tab" href="#">Tab 3</a>
  </li>
</ul>
```

Because the list is declared to be a tablist, the list items are not in a list context.
It could confuse users if an assistive technology were to render those list items.
Applying role `presentation` to the `li` elements tells browsers to leave those elements out of their accessibility tree.
Assistive technologies will thus be unaware of the list item elements and see the tab elements as immediate children of the tablist.

## Common Uses of Role `presentation`

Three common uses of role `presentation` are:

1. Hiding a decorative image; it is equivalent to giving the image null alt text.
2. Suppressing table semantics of tables used for layout in circumstances where the table semantics do not convey meaningful relationships.
3. Eliminating semantics of intervening orphan elements in the structure of a composite widget, such as a tablist, menu, or tree as demonstrated in the example above.

## Effects of Role `presentation`

When `role="presentation"` is specified on an element, if a [condition that requires a browser to ignore the `presentation` role](#presentation_role_ignored) does not exist, it has the following three effects.

1. The element’s implied ARIA role and any ARIA states and properties associated with that role are hidden from assistive technologies.
2. Text contained by the element, i.e., inner text, as well as inner text of all its descendant elements remains visible to assistive technologies.
   Of course, text that is explicitly hidden, e.g., styled with `display: none` or has `aria-hidden="true"`, is not visible to assistive technologies.
3. The roles, states, and properties of each descendant element remain visible to assistive technologies unless the descendant requires the context of the presentational element.
   For example:
   - If `presentation` is applied to a `ul` or `ol` element, each child `li` element inherits the `presentation` role because ARIA requires the `listitem` elements to have the parent `list` element.
     So, the `li` elements are not exposed to assistive technologies, but elements contained inside of those `li` elements, including nested lists, are visible to assistive technologies.
   - Similarly, if `presentation` is applied to a `table` element, the descendant `caption`, `thead`, `tbody`, `tfoot`, `tr`, `th`, and `td` elements inherit role `presentation` and are thus not exposed to assistive technologies.
     But, elements inside of the `th` and `td` elements, including nested tables, are exposed to assistive technologies.

## Conditions That Cause Role `presentation` to be Ignored

Browsers ignore `role="presentation"`, and it therefore has no effect, if either of the following are true about the element to which it is applied:

- The element is focusable, e.g. it is natively focusable like an HTML link or input, or it has a `tabindex` attribute.
- The element has any [global ARIA states and properties](https://w3c.github.io/aria/#global_states), e.g., `aria-label`.

## Example Demonstrating Effects of the `presentation` Role

In the following code, role `presentation` suppresses the list and list item semantics.

```
<ul role="presentation">
  <li>Date of birth:</li>
  <li>January 1, 3456</li>
</ul>
```

When the above code is parsed by a browser, it is semantically equivalent to the following code:

```
<div>Date of birth:</div>
<div>January 1, 3456</div>
```

## Roles That Automatically Hide Semantics by Making Their Descendants Presentational

There are some types of user interface components that, when represented in a platform accessibility API, can only contain text.
For example, accessibility APIs do not have a way of representing semantic elements contained in a button.
To deal with this limitation, WAI-ARIA requires browsers to automatically apply role `presentation` to all descendant elements of any element with a role that cannot support semantic children.

The roles that require all children to be presentational are:

- button
- checkbox
- img
- meter
- menuitemcheckbox
- menuitemradio
- option
- progressbar
- radio
- scrollbar
- separator
- slider
- switch
- tab

For instance, consider the following tab element, which contains a heading.

```
<li role="tab"><h2>Title of My Tab</h2></li>
```

Because WAI-ARIA requires descendants of tab to be presentational, the heading semantic is not exposed to assistive technology users.
Thus, the following code is equivalent.

```
<li role="tab"><h2 role="presentation">Title of My Tab</h2></li>
```

So, from the perspective of anyone using a technology that relies on an accessibility API, such as a screen reader, the heading does not exist.
As described above in the section on [Effects of Role `presentation`](#presentation_role_effects), the previous code is equivalent to the following.

```
<li role="tab">Title of My Tab</li>
```