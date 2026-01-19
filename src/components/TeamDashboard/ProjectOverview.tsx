import { ProjectOverviewProps } from '../../types/project'
import TeamMembers from './TeamMembers'

const ProjectOverview = ({ title, subtitle, metrics, teamMembers, onAddMember }: ProjectOverviewProps) => {
  return (
    <div className="bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 rounded-2xl p-6 md:p-8 text-white shadow-2xl">
      <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center">
              <span className="text-2xl">🚀</span>
            </div>
            <div>
              <h1 className="text-2xl md:text-3xl font-bold">{title}</h1>
              <p className="text-blue-100">{subtitle}</p>
            </div>
          </div>
          <div className="flex flex-wrap gap-4 mt-4">
            <div className="bg-white/10 backdrop-blur-sm rounded-lg px-4 py-2">
              <div className="text-2xl font-bold">{metrics.totalTasks}</div>
              <div className="text-sm text-blue-100">Total Tasks</div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-lg px-4 py-2">
              <div className="text-2xl font-bold">{metrics.teamMembers}</div>
              <div className="text-sm text-blue-100">Team Members</div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-lg px-4 py-2">
              <div className="text-2xl font-bold">{metrics.activeProjects}</div>
              <div className="text-sm text-blue-100">Active Projects</div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-lg px-4 py-2">
              <div className="text-2xl font-bold">{metrics.completionRate}%</div>
              <div className="text-sm text-blue-100">Completion Rate</div>
            </div>
          </div>
        </div>

        {/* Team Members Section */}
        <TeamMembers members={teamMembers} onAddMember={onAddMember} />
      </div>
    </div>
  )
}

export default ProjectOverview
