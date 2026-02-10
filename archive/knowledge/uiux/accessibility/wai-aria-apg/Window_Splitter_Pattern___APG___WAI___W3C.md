# Window Splitter Pattern | APG | WAI | W3C

Source: https://www.w3.org/WAI/ARIA/apg/patterns/windowsplitter/

---

Window Splitter Pattern

## About This Pattern

**NOTE:** ARIA 1.1 introduced changes to the separator role so it behaves as a widget when focusable.
While this pattern has been revised to match the ARIA 1.1 specification, the task force will not complete its review until a functional example that matches the ARIA 1.1 specification is complete.
Progress on this pattern is tracked by [issue 129.](https://github.com/w3c/aria-practices/issues/129)

A window splitter is a moveable separator between two sections, or panes, of a window that enables users to change the relative size of the panes.
A Window Splitter can be either variable or fixed.
A fixed splitter toggles between two positions whereas a variable splitter can be adjusted to any position within an allowed range.

A window splitter has a value that represents the size of one of the panes, which, in this pattern, is called the primary pane.
When the splitter has its minimum value, the primary pane has its smallest size and the secondary pane has its largest size.
The splitter also has an accessible name that matches the name of the primary pane.

For example, consider a book reading application with a primary pane for the table of contents and a secondary pane that displays content from a section of the book.
The two panes are divided by a vertical splitter labelled "Table of Contents".
When the table of contents pane has its maximum size, the splitter has a value of `100`, and when the table of contents is completely collapsed, the splitter has a value of `0`.

Note that the term "primary pane" does not describe the importance or purpose of content inside the pane.

![](../../../../content-images/wai-aria-practices/images/pattern-windowsplitter.svg)

## Example

Work to develop an example window splitter widget is tracked by [issue 130.](https://github.com/w3c/aria-practices/issues/130)

## Keyboard Interaction

- `Left Arrow`: Moves a vertical splitter to the left.
- `Right Arrow`: Moves a vertical splitter to the right.
- `Up Arrow`: Moves a horizontal splitter up.
- `Down Arrow`: Moves a horizontal splitter down.
- `Enter`: If the primary pane is not collapsed, collapses the pane.
  If the pane is collapsed, restores the splitter to its previous position.
- `Home` (Optional): Moves splitter to the position that gives the primary pane its smallest allowed size.
  This may completely collapse the primary pane.
- `End` (Optional): Moves splitter to the position that gives the primary pane its largest allowed size.
  This may completely collapse the secondary pane.
- `F6` (Optional): Cycle through window panes.

### Note

A fixed size splitter omits implementation of the arrow keys.

## WAI-ARIA Roles, States, and Properties

- The element that serves as the focusable splitter has role [separator](https://w3c.github.io/aria/#separator).
- The separator element has the [aria-valuenow](https://w3c.github.io/aria/#aria-valuenow) property set to a decimal value representing the current position of the separator.
- The separator element has the [aria-valuemin](https://w3c.github.io/aria/#aria-valuemin) property set to a decimal value that represents the position where the primary pane has its minimum size.
  This is typically `0`.
- The separator element has the [aria-valuemax](https://w3c.github.io/aria/#aria-valuemax) property set to a decimal value that represents the position where the primary pane has its maximum size.
  This is typically `100`.
- If the primary pane has a visible label, it is referenced by [aria-labelledby](https://w3c.github.io/aria/#aria-labelledby) on the separator element.
  Otherwise, the separator element has a label provided by [aria-label](https://w3c.github.io/aria/#aria-label).
- The separator element has [aria-controls](https://w3c.github.io/aria/#aria-controls) referring to the primary pane.