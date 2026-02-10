# Providing Accessible Names and Descriptions | APG | WAI | W3C

Source: https://www.w3.org/WAI/ARIA/apg/practices/names-and-descriptions/

---

Providing Accessible Names and Descriptions

## Introduction

Providing elements with accessible names, and where appropriate, accessible descriptions, is one of the most important responsibilities authors have when developing accessible web experiences.
While doing so is straightforward for most elements, technical mistakes that can completely block users of assistive technologies are easy to make and unfortunately common.
To help authors effectively provide accessible names and descriptions, this section explains their purpose, when authors need to provide them, how browsers assemble them, and rules for coding and composing them.
It also guides authors in the use of the following naming and describing techniques and WAI-ARIA properties:

- Naming:
  - Naming with child content.
  - Naming with a string attribute via `aria-label`.
  - Naming by referencing content with `aria-labelledby`.
  - Naming form controls with the label element.
  - Naming fieldsets with the legend element.
  - Naming tables and figures with captions.
  - Fallback names derived from titles and placeholders.
- Describing:
  - Describing by referencing content with `aria-describedby`.
  - Describing tables and figures with captions.
  - Descriptions derived from titles.

## What ARE Accessible Names and Descriptions?

An accessible name is a short string, typically 1 to 3 words, that authors associate with an element to provide users of assistive technologies with a label for the element.
For example, an input field might have an accessible name of "User ID" or a button might be named "Submit".

An accessible name serves two primary purposes for users of assistive technologies, such as screen readers:

1. Convey the purpose or intent of the element.
2. Distinguish the element from other elements on the page.

