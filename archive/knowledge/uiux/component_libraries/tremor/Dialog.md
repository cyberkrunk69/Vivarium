# Dialog

Source: https://tremor.so/docs/ui/dialog

---

UI

# Dialog

A window displayed over the primary window, rendering the content beneath inactive.

[Radix Docs](https://www.radix-ui.com/primitives/docs/components/dialog)[API Reference](https://www.radix-ui.com/primitives/docs/components/dialog#api-reference)[GitHub](https://github.com/tremorlabs/tremor/tree/main/src/components/Dialog)

Preview

Code

Open Dialog

```
import { Button } from '@/components/Button';import {  Dialog,  DialogClose,  DialogContent,  DialogDescription,  DialogFooter,  DialogHeader,  DialogTitle,  DialogTrigger,} from "@/components/Dialog";
export const DialogHero = () => (  <div className="flex justify-center">    <Dialog>      <DialogTrigger asChild>        <Button variant="secondary">Open Dialog</Button>      </DialogTrigger>      <DialogContent className="sm:max-w-lg">        <DialogHeader>          <DialogTitle>Account Created Successfully</DialogTitle>          <DialogDescription className="mt-1 text-sm leading-6">            Your account has been created successfully. You can now login to            your account. For more information, please contact us.          </DialogDescription>        </DialogHeader>        <DialogFooter className="mt-6">          <DialogClose asChild>            <Button              className="mt-2 w-full sm:mt-0 sm:w-fit"              variant="secondary"            >              Go back            </Button>          </DialogClose>          <DialogClose asChild>            <Button className="w-full sm:w-fit">Ok, got it!</Button>          </DialogClose>        </DialogFooter>      </DialogContent>    </Dialog>  </div>);
```

## Installation

1. 1

   ### Install dependencies:

   ```
   npm install @radix-ui/react-dialog
   ```
2. 2

   ### Add component:

   Copy and paste the code into your project’s component directory. Do not forget to update the import paths.

   Show more

   ```
   // Tremor Dialog [v1.0.0]
   import React from "react"import * as DialogPrimitives from "@radix-ui/react-dialog"
   import { cx, focusRing } from "@/lib/utils"
   const Dialog = (  props: React.ComponentPropsWithoutRef<typeof DialogPrimitives.Root>,) => {  return <DialogPrimitives.Root {...props} />}Dialog.displayName = "Dialog"
   const DialogTrigger = DialogPrimitives.Trigger
   DialogTrigger.displayName = "DialogTrigger"
   const DialogClose = DialogPrimitives.Close
   DialogClose.displayName = "DialogClose"
   const DialogPortal = DialogPrimitives.Portal
   DialogPortal.displayName = "DialogPortal"
   const DialogOverlay = React.forwardRef<  React.ElementRef<typeof DialogPrimitives.Overlay>,  React.ComponentPropsWithoutRef<typeof DialogPrimitives.Overlay>>(({ className, ...props }, forwardedRef) => {  return (    <DialogPrimitives.Overlay      ref={forwardedRef}      className={cx(        // base        "fixed inset-0 z-50 overflow-y-auto",        // background color        "bg-black/70",        // transition        "data-[state=open]:animate-dialog-overlay-show",        className,      )}      {...props}    />  )})
   DialogOverlay.displayName = "DialogOverlay"
   const DialogContent = React.forwardRef<  React.ElementRef<typeof DialogPrimitives.Content>,  React.ComponentPropsWithoutRef<typeof DialogPrimitives.Content>>(({ className, ...props }, forwardedRef) => {  return (    <DialogPortal>      <DialogOverlay>        <DialogPrimitives.Content          ref={forwardedRef}          className={cx(            // base            "fixed left-1/2 top-1/2 z-50 w-[95vw] max-w-lg -translate-x-1/2 -translate-y-1/2 overflow-y-auto rounded-md border p-6 shadow-lg",            // border color            "border-gray-200 dark:border-gray-900",            // background color            "bg-white dark:bg-[#090E1A]",            // transition            "data-[state=open]:animate-dialog-content-show",            focusRing,            className,          )}          tremor-id="tremor-raw"          {...props}        />      </DialogOverlay>    </DialogPortal>  )})
   DialogContent.displayName = "DialogContent"
   const DialogHeader = ({  className,  ...props}: React.HTMLAttributes<HTMLDivElement>) => {  return <div className={cx("flex flex-col gap-y-1", className)} {...props} />}
   DialogHeader.displayName = "DialogHeader"
   const DialogTitle = React.forwardRef<  React.ElementRef<typeof DialogPrimitives.Title>,  React.ComponentPropsWithoutRef<typeof DialogPrimitives.Title>>(({ className, ...props }, forwardedRef) => (  <DialogPrimitives.Title    ref={forwardedRef}    className={cx(      // base      "text-lg font-semibold",      // text color      "text-gray-900 dark:text-gray-50",      className,    )}    {...props}  />))
   DialogTitle.displayName = "DialogTitle"
   const DialogDescription = React.forwardRef<  React.ElementRef<typeof DialogPrimitives.Description>,  React.ComponentPropsWithoutRef<typeof DialogPrimitives.Description>>(({ className, ...props }, forwardedRef) => {  return (    <DialogPrimitives.Description      ref={forwardedRef}      className={cx("text-gray-500 dark:text-gray-500", className)}      {...props}    />  )})
   DialogDescription.displayName = "DialogDescription"
   const DialogFooter = ({  className,  ...props}: React.HTMLAttributes<HTMLDivElement>) => {  return (    <div      className={cx(        "flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2",        className,      )}      {...props}    />  )}
   DialogFooter.displayName = "DialogFooter"
   export {  Dialog,  DialogClose,  DialogContent,  DialogDescription,  DialogFooter,  DialogHeader,  DialogTitle,  DialogTrigger,}
   ```
3. 3

   ### Update globals.css

   ```
   @theme {  --animate-dialog-overlay-show: dialogOverlayShow 150ms cubic-bezier(0.16, 1, 0.3, 1);  --animate-dialog-content-show: dialogContentShow 150ms cubic-bezier(0.16, 1, 0.3, 1);
     @keyframes dialogOverlayShow {    from {      opacity: 0;    }    to {      opacity: 1;    }  }  @keyframes dialogContentShow {    from {      opacity: 0;      transform: translate(-50%, -45%) scale(0.95);    }    to {      opacity: 1;      transform: translate(-50%, -50%) scale(1);    }  }}
   ```

## Example

Preview

Code

Open Dialog

```
import { Button } from '@/components/Button';import {  Dialog,  DialogClose,  DialogContent,  DialogDescription,  DialogFooter,  DialogHeader,  DialogTitle,  DialogTrigger,} from "@/components/Dialog";
export const DialogExample = () => (  <>    <div className="flex justify-center">      <Dialog>        <DialogTrigger asChild>          <Button variant="secondary">Open Dialog</Button>        </DialogTrigger>        <DialogContent className="sm:max-w-lg">          <DialogHeader>            <DialogTitle>Account Created Successfully</DialogTitle>            <DialogDescription className="mt-1 text-sm leading-6">              Your account has been created successfully. You can now login to              your account. For more information, please contact us.            </DialogDescription>          </DialogHeader>          <DialogFooter className="mt-6">            <DialogClose asChild>              <Button                className="mt-2 w-full sm:mt-0 sm:w-fit"                variant="secondary"              >                Go back              </Button>            </DialogClose>            <DialogClose asChild>              <Button className="w-full sm:w-fit">Ok, got it!</Button>            </DialogClose>          </DialogFooter>        </DialogContent>      </Dialog>    </div>  </>);
```

## API Reference: Dialog

This component uses the [Radix UI API](https://www.radix-ui.com/primitives/docs/components/dialog#root).

## API Reference: DialogTrigger

This component uses the [Radix UI API](https://www.radix-ui.com/primitives/docs/components/dialog#trigger).

## API Reference: DialogTitle

This component uses the [Radix UI API](https://www.radix-ui.com/primitives/docs/components/dialog#title).

## API Reference: DialogDescription

This component uses the [Radix UI API](https://www.radix-ui.com/primitives/docs/components/dialog#Description).

## API Reference: DialogHeader

This component is based on the div element and supports all of its props.

## API Reference: DialogClose

This component uses the [Radix UI API](https://www.radix-ui.com/primitives/docs/components/dialog#close).

## API Reference: DialogContent

This component uses the [Radix UI API](https://www.radix-ui.com/primitives/docs/components/dialog#content).

## API Reference: DialogFooter

This component is based on the div element and supports all of its props.