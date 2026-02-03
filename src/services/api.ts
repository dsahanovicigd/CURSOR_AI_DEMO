/**
 * API Service for E-Commerce
 * Handles all API calls to the Flask backend
 */

// Use environment variable for API URL, fallback to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001/api';

// Type definitions
interface ApiError extends Error {
  status?: number;
  isNetworkError?: boolean;
  originalError?: string;
}

interface Pagination {
  page: number;
  per_page: number;
  total: number;
  pages: number;
}

interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  category: string;
  image_url?: string;
  stock?: number;
}

interface CartItem {
  id: number;
  product_id: number;
  quantity: number;
  product?: Product;
}

interface Cart {
  id: number;
  items: CartItem[];
  total: number;
  discount_code?: string;
  discount_amount?: number;
}

interface Order {
  id: number;
  user_id?: number;
  order_number?: string;
  total: number;
  status: string;
  created_at?: string;
  items?: CartItem[];
}

interface PaymentInfo {
  card_number: string;
  expiry_date?: string;
  expiry_month?: string;
  expiry_year?: string;
  cvv: string;
  cardholder_name: string;
}

interface ShippingAddress {
  street: string;
  city: string;
  state: string;
  zip_code: string;
  country: string;
}

interface AuthResponse {
  access_token: string;
  refresh_token?: string;
  user?: {
    id: number;
    username: string;
    email: string;
    name?: string;
    first_name?: string;
    last_name?: string;
    role?: string;
  };
}

// Get auth token from localStorage
const getAuthToken = (): string | null => {
  return localStorage.getItem('auth_token');
};

// Get refresh token from localStorage
const getRefreshToken = (): string | null => {
  return localStorage.getItem('refresh_token');
};

// Get auth headers
const getAuthHeaders = (): HeadersInit => {
  const token = getAuthToken();
  return {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
  };
};

// Check if token is expired
const isTokenExpired = (token: string): boolean => {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const exp = payload.exp * 1000; // Convert to milliseconds
    return Date.now() >= exp;
  } catch {
    return true;
  }
};

// Refresh access token using refresh token
const refreshAccessToken = async (): Promise<string | null> => {
  const refreshToken = getRefreshToken();
  if (!refreshToken) {
    return null;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${refreshToken}`,
      },
      mode: 'cors',
    });

    if (response.ok) {
      const data = await response.json();
      if (data.access_token) {
        localStorage.setItem('auth_token', data.access_token);
        return data.access_token;
      }
    }
  } catch (error) {
    console.error('Token refresh failed:', error);
  }

  // If refresh fails, clear tokens
  localStorage.removeItem('auth_token');
  localStorage.removeItem('refresh_token');
  return null;
};

// API request helper with automatic token refresh
const apiRequest = async <T>(
  endpoint: string,
  options: RequestInit = {},
  retryOn401: boolean = true
): Promise<T> => {
  const url = `${API_BASE_URL}${endpoint}`;
  
  try {
    // Check if access token is expired and refresh if needed
    const currentToken = getAuthToken();
    if (currentToken && isTokenExpired(currentToken)) {
      const newToken = await refreshAccessToken();
      if (!newToken && retryOn401) {
        // Refresh failed, user needs to login again
        throw new Error('Session expired. Please login again.') as ApiError;
      }
    }

    const headers = {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
      ...options.headers,
    };
    
    // Remove Content-Type if body is FormData
    if (options.body instanceof FormData) {
      const headersObj = headers as Record<string, string>;
      delete headersObj['Content-Type'];
    }
    
    const response = await fetch(url, {
      ...options,
      headers,
      mode: 'cors', // Explicitly set CORS mode
      credentials: 'include', // Include credentials for CORS
    });

    // Handle 401 Unauthorized - try to refresh token
    if (response.status === 401 && retryOn401 && endpoint !== '/auth/login' && endpoint !== '/auth/refresh') {
      const newToken = await refreshAccessToken();
      if (newToken) {
        // Retry the request with new token
        const retryHeaders = {
          ...headers,
          'Authorization': `Bearer ${newToken}`,
        };
        const retryResponse = await fetch(url, {
          ...options,
          headers: retryHeaders,
          mode: 'cors',
          credentials: 'include',
        });
        
        if (retryResponse.ok) {
          return retryResponse.json();
        }
      }
      
      // Refresh failed or retry failed
      const error = new Error('Authentication failed. Please login again.') as ApiError;
      error.status = 401;
      throw error;
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: `HTTP ${response.status}: ${response.statusText}` }));
      const errorMessage = (error as { error?: string; message?: string }).error || 
                          (error as { error?: string; message?: string }).message || 
                          `Request failed with status ${response.status}`;
      const errorWithStatus = new Error(errorMessage) as ApiError;
      errorWithStatus.status = response.status;
      throw errorWithStatus;
    }

    return response.json();
  } catch (err) {
    // Handle network errors (Failed to fetch)
    const error = err as Error;
    if (error.message === 'Failed to fetch' || error.name === 'TypeError' || error.message?.includes('NetworkError')) {
      const networkError = new Error(`Unable to connect to server at ${url}. Please make sure the Flask API is running on http://localhost:5001`) as ApiError;
      networkError.status = 0;
      networkError.isNetworkError = true;
      networkError.originalError = error.message;
      throw networkError;
    }
    throw err;
  }
};

