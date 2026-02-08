import axios from 'axios'

// API backend URL - même domaine en production, localhost en dev
const API_BASE = import.meta.env.VITE_API_URL || ''

const api = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
})

export const fetchStats = async () => {
  const { data } = await api.get('/api/stats')
  return data
}

export const fetchBrands = async () => {
  const { data } = await api.get('/api/brands')
  return data
}

export const fetchProducts = async (params = {}) => {
  const { data } = await api.get('/api/products', { params })
  return data
}

export const fetchNewProducts = async (days = 7, brand = null) => {
  const params = { days }
  if (brand) params.brand = brand
  const { data } = await api.get('/api/new-products', { params })
  return data
}

export const fetchPromotions = async (days = 7) => {
  const { data } = await api.get('/api/promotions', { params: { days } })
  return data
}

export const fetchPriceHistory = async (productId) => {
  const { data } = await api.get(`/api/price-history/${productId}`)
  return data
}

export const fetchSites = async () => {
  const { data } = await api.get('/api/sites')
  return data
}

export const searchProducts = async (query) => {
  if (!query) return []
  const { data } = await api.get('/api/search', { params: { q: query } })
  return data
}

export default { fetchStats, fetchBrands, fetchProducts, fetchNewProducts, fetchPromotions, fetchPriceHistory, fetchSites, searchProducts }
