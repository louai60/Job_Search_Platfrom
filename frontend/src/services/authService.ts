import axios from 'axios';

const API_URL = 'http://localhost:8000/api/users/';

interface RegisterData {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
}

interface LoginData {
  email: string;
  password: string;
}

interface AuthResponse {
  user: {
    id: number;
    email: string;
    first_name: string;
    last_name: string;
  };
  token: string;
}

const authService = {
  register: async (data: RegisterData): Promise<AuthResponse> => {
    const response = await axios.post(`${API_URL}signup/`, data);
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
    }
    return response.data;
  },

  login: async (data: LoginData): Promise<AuthResponse> => {
    const response = await axios.post(`${API_URL}signin/`, data);
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
    }
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('token');
  },
};

export default authService;