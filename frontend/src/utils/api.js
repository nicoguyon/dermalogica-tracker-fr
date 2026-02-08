import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
})

export const fetchStats = async () => {
  const response = await api.get('/stats')
  return response.data
}

export const fetchBrands = async () => {
  const response = await api.get('/brands')
  return response.data
}

export const fetchProducts = async (params = {}) => {
  const response = await api.get('/products', { params })
  return response.data
}

export const fetchNewProducts = async (days = 7, brand = null) => {
  const params = { days }
  if (brand) params.brand = brand
  const response = await api.get('/new-products', { params })
  return response.data
}

export const fetchPromotions = async (days = 7) => {
  const response = await api.get('/promotions', { params: { days } })
  return response.data
}

export const fetchPriceHistory = async (productId) => {
  const response = await api.get(`/price-history/${productId}`)
  return response.data
}

export const fetchSites = async () => {
  const response = await api.get('/sites')
  return response.data
}

export const searchProducts = async (query) => {
  const response = await api.get('/search', { params: { q: query } })
  return response.data
}

export default api
