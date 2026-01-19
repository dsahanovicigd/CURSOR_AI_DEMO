import { useState, useEffect, useMemo } from 'react'
import {
  DndContext,
  DragEndEvent,
  DragOverlay,
  DragStartEvent,
  PointerSensor,
  useSensor,
  useSensors,
  closestCorners,
} from '@dnd-kit/core'
import BoardColumn from './BoardColumn'
import KanbanTaskCard, { KanbanTask } from './KanbanTaskCard'
import AddTaskModal from './AddTaskModal'

const STORAGE_KEY = 'kanban-tasks'

// Sample initial tasks
const initialTasks: KanbanTask[] = [
  {
    id: '1',
    title: 'Design new landing page',
    description: 'Create mockups for the new product landing page with focus on conversion',
    status: 'in-progress',
    priority: 'high',
    assignee: {
      id: '1',
      name: 'Sarah Chen',
      avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80'
    },
    tags: ['Design', 'UI/UX'],
    dueDate: '2026-01-25',
    createdAt: '2026-01-15T10:00:00Z',
    updatedAt: '2026-01-19T10:00:00Z'
  },
  {
    id: '2',
    title: 'Fix authentication bug',
    description: 'Users reporting issues with social login on mobile devices',
    status: 'review',
    priority: 'urgent',
    assignee: {
      id: '2',
      name: 'John Doe',
      avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80'
    },
    tags: ['Bug', 'Backend'],
    dueDate: '2026-01-20',
    createdAt: '2026-01-18T10:00:00Z',
    updatedAt: '2026-01-19T10:00:00Z'
  },
  {
    id: '3',
    title: 'Update documentation',
    description: 'Add API documentation for the new v2 endpoints',
    status: 'todo',
    priority: 'medium',
    assignee: {
      id: '3',
      name: 'Emma Wilson',
      avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80'
    },
    tags: ['Documentation'],
    dueDate: '2026-01-28',
    createdAt: '2026-01-16T10:00:00Z',
    updatedAt: '2026-01-17T10:00:00Z'
  },
  {
    id: '4',
    title: 'Database optimization',
    description: 'Optimize slow queries and add proper indexes',
    status: 'done',
    priority: 'high',
    assignee: {
      id: '4',
      name: 'Alex Johnson',
      avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=256&h=256&q=80'
    },
    tags: ['Backend', 'Performance'],
    dueDate: '2026-01-18',
    createdAt: '2026-01-12T10:00:00Z',
    updatedAt: '2026-01-18T10:00:00Z'
  }
]

