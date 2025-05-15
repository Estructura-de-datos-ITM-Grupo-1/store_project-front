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
          routePath="/dashboard/lectura"
          label="Lectura"
          icon={<EyeIcon />}
        />
        <SideberItem
          routePath="/dashboard/productos-escaneados"
          label="Últmos escaneados"
          icon={<CheckCircleIcon />}
        />
        <SideberItem
          routePath="/dashboard/orden-producto"
          label="OP"
          icon={<DocumentUploadIcon />}
        />
        <SideberItem
          routePath="/dashboard/movimiento-interno"
          label="Movimiento interno"
          icon={<MapInIcon />}
        />
        <SideberItem
          routePath="/dashboard/despachos"
          label="Despacho"
          icon={<TruckIcon />}
        />
        <SideberItem
          routePath="/dashboard/scanner"
          label="Escanear"
          icon={<EyeIcon />}
        />
        <SideberItem
          routePath="/conductores"
          label="Conductores"
          icon={<UserCircle />}
        />
      </nav>
    </aside>
  );
};

export default Sidebar;
