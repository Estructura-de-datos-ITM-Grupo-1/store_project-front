import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from '@tanstack/react-table';
import { ScannedProduct } from '../../types/products';
import { useEffect, useState } from 'react';
import { getLastScannedProducts } from '../../services/Productos';

const LatestScannedProducts = () => {
  const [data, setData] = useState<ScannedProduct[]>([]);

  const getData = async () => {
    const list = await getLastScannedProducts();
    console.log(list);
    
    setData(list);
  };

  useEffect(() => {
    getData();
  }, []);

  const columnHelper = createColumnHelper<ScannedProduct>();
  const columns = [
    columnHelper.accessor('sku', {
      header: 'SKU',
    }),
    columnHelper.accessor('descriptionProduct', {
      header: 'Descripción',
    }),
    columnHelper.accessor('manufactureDate', {
      header: 'Fecha De elaboración',
    }),
    columnHelper.accessor('expirationDate', {
      header: 'Fecha De Vencimiento',
    }),
    columnHelper.accessor('usefulLife', {
      header: 'Vida útil',
    }),
    columnHelper.accessor('amountReceived', {
      header: 'Cantidad Recibida',
    }),
    columnHelper.accessor('lot', {
      header: 'Lote',
    }),
    columnHelper.accessor('receptionPercentage', {
      header: 'Porcentaje de Recepción',
    }),
    columnHelper.accessor('malfunctions', {
      header: 'Averias',
         cell: ({ row }) => row.getValue('malfunctions'),
    }),
    columnHelper.accessor('observations', {
      header: 'Observaciones',
    }),
  ];
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <>
      <h2 className="text-3xl font-bold">Últimos Productos Escaneados</h2>
      <div className="overflow-x-auto">
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
      </div>
    </>
  );
};

export default LatestScannedProducts;
