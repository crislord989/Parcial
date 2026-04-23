import axios from 'axios';
const API = axios.create({ baseURL: import.meta.env.VITE_API_URL });
export const searchTracks  = (q) => API.get(`/tracks/?q=${encodeURIComponent(q)}`);
export const getTracks     = ()  => API.get('/tracks/');
export const getCustomers  = ()  => API.get('/customers/');
export const createInvoice = (data) => API.post('/invoices/', data);
