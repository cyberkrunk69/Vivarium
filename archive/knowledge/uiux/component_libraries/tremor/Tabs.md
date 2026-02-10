# Tabs

Source: https://tremor.so/docs/ui/tabs

---

UI

# Tabs

A collection of content layers called tab panels, shown individually.

[Radix Docs](https://www.radix-ui.com/primitives/docs/components/tabs)[API Reference](https://www.radix-ui.com/primitives/docs/components/tabs#api-reference)[GitHub](https://github.com/tremorlabs/tremor/tree/main/src/components/Tabs)

Preview

Code

ReturnsShipping

You have 60 days from the time we've shipped your order to return any part of it to us for a refund, provided it is still in its original, unused condition: we do not accept returns of used items.

No return authorization (RMA) is required. If you are within the United States, a pre-paid shipping label will be generated. For direct returns, a flat fee of $10 is deducted from your return for shipping and processing costs.

```
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/Tabs"
export const TabsHero = () => (  <Tabs defaultValue="tab1">    <TabsList>      <TabsTrigger value="tab1">Returns</TabsTrigger>      <TabsTrigger value="tab2">Shipping</TabsTrigger>    </TabsList>    <div className="ml-2 mt-4">      <TabsContent        value="tab1"        className="space-y-2 text-sm leading-7 text-gray-600 dark:text-gray-500"      >        <p>          You have 60 days from the time we've shipped your order to return any          part of it to us for a refund, provided it is still in its original,          unused condition: we do not accept returns of used items.        </p>        <p>          No return authorization (RMA) is required. If you are within the          United States, a pre-paid shipping label will be generated. For direct          returns, a flat fee of $10 is deducted from your return for shipping          and processing costs.        </p>      </TabsContent>      <TabsContent        value="tab2"        className="space-y-2 text-sm leading-7 text-gray-600 dark:text-gray-500"      >        <p>          We ship worldwide via UPS Expedited. We offer flat rate shipping to          customers in Canada ($30), the EU, Japan, and Singapore ($45–$65+),          and Australia ($65). Note that most brokerage fees are included in the          price of UPS Expedited shipping, with the exception of a possible $10          fee assessed in Canada only if prior arrangements to pay for duties          and taxes are not made (see next question and answer).        </p>        <p>          Outside of the United States, tariffs, duties, and taxes are the          responsibility of the customer and are usually paid at time of          delivery.        </p>      </TabsContent>    </div>  </Tabs>);
```

## Installation

1. 1

   ### Install dependencies:

   ```
   npm install @radix-ui/react-tabs
   ```
2. 2

   ### Add component:

   Copy and paste the code into your project’s component directory. Do not forget to update the import paths.

   Show more

   ```
   // Tremor Tabs [v1.0.0]
   import React from "react"import * as TabsPrimitives from "@radix-ui/react-tabs"
   import { cx, focusRing } from "@/lib/utils"
   const Tabs = (  props: Omit<    React.ComponentPropsWithoutRef<typeof TabsPrimitives.Root>,    "orientation"  >,) => {  return <TabsPrimitives.Root tremor-id="tremor-raw" {...props} />}
   Tabs.displayName = "Tabs"
   type TabsListVariant = "line" | "solid"
   const TabsListVariantContext = React.createContext<TabsListVariant>("line")
   interface TabsListProps  extends React.ComponentPropsWithoutRef<typeof TabsPrimitives.List> {  variant?: TabsListVariant}
   const variantStyles: Record<TabsListVariant, string> = {  line: cx(    // base    "flex items-center justify-start border-b",    // border color    "border-gray-200 dark:border-gray-800",  ),  solid: cx(    // base    "inline-flex items-center justify-center rounded-md p-1",    // background color    "bg-gray-100 dark:bg-gray-900",  ),}
   const TabsList = React.forwardRef<  React.ElementRef<typeof TabsPrimitives.List>,  TabsListProps>(({ className, variant = "line", children, ...props }, forwardedRef) => (  <TabsPrimitives.List    ref={forwardedRef}    className={cx(variantStyles[variant], className)}    {...props}  >    <TabsListVariantContext.Provider value={variant}>      {children}    </TabsListVariantContext.Provider>  </TabsPrimitives.List>))
   TabsList.displayName = "TabsList"
   function getVariantStyles(tabVariant: TabsListVariant) {  switch (tabVariant) {    case "line":      return cx(        // base        "-mb-px items-center justify-center border-b-2 border-transparent px-3 pb-2 text-sm font-medium whitespace-nowrap transition-all",        // text color        "text-gray-500 dark:text-gray-500",        // hover        "hover:text-gray-700 dark:hover:text-gray-400",        // border hover        "hover:border-gray-300 dark:hover:border-gray-400",        // selected        "data-[state=active]:border-blue-500 data-[state=active]:text-blue-500",        "dark:data-[state=active]:border-blue-500 dark:data-[state=active]:text-blue-500",        // disabled        "data-disabled:pointer-events-none",        "data-disabled:text-gray-300 dark:data-disabled:text-gray-700",      )    case "solid":      return cx(        // base        "inline-flex items-center justify-center rounded-sm px-3 py-1 text-sm font-medium whitespace-nowrap ring-1 transition-all ring-inset",        // text color        "text-gray-500 dark:text-gray-400",        // hover        "hover:text-gray-700 dark:hover:text-gray-200",        // ring        "ring-transparent",        // selected        "data-[state=active]:bg-white data-[state=active]:text-gray-900 data-[state=active]:shadow-sm",        "dark:data-[state=active]:bg-gray-950 dark:data-[state=active]:text-gray-50",        // disabled        "data-disabled:pointer-events-none data-disabled:text-gray-400 data-disabled:opacity-50 dark:data-disabled:text-gray-600",      )  }}
   const TabsTrigger = React.forwardRef<  React.ElementRef<typeof TabsPrimitives.Trigger>,  React.ComponentPropsWithoutRef<typeof TabsPrimitives.Trigger>>(({ className, children, ...props }, forwardedRef) => {  const variant = React.useContext(TabsListVariantContext)  return (    <TabsPrimitives.Trigger      ref={forwardedRef}      className={cx(getVariantStyles(variant), focusRing, className)}      {...props}    >      {children}    </TabsPrimitives.Trigger>  )})
   TabsTrigger.displayName = "TabsTrigger"
   const TabsContent = React.forwardRef<  React.ElementRef<typeof TabsPrimitives.Content>,  React.ComponentPropsWithoutRef<typeof TabsPrimitives.Content>>(({ className, ...props }, forwardedRef) => (  <TabsPrimitives.Content    ref={forwardedRef}    className={cx("outline-hidden", focusRing, className)}    {...props}  />))
   TabsContent.displayName = "TabsContent"
   export { Tabs, TabsContent, TabsList, TabsTrigger }
   ```

## Example: Tabs solid variant

Preview

Code

ReturnsShipping

You have 60 days from the time we've shipped your order to return any part of it to us for a refund, provided it is still in its original, unused condition: we do not accept returns of used items.

No return authorization (RMA) is required. If you are within the United States, a pre-paid shipping label will be generated. For direct returns, a flat fee of $10 is deducted from your return for shipping and processing costs.

```
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/Tabs"
export const TabsExample = () => (  <Tabs defaultValue="tab1">    <TabsList variant="solid">      <TabsTrigger value="tab1">Returns</TabsTrigger>      <TabsTrigger value="tab2">Shipping</TabsTrigger>    </TabsList>    <div className="ml-2 mt-4">      <TabsContent        value="tab1"        className="space-y-2 text-sm leading-7 text-gray-600 dark:text-gray-500"      >        <p>          You have 60 days from the time we've shipped your order to return any          part of it to us for a refund, provided it is still in its original,          unused condition: we do not accept returns of used items.        </p>        <p>          No return authorization (RMA) is required. If you are within the          United States, a pre-paid shipping label will be generated. For direct          returns, a flat fee of $10 is deducted from your return for shipping          and processing costs.        </p>      </TabsContent>      <TabsContent        value="tab2"        className="space-y-2 text-sm leading-7 text-gray-600 dark:text-gray-500"      >        <p>          We ship worldwide via UPS Expedited. We offer flat rate shipping to          customers in Canada ($30), the EU, Japan, and Singapore ($45–$65+),          and Australia ($65). Note that most brokerage fees are included in the          price of UPS Expedited shipping, with the exception of a possible $10          fee assessed in Canada only if prior arrangements to pay for duties          and taxes are not made (see next question and answer).        </p>        <p>          Outside of the United States, tariffs, duties, and taxes are the          responsibility of the customer and are usually paid at time of          delivery.        </p>      </TabsContent>    </div>  </Tabs>);
```

## Example: Tabs with disabled trigger

Preview

Code

Tab 1Tab 2Tab 3

Tab 1 content

```
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/Tabs"
export const TabsDisabledExample = () => (  <Tabs defaultValue="tab1">    <TabsList variant="line">      <TabsTrigger value="tab1">Tab 1</TabsTrigger>      <TabsTrigger value="tab2">Tab 2</TabsTrigger>      <TabsTrigger value="tab3" disabled>        Tab 3      </TabsTrigger>    </TabsList>    <div className="mt-4">      <TabsContent value="tab1">        <p className="text-sm text-gray-500 sm:text-gray-500">Tab 1 content</p>      </TabsContent>      <TabsContent value="tab2">        <p className="text-sm text-gray-500 sm:text-gray-500">Tab 2 content</p>      </TabsContent>      <TabsContent value="tab3">        <p className="text-sm text-gray-500 sm:text-gray-500">Tab 3 content</p>      </TabsContent>    </div>  </Tabs>);
```

## Example: Tabs with icons

Preview

Code

Pic locationCalculate location

Tab 1 content

Pic locationCalculate location

Tab 1 content

```
import { RiCalculatorLine, RiMapPin2Line } from "@remixicon/react"import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/Tabs"import {  Tabs,  TabsContent,  TabsList,  TabsTrigger,} from "@/components/Tabs"
export const TabsWithIconsExample = () => (  <div className="flex flex-col gap-12">    <Tabs defaultValue="tab1">      <TabsList variant="line">        <TabsTrigger value="tab1" className="inline-flex gap-2">          <RiMapPin2Line className="-ml-1 size-4" aria-hidden="true" />          Pic location        </TabsTrigger>        <TabsTrigger value="tab2" className="inline-flex gap-2">          <RiCalculatorLine className="-ml-1 size-4" aria-hidden="true" />          Calculate location        </TabsTrigger>      </TabsList>      <div className="mt-4">        <TabsContent value="tab1">          <p className="text-sm text-gray-500 sm:text-gray-500">            Tab 1 content          </p>        </TabsContent>        <TabsContent value="tab2">          <p className="text-sm text-gray-500 sm:text-gray-500">            Tab 2 content          </p>        </TabsContent>      </div>    </Tabs>    <Tabs defaultValue="tab1">      <TabsList variant="solid">        <TabsTrigger value="tab1" className="gap-1.5">          <RiMapPin2Line className="-ml-1 size-4" aria-hidden="true" />          Pic location        </TabsTrigger>        <TabsTrigger value="tab2" className="gap-1.5">          <RiCalculatorLine className="-ml-1 size-4" aria-hidden="true" />          Calculate location        </TabsTrigger>      </TabsList>      <div className="mt-4">        <TabsContent value="tab1">          <p className="text-sm text-gray-500 sm:text-gray-500">            Tab 1 content          </p>        </TabsContent>        <TabsContent value="tab2">          <p className="text-sm text-gray-500 sm:text-gray-500">            Tab 2 content          </p>        </TabsContent>      </div>    </Tabs>  </div>);
```

## Example: Streched tabs

Preview

Code

Tab 1Tab 2Tab 3

Tab 1 content

Tab 1Tab 2Tab 3

Tab 1 content

```
import {  Tabs,  TabsContent,  TabsList,  TabsTrigger,} from "@/components/Tabs"
export const TabsStretchWidthExample = () => (  <div className="flex flex-col gap-6">    <Tabs defaultValue="tab1">      <TabsList className="grid w-full grid-cols-3" variant="line">        <TabsTrigger value="tab1">Tab 1</TabsTrigger>        <TabsTrigger value="tab2">Tab 2</TabsTrigger>        <TabsTrigger value="tab3">Tab 3</TabsTrigger>      </TabsList>      <div className="mt-4">        <TabsContent value="tab1">          <p className="text-sm text-gray-500 sm:text-gray-500">            Tab 1 content          </p>        </TabsContent>        <TabsContent value="tab2">          <p className="text-sm text-gray-500 sm:text-gray-500">            Tab 2 content          </p>        </TabsContent>        <TabsContent value="tab3">          <p className="text-sm text-gray-500 sm:text-gray-500">            Tab 3 content          </p>        </TabsContent>      </div>    </Tabs>    <Tabs defaultValue="tab1">      <TabsList className="grid w-full grid-cols-3" variant="solid">        <TabsTrigger value="tab1">Tab 1</TabsTrigger>        <TabsTrigger value="tab2">Tab 2</TabsTrigger>        <TabsTrigger value="tab3">Tab 3</TabsTrigger>      </TabsList>      <div className="mt-4">        <TabsContent value="tab1">          <p className="text-sm text-gray-500 sm:text-gray-500">            Tab 1 content          </p>        </TabsContent>        <TabsContent value="tab2">          <p className="text-sm text-gray-500 sm:text-gray-500">            Tab 2 content          </p>        </TabsContent>        <TabsContent value="tab3">          <p className="text-sm text-gray-500 sm:text-gray-500">            Tab 3 content          </p>        </TabsContent>      </div>    </Tabs>  </div>);
```

## API Reference: Tabs

This component uses the [Radix UI API](https://www.radix-ui.com/primitives/docs/components/tabs#root).

Note: The orientation prop has been removed.

## API Reference: TabsList

This component uses the [Radix UI API](https://www.radix-ui.com/primitives/docs/components/tabs#list).

variant

"line" | "solid"

:   Set a predefined look.

Default: "line"

## API Reference: TabsTrigger

This component uses the [Radix UI API](https://www.radix-ui.com/primitives/docs/components/tabs#trigger).

## API Reference: TabsContent

This component uses the [Radix UI API](https://www.radix-ui.com/primitives/docs/components/tabs#content).