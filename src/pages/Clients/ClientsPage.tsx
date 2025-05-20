import { useEffect, useState } from "react";
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import { SubmitHandler, useForm } from "react-hook-form";

// Tipo de cliente
type Client = {
  id: number;
  name: string;
  email: string;
  phone: string;
};

// Filtros permitidos
type FormValues = {
  name: string;
  email: string;
};

// Servicios ficticios (reemplaza con tus llamadas reales a la API)
const getClients = async (page: number): Promise<Client[]> => {
  // Simulación de llamada a API
  return [
    {
      id: 1,
      name: "Juan Pérez",
      email: "juan@example.com",
      phone: "123456789",
    },
    { id: 2, name: "Ana García", email: "ana@example.com", phone: "987654321" },
  ];
};

const filterClients = async (
  name: string | null,
  email: string | null,
  page: number
): Promise<Client[]> => {
  // Simulación de llamada a API con filtros
  return getClients(page); // Reemplaza con lógica filtrada real
};

const columnHelper = createColumnHelper<Client>();

const ClientsPage = () => {
  const [data, setData] = useState<Client[]>([]);
  const [page, setPage] = useState<number>(1);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const columns = [
    columnHelper.accessor("id", {
      header: "ID",
      cell: ({ row }) => row.getValue("id"),
    }),
    columnHelper.accessor("name", {
      header: "Nombre",
      cell: ({ row }) => row.getValue("name"),
    }),
    columnHelper.accessor("email", {
      header: "Email",
      cell: ({ row }) => row.getValue("email"),
    }),
    columnHelper.accessor("phone", {
      header: "Teléfono",
      cell: ({ row }) => row.getValue("phone"),
    }),
  ];

  const { register, handleSubmit } = useForm<FormValues>();

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  const loadClients = async () => {
    setIsLoading(true);
    try {
      const result = await getClients(page);
      setData(result);
    } catch (error) {
      console.error("Error al obtener clientes:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const applyFilter: SubmitHandler<FormValues> = async (formData) => {
    setIsLoading(true);
    try {
      const filtered = await filterClients(
        formData.name || null,
        formData.email || null,
        page
      );
      setData(filtered);
    } catch (error) {
      console.error("Error al filtrar clientes:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handlePagination = (newPage: number) => {
    setPage(newPage);
  };

  useEffect(() => {
    loadClients();
  }, [page]);

  return (
    <>
      <h2 className="text-3xl font-bold">Gestión de Clientes</h2>
      <div className="my-6">
        <h3 className="text-left text-2xl">Filtrar</h3>
        <form
          onSubmit={handleSubmit(applyFilter)}
          className="flex gap-2 items-center"
        >
          <input
            type="text"
            {...register("name")}
            placeholder="Nombre"
            className="bg-white border focus:border-red py-1 px-2 rounded-md text-center"
          />
          <input
            type="email"
            {...register("email")}
            placeholder="Correo"
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
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext()
                      )}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>

          <div className="flex gap-2 mt-4">
            <button
              disabled={page === 1}
              className="bg-blue-200 p-2 rounded-md hover:bg-blue-300 text-xs disabled:bg-[#90A0B7]"
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
        </>
      )}
    </>
  );
};

export default ClientsPage;
