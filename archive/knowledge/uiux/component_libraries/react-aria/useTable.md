# useTable

Source: https://react-spectrum.adobe.com/react-aria/useTable.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../Table).

# useTable

Provides the behavior and accessibility implementation for a table component.
A table displays data in rows and columns and enables a user to navigate its contents via directional navigation keys,
and optionally supports row selection and sorting.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useTable, useTableCell, useTableColumnHeader, useTableRow, useTableHeaderRow, useTableRowGroup, useTableSelectAllCheckbox, useTableSelectionCheckbox, useTableColumnResize} from 'react-aria'` |

[View ARIA pattern

W3C](https://www.w3.org/WAI/ARIA/apg/patterns/grid/ "View ARIA pattern")[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/table "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/table "View package")

## API[#](#api)

---

`useTable<T>(
props: AriaTableProps,
state: TableState<T>
|Â  |Â TreeGridState<T>,
ref: RefObject<HTMLElement
|Â  |Â null>
): GridAria`
`useTableRowGroup(): GridRowGroupAria`
`useTableHeaderRow<T>(
props: GridRowProps<T>,
state: TableState<T>,
ref: RefObject<Element
|Â  |Â null>
): TableHeaderRowAria`
`useTableColumnHeader<T>(
props: AriaTableColumnHeaderProps<T>,
state: TableState<T>,
ref: RefObject<FocusableElement
|Â  |Â null>
): TableColumnHeaderAria`
`useTableRow<T>(
props: GridRowProps<T>,
state: TableState<T>
|Â  |Â TreeGridState<T>,
ref: RefObject<FocusableElement
|Â  |Â null>
): GridRowAria`
`useTableCell<T>(
props: AriaTableCellProps,
state: TableState<T>,
ref: RefObject<FocusableElement
|Â  |Â null>
): TableCellAria`
`useTableSelectionCheckbox<T>(
(props: AriaTableSelectionCheckboxProps,
, state: TableState<T>
)): TableSelectionCheckboxAria`
`useTableSelectAllCheckbox<T>(
(state: TableState<T>
)): TableSelectAllCheckboxAria`
`useTableColumnResize<T>(
props: AriaTableColumnResizeProps<T>,
state: TableColumnResizeState<T>,
ref: RefObject<HTMLInputElement
|Â  |Â null>
): TableColumnResizeAria`

## Features[#](#features)

---

A table can be built using the [<table>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/table), [<tr>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/tr),
[<td>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/td), and other table specific HTML elements, but is very limited in functionality especially when it comes to user interactions.
HTML tables are meant for static content, rather than tables with rich interactions like focusable elements within cells, keyboard navigation, row selection, sorting, etc.
`useTable` helps achieve accessible and interactive table components that can be styled as needed.

- Exposed to assistive technology as a `grid` using ARIA
- Keyboard navigation between columns, rows, cells, and in-cell focusable elements via the arrow keys
- Single, multiple, or no row selection via mouse, touch, or keyboard interactions
- Support for disabled rows, which cannot be selected
- Optional support for checkboxes in each row for selection, as well as in the header to select all rows
- Support for both `toggle` and `replace` selection behaviors
- Support for row actions via double click, `Enter` key, or tapping
- Long press to enter selection mode on touch when there is both selection and row actions
- Column sorting support
- Async loading, infinite scrolling, filtering, and sorting support
- Support for column groups via nested columns
- Typeahead to allow focusing rows by typing text
- Automatic scrolling support during keyboard navigation
- Labeling support for accessibility
- Support for marking columns as [row headers](https://www.w3.org/TR/wai-aria-1.1/#rowheader), which will be read when navigating the rows with a screen reader
- Ensures that selections are announced using an ARIA live region
- Support for using HTML table elements, or custom element types (e.g. `<div>`) for layout flexibility
- Support for use with virtualized lists
- Support for resizable columns

## Anatomy[#](#anatomy)

---

A table consists of a container element, with columns and rows of cells containing data inside. The cells within a table may contain focusable elements or plain text content.
If the table supports row selection, each row can optionally include a selection checkbox in the first column. Additionally, a "select all" checkbox is displayed as the first column header if the table supports multiple row selection.

The `useTable`, `useTableRow`, `useTableCell`, and `useTableColumnHeader` hooks handle keyboard, mouse, and other interactions to support
row selection, in table navigation, and overall focus behavior. Those hooks, along with `useTableRowGroup` and `useTableHeaderRow`, also handle exposing the table and its contents
to assistive technology using ARIA. `useTableSelectAllCheckbox` and `useTableSelectionCheckbox` handle row selection and associating each checkbox with its respective rows
for assistive technology. Each of these hooks returns props to be spread onto the appropriate HTML element.

State is managed by the `useTableState`
hook from `@react-stately/table`. The state object should be passed as an option to each of the above hooks where applicable.

Note that an `aria-label` or `aria-labelledby` must be passed to the table to identify the element to assistive technology.

## State management[#](#state-management)

---

`useTable` requires knowledge of the rows, cells, and columns in the table in order to handle keyboard
navigation and other interactions. It does this using
the `Collection`
interface, which is a generic interface to access sequential unique keyed data. You can
implement this interface yourself, e.g. by using a prop to pass a list of item objects,
but `useTableState` from
`@react-stately/table` implements a JSX based interface for building collections instead.
See [Collection Components](https://react-spectrum.adobe.com/v3/collections.html) for more information.

Data is defined using the `TableHeader`, `Column`, `TableBody`, `Row`, and `Cell` components, which support both static and dynamic data.
See the examples in the [usage](#usage) section below for details on how to use these components.

In addition, `useTableState`
manages the state necessary for multiple selection and exposes
a `SelectionManager`,
which makes use of the collection to provide an interface to update the selection state.
For more information, see [Selection](https://react-spectrum.adobe.com/v3/selection.html).

## Example[#](#example)

---

Tables are complex [collection components](https://react-spectrum.adobe.com/v3/collections.html) that are built up from many child elements
including columns, rows, and cells. In this example, we'll use the standard HTML table elements along with hooks from React
Aria for each child. You may also use other elements like `<div>` to render these components as appropriate.
Since there are many pieces, we'll walk through each of them one by one.

The `useTable` hook will be used to render the outer most table element. It uses
the `useTableState` hook to construct the table's collection of rows and columns,
and manage state such as the focused row/cell, selection, and sort column/direction. We'll use the collection to iterate through
the rows and cells of the table and render the relevant components, which we'll define below.

```
import {mergeProps, useFocusRing, useTable} from 'react-aria';
import {Cell, Column, Row, TableBody, TableHeader, useTableState} from 'react-stately';
import {useRef} from 'react';

function Table(props) {
  let { selectionMode, selectionBehavior } = props;
  let state = useTableState({
    ...props,
    showSelectionCheckboxes: selectionMode === 'multiple' &&
      selectionBehavior !== 'replace'
  });

  let ref = useRef<HTMLTableElement | null>(null);
  let { collection } = state;
  let { gridProps } = useTable(props, state, ref);

  return (
    <table {...gridProps} ref={ref} style={{ borderCollapse: 'collapse' }}>
      <TableRowGroup type="thead">
        {collection.headerRows.map((headerRow) => (
          <TableHeaderRow key={headerRow.key} item={headerRow} state={state}>
            {[...headerRow.childNodes].map((column) =>
              column.props.isSelectionCell
                ? (
                  <TableSelectAllCell
                    key={column.key}
                    column={column}
                    state={state}
                  />
                )
                : (
                  <TableColumnHeader
                    key={column.key}
                    column={column}
                    state={state}
                  />
                )
            )}
          </TableHeaderRow>
        ))}
      </TableRowGroup>
      <TableRowGroup type="tbody">
        {[...collection.body.childNodes].map((row) => (
          <TableRow key={row.key} item={row} state={state}>
            {[...row.childNodes].map((cell) =>
              cell.props.isSelectionCell
                ? <TableCheckboxCell key={cell.key} cell={cell} state={state} />
                : <TableCell key={cell.key} cell={cell} state={state} />
            )}
          </TableRow>
        ))}
      </TableRowGroup>
    </table>
  );
}
```

```
import {
  mergeProps,
  useFocusRing,
  useTable
} from 'react-aria';
import {
  Cell,
  Column,
  Row,
  TableBody,
  TableHeader,
  useTableState
} from 'react-stately';
import {useRef} from 'react';

function Table(props) {
  let { selectionMode, selectionBehavior } = props;
  let state = useTableState({
    ...props,
    showSelectionCheckboxes: selectionMode === 'multiple' &&
      selectionBehavior !== 'replace'
  });

  let ref = useRef<HTMLTableElement | null>(null);
  let { collection } = state;
  let { gridProps } = useTable(props, state, ref);

  return (
    <table
      {...gridProps}
      ref={ref}
      style={{ borderCollapse: 'collapse' }}
    >
      <TableRowGroup type="thead">
        {collection.headerRows.map((headerRow) => (
          <TableHeaderRow
            key={headerRow.key}
            item={headerRow}
            state={state}
          >
            {[...headerRow.childNodes].map((column) =>
              column.props.isSelectionCell
                ? (
                  <TableSelectAllCell
                    key={column.key}
                    column={column}
                    state={state}
                  />
                )
                : (
                  <TableColumnHeader
                    key={column.key}
                    column={column}
                    state={state}
                  />
                )
            )}
          </TableHeaderRow>
        ))}
      </TableRowGroup>
      <TableRowGroup type="tbody">
        {[...collection.body.childNodes].map((row) => (
          <TableRow key={row.key} item={row} state={state}>
            {[...row.childNodes].map((cell) =>
              cell.props.isSelectionCell
                ? (
                  <TableCheckboxCell
                    key={cell.key}
                    cell={cell}
                    state={state}
                  />
                )
                : (
                  <TableCell
                    key={cell.key}
                    cell={cell}
                    state={state}
                  />
                )
            )}
          </TableRow>
        ))}
      </TableRowGroup>
    </table>
  );
}
```

```
import {
  mergeProps,
  useFocusRing,
  useTable
} from 'react-aria';
import {
  Cell,
  Column,
  Row,
  TableBody,
  TableHeader,
  useTableState
} from 'react-stately';
import {useRef} from 'react';

function Table(props) {
  let {
    selectionMode,
    selectionBehavior
  } = props;
  let state =
    useTableState({
      ...props,
      showSelectionCheckboxes:
        selectionMode ===
          'multiple' &&
        selectionBehavior !==
          'replace'
    });

  let ref = useRef<
    | HTMLTableElement
    | null
  >(null);
  let { collection } =
    state;
  let { gridProps } =
    useTable(
      props,
      state,
      ref
    );

  return (
    <table
      {...gridProps}
      ref={ref}
      style={{
        borderCollapse:
          'collapse'
      }}
    >
      <TableRowGroup type="thead">
        {collection
          .headerRows
          .map(
            (headerRow) => (
              <TableHeaderRow
                key={headerRow
                  .key}
                item={headerRow}
                state={state}
              >
                {[
                  ...headerRow
                    .childNodes
                ].map(
                  (column) =>
                    column
                        .props
                        .isSelectionCell
                      ? (
                        <TableSelectAllCell
                          key={column
                            .key}
                          column={column}
                          state={state}
                        />
                      )
                      : (
                        <TableColumnHeader
                          key={column
                            .key}
                          column={column}
                          state={state}
                        />
                      )
                )}
              </TableHeaderRow>
            )
          )}
      </TableRowGroup>
      <TableRowGroup type="tbody">
        {[
          ...collection
            .body
            .childNodes
        ].map((row) => (
          <TableRow
            key={row.key}
            item={row}
            state={state}
          >
            {[
              ...row
                .childNodes
            ].map(
              (cell) =>
                cell
                    .props
                    .isSelectionCell
                  ? (
                    <TableCheckboxCell
                      key={cell
                        .key}
                      cell={cell}
                      state={state}
                    />
                  )
                  : (
                    <TableCell
                      key={cell
                        .key}
                      cell={cell}
                      state={state}
                    />
                  )
            )}
          </TableRow>
        ))}
      </TableRowGroup>
    </table>
  );
}
```

### Table header[#](#table-header)

A `useTableRowGroup` hook will be used to group the rows in the table header and table body. In this example,
we're using HTML table elements, so this will be either a `<thead>` or `<tbody>` element, as passed from the
above `Table` component via the `type` prop.

```
import {useTableRowGroup} from 'react-aria';

function TableRowGroup({ type: Element, children }) {
  let { rowGroupProps } = useTableRowGroup();
  return (
    <Element
      {...rowGroupProps}
      style={Element === 'thead'
        ? { borderBottom: '2px solid var(--spectrum-global-color-gray-800)' }
        : null}
    >
      {children}
    </Element>
  );
}
```

```
import {useTableRowGroup} from 'react-aria';

function TableRowGroup({ type: Element, children }) {
  let { rowGroupProps } = useTableRowGroup();
  return (
    <Element
      {...rowGroupProps}
      style={Element === 'thead'
        ? {
          borderBottom:
            '2px solid var(--spectrum-global-color-gray-800)'
        }
        : null}
    >
      {children}
    </Element>
  );
}
```

```
import {useTableRowGroup} from 'react-aria';

function TableRowGroup(
  {
    type: Element,
    children
  }
) {
  let { rowGroupProps } =
    useTableRowGroup();
  return (
    <Element
      {...rowGroupProps}
      style={Element ===
          'thead'
        ? {
          borderBottom:
            '2px solid var(--spectrum-global-color-gray-800)'
        }
        : null}
    >
      {children}
    </Element>
  );
}
```

The `useTableHeaderRow` hook will be used to render a header row. Header rows are similar to other rows,
but they don't support user interaction like selection. In this example, there's only one header
row, but there could be multiple in the case of nested columns. See the [example below](#nested-columns) for details.

```
import {useTableHeaderRow} from 'react-aria';

function TableHeaderRow({ item, state, children }) {
  let ref = useRef<HTMLTableRowElement | null>(null);
  let { rowProps } = useTableHeaderRow({ node: item }, state, ref);

  return (
    <tr {...rowProps} ref={ref}>
      {children}
    </tr>
  );
}
```

```
import {useTableHeaderRow} from 'react-aria';

function TableHeaderRow({ item, state, children }) {
  let ref = useRef<HTMLTableRowElement | null>(null);
  let { rowProps } = useTableHeaderRow(
    { node: item },
    state,
    ref
  );

  return (
    <tr {...rowProps} ref={ref}>
      {children}
    </tr>
  );
}
```

```
import {useTableHeaderRow} from 'react-aria';

function TableHeaderRow(
  {
    item,
    state,
    children
  }
) {
  let ref = useRef<
    | HTMLTableRowElement
    | null
  >(null);
  let { rowProps } =
    useTableHeaderRow(
      { node: item },
      state,
      ref
    );

  return (
    <tr
      {...rowProps}
      ref={ref}
    >
      {children}
    </tr>
  );
}
```

The `useTableColumnHeader` hook will be used to render each column header. Column headers act as a label
for all of the cells in that column, and can optionally support user interaction to sort by the column
and change the sort order.

The `allowsSorting` property of the column object can be used to determine
if the column supports sorting at all.

The `sortDescriptor` object stored in the `state` object indicates which column the table is currently sorted by,
as well as the sort direction (ascending or descending). This is used to render an arrow icon to visually
indicate the sort direction. When not sorted by this column, we use `visibility: hidden` to ensure that
we reserve space for this icon at all times. That way the table's layout doesn't shift when we change the
column we're sorting by. See the [example below](#sorting) of all of this in action.

Finally, we use the `useFocusRing` hook to ensure that a focus ring is rendered when
the cell is navigated to with the keyboard.

```
import {useTableColumnHeader} from 'react-aria';

function TableColumnHeader({ column, state }) {
  let ref = useRef<HTMLTableCellElement | null>(null);
  let { columnHeaderProps } = useTableColumnHeader(
    { node: column },
    state,
    ref
  );
  let { isFocusVisible, focusProps } = useFocusRing();
  let arrowIcon = state.sortDescriptor?.direction === 'ascending' ? 'â²' : 'â¼';

  return (
    <th
      {...mergeProps(columnHeaderProps, focusProps)}
      style={{
        textAlign: column.colSpan > 1 ? 'center' : 'left',
        padding: '5px 10px',
        outline: 'none',
        boxShadow: isFocusVisible ? 'inset 0 0 0 2px orange' : 'none',
        cursor: 'default'
      }}
      ref={ref}
    >
      {column.rendered}
      {column.props.allowsSorting &&
        (
          <span
            aria-hidden="true"
            style={{
              padding: '0 2px',
              visibility: state.sortDescriptor?.column === column.key
                ? 'visible'
                : 'hidden'
            }}
          >
            {arrowIcon}
          </span>
        )}
    </th>
  );
}
```

```
import {useTableColumnHeader} from 'react-aria';

