const AppConfig = {
  site_name: "Fvsion",
  title: "Fvsion - Your entrypoint to stable diffusion",
  description: "Your entrypoint to stable diffusion",
  locale: "en",
};

export default AppConfig;

export const config = {
  baseUrl: import.meta.env.VITE_BASE_URL,
};

// export const configDev = {
//   baseUrl: import.meta.env.VITE_BASE_URL_DEV,
// };

// Page Routes
export const ROUTE_HOME = "/";

// Default payload/responses
export const RESP_USER_GUEST = {
  guest: true,
};
