export type ScannedProduct = {
  expirationDate: Date;
  manufactureDate: string;
  usefulLife: number;
  receptionPercentage: number;
  lot?: string;
  sku?: string | undefined;
  descriptionProduct?: string | undefined;
  amountReceived?: number;
  warehouseLocationId?: string | number;
  malfunctions?: number | string;
  observations: string | number;
};
