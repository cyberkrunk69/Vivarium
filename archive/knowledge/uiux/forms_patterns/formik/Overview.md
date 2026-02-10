# Overview

Source: https://formik.org/docs/overview

---

# Overview

Let's face it, forms are really verbose in
[React](https://github.com/facebook/react). To make matters worse, most form
helpers do wayyyy too much magic and often have a significant performance cost
associated with them. Formik is a small library that helps you with the 3 most
annoying parts:

1. Getting values in and out of form state
2. Validation and error messages
3. Handling form submission

By colocating all of the above in one place, Formik will keep things
organized--making testing, refactoring, and reasoning about your forms a breeze.

## Motivation

I ([@jaredpalmer](https://twitter.com/jaredpalmer)) wrote Formik while building a large internal administrative dashboard with
[@eonwhite](https://twitter.com/eonwhite). With around ~30 unique forms, it
quickly became obvious that we could benefit by standardizing not just our input
components but also the way in which data flowed through our forms.

### Why not Redux-Form?

By now, you might be thinking, "Why didn't you just use
[Redux-Form](https://github.com/erikras/redux-form)?" Good question.

1. According to our prophet Dan Abramov,
   [**form state is inherently ephemeral and local**, so tracking it in Redux (or any kind of Flux library) is unnecessary](https://github.com/reactjs/redux/issues/1287#issuecomment-175351978)
2. Redux-Form calls your entire top-level Redux reducer multiple times ON EVERY
   SINGLE KEYSTROKE. This is fine for small apps, but as your Redux app grows,
   input latency will continue to increase if you use Redux-Form.
3. Redux-Form is 22.5 kB minified gzipped (Formik is 12.7 kB)

**My goal with Formik was to create a scalable, performant, form helper with a
minimal API that does the really really annoying stuff, and leaves the rest up
to you.**

---

My talk at React Alicante goes much deeper into Formik's motivation and philosophy, introduces the library (by watching me build a mini version of it), and demos how to build a non-trivial form (with arrays, custom inputs, etc.) using the real thing.

## Influences

Formik started by expanding on
[this little higher order component](https://github.com/jxnblk/rebass-recomposed/blob/master/src/withForm.js)
by [Brent Jackson](https://github.com/jxnblk), some naming conventions from
Redux-Form, and (most recently) the render props approach popularized by
[React-Motion](https://github.com/chenglou/react-motion) and
[React-Router 4](https://github.com/ReactTraining/react-router). Whether you
have used any of the above or not, Formik only takes a few minutes to get
started with.

## Installation

You can install Formik with [NPM](https://npmjs.com),
[Yarn](https://yarnpkg.com), or a good ol' `<script>` via
[unpkg.com](https://unpkg.com).

### NPM

Copy

```
npm install formik --save
```

or

Copy

```
yarn add formik
```

Formik is compatible with React v15+ and works with ReactDOM and React Native.

You can also try before you buy with this
**[demo of Formik on CodeSandbox.io](https://codesandbox.io/s/zKrK5YLDZ)**

### In-browser Playgrounds

You can play with Formik in your web browser with these live online playgrounds.

- [CodeSandbox (ReactDOM)](https://codesandbox.io/s/zKrK5YLDZ)
- [Snack (React Native)](https://snack.expo.io/?dependencies=yup%2Cformik%2Creact-native-paper%2Cexpo-constants&sourceUrl=https%3A%2F%2Fgist.githubusercontent.com%2Fbrentvatne%2F700e1dbf9c3e88a11aef8e557627ce3f%2Fraw%2Feeee57721c9890c1212ac34a4c37707f6354f469%2FApp.js)

## The Gist

Formik keeps track of your form's state and then exposes it plus a few reusable
methods and event handlers (`handleChange`, `handleBlur`, and `handleSubmit`) to
your form via `props`. `handleChange` and `handleBlur` work exactly as
expected--they use a `name` or `id` attribute to figure out which field to
update.

Copy

```
1 import React from 'react';

2 import { Formik } from 'formik';

3

4 const Basic = () => (

5   <div>

6     <h1>Anywhere in your app!</h1>

7     <Formik

8       initialValues={{ email: '', password: '' }}

9       validate={values => {

10         const errors = {};

11         if (!values.email) {

12           errors.email = 'Required';

13         } else if (

14           !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(values.email)

15         ) {

16           errors.email = 'Invalid email address';

17         }

18         return errors;

19       }}

20       onSubmit={(values, { setSubmitting }) => {

21         setTimeout(() => {

22           alert(JSON.stringify(values, null, 2));

23           setSubmitting(false);

24         }, 400);

25       }}

26     >

27       {({

28         values,

29         errors,

30         touched,

31         handleChange,

32         handleBlur,

33         handleSubmit,

34         isSubmitting,

35         /* and other goodies */

36       }) => (

37         <form onSubmit={handleSubmit}>

38           <input

39             type="email"

40             name="email"

41             onChange={handleChange}

42             onBlur={handleBlur}

43             value={values.email}

44           />

45           {errors.email && touched.email && errors.email}

46           <input

47             type="password"

48             name="password"

49             onChange={handleChange}

50             onBlur={handleBlur}

51             value={values.password}

52           />

53           {errors.password && touched.password && errors.password}

54           <button type="submit" disabled={isSubmitting}>

55             Submit

56           </button>

57         </form>

58       )}

59     </Formik>

60   </div>

61 );

62

63 export default Basic;
```

### Reducing boilerplate

The code above is very explicit about exactly what Formik is doing. `onChange` -> `handleChange`, `onBlur` -> `handleBlur`, and so on. However, to save you time, Formik comes with a few extra components to make life easier and less verbose: `<Form />`, `<Field />`, and `<ErrorMessage />`. They use React context to hook into the parent `<Formik />` state/methods.

Copy

```
1 // Render Prop

2 import React from 'react';

3 import { Formik, Form, Field, ErrorMessage } from 'formik';

4

5 const Basic = () => (

6   <div>

7     <h1>Any place in your app!</h1>

8     <Formik

9       initialValues={{ email: '', password: '' }}

10       validate={values => {

11         const errors = {};

12         if (!values.email) {

13           errors.email = 'Required';

14         } else if (

15           !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(values.email)

16         ) {

17           errors.email = 'Invalid email address';

18         }

19         return errors;

20       }}

21       onSubmit={(values, { setSubmitting }) => {

22         setTimeout(() => {

23           alert(JSON.stringify(values, null, 2));

24           setSubmitting(false);

25         }, 400);

26       }}

27     >

28       {({ isSubmitting }) => (

29         <Form>

30           <Field type="email" name="email" />

31           <ErrorMessage name="email" component="div" />

32           <Field type="password" name="password" />

33           <ErrorMessage name="password" component="div" />

34           <button type="submit" disabled={isSubmitting}>

35             Submit

36           </button>

37         </Form>

38       )}

39     </Formik>

40   </div>

41 );

42

43 export default Basic;
```

Read below for more information...

### Complementary Packages

As you can see above, validation is left up to you. Feel free to write your own
validators or use a 3rd party library. Personally, I use
[Yup](https://github.com/jquense/yup) for object schema validation. It has an
API that's pretty similar to [Joi](https://github.com/hapijs/joi) /
[React PropTypes](https://github.com/facebook/prop-types) but is small enough
for the browser and fast enough for runtime usage. Because I ❤️ Yup sooo
much, Formik has a special config option / prop for Yup called
[`validationSchema`](/docs/api/formik#validationschema-schema----schema) which will
automatically transform Yup's validation errors into a pretty object whose keys
match [`values`](/docs/api/formik#values-field-string-any) and
[`touched`](/docs/api/formik#touched-field-string-boolean). Anyways, you can
install Yup from npm...

Copy

```
npm install yup --save
```

or

Copy

```
yarn add yup
```

[NextTutorial](/docs/tutorial)

Was this page helpful?

![](/twemoji/1f62d.svg)![](/twemoji/1f615.svg)![](/twemoji/1f600.svg)![](/twemoji/1f929.svg)

[Edit this page on GitHub](https://github.com/formik/formik/edit/main/docs/overview.md)

#### On this page