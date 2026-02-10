# Read Me First | APG | WAI | W3C

Source: https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/

---

Read Me First

## No ARIA is better than Bad ARIA

Functionally, ARIA roles, states, and properties are analogous to a CSS for assistive technologies.
For screen reader users, ARIA controls the rendering of their non-visual experience.
Incorrect ARIA misrepresents visual experiences, with potentially devastating effects on their corresponding non-visual experiences.

Before using ARIA or any of the guidance in this document, please take time to understand the following two essential principles.

### Principle 1: A role is a promise

This code:

```
<div role="button">Place Order</div>
```

Is a promise that the author of that `<div>` has also incorporated JavaScript that provides the keyboard interactions expected for a button.
Unlike HTML input elements, ARIA roles do not cause browsers to provide keyboard behaviors or styling.

Using a role without fulfilling the promise of that role is similar to making a "Place Order" button that abandons an order and empties the shopping cart.

One of the objectives of this guide is to define expected behaviors for each ARIA role.

### Principle 2: ARIA Can Both Cloak and Enhance, Creating Both Power and Danger

The information assistive technologies need about the meaning and purpose of user interface elements is called accessibility semantics.
From the perspective of assistive technologies, ARIA gives authors the ability to dress up HTML and SVG elements with critical accessibility semantics that the assistive technologies would not otherwise be able to reliably derive.

Some of ARIA is like a cloak; it covers up, or overrides, the original semantics or content.

```
<a role="menuitem">Assistive tech users perceive this element as an item in a menu, not a link.</a>
  <a aria-label="Assistive tech users can only perceive the contents of this aria-label, not the link text">Link Text</a>
```

On the other hand, some uses of ARIA are more like suspenders or belts; they add meaning that provides essential support to the original content.

```
<button aria-pressed="false">Mute</button>
```

This is the power of ARIA.
It enables authors to describe nearly any user interface component in ways that assistive technologies can reliably interpret, thus making components accessible to assistive technology users.

This is also the danger of ARIA.
Authors can inadvertently override accessibility semantics.

```
<table role="log">
  <!--
    Table that assistive technology users will not perceive as a table.
    The log role tells browser this is a log, not a table.
  -->
</table>
<ul role="navigation">
  <!-- This is a navigation region, not a list. -->
  <li><a href="uri1">nav link 1</a></li>
  <li><a href="uri2">nav link 2</a></li>
  <!-- ERROR! Previous list items are not in a list! -->
</ul>
```

## Browser and Assistive Technology Support

**Testing assistive technology interoperability is essential before using code from this guide in production.**
Because the purpose of this guide is to illustrate appropriate use of ARIA 1.2 as defined in the ARIA specification, the design patterns, reference examples, and sample code intentionally **do not** describe and implement coding techniques for working around problems caused by gaps in support for ARIA 1.2 in browsers and assistive technologies.
It is thus advisable to test implementations thoroughly with each browser and assistive technology combination that is relevant within a target audience.

Similarly, JavaScript and CSS in this guide is written to be compatible with the most recent version of Chrome, Firefox, and Safari at the time of writing.

Except in cases where the ARIA Working Group and other contributors have overlooked an error,
examples in this guide that do not function well in a particular browser or with a specific assistive technology are demonstrating browser or assistive technology bugs.
Browser and assistive technology developers can thus utilize code in this guide to help assess the quality of their support for ARIA 1.2.

## Mobile and Touch Support

Currently, this guide does not indicate which examples are compatible with mobile browsers or touch interfaces.
While some of the examples include specific features that enhance mobile and touch support, some ARIA features are not supported in any mobile browser.
In addition, there is not yet a standardized approach for providing touch interactions that work across mobile browsers.

More guidance about touch and mobile support is planned for future releases of the guide.