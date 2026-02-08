import { Link, useLocation } from 'react-router-dom'
import { Sun, Moon, Package, TrendingUp, Tag, Sparkles, BarChart3, GitCompare, Bell, Menu, X } from 'lucide-react'
import { useState } from 'react'

const Navbar = ({ darkMode, setDarkMode }) => {
  const location = useLocation()
  const [mobileOpen, setMobileOpen] = useState(false)

  const navItems = [
    { path: '/', label: 'Dashboard', icon: BarChart3 },
    { path: '/products', label: 'Produits', icon: Package },
    { path: '/brands', label: 'Marques', icon: Tag },
    { path: '/compare', label: 'Analyse', icon: GitCompare },
    { path: '/alerts', label: 'Alertes', icon: Bell },
    { path: '/promotions', label: 'Promos', icon: TrendingUp },
    { path: '/new', label: 'Nouveautés', icon: Sparkles },
  ]

  return (
    <nav className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-gray-900 dark:bg-white rounded flex items-center justify-center">
                <span className="text-white dark:text-gray-900 font-bold text-sm">d</span>
              </div>
              <div className="hidden sm:block">
                <span className="text-lg font-semibold text-gray-900 dark:text-white tracking-tight">
                  dermalogica
                </span>
                <span className="text-xs text-gray-400 dark:text-gray-500 ml-2 font-medium uppercase tracking-wider">
                  tracker
                </span>
              </div>
            </Link>
            <div className="hidden md:ml-8 md:flex md:space-x-1">
              {navItems.map((item) => {
                const Icon = item.icon
                const isActive = location.pathname === item.path
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`inline-flex items-center px-3 py-2 text-sm font-medium rounded-md transition-all ${
                      isActive
                        ? 'bg-gray-900 dark:bg-white text-white dark:text-gray-900'
                        : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-white'
                    }`}
                  >
                    <Icon className="h-4 w-4 mr-1.5" />
                    {item.label}
                  </Link>
                )
              })}
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setDarkMode(!darkMode)}
              className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
              aria-label="Toggle dark mode"
            >
              {darkMode ? (
                <Sun className="h-5 w-5 text-yellow-500" />
              ) : (
                <Moon className="h-5 w-5 text-gray-600" />
              )}
            </button>
            <button
              onClick={() => setMobileOpen(!mobileOpen)}
              className="md:hidden p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            >
              {mobileOpen ? (
                <X className="h-5 w-5 text-gray-600 dark:text-gray-400" />
              ) : (
                <Menu className="h-5 w-5 text-gray-600 dark:text-gray-400" />
              )}
            </button>
          </div>
        </div>
      </div>
      {/* Mobile menu */}
      {mobileOpen && (
        <div className="md:hidden border-t border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 pb-3">
          {navItems.map((item) => {
            const Icon = item.icon
            const isActive = location.pathname === item.path
            return (
              <Link
                key={item.path}
                to={item.path}
                onClick={() => setMobileOpen(false)}
                className={`flex items-center px-4 py-3 text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white'
                    : 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800'
                }`}
              >
                <Icon className="h-4 w-4 mr-3" />
                {item.label}
              </Link>
            )
          })}
        </div>
      )}
    </nav>
  )
}

export default Navbar
