import axios from 'axios';
const token = localStorage.getItem('token');
export const getAllDrivers = async () => {
  try {
    const response = await axios.get(
      'https://api.service.tutti.addiis.co/drivers',{
        headers: {
          Authorization: token,
        } 
      }
    );

    return response.data;
  } catch (error) {
    console.log(error);
  }
};
