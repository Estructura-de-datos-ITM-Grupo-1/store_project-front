import axios from 'axios';


const token = localStorage.getItem('token');
export const getAllVehicles = async () => {
  try {
    const response = await axios.get(
      'https://api.service.tutti.addiis.co/vehicles',{
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
