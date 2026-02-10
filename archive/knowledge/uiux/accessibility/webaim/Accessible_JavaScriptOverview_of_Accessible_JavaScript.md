# Accessible JavaScriptOverview of Accessible JavaScript

Source: https://webaim.org/techniques/javascript/

---

# Accessible JavaScript Overview of Accessible JavaScript

You are here: [Home](/) > [Articles](/articles/) > JavaScript

## JavaScript Accessibility Issues

JavaScript allows developers to add increased interaction, information processing, and control in web-based content. However, JavaScript can also introduce accessibility issues. These issues may include:

- **Navigation.** Inability or difficulty navigating using a keyboard or assistive technology.
- **User control.**  Lack of user control over automated content changes.
- **Confusion/Disorientation.** Altering or disabling the normal functionality of the browser or triggering events or content that the user may not be aware of.

A web page containing JavaScript will typically be fully accessible if the functionality of the script is device independent (does not require only a mouse or only a keyboard) and the information (content) is available to assistive technologies. There is no easy fix that can be applied to solve all accessibility problems associated with JavaScript. The only way to ensure JavaScript accessibility is by evaluating each page that utilizes scripting and devising a unique solution to any accessibility problem found.

### JavaScript that does not impact accessibility

Just because JavaScript is used on a page does not mean that the page is inaccessible. In many cases, JavaScript can be used to greatly improve accessibility and optimize the user experience. Some aspects of accessibility compliance would be difficult without JavaScript, especially for complex web applications.

JavaScript is sometimes used to create visual interface elements that do not affect accessibility. As an example, subtle image changes on mouse roll-over or other visual-only modifications may not need additional accessibility features incorporated because important content is not affected by the scripting.

## JavaScript Reliance

People with disabilities will experience scripted content, so it must be made natively accessible. It is a misconception that people with disabilities don't have or enable JavaScript, so it is thus acceptable to present an inaccessible scripted interfaces, so long as there is an accessible, non-JavaScripted version available. A survey by WebAIM of screen reader users found that [99.3% of respondents had JavaScript enabled](/projects/screenreadersurvey8/#javascript). The numbers are even higher for users with [low vision](/projects/lowvisionsurvey/#javascript) or [motor disabilities](projects/motordisabilitysurvey/#javascript).

Accessibility guidelines require scripted interfaces to be accessible. While WCAG 1.0 from 1999 required that pages be functional and accessible with scripting disabled, WCAG 2 and all other modern guidelines allow you to require JavaScript, but the scripted content or interactions must be compliant with the guidelines.

It is important to keep in mind, however, that some users (regardless of disability) do disable JavaScript or may be using technologies that don't fully support scripting, so [alternatives to JavaScript](alternatives) should be provided. If your web page or application requires scripting, consider the impact on users without JavaScript. It is not necessary that all functionality work without scripting (though this would be optimal), but you must avoid presenting something that may appear to function, but does not because of lack of JavaScript support.

[Next](eventhandlers)