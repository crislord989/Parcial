import axios from 'axios';

const API = axios.create({ baseURL: import.meta.env.VITE_API_URL });

export const searchTracks  = (q) => API.get(`/api/tracks/?q=${q}`);
export const getTracks     = ()  => API.get('/api/tracks/');
export const getCustomers  = ()  => API.get('/api/customers/');
export const createInvoice = (data) => API.post('/api/invoices/', data);
