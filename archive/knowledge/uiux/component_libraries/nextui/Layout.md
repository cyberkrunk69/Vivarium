# Layout

Source: https://nextui.org/docs/customization/layout

---

Getting Started

- [Introduction](/docs/guide/introduction)
- [Design Principles](/docs/guide/design-principles)
- [Installation](/docs/guide/installation)
- [CLI](/docs/guide/cli)
- [Routing

  Updated](/docs/guide/routing)
- [Forms](/docs/guide/forms)
- [Tailwind v4

  New](/docs/guide/tailwind-v4)
- [NextUI to HeroUI](/docs/guide/nextui-to-heroui)
- [Figma](/docs/guide/figma)

Frameworks

- [Next.js](/docs/frameworks/nextjs)
- [Vite](/docs/frameworks/vite)
- [Remix](/docs/frameworks/remix)
- [Astro](/docs/frameworks/astro)
- [Laravel](/docs/frameworks/laravel)

Customization

- [Theme](/docs/customization/theme)
- [Layout](/docs/customization/layout)
- [Colors](/docs/customization/colors)
- [Customize theme](/docs/customization/customize-theme)
- [Create theme](/docs/customization/create-theme)
- [Dark mode](/docs/customization/dark-mode)
- [Override styles](/docs/customization/override-styles)
- [Custom variants](/docs/customization/custom-variants)

Components

- [Accordion](/docs/components/accordion)
- [Autocomplete](/docs/components/autocomplete)
- [Alert](/docs/components/alert)
- [Avatar](/docs/components/avatar)
- [Badge](/docs/components/badge)
- [Breadcrumbs](/docs/components/breadcrumbs)
- [Button](/docs/components/button)
- [Calendar](/docs/components/calendar)
- [Card](/docs/components/card)
- [Checkbox](/docs/components/checkbox)
- [Checkbox Group](/docs/components/checkbox-group)
- [Chip](/docs/components/chip)
- [Circular Progress](/docs/components/circular-progress)
- [Code](/docs/components/code)
- [Date Input](/docs/components/date-input)
- [Date Picker](/docs/components/date-picker)
- [Date Range Picker](/docs/components/date-range-picker)
- [Divider](/docs/components/divider)
- [Dropdown](/docs/components/dropdown)
- [Drawer](/docs/components/drawer)
- [Form](/docs/components/form)
- [Image](/docs/components/image)
- [Input

  Updated](/docs/components/input)
- [Input OTP](/docs/components/input-otp)
- [Kbd](/docs/components/kbd)
- [Link](/docs/components/link)
- [Listbox](/docs/components/listbox)
- [Modal](/docs/components/modal)
- [Navbar](/docs/components/navbar)
- [Number Input](/docs/components/number-input)
- [Pagination](/docs/components/pagination)
- [Popover](/docs/components/popover)
- [Progress](/docs/components/progress)
- [Radio Group](/docs/components/radio-group)
- [Range Calendar](/docs/components/range-calendar)
- [Scroll Shadow](/docs/components/scroll-shadow)
- [Select

  Updated](/docs/components/select)
- [Skeleton](/docs/components/skeleton)
- [Slider

  Updated](/docs/components/slider)
- [Snippet](/docs/components/snippet)
- [Spacer](/docs/components/spacer)
- [Spinner](/docs/components/spinner)
- [Switch](/docs/components/switch)
- [Table

  Updated](/docs/components/table)
- [Tabs](/docs/components/tabs)
- [Toast

  Updated](/docs/components/toast)
- [Textarea](/docs/components/textarea)
- [Time Input](/docs/components/time-input)
- [Tooltip](/docs/components/tooltip)
- [User](/docs/components/user)

API References

- [HeroUI CLI

  Updated](/docs/api-references/cli-api)
- [HeroUIProvider](/docs/api-references/heroui-provider)

# Layout

HeroUI provides layout customization options for spacing, fonts, and other visual properties. Layout tokens help maintain consistency across components without modifying Tailwind CSS defaults.

> Layout options are applied to all components.

## [Default Layout](#default-layout)

Default values for the layout tokens are:

### [CSS Variables](#css-variables)

HeroUI creates CSS variables using the format `--prefix-prop-name-scale` for each layout token. By
default the prefix is `heroui`, but you can change it with the `prefix` option.

Then you can use the CSS variables in your CSS files.

#### [API Reference](#api-reference)

| Attribute | Type | Description |
| --- | --- | --- |
| hoverOpacity | string, number | A number between 0 and 1 that is applied as opacity-[value] when the component is hovered. |
| disabledOpacity | string, number | A number between 0 and 1 that is applied as opacity-[value] when the component is disabled. |
| dividerWeight | string | The default height applied to the divider component. We recommend to use `px` units. |
| fontSize | [FontThemeUnit](#fontthemeunit) | The default font size applied across the components. |
| lineHeight | [FontThemeUnit](#fontthemeunit) | The default line height applied across the components. |
| radius | [BaseThemeUnit](#basethemeunit) | The default radius applied across the components. We recommend to use `rem` units. |
| borderWidth | [BaseThemeUnit](#basethemeunit) | The border width applied across the components. |
| boxShadow | [BaseThemeUnit](#basethemeunit) | The box shadow applied across the components. |

#### [BaseThemeUnit](#basethemeunit)

#### [FontThemeUnit](#fontthemeunit)

ThemeColors

On this page

- [Default Layout](#default-layout)
- [CSS Variables](#css-variables)
- [API Reference](#api-reference)
- [BaseThemeUnit](#basethemeunit)
- [FontThemeUnit](#fontthemeunit)
- ---

  [Back to top](#layout)

Ship faster  
with beautiful  
components

Discover 210+ stunning components by HeroUI

Explore Components