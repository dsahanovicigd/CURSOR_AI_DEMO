import { useDroppable } from '@dnd-kit/core'
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable'
import KanbanTaskCard, { KanbanTask } from './KanbanTaskCard'

interface BoardColumnProps {
  id: string
  title: string
  tasks: KanbanTask[]
  onAddTask?: () => void
  onEditTask?: (task: KanbanTask) => void
  onDeleteTask?: (taskId: string) => void
}

const BoardColumn = ({ id, title, tasks, onAddTask, onEditTask, onDeleteTask }: BoardColumnProps) => {
  const { setNodeRef, isOver } = useDroppable({
    id,
  })

  const statusColors = {
    todo: 'bg-gray-100 dark:bg-gray-800 border-gray-300 dark:border-gray-600',
    'in-progress': 'bg-blue-50 dark:bg-blue-900/20 border-blue-300 dark:border-blue-600',
    review: 'bg-purple-50 dark:bg-purple-900/20 border-purple-300 dark:border-purple-600',
    completed: 'bg-green-50 dark:bg-green-900/20 border-green-300 dark:border-green-600',
  }

  const statusIcons = {
    todo: '📝',
    'in-progress': '⚡',
    review: '👀',
    completed: '✅',
  }

  const columnColor = statusColors[id as keyof typeof statusColors] || statusColors.todo

  return (
    <div className="flex flex-col h-full min-h-0">
      {/* Column Header */}
      <div className={`flex items-center justify-between p-4 rounded-t-xl border-2 ${columnColor}`}>
        <div className="flex items-center gap-2">
          <span className="text-xl">{statusIcons[id as keyof typeof statusIcons] || '📋'}</span>
          <h3 className="text-sm font-bold text-gray-900 dark:text-white">
            {title}
          </h3>
          <span className="px-2 py-0.5 text-xs font-semibold bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full">
            {tasks.length}
          </span>
        </div>
        {onAddTask && (
          <button
            onClick={onAddTask}
            className="p-1.5 text-gray-600 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-400 hover:bg-white dark:hover:bg-gray-700 rounded-lg transition-all"
            title="Add new task"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
          </button>
        )}
      </div>

      {/* Column Body - Droppable Area */}
      <div
        ref={setNodeRef}
        className={`flex-1 p-3 space-y-3 overflow-y-auto bg-gray-50 dark:bg-gray-900/50 border-2 border-t-0 rounded-b-xl min-h-[200px] transition-colors ${
          isOver ? 'bg-blue-100 dark:bg-blue-900/30 border-blue-400 dark:border-blue-500' : 'border-gray-200 dark:border-gray-700'
        }`}
      >
        <SortableContext items={tasks.map(t => t.id)} strategy={verticalListSortingStrategy}>
          {tasks.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full py-8 text-center">
              <div className="text-4xl mb-2 opacity-50">📭</div>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                No tasks yet
              </p>
              {onAddTask && (
                <button
                  onClick={onAddTask}
                  className="mt-3 px-4 py-2 text-sm font-medium text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300"
                >
                  Add your first task
                </button>
              )}
            </div>
          ) : (
            tasks.map((task) => (
              <KanbanTaskCard
                key={task.id}
                task={task}
                onEdit={onEditTask}
                onDelete={onDeleteTask}
              />
            ))
          )}
        </SortableContext>
      </div>
    </div>
  )
}

export default BoardColumn
