# useWatch

Source: https://react-hook-form.com/docs/usewatch

---

Select page...Watch

## </> `useWatch:` `({ control?: Control, name?: string, defaultValue?: unknown, disabled?: boolean }) => object`

Behaves similarly to the `watch` API, however, this will isolate re-rendering at the custom hook level and potentially result in better performance for your application.

### Props

---

| Name | Type | Description |
| --- | --- | --- |
| `name` | string | string[] | undefined | Name of the field. |
| `control` | Object | [`control`](/docs/useform/control) object provided by `useForm`. It's optional if you are using `FormProvider`. |
| `compute` | function | Subscribe to selective and computed form values.   - Subscribe to the entire form but only return updated value with certain condition ```    const watchedValue = useWatch({  compute: (data: FormValue) => {  if (data.test?.length) return data.test;    return '';  },  });   ``` - Subscribe to a specific form value state ```    const watchedValue = useWatch({  name: 'test',  compute: (data: string) => {  return data.length ? data : '';  },  });   ``` |
| `defaultValue` | unknown | default value for `useWatch` to return before the initial render.  **Note:** the first render will always return `defaultValue` when it's supplied. |
| `disabled` | boolean = false | Option to disable the subscription. |
| `exact` | boolean = false | This prop will enable an exact match for input name subscriptions. |

### Return

---

| Example | Return |
| --- | --- |
| `useWatch({ name: 'inputName' })` | unknown |
| `useWatch({ name: ['inputName1'] })` | unknown[] |
| `useWatch()` | `{[key:string]: unknown}` |

**RULES**

- The initial return value from `useWatch` will always return what's inside of `defaultValue` or `defaultValues` from `useForm`.
- The only difference between `useWatch` and `watch` is at the root ([`useForm`](/docs/useform)) level or the custom hook level update.
- `useWatch`'s execution order matters, which means if you update a form value before the subscription is in place, then the value updated will be ignored.

  Copy

  ```
  setValue("test", "data")

  useWatch({ name: "test" }) // ❌ subscription is happened after value update, no update received

  useWatch({ name: "example" }) // ✅ input value update will be received and trigger re-render

  setValue("example", "data")
  ```

  You can overcome the above issue with a simple custom hook as below:

  Copy

  ```
  const useFormValues = () => {

  const { getValues } = useFormContext()

  return {

  ...useWatch(), // subscribe to form value updates

  ...getValues(), // always merge with latest form values

  }

  }
  ```
- `useWatch`'s result is optimised for render phase instead of `useEffect`'s deps, to detect value updates you may want to use an external custom hook for value comparison.

**Examples:**

---

**Form**

TSJS

Copy [CodeSandbox TS](https://codesandbox.io/s/react-hook-form-v7-ts-usewatch-h9i5e)

```
import { useForm, useWatch } from "react-hook-form"

interface FormInputs {

firstName: string

lastName: string

}

function FirstNameWatched({ control }: { control: Control<FormInputs> }) {

const firstName = useWatch({

control,

name: "firstName", // without supply name will watch the entire form, or ['firstName', 'lastName'] to watch both

defaultValue: "default", // default value before the render

})

return <p>Watch: {firstName}</p> // only re-render at the custom hook level, when firstName changes

}

function App() {

const { register, control, handleSubmit } = useForm<FormInputs>()

const onSubmit = (data: FormInputs) => {

console.log(data)

}

return (

<form onSubmit={handleSubmit(onSubmit)}>

<label>First Name:</label>

<input {...register("firstName")} />

<input {...register("lastName")} />

<input type="submit" />

<FirstNameWatched control={control} />

</form>

)

}
```

Copy [CodeSandbox JS](https://codesandbox.io/s/react-hook-form-v7-usewatch-forked-9872t)

```
import { useForm, useWatch } from "react-hook-form"

function Child({ control }) {

const firstName = useWatch({

control,

name: "firstName",

})

return <p>Watch: {firstName}</p>

}

function App() {

const { register, control } = useForm({

defaultValues: {

firstName: "test",

},

})

return (

<form>

<input {...register("firstName")} />

<Child control={control} />

</form>

)

}
```

**Advanced Field Array**

Copy [CodeSandbox JS](https://codesandbox.io/s/watchusewatch-calc-4tpnh)

```
import { useWatch } from "react-hook-form"

function totalCal(results) {

let totalValue = 0

for (const key in results) {

for (const value in results[key]) {

if (typeof results[key][value] === "string") {

const output = parseInt(results[key][value], 10)

totalValue = totalValue + (Number.isNaN(output) ? 0 : output)

} else {

totalValue = totalValue + totalCal(results[key][value], totalValue)

}

}

}

return totalValue

}

export const Calc = ({ control, setValue }) => {

const results = useWatch({ control, name: "test" })

const output = totalCal(results)

// isolated re-render to calc the result with Field Array

console.log(results)

setValue("total", output)

return <p>{output}</p>

}
```

# Thank you for your support

If you find React Hook Form to be useful in your project, please consider to star and support it.

Star us on GitHub