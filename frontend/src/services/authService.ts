import axios from '../lib/axiosInstance';

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
    const response = await axios.post('/users/register/', data);
    console.log('Register response:', response.data);
    if (response.data.access) {
      localStorage.setItem('accessToken', response.data.access);
      localStorage.setItem('refreshToken', response.data.refresh);
    } else {
      console.error('Access token not found in response:', response.data);
    }
    return response.data;
  },

  login: async (data: LoginData): Promise<AuthResponse> => {
    const response = await axios.post('/users/login/', data);
    console.log('Login response:', response.data);
    if (response.data.access) {
      localStorage.setItem('accessToken', response.data.access);
      localStorage.setItem('refreshToken', response.data.refresh);
    } else {
      console.error('Access token not found in response:', response.data);
    }
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  },
};

export default authService;