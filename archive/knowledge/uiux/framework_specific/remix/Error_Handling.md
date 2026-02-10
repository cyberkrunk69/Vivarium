# Error Handling

Source: https://remix.run/docs/en/main/guides/errors

---

[Docs](/docs)[Blog](https://remix.run/blog)[Resources](/resources)

React Router v7 has been released. [View the docs](https://reactrouter.com/home)

[Docs](/docs)[Blog](https://remix.run/blog)[Resources](/resources)

[View code on GitHub](https://github.com/remix-run/remix/tree/v2 "View code on GitHub")[Chat on Discord](https://rmx.as/discord "Chat on Discord")

React Router v7 has been released. [View the docs](https://reactrouter.com/home)

Error Handling

# Error Handling

Remix sets a new precedent in web application error handling that you are going to love. Remix automatically catches most errors in your code, on the server or in the browser, and renders the closest [`ErrorBoundary`](../route/error-boundary) to where the error occurred. If you're familiar with React's [`componentDidCatch`](https://react.dev/reference/react/Component#componentdidcatch) and [`getDerivedStateFromError`](https://react.dev/reference/react/Component#static-getderivedstatefromerror) class component hooks, it's just like that but with some extra handling for errors on the server.

Remix will automatically catch errors and render the nearest error boundary for errors thrown while:

- rendering in the browser
- rendering on the server
- in a `loader` during the initial server-rendered document request
- in an `action` during the initial server-rendered document request
- in a `loader` during a client-side transition in the browser (Remix serializes the error and sends it over the network to the browser)
- in an `action` during a client-side transition in the browser

## Root Error Boundary

By default, Remix ships with a default `ErrorBoundary` built-in, but we hope you'll want to add a little branding to your own global error boundary. You can do so by exporting your own [`ErrorBoundary`](../route/error-boundary) from `app/root.tsx`. This is what your users will see whenever an uncaught error is thrown.

```
export function ErrorBoundary() {
  const error = useRouteError();
  console.error(error);
  return (
    <html>
      <head>
        <title>Oh no!</title>
        <Meta />
        <Links />
      </head>
      <body>
        {/* add the UI you want your users to see */}
        <Scripts />
      </body>
    </html>
  );
}
```

You'll want to make sure to still render the [`Links`](../components/links), [`Meta`](../components/meta), and [`Scripts`](../components/scripts) components because the whole document will mount and unmount when the root error boundary is rendered.

## Nested Error Boundaries

Each route in the hierarchy is a potential error boundary. If a nested route exports an error boundary, then any errors below it will be caught and rendered there. This means that the rest of the surrounding UI in the parent routes *continue to render normally* so the user is able to click another link and not lose any client-side state they might have had.

For example, consider these routes:

```
app/
├── routes/
│   ├── sales.tsx
│   ├── sales.invoices.tsx
│   └── sales.invoices.$invoiceId.tsx
└── root.tsx
```

If `app/routes/sales.invoices.$invoiceId.tsx` exports an [`ErrorBoundary`](../route/error-boundary) and an error is thrown in its component, [`action`](../route/action), or [`loader`](../route/loader), the rest of the app renders normally and only the invoice section of the page renders the error.

![error in a nested route where the parent route's navigation renders normally](/docs-images/error-boundary.png)

If a route doesn't have an error boundary, the error "bubbles up" to the closest error boundary, all the way to the root, so you don't have to add error boundaries to every route--only when you want to add that extra touch to your UI.

## Error Sanitization

In production mode, any errors that happen on the server are automatically sanitized to prevent leaking any sensitive server information (such as stack traces) to the client. This means that the `Error` instance you receive from [`useRouteError`](../hooks/use-route-error) will have a generic message and no stack trace:

```
export async function loader() {
  if (badConditionIsTrue()) {
    throw new Error("Oh no! Something went wrong!");
  }
}

export function ErrorBoundary() {
  const error = useRouteError();
  // When NODE_ENV=production:
  // error.message = "Unexpected Server Error"
  // error.stack = undefined
}
```

If you need to log these errors or report them to a third-party service such as [BugSnag](https://www.bugsnag.com/) or [Sentry](https://sentry.io/), then you can do this through a [`handleError`](../file-conventions/entry.server#handleerror) export in your [`app/entry.server.js`](../file-conventions/entry.server). This method receives the unsanitized versions of the error since it is also running on the server.

If you want to trigger an error boundary and display a specific message or data in the browser, then you can throw a `Response` from a `action`/`loader` with that data instead:

```
export async function loader() {
  if (badConditionIsTrue()) {
    throw new Response("Oh no! Something went wrong!", {
      status: 500,
    });
  }
}

export function ErrorBoundary() {
  const error = useRouteError();
  if (isRouteErrorResponse(error)) {
    // error.status = 500
    // error.data = "Oh no! Something went wrong!"
  }
}
```

© [Shopify, Inc.](https://remix.run)

•

Docs and examples licensed under [MIT](https://opensource.org/licenses/MIT)

[Edit](https://github.com/remix-run/remix-v2-website/edit/main/data/docs/guides/errors.md)

![](/assets/icons-CZ8v8NWl.svg)