import { useEffect, useState } from 'react';
import Modal from '../../components/Modal/Modal';
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  Row,
  useReactTable,
} from '@tanstack/react-table';
import { SubmitHandler, useForm } from 'react-hook-form';
import { InternalMovementType } from '../../types/movements';
import { OrdersPallets } from '../../types/dispo';
import {
  filterInternalMovements,
  getInternalMovements,
} from '../../services/Orders';

type FormValues = {
  storeCode: string;
  routeNumber: string;
};

const columnHelper = createColumnHelper<InternalMovementType>();

const InternalMovement = () => {
  const [showModal, setShowModal] = useState<boolean>(false);
  const [data, setData] = useState<InternalMovementType[]>([]);
  const [page, setPage] = useState<number>(1);
  const [currentDispo, setCurrentDispo] = useState<OrdersPallets[]>([]);
  const [currentOrder, setCurrentOrder] = useState<number>(0);
  const [currentChannel, setCurrentChannel] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleDetailClick = (row: Row<InternalMovementType>) => {
    setCurrentDispo(row.getValue('ordersPallets'));
    setCurrentOrder(row.original.id); // Id de la orden
    setCurrentChannel(row.original.channelName); // Id de la orden
    setShowModal(true);
  };

  const columns = [
    columnHelper.accessor('routeName', {
      header: 'id',
      cell: ({ row }) => `${row.getValue('routeName')}`,
    }),
    columnHelper.accessor('storeCode', {
      header: 'Código tienda',
      cell: ({ row }) =>
        `${row.getValue('storeCode')}_${row.original.storeName}`,
    }),
    columnHelper.accessor('channelName', {
      header: 'Canal',
      cell: ({ row }) => row.getValue('channelName') ? row.getValue('channelName') : '-'
    }),
    columnHelper.accessor('bigPallets', {
      header: 'Pallets grandes',
    }),
    columnHelper.accessor('littlePallets', {
      header: 'Pallets pequeños',
    }),
    columnHelper.accessor('totalPallets', {
      header: 'Total Pallets',
      cell: ({ row }) => row.getValue('totalPallets'),
    }),
    columnHelper.accessor('ordersPallets', {
      header: 'Acción',
      cell: ({ row }) => (
        <button
          onClick={() => handleDetailClick(row)}
          className="bg-[#007EF2] text-white px-6 h-7 rounded-lg w-max disabled:bg-[#90A0B7]"
        >
          Detalles
        </button>
      ),
    }),
  ];

  const { register, handleSubmit } = useForm<FormValues>();
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

 const internalMovementGet = async () => {
   setIsLoading(true); 
   try {
     const movements = await getInternalMovements(page);
     console.log("Movimientos internos obtenidos:", movements);
     setData(movements);
   } catch (error) {
     console.error("Error al obtener movimientos internos:", error);
   } finally {
     setIsLoading(false); 
   }
 };

 const changeFilter: SubmitHandler<FormValues> = async (
   formData: FormValues
 ) => {
   setIsLoading(true);
   try {
     const filtered = await filterInternalMovements(
       formData.storeCode || null,
       formData.routeNumber || null,
       page
     );
     setData(filtered);
   } catch (error) {
     console.error("Error al filtrar movimientos internos:", error);
   } finally {
     setIsLoading(false); 
   }
 };

  const handlePagination = (newPageValue: number) => {
    setPage(newPageValue);
    internalMovementGet();
  };

  useEffect(() => {
    internalMovementGet();
  }, []);

  useEffect(() => {
    internalMovementGet();
  }, [showModal]);

  return (
    <>
    <h2 className="text-3xl font-bold">Movimiento interno</h2>
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
            {table.getHeaderGroups().map((group) => (
              <tr key={group.id} className="bg-[#EAEAEA] h-12">
                {group.headers.map((column) => (
                  <th key={column.id} className="font-normal">
                    {flexRender(
                      column.column.columnDef.header,
                      column.getContext()
                    )}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody>
            {table.getRowModel().rows.map((row) => (
              <tr key={row.id} className="bg-white h-12">
                {row.getVisibleCells().map((cell) => (
                  <td key={cell.id}>
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
        <div className="flex gap-2 ">
          <button
            disabled={page === 1}
            className="bg-blue-200 p-2 rounded-md hover:bg-blue-300 text-xs disabled:bg-[#90A0B7] disabled:opacity-50"
            onClick={() => handlePagination(page - 1)}
          >
            Página anterior
          </button>
          <p>
            <b>Página:</b> {page}
          </p>
          <button
            className="bg-blue-200 p-2 rounded-md hover:bg-blue-300 text-xs"
            onClick={() => handlePagination(page + 1)}
          >
            Página siguiente
          </button>
        </div>
        <Modal
          open={showModal}
          disposList={currentDispo}
          setOpen={setShowModal}
          page={page}
          currentOrder={currentOrder}
          currentChannel={currentChannel}
        />
      </>
    )}
  </>
);
}

export default InternalMovement;
