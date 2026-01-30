import { ChartData } from '../../types/analytics.types'

interface ChartPlaceholderProps {
  chart: ChartData
}

const ChartPlaceholder = ({ chart }: ChartPlaceholderProps) => {
  const getChartIcon = () => {
    switch (chart.type) {
      case 'line':
        return '📈'
      case 'bar':
        return '📊'
      case 'pie':
        return '🥧'
      case 'area':
        return '📉'
      case 'donut':
        return '🍩'
      default:
        return '📊'
    }
  }

  // Generate simple placeholder visualization
  const maxValue = Math.max(...chart.data)
  const bars = chart.data.map((value) => ({
    height: (value / maxValue) * 100,
    value
  }))

  return (
    <div
      className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm
        border border-gray-200 dark:border-gray-700 h-full"
      role="img"
      aria-label={`${chart.title} ${chart.type} chart`}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <span>{getChartIcon()}</span>
            {chart.title}
          </h3>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            {chart.type.charAt(0).toUpperCase() + chart.type.slice(1)} Chart
          </p>
        </div>
        <button 
          className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
          aria-label="Chart options menu"
        >
          <svg className="w-5 h-5 text-gray-600 dark:text-gray-400" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
            <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
          </svg>
        </button>
      </div>

      {/* Chart Visualization */}
      {chart.type === 'line' || chart.type === 'area' ? (
        <div className="relative h-64">
          {/* Grid lines */}
          <div className="absolute inset-0 flex flex-col justify-between">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="border-t border-gray-200 dark:border-gray-700" />
            ))}
          </div>

          {/* Line chart visualization */}
          <svg className="absolute inset-0 w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
            <defs>
              <linearGradient id={`gradient-${chart.id}`} x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" className="text-blue-400" stopColor="currentColor" stopOpacity="0.3" />
                <stop offset="100%" className="text-blue-400" stopColor="currentColor" stopOpacity="0.05" />
              </linearGradient>
            </defs>
            
            {chart.type === 'area' && (
              <path
                d={`M 0 ${100 - bars[0].height} ${bars.map((bar, i) => 
                  `L ${(i / (bars.length - 1)) * 100} ${100 - bar.height}`
                ).join(' ')} L 100 100 L 0 100 Z`}
                fill={`url(#gradient-${chart.id})`}
              />
            )}
            
            <polyline
              points={bars.map((bar, i) => 
                `${(i / (bars.length - 1)) * 100},${100 - bar.height}`
              ).join(' ')}
              fill="none"
              stroke="currentColor"
              className="text-blue-500"
              strokeWidth="2"
            />
            
            {bars.map((bar, i) => (
              <circle
                key={i}
                cx={(i / (bars.length - 1)) * 100}
                cy={100 - bar.height}
                r="2"
                fill="currentColor"
                className="text-blue-500"
              />
            ))}
          </svg>

          {/* Labels */}
          <div className="absolute bottom-0 left-0 right-0 flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-2">
            {chart.labels.map((label, i) => (
              <span key={i} className={i > 3 ? 'hidden md:inline' : ''}>
                {label}
              </span>
            ))}
          </div>
        </div>
      ) : chart.type === 'bar' ? (
        <div className="h-64 flex items-end justify-between gap-2">
          {bars.map((bar, i) => (
            <div key={i} className="flex-1 flex flex-col items-center gap-2">
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-t-lg overflow-hidden relative group">
                <div
                  className="bg-gradient-to-t from-blue-500 to-blue-400 transition-all duration-500 hover:from-blue-600 hover:to-blue-500"
                  style={{ height: `${bar.height * 2}px` }}
                >
                  <span className="absolute inset-0 flex items-center justify-center text-white text-xs font-semibold opacity-0 group-hover:opacity-100 transition-opacity">
                    {bar.value}
                  </span>
                </div>
              </div>
              <span className="text-xs text-gray-500 dark:text-gray-400">
                {chart.labels[i]}
              </span>
            </div>
          ))}
        </div>
      ) : (
        <div className="h-64 flex items-center justify-center">
          <div className="relative">
            {/* Pie/Donut placeholder */}
            <svg className="w-48 h-48" viewBox="0 0 100 100">
              <circle
                cx="50"
                cy="50"
                r="40"
                fill="none"
                stroke="currentColor"
                strokeWidth={chart.type === 'donut' ? '15' : '0'}
                className="text-gray-200 dark:text-gray-700"
              />
              {chart.data.map((value, i) => {
                const total = chart.data.reduce((a, b) => a + b, 0)
                const percentage = (value / total) * 100
                const angle = (percentage / 100) * 360
                const colors = ['text-blue-500', 'text-purple-500', 'text-green-500', 'text-orange-500']
                
                return (
                  <circle
                    key={i}
                    cx="50"
                    cy="50"
                    r="40"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth={chart.type === 'donut' ? '15' : '40'}
                    strokeDasharray={`${(angle / 360) * 251.2} 251.2`}
                    strokeDashoffset={-251.2 * i * 0.25}
                    className={colors[i % colors.length]}
                    transform="rotate(-90 50 50)"
                  />
                )
              })}
            </svg>
            
            {/* Legend */}
            <div className="absolute -right-24 top-0 space-y-2">
              {chart.labels.map((label, i) => {
                const colors = ['bg-blue-500', 'bg-purple-500', 'bg-green-500', 'bg-orange-500']
                return (
                  <div key={i} className="flex items-center gap-2 text-xs">
                    <div className={`w-3 h-3 rounded-full ${colors[i % colors.length]}`} />
                    <span className="text-gray-600 dark:text-gray-400">{label}</span>
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default ChartPlaceholder
