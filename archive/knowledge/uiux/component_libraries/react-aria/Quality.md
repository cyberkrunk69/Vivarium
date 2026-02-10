# Quality

Source: https://react-spectrum.adobe.com/react-aria/internationalization.html

---

# Quality

React Aria is built around three core principles: **Accessibility**, **Internationalization**, and **Interactions**. Learn how to apply these tools to build high quality UIs that work for everyone, everywhere, and on every device.

## Accessibility

Accessible applications are usable by everyone, including people with disabilities. Accessibility benefits all users â not just those using assistive technologies â by improving efficiency, consistency, and usability.

React Aria provides built-in support for screen readers and keyboard navigation, following the [WAI-ARIA](https://www.w3.org/TR/wai-aria-1.2/) and [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/) guidelines. It supplies the correct semantics via ARIA roles and attributes, handles keyboard and pointer events, manages focus, and provides screen reader announcements. React Aria components are tested across a wide variety of devices, browsers, and screen readers.

Be sure to create an accessible visual design with meaningful labels, sufficient [color contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast) and [hit target sizes](https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced), visible [focus rings](https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance), and respect [motion preferences](https://www.w3.org/WAI/WCAG21/Understanding/animation-from-interactions). The [WCAG guidelines](https://www.w3.org/WAI/WCAG22/Understanding/) are a good resource to reference when designing and building components with React Aria.

### Labeling

Most components should have a visible label, which is usually provided by rendering a `<Label>` element within it. This is associated with the component automatically.

```
import {TextField, Label, Input} from 'react-aria-components';

<TextField>
  <Label>First name</Label>
  <Input />
</TextField>
```

When a component doesn't have a visible label, it must have an [aria-label](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-label) or [aria-labelledby](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-labelledby) prop to provide an accessible name.

```
import {ProgressBar} from 'react-aria-components';

<ProgressBar
  aria-label="Processing" />
```

### Supported screen readers

React Aria is tested across a variety of devices, browsers, and screen readers.

- [VoiceOver on macOS](https://www.apple.com/accessibility/mac/vision/) in Safari and Chrome
- [JAWS](https://www.freedomscientific.com/products/software/jaws/) on Windows in Firefox and Chrome
- [NVDA](https://www.nvaccess.org) on Windows in Firefox and Chrome
- [VoiceOver on iOS](https://www.apple.com/accessibility/iphone/vision/)
- [TalkBack](https://www.android.com/accessibility/) on Android in Chrome

### Automated testing

Automated accessibility testing tools sometimes catch false positives in React Aria. These are documented in our [wiki](https://github.com/adobe/react-spectrum/wiki/Known-accessibility-false-positives).

## Internationalization

Localization is an important way to make your application usable by the widest number of people. React Aria includes localized strings for 30+ languages, handles dates and numbers in many calendar and numbering systems, and supports right-to-left interactions (e.g. keyboard navigation).

Make sure your design supports right-to-left layout, and adapts to different languages (e.g. using appropriate fonts). Modern CSS grid and flex layouts are automatically mirrored depending on the direction, and [logical properties](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values) can be used to adapt margins, paddings, borders, etc.

### Setting the locale

React Aria automatically detects the user's current language by default. Use the `I18nProvider` component to set the locale to a specific value. You should also set the `lang` and `dir` attributes on the root-most element of your application.

```
import {I18nProvider, useLocale} from 'react-aria-components';

<I18nProvider locale="fr-FR">
  <App />
</I18nProvider>

function App() {
  let {locale, direction} = useLocale();

  return (
    <html lang={locale} dir={direction}>
      {/* your app here */}
    </html>
  );
}
```

### Supported locales

- Arabic (United Arab Emirates) (`ar-AE`)
- Bulgarian (Bulgaria) (`bg-BG`)
- Chinese (Simplified) (`zh-CN`)
- Chinese (Traditional) (`zh-TW`)
- Croatian (Croatia) (`hr-HR`)
- Czech (Czech Republic) (`cs-CZ`)
- Danish (Denmark) (`da-DK`)
- Dutch (Netherlands) (`nl-NL`)
- English (Great Britain) (`en-GB`)
- English (United States) (`en-US`)
- Estonian (Estonia) (`et-EE`)
- Finnish (Finland) (`fi-FI`)
- French (Canada) (`fr-CA`)
- French (France) (`fr-FR`)
- German (Germany) (`de-DE`)
- Greek (Greece) (`el-GR`)
- Hebrew (Israel) (`he-IL`)
- Hungarian (Hungary) (`hu-HU`)
- Italian (Italy) (`it-IT`)
- Japanese (Japan) (`ja-JP`)
- Korean (Korea) (`ko-KR`)
- Latvian (Latvia) (`lv-LV`)
- Lithuanian (Lithuania) (`lt-LT`)
- Norwegian (Norway) (`nb-NO`)
- Polish (Poland) (`pl-PL`)
- Portuguese (Brazil) (`pt-BR`)
- Romanian (Romania) (`ro-RO`)
- Russian (Russia) (`ru-RU`)
- Serbian (Serbia) (`sr-SP`)
- Slovakian (Slovakia) (`sk-SK`)
- Slovenian (Slovenia) (`sl-SI`)
- Spanish (Spain) (`es-ES`)
- Swedish (Sweden) (`sv-SE`)
- Turkish (Turkey) (`tr-TR`)
- Ukrainian (Ukraine) (`uk-UA`)

## Interactions

Modern web apps run on everything from desktops to mobile devices to TVs, with users interacting through mouse, touch, keyboard, and assistive technologies. React Aria normalizes these differences, delivering consistent âpressâ, âhoverâ, and âfocusâ behaviors across all browsers and input types.

React Aria components provide data attributes and render props to style these states:

- `data-pressed` â like the `:active` pseudo class, but removed when the pointer is dragged off.
- `data-hovered` â like `:hover`, but not applied on touch devices, preventing sticky hover states.
- `data-focus-visible` â like `:focus-visible`, but not on input click or programmatic focus.

These states also come with corresponding events such as `onPress` and `onHoverStart`. To use these events in your own custom components, see hooks such as <usePress>, <useHover>, <useMove>, and <useFocusRing>.

Read our blog post series to learn more about the intricacies behind these interactions.

- [Building a Button Part 1: Press Events](blog/building-a-button-part-1)
- [Building a Button Part 2: Hover Interactions](blog/building-a-button-part-2)
- [Building a Button Part 3: Keyboard Focus Behavior](blog/building-a-button-part-3)

Higher level interaction patterns such as <selection> and [drag and drop](dnd) are also built on top of these low level primitives.