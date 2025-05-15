import axios from 'axios';
import { toast } from 'sonner';

const token = localStorage.getItem('token');

export const getAllDispatchs = async (date: string, page: number) => {
  try {
     const utcDate = new Date();

     const gmt5Offset = -5;
     const gmt5Date = new Date(utcDate.getTime() + gmt5Offset * 60 * 60 * 1000);

     const formattedDate = gmt5Date.toISOString().split("T")[0];
    const response = await axios.get(
      `https://api.service.tutti.addiis.co/dispatches/${formattedDate}?page=${page}&size=10`,{
        headers: {
          Authorization: token,
        }
      }
    );

    return response.data.content;
  } catch (error) {
    console.log(error);
  }
};

export const postDispatch = async (
  orderStoreId: number,
  driverId?: number | null, 
  vehicleId?: number | null,
  observation?: string,
  platformId?: number | null
) => {
  try {
    const response = await axios.post(
      `https://api.service.tutti.addiis.co/dispatches`,
      { orderStoreId, driverId, vehicleId, observation , platformId},{
        headers: {
          Authorization: token,
        }
      }
    );
    toast.success('Despacho guardado');
    return response.data;
  } catch (error) {
    toast.error('Conductor o vehiculo no válido')
  }
};

export const updateDispatchObservation = async (
  orderStoreId: number,
  data: string
) => {
  try {
    const response = await axios.patch(
      `https://api.service.tutti.addiis.co/dispatches/${orderStoreId}/observations/`,
      {observation : data },{
        headers: {
          Authorization: token,
        }
      }
      
      
      
    );
    toast.success('Observaciones actualizadas');
    return response.data;
  } catch (error) {
    console.log(error);
  }
};
