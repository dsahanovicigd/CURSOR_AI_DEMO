import { Task } from '../../types/task.types'

interface TaskCardProps {
  task: Task
  onStatusChange?: (taskId: string, newStatus: Task['status']) => void
  onDelete?: (taskId: string) => void
}

const TaskCard = ({ task, onStatusChange, onDelete }: TaskCardProps) => {
  const priorityColors = {
    low: 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300',
    medium: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400',
    high: 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400',
    urgent: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
  }

  const statusColors = {
    'todo': 'bg-gray-500',
    'in-progress': 'bg-blue-500',
    'review': 'bg-purple-500',
    'completed': 'bg-green-500'
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
  }

  const isOverdue = task.dueDate && new Date(task.dueDate) < new Date() && task.status !== 'completed'

  return (
    <article
      className="bg-white dark:bg-gray-800 rounded-xl p-5 shadow-sm hover:shadow-md
        border border-gray-200 dark:border-gray-700 transition-all duration-200
        group hover:-translate-y-0.5"
      role="article"
      aria-label={`Task: ${task.title}`}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1 min-w-0">
          <h3 className="text-base font-semibold text-gray-900 dark:text-white mb-1 line-clamp-1">
            {task.title}
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
            {task.description}
          </p>
        </div>
        
        {/* Actions Menu */}
        <div className="ml-3 flex gap-1">
          <button
            className="p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors opacity-0 group-hover:opacity-100"
            aria-label="More options"
          >
            <svg className="w-4 h-4 text-gray-500 dark:text-gray-400" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
            </svg>
          </button>
        </div>
      </div>

      {/* Tags */}
      {task.tags && task.tags.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-3">
          {task.tags.slice(0, 3).map((tag, index) => (
            <span
              key={index}
              className="px-2 py-1 text-xs font-medium bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-md"
            >
              {tag}
            </span>
          ))}
          {task.tags.length > 3 && (
            <span className="px-2 py-1 text-xs font-medium text-gray-500 dark:text-gray-400">
              +{task.tags.length - 3}
            </span>
          )}
        </div>
      )}

      {/* Progress Bar */}
      {task.progress !== undefined && (
        <div className="mb-3">
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs font-medium text-gray-600 dark:text-gray-400">
              Progress
            </span>
            <span className="text-xs font-semibold text-gray-900 dark:text-white">
              {task.progress}%
            </span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div
              className={`${statusColors[task.status]} h-2 rounded-full transition-all duration-300`}
              style={{ width: `${task.progress}%` }}
              role="progressbar"
              aria-valuenow={task.progress}
              aria-valuemin={0}
              aria-valuemax={100}
            />
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="flex items-center justify-between pt-3 border-t border-gray-100 dark:border-gray-700">
        {/* Left side - Assignee and Priority */}
        <div className="flex items-center gap-3">
          {task.assignee ? (
            <div className="flex items-center gap-2">
              <img
                src={task.assignee.avatar}
                alt={task.assignee.name}
                className="w-6 h-6 rounded-full object-cover border-2 border-white dark:border-gray-800"
              />
              <span className="text-xs text-gray-600 dark:text-gray-400">
                {task.assignee.name.split(' ')[0]}
              </span>
            </div>
          ) : (
            <div className="w-6 h-6 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center">
              <span className="text-xs text-gray-500 dark:text-gray-400">?</span>
            </div>
          )}

          <span className={`px-2 py-1 text-xs font-semibold rounded-md ${priorityColors[task.priority]}`}>
            {task.priority}
          </span>
        </div>

        {/* Right side - Due Date */}
        {task.dueDate && (
          <div className={`flex items-center gap-1 text-xs ${
            isOverdue 
              ? 'text-red-600 dark:text-red-400 font-semibold' 
              : 'text-gray-500 dark:text-gray-400'
          }`}>
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <span>{formatDate(task.dueDate)}</span>
            {isOverdue && <span className="ml-1">⚠️</span>}
          </div>
        )}
      </div>
    </article>
  )
}

export default TaskCard
