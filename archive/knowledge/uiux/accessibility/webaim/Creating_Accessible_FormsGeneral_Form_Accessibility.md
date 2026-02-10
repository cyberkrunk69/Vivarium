# Creating Accessible FormsGeneral Form Accessibility

Source: https://webaim.org/techniques/forms/

---

# Creating Accessible Forms General Form Accessibility

You are here: [Home](/) > [Articles](/articles/) > Forms

## Ensure Forms are Logical and Easy to Use

Accessible forms are easy to understand, complete, and submit. Instructions, cues, required form fields, and field formatting requirements must be clearly identified to users. Error recovery must be intuitive and descriptive.

Ensure that reading and navigation order are logical and intuitive. This can be problematic if [layout tables](/techniques/tables/#uses) are employed to create visual "columns." To check the linearized order of items on the page, try navigating your form with just the `Tab` key.

## Ensure Forms are Keyboard Accessible

Users who cannot use a mouse navigate web pages with the keyboard. Forms that use JavaScript to manipulate form data, set focus, change form elements, or submit forms, can create interactions that only work with a mouse. Ensure that your web site forms can be understood and operated with the keyboard alone.

## Associate Form Labels with Controls

A label describes the function of a form control (i.e., text area, checkbox, radio button, menu, etc.), and generally appears adjacent to it. Sighted users make the connection visually, but others cannot. The `<label>` element programmatically associates a text label to a form control, creating a connection in the code that doesn't rely on vision. ARIA labels (`aria-labelledby` and `aria-label`) may be used when it is not possible to use `<label>`. This causes a screen reader to announce the text label when the user navigates to the form control.

Important

Screen reader users navigate using the `Tab` key. Although labels are announced when form inputs received keyboard focus, other text between the form controls is usually skipped. Be sure to include any instructions at the beginning of the form, or associate them with specific fields using [`aria-describedby`](/techniques/forms/advanced#describedby).

Groups of form controls, such as checkboxes and radio buttons, sometimes require a higher-level label (such as "Shipping Method" for a group of shipping options). This information can be associated to the group of form controls using [`<fieldset>` and `<legend>`](/techniques/forms/controls#checkbox). The `<fieldset>` defines the group and the `<legend>` contains the description. Screen readers announce the `<legend>` when users navigate into the group.

The next page provides details on how this markup is properly implemented.

[Next](controls)