# Font Optimization

Source: https://nextjs.org/docs/app/building-your-application/optimizing/fonts

---

Menu

Using App Router

Features available in /app

Latest Version

16.1.6

[App Router](/docs/app)[Getting Started](/docs/app/getting-started)Font Optimization

Copy page

# Font Optimization

Last updated January 15, 2026

The [`next/font`](/docs/app/api-reference/components/font) module automatically optimizes your fonts and removes external network requests for improved privacy and performance.

It includes **built-in self-hosting** for any font file. This means you can optimally load web fonts with no layout shift.

To start using `next/font`, import it from [`next/font/local`](#local-fonts) or [`next/font/google`](#google-fonts), call it as a function with the appropriate options, and set the `className` of the element you want to apply the font to. For example:

app/layout.tsx

TypeScript

JavaScriptTypeScript

```
import { Geist } from 'next/font/google'
 
const geist = Geist({
  subsets: ['latin'],
})
 
export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={geist.className}>
      <body>{children}</body>
    </html>
  )
}
```

Fonts are scoped to the component they're used in. To apply a font to your entire application, add it to the [Root Layout](/docs/app/api-reference/file-conventions/layout#root-layout).

## Google fonts

You can automatically self-host any Google Font. Fonts are included stored as static assets and served from the same domain as your deployment, meaning no requests are sent to Google by the browser when the user visits your site.

To start using a Google Font, import your chosen font from `next/font/google`:

app/layout.tsx

TypeScript

JavaScriptTypeScript

```
import { Geist } from 'next/font/google'
 
const geist = Geist({
  subsets: ['latin'],
})
 
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={geist.className}>
      <body>{children}</body>
    </html>
  )
}
```

We recommend using [variable fonts](https://fonts.google.com/variablefonts) for the best performance and flexibility. But if you can't use a variable font, you will need to specify a weight:

app/layout.tsx

TypeScript

JavaScriptTypeScript

```
import { Roboto } from 'next/font/google'
 
const roboto = Roboto({
  weight: '400',
  subsets: ['latin'],
})
 
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={roboto.className}>
      <body>{children}</body>
    </html>
  )
}
```

## Local fonts

To use a local font, import your font from `next/font/local` and specify the [`src`](/docs/app/api-reference/components/font#src) of your local font file. Fonts can be stored in the [`public`](/docs/app/api-reference/file-conventions/public-folder) folder or co-located inside the `app` folder. For example:

app/layout.tsx

TypeScript

JavaScriptTypeScript

```
import localFont from 'next/font/local'
 
const myFont = localFont({
  src: './my-font.woff2',
})
 
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={myFont.className}>
      <body>{children}</body>
    </html>
  )
}
```

If you want to use multiple files for a single font family, `src` can be an array:

```
const roboto = localFont({
  src: [
    {
      path: './Roboto-Regular.woff2',
      weight: '400',
      style: 'normal',
    },
    {
      path: './Roboto-Italic.woff2',
      weight: '400',
      style: 'italic',
    },
    {
      path: './Roboto-Bold.woff2',
      weight: '700',
      style: 'normal',
    },
    {
      path: './Roboto-BoldItalic.woff2',
      weight: '700',
      style: 'italic',
    },
  ],
})
```

## API Reference

See the API Reference for the full feature set of Next.js Font

[### Font

Optimizing loading web fonts with the built-in `next/font` loaders.](/docs/app/api-reference/components/font)

Was this helpful?

supported.

Send