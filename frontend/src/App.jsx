import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { useState, useEffect } from 'react'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import Products from './pages/Products'
import Brands from './pages/Brands'
import Promotions from './pages/Promotions'
import NewProducts from './pages/NewProducts'

function App() {
  const [darkMode, setDarkMode] = useState(() => {
    const saved = localStorage.getItem('darkMode')
    return saved ? JSON.parse(saved) : false
  })

  useEffect(() => {
    localStorage.setItem('darkMode', JSON.stringify(darkMode))
    if (darkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [darkMode])

  return (
    <Router>
      <div className={`min-h-screen transition-colors ${darkMode ? 'dark' : ''}`}>
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors">
          <Navbar darkMode={darkMode} setDarkMode={setDarkMode} />
          <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/products" element={<Products />} />
              <Route path="/brands" element={<Brands />} />
              <Route path="/promotions" element={<Promotions />} />
              <Route path="/new" element={<NewProducts />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  )
}

export default App
