# Validation

Source: https://formik.org/docs/guides/validation

---

# Validation

Formik is designed to manage forms with complex validation with ease. Formik supports synchronous and asynchronous
form-level and field-level validation. Furthermore, it comes with baked-in support for schema-based form-level validation through Yup. This guide will describe the ins and outs of all of the above.

## Flavors of Validation

### Form-level Validation

Form-level validation is useful because you have complete access to all of your form's `values` and props whenever the function runs, so you can validate dependent fields at the same time.

There are 2 ways to do form-level validation with Formik:

- `<Formik validate>` and `withFormik({ validate: ... })`
- `<Formik validationSchema>` and `withFormik({ validationSchema: ... })`

#### `validate`

`<Formik>` and `withFormik()` take a prop/option called `validate` that accepts either a synchronous or asynchronous function.

Copy

```
1 // Synchronous validation

2 const validate = (values, props /* only available when using withFormik */) => {

3   const errors = {};

4

5   if (!values.email) {

6     errors.email = 'Required';

7   } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(values.email)) {

8     errors.email = 'Invalid email address';

9   }

10

11   //...

12

13   return errors;

14 };

15

16 // Async Validation

17 const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

18

19 const validate = (values, props /* only available when using withFormik */) => {

20   return sleep(2000).then(() => {

21     const errors = {};

22     if (['admin', 'null', 'god'].includes(values.username)) {

23       errors.username = 'Nice try';

24     }

25     // ...

26     return errors;

27   });

28 };
```

For more information about `<Formik validate>`, see the API reference.

#### `validationSchema`

