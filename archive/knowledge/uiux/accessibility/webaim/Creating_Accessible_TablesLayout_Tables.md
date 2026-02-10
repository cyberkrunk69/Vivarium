# Creating Accessible TablesLayout Tables

Source: https://webaim.org/techniques/tables/

---

# Creating Accessible Tables Layout Tables

You are here: [Home](/) > [Articles](/articles/) > Tables

## Introduction

If you're not a screen reader user, let's pretend that you are for just a moment. You're going to a web site to find out where the biology 205 class is going to be held. You go to a web page that has this information, and this is what you hear:

> Table with 10 columns and 7 rows. Department Code, Class Number, Section, Max Enrollment, Current Enrollment, Room Number, Days, Start Time, End Time, Instructor, BIO, 100, 1, 15, 13, 5, Mon,Wed,Fri, 10:00, 11:00, Magde, 100, 2, 15, 7, 5, Tue,Thu, 11:00, 12:30, Indge, 205, 1, 15, 9, 6, Tue,Thu, 09:00, 10:30, Magde, 315, 1, 12, 3, 6, Mon,Wed,Fri, 13:00, 14:00, Indge, BUS, 150, 1, 15, 15, 13, Mon,Wed,Fri, 09:00, 10:00, Roberts, 210, 1, 10, 9, 13, Mon,Wed,Fri, 08:00, 09:00, Rasid.

After listening to this information, do you have any idea where biology 205 is supposed to be held? Probably not. When you listen to tables straight through, without going into *table reading mode* in a screen reader, this type of information can be quite confusing. Even when you do go into table reading mode, it can still be confusing if the table is not marked up properly.

## Layout Tables vs. Data Tables

There are two basic uses for tables on the web: data tables and layout tables. The original intended use of HTML tables was for *tabular data*. A table is a data table when row headers, column headers, or both are present. For example, here is a simple data table:

Shelly's Daughters

| Name | Age | Birthday |
| Jackie | 5 | April 5 |
| Beth | 8 | January 14 |

Tables are also commonly used for page layout. Layout tables do not have logical headers that can be mapped to information within the table cells. Layout tables were traditionally used to overcome limitations in visual presentation and layout using HTML. With CSS, however, there is much more flexibility in controlling page layout, so it is best to not use tables to do this. Using CSS results in cleaner and more simple HTML code, better end user adaptability, and few potential accessibility issues. Layout tables are also not supposed to be used in HTML5.

It is sometimes suggested, even by some accessibility advocates, that layout tables are bad for accessibility. In reality, layout tables do not pose inherent accessibility issues. There are certainly many worse things that you could do in terms of accessibility. People with all kinds of disabilities can easily access layout tables, as long as the tables are designed with accessibility in mind - ensuring proper linearized reading order, content scaling, etc.

## Layout Table Linearization

Content linearization refers to the order of the content when all formatting is removed. For both data and layout tables, the order in which content is presented can affect its meaning. Many web sites use tables for layout, and most of them use spanned rows and columns to achieve formatting effects. The end result is that the linearized reading order may not be the same as the visual reading order. This can lead to confusion on the part of people who access the linearized reading and navigation order, such as individuals who use screen readers or who navigate with keyboards.

Screen readers essentially ignore the fact that the content is inside of a table. The screen reader just reads the content in the
literal order that it appears in the code. If the literal order of the content in the code is logical, then your linearized reading order is logical.

Important

Screen readers treat layout tables and data tables very differently. For layout tables, they simply read the content of table based on the source code order. For data tables, however, they will identify the presence of the table including number of columns and row, provide table navigation functionality, read row and column headers, etc.

**So how does a screen reader know if a table is a data table or a layout table?** They perform some analysis of the table markup and structure to 'guess'. Because of this, it's vital that data table markup, such as `<caption>`, `<th>`, etc. are *NEVER* used within layout tables, otherwise the screen reader may incorrectly present the table as a data table causing increased overhead and confusion.

Let's take a look at an example in which reading order becomes an issue. Here is a layout table which was created for visual effect:

|  |  |  |  |
| --- | --- | --- | --- |
| Basement |  |  | UP! |
| Toilets | a toilet | Flush |  |
|  | Must |  |  |

The visual user will read: "Basement Toilets Must Flush UP!"

The screen reader will hear (or feel via Braille): "Basement UP! Toilets Flush Must"

Why does this difference exist between the visual order and the screen reader order? To answer this question, we have to look at the table structure. Here is the same table with borders visible and numbers added to each cell to indicate the order in which the screen reader will read them:

|  |  |  |  |
| --- | --- | --- | --- |
| 1 - Basement | 2 | 3 | 4 - UP! |
| 5 - Toilets | 6 - a toilet | 7 - Flush | 8 |
| 9 | 10 - Must | 11 | 12 |

If you view the source code for this table, you'll notice that the source code order matches the order specified above. Tools, such as [WAVE](http://wave.webaim.org/), the Web Developer Toolbar, etc. can help you visually see the linearized reading order of tables.

## Layout Table Sizing

When author's use tables for layout, they are typically doing so to get more precise and (supposedly) flexible control over the positioning of elements within the page. When doing so, layout tables typically define pixel values to attempt to control exact positions. Because there is an immense range of end user browsers and devices, ranging from text-only mobile browsers to large-screen, high definition displays, defining pixel-based sizing is very limiting.

A primary concern of layout tables is their lack of flexibility for accommodating end-user content adjustments, primarily text sizing by users with low vision. If text within a pixel-sized table cell is enlarged by the end user, this can cause readability issues, especially if the text can no longer fit within the pixel dimensions defined. This may result in horizontal scrollbars, text bleeding out of the cell and overlapping other page components, etc. If using layout tables, ensure that the structure of the table allows end user customization and text scaling.

## Use the Simplest Table Configuration Possible

Some designers go crazy with layout tables. They create all kinds of nested tables and unnecessary rows and columns, using spanned rows and columns in every which way, until the table hardly looks like a table at all anymore. All of this may be invisible to sighted users if the table borders are set to zero, but blind users will "see" it all. Their screen readers may inform them of the number of rows and columns in the table. When they try to navigate from one area to the other within the table, they may become disoriented. The rule of thumb here is, the simpler the better.

[Next](data)