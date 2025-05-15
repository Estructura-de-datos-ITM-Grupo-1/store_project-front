import { OrdersPallets } from './dispo';

export type InternalMovementType = {
  id: number;
  date: string; // Puedes usar Date si estás manejando fechas como objetos Date en lugar de strings
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
  vehicle: string;
  driver: { id: string; name: string };
  dispatch: any;
  observations?: string;
};
