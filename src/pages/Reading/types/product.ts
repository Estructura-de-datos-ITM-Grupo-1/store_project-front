export type ProductScann = {
  productId: string;
  productCode: string;
  ean: string | number;
  name: string
  locations: [
    {
      id: string | number;
      ubicacion: string;
      dispo: string;
    }
  ];
  cxp: string;
  uxc: string;
  description: string;
  
};