function TableColumnHeader({ column, state }) {
  let ref = useRef<HTMLTableCellElement | null>(null);
  let { columnHeaderProps } = useTableColumnHeader(
    { node: column },
    state,
    ref
  );
  let { isFocusVisible, focusProps } = useFocusRing();
  let arrowIcon =
    state.sortDescriptor?.direction === 'ascending'
      ? 'â²'
      : 'â¼';

  return (
    <th
      {...mergeProps(columnHeaderProps, focusProps)}
      style={{
        textAlign: column.colSpan > 1 ? 'center' : 'left',
        padding: '5px 10px',
        outline: 'none',
        boxShadow: isFocusVisible
          ? 'inset 0 0 0 2px orange'
          : 'none',
        cursor: 'default'
      }}
      ref={ref}
    >
      {column.rendered}
      {column.props.allowsSorting &&
        (
          <span
            aria-hidden="true"
            style={{
              padding: '0 2px',
              visibility:
                state.sortDescriptor?.column === column.key
                  ? 'visible'
                  : 'hidden'
            }}
          >
            {arrowIcon}
          </span>
        )}
    </th>
  );
}
```

```
import {useTableColumnHeader} from 'react-aria';

function TableColumnHeader(
  { column, state }
) {
  let ref = useRef<
    | HTMLTableCellElement
    | null
  >(null);
  let {
    columnHeaderProps
  } =
    useTableColumnHeader(
      { node: column },
      state,
      ref
    );
  let {
    isFocusVisible,
    focusProps
  } = useFocusRing();
  let arrowIcon =
    state.sortDescriptor
        ?.direction ===
        'ascending'
      ? 'â²'
      : 'â¼';

  return (
    <th
      {...mergeProps(
        columnHeaderProps,
        focusProps
      )}
      style={{
        textAlign:
          column
              .colSpan >
              1
            ? 'center'
            : 'left',
        padding:
          '5px 10px',
        outline: 'none',
        boxShadow:
          isFocusVisible
            ? 'inset 0 0 0 2px orange'
            : 'none',
        cursor: 'default'
      }}
      ref={ref}
    >
      {column.rendered}
      {column.props
        .allowsSorting &&
        (
          <span
            aria-hidden="true"
            style={{
              padding:
                '0 2px',
              visibility:
                state
                    .sortDescriptor
                    ?.column ===
                    column
                      .key
                  ? 'visible'
                  : 'hidden'
            }}
          >
            {arrowIcon}
          </span>
        )}
    </th>
  );
}
```

### Table body[#](#table-body)

Now that we've covered the table header, let's move on to the body. We'll use
the `useTableRow` hook to render each row in the table.
Table rows can be focused and navigated to using the keyboard via the arrow keys. In addition, table rows
can optionally support selection via mouse, touch, or keyboard. Clicking, tapping, or pressing the `Space`
key anywhere in the row selects it. Row actions are also supported, see [below](#row-actions) for details.

We'll use the `SelectionManager` object exposed
by the `state` to determine if a row is selected, and render a pink background if so. We'll also use the `useFocusRing`
hook to render a focus ring when the user navigates to the row with the keyboard.

```
import {useTableRow} from 'react-aria';

function TableRow({ item, children, state }) {
  let ref = useRef<HTMLTableRowElement | null>(null);
  let isSelected = state.selectionManager.isSelected(item.key);
  let { rowProps, isPressed } = useTableRow(
    {
      node: item
    },
    state,
    ref
  );
  let { isFocusVisible, focusProps } = useFocusRing();

  return (
    <tr
      style={{
        background: isSelected
          ? 'blueviolet'
          : isPressed
          ? 'var(--spectrum-global-color-gray-400)'
          : item.index % 2
          ? 'var(--spectrum-alias-highlight-hover)'
          : 'none',
        color: isSelected ? 'white' : null,
        outline: 'none',
        boxShadow: isFocusVisible ? 'inset 0 0 0 2px orange' : 'none',
        cursor: 'default'
      }}
      {...mergeProps(rowProps, focusProps)}
      ref={ref}
    >
      {children}
    </tr>
  );
}
```

```
import {useTableRow} from 'react-aria';

function TableRow({ item, children, state }) {
  let ref = useRef<HTMLTableRowElement | null>(null);
  let isSelected = state.selectionManager.isSelected(
    item.key
  );
  let { rowProps, isPressed } = useTableRow(
    {
      node: item
    },
    state,
    ref
  );
  let { isFocusVisible, focusProps } = useFocusRing();

  return (
    <tr
      style={{
        background: isSelected
          ? 'blueviolet'
          : isPressed
          ? 'var(--spectrum-global-color-gray-400)'
          : item.index % 2
          ? 'var(--spectrum-alias-highlight-hover)'
          : 'none',
        color: isSelected ? 'white' : null,
        outline: 'none',
        boxShadow: isFocusVisible
          ? 'inset 0 0 0 2px orange'
          : 'none',
        cursor: 'default'
      }}
      {...mergeProps(rowProps, focusProps)}
      ref={ref}
    >
      {children}
    </tr>
  );
}
```

```
import {useTableRow} from 'react-aria';

function TableRow(
  {
    item,
    children,
    state
  }
) {
  let ref = useRef<
    | HTMLTableRowElement
    | null
  >(null);
  let isSelected = state
    .selectionManager
    .isSelected(
      item.key
    );
  let {
    rowProps,
    isPressed
  } = useTableRow(
    {
      node: item
    },
    state,
    ref
  );
  let {
    isFocusVisible,
    focusProps
  } = useFocusRing();

  return (
    <tr
      style={{
        background:
          isSelected
            ? 'blueviolet'
            : isPressed
            ? 'var(--spectrum-global-color-gray-400)'
            : item
                .index %
                2
            ? 'var(--spectrum-alias-highlight-hover)'
            : 'none',
        color: isSelected
          ? 'white'
          : null,
        outline: 'none',
        boxShadow:
          isFocusVisible
            ? 'inset 0 0 0 2px orange'
            : 'none',
        cursor: 'default'
      }}
      {...mergeProps(
        rowProps,
        focusProps
      )}
      ref={ref}
    >
      {children}
    </tr>
  );
}
```

Finally, we'll use the `useTableCell` hook to render each cell.
Users can use the left and right arrow keys to navigate to each cell in a row, as well as any focusable elements
within a cell. This is indicated by the focus ring, as created with the `useFocusRing`
hook. The cell's contents are available in the `rendered` property of the cell `Node`
object.

```
import {useTableCell} from 'react-aria';

function TableCell({ cell, state }) {
  let ref = useRef<HTMLTableCellElement | null>(null);
  let { gridCellProps } = useTableCell({ node: cell }, state, ref);
  let { isFocusVisible, focusProps } = useFocusRing();

  return (
    <td
      {...mergeProps(gridCellProps, focusProps)}
      style={{
        padding: '5px 10px',
        outline: 'none',
        boxShadow: isFocusVisible ? 'inset 0 0 0 2px orange' : 'none'
      }}
      ref={ref}
    >
      {cell.rendered}
    </td>
  );
}
```

```
import {useTableCell} from 'react-aria';

function TableCell({ cell, state }) {
  let ref = useRef<HTMLTableCellElement | null>(null);
  let { gridCellProps } = useTableCell(
    { node: cell },
    state,
    ref
  );
  let { isFocusVisible, focusProps } = useFocusRing();

  return (
    <td
      {...mergeProps(gridCellProps, focusProps)}
      style={{
        padding: '5px 10px',
        outline: 'none',
        boxShadow: isFocusVisible
          ? 'inset 0 0 0 2px orange'
          : 'none'
      }}
      ref={ref}
    >
      {cell.rendered}
    </td>
  );
}
```

```
import {useTableCell} from 'react-aria';

function TableCell(
  { cell, state }
) {
  let ref = useRef<
    | HTMLTableCellElement
    | null
  >(null);
  let { gridCellProps } =
    useTableCell(
      { node: cell },
      state,
      ref
    );
  let {
    isFocusVisible,
    focusProps
  } = useFocusRing();

  return (
    <td
      {...mergeProps(
        gridCellProps,
        focusProps
      )}
      style={{
        padding:
          '5px 10px',
        outline: 'none',
        boxShadow:
          isFocusVisible
            ? 'inset 0 0 0 2px orange'
            : 'none'
      }}
      ref={ref}
    >
      {cell.rendered}
    </td>
  );
}
```

With all of the above components in place, we can render an example of our Table in action.
This example shows a static collection, where all of the data is hard coded. [See below](#dynamic-collections)
for examples of using this Table component with dynamic collections (e.g. from a server).

Try tabbing into the table and navigating using the arrow keys.

```
<Table
  aria-label="Example static collection table"
  style={{ height: '210px', maxWidth: '400px' }}
>
  <TableHeader>
    <Column>Name</Column>
    <Column>Type</Column>
    <Column>Date Modified</Column>
  </TableHeader>
  <TableBody>
    <Row>
      <Cell>Games</Cell>
      <Cell>File folder</Cell>
      <Cell>6/7/2020</Cell>
    </Row>
    <Row>
      <Cell>Program Files</Cell>
      <Cell>File folder</Cell>
      <Cell>4/7/2021</Cell>
    </Row>
    <Row>
      <Cell>bootmgr</Cell>
      <Cell>System file</Cell>
      <Cell>11/20/2010</Cell>
    </Row>
    <Row>
      <Cell>log.txt</Cell>
      <Cell>Text Document</Cell>
      <Cell>1/18/2016</Cell>
    </Row>
  </TableBody>
</Table>
```

```
<Table
  aria-label="Example static collection table"
  style={{ height: '210px', maxWidth: '400px' }}
>
  <TableHeader>
    <Column>Name</Column>
    <Column>Type</Column>
    <Column>Date Modified</Column>
  </TableHeader>
  <TableBody>
    <Row>
      <Cell>Games</Cell>
      <Cell>File folder</Cell>
      <Cell>6/7/2020</Cell>
    </Row>
    <Row>
      <Cell>Program Files</Cell>
      <Cell>File folder</Cell>
      <Cell>4/7/2021</Cell>
    </Row>
    <Row>
      <Cell>bootmgr</Cell>
      <Cell>System file</Cell>
      <Cell>11/20/2010</Cell>
    </Row>
    <Row>
      <Cell>log.txt</Cell>
      <Cell>Text Document</Cell>
      <Cell>1/18/2016</Cell>
    </Row>
  </TableBody>
</Table>
```

```
<Table
  aria-label="Example static collection table"
  style={{
    height: '210px',
    maxWidth: '400px'
  }}
>
  <TableHeader>
    <Column>
      Name
    </Column>
    <Column>
      Type
    </Column>
    <Column>
      Date Modified
    </Column>
  </TableHeader>
  <TableBody>
    <Row>
      <Cell>
        Games
      </Cell>
      <Cell>
        File folder
      </Cell>
      <Cell>
        6/7/2020
      </Cell>
    </Row>
    <Row>
      <Cell>
        Program Files
      </Cell>
      <Cell>
        File folder
      </Cell>
      <Cell>
        4/7/2021
      </Cell>
    </Row>
    <Row>
      <Cell>
        bootmgr
      </Cell>
      <Cell>
        System file
      </Cell>
      <Cell>
        11/20/2010
      </Cell>
    </Row>
    <Row>
      <Cell>
        log.txt
      </Cell>
      <Cell>
        Text Document
      </Cell>
      <Cell>
        1/18/2016
      </Cell>
    </Row>
  </TableBody>
</Table>
```

### Adding selection[#](#adding-selection)

Next, let's add support for selection. For multiple selection, we'll want to add a column of checkboxes to the left
of the table to allow the user to select rows. This is done using the `useTableSelectionCheckbox`
hook. It is passed the `parentKey` of the cell, which refers to the row the cell is contained within. When the user
checks or unchecks the checkbox, the row will be added or removed from the Table's selection.

The `Checkbox` component used in this example is independent and can be used separately from `Table`. The code is
available below. See [useCheckbox](../Checkbox/useCheckbox.html) for documentation.

```
import {useTableSelectionCheckbox} from 'react-aria';

// Reuse the Checkbox from your component library. See below for details.
import {Checkbox} from 'your-component-library';

function TableCheckboxCell({ cell, state }) {
  let ref = useRef<HTMLTableCellElement | null>(null);
  let { gridCellProps } = useTableCell({ node: cell }, state, ref);
  let { checkboxProps } = useTableSelectionCheckbox(
    { key: cell.parentKey },
    state
  );

  return (
    <td
      {...gridCellProps}
      ref={ref}
    >
      <Checkbox {...checkboxProps} />
    </td>
  );
}
```

```
import {useTableSelectionCheckbox} from 'react-aria';

// Reuse the Checkbox from your component library. See below for details.
import {Checkbox} from 'your-component-library';

function TableCheckboxCell({ cell, state }) {
  let ref = useRef<HTMLTableCellElement | null>(null);
  let { gridCellProps } = useTableCell(
    { node: cell },
    state,
    ref
  );
  let { checkboxProps } = useTableSelectionCheckbox({
    key: cell.parentKey
  }, state);

  return (
    <td
      {...gridCellProps}
      ref={ref}
    >
      <Checkbox {...checkboxProps} />
    </td>
  );
}
```

```
import {useTableSelectionCheckbox} from 'react-aria';

// Reuse the Checkbox from your component library. See below for details.
import {Checkbox} from 'your-component-library';

function TableCheckboxCell(
  { cell, state }
) {
  let ref = useRef<
    | HTMLTableCellElement
    | null
  >(null);
  let { gridCellProps } =
    useTableCell(
      { node: cell },
      state,
      ref
    );
  let { checkboxProps } =
    useTableSelectionCheckbox(
      {
        key:
          cell.parentKey
      },
      state
    );

  return (
    <td
      {...gridCellProps}
      ref={ref}
    >
      <Checkbox
        {...checkboxProps}
      />
    </td>
  );
}
```

We also want the user to be able to select all rows in the table at once. This is possible using the `â Cmd` + `A`
keyboard shortcut, but we'll also add a checkbox into the table header to do this and represent the selection state visually.
This is done using the `useTableSelectAllCheckbox` hook. When all rows are selected,
the checkbox will be shown as checked, and when only some rows are selected, the checkbox will be rendered in an indeterminate state.
The user can check or uncheck the checkbox to select all or clear the selection, respectively.

**Note**: Always ensure that the cell has accessible content, even when the checkbox is hidden (i.e. in single selection mode). The
[VisuallyHidden](../VisuallyHidden) component can be used to do this.

```
import {useTableSelectAllCheckbox, VisuallyHidden} from 'react-aria';

function TableSelectAllCell({ column, state }) {
  let ref = useRef<HTMLTableCellElement | null>(null);
  let { columnHeaderProps } = useTableColumnHeader(
    { node: column },
    state,
    ref
  );
  let { checkboxProps } = useTableSelectAllCheckbox(state);

  return (
    <th
      {...columnHeaderProps}
      ref={ref}
    >
      {state.selectionManager.selectionMode === 'single'
        ? <VisuallyHidden>{checkboxProps['aria-label']}</VisuallyHidden>
        : <Checkbox {...checkboxProps} />}
    </th>
  );
}
```

```
import {
  useTableSelectAllCheckbox,
  VisuallyHidden
} from 'react-aria';

function TableSelectAllCell({ column, state }) {
  let ref = useRef<HTMLTableCellElement | null>(null);
  let { columnHeaderProps } = useTableColumnHeader(
    { node: column },
    state,
    ref
  );
  let { checkboxProps } = useTableSelectAllCheckbox(state);

  return (
    <th
      {...columnHeaderProps}
      ref={ref}
    >
      {state.selectionManager.selectionMode === 'single'
        ? (
          <VisuallyHidden>
            {checkboxProps['aria-label']}
          </VisuallyHidden>
        )
        : <Checkbox {...checkboxProps} />}
    </th>
  );
}
```

```
import {
  useTableSelectAllCheckbox,
  VisuallyHidden
} from 'react-aria';

