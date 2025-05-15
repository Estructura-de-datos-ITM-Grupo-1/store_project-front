import { OrdersPallets } from "./dispo";
import { VehicleType } from "./vehicle";

export type DriverType = {
  id: number;
  observation: string;
  driver: {
    id: number;
    name: string;
  };
  orderStore: {
    id: number;
    date: string;
    storeName: string;
    storeCode: number;
    routeId: number;
    routeName: string;
    channelId: number;
    channelName: string;
    platformId: number;
    platformName: string;
    bigPallets: number;
    littlePallets: number;
    totalPallets: number;
    ordersPallets: OrdersPallets[];
  };
  vehicle: VehicleType
};