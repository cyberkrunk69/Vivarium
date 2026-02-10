# Form Validation

Source: https://remix.run/docs/en/main/guides/form-validation

---

[Docs](/docs)[Blog](https://remix.run/blog)[Resources](/resources)

React Router v7 has been released. [View the docs](https://reactrouter.com/home)

[Docs](/docs)[Blog](https://remix.run/blog)[Resources](/resources)

[View code on GitHub](https://github.com/remix-run/remix/tree/v2 "View code on GitHub")[Chat on Discord](https://rmx.as/discord "Chat on Discord")

React Router v7 has been released. [View the docs](https://reactrouter.com/home)

Form Validation

On this page

- [Step 1: Setting Up the Signup Form](/docs/guides/form-validation/#step-1-setting-up-the-signup-form)
- [Step 2: Defining the Action](/docs/guides/form-validation/#step-2-defining-the-action)
- [Step 3: Displaying Validation Errors](/docs/guides/form-validation/#step-3-displaying-validation-errors)
- [Conclusion](/docs/guides/form-validation/#conclusion)

- [Step 1: Setting Up the Signup Form](/docs/guides/form-validation/#step-1-setting-up-the-signup-form)
- [Step 2: Defining the Action](/docs/guides/form-validation/#step-2-defining-the-action)
- [Step 3: Displaying Validation Errors](/docs/guides/form-validation/#step-3-displaying-validation-errors)
- [Conclusion](/docs/guides/form-validation/#conclusion)

# Form Validation

This guide walks you through implementing form validation for a simple signup form in Remix. Here, we focus on capturing the fundamentals to help you understand the essential elements of form validation in Remix, including [`action`](../route/action)s, action data, and rendering errors.

## Step 1: Setting Up the Signup Form

We'll start by creating a basic signup form using the [`Form`](../components/form) component from Remix.

```
import { Form } from "@remix-run/react";

export default function Signup() {
  return (
    <Form method="post">
      <p>
        <input type="email" name="email" />
      </p>

      <p>
        <input type="password" name="password" />
      </p>

      <button type="submit">Sign Up</button>
    </Form>
  );
}
```

## Step 2: Defining the Action

In this step, we'll define a server `action` in the same file as our `Signup` component. Note that the aim here is to provide a broad overview of the mechanics involved rather than digging deep into form validation rules or error object structures. We'll use rudimentary checks for the email and password to demonstrate the core concepts.

```
import type { ActionFunctionArgs } from "@remix-run/node"; // or cloudflare/deno
import { json, redirect } from "@remix-run/node"; // or cloudflare/deno
import { Form } from "@remix-run/react";

export default function Signup() {
  // omitted for brevity
}

export async function action({
  request,
}: ActionFunctionArgs) {
  const formData = await request.formData();
  const email = String(formData.get("email"));
  const password = String(formData.get("password"));

  const errors = {};

  if (!email.includes("@")) {
    errors.email = "Invalid email address";
  }

  if (password.length < 12) {
    errors.password =
      "Password should be at least 12 characters";
  }

  if (Object.keys(errors).length > 0) {
    return json({ errors });
  }

  // Redirect to dashboard if validation is successful
  return redirect("/dashboard");
}
```

If any validation errors are found, they are returned from the `action` to the client. This is our way of signaling to the UI that something needs to be corrected; otherwise the user will be redirected to the dashboard.

## Step 3: Displaying Validation Errors

Finally, we'll modify the `Signup` component to display validation errors, if any. We'll use [`useActionData`](../hooks/use-action-data) to access and display these errors.

```
import type { ActionFunctionArgs } from "@remix-run/node"; // or cloudflare/deno
import { json, redirect } from "@remix-run/node"; // or cloudflare/deno
import { Form, useActionData } from "@remix-run/react";

export default function Signup() {
  const actionData = useActionData<typeof action>();

  return (
    <Form method="post">
      <p>
        <input type="email" name="email" />
        {actionData?.errors?.email ? (
          <em>{actionData?.errors.email}</em>
        ) : null}
      </p>

      <p>
        <input type="password" name="password" />
        {actionData?.errors?.password ? (
          <em>{actionData?.errors.password}</em>
        ) : null}
      </p>

      <button type="submit">Sign Up</button>
    </Form>
  );
}

export async function action({
  request,
}: ActionFunctionArgs) {
  // omitted for brevity
}
```

## Conclusion

And there you have it! You've successfully set up a basic form validation flow in Remix. The beauty of this approach is that the errors will automatically display based on the `action` data, and they will be updated each time the user re-submits the form. This reduces the amount of boilerplate code you have to write, making your development process more efficient.

© [Shopify, Inc.](https://remix.run)

•

Docs and examples licensed under [MIT](https://opensource.org/licenses/MIT)

[Edit](https://github.com/remix-run/remix-v2-website/edit/main/data/docs/guides/form-validation.md)

![](/assets/icons-CZ8v8NWl.svg)