// Products API
export const productsAPI = {
  getAll: async (params?: { page?: number; per_page?: number; category?: string; search?: string }) => {
    const queryParams = new URLSearchParams();
    if (params?.page) queryParams.append('page', params.page.toString());
    if (params?.per_page) queryParams.append('per_page', params.per_page.toString());
    if (params?.category) queryParams.append('category', params.category);
    if (params?.search) queryParams.append('search', params.search);
    
    const query = queryParams.toString();
    return apiRequest<{ products: Product[]; pagination: Pagination }>(`/products${query ? `?${query}` : ''}`);
  },
  
  getById: async (id: string | number) => {
    return apiRequest<{ product: Product }>(`/products/${id}`);
  },
};

// Cart API
export const cartAPI = {
  get: async () => {
    return apiRequest<{ cart: Cart }>('/cart');
  },
  
  addItem: async (productId: number, quantity: number) => {
    return apiRequest<{ cart: Cart }>('/cart/items', {
      method: 'POST',
      body: JSON.stringify({ product_id: productId, quantity }),
    });
  },
  
  updateItem: async (itemId: number, quantity: number) => {
    return apiRequest<{ cart: Cart }>(`/cart/items/${itemId}`, {
      method: 'PUT',
      body: JSON.stringify({ quantity }),
    });
  },
  
  removeItem: async (itemId: number) => {
    return apiRequest<{ cart: Cart }>(`/cart/items/${itemId}`, {
      method: 'DELETE',
    });
  },
  
  clear: async () => {
    return apiRequest<{ cart: Cart }>('/cart', {
      method: 'DELETE',
    });
  },
  
  applyDiscount: async (code: string) => {
    return apiRequest<{ cart: Cart }>('/cart/apply-discount', {
      method: 'POST',
      body: JSON.stringify({ discount_code: code }),
    });
  },
  
  removeDiscount: async () => {
    return apiRequest<{ cart: Cart }>('/cart/discount', {
      method: 'DELETE',
    });
  },
};

// Checkout API
export const checkoutAPI = {
  processPayment: async (payment: PaymentInfo, shippingAddress: ShippingAddress) => {
    return apiRequest<{ order: Order; transaction_id: string }>('/checkout/process-payment', {
      method: 'POST',
      body: JSON.stringify({ payment, shipping_address: shippingAddress }),
    });
  },
};

