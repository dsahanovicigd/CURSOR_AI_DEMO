/**
 * Token Manager Utility
 * Handles JWT token management, expiration checking, and automatic refresh
 */

const ACCESS_TOKEN_KEY = 'auth_token'
const REFRESH_TOKEN_KEY = 'refresh_token'

/**
 * Get access token from localStorage
 */
export const getAccessToken = (): string | null => {
  return localStorage.getItem(ACCESS_TOKEN_KEY)
}

/**
 * Get refresh token from localStorage
 */
export const getRefreshToken = (): string | null => {
  return localStorage.getItem(REFRESH_TOKEN_KEY)
}

/**
 * Store tokens in localStorage
 */
export const storeTokens = (accessToken: string, refreshToken?: string): void => {
  localStorage.setItem(ACCESS_TOKEN_KEY, accessToken)
  if (refreshToken) {
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken)
  }
}

/**
 * Clear all tokens from localStorage
 */
export const clearTokens = (): void => {
  localStorage.removeItem(ACCESS_TOKEN_KEY)
  localStorage.removeItem(REFRESH_TOKEN_KEY)
}

/**
 * Check if access token is expired
 */
export const isTokenExpired = (token: string): boolean => {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    const exp = payload.exp * 1000 // Convert to milliseconds
    return Date.now() >= exp
  } catch {
    return true
  }
}

/**
 * Get token expiration time
 */
export const getTokenExpiration = (token: string): number | null => {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return payload.exp * 1000 // Convert to milliseconds
  } catch {
    return null
  }
}

/**
 * Check if token will expire soon (within 5 minutes)
 */
export const isTokenExpiringSoon = (token: string, bufferMinutes: number = 5): boolean => {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    const exp = payload.exp * 1000
    const buffer = bufferMinutes * 60 * 1000
    return Date.now() >= (exp - buffer)
  } catch {
    return true
  }
}

/**
 * Decode token payload
 */
export const decodeToken = (token: string): Record<string, unknown> | null => {
  try {
    return JSON.parse(atob(token.split('.')[1])) as Record<string, unknown>
  } catch {
    return null
  }
}

/**
 * Get user ID from token
 */
export const getUserIdFromToken = (token: string): number | null => {
  const payload = decodeToken(token)
  if (payload) {
    const sub = payload.sub as number | undefined
    const userId = payload.user_id as number | undefined
    const id = payload.id as number | undefined
    return sub || userId || id || null
  }
  return null
}

/**
 * Setup automatic token refresh
 */
export const setupTokenRefresh = (refreshCallback: () => Promise<void>): (() => void) => {
  let intervalId: NodeJS.Timeout | null = null

  const checkAndRefresh = async () => {
    const accessToken = getAccessToken()
    const refreshToken = getRefreshToken()

    if (accessToken && refreshToken) {
      if (isTokenExpiringSoon(accessToken)) {
        try {
          await refreshCallback()
        } catch (error) {
          console.error('Automatic token refresh failed:', error)
        }
      }
    }
  }

  // Check immediately
  checkAndRefresh()

  // Set up interval to check every 5 minutes
  intervalId = setInterval(checkAndRefresh, 5 * 60 * 1000)

  // Return cleanup function
  return () => {
    if (intervalId) {
      clearInterval(intervalId)
    }
  }
}