function TableSelectAllCell(
  { column, state }
) {
  let ref = useRef<
    | HTMLTableCellElement
    | null
  >(null);
  let {
    columnHeaderProps
  } =
    useTableColumnHeader(
      { node: column },
      state,
      ref
    );
  let { checkboxProps } =
    useTableSelectAllCheckbox(
      state
    );

  return (
    <th
      {...columnHeaderProps}
      ref={ref}
    >
      {state
          .selectionManager
          .selectionMode ===
          'single'
        ? (
          <VisuallyHidden>
            {checkboxProps[
              'aria-label'
            ]}
          </VisuallyHidden>
        )
        : (
          <Checkbox
            {...checkboxProps}
          />
        )}
    </th>
  );
}
```

The following example shows how to enable multiple selection support using the Table component we built above.
It's as simple as setting the `selectionMode` prop to `"multiple"`. Because we set the `showSelectionCheckboxes`
option of `useTableState` to true when multiple selection is enabled, an extra column for these checkboxes is
automatically added for us.

And that's it! We now have a fully interactive table component that can support keyboard navigation, single or multiple selection,
as well as column sorting. In addition, it is fully accessible for screen readers and other assistive technology. See below for more
examples of how to use the Table component that we've built.

```
<Table aria-label="Table with selection" selectionMode="multiple">
  <TableHeader>
    <Column>Name</Column>
    <Column>Type</Column>
    <Column>Level</Column>
  </TableHeader>
  <TableBody>
    <Row key="1">
      <Cell>Charizard</Cell>
      <Cell>Fire, Flying</Cell>
      <Cell>67</Cell>
    </Row>
    <Row key="2">
      <Cell>Blastoise</Cell>
      <Cell>Water</Cell>
      <Cell>56</Cell>
    </Row>
    <Row key="3">
      <Cell>Venusaur</Cell>
      <Cell>Grass, Poison</Cell>
      <Cell>83</Cell>
    </Row>
    <Row key="4">
      <Cell>Pikachu</Cell>
      <Cell>Electric</Cell>
      <Cell>100</Cell>
    </Row>
  </TableBody>
</Table>
```

```
<Table
  aria-label="Table with selection"
  selectionMode="multiple"
>
  <TableHeader>
    <Column>Name</Column>
    <Column>Type</Column>
    <Column>Level</Column>
  </TableHeader>
  <TableBody>
    <Row key="1">
      <Cell>Charizard</Cell>
      <Cell>Fire, Flying</Cell>
      <Cell>67</Cell>
    </Row>
    <Row key="2">
      <Cell>Blastoise</Cell>
      <Cell>Water</Cell>
      <Cell>56</Cell>
    </Row>
    <Row key="3">
      <Cell>Venusaur</Cell>
      <Cell>Grass, Poison</Cell>
      <Cell>83</Cell>
    </Row>
    <Row key="4">
      <Cell>Pikachu</Cell>
      <Cell>Electric</Cell>
      <Cell>100</Cell>
    </Row>
  </TableBody>
</Table>
```

```
<Table
  aria-label="Table with selection"
  selectionMode="multiple"
>
  <TableHeader>
    <Column>
      Name
    </Column>
    <Column>
      Type
    </Column>
    <Column>
      Level
    </Column>
  </TableHeader>
  <TableBody>
    <Row key="1">
      <Cell>
        Charizard
      </Cell>
      <Cell>
        Fire, Flying
      </Cell>
      <Cell>67</Cell>
    </Row>
    <Row key="2">
      <Cell>
        Blastoise
      </Cell>
      <Cell>
        Water
      </Cell>
      <Cell>56</Cell>
    </Row>
    <Row key="3">
      <Cell>
        Venusaur
      </Cell>
      <Cell>
        Grass, Poison
      </Cell>
      <Cell>83</Cell>
    </Row>
    <Row key="4">
      <Cell>
        Pikachu
      </Cell>
      <Cell>
        Electric
      </Cell>
      <Cell>100</Cell>
    </Row>
  </TableBody>
</Table>
```

### Checkbox[#](#checkbox)

The `Checkbox` component used in the above example is used to implement row selection. It is built using the [useCheckbox](../Checkbox/useCheckbox.html)
hook, and can be shared with many other components.

 Show code

```
import {useCheckbox} from 'react-aria';
import {useToggleState} from 'react-stately';

function Checkbox(props) {
  let ref = React.useRef<HTMLInputElement | null>(null);
  let state = useToggleState(props);
  let { inputProps } = useCheckbox(props, state, ref);
  return <input {...inputProps} ref={ref} style={props.style} />;
}
```

```
import {useCheckbox} from 'react-aria';
import {useToggleState} from 'react-stately';

function Checkbox(props) {
  let ref = React.useRef<HTMLInputElement | null>(null);
  let state = useToggleState(props);
  let { inputProps } = useCheckbox(props, state, ref);
  return (
    <input {...inputProps} ref={ref} style={props.style} />
  );
}
```

```
import {useCheckbox} from 'react-aria';
import {useToggleState} from 'react-stately';

function Checkbox(
  props
) {
  let ref = React.useRef<
    | HTMLInputElement
    | null
  >(null);
  let state =
    useToggleState(
      props
    );
  let { inputProps } =
    useCheckbox(
      props,
      state,
      ref
    );
  return (
    <input
      {...inputProps}
      ref={ref}
      style={props.style}
    />
  );
}
```

## Usage[#](#usage)

---

### Dynamic collections[#](#dynamic-collections)

So far, our examples have shown static collections, where the data is hard coded.
Dynamic collections, as shown below, can be used when the table data comes from an external data source such as an API, or updates over time.
In the example below, both the columns and the rows are provided to the table via a render function. You can also make the columns static and
only the rows dynamic.

```
function ExampleTable(props) {
  let columns = [
    {name: 'Name', key: 'name'},
    {name: 'Type', key: 'type'},
    {name: 'Date Modified', key: 'date'}
  ];

  let rows = [
    {id: 1, name: 'Games', date: '6/7/2020', type: 'File folder'},
    {id: 2, name: 'Program Files', date: '4/7/2021', type: 'File folder'},
    {id: 3, name: 'bootmgr', date: '11/20/2010', type: 'System file'},
    {id: 4, name: 'log.txt', date: '1/18/2016', type: 'Text Document'}
  ];

  return (
    <Table aria-label="Example dynamic collection table" {...props}>
      <TableHeader columns={columns}>
        {column => (
          <Column>
            {column.name}
          </Column>
        )}
      </TableHeader>
      <TableBody items={rows}>
        {item => (
          <Row>
            {columnKey => <Cell>{item[columnKey]}</Cell>}
          </Row>
        )}
      </TableBody>
    </Table>
  );
}
```

```
function ExampleTable(props) {
  let columns = [
    { name: 'Name', key: 'name' },
    { name: 'Type', key: 'type' },
    { name: 'Date Modified', key: 'date' }
  ];

  let rows = [
    {
      id: 1,
      name: 'Games',
      date: '6/7/2020',
      type: 'File folder'
    },
    {
      id: 2,
      name: 'Program Files',
      date: '4/7/2021',
      type: 'File folder'
    },
    {
      id: 3,
      name: 'bootmgr',
      date: '11/20/2010',
      type: 'System file'
    },
    {
      id: 4,
      name: 'log.txt',
      date: '1/18/2016',
      type: 'Text Document'
    }
  ];

  return (
    <Table
      aria-label="Example dynamic collection table"
      {...props}
    >
      <TableHeader columns={columns}>
        {(column) => (
          <Column>
            {column.name}
          </Column>
        )}
      </TableHeader>
      <TableBody items={rows}>
        {(item) => (
          <Row>
            {(columnKey) => <Cell>{item[columnKey]}</Cell>}
          </Row>
        )}
      </TableBody>
    </Table>
  );
}
```

```
function ExampleTable(
  props
) {
  let columns = [
    {
      name: 'Name',
      key: 'name'
    },
    {
      name: 'Type',
      key: 'type'
    },
    {
      name:
        'Date Modified',
      key: 'date'
    }
  ];

  let rows = [
    {
      id: 1,
      name: 'Games',
      date: '6/7/2020',
      type: 'File folder'
    },
    {
      id: 2,
      name:
        'Program Files',
      date: '4/7/2021',
      type: 'File folder'
    },
    {
      id: 3,
      name: 'bootmgr',
      date: '11/20/2010',
      type: 'System file'
    },
    {
      id: 4,
      name: 'log.txt',
      date: '1/18/2016',
      type:
        'Text Document'
    }
  ];

  return (
    <Table
      aria-label="Example dynamic collection table"
      {...props}
    >
      <TableHeader
        columns={columns}
      >
        {(column) => (
          <Column>
            {column.name}
          </Column>
        )}
      </TableHeader>
      <TableBody
        items={rows}
      >
        {(item) => (
          <Row>
            {(columnKey) => (
              <Cell>
                {item[
                  columnKey
                ]}
              </Cell>
            )}
          </Row>
        )}
      </TableBody>
    </Table>
  );
}
```

### Single selection[#](#single-selection)

By default, `useTableState` doesn't allow row selection but this can be enabled using the `selectionMode` prop. Use `defaultSelectedKeys` to provide a default set of selected rows.
Note that the value of the selected keys must match the `key` prop of the row.

The example below enables single selection mode, and uses `defaultSelectedKeys` to select the row with key equal to "2".
A user can click on a different row to change the selection, or click on the same row again to deselect it entirely.

```
// Using the example above
<ExampleTable selectionMode="single" defaultSelectedKeys={[2]} />
```

```
// Using the example above
<ExampleTable
  selectionMode="single"
  defaultSelectedKeys={[2]}
/>
```

```
// Using the example above
<ExampleTable
  selectionMode="single"
  defaultSelectedKeys={[
    2
  ]}
/>
```

### Multiple selection[#](#multiple-selection)

Multiple selection can be enabled by setting `selectionMode` to `multiple`.

```
// Using the example above
<ExampleTable selectionMode="multiple" defaultSelectedKeys={[2, 4]} />
```

```
// Using the example above
<ExampleTable
  selectionMode="multiple"
  defaultSelectedKeys={[2, 4]}
/>
```

```
// Using the example above
<ExampleTable
  selectionMode="multiple"
  defaultSelectedKeys={[
    2,
    4
  ]}
/>
```

### Disallow empty selection[#](#disallow-empty-selection)

Table also supports a `disallowEmptySelection` prop which forces the user to have at least one row in the Table selected at all times.
In this mode, if a single row is selected and the user presses it, it will not be deselected.

```
// Using the example above
<ExampleTable
  selectionMode="single"
  defaultSelectedKeys={[2]}
  disallowEmptySelection
/>
```

```
// Using the example above
<ExampleTable
  selectionMode="single"
  defaultSelectedKeys={[2]}
  disallowEmptySelection
/>
```

```
// Using the example above
<ExampleTable
  selectionMode="single"
  defaultSelectedKeys={[
    2
  ]}
  disallowEmptySelection
/>
```

### Controlled selection[#](#controlled-selection)

To programmatically control row selection, use the `selectedKeys` prop paired with the `onSelectionChange` callback. The `key` prop from the selected rows will
be passed into the callback when the row is pressed, allowing you to update state accordingly.

```
import type {Selection} from 'react-stately';

function PokemonTable(props) {
  let columns = [
    { name: 'Name', uid: 'name' },
    { name: 'Type', uid: 'type' },
    { name: 'Level', uid: 'level' }
  ];

  let rows = [
    { id: 1, name: 'Charizard', type: 'Fire, Flying', level: '67' },
    { id: 2, name: 'Blastoise', type: 'Water', level: '56' },
    { id: 3, name: 'Venusaur', type: 'Grass, Poison', level: '83' },
    { id: 4, name: 'Pikachu', type: 'Electric', level: '100' }
  ];

  let [selectedKeys, setSelectedKeys] = React.useState<Selection>(new Set([2]));

  return (
    <Table
      aria-label="Table with controlled selection"
      selectionMode="multiple"
      selectedKeys={selectedKeys}
      onSelectionChange={setSelectedKeys}
      {...props}
    >
      <TableHeader columns={columns}>
        {(column) => (
          <Column key={column.uid}>
            {column.name}
          </Column>
        )}
      </TableHeader>
      <TableBody items={rows}>
        {(item) => (
          <Row>
            {(columnKey) => <Cell>{item[columnKey]}</Cell>}
          </Row>
        )}
      </TableBody>
    </Table>
  );
}
```

```
import type {Selection} from 'react-stately';

function PokemonTable(props) {
  let columns = [
    { name: 'Name', uid: 'name' },
    { name: 'Type', uid: 'type' },
    { name: 'Level', uid: 'level' }
  ];

  let rows = [
    {
      id: 1,
      name: 'Charizard',
      type: 'Fire, Flying',
      level: '67'
    },
    {
      id: 2,
      name: 'Blastoise',
      type: 'Water',
      level: '56'
    },
    {
      id: 3,
      name: 'Venusaur',
      type: 'Grass, Poison',
      level: '83'
    },
    {
      id: 4,
      name: 'Pikachu',
      type: 'Electric',
      level: '100'
    }
  ];

  let [selectedKeys, setSelectedKeys] = React.useState<
    Selection
  >(new Set([2]));

  return (
    <Table
      aria-label="Table with controlled selection"
      selectionMode="multiple"
      selectedKeys={selectedKeys}
      onSelectionChange={setSelectedKeys}
      {...props}
    >
      <TableHeader columns={columns}>
        {(column) => (
          <Column key={column.uid}>
            {column.name}
          </Column>
        )}
      </TableHeader>
      <TableBody items={rows}>
        {(item) => (
          <Row>
            {(columnKey) => <Cell>{item[columnKey]}</Cell>}
          </Row>
        )}
      </TableBody>
    </Table>
  );
}
```

```
import type {Selection} from 'react-stately';

function PokemonTable(
  props
) {
  let columns = [
    {
      name: 'Name',
      uid: 'name'
    },
    {
      name: 'Type',
      uid: 'type'
    },
    {
      name: 'Level',
      uid: 'level'
    }
  ];

  let rows = [
    {
      id: 1,
      name: 'Charizard',
      type:
        'Fire, Flying',
      level: '67'
    },
    {
      id: 2,
      name: 'Blastoise',
      type: 'Water',
      level: '56'
    },
    {
      id: 3,
      name: 'Venusaur',
      type:
        'Grass, Poison',
      level: '83'
    },
    {
      id: 4,
      name: 'Pikachu',
      type: 'Electric',
      level: '100'
    }
  ];

  let [
    selectedKeys,
    setSelectedKeys
  ] = React.useState<
    Selection
  >(new Set([2]));

  return (
    <Table
      aria-label="Table with controlled selection"
      selectionMode="multiple"
      selectedKeys={selectedKeys}
      onSelectionChange={setSelectedKeys}
      {...props}
    >
      <TableHeader
        columns={columns}
      >
        {(column) => (
          <Column
            key={column
              .uid}
          >
            {column.name}
          </Column>
        )}
      </TableHeader>
      <TableBody
        items={rows}
      >
        {(item) => (
          <Row>
            {(columnKey) => (
              <Cell>
                {item[
                  columnKey
                ]}
              </Cell>
            )}
          </Row>
        )}
      </TableBody>
    </Table>
  );
}
```

### Disabled rows[#](#disabled-rows)

You can disable specific rows by providing an array of keys to `useTableState` via the `disabledKeys` prop. This will prevent rows from being selectable as shown in the example below.
Note that you are responsible for the styling of disabled rows, however, the selection checkbox will be automatically disabled.

```
// Using the same table as above
<PokemonTable selectionMode="multiple" disabledKeys={[3]} />
```

```
// Using the same table as above
<PokemonTable selectionMode="multiple" disabledKeys={[3]} />
```

```
// Using the same table as above
<PokemonTable
  selectionMode="multiple"
  disabledKeys={[3]}
/>
```

### Selection behavior[#](#selection-behavior)

By default, `useTable` uses the `"toggle"` selection behavior, which behaves like a checkbox group: clicking, tapping, or pressing the `Space` or `Enter` keys toggles selection for the focused row. Using the arrow keys moves focus but does not change selection. The `"toggle"` selection mode is often paired with a column of checkboxes in each row as an explicit affordance for selection.

When the `selectionBehavior` prop is set to `"replace"`, clicking a row with the mouse *replaces* the selection with only that row. Using the arrow keys moves both focus and selection. To select multiple rows, modifier keys such as `Ctrl`, `Cmd`, and `Shift` can be used. To move focus without moving selection, the `Ctrl` key on Windows or the `Option` key on macOS can be held while pressing the arrow keys. Holding this modifier while pressing the `Space` key toggles selection for the focused row, which allows multiple selection of non-contiguous items. On touch screen devices, selection always behaves as toggle since modifier keys may not be available. This behavior emulates native platforms such as macOS and Windows, and is often used when checkboxes in each row are not desired.

```
<PokemonTable selectionMode="multiple" selectionBehavior="replace" />
```

```
<PokemonTable
  selectionMode="multiple"
  selectionBehavior="replace"
