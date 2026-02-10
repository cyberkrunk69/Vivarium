# Getting started

Source: https://react-spectrum.adobe.com/react-aria/getting-started.html

---

# Getting started

How to install React Aria and build your first component.

## Install

Install React Aria with your preferred package manager.

npm

yarn

pnpm

```
npm install react-aria-components
```

## Quick start

Copy and paste the CSS or [Tailwind](https://tailwindcss.com) examples into your project and make them your own. You can also download each example as a ZIP, open in StackBlitz, or install with [shadcn](https://ui.shadcn.com/docs/cli).

Vanilla CSS

Tailwind

Â

### Vanilla CSS theme

This sets the `--tint` CSS variable used by the Vanilla CSS examples.

ThemeÂ

Indigo

IndigoBlueCyanTurquoiseGreenYellowOrangeRedPinkPurple

Favorite animalSelect an item

AardvarkCatDogKangarooPandaSnake

Example

Select.tsx

Select.css

Example

Select.tsx

Select.css

Example

Select.tsx

Select.css

```
import {Select, SelectItem} from './Select';

<Select label="Favorite animal">
  <SelectItem>Aardvark</SelectItem>
  <SelectItem>Cat</SelectItem>
  <SelectItem>Dog</SelectItem>
  <SelectItem>Kangaroo</SelectItem>
  <SelectItem>Panda</SelectItem>
  <SelectItem>Snake</SelectItem>
</Select>
```

Expand code

### shadcn CLI

Use the [shadcn](https://ui.shadcn.com/docs/cli) CLI to add the example code, styles, and dependencies to your project. Install individual components using the menu on each example, or add all components with the command below.

npm

yarn

pnpm

Vanilla CSS

Tailwind

```
npx shadcn@latest add @react-aria/css
```

### Storybook starter kits

If you're building a full component library, download a pre-built [Storybook](https://storybook.js.org/) starter kit. These include every component in a standalone development environment.

[Vanilla CSSDownload ZIP](react-aria-starter.1f945dea2.zip)[Preview](react-aria-starter/)

[Tailwind CSSDownload ZIP](react-aria-tailwind-starter.1f945dea2.zip)[Preview](react-aria-tailwind-starter/)

### Working with AI

Use the menu on each page in the docs to open or copy it into your favorite AI assistant. We also have an [MCP server](mcp) which can be used directly in your IDE, and <llms.txt> which can help AI agents navigate the docs.

## Build a component from scratch

In this tutorial, we'll build a custom <Select> component.

1. ### Import and assemble the parts

   Each React Aria component renders a single DOM element. Complex components like `Select` compose together multiple parts to build a complete pattern.

   ```
   import {Button, Label, ListBox, ListBoxItem, Popover, Select, SelectValue} from 'react-aria-components';

   <Select>
     <Label>Favorite Animal</Label>
     <Button>
       <SelectValue />
     </Button>
     <Popover>
       <ListBox>
         <ListBoxItem>Cat</ListBoxItem>
         <ListBoxItem>Dog</ListBoxItem>
         <ListBoxItem>Kangaroo</ListBoxItem>
       </ListBox>
     </Popover>
   </Select>
   ```
2. ### Add your styles

   React Aria does not include any styles by default, allowing you to build custom designs to fit your application or design system. You can use any styling solution, including vanilla CSS, Tailwind CSS, CSS-in-JS, etc.

   Each React Aria component includes a default class name to use in your CSS, and data attributes for states such as pressed, hovered, selected, etc.

   ```
   .react-aria-ListBoxItem {
     color: black;

     &[data-selected] {
       background: black;
       color: white;
     }
   }
   ```

   You can also override these defaults with a custom `className` prop, and access states via render props. Check out our [styling guide](styling) to learn more.
3. ### Create a reusable component

   To reuse styles throughout your project, wrap all of the parts into a reusable component. Create your own API by extending React Aria's types with additional props. Components such as Popover can also be shared with other patterns so they don't need be styled separately each time.

   ```
   import type {SelectProps as AriaSelectProps, ListBoxItemProps} from 'react-aria-components';
   import {Select as AriaSelect, Button, Label, ListBox, ListBoxItem, SelectValue} from 'react-aria-components';
   import {Popover} from './Popover';
   import './Select.css';

   export interface SelectProps extends AriaSelectProps {
     label?: string
   }

   export function Select(props: SelectProps) {
     return (
       <AriaSelect {...props}>
         <Label>{props.label}</Label>
         <Button className="select-button">
           <SelectValue />
         </Button>
         <Popover>
           <ListBox className="select-listbox">
             {props.children}
           </ListBox>
         </Popover>
       </AriaSelect>
     );
   }

   export function SelectItem(props: ListBoxItemProps) {
     return <ListBoxItem {...props} className="select-item" />;
   }
   ```
4. ### Use your component

   Now you can render a consistently styled `<Select>` anywhere in your project!

   ```
   import {Select, SelectItem} from './Select';

   function App() {
     return (
       <Select label="Favorite animal">
         <SelectItem>Cat</SelectItem>
         <SelectItem>Dog</SelectItem>
         <SelectItem>Kangaroo</SelectItem>
       </Select>
     );
   }
   ```

## Framework setup

React Aria works out of the box in any React framework. When you're ready, follow our [framework setup](frameworks) guide to optimize the bundle size, configure internationalization, and integrate with client side routers.