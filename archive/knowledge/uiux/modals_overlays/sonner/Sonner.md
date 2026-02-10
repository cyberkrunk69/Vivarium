# Sonner

Source: https://sonner.emilkowal.ski/

---

# Sonner

An opinionated toast component for React.

Render a toast[GitHub](https://github.com/emilkowalski/sonner)

[Documentation](/getting-started)

## Installation

`npm install sonner`

## Usage

Render the toaster in the root of your app.

```
import { Toaster, toast } from 'sonner'

// ...

function App() {

return (

<div>

<Toaster />

<button onClick={() => toast('My first toast')}>

Give me a toast

</button>

</div>

)

}
```

## Types

You can customize the type of toast you want to render, and pass an options object as the second argument.

DefaultDescriptionSuccessInfoWarningErrorActionPromiseCustom

```
toast('Event has been created')
```

## Position

Swipe direction changes depending on the position.

top-lefttop-centertop-rightbottom-leftbottom-centerbottom-right

```
<Toaster position="bottom-right" />
```

## Expand

You can change the amount of toasts visible through the `visibleToasts` prop.

ExpandDefault

```
<Toaster expand={false} />
```

## Other

Rich Colors SuccessRich Colors ErrorRich Colors InfoRich Colors WarningClose ButtonHeadless

```
toast.success('Event has been created')

// ...

<Toaster richColors  />
```

## Want to learn how to make components like this one?

I created a course that teaches you how to create animations that feel right.

[Check out my animations course](https://animations.dev/)