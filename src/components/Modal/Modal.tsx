import {
  Dialog,
  DialogBackdrop,
  DialogPanel,
  DialogTitle,
} from '@headlessui/react';
import { OrdersPallets } from '../../types/dispo';
import DispoRow from './DispoRow';
import { useEffect, useState } from 'react';
import { getInternalMovements, updateDispos } from '../../services/Orders';

type ModalProps = {
  open: boolean;
  setOpen: React.Dispatch<React.SetStateAction<boolean>>;
  disposList: OrdersPallets[];
  page: number;
  currentOrder: number;
  currentChannel: string;
};

const Modal: React.FC<ModalProps> = ({
  open,
  setOpen,
  disposList,
  page,
  currentOrder,
  currentChannel,
}) => {
  const [list, setList] = useState<OrdersPallets[]>([]);

  useEffect(() => {
    setList(disposList);
  }, [disposList]);

  const handleSave = async () => {
    setOpen(false);
    console.log(list)
    await updateDispos(currentOrder, list, currentChannel);
  //  await  window.location.reload();

  };

  const handleChangeDispo = (index: number, value: OrdersPallets) => {
    const newList = [...list];
    newList[index] = value;
    setList(newList);
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
                    Pallets
                  </DialogTitle>
                  <div className="mt-2 w-full">
                    <table className="w-full">
                      <thead className="bg-[#EAEAEA] h-12 text-center">
                        <tr>
                          <th>Dispo</th>
                          <th>Pallets Grandes</th>
                          <th>Pallets Pequeños</th>
                        </tr>
                      </thead>
                      <tbody className="text-center">
                        {disposList.map(
                          (dispo: OrdersPallets, index: number) => (
                            <DispoRow
                              key={index}
                              index={index}
                              initialValues={dispo}
                              page={page}
                              currentOrder={currentOrder}
                              handleChangeDispo={handleChangeDispo}
                            />
                          )
                        )}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
            <div className="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
              <button
                onClick={() => handleSave()}
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

export default Modal;
