import { SubmitHandler, useForm } from 'react-hook-form';
import { loginUser } from '../../services/User';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';
import axios from 'axios';

type FormValues = {
  user: string;
  password: string;
};

const Login = () => {
  const {
    register,
    handleSubmit,
    formState: { isValid },
  } = useForm<FormValues>();

  const navigate = useNavigate();

  const login: SubmitHandler<FormValues> = async (data) => {
    
    const response = await loginUser(data);
    console.warn(response);
    if (response) {

      localStorage.setItem('token', response.token);
      axios.defaults.headers.common['Authorization'] = response.token;
      navigate('/dashboard/lectura');
    } else {
      toast.error('El usuario o contraseña no son correctos');
    }
   
  };

  return (
    <main className="flex flex-col h-screen place-content-center justify-center items-center">
      <span className='text-xl font-semibold'>STORE - PROJECT - FT</span>
      <form
        onSubmit={handleSubmit(login)}
        className="w-full md:w-1/3 p-4 rounded bg-white shadow-md flex flex-col gap-5"
      >
        <h2 className="mb-6 text-3xl font-bold">Login</h2>
        <div className="w-full text-left">
          <label htmlFor="" className="text-sm font-medium">
            Usuario
          </label>
          <input
            {...register('user', { required: true })}
            className="bg-white border focus:border-red py-1 px-2 rounded-md text-left w-full mt-2"
            type="text"
            placeholder="Usuario"
          />
        </div>
        <div className="w-full text-left">
          <label htmlFor="" className="text-sm font-medium">
            Contraseña
          </label>
          <input
            {...register('password', { required: true })}
            className="bg-white border focus:border-red py-1 px-2 rounded-md text-left w-full mt-2"
            type="password"
            placeholder="Contraseña"
          />
        </div>
        <div>
          <button
            disabled={!isValid}
            className="bg-[#007EF2] text-white px-6 h-7 rounded-lg w-max disabled:bg-[#90A0B7]"
          >
            Entrar
          </button>
        </div>
      </form>
    </main>
  );
};

export default Login;
