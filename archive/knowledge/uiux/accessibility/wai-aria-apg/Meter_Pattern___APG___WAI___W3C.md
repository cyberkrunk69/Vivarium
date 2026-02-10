# Meter Pattern | APG | WAI | W3C

Source: https://www.w3.org/WAI/ARIA/apg/patterns/meter/

---

Meter Pattern

## About This Pattern

A [meter](https://w3c.github.io/aria/#meter) is a graphical display of a numeric value that varies within a defined range.
For example, a meter could be used to depict a device's current battery percentage or a car's fuel level.

### Note

- A `meter` should not be used to represent a value like the current world population since it does not have a meaningful maximum limit.
- The `meter` should not be used to indicate progress, such as loading or percent completion of a task.
  To communicate progress, use the [progressbar](https://w3c.github.io/aria/#progressbar) role instead.

![](../../../../content-images/wai-aria-practices/images/pattern-meter.svg)

## Example

[Meter Example](examples/meter/)

## Keyboard Interaction

Not applicable.

## WAI-ARIA Roles, States, and Properties

- The element serving as the meter has a role of [meter](https://w3c.github.io/aria/#meter).
- The meter has [aria-valuenow](https://w3c.github.io/aria/#aria-valuenow) set to a decimal value between `aria-valuemin` and `aria-valuemax` representing the current value of the meter.
- The meter has [aria-valuemin](https://w3c.github.io/aria/#aria-valuemin) set to a decimal value less than `aria-valuemax`.
- The meter has [aria-valuemax](https://w3c.github.io/aria/#aria-valuemax) set to a decimal value greater than `aria-valuemin`.
- Assistive technologies often present `aria-valuenow` as a percentage.
  If conveying the value of the meter only in terms of a percentage would not be user friendly, the [aria-valuetext](https://w3c.github.io/aria/#aria-valuetext) property is set to a string that makes the meter value understandable.
  For example, a battery meter value might be conveyed as `aria-valuetext="50% (6 hours) remaining"`.
- If the meter has a visible label, it is referenced by [aria-labelledby](https://w3c.github.io/aria/#aria-labelledby) on the element with role `meter`.
  Otherwise, the element with role `meter` has a label provided by [aria-label](https://w3c.github.io/aria/#aria-label).