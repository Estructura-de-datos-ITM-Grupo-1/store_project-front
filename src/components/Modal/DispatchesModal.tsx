import {
  Dialog,
  DialogBackdrop,
  DialogPanel,
  DialogTitle,
} from '@headlessui/react';
import { ChangeEventHandler, useState } from 'react';
import { postDispatch, updateDispatchObservation } from '../../services/Dispatches.service';

type DispatchesModalProps = {
  open: boolean;
  setOpen: React.Dispatch<React.SetStateAction<boolean>>;
  id: number;
  driverId?: number | null;
  vehicleId?: number  | null;
  platformId?: number | null;

};

const DispatchesModal: React.FC<DispatchesModalProps> = ({
  open,
  setOpen,
  id,
  driverId,
  vehicleId,
  platformId,

}) => {
  const [observations, setObservations] = useState<string>('');

  const handleSaveDetail = async () => {
    await postDispatch(id, driverId, vehicleId, observations, platformId);
    setOpen(false);
  };

  const handleChangeObservation: ChangeEventHandler<HTMLTextAreaElement> = (
    event
  ) => {
    setObservations(event.target.value);
  };

  return (
    <Dialog
      open={open}
      onClose={() => setOpen(!open)}
      className="relative z-10"
    >
      <DialogBackdrop
        transition
        className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity data-[closed]:opacity-0 data-[enter]:duration-300 data-[leave]:duration-200 data-[enter]:ease-out data-[leave]:ease-in"
      />
      <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
        <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
          <DialogPanel
            transition
            className="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all data-[closed]:translate-y-4 data-[closed]:opacity-0 data-[enter]:duration-300 data-[leave]:duration-200 data-[enter]:ease-out data-[leave]:ease-in sm:my-8 sm:w-auto  data-[closed]:sm:translate-y-0 data-[closed]:sm:scale-95"
          >
            <div className="bg-white px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
              <div className="sm:flex sm:items-start w-full">
                <div className="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left w-full">
                  <DialogTitle
                    as="h3"
                    className="text-base font-semibold leading-6 text-gray-900"
                  >
                    Detalle despacho
                  </DialogTitle>
                  <div className="mt-2 w-full">
                    <textarea
                      onChange={handleChangeObservation}
                      name=""
                      id=""
                      className="bg-white border"
                      placeholder="Ingresa descripción"
                    ></textarea>
                  </div>
                </div>
              </div>
            </div>
            <div className="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
              <button
                onClick={handleSaveDetail}
                className="bg-[#007EF2] text-white px-6 h-7 rounded-lg w-max disabled:bg-[#90A0B7] mt-4"
              >
                Guardar
              </button>
              <button
                onClick={() => setOpen(false)}
                className="text-[#007EF2] px-6 h-7 rounded-lg w-max disabled:bg-[#90A0B7] mt-4"
              >
                Cancelar
              </button>
            </div>
          </DialogPanel>
        </div>
      </div>
    </Dialog>
  );
};
export default DispatchesModal;
