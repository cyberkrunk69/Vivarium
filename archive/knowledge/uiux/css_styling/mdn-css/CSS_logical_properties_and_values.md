# CSS logical properties and values

Source: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values

---

# CSS logical properties and values

The **CSS logical properties and values** module defines logical properties and values that can control layout through logical rather than physical direction and dimension mappings. Logical properties define directionârelative equivalents to their corresponding physical properties.

The start of a line is not always the left side of a line. Different writing systems operate in various directions. For example:

- English and Portuguese are written from left to right with new lines added below the previous ones.
- Hebrew and Arabic are right-to-left languages with new lines again being added below the previous ones.
- In some writing modes, the text lines are vertical, written from top to bottom. Chinese, Vietnamese, Korean, and Japanese are traditionally written vertically, from top to bottom, with each new vertical line added to the left of the previous one.
- Traditional Mongolian is also a top-to-bottom language, but new lines are to the right of previous ones.

The logical properties defined in this module enable defining properties relative to the content's writing direction, rather than a physical direction. This means content translated into languages with different writing modes will be rendered as intended.

Logical properties and values use the abstract terms *block* and *inline* to describe the direction in which they flow. The physical meaning of these terms depends on the [writing mode](/en-US/docs/Web/CSS/Guides/Writing_modes).

The **block dimension** is perpendicular to the flow of text within a line, i.e., the vertical dimension in horizontal writing modes, and the horizontal dimension in vertical writing modes. For standard English text, it is the vertical dimension.

The **inline dimension** is parallel to the flow of text within a line, i.e., the horizontal dimension in horizontal writing modes, and the vertical dimension in vertical writing modes. For standard English text, it is the horizontal dimension.

CSS was initially designed with only physical coordinates. The logical properties and values module defines flowârelative equivalents for many [values](/en-US/docs/Web/CSS/Guides/Values_and_units) and [properties](/en-US/docs/Glossary/Property/CSS). Properties that once only accepted physical values (`top`, `bottom`, `left`, `right`) now also accept flow-relative logical values (`block-start`, `block-end`, `inline-start`, `inline-end`).

## [Reference](#reference)

### [Properties](#properties)

- [`block-size`](/en-US/docs/Web/CSS/Reference/Properties/block-size)
- [`border-block`](/en-US/docs/Web/CSS/Reference/Properties/border-block)
- [`border-block-color`](/en-US/docs/Web/CSS/Reference/Properties/border-block-color)
- [`border-block-end`](/en-US/docs/Web/CSS/Reference/Properties/border-block-end)
- [`border-block-end-color`](/en-US/docs/Web/CSS/Reference/Properties/border-block-end-color)
- [`border-block-end-style`](/en-US/docs/Web/CSS/Reference/Properties/border-block-end-style)
- [`border-block-end-width`](/en-US/docs/Web/CSS/Reference/Properties/border-block-end-width)
- [`border-block-start`](/en-US/docs/Web/CSS/Reference/Properties/border-block-start)
- [`border-block-start-color`](/en-US/docs/Web/CSS/Reference/Properties/border-block-start-color)
- [`border-block-start-style`](/en-US/docs/Web/CSS/Reference/Properties/border-block-start-style)
- [`border-block-start-width`](/en-US/docs/Web/CSS/Reference/Properties/border-block-start-width)
- [`border-block-style`](/en-US/docs/Web/CSS/Reference/Properties/border-block-style)
- [`border-block-width`](/en-US/docs/Web/CSS/Reference/Properties/border-block-width)
- [`border-end-end-radius`](/en-US/docs/Web/CSS/Reference/Properties/border-end-end-radius)
- [`border-end-start-radius`](/en-US/docs/Web/CSS/Reference/Properties/border-end-start-radius)
- [`border-inline`](/en-US/docs/Web/CSS/Reference/Properties/border-inline)
- [`border-inline-color`](/en-US/docs/Web/CSS/Reference/Properties/border-inline-color)
- [`border-inline-end`](/en-US/docs/Web/CSS/Reference/Properties/border-inline-end)
- [`border-inline-end-color`](/en-US/docs/Web/CSS/Reference/Properties/border-inline-end-color)
- [`border-inline-end-style`](/en-US/docs/Web/CSS/Reference/Properties/border-inline-end-style)
- [`border-inline-end-width`](/en-US/docs/Web/CSS/Reference/Properties/border-inline-end-width)
- [`border-inline-start`](/en-US/docs/Web/CSS/Reference/Properties/border-inline-start)
- [`border-inline-start-color`](/en-US/docs/Web/CSS/Reference/Properties/border-inline-start-color)
- [`border-inline-start-style`](/en-US/docs/Web/CSS/Reference/Properties/border-inline-start-style)
- [`border-inline-start-width`](/en-US/docs/Web/CSS/Reference/Properties/border-inline-start-width)
- [`border-inline-style`](/en-US/docs/Web/CSS/Reference/Properties/border-inline-style)
- [`border-inline-width`](/en-US/docs/Web/CSS/Reference/Properties/border-inline-width)
- [`border-start-end-radius`](/en-US/docs/Web/CSS/Reference/Properties/border-start-end-radius)
- [`border-start-start-radius`](/en-US/docs/Web/CSS/Reference/Properties/border-start-start-radius)
- [`inline-size`](/en-US/docs/Web/CSS/Reference/Properties/inline-size)
- [`inset`](/en-US/docs/Web/CSS/Reference/Properties/inset)
- [`inset-block`](/en-US/docs/Web/CSS/Reference/Properties/inset-block)
- [`inset-block-end`](/en-US/docs/Web/CSS/Reference/Properties/inset-block-end)
- [`inset-block-start`](/en-US/docs/Web/CSS/Reference/Properties/inset-block-start)
- [`inset-inline`](/en-US/docs/Web/CSS/Reference/Properties/inset-inline)
- [`inset-inline-end`](/en-US/docs/Web/CSS/Reference/Properties/inset-inline-end)
- [`inset-inline-start`](/en-US/docs/Web/CSS/Reference/Properties/inset-inline-start)
- [`margin-block`](/en-US/docs/Web/CSS/Reference/Properties/margin-block)
- [`margin-block-end`](/en-US/docs/Web/CSS/Reference/Properties/margin-block-end)
- [`margin-block-start`](/en-US/docs/Web/CSS/Reference/Properties/margin-block-start)
- [`margin-inline`](/en-US/docs/Web/CSS/Reference/Properties/margin-inline)
- [`margin-inline-end`](/en-US/docs/Web/CSS/Reference/Properties/margin-inline-end)
- [`margin-inline-start`](/en-US/docs/Web/CSS/Reference/Properties/margin-inline-start)
- [`max-block-size`](/en-US/docs/Web/CSS/Reference/Properties/max-block-size)
- [`max-inline-size`](/en-US/docs/Web/CSS/Reference/Properties/max-inline-size)
- [`min-block-size`](/en-US/docs/Web/CSS/Reference/Properties/min-block-size)
- [`min-inline-size`](/en-US/docs/Web/CSS/Reference/Properties/min-inline-size)
- [`padding-block`](/en-US/docs/Web/CSS/Reference/Properties/padding-block)
- [`padding-block-end`](/en-US/docs/Web/CSS/Reference/Properties/padding-block-end)
- [`padding-block-start`](/en-US/docs/Web/CSS/Reference/Properties/padding-block-start)
- [`padding-inline`](/en-US/docs/Web/CSS/Reference/Properties/padding-inline)
- [`padding-inline-end`](/en-US/docs/Web/CSS/Reference/Properties/padding-inline-end)
- [`padding-inline-start`](/en-US/docs/Web/CSS/Reference/Properties/padding-inline-start)

