import { useState } from 'react'
import { useDarkMode } from '../hooks/useDarkMode'
import KPICard from '../components/analytics/KPICard'
import ChartPlaceholder from '../components/analytics/ChartPlaceholder'
import DataTable from '../components/analytics/DataTable'
import FilterControls from '../components/analytics/FilterControls'
import { AnalyticsFilters } from '../types/analytics.types'
import { sampleKPIs, sampleCharts, tableData, tableColumns } from '../data/sampleAnalytics'

const AnalyticsDashboard = () => {
  const { isDarkMode, toggleDarkMode } = useDarkMode()
  
  const today = new Date().toISOString().split('T')[0]
  const lastMonth = new Date()
  lastMonth.setMonth(lastMonth.getMonth() - 1)
  
  const [filters, setFilters] = useState<AnalyticsFilters>({
    dateRange: {
      startDate: lastMonth.toISOString().split('T')[0],
      endDate: today
    }
  })

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 sticky top-0 z-30">
        <div className="px-4 lg:px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white">
                Analytics Dashboard
              </h1>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                Track your business metrics and performance
              </p>
            </div>

            <div className="flex items-center gap-3">
              {/* Dark Mode Toggle */}
              <button
                onClick={toggleDarkMode}
                className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                aria-label={isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'}
              >
                {isDarkMode ? (
                  <svg className="w-6 h-6 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clipRule="evenodd" />
                  </svg>
                ) : (
                  <svg className="w-6 h-6 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
                  </svg>
                )}
              </button>

              {/* Export Button */}
              <button className="hidden md:flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                <span>Export Report</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="p-4 lg:p-6 max-w-[1920px] mx-auto">
        <div className="space-y-6">
          {/* KPI Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6">
            {sampleKPIs.map((kpi) => (
              <KPICard key={kpi.id} kpi={kpi} />
            ))}
          </div>

          {/* Filters and Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            {/* Filters - Left Sidebar */}
            <div className="lg:col-span-1">
              <FilterControls
                filters={filters}
                onFiltersChange={setFilters}
              />
            </div>

            {/* Charts - Right Content */}
            <div className="lg:col-span-3 space-y-6">
              {/* Top Charts */}
              <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                <ChartPlaceholder chart={sampleCharts[0]} />
                <ChartPlaceholder chart={sampleCharts[1]} />
              </div>

              {/* Bottom Charts */}
              <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                <ChartPlaceholder chart={sampleCharts[2]} />
                <ChartPlaceholder chart={sampleCharts[3]} />
              </div>
            </div>
          </div>

          {/* Data Table */}
          <DataTable
            columns={tableColumns}
            data={tableData}
            title="Top Products Performance"
          />

          {/* Additional Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-3 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
                  <span className="text-2xl">📊</span>
                </div>
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Total Transactions</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">1,234</p>
                </div>
              </div>
              <div className="text-sm text-gray-500 dark:text-gray-400">
                <span className="text-green-600 dark:text-green-400 font-semibold">+15.3%</span> from last month
              </div>
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-3 bg-green-100 dark:bg-green-900/30 rounded-lg">
                  <span className="text-2xl">⏱️</span>
                </div>
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Avg. Response Time</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">2.3s</p>
                </div>
              </div>
              <div className="text-sm text-gray-500 dark:text-gray-400">
                <span className="text-green-600 dark:text-green-400 font-semibold">-12.5%</span> improvement
              </div>
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-3 bg-purple-100 dark:bg-purple-900/30 rounded-lg">
                  <span className="text-2xl">⭐</span>
                </div>
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Customer Satisfaction</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">4.8/5.0</p>
                </div>
              </div>
              <div className="text-sm text-gray-500 dark:text-gray-400">
                <span className="text-green-600 dark:text-green-400 font-semibold">+0.3</span> points increase
              </div>
            </div>
          </div>

          {/* Info Card */}
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-6 md:p-8 text-white">
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
              <div>
                <h3 className="text-2xl font-bold mb-2">Need more insights?</h3>
                <p className="text-blue-100">
                  Upgrade to Pro to unlock advanced analytics, custom reports, and more data visualizations.
                </p>
              </div>
              <button className="px-6 py-3 bg-white text-blue-600 font-semibold rounded-lg hover:bg-blue-50 transition-colors shadow-lg whitespace-nowrap">
                Upgrade Now
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default AnalyticsDashboard
