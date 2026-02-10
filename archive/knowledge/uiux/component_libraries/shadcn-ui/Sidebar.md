# Sidebar

Source: https://ui.shadcn.com/docs/components/sidebar

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

# Sidebar

Copy Page

[Previous](/docs/components/radix/sheet)[Next](/docs/components/radix/skeleton)

A composable, themeable and customizable sidebar component.

[Radix UI](/docs/components/radix/sidebar)[Base UI](/docs/components/base/sidebar)

![sidebar-demo](/_next/image?url=%2Fr%2Fstyles%2Fnew-york-v4%2Fsidebar-demo-light.png&w=3840&q=75&dpl=dpl_HcaEp7iRSCdftJFxyj8tTTXJLX3F)![sidebar-demo](/_next/image?url=%2Fr%2Fstyles%2Fnew-york-v4%2Fsidebar-demo-dark.png&w=3840&q=75&dpl=dpl_HcaEp7iRSCdftJFxyj8tTTXJLX3F)

A sidebar that collapses to icons.

Sidebars are one of the most complex components to build. They are central
to any application and often contain a lot of moving parts.

We now have a solid foundation to build on top of. Composable. Themeable.
Customizable.

[Browse the Blocks Library](/blocks).

## Installation

CommandManual

```
pnpmnpmyarnbun

```
pnpm dlx shadcn@latest add sidebar
```

Copy
```

## Structure

A `Sidebar` component is composed of the following parts:

- `SidebarProvider` - Handles collapsible state.
- `Sidebar` - The sidebar container.
- `SidebarHeader` and `SidebarFooter` - Sticky at the top and bottom of the sidebar.
- `SidebarContent` - Scrollable content.
- `SidebarGroup` - Section within the `SidebarContent`.
- `SidebarTrigger` - Trigger for the `Sidebar`.

![Sidebar Structure](/_next/image?url=%2Fimages%2Fsidebar-structure.png&w=1920&q=75&dpl=dpl_HcaEp7iRSCdftJFxyj8tTTXJLX3F)
![Sidebar Structure](/_next/image?url=%2Fimages%2Fsidebar-structure-dark.png&w=1920&q=75&dpl=dpl_HcaEp7iRSCdftJFxyj8tTTXJLX3F)

## Usage

app/layout.tsx

```
Copyimport { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"
 
export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <SidebarProvider>
      <AppSidebar />
      <main>
        <SidebarTrigger />
        {children}
      </main>
    </SidebarProvider>
  )
}
```

components/app-sidebar.tsx

```
Copyimport {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarHeader,
} from "@/components/ui/sidebar"
 
export function AppSidebar() {
  return (
    <Sidebar>
      <SidebarHeader />
      <SidebarContent>
        <SidebarGroup />
        <SidebarGroup />
      </SidebarContent>
      <SidebarFooter />
    </Sidebar>
  )
}
```

## SidebarProvider

The `SidebarProvider` component is used to provide the sidebar context to the `Sidebar` component. You should always wrap your application in a `SidebarProvider` component.

### Props

| Name | Type | Description |
| --- | --- | --- |
| `defaultOpen` | `boolean` | Default open state of the sidebar. |
| `open` | `boolean` | Open state of the sidebar (controlled). |
| `onOpenChange` | `(open: boolean) => void` | Sets open state of the sidebar (controlled). |

### Width

If you have a single sidebar in your application, you can use the `SIDEBAR_WIDTH` and `SIDEBAR_WIDTH_MOBILE` variables in `sidebar.tsx` to set the width of the sidebar.

components/ui/sidebar.tsx

```
Copyconst SIDEBAR_WIDTH = "16rem"
const SIDEBAR_WIDTH_MOBILE = "18rem"
```

For multiple sidebars in your application, you can use the `--sidebar-width` and `--sidebar-width-mobile` CSS variables in the `style` prop.