const KanbanBoard = () => {
  const [tasks, setTasks] = useState<KanbanTask[]>([])
  const [activeTask, setActiveTask] = useState<KanbanTask | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingTask, setEditingTask] = useState<KanbanTask | null>(null)
  const [defaultStatus, setDefaultStatus] = useState<'todo' | 'in-progress' | 'review' | 'done'>('todo')
  const [searchQuery, setSearchQuery] = useState('')
  const [filterPriority, setFilterPriority] = useState<'all' | 'low' | 'medium' | 'high' | 'urgent'>('all')
  const [filterTag, setFilterTag] = useState<string>('all')

  // Load tasks from localStorage on mount
  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored) {
      try {
        setTasks(JSON.parse(stored))
      } catch (error) {
        console.error('Failed to load tasks from localStorage:', error)
        setTasks(initialTasks)
      }
    } else {
      setTasks(initialTasks)
    }
  }, [])

  // Save tasks to localStorage whenever they change
  useEffect(() => {
    if (tasks.length > 0) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks))
    }
  }, [tasks])

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    })
  )

  // Get all unique tags
  const allTags = useMemo(() => {
    const tags = new Set<string>()
    tasks.forEach(task => {
      task.tags?.forEach(tag => tags.add(tag))
    })
    return Array.from(tags).sort()
  }, [tasks])

  // Filter tasks
  const filteredTasks = useMemo(() => {
    return tasks.filter(task => {
      // Search filter
      if (searchQuery && !task.title.toLowerCase().includes(searchQuery.toLowerCase()) &&
          !task.description?.toLowerCase().includes(searchQuery.toLowerCase())) {
        return false
      }

      // Priority filter
      if (filterPriority !== 'all' && task.priority !== filterPriority) {
        return false
      }

      // Tag filter
      if (filterTag !== 'all' && !task.tags?.includes(filterTag)) {
        return false
      }

      return true
    })
  }, [tasks, searchQuery, filterPriority, filterTag])

  // Group tasks by status
  const tasksByStatus = useMemo(() => {
    return {
      todo: filteredTasks.filter(t => t.status === 'todo'),
      'in-progress': filteredTasks.filter(t => t.status === 'in-progress'),
      review: filteredTasks.filter(t => t.status === 'review'),
      done: filteredTasks.filter(t => t.status === 'done'),
    }
  }, [filteredTasks])

  const handleDragStart = (event: DragStartEvent) => {
    const { active } = event
    const task = tasks.find(t => t.id === active.id)
    if (task) {
      setActiveTask(task)
    }
  }

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event
    setActiveTask(null)

    if (!over) return

    const taskId = active.id as string
    const overId = over.id as string

    // Determine the target status
    // If over.id is a column ID, use it directly
    // If over.id is a task ID, find that task's status
    let newStatus: 'todo' | 'in-progress' | 'review' | 'done'
    
    const columnIds = ['todo', 'in-progress', 'review', 'done']
    if (columnIds.includes(overId)) {
      // Dropped on a column
      newStatus = overId as 'todo' | 'in-progress' | 'review' | 'done'
    } else {
      // Dropped on a task - find that task's status
      const targetTask = tasks.find(t => t.id === overId)
      if (!targetTask) return
      newStatus = targetTask.status
    }

    // Update the task status
    setTasks(prevTasks =>
      prevTasks.map(task =>
        task.id === taskId
          ? { ...task, status: newStatus, updatedAt: new Date().toISOString() }
          : task
      )
    )
  }

  const handleAddTask = (taskData: Omit<KanbanTask, 'id' | 'createdAt' | 'updatedAt'>) => {
    const newTask: KanbanTask = {
      ...taskData,
      id: Date.now().toString(),
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    }
    setTasks(prev => [...prev, newTask])
  }

  const handleEditTask = (taskData: Omit<KanbanTask, 'id' | 'createdAt' | 'updatedAt'>) => {
    if (!editingTask) return
    
    setTasks(prev =>
      prev.map(task =>
        task.id === editingTask.id
          ? { ...task, ...taskData, updatedAt: new Date().toISOString() }
          : task
      )
    )
    setEditingTask(null)
  }

  const handleDeleteTask = (taskId: string) => {
    if (confirm('Are you sure you want to delete this task?')) {
      setTasks(prev => prev.filter(task => task.id !== taskId))
    }
  }

  const openAddModal = (status: 'todo' | 'in-progress' | 'review' | 'done') => {
    setDefaultStatus(status)
    setEditingTask(null)
    setIsModalOpen(true)
  }

  const openEditModal = (task: KanbanTask) => {
    setEditingTask(task)
    setIsModalOpen(true)
  }

  const clearFilters = () => {
    setSearchQuery('')
    setFilterPriority('all')
    setFilterTag('all')
  }

  const hasActiveFilters = searchQuery || filterPriority !== 'all' || filterTag !== 'all'

  return (
    <div className="h-full flex flex-col bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 p-4 md:p-6">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
              <span>📋</span>
              Kanban Board
            </h1>
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
              Drag and drop tasks between columns to update their status
            </p>
          </div>
          <button
            onClick={() => openAddModal('todo')}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            New Task
          </button>
        </div>

        {/* Filters */}
        <div className="mt-6 flex flex-col md:flex-row gap-3">
          {/* Search */}
          <div className="flex-1">
            <div className="relative">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search tasks..."
                className="w-full px-4 py-2.5 pl-10 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <svg className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </div>

          {/* Priority Filter */}
          <select
            value={filterPriority}
            onChange={(e) => setFilterPriority(e.target.value as any)}
            className="px-4 py-2.5 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="all">All Priorities</option>
            <option value="urgent">🔴 Urgent</option>
            <option value="high">🟠 High</option>
            <option value="medium">🟡 Medium</option>
            <option value="low">🔵 Low</option>
          </select>

          {/* Tag Filter */}
          <select
            value={filterTag}
            onChange={(e) => setFilterTag(e.target.value)}
            className="px-4 py-2.5 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="all">All Tags</option>
            {allTags.map(tag => (
              <option key={tag} value={tag}>{tag}</option>
            ))}
          </select>

          {/* Clear Filters */}
          {hasActiveFilters && (
            <button
              onClick={clearFilters}
              className="px-4 py-2.5 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 font-medium rounded-lg transition-colors"
            >
              Clear Filters
            </button>
          )}
        </div>

        {/* Stats */}
        <div className="mt-4 flex flex-wrap gap-4">
          <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
            <span className="font-semibold">Total Tasks:</span>
            <span className="px-2 py-0.5 bg-gray-200 dark:bg-gray-700 rounded-full font-medium">{tasks.length}</span>
          </div>
          {hasActiveFilters && (
            <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
              <span className="font-semibold">Filtered:</span>
              <span className="px-2 py-0.5 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 rounded-full font-medium">{filteredTasks.length}</span>
            </div>
          )}
        </div>
      </div>

      {/* Kanban Board */}
      <div className="flex-1 overflow-x-auto overflow-y-hidden p-4 md:p-6">
        <DndContext
          sensors={sensors}
          collisionDetection={closestCorners}
          onDragStart={handleDragStart}
          onDragEnd={handleDragEnd}
        >
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 h-full min-h-0">
            <BoardColumn
              id="todo"
              title="To Do"
              tasks={tasksByStatus.todo}
              onAddTask={() => openAddModal('todo')}
              onEditTask={openEditModal}
              onDeleteTask={handleDeleteTask}
            />
            <BoardColumn
              id="in-progress"
              title="In Progress"
              tasks={tasksByStatus['in-progress']}
              onAddTask={() => openAddModal('in-progress')}
              onEditTask={openEditModal}
              onDeleteTask={handleDeleteTask}
            />
            <BoardColumn
              id="review"
              title="In Review"
              tasks={tasksByStatus.review}
              onAddTask={() => openAddModal('review')}
              onEditTask={openEditModal}
              onDeleteTask={handleDeleteTask}
            />
            <BoardColumn
              id="done"
              title="Done"
              tasks={tasksByStatus.done}
              onAddTask={() => openAddModal('done')}
              onEditTask={openEditModal}
              onDeleteTask={handleDeleteTask}
            />
          </div>

          {/* Drag Overlay */}
          <DragOverlay>
            {activeTask && (
              <div className="opacity-80 rotate-3 scale-105">
                <KanbanTaskCard task={activeTask} />
              </div>
            )}
          </DragOverlay>
        </DndContext>
      </div>

      {/* Add/Edit Task Modal */}
      <AddTaskModal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false)
          setEditingTask(null)
        }}
        onSave={editingTask ? handleEditTask : handleAddTask}
        editTask={editingTask}
        defaultStatus={defaultStatus}
      />
    </div>
  )
}

export default KanbanBoard