/>
```

```
<PokemonTable
  selectionMode="multiple"
  selectionBehavior="replace"
/>
```

### Row actions[#](#row-actions)

`useTable` supports row actions via the `onRowAction` prop, which is useful for functionality such as navigation. In the default `"toggle"` selection behavior, when nothing is selected, clicking or tapping the row triggers the row action.
When at least one item is selected, the table is in selection mode, and clicking or tapping a row toggles the selection. Actions may also be triggered via the `Enter` key, and selection using the `Space` key.

This behavior is slightly different in the `"replace"` selection behavior, where single clicking selects the row and actions are performed via double click. On touch devices, the action becomes the primary tap interaction,
and a long press enters into selection mode, which temporarily swaps the selection behavior to `"toggle"` to perform selection (you may wish to display checkboxes when this happens). Deselecting all items exits selection mode
and reverts the selection behavior back to `"replace"`. Keyboard behaviors are unaffected.

```
<div style={{ display: 'flex', flexWrap: 'wrap', gap: '24px' }}>
  <PokemonTable
    aria-label="Pokemon table with row actions and toggle selection behavior"
    selectionMode="multiple"
    onRowAction={(key) => alert(`Opening item ${key}...`)}
  />
  <PokemonTable
    aria-label="Pokemon table with row actions and replace selection behavior"
    selectionMode="multiple"
    selectionBehavior="replace"
    onRowAction={(key) => alert(`Opening item ${key}...`)}
  />
</div>
```

```
<div
  style={{
    display: 'flex',
    flexWrap: 'wrap',
    gap: '24px'
  }}
>
  <PokemonTable
    aria-label="Pokemon table with row actions and toggle selection behavior"
    selectionMode="multiple"
    onRowAction={(key) =>
      alert(`Opening item ${key}...`)}
  />
  <PokemonTable
    aria-label="Pokemon table with row actions and replace selection behavior"
    selectionMode="multiple"
    selectionBehavior="replace"
    onRowAction={(key) => alert(`Opening item ${key}...`)}
  />
</div>
```

```
<div
  style={{
    display: 'flex',
    flexWrap: 'wrap',
    gap: '24px'
  }}
>
  <PokemonTable
    aria-label="Pokemon table with row actions and toggle selection behavior"
    selectionMode="multiple"
    onRowAction={(key) =>
      alert(
        `Opening item ${key}...`
      )}
  />
  <PokemonTable
    aria-label="Pokemon table with row actions and replace selection behavior"
    selectionMode="multiple"
    selectionBehavior="replace"
    onRowAction={(key) =>
      alert(
        `Opening item ${key}...`
      )}
  />
</div>
```

### Links[#](#links)

Table rows may also be links to another page or website. This can be achieved by passing the `href` prop to the `<Row>` component. Links behave the same way as described above for row actions depending on the `selectionMode` and `selectionBehavior`.

```
<Table aria-label="Bookmarks" selectionMode="multiple">
  <TableHeader>
    <Column isRowHeader>Name</Column>
    <Column>URL</Column>
    <Column>Date added</Column>
  </TableHeader>
  <TableBody>
    <Row href="https://adobe.com/" target="_blank">
      <Cell>Adobe</Cell>
      <Cell>https://adobe.com/</Cell>
      <Cell>January 28, 2023</Cell>
    </Row>
    <Row href="https://google.com/" target="_blank">
      <Cell>Google</Cell>
      <Cell>https://google.com/</Cell>
      <Cell>April 5, 2023</Cell>
    </Row>
    <Row href="https://nytimes.com/" target="_blank">
      <Cell>New York Times</Cell>
      <Cell>https://nytimes.com/</Cell>
      <Cell>July 12, 2023</Cell>
    </Row>
  </TableBody>
</Table>
```

```
<Table aria-label="Bookmarks" selectionMode="multiple">
  <TableHeader>
    <Column isRowHeader>Name</Column>
    <Column>URL</Column>
    <Column>Date added</Column>
  </TableHeader>
  <TableBody>
    <Row href="https://adobe.com/" target="_blank">
      <Cell>Adobe</Cell>
      <Cell>https://adobe.com/</Cell>
      <Cell>January 28, 2023</Cell>
    </Row>
    <Row href="https://google.com/" target="_blank">
      <Cell>Google</Cell>
      <Cell>https://google.com/</Cell>
      <Cell>April 5, 2023</Cell>
    </Row>
    <Row href="https://nytimes.com/" target="_blank">
      <Cell>New York Times</Cell>
      <Cell>https://nytimes.com/</Cell>
      <Cell>July 12, 2023</Cell>
    </Row>
  </TableBody>
</Table>
```

```
<Table
  aria-label="Bookmarks"
  selectionMode="multiple"
>
  <TableHeader>
    <Column
      isRowHeader
    >
      Name
    </Column>
    <Column>
      URL
    </Column>
    <Column>
      Date added
    </Column>
  </TableHeader>
  <TableBody>
    <Row
      href="https://adobe.com/"
      target="_blank"
    >
      <Cell>
        Adobe
      </Cell>
      <Cell>
        https://adobe.com/
      </Cell>
      <Cell>
        January 28,
        2023
      </Cell>
    </Row>
    <Row
      href="https://google.com/"
      target="_blank"
    >
      <Cell>
        Google
      </Cell>
      <Cell>
        https://google.com/
      </Cell>
      <Cell>
        April 5, 2023
      </Cell>
    </Row>
    <Row
      href="https://nytimes.com/"
      target="_blank"
    >
      <Cell>
        New York Times
      </Cell>
      <Cell>
        https://nytimes.com/
      </Cell>
      <Cell>
        July 12, 2023
      </Cell>
    </Row>
  </TableBody>
</Table>
```

#### Client side routing[#](#client-side-routing)

The `<Row>` component works with frameworks and client side routers like [Next.js](https://nextjs.org/) and [React Router](https://reactrouter.com/en/main). As with other React Aria components that support links, this works via the `RouterProvider` component at the root of your app. See the [framework setup guide](../frameworks) to learn how to set this up.

### Sorting[#](#sorting)

Table supports sorting its data when a column header is pressed. To designate that a Column should support sorting, provide it with
the `allowsSorting` prop. The Table accepts a `sortDescriptor` prop that defines the current column key to sort by and the sort direction (ascending/descending).
When the user presses a sortable column header, the column's key and sort direction is passed into the `onSortChange` callback, allowing you to update
the `sortDescriptor` appropriately.

This example performs client side sorting by passing a `sort` function to the [useAsyncList](../useAsyncList.html) hook.
See the docs for more information on how to perform server side sorting.

```
import {useAsyncList} from 'react-stately';

interface Character {
  name: string;
  height: number;
  mass: number;
  birth_year: number;
}

function AsyncSortTable() {
  let list = useAsyncList<Character>({
    async load({ signal }) {
      let res = await fetch(`https://swapi.py4e.com/api/people/?search`, {
        signal
      });
      let json = await res.json();
      return {
        items: json.results
      };
    },
    async sort({ items, sortDescriptor }) {
      return {
        items: items.sort((a, b) => {
          let first = a[sortDescriptor.column];
          let second = b[sortDescriptor.column];
          let cmp = (parseInt(first) || first) < (parseInt(second) || second)
            ? -1
            : 1;
          if (sortDescriptor.direction === 'descending') {
            cmp *= -1;
          }
          return cmp;
        })
      };
    }
  });

  return (
    <Table
      aria-label="Example table with client side sorting"
      sortDescriptor={list.sortDescriptor}
      onSortChange={list.sort}
    >
      <TableHeader>
        <Column key="name" allowsSorting>Name</Column>
        <Column key="height" allowsSorting>Height</Column>
        <Column key="mass" allowsSorting>Mass</Column>
        <Column key="birth_year" allowsSorting>Birth Year</Column>
      </TableHeader>
      <TableBody items={list.items}>
        {(item) => (
          <Row key={item.name}>
            {(columnKey) => <Cell>{item[columnKey]}</Cell>}
          </Row>
        )}
      </TableBody>
    </Table>
  );
}
```

```
import {useAsyncList} from 'react-stately';

interface Character {
  name: string;
  height: number;
  mass: number;
  birth_year: number;
}

function AsyncSortTable() {
  let list = useAsyncList<Character>({
    async load({ signal }) {
      let res = await fetch(
        `https://swapi.py4e.com/api/people/?search`,
        { signal }
      );
      let json = await res.json();
      return {
        items: json.results
      };
    },
    async sort({ items, sortDescriptor }) {
      return {
        items: items.sort((a, b) => {
          let first = a[sortDescriptor.column];
          let second = b[sortDescriptor.column];
          let cmp =
            (parseInt(first) || first) <
                (parseInt(second) || second)
              ? -1
              : 1;
          if (sortDescriptor.direction === 'descending') {
            cmp *= -1;
          }
          return cmp;
        })
      };
    }
  });

  return (
    <Table
      aria-label="Example table with client side sorting"
      sortDescriptor={list.sortDescriptor}
      onSortChange={list.sort}
    >
      <TableHeader>
        <Column key="name" allowsSorting>Name</Column>
        <Column key="height" allowsSorting>Height</Column>
        <Column key="mass" allowsSorting>Mass</Column>
        <Column key="birth_year" allowsSorting>
          Birth Year
        </Column>
      </TableHeader>
      <TableBody items={list.items}>
        {(item) => (
          <Row key={item.name}>
            {(columnKey) => <Cell>{item[columnKey]}</Cell>}
          </Row>
        )}
      </TableBody>
    </Table>
  );
}
```

```
import {useAsyncList} from 'react-stately';

interface Character {
  name: string;
  height: number;
  mass: number;
  birth_year: number;
}

function AsyncSortTable() {
  let list =
    useAsyncList<
      Character
    >({
      async load(
        { signal }
      ) {
        let res =
          await fetch(
            `https://swapi.py4e.com/api/people/?search`,
            { signal }
          );
        let json =
          await res
            .json();
        return {
          items:
            json.results
        };
      },
      async sort(
        {
          items,
          sortDescriptor
        }
      ) {
        return {
          items: items
            .sort(
              (a, b) => {
                let first =
                  a[
                    sortDescriptor
                      .column
                  ];
                let second =
                  b[
                    sortDescriptor
                      .column
                  ];
                let cmp =
                  (parseInt(
                      first
                    ) ||
                      first) <
                      (parseInt(
                        second
                      ) ||
                        second)
                    ? -1
                    : 1;
                if (
                  sortDescriptor
                    .direction ===
                    'descending'
                ) {
                  cmp *=
                    -1;
                }
                return cmp;
              }
            )
        };
      }
    });

  return (
    <Table
      aria-label="Example table with client side sorting"
      sortDescriptor={list
        .sortDescriptor}
      onSortChange={list
        .sort}
    >
      <TableHeader>
        <Column
          key="name"
          allowsSorting
        >
          Name
        </Column>
        <Column
          key="height"
          allowsSorting
        >
          Height
        </Column>
        <Column
          key="mass"
          allowsSorting
        >
          Mass
        </Column>
        <Column
          key="birth_year"
          allowsSorting
        >
          Birth Year
        </Column>
      </TableHeader>
      <TableBody
        items={list
          .items}
      >
        {(item) => (
          <Row
            key={item
              .name}
          >
            {(columnKey) => (
              <Cell>
                {item[
                  columnKey
                ]}
              </Cell>
            )}
          </Row>
        )}
      </TableBody>
    </Table>
  );
}
```

### Nested columns[#](#nested-columns)

Columns can be nested to create column groups. This will result in more than one header row to be created, with the `colSpan`
attribute of each column header cell set to the appropriate value so that the columns line up. Data for the leaf columns
appears in each row of the table body.

This example also shows the use of the `isRowHeader` prop for `Column`, which controls which columns are included in the
accessibility name for each row. By default, only the first column is included, but in some cases more than one column may
be used to represent the row. In this example, the first and last name columns are combined to form the ARIA label for the row.
Only leaf columns may be marked as row headers.

```
<Table aria-label="Example table with nested columns">
  <TableHeader>
    <Column title="Name">
      <Column isRowHeader>First Name</Column>
      <Column isRowHeader>Last Name</Column>
    </Column>
    <Column title="Information">
      <Column>Age</Column>
      <Column>Birthday</Column>
    </Column>
  </TableHeader>
  <TableBody>
    <Row>
      <Cell>Sam</Cell>
      <Cell>Smith</Cell>
      <Cell>36</Cell>
      <Cell>May 3</Cell>
    </Row>
    <Row>
      <Cell>Julia</Cell>
      <Cell>Jones</Cell>
      <Cell>24</Cell>
      <Cell>February 10</Cell>
    </Row>
    <Row>
      <Cell>Peter</Cell>
      <Cell>Parker</Cell>
      <Cell>28</Cell>
      <Cell>September 7</Cell>
    </Row>
    <Row>
      <Cell>Bruce</Cell>
      <Cell>Wayne</Cell>
      <Cell>32</Cell>
      <Cell>December 18</Cell>
    </Row>
  </TableBody>
</Table>
```

```
<Table aria-label="Example table with nested columns">
  <TableHeader>
    <Column title="Name">
      <Column isRowHeader>First Name</Column>
      <Column isRowHeader>Last Name</Column>
    </Column>
    <Column title="Information">
      <Column>Age</Column>
      <Column>Birthday</Column>
    </Column>
  </TableHeader>
  <TableBody>
    <Row>
      <Cell>Sam</Cell>
      <Cell>Smith</Cell>
      <Cell>36</Cell>
      <Cell>May 3</Cell>
    </Row>
    <Row>
      <Cell>Julia</Cell>
      <Cell>Jones</Cell>
      <Cell>24</Cell>
      <Cell>February 10</Cell>
    </Row>
    <Row>
      <Cell>Peter</Cell>
      <Cell>Parker</Cell>
      <Cell>28</Cell>
      <Cell>September 7</Cell>
    </Row>
    <Row>
      <Cell>Bruce</Cell>
      <Cell>Wayne</Cell>
      <Cell>32</Cell>
      <Cell>December 18</Cell>
    </Row>
  </TableBody>
</Table>
```

```
<Table aria-label="Example table with nested columns">
  <TableHeader>
    <Column title="Name">
      <Column
        isRowHeader
      >
        First Name
      </Column>
      <Column
        isRowHeader
      >
        Last Name
      </Column>
    </Column>
    <Column title="Information">
      <Column>
        Age
      </Column>
      <Column>
        Birthday
      </Column>
    </Column>
  </TableHeader>
  <TableBody>
    <Row>
      <Cell>Sam</Cell>
      <Cell>
        Smith
      </Cell>
      <Cell>36</Cell>
      <Cell>
        May 3
      </Cell>
    </Row>
    <Row>
      <Cell>
        Julia
      </Cell>
      <Cell>
        Jones
      </Cell>
      <Cell>24</Cell>
      <Cell>
        February 10
      </Cell>
    </Row>
    <Row>
      <Cell>
        Peter
      </Cell>
      <Cell>
        Parker
      </Cell>
      <Cell>28</Cell>
      <Cell>
        September 7
      </Cell>
    </Row>
    <Row>
      <Cell>
        Bruce
      </Cell>
      <Cell>
        Wayne
      </Cell>
      <Cell>32</Cell>
      <Cell>
        December 18
      </Cell>
    </Row>
  </TableBody>
</Table>
```

### Dynamic nested columns[#](#dynamic-nested-columns)

Nested columns can also be defined dynamically using the function syntax and the `childColumns` prop.
The following example is the same as the example above, but defined dynamically.

```
interface ColumnDefinition {
  name: string,
  key: string,
  children?: ColumnDefinition[],
  isRowHeader?: boolean
}

let columns: ColumnDefinition[] = [
  {name: 'Name', key: 'name', children: [
    {name: 'First Name', key: 'first', isRowHeader: true},
    {name: 'Last Name', key: 'last', isRowHeader: true}
  ]},
  {name: 'Information', key: 'info', children: [
    {name: 'Age', key: 'age'},
    {name: 'Birthday', key: 'birthday'}
  ]}
];

