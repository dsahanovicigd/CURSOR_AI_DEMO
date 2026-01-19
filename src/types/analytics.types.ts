export interface KPI {
  id: string
  title: string
  value: string | number
  change: number
  changeType: 'increase' | 'decrease'
  icon: string
  color: 'blue' | 'green' | 'purple' | 'orange' | 'red'
}

export interface ChartData {
  id: string
  title: string
  type: 'line' | 'bar' | 'pie' | 'area' | 'donut'
  data: number[]
  labels: string[]
  color?: string
}

export interface TableRow {
  id: string
  [key: string]: string | number | boolean
}

export interface TableColumn {
  key: string
  label: string
  sortable?: boolean
  width?: string
}

export interface DateRange {
  startDate: string
  endDate: string
}

export type FilterOption = {
  value: string
  label: string
}

export interface AnalyticsFilters {
  dateRange: DateRange
  category?: string
  status?: string
  region?: string
}
