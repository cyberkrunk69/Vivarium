# Installation

Source: https://nextui.org/docs/guide/installation

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

# Installation

Requirements:

- [React 18](https://reactjs.org/) or later
- [Tailwind CSS v4](https://tailwindcss.com)
- [Framer Motion 11.9](https://www.framer.com/motion/) or later

---

> ⚠️ **Deprecation Notice:** HeroUI v2 will be deprecated soon. We recommend to use [**HeroUI v3**](http://v3.heroui.com/) for the new projects.

## [Automatic Installation](#automatic-installation)

Using the CLI is now the easiest way to start a HeroUI project. You can initialize your project and add components directly via the CLI:

### [Installation](#installation-1)

Execute one of the following commands in your terminal:

pnpm

npm

yarn

bun

### [Initialization and Starting the App](#initialization-and-starting-the-app)

Initialize the project by using the `init` command.

You will be prompted to configure your project:

Install the dependencies to start the local server:

pnpm

npm

yarn

bun

Start the local server:

pnpm

npm

yarn

bun

### [Adding the Components](#adding-the-components)

Once your HeroUI project is ready to develop, you can add individual components using the CLI. For example, to add a button component:

This command adds the Button component to your project and manages all related dependencies.

You can also add multiple components at once:

Or you can add the main library `@heroui/react` by running the following command:

If you leave out the component name, the CLI will prompt you to select the components you want to add.

## [Manual Installation](#manual-installation)

If you prefer not to use the CLI, you may try either global installation or individual installation to set up HeroUI in your project:

### [Global Installation](#global-installation)

The easiest way to get started with HeroUI is to use the global installation, which means
that all the components are imported from a single package.

Follow the steps below to install all HeroUI components:

#### [Install Packages](#install-packages)

To install HeroUI, run one of the following commands in your terminal:

pnpm

npm

yarn

bun

#### [Hoisted Dependencies Setup](#hoisted-dependencies-setup)

> **Note**: This step is only for those who use `pnpm` to install. If you install HeroUI using other package managers, you may skip this step.

If you are using pnpm, you need to add the following line to your `.npmrc` file to hoist our packages to the root `node_modules`.

After modifying the `.npmrc` file, you need to run `pnpm install` again to ensure that the dependencies are installed correctly.

#### [Tailwind CSS Setup](#tailwind-css-setup)

HeroUI is built on top of Tailwind CSS, so you need to install Tailwind CSS first. You can follow the official
[installation guide](https://tailwindcss.com/docs/installation/using-vite) to install Tailwind CSS.

> **Note**: If you are using pnpm and monorepo architecture, please make sure you are pointing to the ROOT `node_modules`

Then you need to create `hero.ts` file

and add the following code to your main css file:

#### [Provider Setup](#provider-setup)

It is essential to add the `HeroUIProvider` at the `root` of your application.

### [Individual Installation](#individual-installation)

HeroUI is also available as individual packages. You can install each package separately. This
is useful if you want to reduce the size of your CSS bundle as it will only include styles for the components
you're actually using.

> **Note**: JavaScript bundle size will not change due to tree shaking support in HeroUI.

Follow the steps below to install each package separately:

#### [Install Core Packages](#install-core-packages)

Although you can install each package separately, you need to install the core packages first
to ensure that all components work correctly.

Run one of the following commands in your terminal to install the core packages:

pnpm

npm

yarn

bun

#### [Install Component](#install-component)

Now, let's install the component you want to use. For example, if you want to use the
[Button](/docs/components/button) component, you need to run one of the following commands
in your terminal:

pnpm

npm

yarn

bun

#### [Hoisted Dependencies Setup](#hoisted-dependencies-setup-1)

> **Note**: This step is only for those who use `pnpm` to install. If you install HeroUI using other package managers, you may skip this step.

If you are using pnpm, you need to add the following line to your `.npmrc` file to hoist our packages to the root `node_modules`.

After modifying the `.npmrc` file, you need to run `pnpm install` again to ensure that the dependencies are installed correctly.

#### [Tailwind CSS Setup](#tailwind-css-setup-1)

TailwindCSS setup changes a bit when you use individual packages. You only need to add the
styles of the components you're using to your `tailwind.config.js` file. For example, for the
[Button](/docs/components/button) component, you need to add the following code to your
`tailwind.config.js` file:

#### [Provider Setup](#provider-setup-1)

It is essential to add the `HeroUIProvider` at the `root` of your application.

#### [Use the Component](#use-the-component)

Now, you can use the component you installed in your application:

## [Framework Guides](#framework-guides)

HeroUI is compatible with your preferred framework. We have compiled comprehensive, step-by-step tutorials for the following frameworks:

Next.js

Vite

Remix

Astro

Design PrinciplesCLI

On this page

- [Automatic Installation](#automatic-installation)
- [Installation](#installation-1)
- [Initialization and Starting the App](#initialization-and-starting-the-app)
- [Adding the Components](#adding-the-components)
- [Manual Installation](#manual-installation)
- [Global Installation](#global-installation)
- [Install Packages](#install-packages)
- [Hoisted Dependencies Setup](#hoisted-dependencies-setup)
- [Tailwind CSS Setup](#tailwind-css-setup)
- [Provider Setup](#provider-setup)
- [Individual Installation](#individual-installation)
- [Install Core Packages](#install-core-packages)
- [Install Component](#install-component)
- [Hoisted Dependencies Setup](#hoisted-dependencies-setup-1)
- [Tailwind CSS Setup](#tailwind-css-setup-1)
- [Provider Setup](#provider-setup-1)
- [Use the Component](#use-the-component)
- [Framework Guides](#framework-guides)
- ---

  [Back to top](#installation)

Ship faster  
with beautiful  
components

Discover 210+ stunning components by HeroUI

Explore Components