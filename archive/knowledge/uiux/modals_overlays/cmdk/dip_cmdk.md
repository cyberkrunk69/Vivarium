# dip/cmdk

Source: https://cmdk.paco.me/

---

[dip](/dip) 
/
**[cmdk](/dip/cmdk)**
Public

- [Notifications](/login?return_to=%2Fdip%2Fcmdk) You must be signed in to change notification settings
- [Fork
  358](/login?return_to=%2Fdip%2Fcmdk)
- [Star
   12.2k](/login?return_to=%2Fdip%2Fcmdk)

Fast, unstyled command menu React component.

### License

[MIT license](/dip/cmdk/blob/main/LICENSE.md)

[12.2k
stars](/dip/cmdk/stargazers) [358
forks](/dip/cmdk/forks) [Branches](/dip/cmdk/branches) [Tags](/dip/cmdk/tags) [Activity](/dip/cmdk/activity)

[Star](/login?return_to=%2Fdip%2Fcmdk)

[Notifications](/login?return_to=%2Fdip%2Fcmdk) You must be signed in to change notification settings

# dip/cmdk

main

[Branches](/dip/cmdk/branches)[Tags](/dip/cmdk/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | | Name | Last commit message | Last commit date |
| --- | --- | --- | --- | --- |
| Latest commit   History[156 Commits](/dip/cmdk/commits/main/)   156 Commits | | |
| [.github](/dip/cmdk/tree/main/.github ".github") | | [.github](/dip/cmdk/tree/main/.github ".github") |  |  |
| [.husky](/dip/cmdk/tree/main/.husky ".husky") | | [.husky](/dip/cmdk/tree/main/.husky ".husky") |  |  |
| [cmdk](/dip/cmdk/tree/main/cmdk "cmdk") | | [cmdk](/dip/cmdk/tree/main/cmdk "cmdk") |  |  |
| [test](/dip/cmdk/tree/main/test "test") | | [test](/dip/cmdk/tree/main/test "test") |  |  |
| [website](/dip/cmdk/tree/main/website "website") | | [website](/dip/cmdk/tree/main/website "website") |  |  |
| [.gitignore](/dip/cmdk/blob/main/.gitignore ".gitignore") | | [.gitignore](/dip/cmdk/blob/main/.gitignore ".gitignore") |  |  |
| [.prettierignore](/dip/cmdk/blob/main/.prettierignore ".prettierignore") | | [.prettierignore](/dip/cmdk/blob/main/.prettierignore ".prettierignore") |  |  |
| [.prettierrc.js](/dip/cmdk/blob/main/.prettierrc.js ".prettierrc.js") | | [.prettierrc.js](/dip/cmdk/blob/main/.prettierrc.js ".prettierrc.js") |  |  |
| [ARCHITECTURE.md](/dip/cmdk/blob/main/ARCHITECTURE.md "ARCHITECTURE.md") | | [ARCHITECTURE.md](/dip/cmdk/blob/main/ARCHITECTURE.md "ARCHITECTURE.md") |  |  |
| [LICENSE.md](/dip/cmdk/blob/main/LICENSE.md "LICENSE.md") | | [LICENSE.md](/dip/cmdk/blob/main/LICENSE.md "LICENSE.md") |  |  |
| [README.md](/dip/cmdk/blob/main/README.md "README.md") | | [README.md](/dip/cmdk/blob/main/README.md "README.md") |  |  |
| [package.json](/dip/cmdk/blob/main/package.json "package.json") | | [package.json](/dip/cmdk/blob/main/package.json "package.json") |  |  |
| [playwright.config.ts](/dip/cmdk/blob/main/playwright.config.ts "playwright.config.ts") | | [playwright.config.ts](/dip/cmdk/blob/main/playwright.config.ts "playwright.config.ts") |  |  |
| [pnpm-lock.yaml](/dip/cmdk/blob/main/pnpm-lock.yaml "pnpm-lock.yaml") | | [pnpm-lock.yaml](/dip/cmdk/blob/main/pnpm-lock.yaml "pnpm-lock.yaml") |  |  |
| [pnpm-workspace.yaml](/dip/cmdk/blob/main/pnpm-workspace.yaml "pnpm-workspace.yaml") | | [pnpm-workspace.yaml](/dip/cmdk/blob/main/pnpm-workspace.yaml "pnpm-workspace.yaml") |  |  |
| [tsconfig.json](/dip/cmdk/blob/main/tsconfig.json "tsconfig.json") | | [tsconfig.json](/dip/cmdk/blob/main/tsconfig.json "tsconfig.json") |  |  |
| View all files | | |

## Repository files navigation

[![](/dip/cmdk/raw/main/website/public/og.png)](/dip/cmdk/blob/main/website/public/og.png)

# ⌘K [cmdk minzip package size](https://www.npmjs.com/package/cmdk?activeTab=code) [cmdk package version](https://www.npmjs.com/package/cmdk)

⌘K is a command menu React component that can also be used as an accessible combobox. You render items, it filters and sorts them automatically. ⌘K supports a fully composable API [How?](/dip/cmdk/blob/main/ARCHITECTURE.md), so you can wrap items in other components or even as static JSX.

## Install

```
pnpm install cmdk
```

## Use

```
import { Command } from 'cmdk'

const CommandMenu = () => {
  return (
    <Command label="Command Menu">
      <Command.Input />
      <Command.List>
        <Command.Empty>No results found.</Command.Empty>

        <Command.Group heading="Letters">
          <Command.Item>a</Command.Item>
          <Command.Item>b</Command.Item>
          <Command.Separator />
          <Command.Item>c</Command.Item>
        </Command.Group>

        <Command.Item>Apple</Command.Item>
      </Command.List>
    </Command>
  )
}
```

Or in a dialog:

```
import { Command } from 'cmdk'

const CommandMenu = () => {
  const [open, setOpen] = React.useState(false)

  // Toggle the menu when ⌘K is pressed
  React.useEffect(() => {
    const down = (e) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault()
        setOpen((open) => !open)
      }
    }

    document.addEventListener('keydown', down)
    return () => document.removeEventListener('keydown', down)
  }, [])

  return (
    <Command.Dialog open={open} onOpenChange={setOpen} label="Global Command Menu">
      <Command.Input />
      <Command.List>
        <Command.Empty>No results found.</Command.Empty>

        <Command.Group heading="Letters">
          <Command.Item>a</Command.Item>
          <Command.Item>b</Command.Item>
          <Command.Separator />
          <Command.Item>c</Command.Item>
        </Command.Group>

        <Command.Item>Apple</Command.Item>
      </Command.List>
    </Command.Dialog>
  )
}
```

## Parts and styling

All parts forward props, including `ref`, to an appropriate element. Each part has a specific data-attribute (starting with `cmdk-`) that can be used for styling.

### Command `[cmdk-root]`

Render this to show the command menu inline, or use [Dialog](#dialog-cmdk-dialog-cmdk-overlay) to render in a elevated context. Can be controlled with the `value` and `onValueChange` props.

> **Note**
>
> Values are always trimmed with the [trim()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/trim) method.

```
const [value, setValue] = React.useState('apple')

return (
  <Command value={value} onValueChange={setValue}>
    <Command.Input />
    <Command.List>
      <Command.Item>Orange</Command.Item>
      <Command.Item>Apple</Command.Item>
    </Command.List>
  </Command>
)
```

You can provide a custom `filter` function that is called to rank each item. Note that the value will be trimmed.

```
<Command
  filter={(value, search) => {
    if (value.includes(search)) return 1
    return 0
  }}
/>
```

A third argument, `keywords`, can also be provided to the filter function. Keywords act as aliases for the item value, and can also affect the rank of the item. Keywords are trimmed.

```
<Command
  filter={(value, search, keywords) => {
    const extendValue = value + ' ' + keywords.join(' ')
    if (extendValue.includes(search)) return 1
    return 0
  }}
/>
```

Or disable filtering and sorting entirely:

```
<Command shouldFilter={false}>
  <Command.List>
    {filteredItems.map((item) => {
      return (
        <Command.Item key={item} value={item}>
          {item}
        </Command.Item>
      )
    })}
  </Command.List>
</Command>
```

You can make the arrow keys wrap around the list (when you reach the end, it goes back to the first item) by setting the `loop` prop:

```
<Command loop />
```

### Dialog `[cmdk-dialog]` `[cmdk-overlay]`

Props are forwarded to [Command](#command-cmdk-root). Composes Radix UI's Dialog component. The overlay is always rendered. See the [Radix Documentation](https://www.radix-ui.com/docs/primitives/components/dialog) for more information. Can be controlled with the `open` and `onOpenChange` props.

```
const [open, setOpen] = React.useState(false)

return (
  <Command.Dialog open={open} onOpenChange={setOpen}>
    ...
  </Command.Dialog>
)
```

You can provide a `container` prop that accepts an HTML element that is forwarded to Radix UI's Dialog Portal component to specify which element the Dialog should portal into (defaults to `body`). See the [Radix Documentation](https://www.radix-ui.com/docs/primitives/components/dialog#portal) for more information.

```
const containerElement = React.useRef(null)

return (
  <>
    <Command.Dialog container={containerElement.current} />
    <div ref={containerElement} />
  </>
)
```

### Input `[cmdk-input]`

All props are forwarded to the underlying `input` element. Can be controlled with the `value` and `onValueChange` props.

```
const [search, setSearch] = React.useState('')

return <Command.Input value={search} onValueChange={setSearch} />
```

### List `[cmdk-list]`

Contains items and groups. Animate height using the `--cmdk-list-height` CSS variable.

```
[cmdk-list] {
  min-height: 300px;
  height: var(--cmdk-list-height);
  max-height: 500px;
  transition: height 100ms ease;
}
```

To scroll item into view earlier near the edges of the viewport, use scroll-padding:

```
[cmdk-list] {
  scroll-padding-block-start: 8px;
  scroll-padding-block-end: 8px;
}
```

### Item `[cmdk-item]` `[data-disabled?]` `[data-selected?]`

Item that becomes active on pointer enter. You should provide a unique `value` for each item, but it will be automatically inferred from the `.textContent`.

```
<Command.Item
  onSelect={(value) => console.log('Selected', value)}
  // Value is implicity "apple" because of the provided text content
>
  Apple
</Command.Item>
```

You can also provide a `keywords` prop to help with filtering. Keywords are trimmed.

```
<Command.Item keywords={['fruit', 'apple']}>Apple</Command.Item>
```

```
<Command.Item
  onSelect={(value) => console.log('Selected', value)}
  // Value is implicity "apple" because of the provided text content
>
  Apple
</Command.Item>
```

You can force an item to always render, regardless of filtering, by passing the `forceMount` prop.

### Group `[cmdk-group]` `[hidden?]`

Groups items together with the given `heading` (`[cmdk-group-heading]`).

```
<Command.Group heading="Fruit">
  <Command.Item>Apple</Command.Item>
</Command.Group>
```

Groups will not unmount from the DOM, rather the `hidden` attribute is applied to hide it from view. This may be relevant in your styling.

You can force a group to always render, regardless of filtering, by passing the `forceMount` prop.

### Separator `[cmdk-separator]`

Visible when the search query is empty or `alwaysRender` is true, hidden otherwise.

### Empty `[cmdk-empty]`

Automatically renders when there are no results for the search query.

### Loading `[cmdk-loading]`

You should conditionally render this with `progress` while loading asynchronous items.

```
const [loading, setLoading] = React.useState(false)

return <Command.List>{loading && <Command.Loading>Hang on…</Command.Loading>}</Command.List>
```

### `useCommandState(state => state.selectedField)`

Hook that composes [`useSyncExternalStore`](https://reactjs.org/docs/hooks-reference.html#usesyncexternalstore). Pass a function that returns a slice of the command menu state to re-render when that slice changes. This hook is provided for advanced use cases and should not be commonly used.

A good use case would be to render a more detailed empty state, like so:

```
const search = useCommandState((state) => state.search)
return <Command.Empty>No results found for "{search}".</Command.Empty>
```

## Examples

Code snippets for common use cases.

### Nested items

Often selecting one item should navigate deeper, with a more refined set of items. For example selecting "Change theme…" should show new items "Dark theme" and "Light theme". We call these sets of items "pages", and they can be implemented with simple state:

```
const ref = React.useRef(null)
const [open, setOpen] = React.useState(false)
const [search, setSearch] = React.useState('')
const [pages, setPages] = React.useState([])
const page = pages[pages.length - 1]

return (
  <Command
    onKeyDown={(e) => {
      // Escape goes to previous page
      // Backspace goes to previous page when search is empty
      if (e.key === 'Escape' || (e.key === 'Backspace' && !search)) {
        e.preventDefault()
        setPages((pages) => pages.slice(0, -1))
      }
    }}
  >
    <Command.Input value={search} onValueChange={setSearch} />
    <Command.List>
      {!page && (
        <>
          <Command.Item onSelect={() => setPages([...pages, 'projects'])}>Search projects…</Command.Item>
          <Command.Item onSelect={() => setPages([...pages, 'teams'])}>Join a team…</Command.Item>
        </>
      )}

      {page === 'projects' && (
        <>
          <Command.Item>Project A</Command.Item>
          <Command.Item>Project B</Command.Item>
        </>
      )}

      {page === 'teams' && (
        <>
          <Command.Item>Team 1</Command.Item>
          <Command.Item>Team 2</Command.Item>
        </>
      )}
    </Command.List>
  </Command>
)
```

### Show sub-items when searching

If your items have nested sub-items that you only want to reveal when searching, render based on the search state:

```
const SubItem = (props) => {
  const search = useCommandState((state) => state.search)
  if (!search) return null
  return <Command.Item {...props} />
}

return (
  <Command>
    <Command.Input />
    <Command.List>
      <Command.Item>Change theme…</Command.Item>
      <SubItem>Change theme to dark</SubItem>
      <SubItem>Change theme to light</SubItem>
    </Command.List>
  </Command>
)
```

### Asynchronous results

Render the items as they become available. Filtering and sorting will happen automatically.

```
const [loading, setLoading] = React.useState(false)
const [items, setItems] = React.useState([])

React.useEffect(() => {
  async function getItems() {
    setLoading(true)
    const res = await api.get('/dictionary')
    setItems(res)
    setLoading(false)
  }

  getItems()
}, [])

return (
  <Command>
    <Command.Input />
    <Command.List>
      {loading && <Command.Loading>Fetching words…</Command.Loading>}
      {items.map((item) => {
        return (
          <Command.Item key={`word-${item}`} value={item}>
            {item}
          </Command.Item>
        )
      })}
    </Command.List>
  </Command>
)
```

### Use inside Popover

We recommend using the [Radix UI popover](https://www.radix-ui.com/docs/primitives/components/popover) component. ⌘K relies on the Radix UI Dialog component, so this will reduce your bundle size a bit due to shared dependencies.

```
$ pnpm install @radix-ui/react-popover
```

Render `Command` inside of the popover content:

```
import * as Popover from '@radix-ui/react-popover'

return (
  <Popover.Root>
    <Popover.Trigger>Toggle popover</Popover.Trigger>

    <Popover.Content>
      <Command>
        <Command.Input />
        <Command.List>
          <Command.Item>Apple</Command.Item>
        </Command.List>
      </Command>
    </Popover.Content>
  </Popover.Root>
)
```

### Drop in stylesheets

You can find global stylesheets to drop in as a starting point for styling. See [website/styles/cmdk](/dip/cmdk/blob/main/website/styles/cmdk) for examples.

## FAQ

**Accessible?** Yes. Labeling, aria attributes, and DOM ordering tested with Voice Over and Chrome DevTools. [Dialog](#dialog-cmdk-dialog-cmdk-overlay) composes an accessible Dialog implementation.

**Virtualization?** No. Good performance up to 2,000-3,000 items, though. Read below to bring your own.

**Filter/sort items manually?** Yes. Pass `shouldFilter={false}` to [Command](#command-cmdk-root). Better memory usage and performance. Bring your own virtualization this way.

**React 18 safe?** Yes, required. Uses React 18 hooks like `useId` and `useSyncExternalStore`.

**Unstyled?** Yes, use the listed CSS selectors.

**Hydration mismatch?** No, likely a bug in your code. Ensure the `open` prop to `Command.Dialog` is `false` on the server.

**React strict mode safe?** Yes. Open an issue if you notice an issue.

**Weird/wrong behavior?** Make sure your `Command.Item` has a `key` and unique `value`.

**Concurrent mode safe?** Maybe, but concurrent mode is not yet real. Uses risky approaches like manual DOM ordering.

**React server component?** No, it's a client component.

**Listen for ⌘K automatically?** No, do it yourself to have full control over keybind context.

**React Native?** No, and no plans to support it. If you build a React Native version, let us know and we'll link your repository here.

## History

Written in 2019 by Paco ([@pacocoursey](https://twitter.com/pacocoursey)) to see if a composable combobox API was possible. Used for the Vercel command menu and autocomplete by Rauno ([@raunofreiberg](https://twitter.com/raunofreiberg)) in 2020. Re-written independently in 2022 with a simpler and more performant approach. Ideas and help from Shu ([@shuding\_](https://twitter.com/shuding_)).

[use-descendants](https://github.com/pacocoursey/use-descendants) was extracted from the 2019 version.

## Testing

First, install dependencies and Playwright browsers:

```
pnpm install
pnpm playwright install
```

Then ensure you've built the library:

```
pnpm build
```

Then run the tests using your local build against real browser engines:

```
pnpm test
```

## About

Fast, unstyled command menu React component.

### Topics

[react](/topics/react "Topic: react")
[command-palette](/topics/command-palette "Topic: command-palette")
[combobox](/topics/combobox "Topic: combobox")
[radix-ui](/topics/radix-ui "Topic: radix-ui")
[command-menu](/topics/command-menu "Topic: command-menu")

### Resources

[Readme](#readme-ov-file)

### License

[MIT license](#MIT-1-ov-file)

### Uh oh!

There was an error while loading. Please reload this page.

[Activity](/dip/cmdk/activity)

[Custom properties](/dip/cmdk/custom-properties)

### Stars

[**12.2k**
stars](/dip/cmdk/stargazers)

### Watchers

[**26**
watching](/dip/cmdk/watchers)

### Forks

[**358**
forks](/dip/cmdk/forks)

[Report repository](/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fdip%2Fcmdk&report=dip+%28user%29)

## [Releases 12](/dip/cmdk/releases)

[v1.1.1

Latest

Mar 14, 2025](/dip/cmdk/releases/tag/v1.1.1)

[+ 11 releases](/dip/cmdk/releases)

## [Used by 401k](/dip/cmdk/network/dependents)

[- ![@Glyphor-Fuse](https://avatars.githubusercontent.com/u/254348344?s=64&v=4)
- ![@learnhouse](https://avatars.githubusercontent.com/u/101737021?s=64&v=4)
- ![@BankkRoll](https://avatars.githubusercontent.com/u/106103625?s=64&v=4)
- ![@Pantkartik](https://avatars.githubusercontent.com/u/181591353?s=64&v=4)
- ![@liamwilliams-67](https://avatars.githubusercontent.com/u/235625728?s=64&v=4)
- ![@Glyphor-Fuse](https://avatars.githubusercontent.com/u/254348344?s=64&v=4)
- ![@letta-ai](https://avatars.githubusercontent.com/u/177780362?s=64&v=4)
- ![@nk2028](https://avatars.githubusercontent.com/u/63484757?s=64&v=4)

+ 401,473](/dip/cmdk/network/dependents)

## [Contributors 51](/dip/cmdk/graphs/contributors)

- [![@pacocoursey](https://avatars.githubusercontent.com/u/34928425?s=64&v=4)](https://github.com/pacocoursey)
- [![@raunofreiberg](https://avatars.githubusercontent.com/u/23662329?s=64&v=4)](https://github.com/raunofreiberg)
- [![@joaom00](https://avatars.githubusercontent.com/u/48808846?s=64&v=4)](https://github.com/joaom00)
- [![@Kilian](https://avatars.githubusercontent.com/u/41970?s=64&v=4)](https://github.com/Kilian)
- [![@flaviouk](https://avatars.githubusercontent.com/u/8357327?s=64&v=4)](https://github.com/flaviouk)
- [![@0xcadams](https://avatars.githubusercontent.com/u/32714304?s=64&v=4)](https://github.com/0xcadams)
- [![@prestonbourne](https://avatars.githubusercontent.com/u/90055250?s=64&v=4)](https://github.com/prestonbourne)
- [![@tmcw](https://avatars.githubusercontent.com/u/32314?s=64&v=4)](https://github.com/tmcw)
- [![@Pagebakers](https://avatars.githubusercontent.com/u/32583?s=64&v=4)](https://github.com/Pagebakers)
- [![@bkrausz](https://avatars.githubusercontent.com/u/364070?s=64&v=4)](https://github.com/bkrausz)
- [![@pengx17](https://avatars.githubusercontent.com/u/584378?s=64&v=4)](https://github.com/pengx17)
- [![@kachkaev](https://avatars.githubusercontent.com/u/608862?s=64&v=4)](https://github.com/kachkaev)
- [![@Simek](https://avatars.githubusercontent.com/u/719641?s=64&v=4)](https://github.com/Simek)
- [![@alexcarpenter](https://avatars.githubusercontent.com/u/825855?s=64&v=4)](https://github.com/alexcarpenter)

[+ 37 contributors](/dip/cmdk/graphs/contributors)

## Languages

- [TypeScript
  78.6%](/dip/cmdk/search?l=typescript)
- [SCSS
  21.2%](/dip/cmdk/search?l=scss)
- Other
  0.2%