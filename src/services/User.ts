import axios from "axios";

export const loginUser = async (loginData: {
  user: string;
  password: string;
}) => {

  try {
    console.log(loginData);
    const response = await axios.post(
      `https://api.service.tutti.addiis.co/auth/login`,
      {
        user: loginData.user,
        password: loginData.password,
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    return response.data;
  } catch (error) {
    console.log(error);
  }
};
