import { SubmitHandler, useForm } from "react-hook-form";
import { ProductScann } from "../types/product";
import React, { useState, useEffect } from "react";
import dayjs from "dayjs";
import { saveProductScanned } from "../../../services/Productos";

type FormValues = {
  manufactureDate: string;
  expirationDate: Date;
  lot: string;
  amountReceived: number;
  malfunctions: number;
  observations: string;
};

type ScannedProductFormProps = {
  data: ProductScann | undefined;
};

const ScannedProductForm: React.FC<ScannedProductFormProps> = ({ data }) => {
  const {
    register,
    handleSubmit,
    formState: { isValid },
  } = useForm<FormValues>();

  const [expirationDate, setExpirationDate] = useState<Date>(new Date());
  const [usefulLife, setUsefulLife] = useState<number>(0);
  const [receptionPercentage, setReceptionPercentage] = useState<number>(0);
  const [showFormResult, setShowFormResult] = useState<boolean>(false);
  const [formData, setFormData] = useState<FormValues | null>(null);

  const calculateValues = (data: FormValues) => {
    const usefulDays = dayjs(data.expirationDate).diff(
      data.manufactureDate,
      "days"
    );
    setUsefulLife(usefulDays);

    let lifePercentage: number;
    if (usefulDays < 30) {
      lifePercentage = 94;
    } else if (usefulDays >= 30 && usefulDays <= 39) {
      lifePercentage = 90;
    } else if (usefulDays >= 40 && usefulDays <= 44) {
      lifePercentage = 80;
    } else if (usefulDays >= 45 && usefulDays <= 119) {
      lifePercentage = 70;
    } else if (usefulDays >= 120 && usefulDays <= 179) {
      lifePercentage = 60;
    } else {
      lifePercentage = 50;
    }
    setReceptionPercentage(lifePercentage);
  };

  useEffect(() => {
    if (formData) {
      saveProductScanned({
        expirationDate: formData.expirationDate,
        manufactureDate: formData.manufactureDate,
        usefulLife,
        receptionPercentage,
        lot: formData.lot,
        warehouseLocationId: data?.locations[0].id,
        descriptionProduct: data?.name,
        amountReceived: formData.amountReceived,
        sku: data?.productCode,
        malfunctions: Number(formData.malfunctions),
        observations: formData.observations,
      });
      setShowFormResult(true);
    }
  }, [usefulLife, receptionPercentage]); 

  //TODO : Mostrar notificacion de guardado en db
  //TODO : Quitar bloqueo de boton para no tener que recargar y enviar otro producto

  const sendProduct: SubmitHandler<FormValues> = (dataForm) => {
    calculateValues(dataForm); 
    setExpirationDate(dataForm.expirationDate);
    setFormData(dataForm); 
  };

  return (
    <>
      {data ? (
        <div className="text-left w-full">
          <p>
            <b>EAN: </b> {data?.ean}
          </p>
          <p>
            <b>Descripción:</b> {data?.name}
          </p>
          <p>
            <b>SKU:</b> {data?.productCode}
          </p>
          <p>
            <b>CXP:</b> {data?.cxp}
          </p>
          <p>
            <b>UXC:</b> {data?.uxc}
          </p>

          <div className="flex justify-between my-4">
            <div className="bg-[#EAEAEA] py-2 px-4 rounded-lg">
              <b>Ubicación</b>: {data?.locations[0]?.ubicacion}
            </div>
            <div className="bg-[#EAEAEA] py-2 px-4 rounded-lg">
              <b>Dispo</b>: {data?.locations[0]?.dispo}
            </div>
          </div>

          {showFormResult ? (
            <>
              <p>
                <b>Vencimiento:</b> {dayjs(expirationDate).format("D-M-YYYY")}
              </p>
              <p>
                <b>Vida útil:</b> {usefulLife} días
              </p>
              <p>
                <b>Recepción:</b> {receptionPercentage}%
              </p>
            </>
          ) : (
            <form
              className="flex flex-col gap-4 items-center"
              onSubmit={handleSubmit(sendProduct)}
            >
              <div className="w-full">
                <label className="text-sm font-medium">
                  Fecha de elaboración
                </label>
                <input
                  type="date"
                  {...register("manufactureDate", { required: true })}
                  className="bg-white border focus:border-red py-1 px-2 rounded-md w-full text-sm"
                />
              </div>
              <div className="w-full">
                <label className="text-sm font-medium">
                  Fecha de vencimiento
                </label>
                <input
                  type="date"
                  {...register("expirationDate", { required: true })}
                  className="bg-white border focus:border-red py-1 px-2 rounded-md w-full text-sm"
                />
              </div>
              <div className="w-full">
                <label className="text-sm font-medium">Lote</label>
                <input
                  type="text"
                  {...register("lot", { required: true })}
                  className="bg-white border focus:border-red py-1 px-2 rounded-md w-full text-sm"
                />
              </div>
              <div className="w-full">
                <label className="text-sm font-medium">Cantidad</label>
                <input
                  type="text"
                  {...register("amountReceived", { required: true })}
                  className="bg-white border focus:border-red py-1 px-2 rounded-md w-full text-sm"
                />
              </div>
              <div className="w-full">
                <label className="text-sm font-medium">Averias</label>
                <input
                  type="text"
                  {...register("malfunctions", { required: true })}
                  className="bg-white border focus:border-red py-1 px-2 rounded-md w-full text-sm"
                />
              </div>
              <div className="w-full">
                <label className="text-sm font-medium">Observaciones</label>
                <input
                  type="text"
                  {...register("observations", { required: true })}
                  className="bg-white border focus:border-red py-1 px-2 rounded-md w-full text-sm"
                />
              </div>
              <button
                disabled={!isValid}
                className="bg-[#007EF2] text-white px-6 h-7 rounded-lg w-max disabled:bg-[#90A0B7] mt-4"
              >
                Guardar
              </button>
            </form>
          )}
        </div>
      ) : null}
    </>
  );
};

export default ScannedProductForm;
