# Data Fetching

Source: https://swr.vercel.app/docs/data-fetching

---

# Data Fetching

```
const { data, error } = useSWR(key, fetcher)
```

This is the very fundamental API of SWR. The `fetcher` here is an async function that **accepts the `key`** of SWR, and returns the data.

The returned value will be passed as `data`, and if it throws, it will be caught as `error`.

Note that `fetcher` can be omitted from the parameters if it's 
[provided globally](/docs/global-configuration).

## [Fetch](#fetch)

You can use any library to handle data fetching, for example a `fetch` polyfill [developit/unfetch](https://github.com/developit/unfetch):

```
import fetch from 'unfetch'

const fetcher = url => fetch(url).then(r => r.json())

function App () {
  const { data, error } = useSWR('/api/data', fetcher)
  // ...
}
```

If you are using **Next.js**, you don't need to import this polyfill:  
[New Built-In Polyfills: fetch(), URL, and Object.assign](https://nextjs.org/blog/next-9-1-7#new-built-in-polyfills-fetch-url-and-objectassign)

## [Axios](#axios)

```
import axios from 'axios'

const fetcher = url => axios.get(url).then(res => res.data)

function App () {
  const { data, error } = useSWR('/api/data', fetcher)
  // ...
}
```

## [GraphQL](#graphql)

Or using GraphQL with libs like [graphql-request](https://github.com/prisma-labs/graphql-request):

```
import { request } from 'graphql-request'

const fetcher = query => request('/api/graphql', query)

function App () {
  const { data, error } = useSWR(
    `{
      Movie(title: "Inception") {
        releaseDate
        actors {
          name
        }
      }
    }`,
    fetcher
  )
  // ...
}
```

*If you want to pass variables to a GraphQL query, check out [Multiple Arguments](/en/docs/arguments).*