# React Aria

Source: https://react-spectrum.adobe.com/react-aria/why.html

---

## Bring your own styles.

React Aria is style-free out of the box, allowing you to build custom designs to fit your application or design system using any styling and animation solution. Each component is broken down into individual parts with built-in states, render props, and slots that make styling a breeze.

[Learn more](styling)

Vanilla CSS

Tailwind

Styled Components

Panda

DatePicker.tsx

DatePicker.css

```
<DatePicker>
  <Label>Date Planted</Label>
  <Group>
    <DateInput>
      {segment => <DateSegment segment={segment} />}
    </DateInput>
    <Button><CalendarIcon /></Button>
  </Group>
  <Popover>
    <Dialog>
      <Calendar>
        <Button slot="previous"><LeftIcon /></Button>
        <Heading />
        <Button slot="next"><RightIcon /></Button>
        <CalendarGrid>
          {date => <CalendarCell date={date} />}
        </CalendarGrid>
      </Calendar>
    </Dialog>
  </Popover>
</DatePicker>
```

DatePicker.css

```
/* Consistent default classes for each component */
.react-aria-DatePicker {
  /* ... */

  .react-aria-Group {
    border: 2px solid var(--gray-300);
  }
}

.react-aria-CalendarCell {
  color: var(--gray-900);

  /* Style interactive states with data attributes */
  &[data-pressed] {
    background: var(--gray-100);
  }

  &[data-selected] {
    color: var(--gray-50);
    background: var(--blue-600);
  }
}
```

https://your-app.com

Date Planted

mm/dd/yyyy

ComboBox.tsx

```
<ComboBox className="group flex ...">
  <Label>Assignee</Label>
  {/* Tailwind plugin for all UI states. */}
  <Group className="... focus-visible:outline-blue-600">
    <Input className="flex-1 ..." />
    <Button className="... pressed:bg-gray-100">
      <ChevronsUpDownIcon />
    </Button>
  </Group>
  {/* Built-in entry and exit animation states. */}
  <Popover className="w-(--trigger-width) ... entering:animate-in entering:fade-in exiting:animate-out exiting:fade-out">
    <ListBox items={people}>
      {item => (
        <ListBoxItem textValue={item.name} className="group text-gray-900 ... focus:bg-blue-600 focus:text-white">
          {/* Use render props to customize children based on state. */}
          {({ isSelected }) => <>
            <img alt="" src={item.avatar} />
            <span className="... font-normal group-selected:font-semibold">{item.name}</span>
            {isSelected &&
              <CheckIcon />
            }
          </>}
        </ListBoxItem>
      )}
    </ListBox>
  </Popover>
</ComboBox>
```

https://your-app.com

Assignee

Slider.tsx

```
const StyledSlider = styled(Slider)`
  display: grid;
  /* ... */
`;

const StyledSliderTrack = styled(SliderTrack)`
  background: var(--gray-300);
`;

const StyledSliderThumb = styled(SliderThumb)`
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--gray-50);
  border: 2px solid var(--gray-600);

  &[data-dragging] {
    background: var(--gray-600);
  }
`;

<StyledSlider defaultValue={30}>
  <Label>Opacity</Label>
  <SliderOutput />
  <StyledSliderTrack>
    <StyledSliderThumb />
  </StyledSliderTrack>
</StyledSlider>
```

https://your-app.com

Opacity30

Button.tsx

```
import {Button} from 'react-aria-components';
import {styled} from '../styled-system/jsx';

const StyledButton = styled(Button, {
  base: {
    /* ... */
  },
  variants: {
    variant: {
      primary: {
        background: 'blue.600',
        '&[data-pressed]': {
          background: 'blue.700',
        }
      },
      secondary: {
        background: 'gray.300',
        '&[data-pressed]': {
          background: 'gray.400',
        }
      }
    }
  }
});

<StyledButton variant="primary">
  Initiate launch sequenceâ¦
</StyledButton>
```

https://your-app.com

Initiate launch sequenceâ¦

## Advanced features for ambitious apps.

Make your web app feel native with rich interactions that adapt to the device, platform, and user. React Aria supports advanced features like accessible drag and drop, keyboard multi-selection, built-in form validation, table column resizing, and a ton more.

[Learn more](dnd)

UI Button Alignment Issue#101Buttons in the Settings menu are misaligned on smaller screens.![](https://images.unsplash.com/photo-1599566150163-29194dcaad36?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1auto=format&fit=facearea&facepad=2&w=256&h=256&q=80)Gilberto Miguelâ¡

Login Page Redesign#102Requesting a redesign of the login page to improve user experience.![](https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80)Maia Pettegreeâ¡

Feature: Dark Mode#104Implement a dark mode option for improved accessibility and user preference.![](https://images.unsplash.com/photo-1569913486515-b74bf7751574?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80)Sarah Leeâ¡

Missing User Profile Pictures#105Some user profile pictures are not displaying properly in the user dashboard.![](https://images.unsplash.com/photo-1528763380143-65b3ac89a3ff?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80)David Chenâ¡

