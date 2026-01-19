import { ProgressChartProps } from '../../types/project'

const ProgressChart = ({ progressData, priorityData, performanceMetrics }: ProgressChartProps) => {
  return (
    <div className="lg:col-span-2 space-y-6">
      {/* Task Progress Chart */}
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <span className="text-2xl">📊</span>
            Task Progress Overview
          </h2>
          <select className="px-3 py-1.5 border border-gray-300 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white">
            <option>This Week</option>
            <option>This Month</option>
            <option>This Quarter</option>
          </select>
        </div>

        {/* Progress Bars */}
        <div className="space-y-4">
          {progressData.map((item, index) => (
            <div key={index}>
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <div className={`w-3 h-3 rounded-full ${item.color}`}></div>
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {item.label}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-sm font-bold text-gray-900 dark:text-white">
                    {item.count}
                  </span>
                  <span className="text-xs text-gray-500 dark:text-gray-400">
                    ({item.percentage.toFixed(0)}%)
                  </span>
                </div>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
                <div 
                  className={`${item.color} h-3 rounded-full transition-all duration-500 relative overflow-hidden`}
                  style={{ width: `${item.percentage}%` }}
                >
                  <div className="absolute inset-0 bg-white/20 animate-pulse"></div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Visual Chart */}
        <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
          <div className="flex items-end justify-between gap-2 h-40">
            {progressData.map((item, index) => (
              <div key={index} className="flex-1 flex flex-col items-center gap-2">
                <div className="w-full flex items-end justify-center" style={{ height: '100%' }}>
                  <div 
                    className={`w-full ${item.color} rounded-t-lg transition-all duration-500 hover:opacity-80 cursor-pointer relative group`}
                    style={{ height: `${item.percentage}%`, minHeight: '20px' }}
                  >
                    <div className="absolute inset-0 flex items-center justify-center text-white font-bold text-sm">
                      {item.count}
                    </div>
                  </div>
                </div>
                <div className="text-xs font-medium text-gray-600 dark:text-gray-400 text-center">
                  {item.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Priority Breakdown */}
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2 mb-6">
          <span className="text-2xl">🎯</span>
          Priority Breakdown
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {priorityData.map((item, index) => (
            <div key={index} className={`${item.color} rounded-lg p-4 text-center`}>
              <div className="text-3xl font-bold mb-1">{item.count}</div>
              <div className="text-sm font-medium">{item.label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Team Performance Stats */}
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2 mb-6">
          <span className="text-2xl">📈</span>
          Team Performance
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="w-20 h-20 mx-auto mb-3 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center">
              <span className="text-3xl font-bold text-green-600 dark:text-green-400">
                {performanceMetrics.productivity}%
              </span>
            </div>
            <div className="text-sm font-semibold text-gray-900 dark:text-white">Productivity</div>
            <div className="text-xs text-gray-500 dark:text-gray-400">Above target</div>
          </div>
          <div className="text-center">
            <div className="w-20 h-20 mx-auto mb-3 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
              <span className="text-3xl font-bold text-blue-600 dark:text-blue-400">
                {performanceMetrics.completionRate}%
              </span>
            </div>
            <div className="text-sm font-semibold text-gray-900 dark:text-white">Completion Rate</div>
            <div className="text-xs text-gray-500 dark:text-gray-400">This week</div>
          </div>
          <div className="text-center">
            <div className="w-20 h-20 mx-auto mb-3 rounded-full bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center">
              <span className="text-3xl font-bold text-purple-600 dark:text-purple-400">
                {performanceMetrics.tasksDone}
              </span>
            </div>
            <div className="text-sm font-semibold text-gray-900 dark:text-white">Tasks Done</div>
            <div className="text-xs text-gray-500 dark:text-gray-400">This week</div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ProgressChart
