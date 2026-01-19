import { useDarkMode } from '../hooks/useDarkMode'
import KanbanBoard from '../components/kanban/KanbanBoard'

const KanbanPage = () => {
  const { isDarkMode } = useDarkMode()

  return (
    <div className={`h-screen ${isDarkMode ? 'dark' : ''}`}>
      <KanbanBoard />
    </div>
  )
}

export default KanbanPage
