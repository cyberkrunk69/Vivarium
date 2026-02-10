# Form

Source: https://www.radix-ui.com/primitives/docs/components/form

---

[Radix Homepage](/)[Made by WorkOS](https://workos.com)

[Radix Homepage](/)[Made by WorkOS](https://workos.com)

[ThemesThemes](/)[PrimitivesPrimitives](/primitives)[IconsIcons](/icons)[ColorsColors](/colors)

[Documentation](/primitives/docs)[Case studies](/primitives/case-studies)[Blog](/blog)

Search

`/`

#### Overview

[Introduction](/primitives/docs/overview/introduction)[Getting started](/primitives/docs/overview/getting-started)[Accessibility](/primitives/docs/overview/accessibility)[Releases](/primitives/docs/overview/releases)

#### Guides

[Styling](/primitives/docs/guides/styling)[Animation](/primitives/docs/guides/animation)[Composition](/primitives/docs/guides/composition)[Server-side rendering](/primitives/docs/guides/server-side-rendering)

#### Components

[Accordion](/primitives/docs/components/accordion)[Alert Dialog](/primitives/docs/components/alert-dialog)[Aspect Ratio](/primitives/docs/components/aspect-ratio)[Avatar](/primitives/docs/components/avatar)[Checkbox](/primitives/docs/components/checkbox)[Collapsible](/primitives/docs/components/collapsible)[Context Menu](/primitives/docs/components/context-menu)[Dialog](/primitives/docs/components/dialog)[Dropdown Menu](/primitives/docs/components/dropdown-menu)[Form

Preview](/primitives/docs/components/form)[Hover Card](/primitives/docs/components/hover-card)[Label](/primitives/docs/components/label)[Menubar](/primitives/docs/components/menubar)[Navigation Menu](/primitives/docs/components/navigation-menu)[One-Time Password Field

Preview](/primitives/docs/components/one-time-password-field)[Password Toggle Field

Preview](/primitives/docs/components/password-toggle-field)[Popover](/primitives/docs/components/popover)[Progress](/primitives/docs/components/progress)[Radio Group](/primitives/docs/components/radio-group)[Scroll Area](/primitives/docs/components/scroll-area)[Select](/primitives/docs/components/select)[Separator](/primitives/docs/components/separator)[Slider](/primitives/docs/components/slider)[Switch](/primitives/docs/components/switch)[Tabs](/primitives/docs/components/tabs)[Toast](/primitives/docs/components/toast)[Toggle](/primitives/docs/components/toggle)[Toggle Group](/primitives/docs/components/toggle-group)[Toolbar](/primitives/docs/components/toolbar)[Tooltip](/primitives/docs/components/tooltip)

#### Utilities

[Accessible Icon](/primitives/docs/utilities/accessible-icon)[Direction Provider](/primitives/docs/utilities/direction-provider)[Portal](/primitives/docs/utilities/portal)[Slot](/primitives/docs/utilities/slot)[Visually Hidden](/primitives/docs/utilities/visually-hidden)

Components

# Form

Collect information from your users using validation rules.

Email

Question

Post question

index.jsxindex.jsxstyles.cssstyles.css

```
import * as React from "react";

import { Form } from "radix-ui";

import "./styles.css";

const FormDemo = () => (

<Form.Root className="FormRoot">

<Form.Field className="FormField" name="email">

<div
				style={{
					display: "flex",
					alignItems: "baseline",
					justifyContent: "space-between",
				}}
			>

<Form.Label className="FormLabel">Email</Form.Label>

<Form.Message className="FormMessage" match="valueMissing">

Please enter your email

</Form.Message>

<Form.Message className="FormMessage" match="typeMismatch">

Please provide a valid email

</Form.Message>

</div>

<Form.Control asChild>

<input className="Input" type="email" required />

</Form.Control>

</Form.Field>

<Form.Field className="FormField" name="question">

<div
				style={{
					display: "flex",
					alignItems: "baseline",
					justifyContent: "space-between",
				}}
			>

<Form.Label className="FormLabel">Question</Form.Label>

<Form.Message className="FormMessage" match="valueMissing">

Please enter a question

</Form.Message>

</div>

<Form.Control asChild>

<textarea className="Textarea" required />

</Form.Control>

</Form.Field>

<Form.Submit asChild>

<button className="Button" style={{ marginTop: 10 }}>

Post question

</button>

</Form.Submit>

</Form.Root>

);

export default FormDemo;

Expand code
```

## Features

Built on top of the native browser [constraint validation API.](https://developer.mozilla.org/en-US/docs/Web/HTML/Constraint_validation)

Supports built-in validation.

Supports custom validation.

Full customization of validation messages.

Accessible validation messages.

Supports client-side and server-side scenarios.

Focus is fully managed.

## [Installation](#installation)

Install the component from your command line.

```
npm install @radix-ui/react-form
```

## [Anatomy](#anatomy)

Import all parts and piece them together.

```
import { Form } from "radix-ui";

export default () => (

<Form.Root>

<Form.Field>

<Form.Label />

<Form.Control />

<Form.Message />

<Form.ValidityState />

</Form.Field>

<Form.Message />

<Form.ValidityState />

<Form.Submit />

</Form.Root>

);
```

## [API Reference](#api-reference)

### [Root](#root)

Contains all the parts of a form.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |
| `onClearServerErrors` Prop description | `function` See full type | No default value |

### [Field](#field)

The wrapper for a field. It handles id/name and label accessibility automatically.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |
| `name*` Prop description | `string` | No default value |
| `serverInvalid` Prop description | `boolean` | No default value |

| Data attribute | Values |
| --- | --- |
| `[data-invalid]` | Present when the field is invalid |
| `[data-valid]` | Present when the field is valid |

### [Label](#label)

A label element which is automatically wired when nested inside a `Field` part.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |

| Data attribute | Values |
| --- | --- |
| `[data-invalid]` | Present when the field is invalid |
| `[data-valid]` | Present when the field is valid |

### [Control](#control)

A control element (by default an `input`) which is automatically wired when nested inside a `Field` part.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |

| Data attribute | Values |
| --- | --- |
| `[data-invalid]` | Present when the field is invalid |
| `[data-valid]` | Present when the field is valid |

### [Message](#message)

A validation message which is automatically wired (functionality and accessibility) to a given control when nested inside a `Field` part. It can be used for built-in and custom client-side validation, as well as server-side validation. When used outside a `Field` you must pass a `name` prop matching a field.

`Form.Message` accepts a `match` prop which is used to determine when the message should show. It matches the native HTML validity state (`ValidityState` on [MDN](https://developer.mozilla.org/en-US/docs/Web/API/ValidityState)) which validates against attributes such as `required`, `min`, `max`. The message will show if the given `match` is `true` on the control’s validity state.

You can also pass a function to `match` to provide custom validation rules.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |
| `match` Prop description | `Matcher` See full type | No default value |
| `forceMatch` Prop description | `boolean` | `false` |
| `name` Prop description | `string` | No default value |

### [ValidityState](#validitystate)

Use this render-prop component to access a given field’s validity state in render (see `ValidityState` on [MDN](https://developer.mozilla.org/en-US/docs/Web/API/ValidityState)). A field's validity is available automatically when nested inside a `Field` part, otherwise you must pass a `name` prop to associate it.

| Prop | Type | Default |
| --- | --- | --- |
| `children` Prop description | `function` See full type | No default value |
| `name` Prop description | `string` | No default value |

### [Submit](#submit)

The submit button.

| Prop | Type | Default |
| --- | --- | --- |
| `asChild` Prop description | `boolean` | `false` |

## [Examples](#examples)

### [Composing with your own components](#composing-with-your-own-components)

Using `asChild` you can compose the `Form` primitive parts with your own components.

```
<Form.Field name="name">

<Form.Label>Full name</Form.Label>

<Form.Control asChild>

<TextField.Input variant="primary" />

</Form.Control>

</Form.Field>
```

It can also be used to compose other types of controls, such as a `select`:

```
<Form.Field name="country">

<Form.Label>Country</Form.Label>

<Form.Control asChild>

<select>

<option value="uk">United Kingdom</option>…

</select>

</Form.Control>

</Form.Field>
```

> Note: At the moment, it is not possible to compose `Form` with Radix's other form primitives such as `Checkbox`, `Select`, etc. We are working on a solution for this.

### [Providing your own validation messages](#providing-your-own-validation-messages)

When no `children` are provided, `Form.Message` will render a default error message for the given `match`.

```
// will yield "This value is missing"

<Form.Message match="valueMissing" />
```

You can provide a more meaningful message by passing your own `children`. This is also useful for internationalization.

```
// will yield "Please provide a name"

<Form.Message match="valueMissing">Please provide a name</Form.Message>
```

### [Custom validation](#custom-validation)

On top of all the built-in client-side validation matches described above you can also provide your own custom validation whilst still making use of the platform's validation abilities. It uses the `customError` type present in the [constraint validition API](https://developer.mozilla.org/en-US/docs/Web/HTML/Constraint_validation).

You can pass your own validation function into the `match` prop on `Form.Message`. Here's an example:

```
<Form.Field name="name">

<Form.Label>Full name</Form.Label>

<Form.Control />

<Form.Message match={(value, formData) => value !== "John"}>

Only John is allowed.

</Form.Message>

</Form.Field>
```

> `match` will be called with the current value of the control as first argument and the entire `FormData` as second argument.
> `match` can also be an `async` function (or return a promise) to perform async validation.

### [Styling based on validity](#styling-based-on-validity)

We add `data-valid` and `data-invalid` attributes to the relevant parts. Use it to style your components accordingly.
Here is an example styling the `Label` part.

```
//index.jsx

import * as React from "react";

import { Form } from "radix-ui";

export default () => (

<Form.Root>

<Form.Field name="email">

<Form.Label className="FormLabel">Email</Form.Label>

<Form.Control type="email" />

</Form.Field>

</Form.Root>

);
```

```
/* styles.css */

.FormLabel[data-invalid] {

color: red;

}

.FormLabel[data-valid] {

color: green;

}
```

### [Accessing the validity state for more control](#accessing-the-validity-state-for-more-control)

You may need to access the raw validity state of a field in order to display your own icons, or interface with a component library via it's defined props. You can do this by using the `Form.ValidityState` part:

```
<Form.Field name="name">

<Form.Label>Full name</Form.Label>

<Form.ValidityState>

{(validity) => (

<Form.Control asChild>

<TextField.Input
					variant="primary"
					state={getTextFieldInputState(validity)}
				/>

</Form.Control>

)}

</Form.ValidityState>

</Form.Field>
```

### [Server-side validation](#server-side-validation)

The component also supports server-side validation using the same `Form.Message` component.
You can re-use the same messages you defined for client-side errors by passing a `forceMatch` prop which will force the message to show regardless of the client-side matching logic.

If the message doesn't exist on the client-side, you can render a `Form.Message` without a `match` too.
The field is marked as invalid by passing a `serverInvalid` boolean prop to the `Form.Field` part.

Here's an example with server-side error handling:

```
import * as React from "react";

import { Form } from "radix-ui";

function Page() {

const [serverErrors, setServerErrors] = React.useState({

email: false,

password: false,

});

return (

<Form.Root
			// `onSubmit` only triggered if it passes client-side validation
			onSubmit={(event) => {
				const data = Object.fromEntries(new FormData(event.currentTarget));

				// Submit form data and catch errors in the response
				submitForm(data)
					.then(() => {})
					/**
					 * Map errors from your server response into a structure you'd like to work with.
					 * In this case resulting in this object: `{ email: false, password: true }`
					 */
					.catch((errors) => setServerErrors(mapServerErrors(errors)));

				// prevent default form submission
				event.preventDefault();
			}}
			onClearServerErrors={() =>
				setServerErrors({ email: false, password: false })
			}
		>

<Form.Field name="email" serverInvalid={serverErrors.email}>

<Form.Label>Email address</Form.Label>

<Form.Control type="email" required />

<Form.Message match="valueMissing">

Please enter your email.

</Form.Message>

<Form.Message match="typeMismatch" forceMatch={serverErrors.email}>

Please provide a valid email.

</Form.Message>

</Form.Field>

<Form.Field name="password" serverInvalid={serverErrors.password}>

<Form.Label>Password</Form.Label>

<Form.Control type="password" required />

<Form.Message match="valueMissing">

Please enter a password.

</Form.Message>

{serverErrors.password && (

<Form.Message>

Please provide a valid password. It should contain at least 1 number

and 1 special character.

</Form.Message>

)}

</Form.Field>

<Form.Submit>Submit</Form.Submit>

</Form.Root>

);

}
```

You should clear the server errors using the `onClearServerErrors` callback prop on the `Form.Root` part. It will clear the server errors before the form is re-submitted, and when the form is reset.

In addition, this provides control over when to reset single server errors. For example you could reset the email server error as soon as the user edits it:

```
<Form.Field name="email" serverInvalid={serverErrors.email}>

<Form.Label>Email address</Form.Label>

<Form.Control
		type="email"
		onChange={() => setServerErrors((prev) => ({ ...prev, email: false }))}
	/>

<Form.Message match="valueMissing">Please enter your email.</Form.Message>

<Form.Message match="typeMismatch" forceMatch={serverErrors.email}>

Please provide a valid email.

</Form.Message>

</Form.Field>
```

## [Accessibility](#accessibility)

The component follows the "inline errors" pattern for validation:

- Label and control are associated using the `name` provided on `Form.Field`
- When one or more client-side error messages display, they are automatically associated with their matching control and announced accordingly
- Focus is moved to the first invalid control

Previous[Dropdown Menu](/primitives/docs/components/dropdown-menu)

Next[Hover Card](/primitives/docs/components/hover-card)

[Edit this page on GitHub.](https://github.com/radix-ui/website/edit/main/data/primitives/docs/components/form.mdx "Edit this page on GitHub.")