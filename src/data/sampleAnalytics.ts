import { KPI, ChartData, TableRow, TableColumn } from '../types/analytics.types'

export const sampleKPIs: KPI[] = [
  {
    id: '1',
    title: 'Total Revenue',
    value: '$45,231',
    change: 12.5,
    changeType: 'increase',
    icon: '💰',
    color: 'blue'
  },
  {
    id: '2',
    title: 'Active Users',
    value: '8,234',
    change: 8.3,
    changeType: 'increase',
    icon: '👥',
    color: 'green'
  },
  {
    id: '3',
    title: 'Conversion Rate',
    value: '3.42%',
    change: 2.1,
    changeType: 'decrease',
    icon: '📈',
    color: 'purple'
  },
  {
    id: '4',
    title: 'Avg. Order Value',
    value: '$127.50',
    change: 5.7,
    changeType: 'increase',
    icon: '💳',
    color: 'orange'
  }
]

export const sampleCharts: ChartData[] = [
  {
    id: 'revenue-chart',
    title: 'Revenue Over Time',
    type: 'area',
    data: [25, 32, 28, 45, 52, 48, 65, 70, 68, 82, 88, 95],
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  },
  {
    id: 'users-chart',
    title: 'User Growth',
    type: 'line',
    data: [150, 180, 210, 245, 280, 320, 365, 410, 445, 490, 535, 580],
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  },
  {
    id: 'sales-chart',
    title: 'Sales by Category',
    type: 'bar',
    data: [450, 320, 280, 150],
    labels: ['Electronics', 'Clothing', 'Food', 'Other']
  },
  {
    id: 'traffic-chart',
    title: 'Traffic Sources',
    type: 'donut',
    data: [45, 25, 15, 15],
    labels: ['Organic', 'Direct', 'Social', 'Referral']
  }
]

export const tableColumns: TableColumn[] = [
  { key: 'product', label: 'Product', sortable: true, width: '30%' },
  { key: 'category', label: 'Category', sortable: true },
  { key: 'sales', label: 'Sales', sortable: true },
  { key: 'revenue', label: 'Revenue', sortable: true },
  { key: 'status', label: 'Status', sortable: true }
]

export const tableData: TableRow[] = [
  {
    id: '1',
    product: 'Wireless Headphones',
    category: 'Electronics',
    sales: 245,
    revenue: '$61,225',
    status: true
  },
  {
    id: '2',
    product: 'Smart Watch Pro',
    category: 'Electronics',
    sales: 189,
    revenue: '$75,600',
    status: true
  },
  {
    id: '3',
    product: 'Running Shoes',
    category: 'Footwear',
    sales: 156,
    revenue: '$20,280',
    status: true
  },
  {
    id: '4',
    product: 'Leather Backpack',
    category: 'Accessories',
    sales: 134,
    revenue: '$25,460',
    status: false
  },
  {
    id: '5',
    product: 'Desk Lamp',
    category: 'Home',
    sales: 98,
    revenue: '$5,880',
    status: true
  },
  {
    id: '6',
    product: 'Bluetooth Speaker',
    category: 'Electronics',
    sales: 87,
    revenue: '$6,960',
    status: true
  },
  {
    id: '7',
    product: 'Organic T-Shirt',
    category: 'Clothing',
    sales: 76,
    revenue: '$2,280',
    status: false
  },
  {
    id: '8',
    product: 'Water Bottle',
    category: 'Home',
    sales: 65,
    revenue: '$2,275',
    status: true
  },
  {
    id: '9',
    product: 'Wireless Charger',
    category: 'Electronics',
    sales: 54,
    revenue: '$2,160',
    status: true
  },
  {
    id: '10',
    product: 'Yoga Mat',
    category: 'Fitness',
    sales: 45,
    revenue: '$2,250',
    status: true
  }
]
