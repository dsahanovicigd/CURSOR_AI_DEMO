export interface QuickAction {
  icon: string
  label: string
  color: string
  action: () => void
}

interface QuickActionsProps {
  actions: QuickAction[]
}

const QuickActions = ({ actions }: QuickActionsProps) => {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 md:gap-4">
      {actions.map((action, index) => (
        <button
          key={index}
          onClick={action.action}
          className={`${action.color} text-white rounded-xl p-4 md:p-6 shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-1 active:scale-95`}
          aria-label={action.label}
        >
          <div className="text-3xl mb-2">{action.icon}</div>
          <div className="font-semibold text-sm md:text-base">{action.label}</div>
        </button>
      ))}
    </div>
  )
}

export default QuickActions