let rows = [
  {id: 1, first: 'Sam', last: 'Smith', age: 36, birthday: 'May 3'},
  {id: 2, first: 'Julia', last: 'Jones', age: 24, birthday: 'February 10'},
  {id: 3, first: 'Peter', last: 'Parker', age: 28, birthday: 'September 7'},
  {id: 4, first: 'Bruce', last: 'Wayne', age: 32, birthday: 'December 18'}
];

<Table aria-label="Example table with dynamic nested columns">
  <TableHeader columns={columns}>
    {column => (
      <Column isRowHeader={column.isRowHeader} childColumns={column.children}>
        {column.name}
      </Column>
    )}
  </TableHeader>
  <TableBody items={rows}>
    {item => (
      <Row>
        {columnKey => <Cell>{item[columnKey]}</Cell>}
      </Row>
    )}
  </TableBody>
</Table>
```

```
interface ColumnDefinition {
  name: string;
  key: string;
  children?: ColumnDefinition[];
  isRowHeader?: boolean;
}

let columns: ColumnDefinition[] = [
  {
    name: 'Name',
    key: 'name',
    children: [
      {
        name: 'First Name',
        key: 'first',
        isRowHeader: true
      },
      { name: 'Last Name', key: 'last', isRowHeader: true }
    ]
  },
  {
    name: 'Information',
    key: 'info',
    children: [
      { name: 'Age', key: 'age' },
      { name: 'Birthday', key: 'birthday' }
    ]
  }
];

let rows = [
  {
    id: 1,
    first: 'Sam',
    last: 'Smith',
    age: 36,
    birthday: 'May 3'
  },
  {
    id: 2,
    first: 'Julia',
    last: 'Jones',
    age: 24,
    birthday: 'February 10'
  },
  {
    id: 3,
    first: 'Peter',
    last: 'Parker',
    age: 28,
    birthday: 'September 7'
  },
  {
    id: 4,
    first: 'Bruce',
    last: 'Wayne',
    age: 32,
    birthday: 'December 18'
  }
];

<Table aria-label="Example table with dynamic nested columns">
  <TableHeader columns={columns}>
    {(column) => (
      <Column
        isRowHeader={column.isRowHeader}
        childColumns={column.children}
      >
        {column.name}
      </Column>
    )}
  </TableHeader>
  <TableBody items={rows}>
    {(item) => (
      <Row>
        {(columnKey) => <Cell>{item[columnKey]}</Cell>}
      </Row>
    )}
  </TableBody>
</Table>
```

```
interface ColumnDefinition {
  name: string;
  key: string;
  children?:
    ColumnDefinition[];
  isRowHeader?: boolean;
}

let columns:
  ColumnDefinition[] = [
    {
      name: 'Name',
      key: 'name',
      children: [
        {
          name:
            'First Name',
          key: 'first',
          isRowHeader:
            true
        },
        {
          name:
            'Last Name',
          key: 'last',
          isRowHeader:
            true
        }
      ]
    },
    {
      name:
        'Information',
      key: 'info',
      children: [
        {
          name: 'Age',
          key: 'age'
        },
        {
          name:
            'Birthday',
          key: 'birthday'
        }
      ]
    }
  ];

let rows = [
  {
    id: 1,
    first: 'Sam',
    last: 'Smith',
    age: 36,
    birthday: 'May 3'
  },
  {
    id: 2,
    first: 'Julia',
    last: 'Jones',
    age: 24,
    birthday:
      'February 10'
  },
  {
    id: 3,
    first: 'Peter',
    last: 'Parker',
    age: 28,
    birthday:
      'September 7'
  },
  {
    id: 4,
    first: 'Bruce',
    last: 'Wayne',
    age: 32,
    birthday:
      'December 18'
  }
];

<Table aria-label="Example table with dynamic nested columns">
  <TableHeader
    columns={columns}
  >
    {(column) => (
      <Column
        isRowHeader={column
          .isRowHeader}
        childColumns={column
          .children}
      >
        {column.name}
      </Column>
    )}
  </TableHeader>
  <TableBody
    items={rows}
  >
    {(item) => (
      <Row>
        {(columnKey) => (
          <Cell>
            {item[
              columnKey
            ]}
          </Cell>
        )}
      </Row>
    )}
  </TableBody>
</Table>
```

## Resizable Columns[#](#resizable-columns)

---

For resizable column support, two additional hooks need to be added to the table implementation above. The `useTableColumnResizeState`
hook from `@react-stately/table` is responsible for initializing and tracking the widths of every column in your table, returning functions that you can use to
update the column widths during a column resize operation. Note that this state is supplementary to the state returned by `useTableState`.

The second column resizing hook is `useTableColumnResize`. This hook handles the interactions for a table column's resizer
element, allowing the user to drag the resizer or use the keyboard arrows to expand the column's width. Be sure to pass the state returned by `useTableColumnResizeState`
to this hook so the tracked widths can be updated appropriately. We'll walk through all the required changes to the previous table implementation step by step below. For simplicity's sake, we'll be
omitting support for selection, sorting, and nested columns.

### Table[#](#table)

As mentioned previously, we first need to call `useTableColumnResizeState` to initialize the widths for our table's columns.
We'll pass the state returned by `useTableColumnResizeState` along with any user defined `onResize` handlers
to our `ResizableTableColumnHeaders` so it can be used by `useTableColumnResize`.

The various style changes below are to add a wrapper div so the table is scrollable when the row content overflows and to support table body/column widths greater than the 300px applied to the table itself.

```
import {useTableColumnResizeState} from 'react-stately';
import {useCallback} from 'react';

function ResizableColumnsTable(props) {
  let state = useTableState(props);
  let scrollRef = useRef<HTMLDivElement | null>(null);
  let ref = useRef<HTMLTableElement | null>(null);
  let { collection } = state;
  let { gridProps } = useTable(
    {
      ...props,
      // The table wrapper is scrollable rather than just the body
      scrollRef
          },
    state,
    ref
  );

  // Set the minimum width of the columns to 40px
  let getDefaultMinWidth = useCallback(() => {
    return 40;
  }, []);

  let layoutState = useTableColumnResizeState({
    // Matches the width of the table itself
    tableWidth: 300,
    getDefaultMinWidth
  }, state);
  return (
    <div className="aria-table-wrapper" ref={scrollRef}>      <table
        {...gridProps}
        className="aria-table"
        ref={ref}
      >
        <TableRowGroup type="thead">
          {collection.headerRows.map((headerRow) => (
            <TableHeaderRow key={headerRow.key} item={headerRow} state={state}>
              {[...headerRow.childNodes].map((column) => (
                <ResizableTableColumnHeader
                  key={column.key}
                  column={column}
                  state={state}
                  layoutState={layoutState}
                  onResizeStart={props.onResizeStart}
                  onResize={props.onResize}
                  onResizeEnd={props.onResizeEnd}                />
              ))}
            </TableHeaderRow>
          ))}
        </TableRowGroup>
        <TableRowGroup type="tbody">
          {[...collection.body.childNodes].map((row) => (
            <TableRow key={row.key} item={row} state={state}>
              {[...row.childNodes].map((cell) => (
                <TableCell key={cell.key} cell={cell} state={state} />
              ))}
            </TableRow>
          ))}
        </TableRowGroup>
      </table>
    </div>
  );
}
```

```
import {useTableColumnResizeState} from 'react-stately';
import {useCallback} from 'react';

function ResizableColumnsTable(props) {
  let state = useTableState(props);
  let scrollRef = useRef<HTMLDivElement | null>(null);
  let ref = useRef<HTMLTableElement | null>(null);
  let { collection } = state;
  let { gridProps } = useTable(
    {
      ...props,
      // The table wrapper is scrollable rather than just the body
      scrollRef
          },
    state,
    ref
  );

  // Set the minimum width of the columns to 40px
  let getDefaultMinWidth = useCallback(() => {
    return 40;
  }, []);

  let layoutState = useTableColumnResizeState({
    // Matches the width of the table itself
    tableWidth: 300,
    getDefaultMinWidth
  }, state);
  return (
    <div className="aria-table-wrapper" ref={scrollRef}>      <table
        {...gridProps}
        className="aria-table"
        ref={ref}
      >
        <TableRowGroup type="thead">
          {collection.headerRows.map((headerRow) => (
            <TableHeaderRow
              key={headerRow.key}
              item={headerRow}
              state={state}
            >
              {[...headerRow.childNodes].map((column) => (
                <ResizableTableColumnHeader
                  key={column.key}
                  column={column}
                  state={state}
                  layoutState={layoutState}
                  onResizeStart={props.onResizeStart}
                  onResize={props.onResize}
                  onResizeEnd={props.onResizeEnd}                />
              ))}
            </TableHeaderRow>
          ))}
        </TableRowGroup>
        <TableRowGroup type="tbody">
          {[...collection.body.childNodes].map((row) => (
            <TableRow
              key={row.key}
              item={row}
              state={state}
            >
              {[...row.childNodes].map((cell) => (
                <TableCell
                  key={cell.key}
                  cell={cell}
                  state={state}
                />
              ))}
            </TableRow>
          ))}
        </TableRowGroup>
      </table>
    </div>
  );
}
```

```
import {useTableColumnResizeState} from 'react-stately';
import {useCallback} from 'react';

function ResizableColumnsTable(
  props
) {
  let state =
    useTableState(props);
  let scrollRef = useRef<
    HTMLDivElement | null
  >(null);
  let ref = useRef<
    | HTMLTableElement
    | null
  >(null);
  let { collection } =
    state;
  let { gridProps } =
    useTable(
      {
        ...props,
        // The table wrapper is scrollable rather than just the body
        scrollRef
              },
      state,
      ref
    );

  // Set the minimum width of the columns to 40px
  let getDefaultMinWidth =
    useCallback(() => {
      return 40;
    }, []);

  let layoutState =
    useTableColumnResizeState(
      {
        // Matches the width of the table itself
        tableWidth: 300,
        getDefaultMinWidth
      },
      state
    );
  return (
    <div
      className="aria-table-wrapper"
      ref={scrollRef}
    >      <table
        {...gridProps}
        className="aria-table"
        ref={ref}
      >
        <TableRowGroup type="thead">
          {collection
            .headerRows
            .map(
              (headerRow) => (
                <TableHeaderRow
                  key={headerRow
                    .key}
                  item={headerRow}
                  state={state}
                >
                  {[
                    ...headerRow
                      .childNodes
                  ].map(
                    (column) => (
                      <ResizableTableColumnHeader
                        key={column
                          .key}
                        column={column}
                        state={state}
                        layoutState={layoutState}
                        onResizeStart={props
                          .onResizeStart}
                        onResize={props
                          .onResize}
                        onResizeEnd={props
                          .onResizeEnd}                      />
                    )
                  )}
                </TableHeaderRow>
              )
            )}
        </TableRowGroup>
        <TableRowGroup type="tbody">
          {[
            ...collection
              .body
              .childNodes
          ].map(
            (row) => (
              <TableRow
                key={row
                  .key}
                item={row}
                state={state}
              >
                {[
                  ...row
                    .childNodes
                ].map(
                  (cell) => (
                    <TableCell
                      key={cell
                        .key}
                      cell={cell}
                      state={state}
                    />
                  )
                )}
              </TableRow>
            )
          )}
        </TableRowGroup>
      </table>
    </div>
  );
}
```

 Show CSS

```
.aria-table-wrapper {
  width: 300px;
  overflow: auto;
}

.aria-table {
  border-collapse: collapse;
  table-layout: fixed;
  width: fit-content;

  & td {
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }
}
```

```
.aria-table-wrapper {
  width: 300px;
  overflow: auto;
}

.aria-table {
  border-collapse: collapse;
  table-layout: fixed;
  width: fit-content;

  & td {
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }
}
```

```
.aria-table-wrapper {
  width: 300px;
  overflow: auto;
}

.aria-table {
  border-collapse: collapse;
  table-layout: fixed;
  width: fit-content;

  & td {
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }
}
```

### Resizable table header[#](#resizable-table-header)

The `TableColumnHeader` is where we see the bulk of the changes required to support resizable columns. First of all, we need to accommodate a `Resizer` element in every resizable column that
the user can drag or focus to perform a resize operation. Since the resizer will be a focusable element within the table header, we need to make the header title a focusable element as well so keyboard
focus won't be immediately sent to the resizer as you navigate between the column headers. Finally, we apply the computed width of our column from `useTableColumnResizeState`
to the header element.

```
// Reuse the Button from your component library. See below for details.
import {Button} from 'your-component-library';

function ResizableTableColumnHeader(
  { column, state, layoutState, onResizeStart, onResize, onResizeEnd }
) {
  let allowsResizing = column.props.allowsResizing;
  let ref = useRef<HTMLTableCellElement | null>(null);
  let { columnHeaderProps } = useTableColumnHeader(
    { node: column },
    state,
    ref
  );

  return (
    <th
      {...columnHeaderProps}
      className="aria-table-headerCell"
      style={{ width: layoutState.getColumnWidth(column.key) }}
      ref={ref}
    >
      <div style={{ display: 'flex', position: 'relative' }}>
        <Button className="aria-table-headerTitle">
          {column.rendered}
        </Button>
        {allowsResizing &&
          (
            <Resizer
              column={column}
              layoutState={layoutState}
              onResizeStart={onResizeStart}
              onResize={onResize}
              onResizeEnd={onResizeEnd}
            />
          )}
      </div>
    </th>
  );
}
```

```
// Reuse the Button from your component library. See below for details.
import {Button} from 'your-component-library';

function ResizableTableColumnHeader(
  {
    column,
    state,
    layoutState,
    onResizeStart,
    onResize,
    onResizeEnd
  }
) {
  let allowsResizing = column.props.allowsResizing;
  let ref = useRef<HTMLTableCellElement | null>(null);
  let { columnHeaderProps } = useTableColumnHeader(
    { node: column },
    state,
    ref
  );

  return (
    <th
      {...columnHeaderProps}
      className="aria-table-headerCell"
      style={{
        width: layoutState.getColumnWidth(column.key)
      }}
      ref={ref}
    >
      <div
        style={{ display: 'flex', position: 'relative' }}
      >
        <Button className="aria-table-headerTitle">
          {column.rendered}
        </Button>
        {allowsResizing &&
          (
            <Resizer
              column={column}
              layoutState={layoutState}
              onResizeStart={onResizeStart}
              onResize={onResize}
              onResizeEnd={onResizeEnd}
            />
          )}
      </div>
    </th>
  );
}
```

```
// Reuse the Button from your component library. See below for details.
import {Button} from 'your-component-library';

function ResizableTableColumnHeader(
  {
    column,
    state,
    layoutState,
    onResizeStart,
    onResize,
    onResizeEnd
  }
) {
  let allowsResizing =
    column.props
      .allowsResizing;
  let ref = useRef<
    | HTMLTableCellElement
    | null
  >(null);
  let {
    columnHeaderProps
  } =
    useTableColumnHeader(
      { node: column },
      state,
      ref
    );

  return (
    <th
      {...columnHeaderProps}
      className="aria-table-headerCell"
      style={{
        width:
          layoutState
            .getColumnWidth(
              column.key
            )
      }}
      ref={ref}
    >
      <div
        style={{
          display:
            'flex',
          position:
            'relative'
        }}
      >
        <Button className="aria-table-headerTitle">
          {column
            .rendered}
        </Button>
        {allowsResizing &&
          (
            <Resizer
              column={column}
              layoutState={layoutState}
              onResizeStart={onResizeStart}
              onResize={onResize}
              onResizeEnd={onResizeEnd}
            />
          )}
      </div>
    </th>
  );
}
```

 Show CSS

```
.aria-table-headerCell {
  padding: 5px 10px;
  outline: none;
  cursor: default;
  box-sizing: border-box;
  box-shadow: none;
  text-align: left;
}

.aria-table-headerTitle {
  width: 100%;
  text-align: left;
  border: none;
  background: transparent;
  flex: 1 1 auto;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  margin-inline-start: -6px;
  outline: none;
}

.aria-table-headerTitle.focus {
  outline: 2px solid orange;
}
```

```
.aria-table-headerCell {
  padding: 5px 10px;
  outline: none;
  cursor: default;
  box-sizing: border-box;
  box-shadow: none;
  text-align: left;
}

.aria-table-headerTitle {
  width: 100%;
  text-align: left;
  border: none;
  background: transparent;
  flex: 1 1 auto;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  margin-inline-start: -6px;
  outline: none;
}

.aria-table-headerTitle.focus {
  outline: 2px solid orange;
}
```

```
.aria-table-headerCell {
  padding: 5px 10px;
  outline: none;
  cursor: default;
  box-sizing: border-box;
  box-shadow: none;
  text-align: left;
}

