# Table

Source: https://ui.shadcn.com/docs/components/table

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

# Table

Copy Page

[Previous](/docs/components/radix/switch)[Next](/docs/components/radix/tabs)

A responsive table component.

[Radix UI](/docs/components/radix/table)[Base UI](/docs/components/base/table)

A list of your recent invoices.

| Invoice | Status | Method | Amount |
| --- | --- | --- | --- |
| INV001 | Paid | Credit Card | $250.00 |
| INV002 | Pending | PayPal | $150.00 |
| INV003 | Unpaid | Bank Transfer | $350.00 |
| INV004 | Paid | Credit Card | $450.00 |
| INV005 | Paid | PayPal | $550.00 |
| INV006 | Pending | Bank Transfer | $200.00 |
| INV007 | Unpaid | Credit Card | $300.00 |
|  |  |  |  |
| --- | --- | --- | --- |
| Total | | | $2,500.00 |

Copy

```
import {
  Table,
  TableBody,
```

View Code

## Installation

CommandManual

```
pnpmnpmyarnbun

```
pnpm dlx shadcn@latest add table
```

Copy
```

## Usage

```
Copyimport {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
```

```
Copy<Table>
  <TableCaption>A list of your recent invoices.</TableCaption>
  <TableHeader>
    <TableRow>
      <TableHead className="w-[100px]">Invoice</TableHead>
      <TableHead>Status</TableHead>
      <TableHead>Method</TableHead>
      <TableHead className="text-right">Amount</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    <TableRow>
      <TableCell className="font-medium">INV001</TableCell>
      <TableCell>Paid</TableCell>
      <TableCell>Credit Card</TableCell>
      <TableCell className="text-right">$250.00</TableCell>
    </TableRow>
  </TableBody>
</Table>
```

## Examples

### Footer

Use the `<TableFooter />` component to add a footer to the table.

A list of your recent invoices.

| Invoice | Status | Method | Amount |
| --- | --- | --- | --- |
| INV001 | Paid | Credit Card | $250.00 |
| INV002 | Pending | PayPal | $150.00 |
| INV003 | Unpaid | Bank Transfer | $350.00 |
|  |  |  |  |
| --- | --- | --- | --- |
| Total | | | $2,500.00 |

Copy

```
import {
  Table,
  TableBody,
```

View Code

### Actions

A table showing actions for each row using a `<DropdownMenu />` component.

| Product | Price | Actions |
| --- | --- | --- |
| Wireless Mouse | $29.99 | Open menu |
| Mechanical Keyboard | $129.99 | Open menu |
| USB-C Hub | $49.99 | Open menu |

Copy

```
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
```

View Code

## Data Table

You can use the `<Table />` component to build more complex data tables. Combine it with [@tanstack/react-table](https://tanstack.com/table/v8) to create tables with sorting, filtering and pagination.

See the [Data Table](/docs/components/data-table) documentation for more information.

You can also see an example of a data table in the [Tasks](/examples/tasks) demo.

## RTL

To enable RTL support in shadcn/ui, see the [RTL configuration guide](/docs/rtl).

Arabic (العربية)Toggle

قائمة بفواتيرك الأخيرة.

| الفاتورة | الحالة | الطريقة | المبلغ |
| --- | --- | --- | --- |
| INV001 | مدفوع | بطاقة ائتمانية | $250.00 |
| INV002 | قيد الانتظار | PayPal | $150.00 |
| INV003 | غير مدفوع | تحويل بنكي | $350.00 |
| INV004 | مدفوع | بطاقة ائتمانية | $450.00 |
| INV005 | مدفوع | PayPal | $550.00 |
| INV006 | قيد الانتظار | تحويل بنكي | $200.00 |
| INV007 | غير مدفوع | بطاقة ائتمانية | $300.00 |
|  |  |  |  |
| --- | --- | --- | --- |
| المجموع | | | $2,500.00 |

Copy

```
"use client"

import * as React from "react"
```

View Code

[Switch](/docs/components/radix/switch)[Tabs](/docs/components/radix/tabs)

On This Page

[Installation](#installation)[Usage](#usage)[Examples](#examples)[Footer](#footer)[Actions](#actions)[Data Table](#data-table)[RTL](#rtl)

Deploy your shadcn/ui app on Vercel

Trusted by OpenAI, Sonos, Adobe, and more.

Vercel provides tools and infrastructure to deploy apps and features at scale.

Deploy Now[Deploy to Vercel](https://vercel.com/new?utm_source=shadcn_site&utm_medium=web&utm_campaign=docs_cta_deploy_now_callout)