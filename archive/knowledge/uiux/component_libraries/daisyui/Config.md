# Config

Source: https://daisyui.com/docs/config/

---

# Config

 

How to change the default configuration of daisyUI?

 

daisyUI can be configured from your CSS file.

Replace the semicolon `;` after `@plugin "daisyui"` with brackets `{}` and add the configuration inside the brackets.

app.css

```
- @plugin "daisyui";
+ @plugin "daisyui" {
+ }
```

Default config:

app.css

```
@plugin "daisyui" {
  themes: light --default, dark --prefersdark;
  root: ":root";
  include: ;
  exclude: ;
  prefix: ;
  logs: true;
}
```

## themes

| Default value | Type | Description |
| --- | --- | --- |
| `light --default, dark --prefersdark` | string or comma separated list or `false` or `all` | List of themes to enable. Use `false` to disable all themes. Use `all` to enable all themes. Add `--default` flag next to a theme name to set it as default theme. Add `--prefersdark` flag next to a theme name to set it as default theme for dark mode. |

Example

```
@plugin "daisyui" {
  themes: nord --default, abyss --prefersdark, cupcake, dracula;
}
```

In above example, we have 4 themes: `nord`, `abyss`, `cupcake`, and `dracula`. nord is the default theme, abyss is the default theme for dark mode, and cupcake and dracula are available to use with `data-theme="cupcake"` and `data-theme="dracula"`.

Example

```
@plugin "daisyui" {
  themes: all;
}
```

In above example, we enable all themes.

Example

```
@plugin "daisyui" {
  themes: false;
}
```

In above example, we disable all themes. it's useful to disable all themes and add custom themes using [`@plugin "daisyui/theme"`](/docs/themes/#how-to-add-a-new-custom-theme)

Example

```
@plugin "daisyui" {
  themes: dracula --default;
}
```

In above example, we set dracula as the default theme. setting one value like this means only one theme will be available. Unless you add custom themes using [`@plugin "daisyui/theme"`](/docs/themes/#how-to-add-a-new-custom-theme)

## root

| Default value | Type | Description |
| --- | --- | --- |
| `":root"` | string | The CSS selector to receive the CSS variables. |

Example

```
@plugin "daisyui" {
  root: "#my-app";
}
```

In above example, we set the CSS variables on `#my-app` instead of `:root`. This way all daisyUI global CSS variables will be scoped to `#my-app`.  
 This is useful to use daisyUI in a scoped environment like a web component or a shadow DOM or a specific part of the page.

## include

| Default value | Type | Description |
| --- | --- | --- |
|  | comma separated list | List of components to include. |

Example

```
@plugin "daisyui" {
  include: button, input, select;
}
```

In above example, we only include the button, input, and select components. All other styles of daisyUI library will be excluded.  
 [Here are the file names you can include or exclude](https://github.com/saadeghi/daisyui/tree/master/packages/daisyui/src).

## exclude

| Default value | Type | Description |
| --- | --- | --- |
|  | comma separated list | List of components to exclude. |

Example

```
@plugin "daisyui" {
  exclude: rootscrollgutter;
}
```

In above example, we exclude the `rootscrollgutter` style which is added to the `:root` when a modal or drawer is open.

Example

```
@plugin "daisyui" {
  exclude: checkbox, footer, typography, glass, rootcolor, rootscrollgutter;
}
```

In above example, we exclude the the listed files. All other parts of daisyUI will be available to use. This is useful if you want to opt out of some parts of daisyUI or if you want to mix daisyUI for some parts and another library for the rest.  
 [Here are the file names you can include or exclude](https://github.com/saadeghi/daisyui/tree/master/packages/daisyui/src).

## prefix

| Default value | Type | Description |
| --- | --- | --- |
| `""` | string | Prefix for all daisyUI classes. |

Example

```
@plugin "daisyui" {
  prefix: "d-";
}
```

In above example, all daisyUI classes will be prefixed with `d-`. For example, `btn` will be `d-btn`.

#### Using Tailwind CSS prefix AND daisyUI prefix together:

Probably you don't have to do this, but if you need to use both [Tailwind CSS prefix](https://tailwindcss.com/docs/styling-with-utility-classes#using-the-prefix-option) and daisyUI prefix together:

Example

```
@import "tailwindcss" prefix(tw);
@plugin "daisyui" {
  prefix: "d-";
}
```

In above example:

- Tailwind class names will be prefixed with `tw:`, for example `p-4` will be `tw:p-4`.
- All daisyUI classes will be prefixed with `d-`, and `tw:`, for example `btn` will be `tw:d-btn`.
- daisyUI class name [theme-controller](/components/theme-controller/) is an exception and it only gets the daisyUI prefix, like this: `d-theme-controller`.

For example, `btn` will be `tw:d-btn`.

## logs

| Default value | Type | Description |
| --- | --- | --- |
| `true` | boolean | Enable or disable logs. |

Example

```
@plugin "daisyui" {
  logs: false;
}
```

In above example, we disable the logs of daisyUI. This is useful if you want to clean up the console output.

[Prev Customize](/docs/customize/)

[Next Colors](/docs/colors/)

  

Do you have a question? [Ask on GitHub](https://github.com/saadeghi/daisyui/discussions) or [Discord server](https://daisyui.com/discord/)

Do you see a bug? [open an issue on GitHub](https://github.com/saadeghi/daisyui/issues?q=Config)

Do you like daisyUI? [Post about it!](https://x.com/intent/post?text=daisyUI%20%0D%0AComponents%20for%20Tailwind%20CSS%20%0D%0Ahttps://daisyui.com)

Support daisyUI's development: [Open Collective](https://opencollective.com/daisyui)

[Edit this page on GitHub](https://github.com/saadeghi/daisyui/blob/master/packages/docs/src/routes/(routes)/docs/config/+page.md?plain=1)

[Text version for AI prompts](https://raw.githubusercontent.com/saadeghi/daisyui/refs/heads/master/packages/docs/src/routes/(routes)/docs/config/+page.md?plain=1)

![daisyUI store](https://img.daisyui.com/images/store/nexus.webp)

## NEXUS Official daisyUI Dashboard Template

## Available on daisyUI store

[More details](/store/)