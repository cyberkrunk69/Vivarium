# Radio Group

Source: https://ui.shadcn.com/docs/components/radio-group

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

# Radio Group

Copy Page

[Previous](/docs/components/radix/progress)[Next](/docs/components/radix/resizable)

A set of checkable buttons—known as radio buttons—where no more than one of the buttons can be checked at a time.

[Radix UI](/docs/components/radix/radio-group)[Base UI](/docs/components/base/radio-group)

Default

Comfortable

Compact

Copy

```
import { Label } from "@/components/ui/label"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
```

View Code

## Installation

CommandManual

```
pnpmnpmyarnbun

```
pnpm dlx shadcn@latest add radio-group
```

Copy
```

## Usage

```
Copyimport { Label } from "@/components/ui/label"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
```

```
Copy<RadioGroup defaultValue="option-one">
  <div className="flex items-center gap-3">
    <RadioGroupItem value="option-one" id="option-one" />
    <Label htmlFor="option-one">Option One</Label>
  </div>
  <div className="flex items-center gap-3">
    <RadioGroupItem value="option-two" id="option-two" />
    <Label htmlFor="option-two">Option Two</Label>
  </div>
</RadioGroup>
```

## Examples

### Description

Radio group items with a description using the `Field` component.

Default

Standard spacing for most use cases.

Comfortable

More space between elements.

Compact

Minimal spacing for dense layouts.

Copy

```
import {
  Field,
  FieldContent,
```

View Code

### Choice Card

Use `FieldLabel` to wrap the entire `Field` for a clickable card-style selection.

Plus

For individuals and small teams.

Pro

For growing businesses.

Enterprise

For large teams and enterprises.

Copy

```
import {
  Field,
  FieldContent,
```

View Code

### Fieldset

Use `FieldSet` and `FieldLegend` to group radio items with a label and description.

Subscription Plan

Yearly and lifetime plans offer significant savings.

Monthly ($9.99/month)

Yearly ($99.99/year)

Lifetime ($299.99)

Copy

```
import {
  Field,
  FieldDescription,
```

View Code

### Disabled

Use the `disabled` prop on `RadioGroupItem` to disable individual items.

Disabled

Option 2

Option 3

Copy

```
import { Field, FieldLabel } from "@/components/ui/field"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
```

View Code

### Invalid

Use `aria-invalid` on `RadioGroupItem` and `data-invalid` on `Field` to show validation errors.

Notification Preferences

Choose how you want to receive notifications.

Email only

SMS only

Both Email & SMS

Copy

```
import {
  Field,
  FieldDescription,
```

View Code

## RTL

To enable RTL support in shadcn/ui, see the [RTL configuration guide](/docs/rtl).

Arabic (العربية)Toggle

افتراضي

تباعد قياسي لمعظم حالات الاستخدام.

مريح

مساحة أكبر بين العناصر.

مضغوط

تباعد أدنى للتخطيطات الكثيفة.

Copy

```
"use client"

import * as React from "react"
```

View Code

## API Reference

See the [Radix UI Radio Group](https://www.radix-ui.com/docs/primitives/components/radio-group#api-reference) documentation.

[Progress](/docs/components/radix/progress)[Resizable](/docs/components/radix/resizable)

On This Page

[Installation](#installation)[Usage](#usage)[Examples](#examples)[Description](#description)[Choice Card](#choice-card)[Fieldset](#fieldset)[Disabled](#disabled)[Invalid](#invalid)[RTL](#rtl)[API Reference](#api-reference)

Deploy your shadcn/ui app on Vercel

Trusted by OpenAI, Sonos, Adobe, and more.

Vercel provides tools and infrastructure to deploy apps and features at scale.

Deploy Now[Deploy to Vercel](https://vercel.com/new?utm_source=shadcn_site&utm_medium=web&utm_campaign=docs_cta_deploy_now_callout)