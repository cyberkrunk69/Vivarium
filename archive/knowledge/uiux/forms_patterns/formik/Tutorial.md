# Tutorial

Source: https://formik.org/docs/tutorial

---

# Tutorial

## Before we start

Welcome to the Formik tutorial. This will teach you everything you need to know to build simple and complex forms in React.

If you’re impatient and just want to start hacking on your machine locally, check out [the 60-second quickstart](/docs/overview#installation).

### What are we building?

In this tutorial, we’ll build a complex newsletter signup form with React and Formik.

You can see what we’ll be building here: [Final Result](https://codesandbox.io/s/formik-v2-tutorial-final-ge1pt). If the code doesn’t make sense to you, don’t worry! The goal of this tutorial is to help you understand Formik.

### Prerequisites

You’ll need to have familiarity with HTML, CSS, [modern JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript/A_re-introduction_to_JavaScript), and [React](https://reactjs.org) (and [React Hooks](https://reactjs.org/docs/hooks-intro.html)) to fully understand Formik and how it works. In this tutorial, we’re using [arrow functions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions), [let](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/let), [const](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/const), [spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax), [destructuring](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment), [computed property names](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Object_initializer#Computed_property_names), and [async/await](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function) . You can use the [Babel REPL](https://babeljs.io/repl/#?presets=react&code_lz=MYewdgzgLgBApgGzgWzmWBeGAeAFgRgD4AJRBEAGhgHcQAnBAEwEJsB6AwgbgChRJY_KAEMAlmDh0YWRiGABXVOgB0AczhQAokiVQAQgE8AkowAUAcjogQUcwEpeAJTjDgUACIB5ALLK6aRklTRBQ0KCohMQk6Bx4gA) to check what ES6 code compiles to.

## Setup for the Tutorial

There are two ways to complete this tutorial: you can either write the code in your browser, or you can set up a local development environment on your computer.

### Setup Option 1: Write Code in the Browser

This is the quickest way to get started!

First, open this [Starter Code](https://codesandbox.io/s/formik-v2-tutorial-start-s04yr) in a new tab. The new tab should display an email address input, a submit button, and some React code. We’ll be editing the React code in this tutorial.

Skip the second setup option, and go to the [Overview](/docs/tutorial#overview-what-is-formik) section to get an overview of Formik.

### Setup Option 2: Local Development Environment

This is completely optional and not required for this tutorial!

**Optional: Instructions for following along locally using your preferred text editor**

This setup requires more work, but allows you to complete the tutorial using an editor of your choice. Here are the steps to follow:

1. Make sure you have a recent version of [Node.js](https://nodejs.org/en/) installed.
2. Follow the [installation instructions for Create React App](https://create-react-app.dev) to make a new project.

Copy

```
npx create-react-app my-app
```

1. Install Formik

Copy

```
npm i formik
```

Or

Copy

```
yarn add formik
```

1. Delete all files in the `src/` folder of the new project

> Note:
>
> **Don’t delete the entire `src` folder, just the original source files inside it.** We’ll replace the default source files with examples for this project in the next step.

Copy

```
1 cd my-app

2 cd src

3

4 # If you’re using a Mac or Linux:

5 rm -f *

6

7 # Or, if you’re on Windows:

8 del *

9

10 # Then, switch back to the project folder

11 cd ..
```

5. Add a file named `styles.css` in the `src/` folder with [this CSS code](https://codesandbox.io/s/formik-v2-tutorial-start-s04yr?file=/src/styles.css).
6. Add a file named `index.js` in the `src/` folder with [this JS code](https://codesandbox.io/s/formik-v2-tutorial-start-s04yr?file=/src/index.js:0-759).

Now run `npm start` in the project folder and open `http://localhost:3000` in the browser. You should see an email input and a submit button.

We recommend following [these instructions](https://babeljs.io/docs/editors/) to configure syntax highlighting for your editor.

### Help, I’m Stuck!

If you get stuck, check out Formik’s [GitHub Discussions](https://github.com/formik/formik/discussions). In addition, the [Formium Community Discord Server](https://discord.gg/pJSg287) is a great way to get help quickly too. If you don’t receive an answer, or if you remain stuck, please file an issue, and we’ll help you out.

## Overview: What is Formik?

Formik is a small group of React components and hooks for building forms in React and React Native. It helps with the three most annoying parts:

1. Getting values in and out of form state
2. Validation and error messages
3. Handling form submission

By colocating all of the above in one place, Formik keeps things
organized--making testing, refactoring, and reasoning about your forms a breeze.

## The Basics

We’re going to start with the *most verbose* way of using Formik. While this may seem a bit long-winded, it’s important to see how Formik builds on itself so you have a full grasp of what’s possible and a complete mental model of how it works.

### A simple newsletter signup form

Imagine we want to add a newsletter signup form for a blog. To start, our form will have just one field named `email`. With Formik, this is just a few lines of code.

Copy

```
1 import React from 'react';

2 import { useFormik } from 'formik';

3

4 const SignupForm = () => {

5   // Pass the useFormik() hook initial form values and a submit function that will

6   // be called when the form is submitted

7   const formik = useFormik({

8     initialValues: {

9       email: '',

10     },

11     onSubmit: values => {

12       alert(JSON.stringify(values, null, 2));

13     },

14   });

15   return (

16     <form onSubmit={formik.handleSubmit}>

17       <label htmlFor="email">Email Address</label>

18       <input

19         id="email"

20         name="email"

21         type="email"

22         onChange={formik.handleChange}

23         value={formik.values.email}

24       />

25

26       <button type="submit">Submit</button>

27     </form>

28   );

29 };
```

We pass our form’s `initialValues` and a submission function (`onSubmit`) to the `useFormik()` hook. The hook then returns to us a goodie bag of form state and helper methods in a variable we call `formik`. For now, the only helper methods we care about are as follows:

- `handleSubmit`: A submission handler
- `handleChange`: A change handler to pass to each `<input>`, `<select>`, or `<textarea>`
- `values`: Our form’s current values

As you can see above, we pass each of these to their respective props...and that’s it! We can now have a working form powered by Formik. Instead of managing our form’s values on our own and writing our own custom event handlers for every single input, we can just use `useFormik()`.

This is pretty neat, but with just one single input, the benefits of using `useFormik()` are unclear. So let’s add two more inputs: one for the user’s first and last name, which we’ll store as `firstName` and `lastName` in the form.

Copy

```
1 import React from 'react';

2 import { useFormik } from 'formik';

3

4 const SignupForm = () => {

5   // Note that we have to initialize ALL of fields with values. These

6   // could come from props, but since we don’t want to prefill this form,

7   // we just use an empty string. If we don’t do this, React will yell

8   // at us.

9   const formik = useFormik({

10     initialValues: {

11       firstName: '',

12       lastName: '',

13       email: '',

14     },

15     onSubmit: values => {

16       alert(JSON.stringify(values, null, 2));

17     },

18   });

19   return (

20     <form onSubmit={formik.handleSubmit}>

21       <label htmlFor="firstName">First Name</label>

22       <input

23         id="firstName"

24         name="firstName"

25         type="text"

26         onChange={formik.handleChange}

27         value={formik.values.firstName}

28       />

29

30       <label htmlFor="lastName">Last Name</label>

31       <input

32         id="lastName"

33         name="lastName"

34         type="text"

35         onChange={formik.handleChange}

36         value={formik.values.lastName}

37       />

38

39       <label htmlFor="email">Email Address</label>

40       <input

41         id="email"

42         name="email"

43         type="email"

44         onChange={formik.handleChange}

45         value={formik.values.email}

46       />

47

48       <button type="submit">Submit</button>

49     </form>

50   );

51 };
```

If you look carefully at our new code, you’ll notice some patterns and symmetry *forming*.

1. We reuse the same exact change handler function `handleChange` for each HTML input
2. We pass an `id` and `name` HTML attribute that *matches* the property we defined in `initialValues`
3. We access the field’s value using the same name (`email` -> `formik.values.email`)

If you’re familiar with building forms with plain React, you can think of Formik’s `handleChange` as working like this:

Copy

```
1 const [values, setValues] = React.useState({});

2

3 const handleChange = event => {

4   setValues(prevValues => ({

5     ...prevValues,

6     // we use the name to tell Formik which key of `values` to update

7     [event.target.name]: event.target.value

8   });

9 }
```

## Validation

While our contact form works, it’s not quite feature-complete; users can submit it, but it doesn’t tell them which (if any) fields are required.

If we’re okay with using the browser’s built-in HTML input validation, we could add a `required` prop to each of our inputs, specify minimum/maximum lengths (`maxlength` and `minlength`), and/or add a `pattern` prop for regex validation for each of these inputs. These are great if we can get away with them. However, HTML validation has its limitations. First, it only works in the browser! So this clearly is not viable for React Native. Second, it’s hard/impossible to show custom error messages to our user. Third, it’s very janky.

As mentioned earlier, Formik keeps track of not only your form’s `values`, but also its validation and error messages. To add validation with JS, let’s specify a custom validation function and pass it as `validate` to the `useFormik()` hook. If an error exists, this custom validation function should produce an `error` object with a matching shape to our `values`/`initialValues`. Again...*symmetry*...yes...

Copy

```
1 import React from 'react';

2 import { useFormik } from 'formik';

3

4 // A custom validation function. This must return an object

5 // which keys are symmetrical to our values/initialValues

6 const validate = values => {

7   const errors = {};

8   if (!values.firstName) {

9     errors.firstName = 'Required';

10   } else if (values.firstName.length > 15) {

11     errors.firstName = 'Must be 15 characters or less';

12   }

13

14   if (!values.lastName) {

15     errors.lastName = 'Required';

16   } else if (values.lastName.length > 20) {

17     errors.lastName = 'Must be 20 characters or less';

18   }

19

20   if (!values.email) {

21     errors.email = 'Required';

22   } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(values.email)) {

23     errors.email = 'Invalid email address';

24   }

25

26   return errors;

27 };

28

29 const SignupForm = () => {

30   // Pass the useFormik() hook initial form values, a validate function that will be called when

31   // form values change or fields are blurred, and a submit function that will

32   // be called when the form is submitted

33   const formik = useFormik({

34     initialValues: {

35       firstName: '',

36       lastName: '',

37       email: '',

38     },

39     validate,

40     onSubmit: values => {

41       alert(JSON.stringify(values, null, 2));

42     },

43   });

44   return (

45     <form onSubmit={formik.handleSubmit}>

46       <label htmlFor="firstName">First Name</label>

47       <input

48         id="firstName"

49         name="firstName"

50         type="text"

51         onChange={formik.handleChange}

52         value={formik.values.firstName}

53       />

54       {formik.errors.firstName ? <div>{formik.errors.firstName}</div> : null}

55

56       <label htmlFor="lastName">Last Name</label>

57       <input

58         id="lastName"

59         name="lastName"

60         type="text"

61         onChange={formik.handleChange}

62         value={formik.values.lastName}

63       />

64       {formik.errors.lastName ? <div>{formik.errors.lastName}</div> : null}

65

66       <label htmlFor="email">Email Address</label>

67       <input

68         id="email"

69         name="email"

70         type="email"

71         onChange={formik.handleChange}

72         value={formik.values.email}

73       />

74       {formik.errors.email ? <div>{formik.errors.email}</div> : null}

75

76       <button type="submit">Submit</button>

77     </form>

78   );

79 };
```

`formik.errors` is populated via the custom validation function. By default, Formik will validate after each keystroke (change event), each input’s [blur event](https://developer.mozilla.org/en-US/docs/Web/API/Element/blur_event), as well as prior to submission. The `onSubmit` function we passed to `useFormik()` will be executed only if there are no errors (i.e. if our `validate` function returns `{}`).

## Visited fields

While our form works, and our users see each error, it’s not a great user experience for them. Since our validation function runs on each keystroke against the *entire* form’s `values`, our `errors` object contains *all* validation errors at any given moment. In our component, we’re just checking if an error exists and then immediately showing it to the user. This is awkward since we’re going to show error messages for fields that the user hasn’t even visited yet. Most of the time, we only want to show a field’s error message *after* our user is done typing in that field.

Like `errors` and `values`, Formik keeps track of which fields have been visited. It stores this information in an object called `touched` that also mirrors the shape of `values`/`initialValues`. The keys of `touched` are the field names, and the values of `touched` are booleans `true`/`false`.

To take advantage of `touched`, we pass `formik.handleBlur` to each input’s `onBlur` prop. This function works similarly to `formik.handleChange` in that it uses the `name` attribute to figure out which field to update.

Copy

```
1 import React from 'react';

2 import { useFormik } from 'formik';

3

4 const validate = values => {

5   const errors = {};

6

7   if (!values.firstName) {

8     errors.firstName = 'Required';

9   } else if (values.firstName.length > 15) {

10     errors.firstName = 'Must be 15 characters or less';

11   }

12

13   if (!values.lastName) {

14     errors.lastName = 'Required';

15   } else if (values.lastName.length > 20) {

16     errors.lastName = 'Must be 20 characters or less';

17   }

18

19   if (!values.email) {

20     errors.email = 'Required';

21   } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(values.email)) {

22     errors.email = 'Invalid email address';

23   }

24

25   return errors;

26 };

27

28 const SignupForm = () => {

29   const formik = useFormik({

30     initialValues: {

31       firstName: '',

32       lastName: '',

33       email: '',

34     },

35     validate,

36     onSubmit: values => {

37       alert(JSON.stringify(values, null, 2));

38     },

39   });

40   return (

41     <form onSubmit={formik.handleSubmit}>

42       <label htmlFor="firstName">First Name</label>

43       <input

44         id="firstName"

45         name="firstName"

46         type="text"

47         onChange={formik.handleChange}

48         onBlur={formik.handleBlur}

49         value={formik.values.firstName}

50       />

51       {formik.errors.firstName ? <div>{formik.errors.firstName}</div> : null}

52

53       <label htmlFor="lastName">Last Name</label>

54       <input

55         id="lastName"

56         name="lastName"

57         type="text"

58         onChange={formik.handleChange}

59         onBlur={formik.handleBlur}

60         value={formik.values.lastName}

61       />

62       {formik.errors.lastName ? <div>{formik.errors.lastName}</div> : null}

63

64       <label htmlFor="email">Email Address</label>

65       <input

66         id="email"

67         name="email"

68         type="email"

69         onChange={formik.handleChange}

70         onBlur={formik.handleBlur}

71         value={formik.values.email}

72       />

73       {formik.errors.email ? <div>{formik.errors.email}</div> : null}

74

75       <button type="submit">Submit</button>

76     </form>

77   );

78 };
```

Almost there! Now that we’re tracking `touched`, we can now change our error message render logic to *only* show a given field’s error message if it exists *and* if our user has visited that field.

Copy

```
1 import React from 'react';

2 import { useFormik } from 'formik';

3

4 const validate = values => {

5   const errors = {};

6

7   if (!values.firstName) {

8     errors.firstName = 'Required';

9   } else if (values.firstName.length > 15) {

10     errors.firstName = 'Must be 15 characters or less';

11   }

12

13   if (!values.lastName) {

14     errors.lastName = 'Required';

15   } else if (values.lastName.length > 20) {

16     errors.lastName = 'Must be 20 characters or less';

17   }

18

19   if (!values.email) {

20     errors.email = 'Required';

21   } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(values.email)) {

22     errors.email = 'Invalid email address';

23   }

24

25   return errors;

26 };

27

28 const SignupForm = () => {

29   const formik = useFormik({

30     initialValues: {

31       firstName: '',

32       lastName: '',

33       email: '',

34     },

35     validate,

36     onSubmit: values => {

37       alert(JSON.stringify(values, null, 2));

38     },

39   });

40   return (

41     <form onSubmit={formik.handleSubmit}>

42       <label htmlFor="firstName">First Name</label>

43       <input

44         id="firstName"

45         name="firstName"

46         type="text"

47         onChange={formik.handleChange}

48         onBlur={formik.handleBlur}

49         value={formik.values.firstName}

50       />

51       {formik.touched.firstName && formik.errors.firstName ? (

52         <div>{formik.errors.firstName}</div>

53       ) : null}

54

55       <label htmlFor="lastName">Last Name</label>

56       <input

57         id="lastName"

58         name="lastName"

59         type="text"

60         onChange={formik.handleChange}

61         onBlur={formik.handleBlur}

62         value={formik.values.lastName}

63       />

64       {formik.touched.lastName && formik.errors.lastName ? (

65         <div>{formik.errors.lastName}</div>

66       ) : null}

67

68       <label htmlFor="email">Email Address</label>

69       <input

70         id="email"

71         name="email"

72         type="email"

73         onChange={formik.handleChange}

74         onBlur={formik.handleBlur}

75         value={formik.values.email}

76       />

77       {formik.touched.email && formik.errors.email ? (

78         <div>{formik.errors.email}</div>

79       ) : null}

80

81       <button type="submit">Submit</button>

82     </form>

83   );

84 };
```

### Schema Validation with Yup

As you can see above, validation is left up to you. Feel free to write your own validators or use a 3rd-party helper library. Formik’s authors/a large portion of its users use [Jason Quense](https://github.com/jquense)’s library [Yup](https://github.com/jquense/yup) for object schema validation. Yup has an API that’s similar to [Joi](https://github.com/hapijs/joi) and [React PropTypes](https://github.com/facebook/prop-types), but is also small enough for the browser and fast enough for runtime usage. You can try it out here with this [REPL](https://runkit.com/jquense/yup).

Since Formik authors/users *love* Yup so much, Formik has a special configuration prop for Yup called `validationSchema` which will automatically transform Yup’s validation errors messages into a pretty object whose keys match `values`/`initialValues`/`touched` (just like any custom validation function would have to). Anyways, you can install Yup from NPM/yarn like so...

Copy

```
1 npm install yup --save

2

3 # or via yarn

4

5 yarn add yup
```

To see how Yup works, let’s get rid of our custom validation function `validate` and re-write our validation with Yup and `validationSchema`:

Copy

```
1 import React from 'react';

2 import { useFormik } from 'formik';

3 import * as Yup from 'yup';

4

5 const SignupForm = () => {

6   const formik = useFormik({

7     initialValues: {

8       firstName: '',

9       lastName: '',

10       email: '',

11     },

12     validationSchema: Yup.object({

13       firstName: Yup.string()

14         .max(15, 'Must be 15 characters or less')

15         .required('Required'),

16       lastName: Yup.string()

17         .max(20, 'Must be 20 characters or less')

18         .required('Required'),

19       email: Yup.string().email('Invalid email address').required('Required'),

20     }),

21     onSubmit: values => {

22       alert(JSON.stringify(values, null, 2));

23     },

24   });

25   return (

26     <form onSubmit={formik.handleSubmit}>

27       <label htmlFor="firstName">First Name</label>

28       <input

29         id="firstName"

30         name="firstName"

31         type="text"

32         onChange={formik.handleChange}

33         onBlur={formik.handleBlur}

34         value={formik.values.firstName}

35       />

36       {formik.touched.firstName && formik.errors.firstName ? (

37         <div>{formik.errors.firstName}</div>

38       ) : null}

39

40       <label htmlFor="lastName">Last Name</label>

41       <input

42         id="lastName"

43         name="lastName"

44         type="text"

45         onChange={formik.handleChange}

46         onBlur={formik.handleBlur}

47         value={formik.values.lastName}

48       />

49       {formik.touched.lastName && formik.errors.lastName ? (

50         <div>{formik.errors.lastName}</div>

51       ) : null}

52

53       <label htmlFor="email">Email Address</label>

54       <input

55         id="email"

56         name="email"

57         type="email"

58         onChange={formik.handleChange}

59         onBlur={formik.handleBlur}

60         value={formik.values.email}

61       />

62       {formik.touched.email && formik.errors.email ? (

63         <div>{formik.errors.email}</div>

64       ) : null}

65

66       <button type="submit">Submit</button>

67     </form>

68   );

69 };
```

Again, Yup is 100% optional. However, we suggest giving it a try. As you can see above, we expressed the exact same validation function with just 10 lines of code instead of 30. One of Formik’s core design principles is to help you stay organized. Yup definitely helps a lot with this--schemas are extremely expressive, intuitive (since they mirror your values), and reusable. Whether or not you use Yup, we highly recommended you share commonly used validation methods across your application. This will ensure that common fields (e.g. email, street addresses, usernames, phone numbers, etc.) are validated consistently and result in a better user experience.

## Reducing Boilerplate

### `getFieldProps()`

The code above is very explicit about exactly what Formik is doing. `onChange` -> `handleChange`, `onBlur` -> `handleBlur`, and so on. However, to save you time, `useFormik()` returns a helper method called `formik.getFieldProps()` to make it faster to wire up inputs. Given some field-level info, it returns to you the exact group of `onChange`, `onBlur`, `value`, `checked` for a given field. You can then spread that on an `input`, `select`, or `textarea`.

Copy

```
1 import React from 'react';

2 import { useFormik } from 'formik';

3 import * as Yup from 'yup';

4

5 const SignupForm = () => {

6   const formik = useFormik({

7     initialValues: {

8       firstName: '',

9       lastName: '',

10       email: '',

11     },

12     validationSchema: Yup.object({

13       firstName: Yup.string()

14         .max(15, 'Must be 15 characters or less')

15         .required('Required'),

16       lastName: Yup.string()

17         .max(20, 'Must be 20 characters or less')

18         .required('Required'),

19       email: Yup.string().email('Invalid email address').required('Required'),

20     }),

21     onSubmit: values => {

22       alert(JSON.stringify(values, null, 2));

23     },

24   });

25   return (

26     <form onSubmit={formik.handleSubmit}>

27       <label htmlFor="firstName">First Name</label>

28       <input

29         id="firstName"

30         type="text"

31         {...formik.getFieldProps('firstName')}

32       />

33       {formik.touched.firstName && formik.errors.firstName ? (

34         <div>{formik.errors.firstName}</div>

35       ) : null}

36

37       <label htmlFor="lastName">Last Name</label>

38       <input id="lastName" type="text" {...formik.getFieldProps('lastName')} />

39       {formik.touched.lastName && formik.errors.lastName ? (

40         <div>{formik.errors.lastName}</div>

41       ) : null}

42

43       <label htmlFor="email">Email Address</label>

44       <input id="email" type="email" {...formik.getFieldProps('email')} />

45       {formik.touched.email && formik.errors.email ? (

46         <div>{formik.errors.email}</div>

47       ) : null}

48

49       <button type="submit">Submit</button>

50     </form>

51   );

52 };
```

### Leveraging React Context

Our code above is again very explicit about exactly what Formik is doing. `onChange` -> `handleChange`, `onBlur` -> `handleBlur`, and so on. However, we still have to manually pass each input this "prop getter" `getFieldProps()`. To save you even more time, Formik comes with [React Context](https://reactjs.org/docs/context.html)-powered API/components to make life easier and code less verbose: `<Formik />`, `<Form />`, `<Field />`, and `<ErrorMessage />`. More explicitly, they use React Context implicitly to connect with the parent `<Formik />` state/methods.

Since these components use React Context, we need to render a [React Context Provider](https://reactjs.org/docs/context.html#contextprovider) that holds our form state and helpers in our tree. If you did this yourself, it would look like:

Copy

```
1 import React from 'react';

2 import { useFormik } from 'formik';

3

4 // Create empty context

5 const FormikContext = React.createContext({});

6

7 // Place all of what’s returned by useFormik into context

8 export const Formik = ({ children, ...props }) => {

9   const formikStateAndHelpers = useFormik(props);

10   return (

11     <FormikContext.Provider value={formikStateAndHelpers}>

12       {typeof children === 'function'

13         ? children(formikStateAndHelpers)

14         : children}

15     </FormikContext.Provider>

16   );

17 };
```

Luckily, we’ve done this for you in a `<Formik>` component that works just like this.

Let’s now swap out the `useFormik()` hook for Formik’s `<Formik>` component/render-prop. Since it’s a component, we’ll convert the object passed to `useFormik()` to JSX, with each key becoming a prop.

Copy

```
1 import React from 'react';

2 import { Formik } from 'formik';

3 import * as Yup from 'yup';

4

5 const SignupForm = () => {

6   return (

7     <Formik

8       initialValues={{ firstName: '', lastName: '', email: '' }}

9       validationSchema={Yup.object({

10         firstName: Yup.string()

11           .max(15, 'Must be 15 characters or less')

12           .required('Required'),

13         lastName: Yup.string()

14           .max(20, 'Must be 20 characters or less')

15           .required('Required'),

16         email: Yup.string().email('Invalid email address').required('Required'),

17       })}

18       onSubmit={(values, { setSubmitting }) => {

19         setTimeout(() => {

20           alert(JSON.stringify(values, null, 2));

21           setSubmitting(false);

22         }, 400);

23       }}

24     >

25       {formik => (

26         <form onSubmit={formik.handleSubmit}>

27           <label htmlFor="firstName">First Name</label>

28           <input

29             id="firstName"

30             type="text"

31             {...formik.getFieldProps('firstName')}

32           />

33           {formik.touched.firstName && formik.errors.firstName ? (

34             <div>{formik.errors.firstName}</div>

35           ) : null}

36

37           <label htmlFor="lastName">Last Name</label>

38           <input

39             id="lastName"

40             type="text"

41             {...formik.getFieldProps('lastName')}

42           />

43           {formik.touched.lastName && formik.errors.lastName ? (

44             <div>{formik.errors.lastName}</div>

45           ) : null}

46

47           <label htmlFor="email">Email Address</label>

48           <input id="email" type="email" {...formik.getFieldProps('email')} />

49           {formik.touched.email && formik.errors.email ? (

50             <div>{formik.errors.email}</div>

51           ) : null}

52

53           <button type="submit">Submit</button>

54         </form>

55       )}

56     </Formik>

57   );

58 };
```

As you can see above, we swapped out `useFormik()` hook and replaced it with the `<Formik>` component. The `<Formik>` component accepts a function as its children (a.k.a. a [render prop](https://reactjs.org/docs/render-props.html)). Its argument is the *exact* same object returned by `useFormik()` (in fact, `<Formik>` calls `useFormik()` internally!). Thus, our form works the same as before, except now we can use new components to express ourselves in a more concise manner.

Copy

```
1 import React from 'react';

2 import { Formik, Field, Form, ErrorMessage } from 'formik';

3 import * as Yup from 'yup';

4

5 const SignupForm = () => {

6   return (

7     <Formik

8       initialValues={{ firstName: '', lastName: '', email: '' }}

9       validationSchema={Yup.object({

10         firstName: Yup.string()

11           .max(15, 'Must be 15 characters or less')

12           .required('Required'),

13         lastName: Yup.string()

14           .max(20, 'Must be 20 characters or less')

15           .required('Required'),

16         email: Yup.string().email('Invalid email address').required('Required'),

17       })}

18       onSubmit={(values, { setSubmitting }) => {

19         setTimeout(() => {

20           alert(JSON.stringify(values, null, 2));

21           setSubmitting(false);

22         }, 400);

23       }}

24     >

25       <Form>

26         <label htmlFor="firstName">First Name</label>

27         <Field name="firstName" type="text" />

28         <ErrorMessage name="firstName" />

29

30         <label htmlFor="lastName">Last Name</label>

31         <Field name="lastName" type="text" />

32         <ErrorMessage name="lastName" />

33

34         <label htmlFor="email">Email Address</label>

35         <Field name="email" type="email" />

36         <ErrorMessage name="email" />

37

38         <button type="submit">Submit</button>

39       </Form>

40     </Formik>

41   );

42 };
```

The `<Field>` component by default will render an `<input>` component that, given a `name` prop, will implicitly grab the respective `onChange`, `onBlur`, `value` props and pass them to the element as well as any props you pass to it. However, since not everything is an input, `<Field>` also accepts a few other props to let you render whatever you want. Some examples..

Copy

```
1 // <input className="form-input" placeHolder="Jane"  />

2 <Field name="firstName" className="form-input" placeholder="Jane" />

3

4 // <textarea className="form-textarea"/></textarea>

5 <Field name="message" as="textarea" className="form-textarea" />

6

7 // <select className="my-select"/>

8 <Field name="colors" as="select" className="my-select">

9   <option value="red">Red</option>

10   <option value="green">Green</option>

11   <option value="blue">Blue</option>

12 </Field>
```

React is all about composition, and while we’ve cut down on a lot of the [prop-drilling](https://kentcdodds.com/blog/prop-drilling), we’re still repeating ourselves with a `label`, `<Field>`, and `<ErrorMessage>` for each of our inputs. We can do better with an abstraction! With Formik, you can and should build reusable input primitive components that you can share around your application. Turns out our `<Field>` render-prop component has a sister and her name is `useField` that’s going to do the same thing, but via React Hooks! Check this out...

Copy

```
1 import React from 'react';

2 import ReactDOM from 'react-dom';

3 import { Formik, Form, useField } from 'formik';

4 import * as Yup from 'yup';

5

6 const MyTextInput = ({ label, ...props }) => {

7   // useField() returns [formik.getFieldProps(), formik.getFieldMeta()]

8   // which we can spread on <input>. We can use field meta to show an error

9   // message if the field is invalid and it has been touched (i.e. visited)

10   const [field, meta] = useField(props);

11   return (

12     <>

13       <label htmlFor={props.id || props.name}>{label}</label>

14       <input className="text-input" {...field} {...props} />

15       {meta.touched && meta.error ? (

16         <div className="error">{meta.error}</div>

17       ) : null}

18     </>

19   );

20 };

21

22 const MyCheckbox = ({ children, ...props }) => {

23   // React treats radios and checkbox inputs differently from other input types: select and textarea.

24   // Formik does this too! When you specify `type` to useField(), it will

25   // return the correct bag of props for you -- a `checked` prop will be included

26   // in `field` alongside `name`, `value`, `onChange`, and `onBlur`

27   const [field, meta] = useField({ ...props, type: 'checkbox' });

28   return (

29     <div>

30       <label className="checkbox-input">

31         <input type="checkbox" {...field} {...props} />

32         {children}

33       </label>

34       {meta.touched && meta.error ? (

35         <div className="error">{meta.error}</div>

36       ) : null}

37     </div>

38   );

39 };

40

41 const MySelect = ({children, label, ...props }) => {

42   const [field, meta] = useField(props);

43   return (

44     <div>

45       <label htmlFor={props.id || props.name}>{label}</label>

46       <select {...field} {...props} />

47       {children}

48       {meta.touched && meta.error ? (

49         <div className="error">{meta.error}</div>

50       ) : null}

51     </div>

52   );

53 };

54

55 // And now we can use these

56 const SignupForm = () => {

57   return (

58     <>

59       <h1>Subscribe!</h1>

60       <Formik

61         initialValues={{

62           firstName: '',

63           lastName: '',

64           email: '',

65           acceptedTerms: false, // added for our checkbox

66           jobType: '', // added for our select

67         }}

68         validationSchema={Yup.object({

69           firstName: Yup.string()

70             .max(15, 'Must be 15 characters or less')

71             .required('Required'),

72           lastName: Yup.string()

73             .max(20, 'Must be 20 characters or less')

74             .required('Required'),

75           email: Yup.string()

76             .email('Invalid email address')

77             .required('Required'),

78           acceptedTerms: Yup.boolean()

79             .required('Required')

80             .oneOf([true], 'You must accept the terms and conditions.'),

81           jobType: Yup.string()

82             .oneOf(

83               ['designer', 'development', 'product', 'other'],

84               'Invalid Job Type'

85             )

86             .required('Required'),

87         })}

88         onSubmit={(values, { setSubmitting }) => {

89           setTimeout(() => {

90             alert(JSON.stringify(values, null, 2));

91             setSubmitting(false);

92           }, 400);

93         }}

94       >

95         <Form>

96           <MyTextInput

97             label="First Name"

98             name="firstName"

99             type="text"

100             placeholder="Jane"

101           />

102

103           <MyTextInput

104             label="Last Name"

105             name="lastName"

106             type="text"

107             placeholder="Doe"

108           />

109

110           <MyTextInput

111             label="Email Address"

112             name="email"

113             type="email"

114             placeholder="jane@formik.com"

115           />

116

117           <MySelect label="Job Type" name="jobType">

118             <option value="">Select a job type</option>

119             <option value="designer">Designer</option>

120             <option value="development">Developer</option>

121             <option value="product">Product Manager</option>

122             <option value="other">Other</option>

123           </MySelect>

124

125           <MyCheckbox name="acceptedTerms">

126             I accept the terms and conditions

127           </MyCheckbox>

128

129           <button type="submit">Submit</button>

130         </Form>

131       </Formik>

132     </>

133   );

134 };
```

As you can see above, `useField()` gives us the ability to connect any kind input of React component to Formik as if it were a `<Field>` + `<ErrorMessage>`. We can use it to build a group of reusable inputs that fit our needs.

## Wrapping Up

Congratulations! You’ve created a signup form with Formik that:

- Has complex validation logic and rich error messages
- Properly displays errors messages to the user at the correct time (after they have blurred a field)
- Leverages your own custom input components you can use on other forms in your app

Nice work! We hope you now feel like you have a decent grasp on how Formik works.

Check out the final result here: [Final Result](https://codesandbox.io/s/formik-v2-tutorial-final-ge1pt).

If you have extra time or want to practice your new Formik skills, here are some ideas for improvements that you could make to the signup form which are listed in order of increasing difficulty:

- Disable the submit button while the user has attempted to submit (hint: `formik.isSubmitting`)
- Add a reset button with `formik.handleReset` or `<button type="reset">`.
- Pre-populate `initialValues` based on URL query string or props passed to `<SignupForm>`.
- Change the input border color to red when a field has an error and isn’t focused
- Add a shake animation to each field when it displays an error and has been visited
- Persist form state to the browser’s [sessionStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/sessionStorage) so that form progress is kept in between page refreshes

Throughout this tutorial, we touched on Formik concepts including form state, fields, validation, hooks, render props, and React context. For a more detailed explanation of each of these topics, check out the rest of the [documentation](/docs/overview). To learn more about defining the components and hooks in the tutorial, check out the [API reference](/docs/api/formik).

[PreviousGetting Started](/docs/overview)[NextResources](/docs/resources)

Was this page helpful?

![](/twemoji/1f62d.svg)![](/twemoji/1f615.svg)![](/twemoji/1f600.svg)![](/twemoji/1f929.svg)

[Edit this page on GitHub](https://github.com/formik/formik/edit/main/docs/tutorial.md)

#### On this page