As you can see above, validation is left up to you. Feel free to write your own
validators or use a 3rd party library. At The Palmer Group, we use
[Yup](https://github.com/jquense/yup) for object schema validation. It has an
API that's pretty similar to [Joi](https://github.com/hapijs/joi) and
[React PropTypes](https://github.com/facebook/prop-types) but is small enough
for the browser and fast enough for runtime usage. Because we ❤️ Yup sooo
much, Formik has a special config option / prop for Yup object schemas called `validationSchema` which will automatically transform Yup's validation errors into a pretty object whose keys match `values` and `touched`. This symmetry makes it easy to manage business logic around error messages.

To add Yup to your project, install it from NPM.

Copy

```
npm install yup --save
```

Copy

```
1 import React from 'react';

2 import { Formik, Form, Field } from 'formik';

3 import * as Yup from 'yup';

4

5 const SignupSchema = Yup.object().shape({

6   firstName: Yup.string()

7     .min(2, 'Too Short!')

8     .max(50, 'Too Long!')

9     .required('Required'),

10   lastName: Yup.string()

11     .min(2, 'Too Short!')

12     .max(50, 'Too Long!')

13     .required('Required'),

14   email: Yup.string().email('Invalid email').required('Required'),

15 });

16

17 export const ValidationSchemaExample = () => (

18   <div>

19     <h1>Signup</h1>

20     <Formik

21       initialValues={{

22         firstName: '',

23         lastName: '',

24         email: '',

25       }}

26       validationSchema={SignupSchema}

27       onSubmit={values => {

28         // same shape as initial values

29         console.log(values);

30       }}

31     >

32       {({ errors, touched }) => (

33         <Form>

34           <Field name="firstName" />

35           {errors.firstName && touched.firstName ? (

36             <div>{errors.firstName}</div>

37           ) : null}

38           <Field name="lastName" />

39           {errors.lastName && touched.lastName ? (

40             <div>{errors.lastName}</div>

41           ) : null}

42           <Field name="email" type="email" />

43           {errors.email && touched.email ? <div>{errors.email}</div> : null}

44           <button type="submit">Submit</button>

45         </Form>

46       )}

47     </Formik>

48   </div>

49 );
```

For more information about `<Formik validationSchema>`, see the API reference.

### Field-level Validation

#### `validate`

Formik supports field-level validation via the `validate` prop of `<Field>`/`<FastField>` components or `useField` hook. This function can be synchronous or asynchronous (return a Promise). It will run after any `onChange` and `onBlur` by default. This behavior can be altered at the top level `<Formik/>` component using the `validateOnChange` and `validateOnBlur` props respectively. In addition to change/blur, all field-level validations are run at the beginning of a submission attempt and then the results are deeply merged with any top-level validation results.

> Note: The `<Field>/<FastField>` components' `validate` function will only be executed on mounted fields. That is to say, if any of your fields unmount during the flow of your form (e.g. Material-UI's `<Tabs>` unmounts the previous `<Tab>` your user was on), those fields will not be validated during form validation/submission.

Copy

```
1 import React from 'react';

2 import { Formik, Form, Field } from 'formik';

3

4 function validateEmail(value) {

5   let error;

6   if (!value) {

7     error = 'Required';

8   } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(value)) {

9     error = 'Invalid email address';

10   }

11   return error;

12 }

13

14 function validateUsername(value) {

15   let error;

16   if (value === 'admin') {

17     error = 'Nice try!';

18   }

19   return error;

20 }

21

22 export const FieldLevelValidationExample = () => (

23   <div>

24     <h1>Signup</h1>

25     <Formik

26       initialValues={{

27         username: '',

28         email: '',

29       }}

30       onSubmit={values => {

31         // same shape as initial values

32         console.log(values);

33       }}

34     >

35       {({ errors, touched, isValidating }) => (

36         <Form>

37           <Field name="email" validate={validateEmail} />

38           {errors.email && touched.email && <div>{errors.email}</div>}

39

40           <Field name="username" validate={validateUsername} />

41           {errors.username && touched.username && <div>{errors.username}</div>}

42

43           <button type="submit">Submit</button>

44         </Form>

45       )}

46     </Formik>

47   </div>

48 );
```

### Manually Triggering Validation

You can manually trigger both form-level and field-level validation with Formik using the `validateForm` and `validateField` methods respectively.

Copy

```
1 import React from 'react';

2 import { Formik, Form, Field } from 'formik';

3

4 function validateEmail(value) {

5   let error;

6   if (!value) {

7     error = 'Required';

8   } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(value)) {

9     error = 'Invalid email address';

10   }

11   return error;

12 }

13

14 function validateUsername(value) {

15   let error;

16   if (value === 'admin') {

17     error = 'Nice try!';

18   }

19   return error;

20 }

21

22 export const FieldLevelValidationExample = () => (

23   <div>

24     <h1>Signup</h1>

25     <Formik

26       initialValues={{

27         username: '',

28         email: '',

29       }}

30       onSubmit={values => {

31         // same shape as initial values

32         console.log(values);

33       }}

34     >

35       {({ errors, touched, validateField, validateForm }) => (

36         <Form>

37           <Field name="email" validate={validateEmail} />

38           {errors.email && touched.email && <div>{errors.email}</div>}

39

40           <Field name="username" validate={validateUsername} />

41           {errors.username && touched.username && <div>{errors.username}</div>}

42           {/** Trigger field-level validation

43            imperatively */}

44           <button type="button" onClick={() => validateField('username')}>

45             Check Username

46           </button>

47           {/** Trigger form-level validation

48            imperatively */}

49           <button

50             type="button"

51             onClick={() => validateForm().then(() => console.log('blah'))}

52           >

53             Validate All

54           </button>

55           <button type="submit">Submit</button>

56         </Form>

57       )}

58     </Formik>

59   </div>

60 );
```

## When Does Validation Run?

You can control when Formik runs validation by changing the values of `<Formik validateOnChange>` and/or `<Formik validateOnBlur>` props depending on your needs. By default, Formik will run validation methods as follows:

**After "change" events/methods** (things that update`values`)

- `handleChange`
- `setFieldValue`
- `setValues`

**After "blur" events/methods** (things that update `touched`)

- `handleBlur`
- `setTouched`
- `setFieldTouched`

**Whenever submission is attempted**

- `handleSubmit`
- `submitForm`

There are also imperative helper methods provided to you via Formik's render/injected props which you can use to imperatively call validation.

- `validateForm`
- `validateField`

## Displaying Error Messages

Error messages are dependent on the form's validation. If an error exists, and the validation function produces an error object (as it should) with a matching shape to our values/initialValues, dependent field errors can be accessed from the errors object.

Copy

```
1 import React from 'react';

2 import { Formik, Form, Field } from 'formik';

3 import * as Yup from 'yup';

4

5 const DisplayingErrorMessagesSchema = Yup.object().shape({

6   username: Yup.string()

7     .min(2, 'Too Short!')

8     .max(50, 'Too Long!')

9     .required('Required'),

10   email: Yup.string().email('Invalid email').required('Required'),

11 });

12

13 export const DisplayingErrorMessagesExample = () => (

14   <div>

15     <h1>Displaying Error Messages</h1>

16     <Formik

17       initialValues={{

18         username: '',

19         email: '',

20       }}

21       validationSchema={DisplayingErrorMessagesSchema}

22       onSubmit={values => {

23         // same shape as initial values

24         console.log(values);

25       }}

26     >

27       {({ errors, touched }) => (

28         <Form>

29           <Field name="username" />

30           {/* If this field has been touched, and it contains an error, display it

31            */}

32           {touched.username && errors.username && <div>{errors.username}</div>}

33           <Field name="email" />

34           {/* If this field has been touched, and it contains an error, display

35           it */}

36           {touched.email && errors.email && <div>{errors.email}</div>}

37           <button type="submit">Submit</button>

38         </Form>

39       )}

40     </Formik>

41   </div>

42 );
```

> The [ErrorMessage](/docs/api/errormessage) component can also be used to display error messages.

## Frequently Asked Questions

How do I determine if my form is validating?

If `isValidating` prop is `true`

Can I return `null` as an error message?

No. Use `undefined` instead. Formik uses `undefined` to represent empty states. If you use `null`, several parts of Formik's computed props (e.g. `isValid` for example), will not work as expected.

How do I test validation?

Formik has extensive unit tests for Yup validation so you do not need to test that. However, if you are rolling your own validation functions, you should simply unit test those. If you do need to test Formik's execution you should use the imperative `validateForm` and `validateField` methods respectively.

[PreviousMigrating from v1.x to v2.x](/docs/migrating-v2)[NextArrays](/docs/guides/arrays)

Was this page helpful?

![](/twemoji/1f62d.svg)![](/twemoji/1f615.svg)![](/twemoji/1f600.svg)![](/twemoji/1f929.svg)

[Edit this page on GitHub](https://github.com/formik/formik/edit/main/docs/guides/validation.md)

#### On this page