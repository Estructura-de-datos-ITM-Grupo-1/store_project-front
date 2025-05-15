import { postDispatch } from '../../services/Dispatches.service';
import { InternalMovementType } from '../../types/movements';
import React, { useEffect, useState } from 'react';
import { VehicleType } from '../../types/vehicle';
import DispatchesModal from '../../components/Modal/DispatchesModal';

type DispatchesRowProps = {
  row: InternalMovementType;
  vehicleData: VehicleType[];
  driversData: { id: string; name: string }[];
};
type DataPostType = {
  id: number;
  driverId: number;
  vehicleId: number;
  observation: string;
};

const DispatchesRow: React.FC<DispatchesRowProps> = ({
  row,
  vehicleData,
  driversData,
}) => {
  const [selectedVehicleId, setSelectedVehicleId] = useState<number | null>(
    null
  );
  const [selectedDriverId, setSelectedDriverId] = useState<number | null>(null);
  const [dataPost, setDataPost] = useState<DataPostType>({
    id: 0,
    driverId: 0,
    vehicleId: 0,
    observation: '',
  });
  const [openModal, setOpenModal] = useState<boolean>(false);

  const handleVehicleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedVehicleId(parseInt(event.target.value));
  };

  const handleDriverChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedDriverId(parseInt(event.target.value));
  };

  const handleDetailClick = (data: InternalMovementType) => {
    setOpenModal(true);
  };

  const handleSaveClick = async (data: InternalMovementType) => {
    const orderId = data.id; // Assuming the order ID is stored in the "id" field
    const platformId = data.platformId; // Assuming the platformId is stored in the "platformId" field
    const validVehicleId = selectedVehicleId ?? 0; // Ensure the value is not null or undefined
    const validDriverId = selectedDriverId ?? 0; //
    const observations = '-';
    await postDispatch(orderId, validDriverId, validVehicleId, observations , platformId);

    // Add your logic to save these IDs or make API calls
  };

  useEffect(() => {
    setSelectedVehicleId(row?.dispatch?.vehicle?.id ?? null);
    setSelectedDriverId(row?.dispatch?.driver?.id ?? null);
  }, [row]);

  return (
    <>
      <tr className="bg-white">
        <td>
          {row.storeCode}_{row.storeName}
        </td>
        <td>{row.routeName}</td>
        <td>{row.bigPallets}</td>
        <td>{row.littlePallets}</td>
        <td>{row.totalPallets}</td>
        <td>{row.channelName}</td>
        <td>{row.platformName}</td>

        <td>
          <select
            name="vehicle"
            className="bg-white border focus:border-red py-1 px-8 rounded-md text-center"
            onChange={handleVehicleChange}
            value={String(selectedVehicleId)}
          >
            <option value="" defaultChecked>
              Vehiculo
            </option>
            {vehicleData?.map((vehicle: VehicleType) => (
              <option key={vehicle.id} value={vehicle.id}>
                {vehicle.plate}
              </option>
            ))}
          </select>
        </td>
        <td>
          <select
            name="driver"
            className="bg-white border focus:border-red py-1 px-2 rounded-md text-center "
            onChange={handleDriverChange}
            value={String(selectedDriverId)}
          >
            <option value="" defaultChecked>
              Conductor
            </option>
            {driversData?.map((driver) => (
              <option key={driver.id} value={driver.id}>
                {driver.name}
              </option>
            ))}
          </select>
        </td>
        <td>
          <>
            <button
              onClick={() => handleSaveClick(row)}
              className="bg-[#007EF2] text-white px-6 h-7 rounded-lg w-max disabled:bg-[#90A0B7] mt-4"
            >
              Guardar
            </button>
            <button
              onClick={() => handleDetailClick(row)}
              className="text-[#007EF2] px-6 h-7 rounded-lg w-max disabled:bg-[#90A0B7] mt-4"
            >
              Ver detalle
            </button>
          </>
        </td>
      </tr>
      <DispatchesModal
        open={openModal}
        setOpen={setOpenModal}
        id={row.id}
        driverId={selectedDriverId}
        vehicleId={selectedVehicleId}
        platformId={row.platformId}
      />
    </>
  );
};

export default DispatchesRow;