Both the WAI-ARIA specification and WCAG require all focusable, interactive elements to have an accessible name.
In addition dialogs and some structural containers, such as [tables](https://w3c.github.io/aria/#table) and [regions](https://w3c.github.io/aria/#region), are required to have a name.
Many other elements can be named, but whether a name will enhance the accessible experience is determined by various characteristics of the surrounding context.
Finally, there are some elements where providing an accessible name is technically possible but not advisable.
The [Accessible Name Guidance by Role](#naming_role_guidance) section lists naming requirements and guidelines for every ARIA role.

An accessible description is also an author-provided string that is rendered by assistive technologies.
Authors supply a description when there is a need to associate additional information with an element, such as instructions or format requirements for an input field.

Assistive technologies present names differently from descriptions.
For instance, screen readers typically announce the name and role of an element first, e.g., a button named "Mute Conversation"could be spoken as "Mute Conversation button".
If an element has a state, it could be announced either before or after the name and role; after name and role is the typical default.
For example, a switch button named "Mute Conversation" in the "off" state could be announced as "Mute Conversation switch button off".
Because descriptions are optional strings that are usually significantly longer than names, they are presented last, sometimes after a slight delay.
For example, "Mute Conversation Switch button off, Silences alerts and notifications about activity in this conversation."
To reduce verbosity, some screen readers do not announce descriptions by default but instead inform users of their presence so that users can press a key that will announce the description.

## How Are Name and Description Strings Derived?

Because there are several elements and attributes for specifying text to include in an accessible name or description string, and because authors can combine them in a practically endless number of ways, browsers implement fairly complex algorithms for assembling the strings.
The sections on [accessible name calculation](#name_calculation) and [accessible description calculation](#description_calculation) explain the algorithms and how they implement precedence.
However, most authors do not need such detailed understanding of the algorithms since nearly all circumstances where a name or description is useful are supported by the coding patterns described in the [naming techniques](#naming_techniques) and [describing techniques](#describing_techniques) sections.

## Cardinal Rules of Naming

### Rule 1: Heed Warnings and Test Thoroughly

Several of the [naming techniques](#naming_techniques) below include notes that warn against specific coding patterns that are either prohibited by the ARIA specification or fall into gray space that is not yet fully specified.
Some of these prohibited or ambiguous patterns may appear logical and even yield desired names in some browsers.
However, it is unlikely they will provide consistent results across browsers, especially over time as work to improve the consistency of name calculation across browsers progresses.

In addition to heeding the warnings provided in the naming techniques, it is difficult to over emphasize the importance of testing to ensure that names browsers calculate match expectations.

### Rule 2: Prefer Visible Text

When a user interface includes visible text that could be used to provide an appropriate accessible name, using the visible text for the accessible name simplifies maintenance, prevents bugs, and reduces language translation requirements.
When names are generated from text that exists only in markup and is never displayed visually, there is a greater likelihood that accessible names will not be updated when the user interface design or content are changed.

If an interactive element, such as an input field or button, does not have a visually persistent text label, consider adjusting the design to include one.
In addition to serving as a more robust source for an accessible name, visible text labels enhance accessibility for many people with disabilities who do not use assistive technologies that present invisible accessible names.
In most circumstances, visible text labels also make the user interface easier to understand for all users.

### Rule 3: Prefer Native Techniques

In HTML documents, whenever possible, rely on HTML naming techniques, such as the HTML `label` element for form elements and `caption` element for tables.
While less flexible, their simplicity and reliance on visible text help ensure robust accessible experiences.
Several of the [naming techniques](#naming_techniques) highlight specific accessibility advantages of using HTML features instead of ARIA attributes.

### Rule 4: Avoid Browser Fallback

When authors do not specify an accessible name using an element or attribute that is intended for naming, browsers attempt to help assistive technology users by resorting to fallback methods for generating a name.
For example, the HTML `title` and `placeholder` attributes are used as last resort sources of content for accessible names.
Because the purpose of these attributes is not naming, their content typically yields low quality accessible names that are not effective.

### Rule 5: Compose Brief, Useful Names

Similar to how visually crowded screens and ambiguous icons reduce usability, excessively long, insufficiently distinct, or unclear accessible names can make a user interface very difficult, or even impossible, to use for someone who relies on a non-visual form of the user interface.
In other words, for a web experience to be accessible, its accessible names must be effective.
The section on [Composing Effective and User-friendly Accessible Names](#naming_effectively) provides guidance for balancing brevity and clarity.

## Naming Techniques

### Naming with Child Content

Certain elements get their name from the content they contain.
For example, the following link is named "Home".

```
<a href="/">Home</a>
```

When assistive technologies render an element that gets its accessible name from its content, such as a link or button, the accessible name is the only content the user can perceive for that element.
This is in contrast to other elements, such as text fields or tables, where the accessible name is a label that is presented in addition to the value or content of the element.
For instance, the accessible name of a table can be derived from a caption element, and assistive technologies render both the caption and all other content contained inside the table.

Elements having one of the following roles are, by default, named by a string calculated from their descendant content:

- button
- cell
- checkbox
- columnheader
- gridcell
- heading
- link
- menuitem (content contained in a child `menu` element is excluded.)
- menuitemcheckbox
- menuitemradio
- option
- radio
- row
- rowheader
- switch
- tab
- tooltip
- treeitem (content included in a child `group` element is excluded.)

When calculating a name from content for an element, user agents recursively walk through each of its descendant elements, calculate a name string for each descendant, and concatenate the resulting strings.
In two special cases, certain descendants are ignored: `group` descendants of `treeitem` elements and `menu` descendants of `menuitem` elements are omitted from the calculation.
For example, in the following `tree`, the name of the first tree item is "Fruits"; "Apples", "Bananas", and "Oranges" are omitted.

```
<ul role="tree">
  <li role="treeitem">Fruits
    <ul role="group">
      <li role="treeitem">Apples</li>
      <li role="treeitem">Bananas</li>
      <li role="treeitem">Oranges</li>
    </ul>
  </li>
</ul>
```

#### Warning

If an element with one of the above roles that supports naming from child content is named by using `aria-label` or `aria-labelledby`, content contained in the element and its descendants is hidden from assistive technology users unless the descendant content is referenced by `aria-labelledby`.
It is strongly recommended to avoid using either of these attributes to override content of one of the above elements except in rare circumstances where hiding content from assistive technology users is beneficial.
In addition, in situations where visible content is hidden from assistive technology users by use of one of these attributes, thorough testing with assistive technologies is particularly important.

### Naming with a String Attribute Via `aria-label`

The [aria-label](https://w3c.github.io/aria/#aria-label) property enables authors to name an element with a string that is not visually rendered.
For example, the name of the following button is "Close".

```
<button type="button" aria-label="Close">X</button>
```

The `aria-label` property is useful when there is no visible text content that will serve as an appropriate accessible name.

The `aria-label` property affects assistive technology users in one of two different ways, depending on the role of the element to which it is applied.
When applied to an element with one of the roles that supports [naming from child content](#naming_with_child_content), `aria-label` hides descendant content from assistive technology users and replaces it with the value of `aria-label`.
However, when applied to nearly any other type of element, assistive technologies will render both the value of `aria-label` and the content of the element.
For example, the name of the following navigation region is "Product".

```
<nav aria-label="Product">
  <!-- list of navigation links to product pages -->
</nav>
```

When encountering this navigation region, a screen reader user will hear the name and role of the element, e.g., "Product navigation region", and then be able to read through the links contained in the region.

#### Warning

1. If `aria-label` is applied to an element with one of the roles that supports [naming from child content](#naming_with_child_content), content contained in the element and its descendants is hidden from assistive technology users.
   It is strongly recommended to avoid using `aria-label` to override content of one of these elements except in rare circumstances where hiding content from assistive technology users is beneficial.
2. There are certain types of elements, such as paragraphs and list items, that should not be named with `aria-label`.
   They are identified in the table in the [Accessible Name Guidance by Role](#naming_role_guidance) section.
3. Because the value of `aria-label` is not rendered visually, testing with assistive technologies to ensure the expected name is presented to users is particularly important.
4. When a user interface is translated into multiple languages, ensure that `aria-label` values are translated.

### Naming with Referenced Content Via `aria-labelledby`

The [aria-labelledby property](https://w3c.github.io/aria/#aria-labelledby) enables authors to reference other elements on the page to define an accessible name.
For example, the following switch is named by the text content of a previous sibling element.

```
<span id="night-mode-label">Night mode</span>
<span role="switch" aria-checked="false" tabindex="0" aria-labelledby="night-mode-label"></span>
```

Note that while using `aria-labelledby` is similar in this situation to using an HTML `label` element with the `for` attribute, one significant difference is that browsers do not automatically make clicking on the labeling element activate the labeled element; that is an author responsibility.
However, HTML `label` cannot be used to label a `span` element.
Fortunately, an HTML `input` with `type="checkbox"` allows the ARIA `switch` role, so when feasible, using the following approach creates a more robust solution.

```
<label for="night-mode">Night mode</label>
<input type="checkbox" role="switch" id="night-mode">
```

The `aria-labelledby` property is useful in a wide variety of situations because:

- It has the highest precedence when browsers calculate accessible names, i.e., it overrides names from child content and all other naming attributes, including `aria-label`.
- It can concatenate content from multiple elements into a single name string.
- It incorporates content from elements regardless of their visibility, i.e., it even includes content from elements with the HTML `hidden` attribute, CSS `display: none`, or CSS `visibility: hidden` in the calculated name string.
- It incorporates the value of input elements, i.e., if it references a textbox, the value of the textbox is included in the calculated name string.

An example of referencing a hidden element with `aria-labelledby` could be a label for a night switch control:

```
<span id="night-mode-label" hidden>Night mode</span>
<input type="checkbox" role="switch" aria-labelledby="night-mode-label">
```

In some cases, the most effective name for an element is its own content combined with the content of another element.
Because `aria-labelledby` has highest precedence in name calculation, in those situations, it is possible to use `aria-labelledby` to reference both the element itself and the other element.
In the following example, the "Read more..." link is named by the element itself and the article’s heading, resulting in a name for the link of "Read more... 7 ways you can help save the bees".

```
<h2 id="bees-heading">7 ways you can help save the bees</h2>
<p>Bees are disappearing rapidly. Here are seven things you can do to help.</p>
<p><a id="bees-read-more" aria-labelledby="bees-read-more bees-heading">Read more...</a></p>
```

When multiple elements are referenced by `aria-labelledby`, text content from each referenced element is concatenated in the order specified in the `aria-labelledby` value.
If an element is referenced more than one time, only the first reference is processed.
When concatenating content from multiple elements, browsers trim leading and trailing white space and separate content from each element with a single space.

```
<button id="download-button" aria-labelledby="download-button download-details">Download</button>
<span id="download-details">PDF, 2.4 MB</span>
```

In the above example, the accessible name of the button will be "Download PDF, 2.4 MB", with a space between "Download" and "PDF", and not "DownloadPDF, 2.4 MB".

#### Warning

1. The `aria-labelledby` property cannot be chained, i.e., if an element with `aria-labelledby` references another element that also has `aria-labelledby`, the `aria-labelledby` attribute on the referenced element will be ignored.
2. If an element is referenced by `aria-labelledby` more than one time during a name calculation, the second and any subsequent references will be ignored.
3. There are certain types of elements, such as paragraphs and list items, that should not be named with `aria-labelledby`.
   They are identified in the table in the [Accessible Name Guidance by Role](#naming_role_guidance) section.
4. If `aria-labelledby` is applied to an element with one of the roles that supports [naming from child content](#naming_with_child_content), content contained in the element and its descendants is hidden from assistive technology users unless it is also referenced by `aria-labelledby`.
   It is strongly recommended to avoid using this attribute to override content of one of these elements except in rare circumstances where hiding content from assistive technology users is beneficial.
5. Because calculating the name of an element with `aria-labelledby` can be complex and reference hidden content, testing with assistive technologies to ensure the expected name is presented to users is particularly important.

### Naming Form Controls with the Label Element

The HTML `label` element enables authors to identify content that serves as a label and associate it with a form control.
When a `label` element is associated with a form control, browsers calculate an accessible name for the form control from the `label` content.
For example, text displayed adjacent to a checkbox may be visually associated with the checkbox, so it is understood as the checkbox label by users who can perceive that visual association.
However, unless the text is programmatically associated with the checkbox, assistive technology users will experience a checkbox without a label.

HTML provides two ways of associating a label with a form control.
The one that provides the broadest browser and assistive technology support is to set the `for` attribute on the `label` element to the `id` of the control.
This way of associating the label with the control is often called explicit association.

```
<input type="checkbox" name="subscribe" id="subscribe_checkbox">
<label for="subscribe_checkbox">subscribe to our newsletter</label>
```

The other way, which is known as implicit association, is to wrap the checkbox and the labeling text in a `label` element.
Some combinations of assistive technologies and browsers fail to treat the element as having an accessible name that is specified by using implicit association.

```
<label>
<input type="checkbox" name="subscribe">
subscribe to our newsletter
</label>
```

Using the `label` element is an effective technique for satisfying [Rule 2: Prefer Visible Text](#naming_rule_visible_text).
It also satisfies [Rule 3: Prefer Native Techniques](#naming_rule_native_techniques).
Native HTML labels offer an important usability and accessibility advantage over ARIA labeling techniques: browsers automatically make clicking the label equivalent to clicking the form control.
This increases the hit area of the form control.

### Naming Fieldsets with the Legend Element

The HTML `fieldset` element can be used to group form controls, and the `legend` element can be used to give the group a name.
For example, a group of radio buttons can be grouped together in a `fieldset`, where the `legend` element labels the group for the radio buttons.

```
<fieldset>
  <legend>Select your starter class</legend>
  <label><input type="radio" name="starter-class" value="green">Green</label>
  <label><input type="radio" name="starter-class" value="red">Red</label>
  <label><input type="radio" name="starter-class" value="blue">Blue</label>
</fieldset>
```

This grouping technique is particularly useful for presenting multiple choice questions.
It enables authors to associate a question with a group of answers.
If a question is not programmatically associated with its answer options, assistive technology users may access the answers without being aware of the question.

Similar benefits can be gained from grouping and naming other types of related form fields using `fieldset` and `legend`.

```
<fieldset>
  <legend>Shipping address</legend>
  <p><label>Full name <input name="name" required></label></p>
  <p><label>Address line 1 <input name="address-1" required></label></p>
  <p><label>Address line 2 <input name="address-2"></label></p>
  ...
</fieldset>
<fieldset>
  <legend>Billing address</legend>
  ...
</fieldset>
```

Using the `legend` element to name a `fieldset` element satisfies [Rule 2: Prefer Visible Text](#naming_rule_visible_text) and [Rule 3: Prefer Native Techniques](#naming_rule_native_techniques).

### Naming Tables and Figures with Captions

The accessible name for HTML `table` and `figure` elements can be derived from a child `caption` or `figcaption` element, respectively.
Tables and figures often have a caption to explain what they are about, how to read them, and sometimes giving them numbers used to refer to them in surrounding prose.
Captions can help all users better understand content, but are especially helpful to users of assistive technologies.

In HTML, the `table` element marks up a data table, and can be provided with a caption using the `caption` element.
If the `table` element does not have `aria-label` or `aria-labelledby`, then the `caption` will be used as the accessible name.
For example, the accessible name of the following table is "Special opening hours".

```
<table>
  <caption>Special opening hours</caption>
  <tr><td>30 May</td><td>Closed</td></tr>
  <tr><td>6 June</td><td>11:00-16:00</td></tr>
</table>
```

The following example gives the table a number ("Table 1") so it can be referenced.

```
<table>
  <caption>Table 1. Traditional dietary intake of Okinawans and other Japanese circa 1950</caption>
  <thead>
    <tr>
      <th></th>
      <th>Okinawa, 1949</th>
      <th>Japan, 1950</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Total calories</th>
      <td>1785</td>
      <td>2068</td>

      [...]

</table>
```

Note: Above table content is from [Caloric restriction, the traditional Okinawan diet, and healthy aging: the diet of the world's longest-lived people and its potential impact on morbidity and life span](https://www.ncbi.nlm.nih.gov/pubmed/17986602).

If a `table` is named using `aria-label` or `aria-labelledby`, then a `caption` element, if present, will become an accessible description.
For an example, see [Describing Tables and Figures with Captions](#describing_with_captions).

Similarly, an HTML `figure` element can be given a caption using the `figcaption` element.
The caption can appear before or after the figure, but it is more common for figures to have the caption after.

```
<figure>
  <img alt="Painting of a person walking in a desert." src="Hole_JesusalDesierto.jpg">
  <figcaption>Jesus entering the desert as imagined by William Hole, 1908</figcaption>
</figure>
```

Like with `table` elements, if a `figure` is not named using `aria-label` or `aria-labelledby`, the content of the `figcaption` element will be used as the accessible name.
However unlike `table` elements, if the `figcaption` element is not used for the name, it does not become an accessible description unless it is referenced by `aria-describedby`.
Nevertheless, assistive technologies will render the content of a `figcaption` regardless of whether it is used as a name, description, or neither.

Using the `caption` element to name a `table` element, or a `figcaption` element to name a `figure` element, satisfies [Rule 2: Prefer Visible Text](#naming_rule_visible_text) and [Rule 3: Prefer Native Techniques](#naming_rule_native_techniques).

### Fallback Names Derived from Titles and Placeholders

When an accessible name is not provided using one of the primary techniques (e.g., the `aria-label` or `aria-labelledby` attributes), or native markup techniques (e.g., the HTML `label` element, or the `alt` attribute of the HTML `img` element), browsers calculate an accessible name from other attributes as a fallback mechanism.
Because the attributes used in fallback name calculation are not intended for naming, they typically yield low quality accessible names that are not effective.
So, As advised by [Rule 4: Avoid Browser Fallback](#naming_rule_avoid_fallback), prefer the explicit labeling techniques described above over fallback techniques described in this section.

Any HTML element can have a `title` attribute specified.
The `title` attribute may be used as the element's fallback accessible name.
The `title` attribute is commonly presented visually as a tooltip when the user hovers over the element with a pointing device, which is not particularly discoverable, and is also not accessible to visual users without a pointing device.

For example, a `fieldset` element without a `legend` element child, but with a `title` attribute, gets its accessible name from the `title` attribute.

```
<fieldset title="Select your starter class">
  <label><input type="radio" name="starter-class" value="green">Green</label>
  <label><input type="radio" name="starter-class" value="red">Red</label>
  <label><input type="radio" name="starter-class" value="blue">Blue</label>
</fieldset>
```

For the HTML `input` and `textarea` elements, the `placeholder` attribute is used as a fallback labeling mechanism if nothing else (including the `title` attribute) results in a label.
It is better to use a `label` element, since it does not disappear visually when the user focuses the form control.

```
<!-- Using a <label> is recommended -->
<label>Search <input type=search name=q></label>

<!-- A placeholder is used as fallback -->
<input type=search name=q placeholder="Search">
```

## Composing Effective and User-friendly Accessible Names

For assistive technology users, especially screen reader users, the quality of accessible names is one of the most significant contributors to usability.
Names that do not provide enough information reduce users' effectiveness while names that are too long reduce efficiency.
And, names that are difficult to understand reduce effectiveness, efficiency, and enjoyment.

The following guidelines provide a starting point for crafting user friendly names.

- Convey function or purpose, not form.
  For example, if an icon that looks like the letter "X" closes a dialog, name it "Close", not "X".
  Similarly, if a set of navigation links in the left side bar navigate among the product pages in a shopping site, name the navigation region "Product", not "Left".
- Put the most distinguishing and important words first.
  Often, for interactive elements that perform an action, this means a verb is the first word.
  For instance, if a list of contacts displays "Edit", "Delete", and "Actions" buttons for each contact, then "Edit John Doe", "Delete John Doe", and "Actions for John Doe" would be better accessible names than "John Doe edit", "John Doe delete", and "John Doe actions".
  By placing the verb first in the name, screen reader users can more easily and quickly distinguish the buttons from one another as well as from the element that opens the contact card for John Doe.
- Be concise.
  For many elements, one to three words is sufficient.
  Only add more words when necessary.
- Do NOT include a WAI-ARIA role name in the accessible name.
  For example, do not include the word "button" in the name of a button, the word "image" in the name of an image, or the word "navigation" in the name of a navigation region.
  Doing so would create duplicate screen reader output since screen readers convey the role of an element in addition to its name.
- Create unique names for elements with the same role unless the elements are actually identical.
  For example, ensure every link on a page has a different name except in cases where multiple links reference the same location.
  Similarly, give every navigation region on a page a different name unless there are regions with identical content that performs identical navigation functions.
- Start names with a capital letter; it helps some screen readers speak them with appropriate inflection.
  Do not end names with a period; they are not sentences.

## Accessible Name Guidance by Role

Certain elements always require a name, others may usually or sometimes require a name, and still others should never be named.
The table below lists all ARIA roles and provides the following information for each:

Necessity of Naming
:   Indicates how necessary it is for authors to add a naming attribute or element to supplement or override the content of an element with the specified role.
    This column may include one of the following values:

    - Required **Only If** Content Insufficient: An element with this role is named by its descendant content.
      If `aria-label` or `aria-labelledby` is applied, content contained in the element and its descendants is hidden from assistive technology users unless it is also referenced by `aria-labelledby`.
      Avoid hiding descendant content except in the rare circumstances where doing so benefits assistive technology users.
    - Required: The ARIA specification requires authors to provide a name; a missing name causes accessibility validators to report an error.
    - Recommended: Providing a name is strongly recommended.
    - Discretionary: Naming is either optional or, in the circumstances described in the guidance column, is discouraged.
    - Do Not Name: Naming is strongly discouraged even if it is technically permitted; often assistive technologies do not render a name even if provided.
    - Prohibited: The ARIA specification does not permit the element to be named; If a name is specified, accessibility validators will report an error.

Guidance:
:   Provides information to help determine if providing a name is beneficial, and if so, describes any recommended techniques.

| role | Necessity of Naming | Guidance |
| --- | --- | --- |
| [`alert`](https://w3c.github.io/aria/#alert) | Discretionary | Some screen readers announce the name of an alert before announcing the content of the alert. Thus, `aria-label` provides a method for prefacing the visible content of an alert with text that is not displayed as part of the alert. Using `aria-label` is functionally equivalent to providing off-screen text in the contents of the alert, except off-screen text would be announced by screen readers that do not support `aria-label` on `alert` elements. |
| [`alertdialog`](https://w3c.github.io/aria/#alertdialog) | Required | Use `aria-labelledby` if a visible label is present, otherwise use `aria-label`. |
| [`application`](https://w3c.github.io/aria/#application) | Required | Use `aria-labelledby` if a visible label is present, otherwise use `aria-label`. |
| [`article`](https://w3c.github.io/aria/#article) | Recommended | - Recommended to distinguish articles from one another; helps users when navigating among articles. - Use `aria-labelledby` if a visible label is present, otherwise use `aria-label`. |
| [`banner`](https://w3c.github.io/aria/#banner) | Discretionary | - Necessary in the uncommon circumstance where two banner landmark regions are present on the same page.   It is otherwise optional. - Named using `aria-labelledby` if a visible label is present, otherwise with `aria-label`. - See the [Banner Landmark](../landmark-regions/#aria_lh_banner) section. |
| [`blockquote`](https://w3c.github.io/aria/#blockquote) | Discretionary | If a visible label is present, associating it with the blockquote by using `aria-labelledby` could benefit some assistive technology users. |
| [`button`](https://w3c.github.io/aria/#button) | Required **Only If** Content Insufficient | - Warning! Using `aria-label` or `aria-labelledby` will hide descendant content from assistive technologies. - Ideally named by visible, descendant content. |
| [`caption`](https://w3c.github.io/aria/#caption) | Prohibited |  |
| [`cell`](https://w3c.github.io/aria/#cell) | Required **Only If** Content Insufficient | - Warning! Using `aria-label` or `aria-labelledby` will hide descendant content from assistive technologies. - Ideally named by visible, descendant content. - Note that a name is not required; assistive technologies expect an empty cell in a table to be represented by an empty name. - Note that associated row or column headers do not name a `cell`; the name of a cell in a table is its content.   Headers are complementary information. |
| [`checkbox`](https://w3c.github.io/aria/#checkbox) | Required **Only If** Content Insufficient | - Warning! Using `aria-label` or `aria-labelledby` will hide any descendant content from assistive technologies. - If based on HTML `type="checkbox"`, use a `label` element. - Otherwise, reference visible content via `aria-labelledby`. |
| [`code`](https://w3c.github.io/aria/#code) | Prohibited |  |
| [`columnheader`](https://w3c.github.io/aria/#columnheader) | Required **Only If** Content Insufficient | - Warning! Using `aria-label` or `aria-labelledby` will hide descendant content from assistive technologies. - Ideally named by visible, descendant content. - If the `columnheader` role is implied from an HTML `th`, the HTML `abbr` attribute can be used to specify an abbreviated version of the name that is only announced when screen readers are reading an associated `cell` within the `table`, `grid`, or `treegrid`. |
| [`combobox`](https://w3c.github.io/aria/#combobox) | Required | - If the `combobox` role is applied to an HTML `select` or `input` element, can be named with an HTML `label` element. - Otherwise use `aria-labelledby` if a visible label is present. - Use `aria-label` if a visible label is not present. |
| [`complementary`](https://w3c.github.io/aria/#complementary) | Recommended | - Naming is necessary when two complementary landmark regions are present on the same page. - Naming is recommended even when one complementary region is present to help users understand the purpose of the region's content when navigating among landmark regions. - Use `aria-labelledby` if a visible label is present, otherwise use `aria-label`. - See the [Complementary Landmark](../landmark-regions/#aria_lh_complementary) section. |
| [`contentinfo`](https://w3c.github.io/aria/#contentinfo) | Discretionary | - Necessary in the uncommon circumstance where two contentinfo landmark regions are present on the same page.   It is otherwise optional. - Named using `aria-labelledby` if a visible label is present, otherwise with `aria-label`. |
| [`definition`](https://w3c.github.io/aria/#definition) | Recommended | Reference the term being defined with `role="term"`, using `aria-labelledby`. |
| [`deletion`](https://w3c.github.io/aria/#deletion) | Prohibited |  |
| [`dialog`](https://w3c.github.io/aria/#dialog) | Required | Use `aria-labelledby` if a visible label is present, otherwise use `aria-label`. |
| [`directory`](https://w3c.github.io/aria/#directory) | Discretionary | - Naming can help users understand the purpose of the directory. - Use `aria-labelledby` if a visible label is present, otherwise use `aria-label`. |
| [`document`](https://w3c.github.io/aria/#document) | Discretionary | Elements with the `document` role are contained within an element with the `application` role, which is required to have a name. Typically, the name of the `application` element will provide sufficient context and identity for the `document` element. Because the `application` element is used only to create unusual, custom widgets, careful assessment is necessary to determine whether or not adding an accessible name is beneficial. |
| [`emphasis`](https://w3c.github.io/aria/#emphasis) | Prohibited |  |
| [`feed`](https://w3c.github.io/aria/#feed) | Recommended | - Helps screen reader users understand the context and purpose of the feed. - Use `aria-labelledby` if a visible label is present, otherwise use `aria-label`. - See the [Feed Pattern](../../patterns/feed/). |
| [`figure`](https://w3c.github.io/aria/#figure) | Recommended | - For HTML, use the `figure` and `figcaption` elements.   The `figcaption` will serve as the accessible name for the `figure`.   See the [Naming Tables and Figures with Captions](#naming_with_captions) section. - When not using HTML, or when retrofitting legacy HTML, use the `aria-labelledby` on the figure, pointing to the figure's caption. - If there is no visible caption, `aria-label` can be used. |
| [`form`](https://w3c.github.io/aria/#form) | Recommended | - Helps screen reader users understand the context and purpose of the form landmark. - Use `aria-labelledby` if a visible label is present, otherwise use `aria-label`. - See the [Form Landmark](../landmark-regions/#aria_lh_form) section. |
| [`generic`](https://w3c.github.io/aria/#generic) | Prohibited |  |
| [`grid`](https://w3c.github.io/aria/#grid) | Required | - If the `grid` is applied to an HTML `table` element, then the accessible name can be derived from the table's `caption` element. - Otherwise, use `aria-labelledby` if a visible label is present, otherwise use `aria-label`. |
| [`gridcell`](https://w3c.github.io/aria/#gridcell) | Required **Only If** Content Insufficient | - Warning! Using `aria-label` or `aria-labelledby` will hide descendant content from assistive technologies. - Ideally named by visible, descendant content. - Note that a name is not required; assistive technologies expect an empty cell in a grid to be represented by an empty name. - Note that associated row or column headers do not name a `gridcell`; the name of a cell in a grid is its content.   Headers are complementary information. |
| [`group`](https://w3c.github.io/aria/#group) | Discretionary | - When using the HTML `fieldset` element, the accessible name can be derived from the `legend` element. - When using the HTML `details` element, do not provide an accessible name for this element.   The user interacts with the `summary` element, and that can derive its accessible name from its contents. - When using the HTML `optgroup` element, use the `label` attribute. - Otherwise, use `aria-labelledby` if a visible label is present, otherwise use `aria-label`. |
| [`heading`](https://w3c.github.io/aria/#heading) | Required **Only If** Content Insufficient | - Warning! Using `aria-label` or `aria-labelledby` will hide descendant content from assistive technologies. - Ideally named by visible, descendant content. |
| [`insertion`](https://w3c.github.io/aria/#insertion) | Prohibited |  |
| [`img`](https://w3c.github.io/aria/#img) | Required | For the HTML `img` element, use the `alt` attribute. For other elements with the `img` role, use `aria-labelledby` or `aria-label`. |
| [`link`](https://w3c.github.io/aria/#link) | Required **Only If** Content Insufficient | - Warning! Using `aria-label` or `aria-labelledby` will hide descendant content from assistive technologies. - Ideally named by visible, descendant content. |
| [`list`](https://w3c.github.io/aria/#list) | Discretionary | - Potentially beneficial for users of screen readers that support both list names and navigation among lists on a page. - Potentially a source of distracting or undesirable screen reader verbosity, especially if nested within a named container, such as a navigation region. - Can be named using `aria-labelledby` if a visible label is present, otherwise with `aria-label`. |
| [`listbox`](https://w3c.github.io/aria/#listbox) | Required | - If the `listbox` role is applied to an HTML `select` element (with the `multiple` attribute or a `size` attribute having a value greater than 1), can be named with an HTML `label` element. - Otherwise use `aria-labelledby` if a visible label is present. - Use `aria-label` if a visible label is not present. - See the [Listbox Pattern](../../patterns/listbox/). |
| [`listitem`](https://w3c.github.io/aria/#listitem) | Do Not Name | Naming is not supported by assistive technologies; it is necessary to include relevant content within the list item. |
| [`log`](https://w3c.github.io/aria/#log) | Discretionary | Some screen readers announce the name of a log element before announcing the content of the log element. Thus, `aria-label` provides a method for prefacing the visible content of a log element with text that is not displayed as part of the log element. Using `aria-label` is functionally equivalent to providing off-screen text in the contents of the log element, except off-screen text would be announced by screen readers that do not support `aria-label` on `log` elements. |
| [`mark`](https://w3c.github.io/aria/#mark) | Prohibited |  |
| [`main`](https://w3c.github.io/aria/#main) | Discretionary | - Potentially helpful for orienting assistive technology users, especially in single-page applications where main content changes happen without generating a page load event. - Can be named using `aria-labelledby` if a visible label is present, otherwise with `aria-label`. - See the [Main Landmark](../landmark-regions/#aria_lh_main) section. |
| [`marquee`](https://w3c.github.io/aria/#marquee) | Discretionary | Use `aria-labelledby` if a visible label is present, otherwise use `aria-label`. |
| [`math`](https://w3c.github.io/aria/#math) | Recommended | - If the `math` element has only presentational children and the accessible name is intended to convey the mathematical expression, use `aria-label` to provide a string that represents the expression. - If the `math` element contains navigable content that conveys the mathematical expression and a visible label for the expression is present, use `aria-labelledby`. - Otherwise, use a`aria-label` to name the expression, e.g., `aria-label="Pythagorean Theorem"`. |
| [`menu`](https://w3c.github.io/aria/#menu) | Recommended | - Use `aria-labelledby` to refer to the menuitem or button that controls this element's display. - Otherwise, use `aria-label`. - See the [Menu and Menubar Pattern](../../patterns/menubar/). |
| [`menubar`](https://w3c.github.io/aria/#menubar) | Recommended | - Helps screen reader users understand the context and purpose of `menuitem` elements in a `menubar`.   Naming a `menubar` is comparable to naming a menu button.   The name of a `button` that opens a `menu` conveys the purpose of the menu it opens.   Since a `menubar` element is displayed persistently, a name on the `menubar` can serve that same purpose. - Use `aria-labelledby` if a visible label is present, otherwise use `aria-label`. - See the [Menu and Menubar Pattern](../../patterns/menubar/). |
| [`menuitem`](https://w3c.github.io/aria/#menuitem) | Required **Only If** Content Insufficient | - Warning! Using `aria-label` or `aria-labelledby` will hide any descendant content from assistive technologies. - Ideally named by visible, descendant content. - Note: content contained within a child `menu` is automatically excluded from the accessible name calculation. - See the [Menu and Menubar Pattern](../../patterns/menubar/). |
| [`menuitemcheckbox`](https://w3c.github.io/aria/#menuitemcheckbox) | Required **Only If** Content Insufficient | - Warning! Using `aria-label` or `aria-labelledby` will hide any descendant content from assistive technologies. - Ideally named by visible, descendant content. - See the [Menu and Menubar Pattern](../../patterns/menubar/). |
| [`menuitemradio`](https://w3c.github.io/aria/#menuitemradio) | Required **Only If** Content Insufficient | - Warning! Using `aria-label` or `aria-labelledby` will hide any descendant content from assistive technologies. - Ideally named by visible, descendant content. - See the [Menu and Menubar Pattern](../../patterns/menubar/). |
| [`meter`](https://w3c.github.io/aria/#meter) | Required | - If based on an HTML `meter` element, can be named with an HTML `label` element. - Otherwise use `aria-labelledby` if a visible label is present. - Use `aria-label` if a visible label is not present. |
| [`navigation`](https://w3c.github.io/aria/#navigation) | Recommended | - Helps screen reader users understand the context and purpose of the navigation landmark. - Use `aria-labelledby` if a visible label is present, otherwise use `aria-label`. - See the [Navigation Landmark](../landmark-regions/#aria_lh_navigation) section. |
| [`none`](https://w3c.github.io/aria/#none) | Prohibited | An element with `role="none"` is not part of the accessibility tree (except in error cases). Do not use `aria-labelledby` or `aria-label`. |
| [`note`](https://w3c.github.io/aria/#note) | Discretionary | - Naming is optional, but can help screen reader users understand the context and purpose of the note. - Named using `aria-labelledby` if a visible label is present, otherwise with `aria-label`. |
| [`option`](https://w3c.github.io/aria/#option) | Required **Only If** Content Insufficient | - Warning! Using `aria-label` or `aria-labelledby` will hide any descendant content from assistive technologies. - Ideally named by visible, descendant content. - See the [Combobox Pattern](../../patterns/combobox/). |
| [`paragraph`](https://w3c.github.io/aria/#paragraph) | Prohibited |  |
| [`presentation`](https://w3c.github.io/aria/#presentation) | Prohibited | An element with `role="presentation"` is not part of the accessibility tree (except in error cases). Do not use `aria-labelledby` or `aria-label`. |
| [`progressbar`](https://w3c.github.io/aria/#progressbar) | Required | - If the `progressbar` role is applied to an HTML `progress` element, can be named with an HTML `label` element. - Otherwise use `aria-labelledby` if a visible label is present. - Use `aria-label` if a visible label is not present. |
| [`radio`](https://w3c.github.io/aria/#radio) | Required **Only If** Content Insufficient | - Warning! Using `aria-label` or `aria-labelledby` will hide any descendant content from assistive technologies. - If based on HTML `type="checkbox"`, use a `label` element. - Otherwise, reference visible content via `aria-labelledby`. |
| [`radiogroup`](https://w3c.github.io/aria/#radiogroup) | Required | - Recommended to help assistive technology users understand the purpose of the group of `radio` buttons. - Use `aria-labelledby` if a visible label is present, otherwise use `aria-label`. - See the [Radio Group Pattern](../../patterns/radio/). |
| [`region`](https://w3c.github.io/aria/#region) | Required | - Helps screen reader users understand the context and purpose of the landmark. - Use `aria-labelledby` if a visible label is present, otherwise use `aria-label`. - See the [Region Landmark](../landmark-regions/#aria_lh_region) section. |
| [`row`](https://w3c.github.io/aria/#row) | Required **Only If** Content Insufficient **AND** descendant of a `treegrid` **AND** the row is focusable | When `row` elements are focusable in a [treegrid](../../patterns/treegrid/), screen readers announce the entire contents of a row when navigating by row. This is typically the most appropriate behavior. However, in some circumstances, it could be beneficial to change the order in which cells are announced or exclude announcement of certain cells by using `aria-labelledby` to specify which cells to announce. |
| [`rowgroup`](https://w3c.github.io/aria/#rowgroup) | Do Not Name | Naming is not supported by assistive technologies. |
| [`rowheader`](https://w3c.github.io/aria/#rowheader) | Required **Only If** Content Insufficient | - Warning! Using `aria-label` or `aria-labelledby` will hide descendant content from assistive technologies. - Ideally named by visible, descendant content. - If the `rowheader` role is implied from an HTML `th`, the HTML `abbr` attribute can be used to specify an abbreviated version of the name that is only announced when screen readers are reading an associated `cell` within the `table`, `grid`, or `treegrid`. |
| [`scrollbar`](https://w3c.github.io/aria/#scrollbar) | Discretionary | - Naming is optional, but can potentially help screen reader users understand the purpose of the scrollbar.   The purpose is also conveyed using the `aria-controls` attribute, which is required for `scrollbar`. - Named using `aria-labelledby` if a visible label is present, otherwise with `aria-label`. |
| [`search`](https://w3c.github.io/aria/#search) | Recommended | - Helps screen reader users understand the context and purpose of the search landmark. - Named using `aria-labelledby` if a visible label is present, otherwise with `aria-label`. - See the [Search Landmark](../landmark-regions/#aria_lh_search) section. |
| [`searchbox`](https://w3c.github.io/aria/#searchbox) | Required | - If the `searchbox` role is applied to an HTML `input` element, can be named with an HTML `label` element. - Otherwise use `aria-labelledby` if a visible label is present. - Use `aria-label` if a visible label is not present. |
| [`separator`](https://w3c.github.io/aria/#separator) | Discretionary | - Recommended if there is more than one focusable `separator` element on the page. - Can help assistive technology users understand the purpose of the separator. - Named using `aria-labelledby` if a visible label is present, otherwise with `aria-label`. |
| [`slider`](https://w3c.github.io/aria/#slider) | Required | - If the `slider` role is applied to an HTML `input` element, can be named with an HTML `label` element. - Otherwise use `aria-labelledby` if a visible label is present. - Use `aria-label` if a visible label is not present. - See the [Slider Pattern](../../patterns/slider/) and the [Slider (Multi-Thumb) Pattern](../../patterns/slider-multithumb/). |
| [`spinbutton`](https://w3c.github.io/aria/#spinbutton) | Required | - If the `textbox` role is applied to an HTML `input` element, can be named with an HTML `label` element. - Otherwise use `aria-labelledby` if a visible label is present. - Use `aria-label` if a visible label is not present. - See the [Spinbutton Pattern](../../patterns/spinbutton/). |
| [`status`](https://w3c.github.io/aria/#status) | Discretionary | Some screen readers announce the name of a status element before announcing the content of the status element. Thus, `aria-label` provides a method for prefacing the visible content of a status element with text that is not displayed as part of the status element. Using `aria-label` is functionally equivalent to providing off-screen text in the contents of the status element, except off-screen text would be announced by screen readers that do not support `aria-label` on `status` elements. |
| [`strong`](https://w3c.github.io/aria/#strong) | Prohibited |  |
| [`subscript`](https://w3c.github.io/aria/#subscript) | Prohibited |  |
| [`superscript`](https://w3c.github.io/aria/#superscript) | Prohibited |  |
| [`switch`](https://w3c.github.io/aria/#switch) | Required **Only If** Content Insufficient | - Warning! Using `aria-label` or `aria-labelledby` will hide any descendant content from assistive technologies. - If based on HTML `type="checkbox"`, use a `label` element. - Otherwise, reference visible content via `aria-labelledby`. |
| [`tab`](https://w3c.github.io/aria/#tab) | Required **Only If** Content Insufficient | - Warning! Using `aria-label` or `aria-labelledby` will hide descendant content from assistive technologies. - Ideally named by visible, descendant content. |
| [`table`](https://w3c.github.io/aria/#table) | Required | - If using HTML `table` element, use the `caption` element. - Otherwise use `aria-labelledby` if a visible label is present. - Use `aria-label` if a visible label is not present. - See the [Table Pattern](../../patterns/table/). |
| [`tablist`](https://w3c.github.io/aria/#tablist) | Recommended | - Helps screen reader users understand the context and purpose of the tablist. - Use `aria-labelledby` if a visible label is present, otherwise use `aria-label`. - See the [Carousel Pattern](../../patterns/carousel/) and [Tabs Pattern](../../patterns/tabs/). |
| [`tabpanel`](https://w3c.github.io/aria/#tabpanel) | Required | - Use `aria-labelledby` pointing to the `tab` element that controls the `tabpanel`. - See the [Carousel Pattern](../../patterns/carousel/) and [Tabs Pattern](../../patterns/tabs/). |
| [`term`](https://w3c.github.io/aria/#term) | Do Not Name | Since a term is usually the name for the `role="definition"` element, it could be confusing if the term itself also has a name. |
| [`textbox`](https://w3c.github.io/aria/#textbox) | Required | - If the `textbox` role is applied to an HTML `input` or `textarea` element, can be named with an HTML `label` element. - Otherwise use `aria-labelledby` if a visible label is present. - Use `aria-label` if a visible label is not present. |
| [`time`](https://w3c.github.io/aria/#time) | Do Not Name | Naming is not supported by assistive technologies. |
| [`timer`](https://w3c.github.io/aria/#timer) | Discretionary | Some screen readers announce the name of a timer element before announcing the content of the timer element. Thus, `aria-label` provides a method for prefacing the visible content of a timer element with text that is not displayed as part of the timer element. Using `aria-label` is functionally equivalent to providing off-screen text in the contents of the timer element, except off-screen text would be announced by screen readers that do not support `aria-label` on `timer` elements. |
| [`toolbar`](https://w3c.github.io/aria/#toolbar) | Recommended | - If there is more than one `toolbar` element on the page, naming is required. - Helps assistive technology users to understand the purpose of the toolbar, even when there is only one toolbar on the page. - Use `aria-labelledby` if a visible label is present, otherwise use `aria-label`. - See the [Toolbar Pattern](../../patterns/toolbar/). |
| [`tooltip`](https://w3c.github.io/aria/#tooltip) | Required **Only If** Content Insufficient | - Warning! Using `aria-label` or `aria-labelledby` will hide descendant content from assistive technologies. - Ideally named by visible, descendant content. |
| [`tree`](https://w3c.github.io/aria/#tree) | Required | - Use `aria-labelledby` if a visible label is present, otherwise use `aria-label`. - See the [Tree View Pattern](../../patterns/treeview/). |
| [`treegrid`](https://w3c.github.io/aria/#treegrid) | Required | - If the `treegrid` is applied to an HTML `table` element, then the accessible name can be derived from the table's `caption` element. - Otherwise, use `aria-labelledby` if a visible label is present, otherwise use `aria-label`. - See the [Treegrid Pattern](../../patterns/treegrid/). |
| [`treeitem`](https://w3c.github.io/aria/#treeitem) | Required **Only If** Content Insufficient | - Warning! Using `aria-label` or `aria-labelledby` will hide any descendant content from assistive technologies. - Ideally named by visible, descendant content. - Note: content contained within a child `group` is automatically excluded from the accessible name calculation. - See the [Tree View Pattern](../../patterns/treeview/). |

## Accessible name calculation

User agents construct an accessible name string for an element by walking through a list of potential naming methods and using the first that generates a name.
The algorithm they follow is defined in the [accessible name specification](https://w3c.github.io/accname/).
It is roughly like the following:

1. The `aria-labelledby` property is used if present.
2. If the name is still empty, the `aria-label` property is used if present.
3. If the name is still empty, then host-language-specific attributes or elements are used if present.
   For HTML, these are, depending on the element:

   `input` whose `type` attribute is in the Button, Submit Button, or Reset Button state
   :   The `value` attribute.

   `input` whose `type` attribute is in the Image Button state

   `img`

   `area`
   :   The `alt` attribute.

   `fieldset`
   :   The first child `legend` element.

   Other form elements
   :   The associated `label` element(s).

   `figure`
   :   The first child `figcaption` element.

   `table`
   :   The first child `caption` element.
4. If the name is still empty, then for elements with a role that supports naming from child content, the content of the element is used.
5. Finally, if the name is still empty, then other fallback host-language-specific attributes or elements are used if present.
   For HTML, these are, depending on the element:

   `input` whose `type` attribute is in the Text, Password, Search, Telephone, or URL states

   `textarea`
   :   The `title` attribute.
       Otherwise, the `placeholder` attribute.

   `input` whose `type` attribute is in the Submit Button state
   :   A localized string of the word "submit".

   `input` whose `type` attribute is in the Reset Button state
   :   A localized string of the word "reset".

   `input` whose `type` attribute is in the Image Button state
   :   The `title` attribute.
       Otherwise, a localized string of the phrase "Submit Query".

   `summary`
   :   The word "Details".

   Other elements
   :   The `title` attribute.

The final step is a fallback mechanism.
Generally when labeling an element, use one of the non-fallback mechanisms.

When calculating a name from content, the user agent walks through all descendant nodes except in the cases of `treeitem` and `menuitem` as described below.
And, when following references in an `aria-labelledby` attribute, it similarly walks the tree of each referenced element.
Thus, the naming algorithm is recursive.
The following two sections explain non-recursive and recursive examples of how the algorithm works.

When calculating a name from content for the `treeitem` role, descendant content of child `group` elements are not included.
For example, in the following `tree`, the name of the first tree item is "Fruits"; "Apples", "Bananas", and "Oranges" are automatically omitted.

```
<ul role="tree">
  <li role="treeitem">Fruits
    <ul role="group">
      <li role="treeitem">Apples</li>
      <li role="treeitem">Bananas</li>
      <li role="treeitem">Oranges</li>
    </ul>
  </li>
</ul>
```

Similarly, when calculating a name from content for the `menuitem` role, descendant content of child `menu` elements are not included.
So, the name of the first parent `menuitem` in the following `menu` is "Fruits".

```
<ul role="menu">
  <li role="menuitem">Fruits
    <ul role="menu">
      <li role="menuitem">Apples</li>
      <li role="menuitem">Bananas</li>
      <li role="menuitem">Oranges</li>
    </ul>
  </li>
</ul>
```

### Examples of non-recursive accessible name calculation

Consider an `input` element that has no associated `label` element and only a `name` attribute and so does not have an accessible name (do not do this):

```
<input name="code">
```

If there is a `placeholder` attribute, then it serves as a naming fallback mechanism (avoid doing this):

```
<input name="code"
  placeholder="One-time code">
```

If there is also a `title` attribute, then it is used as the accessible name instead of `placeholder`, but it is still a fallback (avoid doing this):

```
<input name="code"
  placeholder="123456"
  title="One-time code">
```

If there is also a `label` element (recommended), then that is used as the accessible name, and the `title` attribute is instead used as the accessible description:

```
<label>One-time code
  <input name="code"
    placeholder="123456"
    title="Get your code from the app.">
</label>
```

If there is also an `aria-label` attribute (not recommended unless it adds clarity for assistive technology users), then that becomes the accessible name, overriding the `label` element:

```
<label>Code
  <input name="code"
    aria-label="One-time code"
    placeholder="123456"
    title="Get your code from the app.">
</label>
```

If there is also an `aria-labelledby` attribute, that wins over the other elements and attributes (the `aria-label` attribute ought to be removed if it is not used):

```
<p>Please fill in your <span id="code-label">one-time code</span> to log in.</p>
<p>
  <label>Code
    <input name="code"
    aria-labelledby="code-label"
    aria-label="This is ignored"
    placeholder="123456"
    title="Get your code from the app.">
  </label>
</p>
```

### Examples of recursive accessible name calculation

The accessible name calculation algorithm will be invoked recursively when necessary.
An `aria-labelledby` reference causes the algorithm to be invoked recursively, and when computing an accessible name from content the algorithm is invoked recursively for each child node.

In this example, the label for the button is computed by recursing into each child node, resulting in "Move to trash".

```
<button>Move to <img src="bin.svg" alt="trash"></button>
```

When following an `aria-labelledby` reference, the algorithm avoids following the same reference twice to avoid infinite loops.

In this example, the label for the button is computed by first following the `aria-labelledby` reference to the parent element, and then computing the label for that element from the child nodes, first visiting the `button` element again but ignoring the `aria-labelledby` reference and instead using the `aria-label`, and then visiting the next child (the text node).
The resulting label is "Remove meeting: Daily status report".

```
<div id="meeting-1">
  <button aria-labelledby="meeting-1" aria-label="Remove meeting:">X</button>
  Daily status report
</div>
```

## Describing Techniques

### Describing by referencing content with `aria-describedby`

The `aria-describedby` property works similarly to the `aria-labelledby` property.
For example, a button could be described by a sibling paragraph.

```
<button aria-describedby="trash-desc">Move to trash</button>
...
<p id="trash-desc">Items in the trash will be permanently removed after 30 days.</p>
```

Descriptions are reduced to text strings.
For example, if the description contains an HTML `img` element, a text equivalent of the image is computed.

```
<button aria-describedby="trash-desc">Move to <img src="bin.svg" alt="trash"></button>
...
<p id="trash-desc">Items in <img src="bin.svg" alt="the trash"> will be permanently removed after 30 days.</p>
```

As with `aria-labelledby`, it is possible to reference an element using `aria-describedby` even if that element is hidden.
For example, a text field in a form could have a description that is hidden by default, but can be revealed on request using a disclosure widget.
The description could also be referenced from the text field directly with `aria-describedby`.
In the following example, the accessible description for the `input` element is "Your username is the name that you use to log in to this service."

```
<label for="username">Username</label>
<input id="username" name="username" aria-describedby="username-desc">
<button aria-expanded="false" aria-controls="username-desc" aria-label="Help about username">?</button>
<p id="username-desc" hidden>
  Your username is the name that you use to log in to this service.
</p>
```

### Describing Tables and Figures with Captions

In HTML, if the `table` is named using `aria-label` or `aria-labelledby`, a child `caption` element becomes an accessible description.
For example, a preceding heading might serve as an appropriate accessible name, and the `caption` element might contain a longer description.
In such a situation, `aria-labelledby` could be used on the `table` to set the accessible name to the heading content and the `caption` would become the accessible description.

```
<h2 id="events-heading">Upcoming events</h2>
<table aria-labelledby="events-heading">
  <caption>
    Calendar of upcoming events, weeks 27 through 31, with each week starting with
    Monday. The first column is the week number.
  </caption>
  <tr><th>Week</th><th>Monday</th><th>Tuesday</th><th>Wednesday</th><th>Thursday</th><th>Friday</th><th>Saturday</th><th>Sunday</th></tr>
  <tr><td>27</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
  <tr><td>28</td><td></td><td></td><td></td><td></td><td></td><td></td><td><a href="/events/9856">Crown Princess's birthday</a></td></tr>
  <tr><td>29</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
  <tr><td>30</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
  <tr><td>31</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
</table>
```

The HTML `figure` element can get its accessible *name* from its `figcaption` element, but it will not be used as the accessible *description*, even if it was not used as the accessible name.
If the `figcaption` element is appropriate as an accessible description, and the accessible name is set using `aria-labelledby` or `aria-label`, then the `figcaption` can be explicitly set as the accessible description using the `aria-describedby` attribute.

```
<h2 id="neutron">Neutron</h2>
<figure aria-labelledby="neutron" aria-describedby="neutron-caption">
  <img src="neutron.svg" alt="Within the neutron are three quarks (blue 'u', red 'd', green 'd') that are interconnected.">
  <figcaption id="neutron-caption">
    The quark content of the neutron. The color assignment of individual quarks is
    arbitrary, but all three colors must be present. Forces between quarks are
    mediated by gluons.
  </figcaption>
</figure>
```

### Descriptions Derived from Titles

If an accessible description was not provided using the `aria-describedby` attribute or one of the primary host-language-specific attributes or elements (e.g., the `caption` element for `table`), then, for HTML, if the element has a `title` attribute, that is used as the accessible description.

A visible description together with `aria-describedby` is generally recommended.
If a description that is not visible is desired, then the `title` attribute can be used, for any HTML element that can have an accessible description.

Note that the `title` attribute might not be accessible to some users, in particular sighted users not using a screen reader and not using a pointing device that supports hover (e.g., a mouse).

For example, an `input` element with input constrained using the `pattern` attribute can use the `title` attribute to describe what the expected input is.

```
<label> Part number:
  <input pattern="[0-9][A-Z]{3}" name="part"
    title="A part number is a digit followed by three uppercase letters."/>
</label>
```

The `title` attribute in this case can be shown to the user as a tooltip when the user hovers or focuses the control, but also as part of the error message when the user agent validates the form, if the `input` element's value doesn't match the `pattern`.

As another example, a link can use the `title` attribute to describe the link in more detail.

```
<a href="http://twitter.com/W3C"
  title="Follow W3C on Twitter">
  <img src="/2008/site/images/Twitter_bird_logo_2012.svg"
    alt="Twitter" class="social-icon" height="40" />
</a>
```

## Accessible description calculation

Like the [accessible name calculation](#name_calculation), the accessible description calculation produces a text string.

The accessible description calculation algorithm is the same as the accessible name calculation algorithm except for a few branch points that depend on whether a name or description is being calculated.
In particular, when accumulating text for an accessible description, the algorithm uses `aria-describedby` instead of `aria-labelledby`.

User agents construct an accessible description string for an element by walking through a list of potential description methods and using the first that generates a description.
The algorithm they follow is defined in the [accessible name specification](https://w3c.github.io/accname/).
It is roughly like the following:

1. The `aria-describedby` property is used if present.
2. If the description is still empty, then host-language-specific attributes or elements are used if present, if it wasn't already used as the accessible name.
   For HTML, these are, depending on the element:

   `input` whose `type` attribute is in the Button, Submit Button, or Reset Button state
   :   The `value` attribute.

   `summary`
   :   The element's subtree.

   `table`
   :   The first child `caption` element.
3. Finally, if the description is still empty, then other host-language-specific attributes or elements are used if present, if it wasn't already used for the accessible name.
   For HTML, this is the `title` attribute.