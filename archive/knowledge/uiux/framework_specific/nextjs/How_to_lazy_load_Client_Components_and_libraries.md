# How to lazy load Client Components and libraries

Source: https://nextjs.org/docs/app/building-your-application/optimizing/lazy-loading

---

Menu

Using App Router

Features available in /app

Latest Version

16.1.6

[App Router](/docs/app)[Guides](/docs/app/guides)Lazy Loading

Copy page

# How to lazy load Client Components and libraries

Last updated October 15, 2025

[Lazy loading](https://developer.mozilla.org/docs/Web/Performance/Lazy_loading) in Next.js helps improve the initial loading performance of an application by decreasing the amount of JavaScript needed to render a route.

It allows you to defer loading of **Client Components** and imported libraries, and only include them in the client bundle when they're needed. For example, you might want to defer loading a modal until a user clicks to open it.

There are two ways you can implement lazy loading in Next.js:

1. Using [Dynamic Imports](#nextdynamic) with `next/dynamic`
2. Using [`React.lazy()`](https://react.dev/reference/react/lazy) with [Suspense](https://react.dev/reference/react/Suspense)

By default, Server Components are automatically [code split](https://developer.mozilla.org/docs/Glossary/Code_splitting), and you can use [streaming](/docs/app/api-reference/file-conventions/loading) to progressively send pieces of UI from the server to the client. Lazy loading applies to Client Components.

## `next/dynamic`

`next/dynamic` is a composite of [`React.lazy()`](https://react.dev/reference/react/lazy) and [Suspense](https://react.dev/reference/react/Suspense). It behaves the same way in the `app` and `pages` directories to allow for incremental migration.

## Examples

### Importing Client Components

app/page.js

```
'use client'
 
import { useState } from 'react'
import dynamic from 'next/dynamic'
 
// Client Components:
const ComponentA = dynamic(() => import('../components/A'))
const ComponentB = dynamic(() => import('../components/B'))
const ComponentC = dynamic(() => import('../components/C'), { ssr: false })
 
export default function ClientComponentExample() {
  const [showMore, setShowMore] = useState(false)
 
  return (
    <div>
      {/* Load immediately, but in a separate client bundle */}
      <ComponentA />
 
      {/* Load on demand, only when/if the condition is met */}
      {showMore && <ComponentB />}
      <button onClick={() => setShowMore(!showMore)}>Toggle</button>
 
      {/* Load only on the client side */}
      <ComponentC />
    </div>
  )
}
```

> **Note:** When a Server Component dynamically imports a Client Component, automatic [code splitting](https://developer.mozilla.org/docs/Glossary/Code_splitting) is currently **not** supported.

### Skipping SSR

When using `React.lazy()` and Suspense, Client Components will be [prerendered](https://github.com/reactwg/server-components/discussions/4) (SSR) by default.

> **Note:** `ssr: false` option will only work for Client Components, move it into Client Components ensure the client code-splitting working properly.

If you want to disable pre-rendering for a Client Component, you can use the `ssr` option set to `false`:

```
const ComponentC = dynamic(() => import('../components/C'), { ssr: false })
```

### Importing Server Components

If you dynamically import a Server Component, only the Client Components that are children of the Server Component will be lazy-loaded - not the Server Component itself.
It will also help preload the static assets such as CSS when you're using it in Server Components.

app/page.js

```
import dynamic from 'next/dynamic'
 
// Server Component:
const ServerComponent = dynamic(() => import('../components/ServerComponent'))
 
export default function ServerComponentExample() {
  return (
    <div>
      <ServerComponent />
    </div>
  )
}
```

> **Note:** `ssr: false` option is not supported in Server Components. You will see an error if you try to use it in Server Components.
> `ssr: false` is not allowed with `next/dynamic` in Server Components. Please move it into a Client Component.

### Loading External Libraries

External libraries can be loaded on demand using the [`import()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/import) function. This example uses the external library `fuse.js` for fuzzy search. The module is only loaded on the client after the user types in the search input.

app/page.js

```
'use client'
 
import { useState } from 'react'
 
const names = ['Tim', 'Joe', 'Bel', 'Lee']
 
export default function Page() {
  const [results, setResults] = useState()
 
  return (
    <div>
      <input
        type="text"
        placeholder="Search"
        onChange={async (e) => {
          const { value } = e.currentTarget
          // Dynamically load fuse.js
          const Fuse = (await import('fuse.js')).default
          const fuse = new Fuse(names)
 
          setResults(fuse.search(value))
        }}
      />
      <pre>Results: {JSON.stringify(results, null, 2)}</pre>
    </div>
  )
}
```

### Adding a custom loading component

app/page.js

```
'use client'
 
import dynamic from 'next/dynamic'
 
const WithCustomLoading = dynamic(
  () => import('../components/WithCustomLoading'),
  {
    loading: () => <p>Loading...</p>,
  }
)
 
export default function Page() {
  return (
    <div>
      {/* The loading component will be rendered while  <WithCustomLoading/> is loading */}
      <WithCustomLoading />
    </div>
  )
}
```

### Importing Named Exports

To dynamically import a named export, you can return it from the Promise returned by [`import()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/import) function:

components/hello.js

```
'use client'
 
export function Hello() {
  return <p>Hello!</p>
}
```

app/page.js

```
import dynamic from 'next/dynamic'
 
const ClientComponent = dynamic(() =>
  import('../components/hello').then((mod) => mod.Hello)
)
```

Was this helpful?

supported.

Send