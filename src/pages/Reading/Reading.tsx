import { useState } from "react";
import { getProductDetail } from "../../services/Productos";
import { SubmitHandler, useForm } from "react-hook-form";
import ScannedProductForm from "./components/ScannedProductForm";
import { ProductScann } from "./types/product";
import Scanner from "../scanner/Scanner";

type FormValues = {
  ean: string;
};

const Reading = () => {
  const {
    register,
    handleSubmit,
    reset,
    formState: { isValid },
  } = useForm<FormValues>();

  const [showDetail, setShowDetail] = useState<boolean>(false);
  const [data, setData] = useState<ProductScann>();
  const [showScanner, setShowScanner] = useState<boolean>(false);
  const [ean, setEan] = useState<string>("");

  const searchDetail: SubmitHandler<FormValues> = async (formData) => {
    try {
      const product = await getProductDetail(formData.ean);

      if (!product) {
        setShowDetail(false);
        return;
      }

      setData(product);
      setShowDetail(true);
    } finally {
      reset();
    }
  };

  const onCodeScanned = (scannedCode: string) => {
    setEan(scannedCode);
    setShowScanner(false); // Ocultar el escáner una vez escaneado el código
  };

  const onStopScanning = () => {
    setShowScanner(false); // Ocultar el escáner cuando se presione "Detener Scanner"
  };

  return (
    <>
      <h2 className="text-3xl font-bold mb-6">Lectura</h2>
      <section className="flex justify-center">
        <div className="shadow-md bg-white p-4 flex flex-col gap-4 rounded-sm w-80 items-center">
          <h3 className="font-semibold text-xl">Ubicación de productos</h3>
          <form onSubmit={handleSubmit(searchDetail)}>
            <input
              id="ean"
              type="text"
              defaultValue={ean}
              {...register("ean", {
                required: "El código de barras es obligatorio",
              })}
              placeholder="Código de barras"
              className="bg-white border py-1 px-2 rounded-md text-center"
            />
            <div className=" flex gap-2 justify-center">
              <button
                disabled={!isValid}
                className="bg-[#007EF2] text-white px-6 h-7 rounded-lg w-max disabled:bg-[#90A0B7] mt-4"
              >
                Detalles
              </button>
              <button
                type="button"
                onClick={() => setShowScanner(true)}
                className="bg-[#007EF2] text-white px-6 h-7 rounded-lg w-max mt-4"
              >
                Scanner
              </button>
            </div>
          </form>
          {showDetail && data && <ScannedProductForm data={data} />}
          {showScanner && (
            <Scanner
              onCodeScanned={onCodeScanned}
              onStopScanning={onStopScanning}
            />
          )}
        </div>
      </section>
    </>
  );
};

export default Reading;
