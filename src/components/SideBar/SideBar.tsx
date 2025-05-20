import CheckCircleIcon from '../Icons/CheckCircleIcon';
import DocumentUploadIcon from '../Icons/DocumentUpIcon';
import EyeIcon from '../Icons/EyeIcon';
import MapInIcon from '../Icons/MapInIcon';
import TruckIcon from '../Icons/TruckIcon';
import UserCircle from '../Icons/UserCircle';
import SideberItem from './SideBarItem';

const Sidebar = () => {
  return (
    <aside className="hidden sm:block md:w-auto bg-white h-screen fixed top-0 left-0 pt-16">
      <nav className="text-left px-4 flex flex-col gap-2 py-4">
        <SideberItem
          routePath="/dashboard/clients"
          label="Clientes"
          icon={<EyeIcon />}
        />
        <SideberItem
          routePath="/dashboard/cash-balancing"
          label="Cuadre de Caja"
          icon={<CheckCircleIcon />}
        />
        <SideberItem
          routePath="/dashboard/config-module"
          label="Configuración del módulo"
          icon={<DocumentUploadIcon />}
        />
        <SideberItem
          routePath="/dashboard/inventory"
          label="Inventario"
          icon={<MapInIcon />}
        />
        <SideberItem
          routePath="/dashboard/reports"
          label="Reportes"
          icon={<TruckIcon />}
        />
        <SideberItem
          routePath="/dashboard/services"
          label="Servicios de la compañia"
          icon={<EyeIcon />}
        />
        <SideberItem
          routePath="/dashboard/tax"
          label="Facturación"
          icon={<UserCircle />}
        />
      </nav>
    </aside>
  );
};

export default Sidebar;
