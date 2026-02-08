const StatCard = ({ title, value, icon: Icon, trend, color = 'dark' }) => {
  const colorClasses = {
    dark: 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white',
    accent: 'bg-accent-50 dark:bg-accent-900/30 text-accent-600 dark:text-accent-400',
    green: 'bg-green-50 dark:bg-green-900/30 text-green-600 dark:text-green-400',
    blue: 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400',
    purple: 'bg-purple-50 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400',
    orange: 'bg-orange-50 dark:bg-orange-900/30 text-orange-600 dark:text-orange-400',
    primary: 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white',
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5 transition-all hover:shadow-md">
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2">
            {title}
          </p>
          <p className="text-3xl font-bold text-gray-900 dark:text-white">
            {value}
          </p>
          {trend && (
            <p className={`text-sm mt-2 ${trend.positive ? 'text-green-600' : 'text-red-600'}`}>
              {trend.value}
            </p>
          )}
        </div>
        {Icon && (
          <div className={`p-3 rounded-xl ${colorClasses[color]}`}>
            <Icon className="h-5 w-5" />
          </div>
        )}
      </div>
    </div>
  )
}

export default StatCard
