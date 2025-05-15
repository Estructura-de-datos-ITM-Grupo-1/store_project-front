import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from '@tanstack/react-table';

import { useEffect, useState } from 'react';
import { DriverType } from '../../types/driver';
import { getAllDispatchs } from '../../services/Dispatches.service';

const columnHelper = createColumnHelper<DriverType>();

const Drivers = () => {

  const [data, setData] = useState<DriverType[]>([]);
  const [page, setPage] = useState<number>(1);
  

  const columns = [
    columnHelper.accessor('driver.name', {
      header: 'Conductor',
    }),
    columnHelper.accessor('vehicle.plate', {
      header: 'N° Placa',
     
    }),
    columnHelper.accessor('observation', {
      header: 'Observaciones',
      cell: ({ row }) => row.getValue('observation'),
    }),
    columnHelper.accessor('orderStore.routeName', {
      header: 'Ruta',
    }),
    columnHelper.accessor('orderStore.bigPallets', {
      header: 'PG',
    }),
    columnHelper.accessor('orderStore.littlePallets', {
      header: 'PP',
    }),
    columnHelper.accessor('orderStore.totalPallets', {
      header: 'TP',
    }),
    columnHelper.accessor('orderStore.platformName', {
      header: 'Anden',
    }),
    columnHelper.accessor('orderStore.channelName', {
      header: 'Canal',
    }),
  ];

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });
const getDispatchs = async () => {
  const date = new Date().toISOString().split('T')[0];
  const dispatchs = await getAllDispatchs(date, page);
  setData(dispatchs);
};

useEffect(() => {
  getDispatchs();

}, [page]);

useEffect(() => {
  getDispatchs();
}, []);
  return (
    <main className="px-6">
      <h2 className="text-3xl font-bold my-6">Conductores</h2>
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
          className="bg-blue-200 p-2 rounded-md hover:bg-blue-300 text-xs"
          onClick={() => setPage(page - 1)}
        >
          Página anterior
        </button>
        <button
          className="bg-blue-200 p-2 rounded-md hover:bg-blue-300 text-xs"
          onClick={() => setPage(page + 1)}
        >
          Página siguiente
        </button>
      </div>
    </main>
  );
};

export default Drivers;
