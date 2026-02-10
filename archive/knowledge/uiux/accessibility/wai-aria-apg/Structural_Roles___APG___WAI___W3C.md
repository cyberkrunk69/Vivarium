# Structural Roles | APG | WAI | W3C

Source: https://www.w3.org/WAI/ARIA/apg/practices/structural-roles/

---

Structural Roles

## Introduction

ARIA provides a set of roles that convey the accessibility semantics of structures on a page.
These roles express the meaning that is conveyed by the layout and appearance of elements that organize and structure content, such as headings, lists, and tables.

Some host languages, such as HTML, include elements that express the same semantics as an ARIA role.
For instance, the HTML `<p>` element is mapped to accessibility APIs in exactly the same way as `<div role="paragraph">`.
The ARIA and HTML specifications refer to this mapping of HTML elements to ARIA attributes as implied semantics, i.e., the implied ARIA role of the HTML `<p>` element is `paragraph`.

## When to Use Structural Roles

When developing HTML, it is important to use native HTML elements where ever possible.
Do not use an ARIA role or property if it is possible to use an HTML element that has equivalent semantics.

Circumstances where it is appropriate to use ARIA attributes instead of equivalent HTML are:

1. When the HTML element cannot be styled in a way that meets visual design requirements.
2. When testing reveals that browsers or assistive technologies provide better support for the ARIA equivalent.
3. When remediating or retrofitting legacy content and altering the underlying DOM to use the HTML would be cost prohibitive.
4. When building a web component to compose a
   [custom element](https://html.spec.whatwg.org/multipage/#custom-elements)
   and the element being extended does not convey the appropriate or sufficient accessibility semantics.

## All Structural Roles and Their HTML Equivalents

The following table lists all structural roles defined in ARIA 1.2.
As described above in the section on [When to Use Structural Roles](#when_to_use_structural_roles), use an equivalent HTML element instead of an ARIA structural role unless the ARIA role does not have an HTML equivalent or one of the four circumstances that makes using ARIA necessary exists.

ARIA structural roles

| ARIA Role | HTML Equivalent |
| --- | --- |
| application | No equivalent element |
| article | article |
| blockquote | blockquote |
| caption | caption |
| cell | td |
| code | code |
| columnheader | th |
| definition | dd |
| deletion | del |
| directory | No equivalent element |
| document | No equivalent element |
| emphasis | em |
| feed | No equivalent element |
| figure | figure |
| generic | div, span |
| group | No equivalent element |
| heading with aria-level="N" where N is 1, 2, 3, 4, 5, or 6 | h1, h2, h3, h4, h5, h6 |
| insertion | ins |
| img | img |
| list | ul, ol |
| listitem | li |
| mark | mark |
| math | No equivalent element |
| none | No equivalent element |
| note | No equivalent element |
| presentation | No equivalent element |
| paragraph | p |
| row | tr |
| rowgroup | tbody, thead, tfoot |
| rowheader | th |
| separator (when not focusable) | hr |
| strong | strong |
| subscript | sub |
| superscript | sup |
| table | table |
| term | dfn |
| time | time |
| toolbar | No equivalent element |
| tooltip | No equivalent element |