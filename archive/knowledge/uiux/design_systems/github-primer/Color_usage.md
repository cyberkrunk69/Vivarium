# Color usage

Source: https://primer.style/foundations/color/base-scales

---

# Color usage

Color is a fundamental part of Primer's visual language. In this guide you will learn about the principles, patterns, and abstractions that make up Primer’s color system.

Looking for Primer's color design tokens? See the [color primitives](/product/primitives/color/) page.

## [Overview](#overview)

![Comparative display of GitHub interface elements in light and dark modes. The light mode shows a browser window with a light background, green contribution graph, and standard browser controls. The dark mode presents the same design with a dark background, enhancing the visibility of green contribution graph and browser controls.](https://github.com/primer/primitives/assets/18661030/615e3e06-9289-4adc-ab85-2213fae96e8c)

GitHub's UI offers two color modes, `light` and `dark`. Primer supports both color modes across nine [themes](/product/primitives/#theming). Every pattern in Primer is built to work across all color modes out of the box.

### [Color modes in Figma](#color-modes-in-figma)

When designing product interfaces in Figma, we recommend using **light mode** or **dark mode** as the Primer Web Figma library provides components and tokens in those two modes.

### [Color design tokens](#color-design-tokens)

Primer delivers colors in the form of [design tokens](/product/primitives/). Design tokens are a layer of abstraction that allows for better maintainability, consistency and theming. Within Primer, design tokens are represented as CSS variables for code and Figma variables for design. For a full reference table of all available design tokens, see the [color CSS variables](/product/primitives/color/) page.

As an example of how color tokens work, when `bgColor-default` is referenced for a background color, the value of that token will automatically change depending on the color mode.

![GitHub Wiki page theming comparison. On the left, a light theme featuring a card with a welcome message, a green 'Create the first page' button, and annotated with 'fgColor-default' for foreground and 'bgColor-default' for background colors. On the right, the same card is shown in dark mode with the text and button colors adjusted for contrast, also annotated with color roles.](https://github.com/primer/react/assets/18661030/21726ed0-2175-44a3-a821-af002778c0b3)

### [Design token categories](#design-token-categories)

Primer design tokens are categorized into three groups:

- Base
- Functional
- Component/pattern

To read more about the naming convention, see the [design token naming guidelines](/product/primitives/token-names/) page.

![Color design guide for GitHub interface elements showing a transition from a base color, a magenta (#bf3989) to a functional color name 'color-scale-pink-5', and then to 'borderColor-sponsors-emphasis'. Below the base color, a color scale from 0 to 9 shows varying shades of pink. Two button examples demonstrate the practical application of the colors: one in a light theme with 'Sponsor' text and heart icon and another in a dark theme with the same elements.](https://github.com/primer/primitives/assets/18661030/10dd4c91-5faa-464c-ab07-9e26afd54e5f)

**Base** color tokens are the lowest level tokens and map directly to a raw value. They are **only** to be used as a reference for functional and component/pattern tokens. Base color tokens don't respect color modes and should never be used directly in code or design.

Example: `color-scale-pink-5`

**Functional** color tokens represent global UI patterns such as text, borders, shadows, and backgrounds. These are the most commonly used design tokens throughout all of Primer and GitHub UI. Functional color tokens reference base color tokens under the hood, and respect color modes.

Example: `borderColor-sponsors-emphasis`

![GitHub interface component patterns displaying color coding for UI elements. On the left, a red border box indicates 'borderColor-danger-emphasis' changing to 'control-borderColor-danger'. On the right, a blue border box signifies 'borderColor-accent-emphasis' transitioning to 'focus-outlineColor'. Examples include text input fields for an email address with error messages and toggle switches in both light and dark themes.](https://github.com/primer/primitives/assets/18661030/4b91c346-24c4-4926-911d-de9d27c851d3)

**Component/pattern** tokens are used for values that are more specific or unique than functional tokens. These tokens are limited and functional tokens are preferred. Component/pattern color tokens may reference both base and functional tokens under the hood, and respect color modes.

Example: `focus-outlineColor`

## [Neutral colors](#neutral-colors)

![Two neutral scales stacked on top of each other labeled from 0 to 11. The top scale is the light scale, which starts with white and ends with black. The bottom scale is the dark scale, which starts with black and ends with white.](https://github.com/user-attachments/assets/34d35d01-3422-465b-bd64-4f7cb2dba0d4)

Primer's neutral scales offer shades of gray between 0 and 13, including white and black. There are two versions of the neutral scale: light, and dark.

The light and dark scale directions are inverted, with the light scale starting with white and the dark scale starting with black. By inverting the scales, light and dark themes are able to share many of the same functional color tokens without custom overrides.

![A split view of how muted text colors reference the same base scale color in both light and dark themes.](https://github.com/user-attachments/assets/7e0de1f9-619b-4378-b6ea-8842392ddffe)

### [Background](#background)

The first six steps of the neutral scales are typically used for background colors. The two most commonly used background colors are `bgColor-default` and `bgColor-muted`. All contrast values for text and borders are calculated against `bgColor-muted` to ensure proper contrast ratios for both `muted` and `default`.

![Two neutral scales stacked on top of each other labelled with background, border, and text to show how the scales are used for different UI elements. In this graphic the background portion is highlighted.](https://github.com/user-attachments/assets/c770498b-50e9-4b28-9e16-d7ae513ba8c1)

For control components with state, the scale accommodates rest, hover, and active.

![A split view showing how neutral scale colors are used for the default button background in both light and dark themes.](https://github.com/user-attachments/assets/d686e7fa-55c9-4c8c-bc02-720b48153d8d)

### [Borders and dividers](#borders-and-dividers)

Steps 7 and 8 are typically used for borders and dividers in the default light/dark themes. Step 8 is considered the minimum contrast value for interactive control borders against `bgColor-muted`.

![Two neutral scales stacked on top of each other labelled with background, border, and text to show how the scales are used for different UI elements. In this graphic the border portion is highlighted.](https://github.com/user-attachments/assets/af8c453c-c3ae-4e7c-9833-c23d988b4cac)

### [Text and icons](#text-and-icons)

Steps 9 and 10 are typically used for text and icons. Step 9 is considered the minimum contrast value for text against steps 0 through 4, while 10 meets the minimum against 5 and 6.

![Two neutral scales stacked on top of each other labelled with background, border, and text to show how the scales are used for different UI elements. In this graphic the text portion is highlighted.](https://github.com/user-attachments/assets/dd0f077a-8e83-44e8-a182-8e8e765a864b)

### [Adjusting contrast](#adjusting-contrast)

Contrast levels can be adjusted by moving up or down the scale. For example, the light high contrast theme utilizes steps 2 through 7 for backgrounds, 10 for borders, and 11 to 13 for text.

For high contrast themes, the goal is to hit a minimum of 7:1 for most text and interactive elements. If a softer background color must be used, make use of borders around elements to increase contrast.

![The light color scale is duplicated and labeled to show how its used for UI elements between light and light high contrast themes.](https://github.com/user-attachments/assets/3f3b24b1-49cf-4b00-af96-dd41dba8a09d)

## [Semantic colors](#semantic-colors)

Semantic colors are typically used to communicate status, action, or emphasis. Each semantic color is tied to a [role](#color-roles) with a specific meaning. Color tokens are available for foreground, background, and border. Background and border colors have both a `muted` and `emphasis` option.

![Overview of GitHub UI color roles in light and dark themes. Each theme displays labeled color swatches for: 'accent-emphasis' in blue, 'accent-muted' in light blue, 'success-emphasis' in green, 'success-muted' in light green, 'danger-emphasis' in red, 'danger-muted' in light red, 'warning-emphasis' in yellow, 'warning-muted' in light yellow, 'done-emphasis' in purple, 'done-muted' in light purple, 'sponsor-emphasis' in magenta, and 'sponsor-muted' in light magenta.](https://github.com/primer/primitives/assets/18661030/165ceeae-9933-473a-976f-655c918be1c2)

### [Muted](#muted)

Muted background and border colors are often combined to draw attention to a specific piece of content with a subtle emphasis.

![GitHub interface elements showing a warning message and a user comment in both light and dark modes. The warning message has a yellow background with a caution icon and is dismissible with a close button. The user comment by 'monalisa' features a speech bubble with a light blue background in light mode and a dark blue background in dark mode, both with muted borders.](https://github.com/primer/react/assets/18661030/df33b03c-ef06-4dc6-9d85-f6dd9cd3f3f0)

### [Emphasis](#emphasis)

Emphasis background colors provide a stronger emphasis for UI elements and are always combined with `fgColor-onEmphasis` tokens for text and icons.

![GitHub interface showcasing button styles with emphasis colors in light and dark modes. The 'Primary' button is green, the 'Danger' button is red with a trash icon, the 'Queued' button is brown with a clock icon, and the 'Beta' button is outlined in green. Annotations indicate 'borderColor-{role}-emphasis' and 'bgColor-{role}-emphasis' for each button style.](https://github.com/primer/react/assets/18661030/3e4ec1f8-cbc5-4ebf-9816-7f247474b9c6)

### [Semantic foreground](#semantic-foreground)

Foreground semantic colors provide contrast against `muted` and default background colors and should be used for text and icons.

![GitHub interface elements displaying in light and dark themes with foreground color roles. Tags include 'Sponsor' with a heart icon, 'Verified' with a checkmark, and language tags 'css' and 'ruby'. The colors of text and icons are adjusted according to the theme for optimal contrast, annotated with 'fgColor-{role}'.](https://github.com/primer/react/assets/18661030/7fcd6efb-ec86-4460-98aa-e3e5be062bec)

## [Base colors](#base-colors)

Base color values should only be used to construct functional and component/pattern design tokens, never used directly
in code

Use the theme menu to see how the base scales change per theme.

Theme: Light[View in Storybook](https://primer.style/primitives/storybook?path=/story/color-base-scales--all-scales&globals=theme%3Alight)

Loading

## [Color roles](#color-roles)

| Color roles | Usage |
| --- | --- |
| `accent` | Links, selected, active, and focus states, and neutral information |
| `success` | Primary buttons, positive messaging and successful states |
| `attention` | Warning states, active processes such as queued PRs and tests in progress |
| `danger` | Danger buttons and error states |
| `open` | Open tasks, PRs or workflows |
| `closed` | Closed tasks, PRs or workflows |
| `done` | Completed tasks, PRs or workflows |
| `sponsors` | Text and icons related to GitHub Sponsors |

## [Developers](#developers)

Colors are available in the form of CSS variables and CSS utility classes that can be used across all frameworks including React and Rails. Check out the [color CSS variables](/product/primitives/color/) for more information.