### [Data types and values](#data_types_and_values)

[Flow relative values](/en-US/docs/Glossary/Flow_relative_values):

- `block-start`
- `block-end`
- `inline-start`
- `inline-end`
- `start`
- `end`

### [Glossary terms](#glossary_terms)

- [Flow relative values](/en-US/docs/Glossary/Flow_relative_values)
- [Inset properties](/en-US/docs/Glossary/Inset_properties)
- [Logical properties](/en-US/docs/Glossary/Logical_properties)
- [Physical properties](/en-US/docs/Glossary/Physical_properties)

## [Guides](#guides)

[Basic concepts of logical properties and values](/en-US/docs/Web/CSS/Guides/Logical_properties_and_values/Basic_concepts)
:   Overview of flow relative properties and values.

[Logical properties for sizing](/en-US/docs/Web/CSS/Guides/Logical_properties_and_values/Sizing)
:   Flow-relative mappings between physical properties and logical properties used for sizing elements on the page.

[Logical properties for margins, borders, and padding](/en-US/docs/Web/CSS/Guides/Logical_properties_and_values/Margins_borders_padding)
:   Flow-relative mappings for the various margin, border, and padding properties and their shorthands.

[Logical properties for floating and positioning](/en-US/docs/Web/CSS/Guides/Logical_properties_and_values/Floating_and_positioning)
:   Details mappings between the physical and logical values for `float` and `clear`, [inset properties](/en-US/docs/Glossary/Inset_properties), and `resize`.

## [Related concepts](#related_concepts)

- [`caption-side`](/en-US/docs/Web/CSS/Reference/Properties/caption-side)
- [`clear`](/en-US/docs/Web/CSS/Reference/Properties/clear)
- [`float`](/en-US/docs/Web/CSS/Reference/Properties/float)
- [`resize`](/en-US/docs/Web/CSS/Reference/Properties/resize)
- [`text-align`](/en-US/docs/Web/CSS/Reference/Properties/text-align)

[CSS box model](/en-US/docs/Web/CSS/Guides/Box_model)

- [`margin`](/en-US/docs/Web/CSS/Reference/Properties/margin) shorthand
- [`padding`](/en-US/docs/Web/CSS/Reference/Properties/padding) shorthand