```
Copy<SidebarProvider
  style={{
    "--sidebar-width": "20rem",
    "--sidebar-width-mobile": "20rem",
  }}
>
  <Sidebar />
</SidebarProvider>
```

### Keyboard Shortcut

To trigger the sidebar, you use the `cmd+b` keyboard shortcut on Mac and `ctrl+b` on Windows.

components/ui/sidebar.tsx

```
Copyconst SIDEBAR_KEYBOARD_SHORTCUT = "b"
```

## Sidebar

The main `Sidebar` component used to render a collapsible sidebar.

### Props

| Property | Type | Description |
| --- | --- | --- |
| `side` | `left` or `right` | The side of the sidebar. |
| `variant` | `sidebar`, `floating`, or `inset` | The variant of the sidebar. |
| `collapsible` | `offcanvas`, `icon`, or `none` | Collapsible state of the sidebar. |

| Prop | Description |
| --- | --- |
| `offcanvas` | A collapsible sidebar that slides in from the left or right. |
| `icon` | A sidebar that collapses to icons. |
| `none` | A non-collapsible sidebar. |

**Note:** If you use the `inset` variant, remember to wrap your main content
in a `SidebarInset` component.

```
Copy<SidebarProvider>
  <Sidebar variant="inset" />
  <SidebarInset>
    <main>{children}</main>
  </SidebarInset>
</SidebarProvider>
```

## useSidebar

The `useSidebar` hook is used to control the sidebar.

```
Copyimport { useSidebar } from "@/components/ui/sidebar"
 
export function AppSidebar() {
  const {
    state,
    open,
    setOpen,
    openMobile,
    setOpenMobile,
    isMobile,
    toggleSidebar,
  } = useSidebar()
}
```

| Property | Type | Description |
| --- | --- | --- |
| `state` | `expanded` or `collapsed` | The current state of the sidebar. |
| `open` | `boolean` | Whether the sidebar is open. |
| `setOpen` | `(open: boolean) => void` | Sets the open state of the sidebar. |
| `openMobile` | `boolean` | Whether the sidebar is open on mobile. |
| `setOpenMobile` | `(open: boolean) => void` | Sets the open state of the sidebar on mobile. |
| `isMobile` | `boolean` | Whether the sidebar is on mobile. |
| `toggleSidebar` | `() => void` | Toggles the sidebar. Desktop and mobile. |

## SidebarHeader

Use the `SidebarHeader` component to add a sticky header to the sidebar.

components/app-sidebar.tsx

```
Copy<Sidebar>
  <SidebarHeader>
    <SidebarMenu>
      <SidebarMenuItem>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <SidebarMenuButton>
              Select Workspace
              <ChevronDown className="ml-auto" />
            </SidebarMenuButton>
          </DropdownMenuTrigger>
          <DropdownMenuContent className="w-[--radix-popper-anchor-width]">
            <DropdownMenuItem>
              <span>Acme Inc</span>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </SidebarMenuItem>
    </SidebarMenu>
  </SidebarHeader>
</Sidebar>
```

## SidebarFooter

Use the `SidebarFooter` component to add a sticky footer to the sidebar.

```
Copy<Sidebar>
  <SidebarFooter>
    <SidebarMenu>
      <SidebarMenuItem>
        <SidebarMenuButton>
          <User2 /> Username
        </SidebarMenuButton>
      </SidebarMenuItem>
    </SidebarMenu>
  </SidebarFooter>
</Sidebar>
```

## SidebarContent

The `SidebarContent` component is used to wrap the content of the sidebar. This is where you add your `SidebarGroup` components. It is scrollable.

```
Copy<Sidebar>
  <SidebarContent>
    <SidebarGroup />
    <SidebarGroup />
  </SidebarContent>
</Sidebar>
```

## SidebarGroup

Use the `SidebarGroup` component to create a section within the sidebar.

A `SidebarGroup` has a `SidebarGroupLabel`, a `SidebarGroupContent` and an optional `SidebarGroupAction`.

