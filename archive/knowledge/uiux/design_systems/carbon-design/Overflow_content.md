# Overflow content

Source: https://carbondesignsystem.com/patterns/overflow-content/

---

# Overflow content

Overflow content is text, such as a paragraph or a text string, that exceeds a
desired space. It also applies to a series of components that surpass a given
space. Overflow content is typically reduced to fit a space or reduce
repetition. Truncation and “Show more” buttons are two ways to indicate that
overflow content is continued elsewhere or below the fold.

## Truncation

- [Usage](#usage)
- [Variations](#variations)
- [Code](#code)
- [“Show more” buttons](#"show-more"-buttons)

Truncation, or shortening, is typically used for static text or links that
exceed the size of their container. Truncated items are represented by an
ellipsis

```
...
```

Copy to clipboard

and should represent three or more truncated characters in a text
string. There must be at least four characters of non-truncated content in a
truncated string. Truncated items always include a browser tooltip on hover to
show the entire string, name, or phrase that the ellipsis is representing. The
only time a browser tooltip does not need to be used is at the end of a
truncated paragraph.

![Example of a browser tooltip being used for truncation.](/static/3e4f07809d200d6e7573d160993093d4/3cbba/BrowserTooltip.png)

Example of a browser tooltip being used for truncation.

![Example of end-line truncation for a paragraph.](/static/0d73cf90c445a6c021308d1ef4c487d1/3cbba/Truncated-Paragraph.png)

Example of end-line truncation for a paragraph.

### Usage

Good use cases for truncation include:

- Breadcrumbs
- Pagination
- Long URL links
- Paragraph of text (i.e. a description paragraph)
- Shortening of a long item name (user- or platform-generated)

Truncation should **not** be used on page headers, titles, labels, error
messages, validation messages, or notifications.

### Variations

There are three types of truncation: front-line, mid-line, and end-line.

| Type | Purpose |  | Default | Truncated |
| --- | --- | --- | --- | --- |
| *Front-line* | Used at the beginning of a text string to indicate the text is continued from a previous location. |  | ```  123456789 ```   Copy to clipboard | ```  ...56789 ```   Copy to clipboard |
| *Mid-line* | Used when several text strings have different beginnings and/or endings but the exact same middle characters. Can also be used to shorten a phrase or text string when the end of a string cannot be truncated by an ellipsis. |  | ```  123400005678 ```   Copy to clipboard  ```  987600004321 ```   Copy to clipboard | ```  1234...5678 ```   Copy to clipboard  ```  9876...4321 ```   Copy to clipboard |
| *End-line* | Used at the end of a character string or paragraph to indicate that there is more content in another location, to show that the pattern in a sequence continues, or to shorten a long text string. |  | ```  123456789 ```   Copy to clipboard | ```  12345... ```   Copy to clipboard |

  

#### Ellipses alone

An ellipsis on its own may also represent condensed content. This type of
truncation requires an overflow menu on hover instead of a browser tooltip.

![Example of a truncated Breadcrumb utilizing an ellipse with an Overflow Menu.](/static/764901269621fc83074b8a37c6f806e9/3cbba/Ellipse.png)

Example of a truncated breadcrumb utilizing an ellipsis with an overflow menu.

### Code

To use front- and end-line truncation, enter the appropriate class below and add

```
title
```

Copy to clipboard

to populate the browser tooltip that appears when truncated text is
hovered. The

```
width
```

Copy to clipboard

of the container (or the text element itself) also needs to
be configured in order to calculate where the truncation will start.

| Type | Class |
| --- | --- |
| *Frontline* | ```  .cds--text-truncate--front ```   Copy to clipboard |
| *End-line* | ```  .cds--text-truncate--end ```   Copy to clipboard |

  
 Example Usage 

```
```
<div class="container">

<span title="123456789" class="cds--front-line">123456789</span>

</div>
```

Copy to clipboard
```

```
```
.container {

width: 65px;

}
```

Copy to clipboard
```

```
```
.cds--front-line {

width: 100%;

display: inline-block;

direction: rtl;

text-overflow: ellipsis;

white-space: nowrap;

overflow: hidden;

}
```

Copy to clipboard
```

  
 Result 

![Result.](/static/c2654dd5baadcfb25d0f5dea6bbc17fb/3cbba/1c695894-538c-11e8-8cd2-bb0b1cac151b.png)

  

#### Mid-line truncation

Mid-line truncation does not have its own class as it requires JavaScript.
[This example in CodePen shows how it is implemented](https://codepen.io/team/carbon/pen/KRoBQe/).

  

### “Show more” buttons

The “Show more” button is used when there is a significant amount of overflow
content. Implementing a “Show more” button gives a user the ability to see the
content in more digestible chunks, as opposed to all at once. A “Show more”
button is used in place of scrolling, gradients, or fades as they are more
prominent and actionable. If needed, a “Show less” can be used to again hide the
content the user opened. “Show more” can also be presented as “Load more” in
cases where performance is a concern. See the
[Loading](/components/loading/usage) section for additional details.

![Example of a Code Snippet utilizing the “Show more” Button.](/5eedf92798d12e330f5ed78cf9611e7a/show-more.gif)

![Example of a Code Snippet utilizing the “Show more” Button.](/static/8cd61424de9030252aceff5ac2a26d98/3cbba/show-more.png)

Example of the “Show more” button in context.

[Edit this page on GitHub](https://github.com/carbon-design-system/carbon-website/edit/main/src/pages/patterns/overflow-content/index.mdx)

[Previous

Patterns: Notifications](/patterns/notification-pattern/)

[Next

Patterns: Read-only states](/patterns/read-only-states-pattern/)