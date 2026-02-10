# Accordion

Source: https://tremor.so/docs/ui/accordion

---

UI

# Accordion

A vertical stack of clickable headings that expand to show content.

[Radix Docs](https://www.radix-ui.com/primitives/docs/components/accordion)[API Reference](https://www.radix-ui.com/primitives/docs/components/accordion#api-reference)[GitHub](https://github.com/tremorlabs/tremor/tree/main/src/components/Accordion)

Preview

Code

### In the app

### Via browser extension

### Via email forwarding

```
import {Accordion,AccordionContent,AccordionItem,AccordionTrigger,} from '@/components/Accordion';
export const AccordionHero = () => (  <Accordion type="single" className="mx-auto mt-3 max-w-sm" collapsible>    <AccordionItem value="item-1">      <AccordionTrigger>In the app</AccordionTrigger>      <AccordionContent>        <ol className="flex flex-col gap-2">          <li>            <span className="font-semibold text-gray-900 dark:text-gray-50">              Step 1:            </span>{" "}            Tap the Inbox icon and then tap Add receipts.          </li>          <li>            <span className="font-semibold text-gray-900 dark:text-gray-50">              Step 2:            </span>{" "}            Tap the + symbol to attach a photo or PDF of the receipt for our            system to match.          </li>        </ol>      </AccordionContent>    </AccordionItem>    <AccordionItem value="item-2">      <AccordionTrigger>Via browser extension</AccordionTrigger>      <AccordionContent>        <ol className="flex flex-col gap-2">          <li>            <span className="font-semibold text-gray-900 dark:text-gray-50">              Step 1:            </span>{" "}            <span className="underline">Download</span> the browser extension            for Chrome or Safari. (Firefox support is coming soon.)          </li>          <li>            <span className="font-semibold text-gray-900 dark:text-gray-50">              Step 2:            </span>{" "}            Click the extension icon at the top of your browser. Under the            Receipts tab, upload an image or click Screenshot current tab to            automatically attach the receipt to the expense.          </li>        </ol>      </AccordionContent>    </AccordionItem>    <AccordionItem value="item-3" disabled>      <AccordionTrigger>Via email forwarding</AccordionTrigger>      <AccordionContent>        Yes! You can animate the Accordion with CSS or JavaScript.      </AccordionContent>    </AccordionItem>  </Accordion>);
```

## Installation

1. 1

   ### Install dependencies:

   ```
   npm install @radix-ui/react-accordion @remixicon/react
   ```
2. 2

   ### Add component:

   Copy and paste the code into your project’s component directory. Do not forget to update the import paths.

   Show more

   ```
   // Tremor Accordion [v1.0.0]
   import React from "react"import * as AccordionPrimitives from "@radix-ui/react-accordion"import { RiAddLine } from "@remixicon/react"
   import { cx } from "@/lib/utils"
   const Accordion = AccordionPrimitives.Root
   Accordion.displayName = "AccordionItem"
   const AccordionTrigger = React.forwardRef<  React.ElementRef<typeof AccordionPrimitives.Trigger>,  React.ComponentPropsWithoutRef<typeof AccordionPrimitives.Trigger>>(({ className, children, ...props }, forwardedRef) => (  <AccordionPrimitives.Header className="flex">    <AccordionPrimitives.Trigger      className={cx(        // base        "group flex flex-1 cursor-pointer items-center justify-between py-3 text-left text-sm leading-none font-medium",        // text color        "text-gray-900 dark:text-gray-50",        // disabled        "data-disabled:cursor-default data-disabled:text-gray-400 dark:data-disabled:text-gray-600",        //focus        "focus-visible:z-10 focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:outline-hidden focus-visible:ring-inset",        className,      )}      {...props}      ref={forwardedRef}    >      {children}      <RiAddLine        className={cx(          // base          "size-5 shrink-0 transition-transform duration-150 ease-[cubic-bezier(0.87,_0,_0.13,_1)] group-data-[state=open]:-rotate-45",          // text color          "text-gray-400 dark:text-gray-600",          // disabled          "group-data-disabled:text-gray-300 dark:group-data-disabled:text-gray-700",        )}        aria-hidden="true"        focusable="false"      />    </AccordionPrimitives.Trigger>  </AccordionPrimitives.Header>))
   AccordionTrigger.displayName = "AccordionTrigger"
   const AccordionContent = React.forwardRef<  React.ElementRef<typeof AccordionPrimitives.Content>,  React.ComponentPropsWithoutRef<typeof AccordionPrimitives.Content>>(({ className, children, ...props }, forwardedRef) => (  <AccordionPrimitives.Content    ref={forwardedRef}    className={cx(      "data-[state=closed]:animate-accordion-close data-[state=open]:animate-accordion-open transform-gpu",    )}    {...props}  >    <div      className={cx(        // base        "overflow-hidden pb-4 text-sm",        // text color        "text-gray-700 dark:text-gray-200",        className,      )}    >      {children}    </div>  </AccordionPrimitives.Content>))
   AccordionContent.displayName = "AccordionContent"
   const AccordionItem = React.forwardRef<  React.ElementRef<typeof AccordionPrimitives.Item>,  React.ComponentPropsWithoutRef<typeof AccordionPrimitives.Item>>(({ className, ...props }, forwardedRef) => (  <AccordionPrimitives.Item    ref={forwardedRef}    className={cx(      // base      "overflow-hidden border-b first:mt-0",      // border color      "border-gray-200 dark:border-gray-800",      className,    )}    tremor-id="tremor-raw"    {...props}  />))
   AccordionItem.displayName = "AccordionItem"
   export { Accordion, AccordionContent, AccordionItem, AccordionTrigger }
   ```
3. 3

   ### Update globals.css

   ```
   @theme {  --animate-accordion-open: accordionOpen 150ms cubic-bezier(0.87, 0, 0.13, 1);  --animate-accordion-close: accordionClose 150ms cubic-bezier(0.87, 0, 0.13, 1);
     @keyframes accordionOpen {    from {      height: 0px;    }    to {      height: var(--radix-accordion-content-height);    }  }  @keyframes accordionClose {    from {      height: var(--radix-accordion-content-height);    }    to {      height: 0px;    }  }}
   ```

## Example: Multiple items open at the same time

To open more than one item at a time, set the type prop to multiple.

Preview

Code

Managing Your Booking Online

### Access Your Booking

### Change Flights

### Add Special Requests

### Check-In Online

```
import {  Accordion,  AccordionContent,  AccordionItem,  AccordionTrigger,} from '@/components/Accordion';
import {  RiAddCircleFill,  RiArrowLeftRightLine,  RiCheckboxMultipleFill,  RiCoupon3Fill,} from '@remixicon/react';
export const AccordionExample = () => (  <div className="mx-auto max-w-lg">    <h1 className="text-md font-semibold text-gray-900 dark:text-gray-50">      Managing Your Booking Online    </h1>    <Accordion type="multiple" className="mt-3">      <AccordionItem value="item-1">        <AccordionTrigger>          <span className="flex items-center gap-2 ">            <RiCoupon3Fill className="size-4 text-blue-500" />            Access Your Booking          </span>        </AccordionTrigger>        <AccordionContent>          <p>            Simply navigate to the "My Trips" section on our website and input            your booking reference and last name to view your itinerary details.          </p>        </AccordionContent>      </AccordionItem>      <AccordionItem value="item-2">        <AccordionTrigger>          <span className="flex items-center gap-2 ">            <RiArrowLeftRightLine className="size-4 text-blue-500" />            Change Flights          </span>        </AccordionTrigger>        <AccordionContent>          <ol className="flex flex-col gap-2">            <li>              <span className="font-semibold text-gray-900 dark:text-gray-50">                Step 1:              </span>{" "}              Within your booking details, select "Change Flights."            </li>            <li>              <span className="font-semibold text-gray-900 dark:text-gray-50">                Step 2:              </span>{" "}              Follow the prompts to select new flight options and confirm the              changes.            </li>            <li>              <span className="font-semibold text-gray-900 dark:text-gray-50">                Step 3:              </span>{" "}              Review your new flight details and any fare differences.            </li>            <li>              <span className="font-semibold text-gray-900 dark:text-gray-50">                Step 4:              </span>{" "}              Complete the change and receive your updated itinerary via email.            </li>          </ol>        </AccordionContent>      </AccordionItem>      <AccordionItem value="item-3">        <AccordionTrigger>          <span className="flex items-center gap-2 ">            <RiAddCircleFill className="size-4 text-blue-500" />            Add Special Requests          </span>        </AccordionTrigger>        <AccordionContent>          <p>            Look for the "Special Requests" option within your booking to            specify any meal preferences, seating arrangements, or assistance            services you may require during your flight.          </p>        </AccordionContent>      </AccordionItem>      <AccordionItem value="item-4">        <AccordionTrigger>          <span className="flex items-center gap-2 ">            <RiCheckboxMultipleFill className="size-4 text-blue-500" />            Check-In Online          </span>        </AccordionTrigger>        <AccordionContent>          <ol className="flex flex-col gap-2">            <li>              <span className="font-semibold text-gray-900 dark:text-gray-50">                Step 1:              </span>{" "}              Starting 48 hours before your flight, access the "Check-In"              option.            </li>            <li>              <span className="font-semibold text-gray-900 dark:text-gray-50">                Step 2:              </span>{" "}              Confirm your details and select your seats to complete the online              check-in process.            </li>          </ol>        </AccordionContent>      </AccordionItem>    </Accordion>  </div>);
```

## Example: Default open and disabled item

Use the defaultValue prop in <Accordion/> to define the open item by default.

Preview

Code

Managing Your Booking Online

### Access Your Booking

Simply navigate to the "My Trips" section on our website and input your booking reference and last name to view your itinerary details.

### Change Flights

### Add Special Requests

### Check-In Online

```
import {  Accordion,  AccordionContent,  AccordionItem,  AccordionTrigger,} from '@/components/Accordion';
import {  RiAddCircleFill,  RiArrowLeftRightLine,  RiCheckboxMultipleFill,  RiCoupon3Fill,} from '@remixicon/react';
export const AccordionDefaultOpenExample = () => (  <div className="mx-auto max-w-lg">    <h1 className="text-md font-semibold text-gray-900 dark:text-gray-50">      Managing Your Booking Online    </h1>    <Accordion type="single" defaultValue="item-1" className="mt-3" collapsible>      <AccordionItem value="item-1">        <AccordionTrigger>          <span className="flex items-center gap-2 ">            <RiCoupon3Fill className="group-data-[disabled]:texdark:t-blue-200 group-data-[disabled]:t8xt-blue-200 size-4 text-blue-500" />            Access Your Booking          </span>        </AccordionTrigger>        <AccordionContent>          <p>            Simply navigate to the "My Trips" section on our website and input            your booking reference and last name to view your itinerary details.          </p>        </AccordionContent>      </AccordionItem>      <AccordionItem value="item-2">        <AccordionTrigger>          <span className="flex items-center gap-2 ">            <RiArrowLeftRightLine className="size-4 text-blue-500 group-data-disabled:text-blue-200 dark:group-data-disabled:text-blue-900" />            Change Flights          </span>        </AccordionTrigger>        <AccordionContent>          <ol className="flex flex-col gap-2">            <li>              <span className="font-semibold text-gray-900 dark:text-gray-50">                Step 1:              </span>{" "}              Within your booking details, select "Change Flights."            </li>            <li>              <span className="font-semibold text-gray-900 dark:text-gray-50">                Step 2:              </span>{" "}              Follow the prompts to select new flight options and confirm the              changes.            </li>            <li>              <span className="font-semibold text-gray-900 dark:text-gray-50">                Step 3:              </span>{" "}              Review your new flight details and any fare differences.            </li>            <li>              <span className="font-semibold text-gray-900 dark:text-gray-50">                Step 4:              </span>{" "}              Complete the change and receive your updated itinerary via email.            </li>          </ol>        </AccordionContent>      </AccordionItem>      <AccordionItem value="item-3" disabled>        <AccordionTrigger>          <span className="flex items-center gap-2 ">            <RiAddCircleFill className="size-4 text-blue-500 group-data-disabled:text-blue-200 dark:group-data-disabled:text-blue-900" />            Add Special Requests          </span>        </AccordionTrigger>        <AccordionContent>          <p>            Look for the "Special Requests" option within your booking to            specify any meal preferences, seating arrangements, or assistance            services you may require during your flight.          </p>        </AccordionContent>      </AccordionItem>      <AccordionItem value="item-4">        <AccordionTrigger>          <span className="flex items-center gap-2 ">            <RiCheckboxMultipleFill className="size-4 text-blue-500 group-data-disabled:text-blue-200 dark:group-data-disabled:text-blue-900" />            Check-In Online          </span>        </AccordionTrigger>        <AccordionContent>          <ol className="flex flex-col gap-2">            <li>              <span className="font-semibold text-gray-900 dark:text-gray-50">                Step 1:              </span>{" "}              Starting 48 hours before your flight, access the "Check-In"              option.            </li>            <li>              <span className="font-semibold text-gray-900 dark:text-gray-50">                Step 2:              </span>{" "}              Confirm your details and select your seats to complete the online              check-in process.            </li>          </ol>        </AccordionContent>      </AccordionItem>    </Accordion>  </div>);
```

## Example: Controlled accordion

Preview

Code

Open item number two

### In the app

### Via browser extension

### Via email forwarding

```
import React from "react"
import {  Accordion,  AccordionContent,  AccordionItem,  AccordionTrigger,} from '@/components/Accordion';
import { Button } from "@/components/Button"
export const AccordionControlledExample = () => {  const [value, setValue] = React.useState("")
  const handleValueChange = (newValue) => {    // Only update the state if the new value is "item-2"    if (newValue === "item-2" || newValue === "") {      setValue(newValue)    }  }
  return (    <div className="flex flex-col gap-2">      <Button        variant="secondary"        className="w-fit"        onClick={() =>          setValue((prevValue) => (prevValue === "item-2" ? "" : "item-2"))        }      >        {value === "" ? "Open" : "Close"} item number two      </Button>      <Accordion        type="single"        collapsible        value={value}        onValueChange={handleValueChange}      >        <AccordionItem value="item-1">          <AccordionTrigger>In the app</AccordionTrigger>          <AccordionContent>            <ol className="flex flex-col gap-2">              <li>                <span className="font-semibold text-gray-900 dark:text-gray-50">Step 1:</span>{" "}                Tap the Inbox icon and then tap Add receipts.              </li>              <li>                <span className="font-semibold text-gray-900 dark:text-gray-50">Step 2:</span>{" "}                Tap the + symbol to attach a photo or PDF of the receipt for our                system to match.              </li>            </ol>          </AccordionContent>        </AccordionItem>        <AccordionItem value="item-2">          <AccordionTrigger>Via browser extension</AccordionTrigger>          <AccordionContent>            <ol className="flex flex-col gap-2">              <li>                <span className="font-semibold text-gray-900 dark:text-gray-50">Step 1:</span>{" "}                <span className="underline">Download</span> the browser                extension for Chrome or Safari. (Firefox support is coming                soon.)              </li>              <li>                <span className="font-semibold text-gray-900 dark:text-gray-50">Step 2:</span>{" "}                Click the extension icon at the top of your browser. Under the                Receipts tab, upload an image or click Screenshot current tab to                automatically attach the receipt to the expense.              </li>            </ol>          </AccordionContent>        </AccordionItem>        <AccordionItem value="item-3" disabled>          <AccordionTrigger>            <span>Via email forwarding</span>          </AccordionTrigger>          <AccordionContent>            Yes! You can animate the Accordion with CSS or JavaScript.          </AccordionContent>        </AccordionItem>      </Accordion>    </div>  )}
```

## API Reference: Accordion

This component uses the [Radix UI API](https://www.radix-ui.com/primitives/docs/components/accordion#root).

## API Reference: AccordionTrigger

This component uses the [Radix UI API](https://www.radix-ui.com/primitives/docs/components/accordion#trigger).

## API Reference: AccordionItem

This component uses the [Radix UI API](https://www.radix-ui.com/primitives/docs/components/accordion#item).

## API Reference: AccordionContent

This component uses the [Radix UI API](https://www.radix-ui.com/primitives/docs/components/accordion#content).