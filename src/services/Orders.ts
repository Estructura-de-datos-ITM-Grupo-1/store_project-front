import axios from "axios";
import { OrdersPallets } from "../types/dispo";
import { toast } from "sonner";

const token = localStorage.getItem("token");
const utcDate = new Date();

const gmt5Offset = -5;
const gmt5Date = new Date(utcDate.getTime() + gmt5Offset * 60 * 60 * 1000);

const formattedDate = gmt5Date.toISOString().split("T")[0];
export const getInternalMovements = async (page: number) => {
  try {
    const response = await axios.get(
      `https://api.service.tutti.addiis.co/order-stores/byDate/${formattedDate}?page=${page}&size=10`,
      {
        headers: {
          Authorization: token,
        },
      }
    );

    return response.data.content;
  } catch (error) {
    console.log(error);
  }
};

export const filterInternalMovements = async (
  filterStoreCode: string | null,
  routeNumber: string | null,
  page: number
) => {
  try {
    
    let url = `https://api.service.tutti.addiis.co/order-stores/filter/${formattedDate}?page=${page}&size=100`;

    
    if (routeNumber) {
      url += `&routeNumber=${routeNumber}`;
    }
    if (filterStoreCode) {
      url += `&storeCode=${filterStoreCode}`;
    }

    const response = await axios.get(url, {
      headers: {
        Authorization: token,
      },
    });

    return response.data.content;
  } catch (error) {
    console.log(error);
    toast.error("Error al filtrar");
  }
};

export const updateDispos = async (
  orderId: number,
  dispoList: OrdersPallets[],
  channelId: string
) => {
  try {
    console.log(dispoList);
    const response = await axios.patch(
      `https://api.service.tutti.addiis.co/order-stores/${orderId}/pallets`,
      { channelId, orderPalletsInfo: dispoList },
      {
        headers: {
          Authorization: token,
        },
      }
    );
    toast.success("Pallets actualizados");
    return response.data;
  } catch (error) {}
};
