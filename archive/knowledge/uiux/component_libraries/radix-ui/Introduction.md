# Introduction

Source: https://www.radix-ui.com/primitives/docs/overview/introduction

---

[Radix Homepage](/)[Made by WorkOS](https://workos.com)

[Radix Homepage](/)[Made by WorkOS](https://workos.com)

[ThemesThemes](/)[PrimitivesPrimitives](/primitives)[IconsIcons](/icons)[ColorsColors](/colors)

[Documentation](/primitives/docs)[Case studies](/primitives/case-studies)[Blog](/blog)

Search

`/`

#### Overview

[Introduction](/primitives/docs/overview/introduction)[Getting started](/primitives/docs/overview/getting-started)[Accessibility](/primitives/docs/overview/accessibility)[Releases](/primitives/docs/overview/releases)

#### Guides

[Styling](/primitives/docs/guides/styling)[Animation](/primitives/docs/guides/animation)[Composition](/primitives/docs/guides/composition)[Server-side rendering](/primitives/docs/guides/server-side-rendering)

#### Components

[Accordion](/primitives/docs/components/accordion)[Alert Dialog](/primitives/docs/components/alert-dialog)[Aspect Ratio](/primitives/docs/components/aspect-ratio)[Avatar](/primitives/docs/components/avatar)[Checkbox](/primitives/docs/components/checkbox)[Collapsible](/primitives/docs/components/collapsible)[Context Menu](/primitives/docs/components/context-menu)[Dialog](/primitives/docs/components/dialog)[Dropdown Menu](/primitives/docs/components/dropdown-menu)[Form

Preview](/primitives/docs/components/form)[Hover Card](/primitives/docs/components/hover-card)[Label](/primitives/docs/components/label)[Menubar](/primitives/docs/components/menubar)[Navigation Menu](/primitives/docs/components/navigation-menu)[One-Time Password Field

Preview](/primitives/docs/components/one-time-password-field)[Password Toggle Field

Preview](/primitives/docs/components/password-toggle-field)[Popover](/primitives/docs/components/popover)[Progress](/primitives/docs/components/progress)[Radio Group](/primitives/docs/components/radio-group)[Scroll Area](/primitives/docs/components/scroll-area)[Select](/primitives/docs/components/select)[Separator](/primitives/docs/components/separator)[Slider](/primitives/docs/components/slider)[Switch](/primitives/docs/components/switch)[Tabs](/primitives/docs/components/tabs)[Toast](/primitives/docs/components/toast)[Toggle](/primitives/docs/components/toggle)[Toggle Group](/primitives/docs/components/toggle-group)[Toolbar](/primitives/docs/components/toolbar)[Tooltip](/primitives/docs/components/tooltip)

#### Utilities

[Accessible Icon](/primitives/docs/utilities/accessible-icon)[Direction Provider](/primitives/docs/utilities/direction-provider)[Portal](/primitives/docs/utilities/portal)[Slot](/primitives/docs/utilities/slot)[Visually Hidden](/primitives/docs/utilities/visually-hidden)

Overview

# Introduction

An open-source UI component library for building high-quality, accessible
design systems and web apps.

Radix Primitives is a low-level UI component library with a focus on accessibility, customization and developer experience. You can use these components either as the base layer of your design system, or adopt them incrementally.

## [Vision](#vision)

Most of us share similar definitions for common UI patterns like accordion, checkbox,
combobox, dialog, dropdown, select, slider, and tooltip. These UI patterns are [documented by WAI-ARIA](https://www.w3.org/TR/wai-aria-practices/#aria_ex) and generally understood by the community.

However, the implementations provided to us by the web platform are inadequate. They're
either non-existent, lacking in functionality, or cannot be customized sufficiently.

So, developers are forced to build custom components; an incredibly difficult task. As a
result, most components on the web are inaccessible, non-performant, and lacking important
features.

Our goal is to create a well-funded, open-source component library that the community can
use to build accessible design systems.

## [Key Features](#key-features)

### [Accessible](#accessible)

Components adhere to the [WAI-ARIA design patterns](https://www.w3.org/TR/wai-aria-practices-1.2) where possible. We handle many of the difficult implementation details related to accessibility, including aria and role attributes, focus management, and keyboard navigation. Learn more in our [accessibility](/primitives/docs/overview/accessibility) overview.

### [Unstyled](#unstyled)

Components ship without styles, giving you complete control over the look and feel. Components can be styled with any styling solution. Learn more in our [styling](/primitives/docs/guides/styling) guide.

### [Opened](#opened)

Radix Primitives are designed to be customized to suit your needs. Our open component architecture provides you granular access to each component part, so you can wrap them and add your own event listeners, props, or refs.

### [Uncontrolled](#uncontrolled)

Where applicable, components are uncontrolled by default but can also be controlled, alternatively. All of the behavior wiring is handled internally, so you can get up and running as smoothly as possible, without needing to create any local states.

### [Developer experience](#developer-experience)

One of our main goals is to provide the best possible developer experience. Radix Primitives provides a fully-typed API. All components share a similar API, creating a consistent and predictable experience. We've also implemented an `asChild` prop, giving users full control over the rendered element.

### [Incremental adoption](#incremental-adoption)

We recommend installing the `radix-ui` package and importing the primitives you need. This is the simplest way to get started, prevent version conflicts or duplication, and makes it easy to manage updates. The package is tree-shakeable, so you should only ship the components you use.

```
npm install radix-ui
```

```
import { Dialog, DropdownMenu, Tooltip } from "radix-ui";
```

Alternatively, each primitive can be installed individually:

```
npm install @radix-ui/react-dialog

npm install @radix-ui/react-dropdown-menu

npm install @radix-ui/react-tooltip
```

```
import * as Dialog from "@radix-ui/react-dialog";

import * as DropdownMenu from "@radix-ui/react-dropdown-menu";

import * as Tooltip from "@radix-ui/react-tooltip";
```

When installing separately, we recommend updating all Radix packages together to prevent duplication of shared dependencies and keep your bundle size down.

## [Community](#community)

To get involved with the Radix community, ask questions and share tips, [Join our Discord](https://discord.com/invite/7Xb99uG).

To receive updates on new primitives, announcements, blog posts, and general Radix tips, follow along on [Bluesky](https://bsky.app/profile/radix-ui.com) or [Twitter](https://twitter.com/radix_ui).

To file issues, request features, and contribute, check out our GitHub.

- [GitHub repo](https://github.com/radix-ui/primitives)
- [Code of conduct](https://github.com/radix-ui/primitives/blob/main/CODE_OF_CONDUCT.md)

Next[Getting started](/primitives/docs/overview/getting-started)

[Edit this page on GitHub.](https://github.com/radix-ui/website/edit/main/data/primitives/docs/overview/introduction.mdx "Edit this page on GitHub.")