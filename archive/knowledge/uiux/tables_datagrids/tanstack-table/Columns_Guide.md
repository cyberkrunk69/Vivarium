# Columns Guide

Source: https://tanstack.com/table/latest/docs/guide/columns

---

[## API](#api)

[Column API](/table/latest/docs/api/core/column)

[## Columns Guide](#columns-guide)
> Note: This guide is about the actual column objects that are generated within the table instance and NOT about setting up the [column definitions](/table/latest/docs/guide/column-defs) for your table.

This quick guide will discuss the different ways you can retrieve and interact with column objects in TanStack Table.

[### Where to Get Columns From](#where-to-get-columns-from)

You can find the column objects in many places. They are often attached

[#### Header and Cell Objects](#header-and-cell-objects)

Before you reach for one of the table instance APIs, consider if you actually need to retrieve either [headers](/table/latest/docs/guide/headers) or [cells](/table/latest/docs/guide/cells) instead of columns. If you are rending out the markup for your table, you will most likely want to reach for the APIs that return headers or cells instead of columns. The column objects themselves are not really meant to render out the headers or cells, but the header and cell objects will contain references to these column objects from which they can derive the necessary information to render their UI.

js

```
const column = cell.column; // get column from cell
const column = header.column; // get column from header
```

[#### Column Table Instance APIs](#column-table-instance-apis)

There are dozens of table instance APIs you can use to retrieve columns from the table instance. Which APIs you will use will depend entirely on which features you are using in your table and your use-case.

[##### Get Column](#get-column)

If you need to just get a single column by its ID, you can use the table.getColumn API.

js

```
const column = table.getColumn('firstName');
```

[##### Get Columns](#get-columns)

The simplest column API is table.getAllColumns, which will return a list of all columns in the table. There are dozens of other column APIs that are affected by other features and the state of the table that come alongside this API though. table.getAllFlatColumns, table.getAllLeafColumns, getCenterLeafColumns, table.getLeftVisibleLeafColumns are just some examples of other column APIs that you might use in tandem with the column visibility or column pinning features.

[### Column Objects](#column-objects)

Column objects are not actually meant to be used to render out the table UI directly, so they are not associated 1-to-1 with any <th> or <td> elements in your table, but they contain a lot of useful properties and methods that you can use to interact with the table state.

[#### Column IDs](#column-ids)

Every column must have a unique id defined in their associated [Column Definition](/table/latest/docs/guide/column-defs). Usually, you define this id yourself, or it is derived from the accessorKey or header properties in the column definition.

[#### ColumnDef](#columndef)

A reference to the original columnDef object that was used to created the column is always available on the column object.

[#### Nested Grouped Columns Properties](#nested-grouped-columns-properties)

There are a few properties on column objects that are only useful if the column is part of a nested or grouped column structure. These properties include:

- columns: An array of child columns that belong to a group column.
- depth: The header group "row index" that the column group belongs to.
- parent: The parent column of the column. If the column is a top-level column, this will be undefined.

[### More Column APIs](#more-column-apis)

There are dozens of Column APIs that you can use to interact with the table state and extract cell values from the table based on the state of the table. See each features column API documentation for more information.

[### Column Rendering](#column-rendering)

Don't necessarily use column objects to render headers or cells directly. Instead, use the [header](/table/latest/docs/guide/headers) and [cell](/table/latest/docs/guide/cells) objects, as discussed above.

But if you are just rendering a list of columns somewhere else in your UI for something like a column visibility menu or something similar, you can just map over a columns array and render out the UI as you normally would.