.aria-table-headerTitle {
  width: 100%;
  text-align: left;
  border: none;
  background: transparent;
  flex: 1 1 auto;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  margin-inline-start: -6px;
  outline: none;
}

.aria-table-headerTitle.focus {
  outline: 2px solid orange;
}
```

### Button[#](#button)

The `Button` component is used in the above example to represent the table column header title. It is built using the [useButton](../Button/useButton.html) hook, and can be shared with many other components.

 Show code

```
import {useButton} from 'react-aria';

function Button(props) {
  let ref = useRef<HTMLButtonElement | null>(null);
  let { focusProps, isFocusVisible } = useFocusRing();
  let { buttonProps } = useButton(props, ref);
  return (
    <button
      {...mergeProps(buttonProps, focusProps)}
      ref={ref}
      className={`${props.className} ${isFocusVisible ? 'focus' : ''}`}
    >
      {props.children}
    </button>
  );
}
```

```
import {useButton} from 'react-aria';

function Button(props) {
  let ref = useRef<HTMLButtonElement | null>(null);
  let { focusProps, isFocusVisible } = useFocusRing();
  let { buttonProps } = useButton(props, ref);
  return (
    <button
      {...mergeProps(buttonProps, focusProps)}
      ref={ref}
      className={`${props.className} ${
        isFocusVisible ? 'focus' : ''
      }`}
    >
      {props.children}
    </button>
  );
}
```

```
import {useButton} from 'react-aria';

function Button(props) {
  let ref = useRef<
    | HTMLButtonElement
    | null
  >(null);
  let {
    focusProps,
    isFocusVisible
  } = useFocusRing();
  let { buttonProps } =
    useButton(
      props,
      ref
    );
  return (
    <button
      {...mergeProps(
        buttonProps,
        focusProps
      )}
      ref={ref}
      className={`${props.className} ${
        isFocusVisible
          ? 'focus'
          : ''
      }`}
    >
      {props.children}
    </button>
  );
}
```

### Resizer[#](#resizer)

As described above, we need to implement an element that the user can drag/interact with to resize a column. Here we'll use the `useTableColumnResize`
hook to create a visible resizer div for physical drag operations and a visually hidden input responsible for keyboard and screenreader interactions, similar to a [slider](../Slider/useSlider.html).
Users can press and drag on the visible resizer to trigger the `onResize` callbacks and update the tracked column widths accordingly. When focused, keyboard users can begin resizing the column by pressing `Enter`.
Once resizing is activated, they can use the arrow keys to trigger the same resize events and press `Enter`, `Esc`, or `Space` to exit resizing. Touch screen reader users can swipe
left or right to focus the column's resizer input and swipe up and down to resize the column.

```
import {useTableColumnResize} from 'react-aria';

function Resizer(props) {
  let { column, layoutState, onResizeStart, onResize, onResizeEnd } = props;
  let ref = useRef<HTMLInputElement | null>(null);
  let { resizerProps, inputProps, isResizing } = useTableColumnResize(
    {
      column,
      'aria-label': 'Resizer',
      onResizeStart,
      onResize,
      onResizeEnd
    },
    layoutState,
    ref
  );
  let { focusProps, isFocusVisible } = useFocusRing();

  return (
    <div
      role="presentation"
      className={`aria-table-resizer ${isFocusVisible ? 'focus' : ''} ${
        isResizing ? 'resizing' : ''
      }`}
      {...resizerProps}
    >
      <input
        ref={ref}
        {...mergeProps(inputProps, focusProps)}
      />
    </div>
  );
}
```

```
import {useTableColumnResize} from 'react-aria';

function Resizer(props) {
  let {
    column,
    layoutState,
    onResizeStart,
    onResize,
    onResizeEnd
  } = props;
  let ref = useRef<HTMLInputElement | null>(null);
  let { resizerProps, inputProps, isResizing } =
    useTableColumnResize(
      {
        column,
        'aria-label': 'Resizer',
        onResizeStart,
        onResize,
        onResizeEnd
      },
      layoutState,
      ref
    );
  let { focusProps, isFocusVisible } = useFocusRing();

  return (
    <div
      role="presentation"
      className={`aria-table-resizer ${
        isFocusVisible ? 'focus' : ''
      } ${isResizing ? 'resizing' : ''}`}
      {...resizerProps}
    >
      <input
        ref={ref}
        {...mergeProps(inputProps, focusProps)}
      />
    </div>
  );
}
```

```
import {useTableColumnResize} from 'react-aria';

function Resizer(props) {
  let {
    column,
    layoutState,
    onResizeStart,
    onResize,
    onResizeEnd
  } = props;
  let ref = useRef<
    | HTMLInputElement
    | null
  >(null);
  let {
    resizerProps,
    inputProps,
    isResizing
  } =
    useTableColumnResize(
      {
        column,
        'aria-label':
          'Resizer',
        onResizeStart,
        onResize,
        onResizeEnd
      },
      layoutState,
      ref
    );
  let {
    focusProps,
    isFocusVisible
  } = useFocusRing();

  return (
    <div
      role="presentation"
      className={`aria-table-resizer ${
        isFocusVisible
          ? 'focus'
          : ''
      } ${
        isResizing
          ? 'resizing'
          : ''
      }`}
      {...resizerProps}
    >
      <input
        ref={ref}
        {...mergeProps(
          inputProps,
          focusProps
        )}
      />
    </div>
  );
}
```

 Show CSS

```
.aria-table-resizer {
  width: 15px;
  background-color: grey;
  cursor: col-resize;
  height: 30px;
  touch-action: none;
  flex: 0 0 auto;
  box-sizing: border-box;
  border: 5px;
  border-style: none solid;
  border-color: transparent;
  background-clip: content-box;
}

.aria-table-resizer.focus {
  background-color: orange;
}

.aria-table-resizer.resizing {
  border-color: orange;
  background-color: transparent;
}
```

```
.aria-table-resizer {
  width: 15px;
  background-color: grey;
  cursor: col-resize;
  height: 30px;
  touch-action: none;
  flex: 0 0 auto;
  box-sizing: border-box;
  border: 5px;
  border-style: none solid;
  border-color: transparent;
  background-clip: content-box;
}

.aria-table-resizer.focus {
  background-color: orange;
}

.aria-table-resizer.resizing {
  border-color: orange;
  background-color: transparent;
}
```

```
.aria-table-resizer {
  width: 15px;
  background-color: grey;
  cursor: col-resize;
  height: 30px;
  touch-action: none;
  flex: 0 0 auto;
  box-sizing: border-box;
  border: 5px;
  border-style: none solid;
  border-color: transparent;
  background-clip: content-box;
}

.aria-table-resizer.focus {
  background-color: orange;
}

.aria-table-resizer.resizing {
  border-color: orange;
  background-color: transparent;
}
```

And with that, all necessary changes to the previous table implementation have been made and we now have a table that supports resizable columns!
The example below supports resizing via mouse, keyboard, touch, and screen reader interactions. To see an example with sorting and selection, see the
[styled example](#styled-examples)!

```
<ResizableColumnsTable aria-label="Table with resizable columns">
  <TableHeader>
    <Column allowsResizing>Name</Column>
    <Column allowsResizing>Type</Column>
    <Column allowsResizing>Level</Column>
  </TableHeader>
  <TableBody>
    <Row key="1">
      <Cell>Charizard</Cell>
      <Cell>Fire, Flying</Cell>
      <Cell>67</Cell>
    </Row>
    <Row key="2">
      <Cell>Blastoise</Cell>
      <Cell>Water</Cell>
      <Cell>56</Cell>
    </Row>
    <Row key="3">
      <Cell>Venusaur</Cell>
      <Cell>Grass, Poison</Cell>
      <Cell>83</Cell>
    </Row>
    <Row key="4">
      <Cell>Pikachu</Cell>
      <Cell>Electric</Cell>
      <Cell>100</Cell>
    </Row>
  </TableBody>
</ResizableColumnsTable>
```

```
<ResizableColumnsTable aria-label="Table with resizable columns">
  <TableHeader>
    <Column allowsResizing>Name</Column>
    <Column allowsResizing>Type</Column>
    <Column allowsResizing>Level</Column>
  </TableHeader>
  <TableBody>
    <Row key="1">
      <Cell>Charizard</Cell>
      <Cell>Fire, Flying</Cell>
      <Cell>67</Cell>
    </Row>
    <Row key="2">
      <Cell>Blastoise</Cell>
      <Cell>Water</Cell>
      <Cell>56</Cell>
    </Row>
    <Row key="3">
      <Cell>Venusaur</Cell>
      <Cell>Grass, Poison</Cell>
      <Cell>83</Cell>
    </Row>
    <Row key="4">
      <Cell>Pikachu</Cell>
      <Cell>Electric</Cell>
      <Cell>100</Cell>
    </Row>
  </TableBody>
</ResizableColumnsTable>
```

```
<ResizableColumnsTable aria-label="Table with resizable columns">
  <TableHeader>
    <Column
      allowsResizing
    >
      Name
    </Column>
    <Column
      allowsResizing
    >
      Type
    </Column>
    <Column
      allowsResizing
    >
      Level
    </Column>
  </TableHeader>
  <TableBody>
    <Row key="1">
      <Cell>
        Charizard
      </Cell>
      <Cell>
        Fire, Flying
      </Cell>
      <Cell>67</Cell>
    </Row>
    <Row key="2">
      <Cell>
        Blastoise
      </Cell>
      <Cell>
        Water
      </Cell>
      <Cell>56</Cell>
    </Row>
    <Row key="3">
      <Cell>
        Venusaur
      </Cell>
      <Cell>
        Grass, Poison
      </Cell>
      <Cell>83</Cell>
    </Row>
    <Row key="4">
      <Cell>
        Pikachu
      </Cell>
      <Cell>
        Electric
      </Cell>
      <Cell>100</Cell>
    </Row>
  </TableBody>
