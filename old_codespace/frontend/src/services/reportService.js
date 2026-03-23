import api from './api';

export const reportUser = async (data) => {
  const response = await api.post('/report/', data);
  return response.data;
};