Broken Link on Homepage#107The "Learn More" link on the homepage is leading to a 404 error.![](https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80)Alex Turnerâ¡

Feature: Export to PDF#108Implement a feature to allow users to export their data to PDF format.![](https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80)Maia Pettegreeâ¡

Mobile Responsiveness Issue#109The application is not rendering properly on certain mobile devices.![](https://images.unsplash.com/photo-1500648767791-00dcc994a43e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2.25&w=256&h=256&q=80)Kevin Williamsâ¡

Database Connection Error#103Users are experiencing intermittent connection errors when accessing the database.![](https://images.unsplash.com/photo-1531427186611-ecfd6d936c79?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80)Mike Johnsonâ¡

Feature: Two-Factor Authentication#110Requesting the addition of two-factor authentication for improved security.![](https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80)Maia Pettegreeâ¡

Performance Optimization#106Requesting performance optimization for the application to reduce load times.![](https://images.unsplash.com/photo-1569913486515-b74bf7751574?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80)Sarah Leeâ¡

[View example source](examples/kanban)

## High quality interactions on all devices.

React Aria ensures a great experience for users, no matter their device. All components are optimized for mouse, touch, keyboard, and screen reader interactions, with a meticulous attention to detail that makes your app feel responsive and natural on every platform.

[Learn more](quality#interactions)

### Touch optimized.

Micro-interactions like dragging off to cancel a press, long pressing to select, preventing text selection on interactive elements, scroll locking, and multi-touch handling make your app feel native.

### Mouse enhanced.

Hover interactions only apply when using a mouse â no sticky touch hover states. Mouse features like double click, scroll wheel, tooltips, and cursor feedback enhance your app on desktop.

### Keyboard friendly.

Keyboard interactions are first-class, including arrow key navigation, typeahead, multiple selection modifiers, landmark navigation, and much more.

Chocolate

Mint

Strawberry

Vanilla

### Focus managed.

Focus is automatically contained within overlays, restored on close, and moved when list items are deleted. Focus rings appear only when using the keyboard to help users navigate.

## Accessibility that's truly first-class.

React Aria is designed with accessibility as a top priority, and battle tested in production applications. All components are built to work across a wide variety of devices and assistive technologies to ensure the best experience possible for all users.

[Learn more](quality#accessibility)

7:04 PM

PermissionsRead Only

Read OnlyEditAdmin

### ARIA Semantics.

Components implement semantics and keyboard behavior according to the W3C [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/). React Aria builds on this foundation with real-world testing and device support.

### Mobile ready.

All behaviors work without a keyboard, ensuring touch screen reader users have full access. Additional features such as hidden dismiss buttons in dialogs enable a great experience for mobile users.

### Tested. Like, really.

All components are extensively tested using many popular screen readers and devices. React Aria normalizes differing behavior between browsers and assistive technologies to ensure all users have equal access.

## Ready for an international audience.

React Aria is engineered for internationalization out of the box, including translations in over 30 languages, localized date and number formatting and parsing, support for 13 calendar systems, 5 numbering systems, right-to-left layout, and more.

[Learn more](quality#internationalization)

LocaleEnglish (United States)

Amharic (Ethiopia)Arabic (Algeria)Arabic (Egypt)Arabic (Saudi Arabia)Arabic (United Arab Emirates)Bulgarian (Bulgaria)Chinese (China)Chinese (Taiwan)Croatian (Croatia)Czech (Czechia)Danish (Denmark)Dutch (Netherlands)English (United Kingdom)English (United States)Estonian (Estonia)Finnish (Finland)French (Canada)French (France)German (Germany)Greek (Greece)Hebrew (Israel)Hindi (India)Hungarian (Hungary)Italian (Italy)Japanese (Japan)Korean (South Korea)Latvian (Latvia)Lithuanian (Lithuania)Norwegian BokmÃ¥l (Norway)Persian (Afghanistan)Polish (Poland)Portuguese (Brazil)Romanian (Romania)Russian (Russia)Serbian (SP)Slovak (Slovakia)Slovenian (Slovenia)Spanish (Spain)Swedish (Sweden)Thai (Thailand)Turkish (TÃ¼rkiye)Ukrainian (Ukraine)

CalendarGregorian

GregorianJapaneseBuddhistTaiwanPersianIndianIslamic (Umm al-Qura)Islamic CivilIslamic TabularHebrewCopticEthiopicEthiopic (Amete Alem)

Numbering SystemLatin

LatinArabicHanidecDevanagariBengali

Number FormatDecimal

DecimalPercentCurrencyUnit

## December 2025

| S | M | T | W | T | F | S |
| --- | --- | --- | --- | --- | --- | --- |
| 30 | 1 | 2 | 3 | 4 | 5 | 6 |
| 7 | 8 | 9 | 10 | 11 | 12 | 13 |
| 14 | 15 | 16 | 17 | 18 | 19 | 20 |
| 21 | 22 | 23 | 24 | 25 | 26 | 27 |
| 28 | 29 | 30 | 31 | 1 | 2 | 3 |

Number

Date and Time

12/23/2025, â¦7:04â©â¯PM UTC

## Customizable to the max.

React Aria offers a flexible and scalable API that lets you dive as deep into the details as you like. Start with high-level components with a built-in DOM structure and simple styling API, compose custom patterns with contexts, and for the ultimate control, drop down to the low-level Hook-based API. Mix and match as needed.

[Learn more](customization)

### Reuse styles.

React Aria's API is designed around composition, enabling you to share common components between patterns, or even use them standalone. No need to duplicate styling code.

```
<Select>
  <Label>Permissions</Label>
  <Button>
    <SelectValue />
    <span>â¼</span>
  </Button>
  <Popover>
    <ListBox>
      <ListBoxItem>Read Only</ListBoxItem>
      <ListBoxItem>Edit</ListBoxItem>
      <ListBoxItem>Admin</ListBoxItem>
    </ListBox>
  </Popover>
</Select>
```

```
<Select>
  <Label>
    Permissions
  </Label>
  <Button>
    <SelectValue />
    <span>â¼</span>
  </Button>
  <Popover>
    <ListBox>
      <ListBoxItem>
        Read Only
      </ListBoxItem>
      <ListBoxItem>
        Edit
      </ListBoxItem>
      <ListBoxItem>
        Admin
      </ListBoxItem>
    </ListBox>
  </Popover>
</Select>
```

```
<ComboBox>
  <Label>Permissions</Label>
  <Group>
    <Input />
    <Button>â¼</Button>
  </Group>
  <Popover>
    <ListBox>
      <ListBoxItem>Read Only</ListBoxItem>
      <ListBoxItem>Edit</ListBoxItem>
      <ListBoxItem>Admin</ListBoxItem>
    </ListBox>
  </Popover>
</ComboBox>
```

```
<ComboBox>
  <Label>
    Permissions
  </Label>
  <Group>
    <Input />
    <Button>â¼</Button>
  </Group>
  <Popover>
    <ListBox>
      <ListBoxItem>
        Read Only
      </ListBoxItem>
      <ListBoxItem>
        Edit
      </ListBoxItem>
      <ListBoxItem>
        Admin
      </ListBoxItem>
    </ListBox>
  </Popover>
</ComboBox>
```

### Build custom patterns.

Use the exported contexts for each component to build your own custom patterns with compositional APIs just like React Aria's built-in components.

```
// A Stepper component with customizable buttons.
function Stepper({children}) {
  let [value, setValue] = useState(0);

  return (
    <ButtonContext.Provider value={{
      slots: {
        decrement: {onPress: () => setValue(value - 1)},
        increment: {onPress: () => setValue(value + 1)}
      }
    }}>
      <TextContext.Provider value={{children: value}}>
        {children}
      </TextContext.Provider>
    </ButtonContext.Provider>
  );
}

<Stepper>
  <Button slot="decrement">-</Button>
  <Text />
  <Button slot="increment">+</Button>
</Stepper>
```

### Customize component parts.

React Aria's contexts let you extend components with new features, or even replace individual parts with totally custom implementations.

```
// Add a clear button to a DatePicker.
function DatePickerClearButton() {
  let state = useContext(DatePickerStateContext);

  return (
    <Button
      slot={null}
      aria-label="Clear"
      onPress={() => state.setValue(null)}>
      â
    </Button>
  );
}

<DatePicker>
  <Label>Date</Label>
  <Group>
    <DateInput>
      {segment => <DateSegment segment={segment} />}
    </DateInput>
    <DatePickerClearButton />
    <Button>â¼</Button>
  </Group>
  <Popover>
    <Dialog>
      <Calendar>
        <header>
          <Button slot="previous">â</Button>
          <Heading />
          <Button slot="next">â¶</Button>
        </header>
        <CalendarGrid>
          {date => <CalendarCell date={date} />}
        </CalendarGrid>
      </Calendar>
    </Dialog>
  </Popover>
</DatePicker>
```

### Get complete control with hooks.

Drop down to the low-level Hook-based API to intercept events, override behavior, customize DOM elements, and much more. Mix and match components and hooks as needed.

```
import {useCalendarGrid} from 'react-aria';

// Custom calendar that displays one week at a time.
function WeekCalendarGrid(props) {
  let state = useContext(CalendarStateContext);
  let {gridProps} = useCalendarGrid(props, state);

  return (
    <table {...gridProps}>
      <tbody>
        <tr>
          {state.getDatesInWeek(0).map((date, i) =>
            <CalendarCell key={i} date={date} />
          )}
        </tr>
      </tbody>
    </table>
  );
}

<Calendar visibleDuration={{weeks: 1}}>
  <Button slot="previous">â</Button>
  <WeekCalendarGrid />
  <Button slot="next">â¶</Button>
</Calendar>
```

## Ready to get started?

[### Install and Setup

Learn how to install and setup React Aria in your project, and build and style a component.](getting-started)

### View Components

See an overview of all of the components and hooks offered by React Aria.

### View Components

See an overview of all of the components and hooks offered by React Aria.

[### Explore Examples

Check out some fully styled examples showing what is possible with React Aria.](examples/)