[CSS box sizing](/en-US/docs/Web/CSS/Guides/Box_sizing)

- [`max-height`](/en-US/docs/Web/CSS/Reference/Properties/max-height)
- [`max-width`](/en-US/docs/Web/CSS/Reference/Properties/max-width)
- [`min-height`](/en-US/docs/Web/CSS/Reference/Properties/min-height)
- [`min-width`](/en-US/docs/Web/CSS/Reference/Properties/min-width)

[CSS backgrounds and borders](/en-US/docs/Web/CSS/Guides/Backgrounds_and_borders)

- [`border-color`](/en-US/docs/Web/CSS/Reference/Properties/border-color)
- [`border-style`](/en-US/docs/Web/CSS/Reference/Properties/border-style)
- [`border-width`](/en-US/docs/Web/CSS/Reference/Properties/border-width)
- [`border`](/en-US/docs/Web/CSS/Reference/Properties/border) shorthand
- [`border-radius`](/en-US/docs/Web/CSS/Reference/Properties/border-radius)

[CSS positioned layout](/en-US/docs/Web/CSS/Guides/Positioned_layout)

- [`top`](/en-US/docs/Web/CSS/Reference/Properties/top)
- [`right`](/en-US/docs/Web/CSS/Reference/Properties/right)
- [`bottom`](/en-US/docs/Web/CSS/Reference/Properties/bottom)
- [`left`](/en-US/docs/Web/CSS/Reference/Properties/left)

[CSS writing modes](/en-US/docs/Web/CSS/Guides/Writing_modes)

- [`direction`](/en-US/docs/Web/CSS/Reference/Properties/direction)
- [`text-orientation`](/en-US/docs/Web/CSS/Reference/Properties/text-orientation)
- [`writing-mode`](/en-US/docs/Web/CSS/Reference/Properties/writing-mode)

[CSS containment](/en-US/docs/Web/CSS/Guides/Containment)

- [`contain-intrinsic-block-size`](/en-US/docs/Web/CSS/Reference/Properties/contain-intrinsic-block-size)
- [`contain-intrinsic-inline-size`](/en-US/docs/Web/CSS/Reference/Properties/contain-intrinsic-inline-size)

[CSS overflow](/en-US/docs/Web/CSS/Guides/Overflow)

- [`overflow-block`](/en-US/docs/Web/CSS/Reference/Properties/overflow-block)
- [`overflow-inline`](/en-US/docs/Web/CSS/Reference/Properties/overflow-inline)

[CSS overscroll behavior](/en-US/docs/Web/CSS/Guides/Overscroll_behavior)

- [`overscroll-behavior-block`](/en-US/docs/Web/CSS/Reference/Properties/overscroll-behavior-block)
- [`overscroll-behavior-inline`](/en-US/docs/Web/CSS/Reference/Properties/overscroll-behavior-inline)

## [Specifications](#specifications)

| Specification |
| --- |
| [CSS Logical Properties and Values Module Level 1](https://drafts.csswg.org/css-logical/) |

## [See also](#see_also)

- [Flow layout and writing modes](/en-US/docs/Web/CSS/Guides/Display/Flow_layout_and_writing_modes)
- [CSS flexible box layout](/en-US/docs/Web/CSS/Guides/Flexible_box_layout) module
- [CSS grid layout](/en-US/docs/Web/CSS/Guides/Grid_layout) module

## Help improve MDN

Was this page helpful to you?

Yes

No

[Learn how to contribute](/en-US/docs/MDN/Community/Getting_started)

This page was last modified on Nov 18, 2025 by [MDN contributors](/en-US/docs/Web/CSS/Guides/Logical_properties_and_values/contributors.txt).

[View this page on GitHub](https://github.com/mdn/content/blob/main/files/en-us/web/css/guides/logical_properties_and_values/index.md?plain=1 "Folder: en-us/web/css/guides/logical_properties_and_values (Opens in a new tab)") â¢ [Report a problem with this content](https://github.com/mdn/content/issues/new?template=page-report.yml&mdn-url=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FGuides%2FLogical_properties_and_values&metadata=%3C%21--+Do+not+make+changes+below+this+line+--%3E%0A%3Cdetails%3E%0A%3Csummary%3EPage+report+details%3C%2Fsummary%3E%0A%0A*+Folder%3A+%60en-us%2Fweb%2Fcss%2Fguides%2Flogical_properties_and_values%60%0A*+MDN+URL%3A+https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FCSS%2FGuides%2FLogical_properties_and_values%0A*+GitHub+URL%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fblob%2Fmain%2Ffiles%2Fen-us%2Fweb%2Fcss%2Fguides%2Flogical_properties_and_values%2Findex.md%0A*+Last+commit%3A+https%3A%2F%2Fgithub.com%2Fmdn%2Fcontent%2Fcommit%2F81f8fcd666952c1782653a3675347c392cc997ca%0A*+Document+last+modified%3A+2025-11-18T10%3A30%3A16.000Z%0A%0A%3C%2Fdetails%3E "This will take you to GitHub to file a new issue.")