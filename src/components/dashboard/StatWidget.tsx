interface StatWidgetProps {
  title: string
  value: string | number
  icon: string
  trend?: {
    value: number
    isPositive: boolean
  }
  subtitle?: string
  color?: 'blue' | 'green' | 'purple' | 'orange'
}

const StatWidget = ({ title, value, icon, trend, subtitle, color = 'blue' }: StatWidgetProps) => {
  const iconBgColors = {
    blue: 'bg-blue-100 dark:bg-blue-900/30',
    green: 'bg-green-100 dark:bg-green-900/30',
    purple: 'bg-purple-100 dark:bg-purple-900/30',
    orange: 'bg-orange-100 dark:bg-orange-900/30'
  }

  return (
    <div
      className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm hover:shadow-md 
        border border-gray-200 dark:border-gray-700 transition-all duration-200 
        hover:-translate-y-0.5"
      role="article"
      aria-label={`${title}: ${value}`}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">
            {title}
          </p>
          <p className="text-3xl font-bold text-gray-900 dark:text-white mb-1">
            {value}
          </p>
          {subtitle && (
            <p className="text-xs text-gray-500 dark:text-gray-400">
              {subtitle}
            </p>
          )}
          {trend && (
            <div className={`inline-flex items-center gap-1 mt-2 text-xs font-semibold ${
              trend.isPositive 
                ? 'text-green-600 dark:text-green-400' 
                : 'text-red-600 dark:text-red-400'
            }`}>
              <svg className={`w-4 h-4 ${trend.isPositive ? '' : 'rotate-180'}`} fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clipRule="evenodd" />
              </svg>
              <span>{Math.abs(trend.value)}%</span>
              <span className="text-gray-500 dark:text-gray-400 font-normal">vs last week</span>
            </div>
          )}
        </div>

        {/* Icon */}
        <div className={`${iconBgColors[color]} p-3 rounded-lg`}>
          <span className="text-2xl">{icon}</span>
        </div>
      </div>
    </div>
  )
}

export default StatWidget
