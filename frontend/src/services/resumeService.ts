import axios from 'axios';

// Get the API base URL from environment variables
const API_BASE_URL = import.meta.env.VITE_API_URL;

// Function to upload a resume
export const uploadResume = async (formData: FormData) => {
    const token = localStorage.getItem('accessToken');
    try {
        const response = await axios.post(`${API_BASE_URL}/resumes/upload/`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
                Authorization: `Bearer ${token}`
            },
        });
        return response.data;
    } catch (error: any) {
        throw new Error(error.response?.data?.message || 'Failed to upload resume');
    }
};

// Function to fetch resume details
export const getResumeDetails = async (resumeId: number) => {
    const token = localStorage.getItem('accessToken');
    try {
        const response = await axios.get(`${API_BASE_URL}/resumes/${resumeId}/`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });
        return response.data;
    } catch (error: any) {
        throw new Error(error.response?.data?.message || 'Failed to fetch resume details');
    }
}; 