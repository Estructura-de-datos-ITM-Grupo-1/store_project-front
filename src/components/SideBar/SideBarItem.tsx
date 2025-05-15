import React from 'react';
import { Link } from 'react-router-dom';

type SidebarItemProps = {
  routePath: string;
  label: string;
  icon?: React.ReactElement;
};

const SideberItem: React.FC<SidebarItemProps> = ({ routePath, label, icon }) => {
  return (
    <Link
      className="text-[#334D6E] p-2 hover:bg-gray-200 rounded flex items-center gap-1 relative"
      to={routePath}
    >
      <div className="group flex items-center relative">
        {icon}

        <div
          id="tooltip-default"
          role="tooltip"
          className="group-hover:opacity-100 group-hover:visible absolute z-10 invisible inline-block px-3 py-2 text-sm font-medium text-white transition-opacity duration-300 bg-[#007EF2] rounded-lg shadow-sm opacity-0 tooltip w-max left-full ml-4"
        >
          {label}
        </div>
      </div>
    </Link>
  );
};

export default SideberItem;