```
Copy<SidebarGroup>
  <SidebarGroupLabel>Application</SidebarGroupLabel>
  <SidebarGroupAction>
    <Plus /> <span className="sr-only">Add Project</span>
  </SidebarGroupAction>
  <SidebarGroupContent></SidebarGroupContent>
</SidebarGroup>
```

To make a `SidebarGroup` collapsible, wrap it in a `Collapsible`.

```
Copy<Collapsible defaultOpen className="group/collapsible">
  <SidebarGroup>
    <SidebarGroupLabel asChild>
      <CollapsibleTrigger>
        Help
        <ChevronDown className="ml-auto transition-transform group-data-[state=open]/collapsible:rotate-180" />
      </CollapsibleTrigger>
    </SidebarGroupLabel>
    <CollapsibleContent>
      <SidebarGroupContent />
    </CollapsibleContent>
  </SidebarGroup>
</Collapsible>
```

## SidebarMenu

The `SidebarMenu` component is used for building a menu within a `SidebarGroup`.

![Sidebar Menu](/_next/image?url=%2Fimages%2Fsidebar-menu.png&w=1920&q=75&dpl=dpl_HcaEp7iRSCdftJFxyj8tTTXJLX3F)
![Sidebar Menu](/_next/image?url=%2Fimages%2Fsidebar-menu-dark.png&w=1920&q=75&dpl=dpl_HcaEp7iRSCdftJFxyj8tTTXJLX3F)

```
Copy<SidebarMenu>
  {projects.map((project) => (
    <SidebarMenuItem key={project.name}>
      <SidebarMenuButton asChild>
        <a href={project.url}>
          <project.icon />
          <span>{project.name}</span>
        </a>
      </SidebarMenuButton>
    </SidebarMenuItem>
  ))}
</SidebarMenu>
```

## SidebarMenuButton

The `SidebarMenuButton` component is used to render a menu button within a `SidebarMenuItem`.

By default, the `SidebarMenuButton` renders a button but you can use the `asChild` prop to render a different component such as a `Link` or an `a` tag.

Use the `isActive` prop to mark a menu item as active.

```
Copy<SidebarMenuButton asChild isActive>
  <a href="#">Home</a>
</SidebarMenuButton>
```

## SidebarMenuAction

The `SidebarMenuAction` component is used to render a menu action within a `SidebarMenuItem`.

```
Copy<SidebarMenuItem>
  <SidebarMenuButton asChild>
    <a href="#">
      <Home />
      <span>Home</span>
    </a>
  </SidebarMenuButton>
  <SidebarMenuAction>
    <Plus /> <span className="sr-only">Add Project</span>
  </SidebarMenuAction>
</SidebarMenuItem>
```

## SidebarMenuSub

The `SidebarMenuSub` component is used to render a submenu within a `SidebarMenu`.

```
Copy<SidebarMenuItem>
  <SidebarMenuButton />
  <SidebarMenuSub>
    <SidebarMenuSubItem>
      <SidebarMenuSubButton />
    </SidebarMenuSubItem>
  </SidebarMenuSub>
</SidebarMenuItem>
```

## SidebarMenuBadge

The `SidebarMenuBadge` component is used to render a badge within a `SidebarMenuItem`.

```
Copy<SidebarMenuItem>
  <SidebarMenuButton />
  <SidebarMenuBadge>24</SidebarMenuBadge>
</SidebarMenuItem>
```

## SidebarMenuSkeleton

The `SidebarMenuSkeleton` component is used to render a skeleton for a `SidebarMenu`.

```
Copy<SidebarMenu>
  {Array.from({ length: 5 }).map((_, index) => (
    <SidebarMenuItem key={index}>
      <SidebarMenuSkeleton />
    </SidebarMenuItem>
  ))}
</SidebarMenu>
```

## SidebarTrigger

Use the `SidebarTrigger` component to render a button that toggles the sidebar.