</ResizableColumnsTable>
```

### Styled examples[#](#styled-examples)

[![](/Table-tailwind.36cf5f3e.png)

Tailwind CSS

A table supporting resizable columns, selection, and sorting built with Tailwind and React Aria.](https://codesandbox.io/s/objective-cherry-g837on?file=/src/Table.tsx)

## Internationalization[#](#internationalization)

---

`useTable` handles some aspects of internationalization automatically.
For example, type to select is implemented with an
[Intl.Collator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Collator)
for internationalized string matching, and keyboard navigation is mirrored in right-to-left languages.
You are responsible for localizing all text content within the table.

### RTL[#](#rtl)

In right-to-left languages, the table layout should be mirrored. The columns should be ordered from right to left and the
individual column text alignment should be inverted. Ensure that your CSS accounts for this.

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `layoutDelegate` | `LayoutDelegate` | â | The layout object for the table. Computes what content is visible and how to position and style them. |
| `isVirtualized` | `boolean` | â | Whether the grid uses virtual scrolling. |
| `disallowTypeAhead` | `boolean` | `false` | Whether typeahead navigation is disabled. |
| `keyboardDelegate` | `KeyboardDelegate` | â | An optional keyboard delegate implementation for type to select, to override the default. |
| `focusMode` | `'row' |Â 'cell'` | `'row'` | Whether initial grid focus should be placed on the grid row or grid cell. |
| `getRowText` | `( (key: Key )) => string` | `(key) => state.collection.getItem(key)?.textValue` | A function that returns the text that should be announced by assistive technology when a row is added or removed from selection. |
| `scrollRef` | `RefObject<HTMLElement |Â null>` | â | The ref attached to the scrollable body. Used to provided automatic scrolling on item focus for non-virtualized grids. |
| `onRowAction` | `( (key: Key )) => void` | â | Handler that is called when a user performs an action on the row. |
| `onCellAction` | `( (key: Key )) => void` | â | Handler that is called when a user performs an action on the cell. |
| `escapeKeyBehavior` | `'clearSelection' |Â 'none'` | `'clearSelection'` | Whether pressing the escape key should clear selection in the grid or not.  Most experiences should not modify this option as it eliminates a keyboard user's ability to easily clear selection. Only use if the escape key is being handled externally or should not trigger selection clearing contextually. |
| `shouldSelectOnPressUp` | `boolean` | â | Whether selection should occur on press up instead of press down. |
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `aria-label` | `string` | â | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |

A LayoutDelegate provides layout information for collection items.

| Method | Description |
| --- | --- |
| `getItemRect( (key: Key )): Rect |Â null` | Returns a rectangle for the item with the given key. |
| `getVisibleRect(): Rect` | Returns the visible rectangle of the collection. |
| `getContentSize(): Size` | Returns the size of the scrollable content in the collection. |
| `getKeyRange( (from: Key, , to: Key )): Key[]` | Returns a list of keys between `from` and `to`. |

| Name | Type | Description |
| --- | --- | --- |
| `x` | `number` |  |
| `y` | `number` |  |
| `width` | `number` |  |
| `height` | `number` |  |

| Name | Type | Description |
| --- | --- | --- |
| `width` | `number` |  |
| `height` | `number` |  |

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `virtualizer` | `DeprecatedVirtualizer` |  |

### Methods

| Method | Description |
| --- | --- |
| `getLayoutInfo( (key: Key )): DeprecatedLayoutInfo` |  |
| `getContentSize(): Size` |  |

`string |Â number`

| Name | Type | Description |
| --- | --- | --- |
| `rect` | `Rect` |  |

| Name | Type | Description |
| --- | --- | --- |
| `visibleRect` | `Rect` |  |

| Method | Description |
| --- | --- |
| `getKeyBelow( (key: Key )): Key |Â null` | Returns the key visually below the given one, or `null` for none. |
| `getKeyAbove( (key: Key )): Key |Â null` | Returns the key visually above the given one, or `null` for none. |
| `getKeyLeftOf( (key: Key )): Key |Â null` | Returns the key visually to the left of the given one, or `null` for none. |
| `getKeyRightOf( (key: Key )): Key |Â null` | Returns the key visually to the right of the given one, or `null` for none. |
| `getKeyPageBelow( (key: Key )): Key |Â null` | Returns the key visually one page below the given one, or `null` for none. |
| `getKeyPageAbove( (key: Key )): Key |Â null` | Returns the key visually one page above the given one, or `null` for none. |
| `getFirstKey( (key?: Key |Â  |Â null, , global?: boolean )): Key |Â null` | Returns the first key, or `null` for none. |
| `getLastKey( (key?: Key |Â  |Â null, , global?: boolean )): Key |Â null` | Returns the last key, or `null` for none. |
| `getKeyForSearch( (search: string, , fromKey?: Key |Â  |Â null )): Key |Â null` | Returns the next key after `fromKey` that matches the given search string, or `null` for none. |

| Name | Type | Description |
| --- | --- | --- |
| `current` | `T` |  |

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `collection` | `TableCollection<T>` | A collection of rows and columns in the table. |
| `showSelectionCheckboxes` | `boolean` | Whether the row selection checkboxes should be displayed. |
| `sortDescriptor` | `SortDescriptor |Â null` | The current sorted column and direction. |
| `isKeyboardNavigationDisabled` | `boolean` | Whether keyboard navigation is disabled, such as when the arrow keys should be handled by a component within a cell. |
| `setKeyboardNavigationDisabled` | `( (val: boolean )) => void` | Set whether keyboard navigation is disabled, such as when the arrow keys should be handled by a component within a cell. |
| `disabledKeys` | `Set<Key>` | A set of keys for rows that are disabled. |
| `selectionManager` | `SelectionManager` | A selection manager to read and update row selection state. |

### Methods

| Method | Description |
| --- | --- |
| `sort( (columnKey: Key, , direction?: 'ascending' |Â  |Â 'descending' )): void` | Calls the provided onSortChange handler with the provided column key and sort direction. |

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `headerRows` | `GridNode<T>[]` | A list of header row nodes in the table. |
| `columns` | `GridNode<T>[]` | A list of column nodes in the table. |
| `rowHeaderColumnKeys` | `Set<Key>` | A set of column keys that serve as the [row header](https://www.w3.org/TR/wai-aria-1.1/#rowheader). |
| `body` | `GridNode<T>` | The node that makes up the body of the table. |
| `columnCount` | `number` | The number of columns in the grid. |
| `rows` | `GridNode<T>[]` | A list of rows in the grid. |
| `size` | `number` | The number of items in the collection. |
| `head` | `GridNode<T>` | The node that makes up the header of the table. |

### Methods

| Method | Description |
| --- | --- |
| `getKeys(): Iterable<Key>` | Iterate over all keys in the collection. |
| `getItem( (key: Key )): GridNode<T> |Â null` | Get an item by its key. |
| `at( (idx: number )): GridNode<T> |Â null` | Get an item by the index of its key. |
| `getKeyBefore( (key: Key )): Key |Â null` | Get the key that comes before the given key in the collection. |
| `getKeyAfter( (key: Key )): Key |Â null` | Get the key that comes after the given key in the collection. |
| `getFirstKey(): Key |Â null` | Get the first key in the collection. |
| `getLastKey(): Key |Â null` | Get the last key in the collection. |
| `getChildren( (key: Key )): Iterable<GridNode<T>>` | Iterate over the child items of the given key. |
| `getTextValue( (key: Key )): string` | Returns a string representation of the item's contents. |
| `filter( (filterFn: ( (nodeValue: string, , node: GridNode<T> )) => boolean )): Collection<GridNode<T>>` | Filters the collection using the given function. |

| Name | Type | Description |
| --- | --- | --- |
| `type` | `string` | The type of item this node represents. |
| `key` | `Key` | A unique key for the node. |
| `value` | `T |Â null` | The object value the node was created from. |
| `level` | `number` | The level of depth this node is at in the hierarchy. |
| `hasChildNodes` | `boolean` | Whether this item has children, even if not loaded yet. |
| `rendered` | `ReactNode` | The rendered contents of this node (e.g. JSX). |
| `textValue` | `string` | A string value for this node, used for features like typeahead. |
| `index` | `number` | The index of this node within its parent. |
| `column` | `GridNode<T>` |  |
| `colSpan` | `number |Â null` | The number of columns spanned by this cell. |
| `colIndex` | `number |Â null` | The column index of this cell, accounting for any colSpans. |
| `indexOfType` | `number` | The index of this node within its parent, ignoring sibling nodes that aren't of the same type. |
| `aria-label` | `string` | An accessibility label for this node. |
| `wrapper` | `( (element: ReactElement )) => ReactElement` | A function that should be called to wrap the rendered node. |
| `parentKey` | `Key |Â null` | The key of the parent node. |
| `prevKey` | `Key |Â null` | The key of the node before this node. |
| `nextKey` | `Key |Â null` | The key of the node after this node. |
| `props` | `any` | Additional properties specific to a particular node type. |
| `render` | `( (node: Node<any> )) => ReactElement` | A function that renders this node to a React Element in the DOM. |

| Name | Type | Description |
| --- | --- | --- |
| `type` | `string` | The type of item this node represents. |
| `key` | `Key` | A unique key for the node. |
| `value` | `T |Â null` | The object value the node was created from. |
| `level` | `number` | The level of depth this node is at in the hierarchy. |
| `hasChildNodes` | `boolean` | Whether this item has children, even if not loaded yet. |
| `rendered` | `ReactNode` | The rendered contents of this node (e.g. JSX). |
| `textValue` | `string` | A string value for this node, used for features like typeahead. |
| `index` | `number` | The index of this node within its parent. |
| `aria-label` | `string` | An accessibility label for this node. |
| `wrapper` | `( (element: ReactElement )) => ReactElement` | A function that should be called to wrap the rendered node. |
| `parentKey` | `Key |Â null` | The key of the parent node. |
| `prevKey` | `Key |Â null` | The key of the node before this node. |
| `nextKey` | `Key |Â null` | The key of the node after this node. |
| `props` | `any` | Additional properties specific to a particular node type. |
| `render` | `( (node: Node<any> )) => ReactElement` | A function that renders this node to a React Element in the DOM. |

A generic interface to access a readonly sequential
collection of unique keyed items.

**Extends**: `Iterable`

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `size` | `number` | The number of items in the collection. |

### Methods

| Method | Description |
| --- | --- |
| `getKeys(): Iterable<Key>` | Iterate over all keys in the collection. |
| `getItem( (key: Key )): T |Â null` | Get an item by its key. |
| `at( (idx: number )): T |Â null` | Get an item by the index of its key. |
| `getKeyBefore( (key: Key )): Key |Â null` | Get the key that comes before the given key in the collection. |
| `getKeyAfter( (key: Key )): Key |Â null` | Get the key that comes after the given key in the collection. |
| `getFirstKey(): Key |Â null` | Get the first key in the collection. |
| `getLastKey(): Key |Â null` | Get the last key in the collection. |
| `getChildren( (key: Key )): Iterable<T>` | Iterate over the child items of the given key. |
| `getTextValue( (key: Key )): string` | Returns a string representation of the item's contents. |
| `filter( (filterFn: ( (nodeValue: string, , node: T )) => boolean )): Collection<T>` | Filters the collection using the given function. |

| Name | Type | Description |
| --- | --- | --- |
| `column` | `Key` | The key of the column to sort by. |
| `direction` | `SortDirection` | The direction to sort by. |

`'ascending' |Â 'descending'`

An interface for reading and updating multiple selection state.

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `collection` | `Collection<Node<unknown>>` |  |
| `selectionMode` | `SelectionMode` | The type of selection that is allowed in the collection. |
| `disallowEmptySelection` | `boolean` | Whether the collection allows empty selection. |
| `selectionBehavior` | `SelectionBehavior` | The selection behavior for the collection. |
| `isFocused` | `boolean` | Whether the collection is currently focused. |
| `focusedKey` | `Key |Â null` | The current focused key in the collection. |
| `childFocusStrategy` | `FocusStrategy |Â null` | Whether the first or last child of the focused key should receive focus. |
| `selectedKeys` | `Set<Key>` | The currently selected keys in the collection. |
| `rawSelection` | `Selection` | The raw selection value for the collection. Either 'all' for select all, or a set of keys. |
| `isEmpty` | `boolean` | Whether the selection is empty. |
| `isSelectAll` | `boolean` | Whether all items in the collection are selected. |
| `firstSelectedKey` | `Key |Â null` |  |
| `lastSelectedKey` | `Key |Â null` |  |
| `disabledKeys` | `Set<Key>` |  |
| `disabledBehavior` | `DisabledBehavior` |  |

### Methods

| Method | Description |
| --- | --- |
| `constructor( collection: Collection<Node<unknown>>, state: MultipleSelectionState, options?: SelectionManagerOptions ): void` |  |
| `setSelectionBehavior( (selectionBehavior: SelectionBehavior )): void` | Sets the selection behavior for the collection. |
| `setFocused( (isFocused: boolean )): void` | Sets whether the collection is focused. |
| `setFocusedKey( (key: Key |Â  |Â null, , childFocusStrategy?: FocusStrategy )): void` | Sets the focused key. |
| `isSelected( (key: Key )): boolean` | Returns whether a key is selected. |
| `extendSelection( (toKey: Key )): void` | Extends the selection to the given key. |
| `toggleSelection( (key: Key )): void` | Toggles whether the given key is selected. |
| `replaceSelection( (key: Key )): void` | Replaces the selection with only the given key. |
| `setSelectedKeys( (keys: Iterable<Key> )): void` | Replaces the selection with the given keys. |
| `selectAll(): void` | Selects all items in the collection. |
| `clearSelection(): void` | Removes all keys from the selection. |
| `toggleSelectAll(): void` | Toggles between select all and an empty selection. |
| `select( (key: Key, , e?: PressEvent |Â LongPressEvent |Â PointerEvent )): void` |  |
| `isSelectionEqual( (selection: Set<Key> )): boolean` | Returns whether the current selection is equal to the given selection. |
| `canSelectItem( (key: Key )): boolean` |  |
| `isDisabled( (key: Key )): boolean` |  |
| `isLink( (key: Key )): boolean` |  |
| `getItemProps( (key: Key )): any` |  |
| `withCollection( (collection: Collection<Node<unknown>> )): SelectionManager` |  |

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `selectionMode` | `SelectionMode` | The type of selection that is allowed in the collection. |
| `selectionBehavior` | `SelectionBehavior` | The selection behavior for the collection. |
| `disallowEmptySelection` | `boolean` | Whether the collection allows empty selection. |
| `selectedKeys` | `Selection` | The currently selected keys in the collection. |
| `disabledKeys` | `Set<Key>` | The currently disabled keys in the collection. |
| `disabledBehavior` | `DisabledBehavior` | Whether `disabledKeys` applies to selection, actions, or both. |
| `isFocused` | `boolean` | Whether the collection is currently focused. |
| `focusedKey` | `Key |Â null` | The current focused key in the collection. |
| `childFocusStrategy` | `FocusStrategy |Â null` | Whether the first or last child of the focused key should receive focus. |

### Methods

| Method | Description |
| --- | --- |
| `setSelectionBehavior( (selectionBehavior: SelectionBehavior )): void` | Sets the selection behavior for the collection. |
| `setSelectedKeys( (keys: Selection )): void` | Sets the selected keys in the collection. |
| `setFocused( (isFocused: boolean )): void` | Sets whether the collection is focused. |
| `setFocusedKey( (key: Key |Â  |Â null, , child?: FocusStrategy )): void` | Sets the focused key, and optionally, whether the first or last child of that key should receive focus. |

`'none'
|Â 'single'
|Â 'multiple'`

`'toggle' |Â 'replace'`

`'all' |Â Set<Key>`

`'selection' |Â 'all'`

`'first' |Â 'last'`

| Name | Type | Description |
| --- | --- | --- |
| `allowsCellSelection` | `boolean` |  |
| `layoutDelegate` | `LayoutDelegate` |  |

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `type` | `'pressstart' |Â 'pressend' |Â 'pressup' |Â 'press'` | The type of press event being fired. |
| `pointerType` | `PointerType` | The pointer type that triggered the press event. |
| `target` | `Element` | The target element of the press event. |
| `shiftKey` | `boolean` | Whether the shift keyboard modifier was held during the press event. |
| `ctrlKey` | `boolean` | Whether the ctrl keyboard modifier was held during the press event. |
| `metaKey` | `boolean` | Whether the meta keyboard modifier was held during the press event. |
| `altKey` | `boolean` | Whether the alt keyboard modifier was held during the press event. |
| `x` | `number` | X position relative to the target. |
| `y` | `number` | Y position relative to the target. |

### Methods

| Method | Description |
| --- | --- |
| `continuePropagation(): void` | By default, press events stop propagation to parent elements. In cases where a handler decides not to handle a specific event, it can call `continuePropagation()` to allow a parent to handle it. |

`'mouse'
|Â 'pen'
|Â 'touch'
|Â 'keyboard'
|Â 'virtual'`

| Name | Type | Description |
| --- | --- | --- |
| `type` | `'longpressstart' |Â 'longpressend' |Â 'longpress'` | The type of long press event being fired. |
| `pointerType` | `PointerType` | The pointer type that triggered the press event. |
| `target` | `Element` | The target element of the press event. |
| `shiftKey` | `boolean` | Whether the shift keyboard modifier was held during the press event. |
| `ctrlKey` | `boolean` | Whether the ctrl keyboard modifier was held during the press event. |
| `metaKey` | `boolean` | Whether the meta keyboard modifier was held during the press event. |
| `altKey` | `boolean` | Whether the alt keyboard modifier was held during the press event. |
| `x` | `number` | X position relative to the target. |
| `y` | `number` | Y position relative to the target. |

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `expandedKeys` | `'all' |Â Set<Key>` | A set of keys for items that are expanded. |
| `keyMap` | `Map<Key, GridNode<T>>` | The key map containing nodes representing the collection's tree grid structure. |
| `userColumnCount` | `number` | The number of leaf columns provided by the user. |
| `collection` | `TableCollection<T>` | A collection of rows and columns in the table. |
| `showSelectionCheckboxes` | `boolean` | Whether the row selection checkboxes should be displayed. |
| `sortDescriptor` | `SortDescriptor |Â null` | The current sorted column and direction. |
| `isKeyboardNavigationDisabled` | `boolean` | Whether keyboard navigation is disabled, such as when the arrow keys should be handled by a component within a cell. |
| `setKeyboardNavigationDisabled` | `( (val: boolean )) => void` | Set whether keyboard navigation is disabled, such as when the arrow keys should be handled by a component within a cell. |
| `disabledKeys` | `Set<Key>` | A set of keys for rows that are disabled. |
| `selectionManager` | `SelectionManager` | A selection manager to read and update row selection state. |

### Methods

| Method | Description |
| --- | --- |
| `toggleKey( (key: Key )): void` | Toggles the expanded state for a row by its key. |
| `sort( (columnKey: Key, , direction?: 'ascending' |Â  |Â 'descending' )): void` | Calls the provided onSortChange handler with the provided column key and sort direction. |

| Name | Type | Description |
| --- | --- | --- |
| `gridProps` | `DOMAttributes` | Props for the grid element. |

All DOM attributes supported across both HTML and SVG elements.

**Extends**: `AriaAttributes, ReactDOMAttributes`

| Name | Type | Description |
| --- | --- | --- |
| `id` | `string |Â undefined` |  |
| `role` | `AriaRole |Â undefined` |  |
| `tabIndex` | `number |Â undefined` |  |
| `style` | `CSSProperties |Â undefined` |  |
| `className` | `string |Â undefined` |  |

Any focusable element, including both HTML and SVG elements.

**Extends**: `Element, HTMLOrSVGElement`

| Name | Type | Description |
| --- | --- | --- |
| `rowGroupProps` | `DOMAttributes` | Props for the row group element. |

| Name | Type | Description |
| --- | --- | --- |
| `node` | `GridNode<T>` | An object representing the grid row. Contains all the relevant information that makes up the grid row. |
| `isVirtualized` | `boolean` | Whether the grid row is contained in a virtual scroller. |
| `shouldSelectOnPressUp` | `boolean` | Whether selection should occur on press up instead of press down. |

| Name | Type | Description |
| --- | --- | --- |
| `rowProps` | `DOMAttributes` | Props for the grid row element. |

| Name | Type | Description |
| --- | --- | --- |
| `node` | `GridNode<T>` | An object representing the [column header](https://www.w3.org/TR/wai-aria-1.1/#columnheader). Contains all the relevant information that makes up the column header. |
| `isVirtualized` | `boolean` | Whether the [column header](https://www.w3.org/TR/wai-aria-1.1/#columnheader) is contained in a virtual scroller. |

| Name | Type | Description |
| --- | --- | --- |
| `columnHeaderProps` | `DOMAttributes` | Props for the [column header](https://www.w3.org/TR/wai-aria-1.1/#columnheader) element. |
| `isPressed` | `boolean` | Whether the column is currently in a pressed state. |

| Name | Type | Description |
| --- | --- | --- |
| `rowProps` | `DOMAttributes` | Props for the grid row element. |
| `isPressed` | `boolean` | Whether the row is currently in a pressed state. |
| `isSelected` | `boolean` | Whether the item is currently selected. |
| `isFocused` | `boolean` | Whether the item is currently focused. |
| `isDisabled` | `boolean` | Whether the item is non-interactive, i.e. both selection and actions are disabled and the item may not be focused. Dependent on `disabledKeys` and `disabledBehavior`. |
| `allowsSelection` | `boolean` | Whether the item may be selected, dependent on `selectionMode`, `disabledKeys`, and `disabledBehavior`. |
| `hasAction` | `boolean` | Whether the item has an action, dependent on `onAction`, `disabledKeys`, and `disabledBehavior`. It may also change depending on the current selection state of the list (e.g. when selection is primary). This can be used to enable or disable hover styles or other visual indications of interactivity. |

| Name | Type | Description |
| --- | --- | --- |
| `node` | `GridNode<unknown>` | An object representing the table cell. Contains all the relevant information that makes up the row header. |
| `isVirtualized` | `boolean` | Whether the cell is contained in a virtual scroller. |
| `shouldSelectOnPressUp` | `boolean` | Whether selection should occur on press up instead of press down. |

| Name | Type | Description |
| --- | --- | --- |
| `gridCellProps` | `DOMAttributes` | Props for the table cell element. |
| `isPressed` | `boolean` | Whether the cell is currently in a pressed state. |

| Name | Type | Description |
| --- | --- | --- |
| `key` | `Key` | A unique key for the checkbox. |

| Name | Type | Description |
| --- | --- | --- |
| `checkboxProps` | `AriaCheckboxProps` | Props for the row selection checkbox element. |

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `isIndeterminate` | `boolean` | â | Indeterminism is presentational only. The indeterminate visual representation remains regardless of user interaction. |
| `children` | `ReactNode` | â | The label for the element. |
| `value` | `string` | â | The value of the input element, used when submitting an HTML form. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefvalue). |
| `defaultSelected` | `boolean` | â | Whether the element should be selected (uncontrolled). |
| `isSelected` | `boolean` | â | Whether the element should be selected (controlled). |
| `onChange` | `( (isSelected: boolean )) => void` | â | Handler that is called when the element's selection state changes. |
| `isDisabled` | `boolean` | â | Whether the input is disabled. |
| `isReadOnly` | `boolean` | â | Whether the input can be selected but not changed by the user. |
| `isRequired` | `boolean` | â | Whether user input is required on the input before form submission. |
| `isInvalid` | `boolean` | â | Whether the input value is invalid. |
| `validationBehavior` | `'aria' |Â 'native'` | `'aria'` | Whether to use native HTML form validation to prevent form submission when the value is missing or invalid, or mark the field as required or invalid via ARIA. |
| `validate` | `( (value: boolean )) => ValidationError |Â true |Â null |Â undefined` | â | A function that returns an error message if a given value is invalid. Validation errors are displayed to the user when the form is submitted if `validationBehavior="native"`. For realtime validation, use the `isInvalid` prop instead. |
| `autoFocus` | `boolean` | â | Whether the element should receive focus on render. |
| `onFocus` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | â | Handler that is called when the element's focus status changes. |
| `onKeyDown` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is pressed. |
| `onKeyUp` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is released. |
| `name` | `string` | â | The name of the input element, used when submitting an HTML form. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefname). |
| `form` | `string` | â | The `<form>` element to associate the input with. The value of this attribute must be the id of a `<form>` in the same document. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input#form). |
| `aria-controls` | `string` | â | Identifies the element (or elements) whose contents or presence are controlled by the current element. |
| `excludeFromTabOrder` | `boolean` | â | Whether to exclude the element from the sequential tab order. If true, the element will not be focusable via the keyboard by tabbing. This should be avoided except in rare scenarios where an alternative means of accessing the element or its functionality via the keyboard is available. |
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `aria-label` | `string` | â | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |
| `aria-errormessage` | `string` | â | Identifies the element that provides an error message for the object. |
| `onPress` | `( (e: PressEvent )) => void` | â | Handler that is called when the press is released over the target. |
| `onPressStart` | `( (e: PressEvent )) => void` | â | Handler that is called when a press interaction starts. |
| `onPressEnd` | `( (e: PressEvent )) => void` | â | Handler that is called when a press interaction ends, either over the target or when the pointer leaves the target. |
| `onPressChange` | `( (isPressed: boolean )) => void` | â | Handler that is called when the press state changes. |
| `onPressUp` | `( (e: PressEvent )) => void` | â | Handler that is called when a press is released over the target, regardless of whether it started on the target or not. |
| `onClick` | `( (e: MouseEvent<FocusableElement> )) => void` | â | **Not recommended â use `onPress` instead.** `onClick` is an alias for `onPress` provided for compatibility with other libraries. `onPress` provides additional event details for non-mouse interactions. |

`'valid' |Â 'invalid'`

`string |Â string[]`

`BaseEvent<ReactKeyboardEvent<any>>`

`SyntheticEvent &Â {

stopPropagation: () => void,

continuePropagation: () => void

}`

| Name | Type | Description |
| --- | --- | --- |
| `checkboxProps` | `AriaCheckboxProps` | Props for the select all checkbox element. |

| Name | Type | Description |
| --- | --- | --- |
| `column` | `GridNode<T>` | An object representing the [column header](https://www.w3.org/TR/wai-aria-1.1/#columnheader). Contains all the relevant information that makes up the column header. |
| `aria-label` | `string` | Aria label for the hidden input. Gets read when resizing. |
| `triggerRef` | `RefObject<FocusableElement |Â null>` | Ref to the trigger if resizing was started from a column header menu. If it's provided, focus will be returned there when resizing is done. If it isn't provided, it is assumed that the resizer is visible at all time and keyboard resizing is started via pressing Enter on the resizer and not on focus. |
| `isDisabled` | `boolean` | If resizing is disabled. |
| `onResizeStart` | `( (widths: Map<Key, ColumnSize> )) => void` | Called when resizing starts. |
| `onResize` | `( (widths: Map<Key, ColumnSize> )) => void` | Called for every resize event that results in new column sizes. |
| `onResizeEnd` | `( (widths: Map<Key, ColumnSize> )) => void` | Called when resizing ends. |

All possible sizes a column can be assigned.

`ColumnStaticSize |Â ColumnDynamicSize`

Widths that result in a constant pixel value for the same Table width.

`` number
|Â `${number}`
|Â `${number}%` ``

Widths that change size in relation to the remaining space and in ratio to other dynamic columns.
All numbers must be integers and greater than 0.
FR units take up remaining, if any, space in the table.

`` `${number}fr` ``

| Name | Type | Description |
| --- | --- | --- |
| `updateResizedColumns` | `( (key: Key, , width: number )) => Map<Key, ColumnSize>` | Called to update the state that a resize event has occurred. Returns the new widths for all columns based on the resized column. |
| `startResize` | `( (key: Key )) => void` | Callback for when onColumnResize has started. |
| `endResize` | `() => void` | Callback for when onColumnResize has ended. |
| `getColumnWidth` | `( (key: Key )) => number` | Gets the current width for the specified column. |
| `getColumnMinWidth` | `( (key: Key )) => number` | Gets the current minWidth for the specified column. |
| `getColumnMaxWidth` | `( (key: Key )) => number` | Gets the current maxWidth for the specified column. |
| `resizingColumn` | `Key |Â null` | Key of the currently resizing column. |
| `tableState` | `TableState<T>` | A reference to the table state. |
| `columnWidths` | `Map<Key, number>` | A map of the current column widths. |

| Name | Type | Description |
| --- | --- | --- |
| `inputProps` | `DOMAttributes` | Props for the visually hidden input element. |
| `resizerProps` | `DOMAttributes` | Props for the resizer element. |
| `isResizing` | `boolean` | Whether this column is currently being resized. |

Provides the behavior and accessibility implementation for a table component.
A table displays data in rows and columns and enables a user to navigate its contents via directional navigation keys,
and optionally supports row selection and sorting.

`useTable<T>(
props: AriaTableProps,
state: TableState<T>
|Â  |Â TreeGridState<T>,
ref: RefObject<HTMLElement
|Â  |Â null>
): GridAria`

Provides the behavior and accessibility implementation for a row in a table.

`useTableRow<T>(
props: GridRowProps<T>,
state: TableState<T>
|Â  |Â TreeGridState<T>,
ref: RefObject<FocusableElement
|Â  |Â null>
): GridRowAria`

Provides the behavior and accessibility implementation for a cell in a table.

`useTableCell<T>(
props: AriaTableCellProps,
state: TableState<T>,
ref: RefObject<FocusableElement
|Â  |Â null>
): TableCellAria`

Provides the behavior and accessibility implementation for a column header in a table.

`useTableColumnHeader<T>(
props: AriaTableColumnHeaderProps<T>,
state: TableState<T>,
ref: RefObject<FocusableElement
|Â  |Â null>
): TableColumnHeaderAria`

`useTableRowGroup(): GridRowGroupAria`

Provides the behavior and accessibility implementation for a header row in a table.

`useTableHeaderRow<T>(
props: GridRowProps<T>,
state: TableState<T>,
ref: RefObject<Element
|Â  |Â null>
): TableHeaderRowAria`

Provides the behavior and accessibility implementation for the select all checkbox in a table.

`useTableSelectAllCheckbox<T>(
(state: TableState<T>
)): TableSelectAllCheckboxAria`

Provides the behavior and accessibility implementation for a selection checkbox in a table.

`useTableSelectionCheckbox<T>(
(props: AriaTableSelectionCheckboxProps,
, state: TableState<T>
)): TableSelectionCheckboxAria`

Provides state management for a table component. Handles building a collection
of columns and rows from props. In addition, it tracks row selection and manages sort order changes.

`useTableState<T extends object>(
(props: TableStateProps<T>
)): TableState<T>`

| Name | Type | Description |
| --- | --- | --- |
| `children` | `[ ReactElement<TableHeaderProps<T>>, ReactElement<TableBodyProps<T>> ]` | The elements that make up the table. Includes the TableHeader, TableBody, Columns, and Rows. |
| `disabledKeys` | `Iterable<Key>` | A list of row keys to disable. |
| `collection` | `TableCollection<T>` | A pre-constructed collection to use instead of building one from items and children. |
| `showSelectionCheckboxes` | `boolean` | Whether the row selection checkboxes should be displayed. |
| `selectionBehavior` | `SelectionBehavior` | How multiple selection should behave in the collection. |
| `allowDuplicateSelectionEvents` | `boolean` | Whether onSelectionChange should fire even if the new set of keys is the same as the last. |
| `disabledBehavior` | `DisabledBehavior` | Whether `disabledKeys` applies to all interactions, or only selection. |
| `selectionMode` | `SelectionMode` | The type of selection that is allowed in the collection. |
| `disallowEmptySelection` | `boolean` | Whether the collection allows empty selection. |
| `selectedKeys` | `'all' |Â Iterable<Key>` | The currently selected keys in the collection (controlled). |
| `defaultSelectedKeys` | `'all' |Â Iterable<Key>` | The initial selected keys in the collection (uncontrolled). |
| `onSelectionChange` | `( (keys: Selection )) => void` | Handler that is called when the selection changes. |
| `sortDescriptor` | `SortDescriptor` | The current sorted column and direction. |
| `onSortChange` | `( (descriptor: SortDescriptor )) => any` | Handler that is called when the sorted column or direction changes. |

| Name | Type | Description |
| --- | --- | --- |
| `children` | `ColumnElement<T> |Â ColumnElement<T>[] |Â ColumnRenderer<T>` | A list of `Column(s)` or a function. If the latter, a list of columns must be provided using the `columns` prop. |
| `columns` | `T[]` | A list of table columns. |

`ReactElement<ColumnProps<T>>`

| Name | Type | Description |
| --- | --- | --- |
| `children` | `ReactNode |Â ColumnElement<T> |Â ColumnElement<T>[]` | Static child columns or content to render as the column header. |
| `title` | `ReactNode` | Rendered contents of the column if `children` contains child columns. |
| `childColumns` | `T[]` | A list of child columns used when dynamically rendering nested child columns. |
| `width` | `ColumnSize |Â null` | The width of the column. |
| `minWidth` | `ColumnStaticSize |Â null` | The minimum width of the column. |
| `maxWidth` | `ColumnStaticSize |Â null` | The maximum width of the column. |
| `defaultWidth` | `ColumnSize |Â null` | The default width of the column. |
| `allowsResizing` | `boolean` | Whether the column allows resizing. |
| `allowsSorting` | `boolean` | Whether the column allows sorting. |
| `isRowHeader` | `boolean` | Whether a column is a [row header](https://www.w3.org/TR/wai-aria-1.1/#rowheader) and should be announced by assistive technology during row navigation. |
| `textValue` | `string` | A string representation of the column's contents, used for accessibility announcements. |

`(
(item: T
)) => ColumnElement<T>`

| Name | Type | Description |
| --- | --- | --- |
| `children` | `RowElement<T> |Â RowElement<T>[] |Â ( (item: T )) => RowElement<T>` | The contents of the table body. Supports static items or a function for dynamic rendering. |
| `items` | `Iterable<T>` | A list of row objects in the table body used when dynamically rendering rows. |
| `loadingState` | `LoadingState` | The current loading state of the table. |
| `onLoadMore` | `() => any` | Handler that is called when more items should be loaded, e.g. while scrolling near the bottom. |

`ReactElement<RowProps<T>>`

| Name | Type | Description |
| --- | --- | --- |
| `children` | `CellElement |Â CellElement[] |Â CellRenderer` | Rendered contents of the row or row child items. |
| `textValue` | `string` | A string representation of the row's contents, used for features like typeahead. |
| `href` | `Href` | A URL to link to. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a#href). |
| `hrefLang` | `string` | Hints at the human language of the linked URL. See[MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a#hreflang). |
| `target` | `HTMLAttributeAnchorTarget` | The target window for the link. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a#target). |
| `rel` | `string` | The relationship between the linked resource and the current page. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/rel). |
| `download` | `boolean |Â string` | Causes the browser to download the linked URL. A string may be provided to suggest a file name. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a#download). |
| `ping` | `string` | A space-separated list of URLs to ping when the link is followed. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a#ping). |
| `referrerPolicy` | `HTMLAttributeReferrerPolicy` | How much of the referrer to send when following the link. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a#referrerpolicy). |
| `routerOptions` | `RouterOptions` | Options for the configured client side router. |

`ReactElement<CellProps>`

| Name | Type | Description |
| --- | --- | --- |
| `children` | `ReactNode` | The contents of the cell. |
| `textValue` | `string` | A string representation of the cell's contents, used for features like typeahead. |
| `colSpan` | `number` | Indicates how many columns the data cell spans. |

`(
(columnKey: Key
)) => CellElement`

`RouterConfig extends {

href: any

} ? H : string`

This type allows configuring link props with router options and type-safe URLs via TS module augmentation.
By default, this is an empty type. Extend with `href` and `routerOptions` properties to configure your router.

`RouterConfig extends {

routerOptions: any

} ? O : never`

`'loading'
|Â 'sorting'
|Â 'loadingMore'
|Â 'error'
|Â 'idle'
|Â 'filtering'`

A TableHeader is a container for the Column elements in a Table. Columns can be statically defined
as children, or generated dynamically using a function based on the data passed to the `columns` prop.

`TableHeader<T>(
(props: TableHeaderProps<T>
)): ReactElement |Â null`

A Column represents a field of each item within a Table. Columns may also contain nested
Column elements to represent column groups. Nested columns can be statically defined as
children, or dynamically generated using a function based on the `childColumns` prop.

`Column<T>(
(props: ColumnProps<T>
)): ReactElement |Â null`

A TableBody is a container for the Row elements of a Table. Rows can be statically defined
as children, or generated dynamically using a function based on the data passed to the `items` prop.

`TableBody<T>(
(props: TableBodyProps<T>
)): ReactElement |Â null`

A Row represents a single item in a Table and contains Cell elements for each column.
Cells can be statically defined as children, or generated dynamically using a function
based on the columns defined in the TableHeader.

`Row<T>(
(props: RowProps<T>
)): ReactElement |Â null`

A Cell represents the value of a single Column within a Table Row.

`Cell(
(props: CellProps
)): ReactElement |Â null`

Determines whether a focus ring should be shown to indicate keyboard focus.
Focus rings are visible only when the user is interacting with a keyboard,
not with a mouse, touch, or other input methods.

`useFocusRing(
(props: AriaFocusRingProps
)): FocusRingAria`

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `within` | `boolean` | `'false'` | Whether to show the focus ring when something inside the container element has focus (true), or only if the container itself has focus (false). |
| `isTextInput` | `boolean` | â | Whether the element is a text input. |
| `autoFocus` | `boolean` | â | Whether the element will be auto focused. |

| Name | Type | Description |
| --- | --- | --- |
| `isFocused` | `boolean` | Whether the element is currently focused. |
| `isFocusVisible` | `boolean` | Whether keyboard focus should be visible. |
| `focusProps` | `DOMAttributes` | Props to apply to the container element with the focus ring. |

A RouterProvider accepts a `navigate` function from a framework or client side router,
and provides it to all nested React Aria links to enable client side navigation.

| Name | Type | Description |
| --- | --- | --- |
| `navigate` | `( (path: Href, , routerOptions: RouterOptions |Â  |Â undefined )) => void` |  |
| `children` | `ReactNode` |  |
| `useHref` | `( (href: Href )) => string` |  |

Provides column width state management for a table component with column resizing support. Handles building
a map of column widths calculated from the table's width and any provided column width information from the collection.
In addition, it tracks the currently resizing column and provides callbacks for updating the widths upon resize operations.

`useTableColumnResizeState<T>(
(props: TableColumnResizeStateProps<T>,
, state: TableState<T>
)): TableColumnResizeState<T>`

| Name | Type | Description |
| --- | --- | --- |
| `tableWidth` | `number` | Current width of the table or table viewport that the columns should be calculated against. |
| `getDefaultWidth` | `( (node: GridNode<T> )) => ColumnSize |Â null |Â undefined` | A function that is called to find the default width for a given column. |
| `getDefaultMinWidth` | `( (node: GridNode<T> )) => ColumnSize |Â null |Â undefined` | A function that is called to find the default minWidth for a given column. |

Provides the behavior and accessibility implementation for a table column resizer element.

`useTableColumnResize<T>(
props: AriaTableColumnResizeProps<T>,
state: TableColumnResizeState<T>,
ref: RefObject<HTMLInputElement
|Â  |Â null>
): TableColumnResizeAria`