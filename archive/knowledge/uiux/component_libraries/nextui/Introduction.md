# Introduction

Source: https://nextui.org/docs/guide/introduction

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

# Introduction

Welcome to the HeroUI documentation!

## [What is HeroUI?](#what-is-heroui)

HeroUI is a UI library for React that helps you build beautiful and accessible user interfaces. Created on top of
[Tailwind CSS](https://v3.tailwindcss.com/) and [React Aria](https://react-spectrum.adobe.com/react-aria/index.html).

HeroUI's primary goal is to streamline the development process, offering a beautiful and adaptable system design for an enhanced user experience.

---

## [FAQ](#faq)

### [Is HeroUI a copy-paste library?](#is-heroui-a-copy-paste-library)

No, HeroUI is not a copy-paste library. All components are available through `npm` and can be installed individually or as a whole package.

### [How is HeroUI different from TailwindCSS?](#how-is-heroui-different-from-tailwindcss)

- **TailwindCSS**:

  Tailwind CSS is a CSS Framework that provides atomic CSS classes to help you style components,
  leaving you to handle lots of other things like accessibility, component composition, keyboard
  navigation, style overrides, etc.
- **HeroUI**:

  HeroUI is a UI library for React that combines the power of TailwindCSS with React Aria to
  provide complete components (logic and styles) for building accessible and customizable user
  interfaces. Since HeroUI uses TailwindCSS as its style engine, you can use all TailwindCSS
  classes within your HeroUI components, ensuring optimal compiled CSS size.

### [How is HeroUI different from TailwindCSS components libraries?](#how-is-heroui-different-from-tailwindcss-components-libraries)

TailwindCSS components libraries such as [TailwindUI](https://tailwindui.com/),
[Flowbite](https://flowbite.com/), or [Preline](https://preline.co/), just to name a few, only offer a curated selection of TailwindCSS classes to style your components.
They don't provide any React specific components, logic, props, composition, or accessibility features.

In contrast to these libraries, HeroUI is a complete UI library that provides a set of accessible and
customizable components, hooks, and utilities.

### [How HeroUI deals with TailwindCSS classes conflicts?](#how-heroui-deals-with-tailwindcss-classes-conflicts)

We created a TailwindCSS utility library called [tailwind-variants](https://www.tailwind-variants.org/) that automatically handles TailwindCSS class conflicts. This ensures your custom classes will
consistently override the default ones, eliminating any duplication.

### [Does HeroUI use runtime CSS?](#does-heroui-use-runtime-css)

No. As HeroUI uses TailwindCSS as its style engine, it generates CSS at build time, eliminating
the need for runtime CSS. This means that HeroUI is fully compatible with the latest React and
Next.js versions.

### [Does HeroUI support TypeScript?](#does-heroui-support-typescript)

Yes, HeroUI is written in TypeScript and has full support for it.

### [Can I use HeroUI with other front-end frameworks or libraries, such as Vue or Angular?](#can-i-use-heroui-with-other-front-end-frameworks-or-libraries-such-as-vue-or-angular)

No, HeroUI is specifically designed for React as it is built on top of React Aria. However, you
can still use the HeroUI components styling part with other frameworks or libraries.

### [Why does HeroUI use Framer Motion?](#why-does-heroui-use-framer-motion)

We use [Framer Motion](https://www.framer.com/motion) to animate some components due to
the complexity of the animations and their physics-based nature. Framer Motion allows us to
handle these animations in a more straightforward and performant way. In addition, it is
well tested and production ready.

---

## [Community](#community)

We're excited to see the community adopt HeroUI, raise issues, and provide feedback.
Whether it's a feature request, bug report, or a project to showcase, please get involved!

X

For announcements, tips and general information.

Discord

To get involved in the community, ask questions and share tips.

Github

To report bugs, request features and contribute to the project.

## [Contributing](#contributing)

PRs on **HeroUI** are always welcome, please see our [contribution guidelines](https://github.com/heroui-inc/heroui/blob/main/CONTRIBUTING.md) to learn how you can contribute to this project.

Design Principles

On this page

- [What is HeroUI?](#what-is-heroui)
- [FAQ](#faq)
- [Is HeroUI a copy-paste library?](#is-heroui-a-copy-paste-library)
- [How is HeroUI different from TailwindCSS?](#how-is-heroui-different-from-tailwindcss)
- [How is HeroUI different from TailwindCSS components libraries?](#how-is-heroui-different-from-tailwindcss-components-libraries)
- [How HeroUI deals with TailwindCSS classes conflicts?](#how-heroui-deals-with-tailwindcss-classes-conflicts)
- [Does HeroUI use runtime CSS?](#does-heroui-use-runtime-css)
- [Does HeroUI support TypeScript?](#does-heroui-support-typescript)
- [Can I use HeroUI with other front-end frameworks or libraries, such as Vue or Angular?](#can-i-use-heroui-with-other-front-end-frameworks-or-libraries-such-as-vue-or-angular)
- [Why does HeroUI use Framer Motion?](#why-does-heroui-use-framer-motion)
- [Community](#community)
- [Contributing](#contributing)
- ---

  [Back to top](#introduction)

Ship faster  
with beautiful  
components

Discover 210+ stunning components by HeroUI

Explore Components