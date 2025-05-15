import { useNavigate } from 'react-router-dom';
import LogoutIcon from '../Icons/LogoutIcon';

const Topbar = () => {
  const navigate = useNavigate();
  const logout = () => {
    localStorage.removeItem('token');
    navigate('/');
  };

  return (
    <div className="h-16 bg-white w-full fixed flex justify-between items-center p-4 font-semibold">
      <h1 className="flex gap-2 items-center justify-center">
        
        STORE - PROJECT - FT
      </h1>
      <div>
        <button
          className="font-normal text-[#007EF2] flex items-center gap-1"
          onClick={logout}
        >
          <LogoutIcon />
          Salir
        </button>
      </div>
    </div>
  );
};

export default Topbar;
