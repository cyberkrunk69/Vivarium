# Label

Source: https://ui.shadcn.com/docs/components/label

---

Sections

- [Introduction](/docs)
- [Components](/docs/components)
- [Installation](/docs/installation)
- [Directory](/docs/directory)
- [RTL](/docs/rtl)
- [MCP Server](/docs/mcp)
- [Registry](/docs/registry)
- [Forms](/docs/forms)
- [Changelog](/docs/changelog)

Components

- [Accordion](/docs/components/radix/accordion)
- [Alert](/docs/components/radix/alert)
- [Alert Dialog](/docs/components/radix/alert-dialog)
- [Aspect Ratio](/docs/components/radix/aspect-ratio)
- [Avatar](/docs/components/radix/avatar)
- [Badge](/docs/components/radix/badge)
- [Breadcrumb](/docs/components/radix/breadcrumb)
- [Button](/docs/components/radix/button)
- [Button Group](/docs/components/radix/button-group)
- [Calendar](/docs/components/radix/calendar)
- [Card](/docs/components/radix/card)
- [Carousel](/docs/components/radix/carousel)
- [Chart](/docs/components/radix/chart)
- [Checkbox](/docs/components/radix/checkbox)
- [Collapsible](/docs/components/radix/collapsible)
- [Combobox](/docs/components/radix/combobox)
- [Command](/docs/components/radix/command)
- [Context Menu](/docs/components/radix/context-menu)
- [Data Table](/docs/components/radix/data-table)
- [Date Picker](/docs/components/radix/date-picker)
- [Dialog](/docs/components/radix/dialog)
- [Direction](/docs/components/radix/direction)
- [Drawer](/docs/components/radix/drawer)
- [Dropdown Menu](/docs/components/radix/dropdown-menu)
- [Empty](/docs/components/radix/empty)
- [Field](/docs/components/radix/field)
- [Hover Card](/docs/components/radix/hover-card)
- [Input](/docs/components/radix/input)
- [Input Group](/docs/components/radix/input-group)
- [Input OTP](/docs/components/radix/input-otp)
- [Item](/docs/components/radix/item)
- [Kbd](/docs/components/radix/kbd)
- [Label](/docs/components/radix/label)
- [Menubar](/docs/components/radix/menubar)
- [Native Select](/docs/components/radix/native-select)
- [Navigation Menu](/docs/components/radix/navigation-menu)
- [Pagination](/docs/components/radix/pagination)
- [Popover](/docs/components/radix/popover)
- [Progress](/docs/components/radix/progress)
- [Radio Group](/docs/components/radix/radio-group)
- [Resizable](/docs/components/radix/resizable)
- [Scroll Area](/docs/components/radix/scroll-area)
- [Select](/docs/components/radix/select)
- [Separator](/docs/components/radix/separator)
- [Sheet](/docs/components/radix/sheet)
- [Sidebar](/docs/components/radix/sidebar)
- [Skeleton](/docs/components/radix/skeleton)
- [Slider](/docs/components/radix/slider)
- [Sonner](/docs/components/radix/sonner)
- [Spinner](/docs/components/radix/spinner)
- [Switch](/docs/components/radix/switch)
- [Table](/docs/components/radix/table)
- [Tabs](/docs/components/radix/tabs)
- [Textarea](/docs/components/radix/textarea)
- [Toast](/docs/components/radix/toast)
- [Toggle](/docs/components/radix/toggle)
- [Toggle Group](/docs/components/radix/toggle-group)
- [Tooltip](/docs/components/radix/tooltip)
- [Typography](/docs/components/radix/typography)

Get Started

- [Installation](/docs/installation)
- [components.json](/docs/components-json)
- [Theming](/docs/theming)
- [Dark Mode](/docs/dark-mode)
- [CLI](/docs/cli)
- [Monorepo](/docs/monorepo)
- [Open in v0](/docs/v0)
- [JavaScript](/docs/javascript)
- [Blocks](/docs/blocks)
- [Figma](/docs/figma)
- [llms.txt](/llms.txt)
- [Legacy Docs](/docs/legacy)

Forms

- [React Hook Form](/docs/forms/react-hook-form)
- [TanStack Form](/docs/forms/tanstack-form)

Registry

- [Introduction](/docs/registry)
- [Getting Started](/docs/registry/getting-started)
- [Namespaces](/docs/registry/namespace)
- [Authentication](/docs/registry/authentication)
- [Examples](/docs/registry/examples)
- [MCP Server](/docs/registry/mcp)
- [Add a Registry](/docs/registry/registry-index)
- [Open in v0](/docs/registry/open-in-v0)
- [registry.json](/docs/registry/registry-json)
- [registry-item.json](/docs/registry/registry-item-json)

# Label

Copy Page

[Previous](/docs/components/radix/kbd)[Next](/docs/components/radix/menubar)

Renders an accessible label associated with controls.

[Radix UI](/docs/components/radix/label)[Base UI](/docs/components/base/label)

Accept terms and conditions

Copy

```
import { Checkbox } from "@/components/ui/checkbox"
import { Label } from "@/components/ui/label"
```

View Code

For form fields, use the [Field](/docs/components/radix/field) component which
includes built-in label, description, and error handling.

## Installation

CommandManual

```
pnpmnpmyarnbun

```
pnpm dlx shadcn@latest add label
```

Copy
```

## Usage

```
Copyimport { Label } from "@/components/ui/label"
```

```
Copy<Label htmlFor="email">Your email address</Label>
```

## Label in Field

For form fields, use the [Field](/docs/components/radix/field) component which
includes built-in `FieldLabel`, `FieldDescription`, and `FieldError` components.

```
Copy<Field>
  <FieldLabel htmlFor="email">Your email address</FieldLabel>
  <Input id="email" />
</Field>
```

Payment Method

All transactions are secure and encrypted

Name on Card

Card Number

Enter your 16-digit card number

MonthMM

YearYYYY

CVV

Billing Address

The billing address associated with your payment method

Same as shipping address

Comments

SubmitCancel

Copy

```
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import {
```

View Code

## RTL

To enable RTL support in shadcn/ui, see the [RTL configuration guide](/docs/rtl).

Arabic (العربية)Toggle

قبول الشروط والأحكام

Copy

```
"use client"

import * as React from "react"
```

View Code

## API Reference

See the [Radix UI Label](https://www.radix-ui.com/docs/primitives/components/label#api-reference) documentation for more information.

[Kbd](/docs/components/radix/kbd)[Menubar](/docs/components/radix/menubar)

On This Page

[Installation](#installation)[Usage](#usage)[Label in Field](#label-in-field)[RTL](#rtl)[API Reference](#api-reference)

Deploy your shadcn/ui app on Vercel

Trusted by OpenAI, Sonos, Adobe, and more.

Vercel provides tools and infrastructure to deploy apps and features at scale.

Deploy Now[Deploy to Vercel](https://vercel.com/new?utm_source=shadcn_site&utm_medium=web&utm_campaign=docs_cta_deploy_now_callout)