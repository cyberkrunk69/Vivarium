# Colors

Source: https://nextui.org/docs/customization/colors

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

# Colors

HeroUI's plugin enables you to personalize the semantic colors of the theme such as `primary`,
`secondary`, `success`, etc.

> **Note**: Colors configurations apply globally across all components.

## [Default Colors](#default-colors)

HeroUI offers a default color palette right out of the box, perfect for when you're
still undecided about your specific branding colors.

These colors are split into [Common Colors](#common-colors) and [Semantic Colors](#semantic-colors).

- [Common Colors](#common-colors): Consistent across themes.
- [Semantic Colors](#semantic-colors): Adjust according to the chosen theme.

### [Common Colors](#common-colors)

Common colors, like [TailwindCSS](https://v3.tailwindcss.com/docs/customizing-colors) colors,
remain consistent regardless of the theme.

To prevent conflicts with TailwindCSS colors, common colors are initially disabled but can
be activated with the `addCommonColors` option.

Enabling this option supplements some TailwindCSS default colors with the following:

## White & Black

#FFFFFF#000000

## Blue

#E6F1FE50#CCE3FD100#99C7FB200#66AAF9300#338EF7400#006FEE500#005BC4600#004493700#002E62800#001731900

## Purple

#F2EAFA50#E4D4F4100#C9A9E9200#AE7EDE300#9353D3400#7828C8500#6020A0600#481878700#301050800#180828900

## Green

#E8FAF050#D1F4E0100#A2E9C1200#74DFA2300#45D483400#17C964500#12A150600#0E793C700#095028800#052814900

## Red

#FEE7EF50#FDD0DF100#FAA0BF200#F871A0300#F54180400#F31260500#C20E4D600#920B3A700#610726800#310413900

## Pink

#FFEDFA50#FFDCF5100#FFB8EB200#FF95E1300#FF71D7400#FF4ECD500#CC3EA4600#992F7B700#661F52800#331029900

## Yellow

#FEFCE850#FDEDD3100#FBDBA7200#F9C97C300#F7B750400#F5A524500#C4841D600#936316700#62420E800#312107900

## Cyan

#F0FCFF50#E6FAFE100#D7F8FE200#C3F4FD300#A5EEFD400#7EE7FC500#06B7DB600#09AACD700#0E8AAA800#053B48900

## Zinc

#FAFAFA50#F4F4F5100#E4E4E7200#D4D4D8300#A1A1AA400#71717A500#52525B600#3F3F46700#27272A800#18181B900

### [Semantic Colors](#semantic-colors)

Semantic colors adapt with the theme, delivering meaning and reinforcing your brand identity.

For an effective palette, we recommend using color ranges from `50` to `900`. You can use tools like [Eva Design System](https://colors.eva.design/),
[Smart Watch](https://smart-swatch.netlify.app/), [Palette](https://palettte.app/) or [Color Box](https://colorbox.io/) to generate your palette.

> Semantic colors should be placed inside the `heroui` plugin options, not inside the TailwindCSS theme object.

> Change the docs theme to see the semantic colors in action.

## Layout

backgroundforegrounddividerfocus

## Content

content1content2content3content4

## Base

defaultprimarysecondarysuccesswarningdanger

## Default

default-50default-100default-200default-300default-400default-500default-600default-700default-800default-900

## Primary

primary-50primary-100primary-200primary-300primary-400primary-500primary-600primary-700primary-800primary-900

## Secondary

secondary-50secondary-100secondary-200secondary-300secondary-400secondary-500secondary-600secondary-700secondary-800secondary-900

## Success

success-50success-100success-200success-300success-400success-500success-600success-700success-800success-900

## Warning

warning-50warning-100warning-200warning-300warning-400warning-500warning-600warning-700warning-800warning-900

## Danger

danger-50danger-100danger-200danger-300danger-400danger-500danger-600danger-700danger-800danger-900

### [Using Semantic Colors](#using-semantic-colors)

Semantic colors can be applied anywhere in your project where colors are used, such as
text color, border color, background color utilities, and more.

### [Javascript Variables](#javascript-variables)

Import semantic and common colors into your JavaScript files as follows:

### [CSS Variables](#css-variables)

HeroUI creates CSS variables using the format `--prefix-colorname-shade` for each semantic color. By
default the prefix is `heroui`, but you can change it with the `prefix` option.

Then you can use the CSS variables in your CSS files.

LayoutCustomize theme

On this page

- [Default Colors](#default-colors)
- [Common Colors](#common-colors)
- [Semantic Colors](#semantic-colors)
- [Using Semantic Colors](#using-semantic-colors)
- [Javascript Variables](#javascript-variables)
- [CSS Variables](#css-variables)
- ---

  [Back to top](#colors)

Ship faster  
with beautiful  
components

Discover 210+ stunning components by HeroUI

Explore Components