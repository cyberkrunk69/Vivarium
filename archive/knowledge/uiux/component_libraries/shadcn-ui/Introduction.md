# Introduction

Source: https://ui.shadcn.com/docs

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

# Introduction

Copy Page

[Previous](/docs/components/radix/typography)[Next](/docs/installation)

shadcn/ui is a set of beautifully-designed, accessible components and a code distribution platform. Works with your favorite frameworks and AI models. Open Source. Open Code.

**This is not a component library. It is how you build your component library.**

You know how most traditional component libraries work: you install a package from NPM, import the components, and use them in your app.

This approach works well until you need to customize a component to fit your design system or require one that isn’t included in the library. **Often, you end up wrapping library components, writing workarounds to override styles, or mixing components from different libraries with incompatible APIs.**

This is what shadcn/ui aims to solve. It is built around the following principles:

- **Open Code:** The top layer of your component code is open for modification.
- **Composition:** Every component uses a common, composable interface, making them predictable.
- **Distribution:** A flat-file schema and command-line tool make it easy to distribute components.
- **Beautiful Defaults:** Carefully chosen default styles, so you get great design out-of-the-box.
- **AI-Ready:** Open code for LLMs to read, understand, and improve.

## Open Code

shadcn/ui hands you the actual component code. You have full control to customize and extend the components to your needs. This means:

- **Full Transparency:** You see exactly how each component is built.
- **Easy Customization:** Modify any part of a component to fit your design and functionality requirements.
- **AI Integration:** Access to the code makes it straightforward for LLMs to read, understand, and even improve your components.

*In a typical library, if you need to change a button’s behavior, you have to override styles or wrap the component. With shadcn/ui, you simply edit the button code directly.*

### How do I pull upstream updates in an Open Code approach?

## Composition

Every component in shadcn/ui shares a common, composable interface. **If a component does not exist, we bring it in, make it composable, and adjust its style to match and work with the rest of the design system.**

*A shared, composable interface means it's predictable for both your team and LLMs. You are not learning different APIs for every new component. Even for third-party ones.*

## Distribution

shadcn/ui is also a code distribution system. It defines a schema for components and a CLI to distribute them.

- **Schema:** A flat-file structure that defines the components, their dependencies, and properties.
- **CLI:** A command-line tool to distribute and install components across projects with cross-framework support.

*You can use the schema to distribute your components to other projects or have AI generate completely new components based on existing schema.*

## Beautiful Defaults

shadcn/ui comes with a large collection of components that have carefully chosen default styles. They are designed to look good on their own and to work well together as a consistent system:

- **Good Out-of-the-Box:** Your UI has a clean and minimal look without extra work.
- **Unified Design:** Components naturally fit with one another. Each component is built to match the others, keeping your UI consistent.
- **Easily Customizable:** If you want to change something, it's simple to override and extend the defaults.

## AI-Ready

The design of shadcn/ui makes it easy for AI tools to work with your code. Its open code and consistent API allow AI models to read, understand, and even generate new components.

*An AI model can learn how your components work and suggest improvements or even create new components that integrate with your existing design.*

[Typography](/docs/components/radix/typography)[Installation](/docs/installation)

On This Page

[Open Code](#open-code)[Composition](#composition)[Distribution](#distribution)[Beautiful Defaults](#beautiful-defaults)[AI-Ready](#ai-ready)

Deploy your shadcn/ui app on Vercel

Trusted by OpenAI, Sonos, Adobe, and more.

Vercel provides tools and infrastructure to deploy apps and features at scale.

Deploy Now[Deploy to Vercel](https://vercel.com/new?utm_source=shadcn_site&utm_medium=web&utm_campaign=docs_cta_deploy_now_callout)