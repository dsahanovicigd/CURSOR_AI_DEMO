import Avatar from '../common/Avatar'

interface TeamMembersProps {
  members: Array<{
    id: string
    name: string
    avatar: string
  }>
  onAddMember?: () => void
}

const TeamMembers = ({ members, onAddMember }: TeamMembersProps) => {
  return (
    <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4">
      <div className="text-sm font-medium text-blue-100 mb-3">Team Members</div>
      <div className="flex flex-wrap gap-2">
        {members.map((member) => (
          <div key={member.id} className="relative group">
            <Avatar
              src={member.avatar}
              alt={member.name}
              size="md"
              className="ring-2 ring-white/50 hover:ring-white transition-all cursor-pointer transform hover:scale-110"
            />
            <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 bg-gray-900 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none z-10">
              {member.name}
            </div>
          </div>
        ))}
        {onAddMember && (
          <button 
            onClick={onAddMember}
            className="w-10 h-10 rounded-full bg-white/20 border-2 border-white/50 border-dashed flex items-center justify-center hover:bg-white/30 transition-colors"
            aria-label="Add team member"
          >
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
            </svg>
          </button>
        )}
      </div>
    </div>
  )
}

export default TeamMembers
