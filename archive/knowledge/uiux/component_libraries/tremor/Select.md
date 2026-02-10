# Select

Source: https://tremor.so/docs/ui/select

---

Inputs

# Select

List of user-selectable options, triggered by a button.

[Radix Docs](https://www.radix-ui.com/primitives/docs/components/select)[API Reference](https://www.radix-ui.com/primitives/docs/components/select#api-reference)[GitHub](https://github.com/tremorlabs/tremor/tree/main/src/components/Select)

Preview

Code

Select

```
import {  Select,  SelectContent,  SelectItem,  SelectTrigger,  SelectValue,} from "@/components/Select"
export function SelectHero() {  const data = [    {      value: "dress-shirt-striped",      label: "Striped Dress Shirt",    },    {      value: "relaxed-button-down",      label: "Relaxed Fit Button Down",    },    {      value: "slim-button-down",      label: "Slim Fit Button Down",    },    {      value: "dress-shirt-solid",      label: "Solid Dress Shirt",    },    {      value: "dress-shirt-check",      label: "Check Dress Shirt",    },  ]
  return (    <Select>      <SelectTrigger>        <SelectValue placeholder="Select" />      </SelectTrigger>      <SelectContent>        {data.map((item) => (          <SelectItem key={item.value} value={item.value}>            {item.label}          </SelectItem>        ))}      </SelectContent>    </Select>  )}
```

## Installation

1. 1

   ### Install dependencies:

   ```
   npm install @radix-ui/react-select
   ```
2. 2

   ### Add component:

   Copy and paste the code into your project’s component directory. Do not forget to update the import paths.

   Show more

   ```
   // Tremor Select [v1.0.0]
   import React from "react"import * as SelectPrimitives from "@radix-ui/react-select"import {  RiArrowDownSLine,  RiArrowUpSLine,  RiCheckLine,  RiExpandUpDownLine,} from "@remixicon/react"
   import { cx, focusInput, hasErrorInput } from "@/lib/utils"
   const Select = SelectPrimitives.RootSelect.displayName = "Select"
   const SelectGroup = SelectPrimitives.GroupSelectGroup.displayName = "SelectGroup"
   const SelectValue = SelectPrimitives.ValueSelectValue.displayName = "SelectValue"
   const selectTriggerStyles = [  cx(    // base    "group/trigger flex w-full select-none items-center justify-between gap-2 truncate rounded-md border px-3 py-2 shadow-xs outline-hidden transition sm:text-sm",    // border color    "border-gray-300 dark:border-gray-800",    // text color    "text-gray-900 dark:text-gray-50",    // placeholder    "data-placeholder:text-gray-500 dark:data-placeholder:text-gray-500",    // background color    "bg-white dark:bg-gray-950",    // hover    "hover:bg-gray-50 dark:hover:bg-gray-950/50",    // disabled    "data-disabled:bg-gray-100 data-disabled:text-gray-400",    "dark:data-disabled:border-gray-700 dark:data-disabled:bg-gray-800 dark:data-disabled:text-gray-500",    focusInput,    // invalid (optional)    // "dark:aria-invalid:ring-red-400/20 aria-invalid:ring-2 aria-invalid:ring-red-200 aria-invalid:border-red-500 invalid:ring-2 invalid:ring-red-200 invalid:border-red-500"  ),]
   const SelectTrigger = React.forwardRef<  React.ElementRef<typeof SelectPrimitives.Trigger>,  React.ComponentPropsWithoutRef<typeof SelectPrimitives.Trigger> & {    hasError?: boolean  }>(({ className, hasError, children, ...props }, forwardedRef) => {  return (    <SelectPrimitives.Trigger      ref={forwardedRef}      className={cx(        selectTriggerStyles,        hasError ? hasErrorInput : "",        className,      )}      tremor-id="tremor-raw"      {...props}    >      <span className="truncate">{children}</span>      <SelectPrimitives.Icon asChild>        <RiExpandUpDownLine          className={cx(            // base            "size-4 shrink-0",            // text color            "text-gray-400 dark:text-gray-600",            // disabled            "group-data-disabled/trigger:text-gray-300 dark:group-data-disabled/trigger:text-gray-600",          )}        />      </SelectPrimitives.Icon>    </SelectPrimitives.Trigger>  )})
   SelectTrigger.displayName = "SelectTrigger"
   const SelectScrollUpButton = React.forwardRef<  React.ElementRef<typeof SelectPrimitives.ScrollUpButton>,  React.ComponentPropsWithoutRef<typeof SelectPrimitives.ScrollUpButton>>(({ className, ...props }, forwardedRef) => (  <SelectPrimitives.ScrollUpButton    ref={forwardedRef}    className={cx(      "flex cursor-default items-center justify-center py-1",      className,    )}    {...props}  >    <RiArrowUpSLine className="size-3 shrink-0" aria-hidden="true" />  </SelectPrimitives.ScrollUpButton>))SelectScrollUpButton.displayName = SelectPrimitives.ScrollUpButton.displayName
   const SelectScrollDownButton = React.forwardRef<  React.ElementRef<typeof SelectPrimitives.ScrollDownButton>,  React.ComponentPropsWithoutRef<typeof SelectPrimitives.ScrollDownButton>>(({ className, ...props }, forwardedRef) => (  <SelectPrimitives.ScrollDownButton    ref={forwardedRef}    className={cx(      "flex cursor-default items-center justify-center py-1",      className,    )}    {...props}  >    <RiArrowDownSLine className="size-3 shrink-0" aria-hidden="true" />  </SelectPrimitives.ScrollDownButton>))SelectScrollDownButton.displayName =  SelectPrimitives.ScrollDownButton.displayName
   const SelectContent = React.forwardRef<  React.ElementRef<typeof SelectPrimitives.Content>,  React.ComponentPropsWithoutRef<typeof SelectPrimitives.Content>>(  (    {      className,      position = "popper",      children,      sideOffset = 8,      collisionPadding = 10,      ...props    },    forwardedRef,  ) => (    <SelectPrimitives.Portal>      <SelectPrimitives.Content        ref={forwardedRef}        className={cx(          // base          "relative z-50 overflow-hidden rounded-md border shadow-xl shadow-black/[2.5%]",          // widths          "min-w-[calc(var(--radix-select-trigger-width)-2px)] max-w-[95vw]",          // heights          "max-h-(--radix-select-content-available-height)",          // background color          "bg-white dark:bg-gray-950",          // text color          "text-gray-900 dark:text-gray-50",          // border color          "border-gray-200 dark:border-gray-800",          // transition          "will-change-[transform,opacity]",          // "data-[state=open]:animate-slide-down-and-fade",          "data-[state=closed]:animate-hide",          "data-[side=bottom]:animate-slide-down-and-fade data-[side=left]:animate-slide-left-and-fade data-[side=right]:animate-slide-right-and-fade data-[side=top]:animate-slide-up-and-fade",          className,        )}        sideOffset={sideOffset}        position={position}        collisionPadding={collisionPadding}        {...props}      >        <SelectScrollUpButton />        <SelectPrimitives.Viewport          className={cx(            "p-1",            position === "popper" &&            "h-[var(--radix-select-trigger-height)] w-full min-w-[calc(var(--radix-select-trigger-width))]",          )}        >          {children}        </SelectPrimitives.Viewport>        <SelectScrollDownButton />      </SelectPrimitives.Content>    </SelectPrimitives.Portal>  ),)
   SelectContent.displayName = "SelectContent"
   const SelectGroupLabel = React.forwardRef<  React.ElementRef<typeof SelectPrimitives.Label>,  React.ComponentPropsWithoutRef<typeof SelectPrimitives.Label>>(({ className, ...props }, forwardedRef) => (  <SelectPrimitives.Label    ref={forwardedRef}    className={cx(      // base      "px-3 py-2 text-xs font-medium tracking-wide",      // text color      "text-gray-500 dark:text-gray-500",      className,    )}    {...props}  />))
   SelectGroupLabel.displayName = "SelectGroupLabel"
   const SelectItem = React.forwardRef<  React.ElementRef<typeof SelectPrimitives.Item>,  React.ComponentPropsWithoutRef<typeof SelectPrimitives.Item>>(({ className, children, ...props }, forwardedRef) => {  return (    <SelectPrimitives.Item      ref={forwardedRef}      className={cx(        // base        "grid cursor-pointer grid-cols-[1fr_20px] gap-x-2 rounded-sm px-3 py-2 outline-hidden transition-colors data-[state=checked]:font-semibold sm:text-sm",        // text color        "text-gray-900 dark:text-gray-50",        // disabled        "data-disabled:pointer-events-none data-disabled:text-gray-400 data-disabled:hover:bg-none dark:data-disabled:text-gray-600",        // focus        "focus-visible:bg-gray-100 dark:focus-visible:bg-gray-900",        // hover        "hover:bg-gray-100 dark:hover:bg-gray-900",        className,      )}      {...props}    >      <SelectPrimitives.ItemText className="flex-1 truncate">        {children}      </SelectPrimitives.ItemText>      <SelectPrimitives.ItemIndicator>        <RiCheckLine          className="size-5 shrink-0 text-gray-800 dark:text-gray-200"          aria-hidden="true"        />      </SelectPrimitives.ItemIndicator>    </SelectPrimitives.Item>  )})
   SelectItem.displayName = "SelectItem"
   const SelectSeparator = React.forwardRef<  React.ElementRef<typeof SelectPrimitives.Separator>,  React.ComponentPropsWithoutRef<typeof SelectPrimitives.Separator>>(({ className, ...props }, forwardedRef) => (  <SelectPrimitives.Separator    ref={forwardedRef}    className={cx(      // base      "-mx-1 my-1 h-px",      // background color      "bg-gray-300 dark:bg-gray-700",      className,    )}    {...props}  />))
   SelectSeparator.displayName = "SelectSeparator"
   export {  Select,  SelectContent,  SelectGroup,  SelectGroupLabel,  SelectItem,  SelectSeparator,  SelectTrigger,  SelectValue,}
   ```
3. 3

   ### Update globals.css

   Show more

   ```
   @theme {  --animate-hide: hide 150ms cubic-bezier(0.16, 1, 0.3, 1);  --animate-slide-down-and-fade: slideDownAndFade 150ms cubic-bezier(0.16, 1, 0.3, 1);  --animate-slide-left-and-fade: slideLeftAndFade 150ms cubic-bezier(0.16, 1, 0.3, 1);  --animate-slide-up-and-fade: slideUpAndFade 150ms cubic-bezier(0.16, 1, 0.3, 1);  --animate-slide-right-and-fade: slideRightAndFade 150ms cubic-bezier(0.16, 1, 0.3, 1);
     @keyframes hide {    from {      opacity: 1;    }    to {      opacity: 0;    }  }  @keyframes slideDownAndFade {    from {      opacity: 0;      transform: translateY(-6px);    }    to {      opacity: 1;      transform: translateY(0);    }  }  @keyframes slideLeftAndFade {    from {      opacity: 0;      transform: translateX(6px);    }    to {      opacity: 1;      transform: translateX(0);    }  }  @keyframes slideUpAndFade {    from {      opacity: 0;      transform: translateY(6px);    }    to {      opacity: 1;      transform: translateY(0);    }  }  @keyframes slideRightAndFade {    from {      opacity: 0;      transform: translateX(-6px);    }    to {      opacity: 1;      transform: translateX(0);    }  }}
   ```

## Example: Select with label

Preview

Code

Select sizeSelect

```
import { Label } from "@/components/Label"import {  Select,  SelectContent,  SelectItem,  SelectTrigger,  SelectValue,} from "@/components/Select"
export function SelectLabelExample() {  const data = [    {      value: "dress-shirt-striped",      label: "Striped Dress Shirt",    },    {      value: "relaxed-button-down",      label: "Relaxed Fit Button Down",    },    {      value: "slim-button-down",      label: "Slim Fit Button Down",    },    {      value: "dress-shirt-solid",      label: "Solid Dress Shirt",    },    {      value: "dress-shirt-check",      label: "Check Dress Shirt",    },  ]
  return (    <>      <Label htmlFor="size">Select size</Label>      <Select>        <SelectTrigger id="size" className="mt-2">          <SelectValue placeholder="Select" />        </SelectTrigger>        <SelectContent>          {data.map((item) => (            <SelectItem key={item.value} value={item.value}>              {item.label}            </SelectItem>          ))}        </SelectContent>      </Select>    </>  )}
```

## Example: Select with defaultValue

Preview

Code

```
import {  Select,  SelectContent,  SelectItem,  SelectTrigger,  SelectValue,} from "@/components/Select"
export function SelectDefaultExample() {  const data = [    {      value: "living-area",      label: "Living area",    },    {      value: "shopping-area",      label: "Shopping area",    },    {      value: "business-park",      label: "Business park",    },  ]
  return (    <>      <Select defaultValue="living-area">        <SelectTrigger className="mx-auto">          <SelectValue placeholder="Select" />        </SelectTrigger>        <SelectContent>          {data.map((item) => (            <SelectItem key={item.value} value={item.value}>              {item.label}            </SelectItem>          ))}        </SelectContent>      </Select>    </>  )}
```

## Example: Select with disabled state

Preview

Code

Select

```
import {  Select,  SelectContent,  SelectItem,  SelectTrigger,  SelectValue,} from "@/components/Select"
export function SelectDisabledExample() {  const data = [    {      value: "dress-shirt-striped",      label: "Striped Dress Shirt",    },    {      value: "relaxed-button-down",      label: "Relaxed Fit Button Down",    },    {      value: "slim-button-down",      label: "Slim Fit Button Down",    },    {      value: "dress-shirt-solid",      label: "Solid Dress Shirt",    },    {      value: "dress-shirt-check",      label: "Check Dress Shirt",    },  ]
  return (    <>      <Select disabled>        <SelectTrigger id="size-disabled">          <SelectValue placeholder="Select" />        </SelectTrigger>        <SelectContent>          {data.map((item) => (            <SelectItem key={item.value} value={item.value}>              {item.label}            </SelectItem>          ))}        </SelectContent>      </Select>    </>  )}
```

## Example: Select with disabled select item

Preview

Code

Select

```
import {  Select,  SelectContent,  SelectItem,  SelectTrigger,  SelectValue,} from "@/components/Select"
export function SelectDisabledItemExample() {  const data = [    {      value: "dress-shirt-striped",      label: "Striped Dress Shirt",    },    {      value: "relaxed-button-down",      label: "Relaxed Fit Button Down",    },    {      value: "slim-button-down",      label: "Slim Fit Button Down",    },    {      value: "dress-shirt-solid",      label: "Solid Dress Shirt",      disabled: true,    },    {      value: "dress-shirt-check",      label: "Check Dress Shirt",    },  ]
  return (    <>      <Select>        <SelectTrigger id="size-disabled">          <SelectValue placeholder="Select" />        </SelectTrigger>        <SelectContent>          {data.map((item) => (            <SelectItem              key={item.value}              value={item.value}              disabled={item.disabled}            >              {item.label}            </SelectItem>          ))}        </SelectContent>      </Select>    </>  )}
```

## Example: Select with groups

Preview

Code

Select size

Select

```
import { Label } from "@/components/Label"
import {  Select,  SelectContent,  SelectGroup,  SelectGroupLabel,  SelectItem,  SelectTrigger,  SelectValue,} from "@/components/Select"
export function SelectGroupExample() {  const data = [    {      label: "Shirts",      items: [        {          value: "dress-shirt-striped",          label: "Striped Dress Shirt",        },        {          value: "relaxed-button-down",          label: "Relaxed Fit Button Down",        },        {          value: "slim-button-down",          label: "Slim Fit Button Down",        },        {          value: "dress-shirt-solid",          label: "Solid Dress Shirt",        },        {          value: "dress-shirt-check",          label: "Check Dress Shirt",        },      ],    },    {      label: "T-Shirts",      items: [        {          value: "v-neck",          label: "V-Neck",        },        {          value: "crew-neck",          label: "Crew Neck",        },        {          value: "henley",          label: "Henley",        },        {          value: "polo",          label: "Polo",        },        {          value: "mock-neck",          label: "Mock Neck",        },        {          value: "turtleneck",          label: "Turtleneck",        },        {          value: "scoop-neck",          label: "Scoop Neck",        },      ],    },  ]
  return (    <>      <div className="flex justify-center">        <div className="space-y-2">          <Label htmlFor="group">Select size</Label>          <div className="w-[250px]">            <Select>              <SelectTrigger id="group">                <SelectValue placeholder="Select" />              </SelectTrigger>              <SelectContent>                {data.map((group) => (                  <SelectGroup key={group.label}>                    <SelectGroupLabel>{group.label}</SelectGroupLabel>                    {group.items.map((item) => (                      <SelectItem key={item.value} value={item.value}>                        {item.label}                      </SelectItem>                    ))}                  </SelectGroup>                ))}              </SelectContent>            </Select>          </div>        </div>      </div>    </>  )}
```

## Example: Select with scroll and custom height

Preview

Code

Select a timezone

```
import {  Select,  SelectContent,  SelectGroup,  SelectGroupLabel,  SelectItem,  SelectTrigger,  SelectValue,} from "@/components/Select"
export function SelectScrollExample() {  return (    <Select>      <SelectTrigger className="mx-auto w-[250px]">        <SelectValue placeholder="Select a timezone" />      </SelectTrigger>      <SelectContent>        <SelectGroup>          <SelectGroupLabel>North America</SelectGroupLabel>          <SelectItem value="est">Eastern Standard Time (EST)</SelectItem>          <SelectItem value="cst">Central Standard Time (CST)</SelectItem>          <SelectItem value="mst">Mountain Standard Time (MST)</SelectItem>          <SelectItem value="pst">Pacific Standard Time (PST)</SelectItem>          <SelectItem value="akst">Alaska Standard Time (AKST)</SelectItem>          <SelectItem value="hst">Hawaii Standard Time (HST)</SelectItem>        </SelectGroup>        <SelectGroup>          <SelectGroupLabel>Europe & Africa</SelectGroupLabel>          <SelectItem value="gmt">Greenwich Mean Time (GMT)</SelectItem>          <SelectItem value="cet">Central European Time (CET)</SelectItem>          <SelectItem value="eet">Eastern European Time (EET)</SelectItem>          <SelectItem value="west">            Western European Summer Time (WEST)          </SelectItem>          <SelectItem value="cat">Central Africa Time (CAT)</SelectItem>          <SelectItem value="eat">East Africa Time (EAT)</SelectItem>        </SelectGroup>        <SelectGroup>          <SelectGroupLabel>Asia</SelectGroupLabel>          <SelectItem value="msk">Moscow Time (MSK)</SelectItem>          <SelectItem value="ist">India Standard Time (IST)</SelectItem>          <SelectItem value="cst_china">China Standard Time (CST)</SelectItem>          <SelectItem value="jst">Japan Standard Time (JST)</SelectItem>          <SelectItem value="kst">Korea Standard Time (KST)</SelectItem>          <SelectItem value="ist_indonesia">            Indonesia Central Standard Time (WITA)          </SelectItem>        </SelectGroup>        <SelectGroup>          <SelectGroupLabel>Australia & Pacific</SelectGroupLabel>          <SelectItem value="awst">            Australian Western Standard Time (AWST)          </SelectItem>          <SelectItem value="acst">            Australian Central Standard Time (ACST)          </SelectItem>          <SelectItem value="aest">            Australian Eastern Standard Time (AEST)          </SelectItem>          <SelectItem value="nzst">New Zealand Standard Time (NZST)</SelectItem>          <SelectItem value="fjt">Fiji Time (FJT)</SelectItem>        </SelectGroup>        <SelectGroup>          <SelectGroupLabel>South America</SelectGroupLabel>          <SelectItem value="art">Argentina Time (ART)</SelectItem>          <SelectItem value="bot">Bolivia Time (BOT)</SelectItem>          <SelectItem value="brt">Brasilia Time (BRT)</SelectItem>          <SelectItem value="clt">Chile Standard Time (CLT)</SelectItem>        </SelectGroup>      </SelectContent>    </Select>  )}
```

## Example: Select with Dialog

Preview

Code

Open Dialog

```
import { Button } from "@/components/Button"
import {  Dialog,  DialogClose,  DialogContent,  DialogDescription,  DialogFooter,  DialogHeader,  DialogTitle,  DialogTrigger,} from "@/components/Dialog"
import {  Select,  SelectContent,  SelectGroup,  SelectGroupLabel,  SelectItem,  SelectTrigger,  SelectValue,} from "@/components/Select"
export function SelectDialogExample() {  const data3 = [    {      label: "Shirts",      items: [        {          value: "dress-shirt-striped",          label: "Striped Dress Shirt",        },        {          value: "relaxed-button-down",          label: "Relaxed Fit Button Down",        },        {          value: "slim-button-down",          label: "Slim Fit Button Down",        },        {          value: "dress-shirt-solid",          label: "Solid Dress Shirt",        },        {          value: "dress-shirt-check",          label: "Check Dress Shirt",        },      ],    },    {      label: "T-Shirts",      items: [        {          value: "v-neck",          label: "V-Neck",        },        {          value: "crew-neck",          label: "Crew Neck",        },        {          value: "henley",          label: "Henley",        },        {          value: "polo",          label: "Polo",        },        {          value: "mock-neck",          label: "Mock Neck",        },        {          value: "turtleneck",          label: "Turtleneck",        },        {          value: "scoop-neck",          label: "Scoop Neck",        },      ],    },  ]
  return (    <div className="flex justify-center">      <Dialog>        <DialogTrigger asChild>          <Button>Open Dialog</Button>        </DialogTrigger>        <DialogContent className="sm:max-w-sm">          <DialogHeader>            <DialogTitle>Select shirt size</DialogTitle>            <DialogDescription className="text-sm leading-7">              Shirt type            </DialogDescription>            <Select>              <SelectTrigger>                <SelectValue placeholder="Select" />              </SelectTrigger>              <SelectContent>                {data3.map((group) => (                  <SelectGroup key={group.label}>                    <SelectGroupLabel>{group.label}</SelectGroupLabel>                    {group.items.map((item) => (                      <SelectItem key={item.value} value={item.value}>                        {item.label}                      </SelectItem>                    ))}                  </SelectGroup>                ))}              </SelectContent>            </Select>          </DialogHeader>          <DialogFooter className="mt-6">            <DialogClose asChild>              <Button                className="mt-2 w-full sm:mt-0 sm:w-fit"                variant="secondary"              >                Go back              </Button>            </DialogClose>            <DialogClose asChild>              <Button className="w-full sm:w-fit">Ok, got it!</Button>            </DialogClose>          </DialogFooter>        </DialogContent>      </Dialog>    </div>  )}
```

## Example: Select with error state

To style the Select for an error state, use the hasError prop.

Preview

Code

Select

```
import {  Select,  SelectContent,  SelectItem,  SelectTrigger,  SelectValue,} from "@/components/Select"
export function SelectHasErrorExample() {  const data = [    {      value: "dress-shirt-striped",      label: "Striped Dress Shirt",    },    {      value: "relaxed-button-down",      label: "Relaxed Fit Button Down",    },    {      value: "slim-button-down",      label: "Slim Fit Button Down",    },    {      value: "dress-shirt-solid",      label: "Solid Dress Shirt",    },    {      value: "dress-shirt-check",      label: "Check Dress Shirt",    },  ]
  return (    <Select>      <SelectTrigger hasError className="mx-auto w-[250px]">        <SelectValue placeholder="Select" />      </SelectTrigger>      <SelectContent>        {data.map((item) => (          <SelectItem key={item.value} value={item.value}>            {item.label}          </SelectItem>        ))}      </SelectContent>    </Select>  )}
```

## Example: Select with icons

Preview

Code

```
import { RiBuilding2Line, RiHome2Line, RiStore2Line } from "@remixicon/react"
import {  Select,  SelectContent,  SelectItem,  SelectTrigger,  SelectValue,} from "@/components/Select"
export function SelectIconExample() {  const data = [    {      value: "living-area",      label: "Living area",      icon: RiHome2Line,    },    {      value: "shopping-area",      label: "Shopping area",      icon: RiStore2Line,    },    {      value: "business-park",      label: "Business park",      icon: RiBuilding2Line,    },  ]
  return (    <>      <Select defaultValue="living-area">        <SelectTrigger className="mx-auto w-[250px]">          <SelectValue placeholder="Select" />        </SelectTrigger>        <SelectContent>          {data.map((item) => (            <SelectItem key={item.value} value={item.value}>              <span className="flex items-center gap-x-2">                <item.icon                  className="size-4 shrink-0 text-gray-500 dark:text-gray-500"                  aria-hidden="true"                />                {item.label}              </span>            </SelectItem>          ))}        </SelectContent>      </Select>    </>  )}
```

## Example: Controlled select

Preview

Code

SelectReset selection

Selected key:

```
import React from "react"import { Button } from "@/components/Button"import {  Select,  SelectContent,  SelectItem,  SelectTrigger,  SelectValue,} from "@/components/Select"
export function SelectControlledExample() {  const [value, setValue] = React.useState("")  const data = [    {      value: "chocolate",      label: "🍫  Schoggi (Swiss german for 'Chocolate')",    },    {      value: "cheese",      label: "🧀  Chäs (Swiss german for 'Cheese')",    },    {      value: "fondue",      label: "🫕  Fondü (Swiss german for 'Fondue')",    },    {      value: "Milk",      label: "🥛  Melch (Swiss german for 'Milk')",    },  ]
  return (    <>      <div className="flex flex-col gap-2 sm:flex-row">        <Select value={value} onValueChange={setValue}>          <SelectTrigger className="mx-auto h-10">            <SelectValue placeholder="Select" aria-label={value} />          </SelectTrigger>          <SelectContent>            {data.map((item) => (              <SelectItem key={item.value} value={item.value}>                <span className="flex items-center gap-x-2">{item.label}</span>              </SelectItem>            ))}          </SelectContent>        </Select>        <Button          className="h-10 whitespace-nowrap"          variant="secondary"          onClick={() => setValue("")}        >          Reset selection        </Button>      </div>      <p className="mt-2 text-sm text-gray-500 dark:text-gray-500">        Selected key: {value}      </p>    </>  )}
```

## API Reference: Select

This component uses the [Radix UI API](https://www.radix-ui.com/primitives/docs/components/select#root).

## API Reference: SelectTrigger

This component uses the [Radix UI API](https://www.radix-ui.com/primitives/docs/components/select#trigger).

hasError

boolean

:   Style for erroneous input.

Default: false

## API Reference: SelectValue

This component uses the [Radix UI API](https://www.radix-ui.com/primitives/docs/components/select#value).

## API Reference: SelectContent

This component uses the [Radix UI API](https://www.radix-ui.com/primitives/docs/components/select#content).

## API Reference: SelectItem

This component uses the [Radix UI API](https://www.radix-ui.com/primitives/docs/components/select#item).

## API Reference: SelectGroupLabel

This component uses the [Radix UI API](https://www.radix-ui.com/primitives/docs/components/select#group).

## API Reference: SelectLabel

This component uses the [Radix UI API](https://www.radix-ui.com/primitives/docs/components/select#label).

## API Reference: SelectSeparator

This component uses the [Radix UI API](https://www.radix-ui.com/primitives/docs/components/select#separator).