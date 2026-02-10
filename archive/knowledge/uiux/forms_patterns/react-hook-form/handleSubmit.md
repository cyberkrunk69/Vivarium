# handleSubmit

Source: https://react-hook-form.com/docs/useform/handlesubmit

---

## </> `handleSubmit:` `((data: Object, e?: Event) => Promise<void>, (errors: Object, e?: Event) => Promise<void>) => Promise<void>`

This function will receive the form data if form validation is successful.

### Props

---

| Name | Type | Description |
| --- | --- | --- |
| SubmitHandler | `(data: Object, e?: Event) => Promise<void>` | A successful callback. |
| SubmitErrorHandler | `(errors: Object, e?: Event) => Promise<void>` | An error callback. |

**RULES**

- You can easily submit form asynchronously with handleSubmit.

  Copy

  ```
  handleSubmit(onSubmit)()

  // You can pass an async function for asynchronous validation.

  handleSubmit(async (data) => await fetchAPI(data))
  ```
- `disabled` inputs will appear as `undefined` values in form values. If you want to prevent users from updating an input and wish to retain the form value, you can use `readOnly` or disable the entire <fieldset />. Here is an [example](https://codesandbox.io/s/react-hook-form-disabled-inputs-oihxx).
- `handleSubmit` function will not swallow errors that occurred inside your onSubmit callback, so we recommend you to try and catch inside async request and handle those errors gracefully for your customers.

  ```
  const onSubmit = async () => {

  // async request which may result error

  try {

  // await fetch()

  } catch (e) {

  // handle your error

  }

  }

  return <form onSubmit={handleSubmit(onSubmit)} />
  ```

**Examples:**

---

**Sync**

TSJS

Copy [CodeSandbox TS](https://codesandbox.io/s/react-hook-form-handlesubmit-ts-v7-lcrtu)

```
import { useForm, SubmitHandler, SubmitErrorHandler } from "react-hook-form"

type FormValues = {

firstName: string

lastName: string

email: string

}

export default function App() {

const { register, handleSubmit } = useForm<FormValues>()

const onSubmit: SubmitHandler<FormValues> = (data) => console.log(data)

const onError: SubmitErrorHandler<FormValues> = (errors) =>

console.log(errors)

return (

<form onSubmit={handleSubmit(onSubmit, onError)}>

<input {...register("firstName")} />

<input {...register("lastName")} />

<input type="email" {...register("email")} />

<input type="submit" />

</form>

)

}
```

Copy [CodeSandbox JS](https://codesandbox.io/s/react-hook-form-handlesubmit-v7-uqmiy)

```
import { useForm } from "react-hook-form"

export default function App() {

const { register, handleSubmit } = useForm()

const onSubmit = (data, e) => console.log(data, e)

const onError = (errors, e) => console.log(errors, e)

return (

<form onSubmit={handleSubmit(onSubmit, onError)}>

<input {...register("firstName")} />

<input {...register("lastName")} />

<button type="submit">Submit</button>

</form>

)

}
```

**Async**

Copy [CodeSandbox JS](https://codesandbox.io/s/react-hook-form-async-submit-validation-kpx0o)

```
import { useForm } from "react-hook-form";

const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

function App() {

const { register, handleSubmit, formState: { errors } } = useForm();

const onSubmit = async data => {

await sleep(2000);

if (data.username === "bill") {

alert(JSON.stringify(data));

} else {

alert("There is an error");

}

};

return (

<form onSubmit={handleSubmit(onSubmit)}>

<label htmlFor="username">User Name</label>

<input placeholder="Bill" {...register("username"} />

<input type="submit" />

</form>

);

}
```

### Video

---

The following video tutorial explains the `handleSubmit` API in detail.

# Thank you for your support

If you find React Hook Form to be useful in your project, please consider to star and support it.

Star us on GitHub