import { useEffect, useState } from "react";
import { InternalMovementType } from "../../types/movements";
import {
  filterInternalMovements,
  getInternalMovements,
} from "../../services/Orders";
import { VehicleType } from "../../types/vehicle";
import { getAllVehicles } from "../../services/Vehicles";
import { getAllDrivers } from "../../services/Drivers";
import DispatchesRow from "./DispatchesRow";
import { SubmitHandler, useForm } from "react-hook-form";
type FormValues = {
  storeCode: string;
  routeNumber: string;
};
const Dispatches = () => {
  const [data, setData] = useState<InternalMovementType[]>([]);
  const [vehicleData, setVehicleData] = useState<VehicleType[]>([]);
  const [driversData, setDriversData] = useState<
    { id: string; name: string }[]
  >([]);
  const [page, setPage] = useState<number>(1);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const { register, handleSubmit } = useForm<FormValues>();

  const internalMovementGet = async () => {
    setIsLoading(true); 
    try {
      const movements = await getInternalMovements(page);
      setData(movements);
    } catch (error) {
      console.error("Error al obtener movimientos internos:", error);
    } finally {
      setIsLoading(false); 
    }
   
  };

  const getVehicles = async () => {
    const vehicles = await getAllVehicles();
    setVehicleData(vehicles);
  };

  const changeFilter: SubmitHandler<FormValues> = async (
    formData: FormValues
  ) => { 

    setIsLoading(true);

    try{
    
    const filtered = await filterInternalMovements(
      formData.storeCode || null,
      formData.routeNumber || null,
      page
    );
    setData(filtered);
  } catch (error) {
    console.log(error);
  } finally {
    setIsLoading(false);  
  }

}

  const getDrivers = async () => {
    const drivers = await getAllDrivers();
    setDriversData(drivers);
  };

  useEffect(() => {
    internalMovementGet();
  }, [page]);

  useEffect(() => {
    internalMovementGet();
    getVehicles();
    getDrivers();
  }, []);

  return (
    <>
      <h2 className="text-3xl font-bold">Despacho</h2>
      <div className="my-6">
        <h3 className="text-left text-2xl">Filtrar</h3>
        <form
          onSubmit={handleSubmit(changeFilter)}
          className="flex gap-2 items-center"
        >
          <input
            type="text"
            {...register("storeCode")}
            placeholder="Código de tienda"
            className="bg-white border focus:border-red py-1 px-2 rounded-md text-center"
          />
          <input
            type="text"
            {...register("routeNumber")}
            placeholder="Número de ruta"
            className="bg-white border focus:border-red py-1 px-2 rounded-md text-center"
          />
          <button className="bg-[#007EF2] text-white px-6 h-7 rounded-lg w-max disabled:bg-[#90A0B7]">
            Buscar
          </button>
        </form>
      </div>
      {isLoading ? (
        <div className="flex justify-center items-center h-32">
          <p>Cargando...</p> 
        </div>
      ) : (
        <>
      <table className="w-full mt-10">
        <thead>
          <tr className="bg-[#EAEAEA] h-12">
            <th>Código tienda</th>
            <th>Ruta</th>
            <th>PG</th>
            <th>PP</th>
            <th>TP</th>
            <th>Canal</th>
            <th>Anden</th>
            <th>Vehiculo</th>
            <th>Conductor</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row) => (
            <DispatchesRow
              key={row.id} 
              row={row}
              driversData={driversData}
              vehicleData={vehicleData}
            />
          ))}
        </tbody>
      </table>
      <div className="flex gap-2 ">
        <button
          className="bg-blue-200 p-2 rounded-md hover:bg-blue-300 text-xs"
          onClick={() => setPage(page - 1)}
        >
          Página anterior
        </button>
        <p>
          <b>Página:</b> {page}
        </p>
        <button
          className="bg-blue-200 p-2 rounded-md hover:bg-blue-300 text-xs"
          onClick={() => setPage(page + 1)}
        >
          Página siguiente
        </button>
      </div>
      </>
      )
    }
    </>
  
  );
};

export default Dispatches;
