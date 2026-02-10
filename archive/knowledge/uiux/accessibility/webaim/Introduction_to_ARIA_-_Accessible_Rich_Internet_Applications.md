# Introduction to ARIA - Accessible Rich Internet Applications

Source: https://webaim.org/techniques/aria/

---

# Introduction to ARIA - Accessible Rich Internet Applications

You are here: [Home](/) > [Articles](/articles/) > Introduction to ARIA

## Introduction to ARIA

WAI-ARIA (Accessible Rich Internet Applications or ARIA) is [a W3C specification](https://www.w3.org/WAI/standards-guidelines/aria/) for enhancing accessibility in ways that plain HTML cannot. When used properly, ARIA can...

- enhance accessibility of interactive controls, such as tree menus, sliders, pop-ups, etc.
- define helpful landmarks for page structure
- define dynamically-updated "live regions"
- improve keyboard accessibility and interactivity
- and much more

HTML has a defined—but evolving—vocabulary. For example, `<blink>` has been removed while `<main>` has been added. **ARIA provides new code attributes and values that expand the vocabulary and semantics of HTML for enhanced screen reader accessibility.**

Like HTML, ARIA evolves over time, and is generally well supported in modern browsers and screen readers. Many scripting libraries also support ARIA.

## Rules of ARIA Use

The ARIA specification defines [five rules of ARIA use](https://www.w3.org/TR/using-aria/#notes2) to support optimal accessibility. Summaries of these rules are below.

### Rule #1 - If you can use HTML a native HTML element or attribute, then do so.

HTML is the foundation of web accessibility. **ARIA should not be used when HTML provides sufficient semantics for accessibility! When used incorrectly, ARIA can introduce significant accessibility barriers.**

### Rule #2 - Do not change native semantics, unless you really have to.

Most HTML elements have default semantics or meaning that can be conveyed to screen reader users. When necessary, ARIA can override and change those semantics.

A `<ul>` element, for example, defines an unordered list. When encountered by a screen reader, it is identified as an unordered list. Screen readers also announce the number of list items, enable list item navigation, and much more. If an ARIA `role` is added to the `<ul>`—for example, —`<ul role="navigation">`—then the list semantics are overridden and lost. The element now becomes a navigation landmark (see below) and the accessibility benefits of the unordered list are gone. Instead, `<div role="navigation"><ul>...</ul></div>` provides the benefits of the navigation landmark AND the benefits of the unordered list. (Better yet, `<nav><ul>...</ul></nav>` is semantically equivalent without relying on ARIA at all.)

### Rule #3 - All interactive ARIA controls must be usable with the keyboard.

The [ARIA Design Patterns](https://www.w3.org/WAI/ARIA/apg/patterns/) define standard keyboard interactions for ARIA widgets and controls. This allows everyone to use the widget using the keyboard, and ensures that instructions provided by screen readers align with the actual functionality in the page.

### Rule #4 - Interactive controls must have proper semantics and cannot be hidden

Any element that is keyboard focusable (primarily using the Tab key), *must* have proper semantics so that it will be identified as a link, button, form control, etc., or other element with an appropriate `role` value. Since `role="presentation"` removes semantics, it must never be applied to a focusable element.

Similarly, interactive elements must be visible. Do not hide focused elements with CSS or with `aria-hidden="true"`.

### Rule #5 - All interactive elements must have an accessible name

Text that describes an interactive control must be presented to screen reader users when the control is encountered. A button must have descriptive text (such as "Register") and a text input must have a descriptive label (such as "First Name"). The content that screen readers announce to identify a control is called its ["accessible name"](/articles/label-name/). ARIA can also be used to define accessible names.

## Core Components

The three main components of ARIA are **roles**, **properties**, and **states**.

### Roles

Roles define what an element is or does. Most HTML elements have a default role that is presented to assistive technology. For example, `<button>` has a default role of "button" and `<form>` has a default role of "form". ARIA can define roles that are not available in HTML, and can also override the default roles of HTML elements (see Rule #2 above).

An example of an ARIA role is `<form role="search">`. In HTML, all forms have the same semantics. But with ARIA, you can define the semantics of a particular form as being a search form.

Default HTML roles should not be duplicated using ARIA—avoid things like `<button role="button">`.

ARIA does not change browser behavior or appearance.

Adding `role="button"` to a `<div>`, for example, will not make the `<div>` function like or appear like a button. However, this will cause screen readers to announce it as a button even though it cannot be navigated to or activated using the keyboard. Authors must implement [appropriate design and interaction patterns](https://www.w3.org/WAI/ARIA/apg/), typically via JavaScript and CSS, along with ARIA.

### Properties

ARIA properties define additional semantics not supported in standard HTML. An example is `<button aria-haspopup="true">`. This property extends the standard button to cause a screen reader to announce that the button, if activated, will trigger a pop-up.

### States

ARIA states are attributes that define the current condition of an element. They generally change based on user interaction or some dynamic variable. An example is `<input aria-invalid="true">`. This property will cause a screen reader to read this input as currently being invalid (meaning it needs to be corrected), but this state value could easily be changed to `false` dynamically based on user input.

ARIA roles, states, and properties can be defined in markup or they can be defined and dynamically set and changed using scripting. ARIA states and property attributes always start with "aria-" (e.g., `aria-required="true"`).

## Landmark Roles

ARIA can define roles for significant page areas or regions. These are identified by screen readers and help with orientation and navigation in the page. The available document landmark roles are:

`banner`
:   Site-orientated content that typically contains the name of the web site, logo, search, and/or main navigation. Semantically equivalent to `<header>`

`navigation`
:   The area that contains the navigation links for the document or web site. Semantically equivalent to `<nav>`

`main`
:   The main or central content of the document. Semantically equivalent to `<main>`

`complementary`
:   Supporting content for the main content, often presented in a side bar. Semantically equivalent to `<aside>`

`contentinfo`
:   Informational child content, such as footnotes, copyrights, links to privacy statement, links to preferences, and so on. Semantically equivalent to `<footer>`

`search`
:   A section that contains the search functionality for the site. There is no equivalent element in HTML.

On a typical web page, the logo and header content might be within an element with role of `banner`. The navigation links across the top would be identified within `navigation`, typically contained within the `banner`. The site search form would be given `<form role="search">`. The main body of an article would be `main`. The related links in a side bar might be identified as `complementary`. The footer content and links at the bottom of a page would have a role of `contentinfo`.

Note

All ARIA landmark roles, except `search`, have equivalent HTML "[regions](/techniques/semanticstructure/#regions)". Whenever possible, it is best to use the HTML markup (see Rule #1 above). While using both the HTML element and the ARIA attribute is allowed (e.g., `<nav role="navigation">`), this introduces unnecessary markup and the possibility for error. The terms "landmark" and "region" are typically synonymous in screen readers. [Learn more about regions.](/techniques/semanticstructure/#regions)

Screen readers provide a list of all landmarks/regions on a page and shortcut keys to navigate among them. Some assistive technologies allow the user to jump to specific landmarks/regions (for instance, M for the main content).

### Generic regions

If a significant page or web application area does not align with the landmark roles above, the `role="region"` attribute can be added to create a generic landmark/region. It must have a descriptive accessible name defined using `aria-label` or `aria-labelledby` (e.g., `<div role="region" aria-label="Filters">`).

## ARIA Labels and Descriptions

HTML facilitates associations that support accessibility—`<label>` for form inputs, `<caption>` for data table descriptions, `<th>` for row and column headers in data tables, etc. When HTML cannot create the necessary associations, ARIA can be used.

With `aria-labelledby`, an element references the `id` attribute value (or, in some cases, multiple `id` attribute values) of the element(s) containing the text that acts as its descriptive label. This region will be labeled by and identified by the text within the `<h2>`—"Filters":

<div role="region" **aria-labelledby="filtersheading"**>  
<h2 **id="filtersheading"**>Filters</h2>

With `aria-label` you apply the label text directly in the attribute value. Even though the `<h2>` content is "Search Filters", this region will be labeled by the `aria-label` value of "Filters":

<div role="region" **aria-label="Filters"**>  
<h2>Search Filters</h2>

The `aria-labelledby` approach is better in this case—it does not duplicate the content, and it ensures that if the heading text is changed, the label for the region will change as well. When text within another element is available to be referenced, then `aria-labelledby` should be used rather than `aria-label`.

Every interactive element needs text describing its function. Additional visually-associated descriptive text can be associated with `aria-describedby`. Like `aria-labelledby`, the descriptive element's `id` attribute value is referenced.

<label for="password">Password:</label>  
<input id="password" **aria-describedby="requirements"**>  
<p **id="requirements"**>Your password must be at least 8 characters in length</p>

Descriptions are typically read by screen readers after labels and sometimes as the very last information for an element. Descriptions are most useful for form inputs. *Note that the previous example uses `<label>` rather than ARIA labeling because `<label>` is sufficient (see Rule #1 above).*

Tip

ARIA labeling is most useful and powerful when used with form inputs. See our article on [Advanced Form Labeling](/techniques/forms/advanced).

Defining labels with ARIA comes with some constraints and warnings. How labels and descriptions are calculated in web pages is [extremely complex](https://www.w3.org/TR/html-aam-1.0/%23accessible-name-and-description-computation), but below are a few general guidelines.

- In order to be assigned an ARIA label, an element must be labelable—either a link, button, or form control, or having specific HTML or ARIA semantics. Many elements are not labelable—`<p>`, `<div>`, and `<span>`, for example, unless assigned an appropriate ARIA `role`.
- ARIA labels override the default text and accessible names for HTML elements. If an input has a `<label>` *and* an `aria-label` or `aria-labelledby`, the `<label>` will not be read. Similarly, link/button text and image `alt` attribute values are overridden by ARIA label text.
- An element can only have one accessible name, though you can reference multiple element `id`s with `aria-labelledby` or `aria-describedby` to concatenate multiple texts:  
  `<table aria-labelledby="tablecaption tabledisclaimer">`
- WCAG requires that the visible text label for an element be included within its accessible name (which is read by a screen reader). When using ARIA labels, ensure consistency between what sighted users see and what screen reader users hear. Many screen reader users have some vision.
- Screen reader users can pause and explore page text content—even reading content word-by-word or letter-by-letter. However, this is not possible with ARIA labels or descriptions which are instead read as a stream of text. Keep these succinct.
- When associated `aria-labelledby` or `aria-describedby` text is read, all semantics are removed. Links, tables, lists, etc. within the referenced element are not identified when the label or description text is presented.
- The best way to ensure that ARIA labels and descriptions have been implemented correctly is to listen in a screen reader. You can also inspect the accessible name and description of an element using browser [Developer Tools](https://developers.google.com/web/tools/chrome-devtools/accessibility/reference).

## Dynamic Content Updates

Dynamic content changes may create accessibility problems. What happens if a screen reader reads an element while it is updated? If the updated content is important, should the user be interrupted? Should focus be set immediately to the new content? Should the user simply be informed of the update so they can find it elsewhere? Should nothing happen at all?

ARIA can flag dynamically-changing page areas as *live regions*. Live regions make content updates screen reader compatible, inform the user of updates, provide controls for the live region, determine the amount of new content that is read, and much more.

To create a live region, the developer adds the `aria-live` property to the element that will update. This attribute must be set when the page first loads; injecting it later doesn't work reliably. The `aria-live` attribute takes values of `off`, `polite`, or `assertive` which specifies what a screen reader should do when the element is updated.

A value of off (`aria-live="off"`) tells the screen reader to not announce the update. If the screen reader user later encounters the updated content, it will be read at that time. This would be used for irrelevant or less important content updates. It is useful primarily for live regions that are dynamically change from `polite` or `assertive` to `off` using scripting.

A value of `polite` will cause the updated content to be read by the screen reader at the next logical pause. This value is most common for status notification, weather or stock updates, chat messages, etc.

An `aria-live` value of `assertive` will announce the content change immediately—quite possibly when the screen reader user is listening to other page content. Assertive is best reserved for critical updates, such as error messages.

Care is necessary with all live regions to ensure that screen reader users are not needlessly interrupted or overwhelmed with notifications, especially if there are multiple live regions on a page. Testing the page in a screen reader will quickly reveal if this is the case.

There are additional ARIA `role` attribute values that create live regions including `alert`, `log`, and `timer`. The high level of fidelity with ARIA live regions allows great flexibility both for developers and for end users.

## Keyboard Accessibility of ARIA Widgets

Examples of widgets include sliders, drop-down and fly-out menus, tree systems, drag-and-drop controls, auto-completing text boxes, dialog windows, and tooltips, to name a few. They are interactive elements that are created and controlled through scripting. Widgets are usually either not native to HTML or are HTML controls that are greatly enhanced through scripting.

Widgets are not natively accessible, and HTML has very limited markup for defining complex widgets. However, by establishing a standard set of roles, properties, and states, ARIA helps developers implement accessibility with relative ease.

The [ARIA Design Patterns and Widgets](https://www.w3.org/WAI/ARIA/apg/patterns/) provides specific requirements for creating a wide variety of widgets. It's vital that this guidance be followed! Below are a few high-level considerations.

In HTML, only links and form controls can receive keyboard focus. As the user presses Tab to navigate through a page, the browser stops or sets focus only on these types of elements, allowing them to be activated and manipulated.

With scripting and CSS, other page elements (such as `<p>` or `<span>`) can be made to appear and behave like interactive controls to sighted mouse users. Without additional effort, though, these would be neither keyboard accessible nor identified as interactive controls to a screen reader user. To avoid this loss of functionality, use HTML markup whenever possible (e.g., `<button>` for elements that function like buttons, `<a>` for links, `<select>` for select menus, etc.). However, when custom widgets are necessary, ARIA can help fill this gap.

Important!

To be accessible, an interactive widget or control must:

1. Be keyboard focusable and have appropriate keyboard interactions.
2. Have a descriptive accessible name.
3. Have appropriate ARIA markup that identifies its role, states, and properties

Standard HTML controls should typically be used to provide keyboard interactivity. Alternatively, an element that is not natively focusable (such as a `<div>`) can be made focusable using `tabindex` ([read more about tabindex](/techniques/keyboard/tabindex)):

- `tabindex="0"` makes any element focusable using the keyboard or scripting, as if it were a link or button.
- `tabindex="-1"` makes any element focusable with scripting, but not with the keyboard.
- Positive tabindex values (`tabindex="1"` or higher) must always be avoided. They force an artificial navigation order on the page that destroys the natural order.

By applying `tabindex="0"`, the browser will stop and set focus to the element in the navigation order of the document when the user Tabs to the element. This allows an element to be interactive, such as triggering functionality when the element receives keyboard focus or when the user presses a key while the element has focus. This is sometimes necessary with certain ARIA widgets, such as tab panels, menus, and tree controls. The keyboard functionality **MUST** align with the ARIA Design Pattern requirements to ensure that the widget provides standard keyboard interaction patterns.

Important!

If an element is focusable by pressing Tab on the keyboard, it must also be functional—meaning it can respond to keyboard activation. Apply `tabindex="0"` only to interactive elements.

`tabindex="-1"` allows an element to receive focus programmatically—when the user follows a link to the element (`<a href="#maincontent"> ...`) or when focus is set with scripting (e.g., `document.getElementById('errormessage').focus();`). This is especially helpful for error messages, dialog boxes, etc. that are not natively-focusable HTML controls, but that you want to be focused for optimal accessibility.

Important!

`tabindex="-1"` removes the element from the keyboard navigation order—users can't Tab to it. As such, it is seldom appropriate on links, buttons, or other elements that the user may need to navigate to.

Once a widget is keyboard focusable, it must have a descriptive accessible name using HTML values (such as button text) or associations (such as `<label>`) or, if not possible using HTML, by using `aria-labelledby` or `aria-label`.

Additionally, the element must have an appropriate ARIA `role` value, as defined in the Design Patterns. This ensures that a screen reader user is informed what the widget is and what it does. This can also cause the screen reader to announce widget-specific instructions on how to interact with it. Certain widgets also require ARIA states and properties to inform the screen reader and support keyboard accessibility.

By expanding the focus capabilities in the browser to elements that otherwise cannot receive focus, and by providing proper accessible names and ARIA markup, web authors have great flexibility and power to build complex widgets and interfaces that are highly accessible.

## Basic ARIA Examples

### Form enhancements

ARIA can enhance form accessibility in ways HTML cannot.

- `aria-labelledby` and `aria-label` allow complex associations of text to form inputs, in ways that `<label>` cannot.
- `aria-describedby` associates secondary descriptions to inputs, such as field requirements or error messages.- `aria-required="true"` identifies inputs that require user input.- `aria-invalid="true"` identifies inputs that are in an error state.- `role="radiogroup"`, when given an ARIA label, provides the same functionality as `<fieldset>`/`<legend>` for groups of inputs, but with more flexibility.

The [Creating Accessible Forms](/techniques/forms/) article provides details on using these ARIA attributes.

### Button enhancements

The semantics of buttons can be enhanced for buttons that have specialized functions.

- `<button aria-haspopup="dialog">` causes screen readers to announce that the button triggers a dialog window. Additional `aria-haspopup` values of `menu`, `listbox`, `tree`, `grid`, and `true` are also available. Be sure to follow the ARIA Design Patterns.
- `<button aria-expanded="true | false">` can be used on buttons that expand or collapse content—often called disclosures, zippies, or accordions. Setting the appropriate values informs screen readers of the state of the button and whether the following content is available or not.
- `<button aria-pressed="true|false">` indicates whether a toggle button is currently pressed/active or not.

Tip

Elements can be styled based on their ARIA attributes and attribute values. This can be helpful to provide visual indications of states—and can allow visual changes to be more effectively controlled via CSS as opposed to scripting. For example, this CSS declaration applies a blue background to any element having `aria-pressed="true"`:  
`[aria-pressed=true] {background-color:#00f;}`

### Decorative and presentational elements

The `role="presentation"` attribute removes the native semantics of an HTML element, making it akin to a `<div>` or `<span>`. This can be useful if an HTML element is used to control presentation or layout, or if the element's native semantics are not appropriate. Common examples include layout tables, lists used for presentational structure, and `<svg>` elements that need no alternative text.

### Hiding content from screen reader users

The `aria-hidden="true"` attribute hides certain types of content from screen readers. There are *very* few use cases for `aria-hidden`—if something is visible in the page, it should almost always be presented to screen reader users. However, `aria-hidden="true"` can be used to avoid significant repetition of content or for elements that should not be presented to screen reader users.

Important!

`aria-hidden="true"` must never be assigned to something that is keyboard-navigable (or that contains something that is), because the element remains within the keyboard navigation flow even though screen readers may not announce its contents or surrounding content. This can easily confuse screen reader users. In very isolated cases `tabindex="-1"` might be used with `aria-hidden="true"` to remove the element from being read and navigated to.

### Scalable Vector Graphics (SVG)

Accessibility for `<svg>` elements is not yet robust. Fortunately, ARIA can be used to ensure the content in SVG elements is accessible.

In the following example, the `role="img"` attribute defines the element as being an image. The accessible name (alternative text) is defined using `aria-labelledby` which references the `<title>` element within the SVG:

<svg role="img" aria-labelledby="title">  
<title id="title">Sales increased 10% from 2010 to 2015</title>  
...  
</svg>

The next example also has `role="img"`, but instead uses `aria-label` to define the alternative text:

<svg role="img" aria-label="Sales increased 10% from 2010 to 2015">  
...  
</svg>

In a screen reader, both examples above sound the same as `<img alt="Sales increased 10% from 2010 to 2015">`

If the SVG were purely decorative, or if adjacent accessible text provided the image alternative, then `<svg role="presentation">` would effectively hide the element—similar to `<img alt="">`.

For more complex and custom-built widgets, be sure to follow the standardized [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/). Screen reader testing is almost always necessary when ARIA is implemented.

## Further Reading

This is only an overview. To ensure accessible ARIA implementation, please follow the [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/). The [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA) also provides a useful ARIA reference. For more details on JavaScript and scripted interactions, see our [JavaScript Accessibility article](https://webaim.org/techniques/javascript/).