```
Copyimport { useSidebar } from "@/components/ui/sidebar"
 
export function CustomTrigger() {
  const { toggleSidebar } = useSidebar()
 
  return <button onClick={toggleSidebar}>Toggle Sidebar</button>
}
```

## SidebarRail

The `SidebarRail` component is used to render a rail within a `Sidebar`. This rail can be used to toggle the sidebar.

```
Copy<Sidebar>
  <SidebarHeader />
  <SidebarContent>
    <SidebarGroup />
  </SidebarContent>
  <SidebarFooter />
  <SidebarRail />
</Sidebar>
```

## Controlled Sidebar

Use the `open` and `onOpenChange` props to control the sidebar.

```
Copyexport function AppSidebar() {
  const [open, setOpen] = React.useState(false)
 
  return (
    <SidebarProvider open={open} onOpenChange={setOpen}>
      <Sidebar />
    </SidebarProvider>
  )
}
```

## Theming

We use the following CSS variables to theme the sidebar.

```
Copy@layer base {
  :root {
    --sidebar-background: 0 0% 98%;
    --sidebar-foreground: 240 5.3% 26.1%;
    --sidebar-primary: 240 5.9% 10%;
    --sidebar-primary-foreground: 0 0% 98%;
    --sidebar-accent: 240 4.8% 95.9%;
    --sidebar-accent-foreground: 240 5.9% 10%;
    --sidebar-border: 220 13% 91%;
    --sidebar-ring: 217.2 91.2% 59.8%;
  }
 
  .dark {
    --sidebar-background: 240 5.9% 10%;
    --sidebar-foreground: 240 4.8% 95.9%;
    --sidebar-primary: 0 0% 98%;
    --sidebar-primary-foreground: 240 5.9% 10%;
    --sidebar-accent: 240 3.7% 15.9%;
    --sidebar-accent-foreground: 240 4.8% 95.9%;
    --sidebar-border: 240 3.7% 15.9%;
    --sidebar-ring: 217.2 91.2% 59.8%;
  }
}
```

## Styling

Here are some tips for styling the sidebar based on different states.

```
Copy<Sidebar collapsible="icon">
  <SidebarContent>
    <SidebarGroup className="group-data-[collapsible=icon]:hidden" />
  </SidebarContent>
</Sidebar>
```

```
Copy<SidebarMenuItem>
  <SidebarMenuButton />
  <SidebarMenuAction className="peer-data-[active=true]/menu-button:opacity-100" />
</SidebarMenuItem>
```

## RTL

To enable RTL support in shadcn/ui, see the [RTL configuration guide](/docs/rtl).

[View RTL Sidebar](/view/radix-nova/sidebar-rtl) 

## Changelog

### RTL Support

If you're upgrading from a previous version of the `Sidebar` component, you'll need to apply the following updates to add RTL support:

### Add `dir` prop to Sidebar component.

Add `dir` to the destructured props and pass it to `SheetContent` for mobile:

```
Copy  function Sidebar({
    side = "left",
    variant = "sidebar",
    collapsible = "offcanvas",
    className,
    children,
+   dir,
    ...props
  }: React.ComponentProps<"div"> & {
    side?: "left" | "right"
    variant?: "sidebar" | "floating" | "inset"
    collapsible?: "offcanvas" | "icon" | "none"
  }) {
```

Then pass it to `SheetContent` in the mobile view:

```
Copy  <Sheet open={openMobile} onOpenChange={setOpenMobile} {...props}>
    <SheetContent
+     dir={dir}
      data-sidebar="sidebar"
      data-slot="sidebar"
      data-mobile="true"
```

### Add `data-side` attribute to sidebar container.

Add `data-side={side}` to the sidebar container element:

```
Copy  <div
    data-slot="sidebar-container"
+   data-side={side}
    className={cn(
```

### Update sidebar container positioning classes.

Replace JavaScript ternary conditional classes with CSS data attribute selectors:

