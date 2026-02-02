import api from './api'
import Cookies from 'js-cookie'

export interface LoginCredentials {
  username: string
  password: string
}

export interface RegisterData {
  username: string
  email: string
  password: string
  password_confirm: string
  first_name: string
  last_name: string
  phone_number?: string
}

export interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  role: string
  is_verified: boolean
  is_approved: boolean
}

export const authService = {
  async login(credentials: LoginCredentials) {
    const response = await api.post('/auth/login/', credentials)
    const { access, refresh } = response.data
    
    Cookies.set('access_token', access, { expires: 1 })
    Cookies.set('refresh_token', refresh, { expires: 7 })
    
    return response.data
  },

  async register(data: RegisterData) {
    const response = await api.post('/auth/register/', data)
    return response.data
  },

  async logout() {
    Cookies.remove('access_token')
    Cookies.remove('refresh_token')
  },

  async getCurrentUser(): Promise<User> {
    const response = await api.get('/auth/me/')
    return response.data
  },

  isAuthenticated(): boolean {
    return !!Cookies.get('access_token')
  },
}