// Orders API
export const ordersAPI = {
  getAll: async (params?: { page?: number; per_page?: number }) => {
    const queryParams = new URLSearchParams();
    if (params?.page) queryParams.append('page', params.page.toString());
    if (params?.per_page) queryParams.append('per_page', params.per_page.toString());
    
    const query = queryParams.toString();
    return apiRequest<{ orders: Order[]; pagination: Pagination }>(`/orders${query ? `?${query}` : ''}`);
  },
  
  getById: async (orderId: number) => {
    return apiRequest<{ order: Order }>(`/orders/${orderId}`);
  },
};

// Auth API
export const authAPI = {
  login: async (username: string, password: string) => {
    const response = await apiRequest<AuthResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    }, false); // Don't retry on 401 for login
    
    // Store tokens
    if (response.access_token) {
      localStorage.setItem('auth_token', response.access_token);
    }
    if (response.refresh_token) {
      localStorage.setItem('refresh_token', response.refresh_token);
    }
    
    return response;
  },
  
  register: async (data: { username: string; email: string; password: string; first_name?: string; last_name?: string }) => {
    await apiRequest<{ message: string }>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    }, false);
    
    // After registration, automatically login to get token
    try {
      const loginResponse = await apiRequest<AuthResponse>('/auth/login', {
        method: 'POST',
        body: JSON.stringify({
          username: data.username,
          password: data.password
        }),
      }, false);
      
      // Store tokens
      if (loginResponse.access_token) {
        localStorage.setItem('auth_token', loginResponse.access_token);
      }
      if (loginResponse.refresh_token) {
        localStorage.setItem('refresh_token', loginResponse.refresh_token);
      }
      
      return loginResponse;
    } catch (loginErr) {
      // If auto-login fails, still return registration response
      console.error('Auto-login after registration failed:', loginErr);
      throw loginErr;
    }
  },
  
  logout: () => {
    // Get token before clearing (for backend call)
    const token = getAuthToken();
    
    // Clear tokens immediately for instant logout - no waiting!
    localStorage.removeItem('auth_token');
    localStorage.removeItem('refresh_token');
    
    // Optionally notify backend (fire and forget, don't wait or handle response)
    if (token) {
      // Call logout endpoint asynchronously without blocking or handling response
      fetch(`${API_BASE_URL}/auth/logout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        mode: 'cors',
      }).catch(() => {
        // Silently ignore all errors - tokens already cleared, logout is complete
      });
    }
    
    // Return immediately - logout is instant
  },
  
  refreshToken: async () => {
    const refreshToken = getRefreshToken();
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${refreshToken}`,
      },
      mode: 'cors',
    });

    if (!response.ok) {
      // Refresh failed, clear tokens
      localStorage.removeItem('auth_token');
      localStorage.removeItem('refresh_token');
      throw new Error('Token refresh failed');
    }

    const data = await response.json();
    
    if (data.access_token) {
      localStorage.setItem('auth_token', data.access_token);
    }
    
    return data;
  },
  
  getCurrentUser: async () => {
    return await apiRequest<{ 
      id: number; 
      username: string; 
      email: string; 
      name?: string;
      first_name?: string;
      last_name?: string;
      role?: string;
    }>('/auth/me', {
      method: 'GET',
    });
  },
  
  isAuthenticated: (): boolean => {
    const token = getAuthToken();
    const refreshToken = getRefreshToken();
    
    // Need at least refresh token to be authenticated
    if (!token && !refreshToken) return false;
    
    // If we have access token, check if it's expired
    if (token) {
      try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const exp = payload.exp * 1000; // Convert to milliseconds
        // Token is valid if not expired, or if expired but we have refresh token
        if (Date.now() < exp) {
          return true;
        }
        // Token expired but we have refresh token - can still authenticate
        return !!refreshToken;
      } catch {
        // Token invalid, but check refresh token
        return !!refreshToken;
      }
    }
    
    // Only refresh token available
    return !!refreshToken;
  },
  
  getStoredRefreshToken: (): string | null => {
    return getRefreshToken();
  },
};
