# Breadcrumb Pattern | APG | WAI | W3C

Source: https://www.w3.org/WAI/ARIA/apg/patterns/breadcrumb/

---

Breadcrumb Pattern

## About This Pattern

A breadcrumb trail consists of a list of links to the parent pages of the current page in hierarchical order.
It helps users find their place within a website or web application.
Breadcrumbs are often placed horizontally before a page's main content.

![](../../../../content-images/wai-aria-practices/images/pattern-breadcrumb.svg)

## Example

[Breadcrumb design pattern example](examples/breadcrumb/)

## Keyboard Interaction

Not applicable.

## WAI-ARIA Roles, States, and Properties

- Breadcrumb trail is contained within a navigation landmark region.
- The landmark region is labelled via [aria-label](https://w3c.github.io/aria/#aria-label) or [aria-labelledby](https://w3c.github.io/aria/#aria-labelledby).
- The link to the current page has [aria-current](https://w3c.github.io/aria/#aria-current) set to `page`.
  If the element representing the current page is not a link, aria-current is optional.