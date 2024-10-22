import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Login from "./components/Login";
import Register from "./components/Register";
import Main from "./components/Main";
import Header from "./components/Header";
import Footer from "./components/Footer";
import { Box, CssBaseline } from "@mui/material";
import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <Router>
      <CssBaseline />
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          minHeight: '100vh',
        }}
      >
        <Header />
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            p: 2,
          }}
        >
          <Routes>
            <Route path='/login' element={<Login />} />
            <Route path='/register' element={<Register />} />
            <Route 
              path='/' 
              element={
                <ProtectedRoute>
                  <Main />
                </ProtectedRoute>
              } 
            />
          </Routes>
        </Box>
        <Footer />
        <ToastContainer
          position="top-right"
          autoClose={5000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
      />
      </Box>
    </Router>
  );
}

export default App;
