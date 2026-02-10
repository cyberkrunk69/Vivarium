# Table

Source: https://tremor.so/docs/ui/table

---

UI

# Table

Display data efficiently in a column and row format.

[GitHub](https://github.com/tremorlabs/tremor/tree/main/src/components/Table)

Preview

Code

Recent invoices.

| Name | Sales ($) | Region | Status | Working Hours (h) |
| --- | --- | --- | --- | --- |
| Peter McCrown | 1,000,000 | Region A | overperforming | 100 |
| Jon Mueller | 2,202,000 | Region B | overperforming | 110 |
| Peter Federer | 1,505,000 | Region C | underperforming | 90 |
| Maxime Bujet | 500,000 | Region D | overperforming | 92 |
| Emma Nelly | 600,000 | Region E | underperforming | 95 |
| 4,642 | | 497 | | |
| --- | --- | --- | --- | --- |

```
import {  Table,  TableBody,  TableCaption,  TableCell,  TableFoot,  TableHead,  TableHeaderCell,  TableRoot,  TableRow,} from "@/components/Table"
export function TableHero() {  const data: Array<{    id: number    name: string    sales: string    region: string    status: string    deltaType: string    hours: number  }> = [    {      id: 1,      name: "Peter McCrown",      sales: "1,000,000",      region: "Region A",      status: "overperforming",      deltaType: "moderateIncrease",      hours: 100,    },    {      id: 2,      name: "Jon Mueller",      sales: "2,202,000",      region: "Region B",      status: "overperforming",      deltaType: "moderateIncrease",      hours: 110,    },    {      id: 3,      name: "Peter Federer",      sales: "1,505,000",      region: "Region C",      status: "underperforming",      deltaType: "moderateDecrease",      hours: 90,    },    {      id: 4,      name: "Maxime Bujet",      sales: "500,000",      region: "Region D",      status: "overperforming",      deltaType: "moderateDecrease",      hours: 92,    },    {      id: 5,      name: "Emma Nelly",      sales: "600,000",      region: "Region E",      status: "underperforming",      deltaType: "moderateDecrease",      hours: 95,    },  ]  return (    <TableRoot>      <Table>        <TableCaption>Recent invoices.</TableCaption>        <TableHead>          <TableRow>            <TableHeaderCell>Name</TableHeaderCell>            <TableHeaderCell>Sales ($)</TableHeaderCell>            <TableHeaderCell>Region</TableHeaderCell>            <TableHeaderCell>Status</TableHeaderCell>            <TableHeaderCell className="text-right">              Working Hours (h)            </TableHeaderCell>          </TableRow>        </TableHead>        <TableBody>          {data.map((item) => (            <TableRow key={item.id}>              <TableCell>{item.name}</TableCell>              <TableCell className="text-right">{item.sales}</TableCell>              <TableCell>{item.region}</TableCell>              <TableCell>{item.status}</TableCell>              <TableCell className="text-right">{item.hours}</TableCell>            </TableRow>          ))}        </TableBody>        <TableFoot>          <TableRow>            <TableHeaderCell colSpan={2} scope="row" className="text-right">              4,642            </TableHeaderCell>            <TableHeaderCell colSpan={3} scope="row" className="text-right">              497            </TableHeaderCell>          </TableRow>        </TableFoot>      </Table>    </TableRoot>  )}
```

## Installation

1. 1

   ### Add component:

   Copy and paste the code into your project’s component directory. Do not forget to update the import paths.

   Show more

   ```
   // Tremor Table [v1.0.0]
   import React from "react"
   import { cx } from "@/lib/utils"
   const TableRoot = React.forwardRef<  HTMLDivElement,  React.HTMLAttributes<HTMLDivElement>>(({ className, children, ...props }, forwardedRef) => (  <div    ref={forwardedRef}    // Activate if table is used in a float environment    // className="flow-root"  >    <div      // make table scrollable on mobile      className={cx("w-full overflow-auto whitespace-nowrap", className)}      {...props}    >      {children}    </div>  </div>))
   TableRoot.displayName = "TableRoot"
   const Table = React.forwardRef<  HTMLTableElement,  React.TableHTMLAttributes<HTMLTableElement>>(({ className, ...props }, forwardedRef) => (  <table    ref={forwardedRef}    tremor-id="tremor-raw"    className={cx(      // base      "w-full caption-bottom border-b",      // border color      "border-gray-200 dark:border-gray-800",      className,    )}    {...props}  />))
   Table.displayName = "Table"
   const TableHead = React.forwardRef<  HTMLTableSectionElement,  React.HTMLAttributes<HTMLTableSectionElement>>(({ className, ...props }, forwardedRef) => (  <thead ref={forwardedRef} className={cx(className)} {...props} />))
   TableHead.displayName = "TableHead"
   const TableHeaderCell = React.forwardRef<  HTMLTableCellElement,  React.ThHTMLAttributes<HTMLTableCellElement>>(({ className, ...props }, forwardedRef) => (  <th    ref={forwardedRef}    className={cx(      // base      "border-b px-4 py-3.5 text-left text-sm font-semibold",      // text color      "text-gray-900 dark:text-gray-50",      // border color      "border-gray-200 dark:border-gray-800",      className,    )}    {...props}  />))
   TableHeaderCell.displayName = "TableHeaderCell"
   const TableBody = React.forwardRef<  HTMLTableSectionElement,  React.HTMLAttributes<HTMLTableSectionElement>>(({ className, ...props }, forwardedRef) => (  <tbody    ref={forwardedRef}    className={cx(      // base      "divide-y",      // divide color      "divide-gray-200 dark:divide-gray-800",      className,    )}    {...props}  />))
   TableBody.displayName = "TableBody"
   const TableRow = React.forwardRef<  HTMLTableRowElement,  React.HTMLAttributes<HTMLTableRowElement>>(({ className, ...props }, forwardedRef) => (  <tr    ref={forwardedRef}    className={cx(      "[&_td:last-child]:pr-4 [&_th:last-child]:pr-4",      "[&_td:first-child]:pl-4 [&_th:first-child]:pl-4",      className,    )}    {...props}  />))
   TableRow.displayName = "TableRow"
   const TableCell = React.forwardRef<  HTMLTableCellElement,  React.TdHTMLAttributes<HTMLTableCellElement>>(({ className, ...props }, forwardedRef) => (  <td    ref={forwardedRef}    className={cx(      // base      "p-4 text-sm",      // text color      "text-gray-600 dark:text-gray-400",      className,    )}    {...props}  />))
   TableCell.displayName = "TableCell"
   const TableFoot = React.forwardRef<  HTMLTableSectionElement,  React.HTMLAttributes<HTMLTableSectionElement>>(({ className, ...props }, forwardedRef) => {  return (    <tfoot      ref={forwardedRef}      className={cx(        // base        "border-t text-left font-medium",        // text color        "text-gray-900 dark:text-gray-50",        // border color        "border-gray-200 dark:border-gray-800",        className,      )}      {...props}    />  )})
   TableFoot.displayName = "TableFoot"
   const TableCaption = React.forwardRef<  HTMLTableCaptionElement,  React.HTMLAttributes<HTMLTableCaptionElement>>(({ className, ...props }, forwardedRef) => (  <caption    ref={forwardedRef}    className={cx(      // base      "mt-3 px-3 text-center text-sm",      // text color      "text-gray-500 dark:text-gray-500",      className,    )}    {...props}  />))
   TableCaption.displayName = "TableCaption"
   export {  Table,  TableBody,  TableCaption,  TableCell,  TableFoot,  TableHead,  TableHeaderCell,  TableRoot,  TableRow,}
   ```

## Example: Table with Badges

Preview

Code

### Workspaces

Overview of all registered workspaces within your organization.

| Workspace | Owner | Status | Region | Capacity | Costs | Last edited |
| --- | --- | --- | --- | --- | --- | --- |
| sales\_by\_day\_api | John Doe | Live | US-West 1 | 99% | $3,509.00 | 23/09/2023 13:00 |
| marketing\_campaign | Jane Smith | Live | US-East 2 | 80% | $5,720.00 | 22/09/2023 10:45 |
| test\_environment | David Clark | Inactive | EU-Central 1 | 40% | $800.00 | 25/09/2023 16:20 |
| sales\_campaign | Jane Smith | Live | US-East 2 | 80% | $5,720.00 | 22/09/2023 10:45 |
| development\_env | Mike Johnson | Inactive | EU-West 1 | 60% | $4,200.00 | 21/09/2023 14:30 |
| new\_workspace\_1 | Alice Brown | Inactive | US-West 2 | 75% | $2,100.00 | 24/09/2023 09:15 |

```
import { Badge } from "@/components/Badge"import {  Table,  TableBody,  TableCell,  TableHead,  TableHeaderCell,  TableRoot,  TableRow,} from "@/components/Table"
export function TableExample() {  const data: Array<{    workspace: string    owner: string    status: string    costs: string    region: string    capacity: string    lastEdited: string  }> = [    {      workspace: "sales_by_day_api",      owner: "John Doe",      status: "Live",      costs: "$3,509.00",      region: "US-West 1",      capacity: "99%",      lastEdited: "23/09/2023 13:00",    },    {      workspace: "marketing_campaign",      owner: "Jane Smith",      status: "Live",      costs: "$5,720.00",      region: "US-East 2",      capacity: "80%",      lastEdited: "22/09/2023 10:45",    },    {      workspace: "test_environment",      owner: "David Clark",      status: "Inactive",      costs: "$800.00",      region: "EU-Central 1",      capacity: "40%",      lastEdited: "25/09/2023 16:20",    },    {      workspace: "sales_campaign",      owner: "Jane Smith",      status: "Live",      costs: "$5,720.00",      region: "US-East 2",      capacity: "80%",      lastEdited: "22/09/2023 10:45",    },    {      workspace: "development_env",      owner: "Mike Johnson",      status: "Inactive",      costs: "$4,200.00",      region: "EU-West 1",      capacity: "60%",      lastEdited: "21/09/2023 14:30",    },    {      workspace: "new_workspace_1",      owner: "Alice Brown",      status: "Inactive",      costs: "$2,100.00",      region: "US-West 2",      capacity: "75%",      lastEdited: "24/09/2023 09:15",    },  ]
  return (    <>      <div>        <h3 className="font-semibold text-gray-900 dark:text-gray-50">          Workspaces        </h3>        <p className="mt-1 text-sm leading-6 text-gray-600 dark:text-gray-400">          Overview of all registered workspaces within your organization.        </p>      </div>      <TableRoot className="mt-8">        <Table>          <TableHead>            <TableRow>              <TableHeaderCell>Workspace</TableHeaderCell>              <TableHeaderCell>Owner</TableHeaderCell>              <TableHeaderCell>Status</TableHeaderCell>              <TableHeaderCell>Region</TableHeaderCell>              <TableHeaderCell>Capacity</TableHeaderCell>              <TableHeaderCell className="text-right">Costs</TableHeaderCell>              <TableHeaderCell className="text-right">                Last edited              </TableHeaderCell>            </TableRow>          </TableHead>          <TableBody>            {data.map((item) => (              <TableRow key={item.workspace}>                <TableCell >{item.workspace}</TableCell>                <TableCell>{item.owner}</TableCell>                <TableCell>                  <Badge                    variant={item.status === "Inactive" ? "warning" : "default"}                  >                    {item.status}                  </Badge>                </TableCell>                <TableCell>{item.region}</TableCell>                <TableCell>{item.capacity}</TableCell>                <TableCell className="text-right">{item.costs}</TableCell>                <TableCell className="text-right">{item.lastEdited}</TableCell>              </TableRow>            ))}          </TableBody>        </Table>      </TableRoot>    </>  )}
```

## API Reference: TableRoot

This component is based on the div element and supports all of its props.

## API Reference: Table

This component is based on the table element and supports all of its props.

## API Reference: TableHead

This component is based on the thead element and supports all of its props.

## API Reference: TableBody

This component is based on the tbody element and supports all of its props.

## API Reference: TableRow

This component is based on the tr element and supports all of its props.

## API Reference: TableCell

This component is based on the td element and supports all of its props.

## API Reference: TableHeaderCell

This component is based on the th element and supports all of its props.

## API Reference: TableFoot

This component is based on the tfoot element and supports all of its props.

## API Reference: TableCaption

This component is based on the caption element and supports all of its props.