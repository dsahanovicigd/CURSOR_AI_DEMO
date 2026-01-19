import { KPI } from '../../types/analytics.types'

interface KPICardProps {
  kpi: KPI
}

const KPICard = ({ kpi }: KPICardProps) => {
  const colorClasses = {
    blue: {
      bg: 'from-blue-500 to-blue-600',
      icon: 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400',
      change: 'text-blue-600 dark:text-blue-400'
    },
    green: {
      bg: 'from-green-500 to-green-600',
      icon: 'bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400',
      change: 'text-green-600 dark:text-green-400'
    },
    purple: {
      bg: 'from-purple-500 to-purple-600',
      icon: 'bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400',
      change: 'text-purple-600 dark:text-purple-400'
    },
    orange: {
      bg: 'from-orange-500 to-orange-600',
      icon: 'bg-orange-100 dark:bg-orange-900/30 text-orange-600 dark:text-orange-400',
      change: 'text-orange-600 dark:text-orange-400'
    },
    red: {
      bg: 'from-red-500 to-red-600',
      icon: 'bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400',
      change: 'text-red-600 dark:text-red-400'
    }
  }

  const colors = colorClasses[kpi.color]

  return (
    <div
      className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm hover:shadow-md
        border border-gray-200 dark:border-gray-700 transition-all duration-200
        hover:-translate-y-0.5 group"
      role="article"
      aria-label={`${kpi.title}: ${kpi.value}`}
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">
            {kpi.title}
          </p>
          <p className="text-3xl font-bold text-gray-900 dark:text-white">
            {kpi.value}
          </p>
        </div>
        <div className={`${colors.icon} p-3 rounded-lg transition-transform group-hover:scale-110`}>
          <span className="text-2xl">{kpi.icon}</span>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <div className={`flex items-center gap-1 px-2 py-1 rounded-md ${
          kpi.changeType === 'increase'
            ? 'bg-green-100 dark:bg-green-900/30'
            : 'bg-red-100 dark:bg-red-900/30'
        }`}>
          <svg
            className={`w-4 h-4 ${
              kpi.changeType === 'increase'
                ? 'text-green-600 dark:text-green-400'
                : 'text-red-600 dark:text-red-400 rotate-180'
            }`}
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fillRule="evenodd"
              d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z"
              clipRule="evenodd"
            />
          </svg>
          <span className={`text-sm font-semibold ${
            kpi.changeType === 'increase'
              ? 'text-green-600 dark:text-green-400'
              : 'text-red-600 dark:text-red-400'
          }`}>
            {Math.abs(kpi.change)}%
          </span>
        </div>
        <span className="text-sm text-gray-500 dark:text-gray-400">
          vs last period
        </span>
      </div>
    </div>
  )
}

export default KPICard