```
Copy  className={cn(
-   "fixed inset-y-0 z-10 hidden h-svh w-(--sidebar-width) transition-[left,right,width] duration-200 ease-linear md:flex",
-   side === "left"
-     ? "left-0 group-data-[collapsible=offcanvas]:left-[calc(var(--sidebar-width)*-1)]"
-     : "right-0 group-data-[collapsible=offcanvas]:right-[calc(var(--sidebar-width)*-1)]",
+   "fixed inset-y-0 z-10 hidden h-svh w-(--sidebar-width) transition-[left,right,width] duration-200 ease-linear md:flex data-[side=left]:left-0 data-[side=right]:right-0 data-[side=left]:group-data-[collapsible=offcanvas]:left-[calc(var(--sidebar-width)*-1)] data-[side=right]:group-data-[collapsible=offcanvas]:right-[calc(var(--sidebar-width)*-1)]",
```

### Update SidebarRail positioning classes.

Update the `SidebarRail` component to use physical positioning for the rail:

```
Copy  className={cn(
-   "hover:after:bg-sidebar-border absolute inset-y-0 z-20 hidden w-4 -translate-x-1/2 transition-all ease-linear group-data-[side=left]:-end-4 group-data-[side=right]:start-0 after:absolute after:inset-y-0 after:start-1/2 after:w-[2px] sm:flex",
+   "hover:after:bg-sidebar-border absolute inset-y-0 z-20 hidden w-4 ltr:-translate-x-1/2 rtl:-translate-x-1/2 transition-all ease-linear group-data-[side=left]:-right-4 group-data-[side=right]:left-0 after:absolute after:inset-y-0 after:start-1/2 after:w-[2px] sm:flex",
```

### Add RTL flip to SidebarTrigger icon.

Add `className="rtl:rotate-180"` to the icon in `SidebarTrigger` to flip it in RTL mode:

```
Copy  <Button ...>
-   <PanelLeftIcon />
+   <PanelLeftIcon className="rtl:rotate-180" />
    <span className="sr-only">Toggle Sidebar</span>
  </Button>
```

After applying these changes, you can use the `dir` prop to set the direction:

```
Copy<Sidebar dir="rtl" side="right">
  {/* ... */}
</Sidebar>
```

The sidebar will correctly position itself and handle interactions in both LTR and RTL layouts.

[Sheet](/docs/components/radix/sheet)[Skeleton](/docs/components/radix/skeleton)

On This Page

[Installation](#installation)[Structure](#structure)[Usage](#usage)[SidebarProvider](#sidebarprovider)[Props](#props)[Width](#width)[Keyboard Shortcut](#keyboard-shortcut)[Sidebar](#sidebar)[Props](#props-1)[useSidebar](#usesidebar)[SidebarHeader](#sidebarheader)[SidebarFooter](#sidebarfooter)[SidebarContent](#sidebarcontent)[SidebarGroup](#sidebargroup)[SidebarMenu](#sidebarmenu)[SidebarMenuButton](#sidebarmenubutton)[SidebarMenuAction](#sidebarmenuaction)[SidebarMenuSub](#sidebarmenusub)[SidebarMenuBadge](#sidebarmenubadge)[SidebarMenuSkeleton](#sidebarmenuskeleton)[SidebarTrigger](#sidebartrigger)[SidebarRail](#sidebarrail)[Controlled Sidebar](#controlled-sidebar)[Theming](#theming)[Styling](#styling)[RTL](#rtl)[Changelog](#changelog)[RTL Support](#rtl-support)

Deploy your shadcn/ui app on Vercel

Trusted by OpenAI, Sonos, Adobe, and more.

Vercel provides tools and infrastructure to deploy apps and features at scale.

Deploy Now[Deploy to Vercel](https://vercel.com/new?utm_source=shadcn_site&utm_medium=web&utm_campaign=docs_cta_deploy_now_callout)