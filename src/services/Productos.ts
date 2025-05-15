import axios from 'axios';
import { toast} from 'sonner';
import { ScannedProduct } from '../types/products';
const token = localStorage.getItem('token');
export const getProductDetail = async (ean: string) => {
  try {
    const response = await axios.get(`http://localhost:8081/products/${ean}`, {
      headers: {
        Authorization: token,
      },
    });

    const { data } = response;
    return data.data;
  } catch (error: any) {
    
    toast.error(error?.response?.data?.message);
  }
};

export const saveProductScanned = async (data: ScannedProduct) => {
  console.log(data)
  try {
    const response = await axios.post(
      //TODO : Cambiar la url por la de la api
      "http://localhost:8081/reception-scanned-products",
      data,
      {
        headers: {
          Authorization: token,
        },
      }
    );
    return response;
  } catch (error: any) {
    toast.error(error?.response?.data?.message);
  }
};

export const getLastScannedProducts = async () => {
  try {
    const response = await axios.get(
      'http://localhost:8081/reception-scanned-products',{
        headers: {
          Authorization: token,
        }
      }
     
    );
    
    return response.data.content;
  } catch (error: any) {
    toast.error(error?.response?.data?.message);
  }
}
